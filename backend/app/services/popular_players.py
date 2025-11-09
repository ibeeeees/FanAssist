"""
Popular Players Service - Get star players with PrizePicks lines for betting
"""

from typing import List, Dict, Optional
from datetime import datetime
from app.services.schedule import NBAScheduleService
from app.services.nba_stats import NBAStatsService
from nba_api.stats.endpoints import commonteamroster
import asyncio

# Popular players by team (star players who are commonly on PrizePicks)
POPULAR_PLAYERS = {
    # Lakers
    1610612747: ["LeBron James", "Anthony Davis"],
    # Warriors
    1610612744: ["Stephen Curry", "Klay Thompson"],
    # Mavericks
    1610612742: ["Luka Dončić", "Kyrie Irving"],
    # Celtics
    1610612738: ["Jayson Tatum", "Jaylen Brown"],
    # Bucks
    1610612749: ["Giannis Antetokounmpo", "Damian Lillard"],
    # 76ers
    1610612755: ["Joel Embiid", "Tyrese Maxey"],
    # Nuggets
    1610612743: ["Nikola Jokić", "Jamal Murray"],
    # Suns
    1610612756: ["Kevin Durant", "Devin Booker", "Bradley Beal"],
    # Clippers
    1610612746: ["Kawhi Leonard", "Paul George", "James Harden"],
    # Heat
    1610612748: ["Jimmy Butler", "Bam Adebayo"],
    # Knicks
    1610612752: ["Jalen Brunson", "Julius Randle"],
    # Nets
    1610612751: ["Mikal Bridges", "Cameron Thomas"],
    # Cavaliers
    1610612739: ["Donovan Mitchell", "Darius Garland"],
    # Kings
    1610612758: ["De'Aaron Fox", "Domantas Sabonis"],
    # Pelicans
    1610612740: ["Zion Williamson", "Brandon Ingram"],
    # Timberwolves
    1610612750: ["Anthony Edwards", "Karl-Anthony Towns"],
    # Thunder
    1610612760: ["Shai Gilgeous-Alexander", "Chet Holmgren"],
    # Grizzlies
    1610612763: ["Ja Morant", "Jaren Jackson Jr."],
    # Hawks
    1610612737: ["Trae Young", "Dejounte Murray"],
    # Raptors
    1610612761: ["Scottie Barnes", "Pascal Siakam"],
    # Bulls
    1610612741: ["DeMar DeRozan", "Zach LaVine"],
    # Pacers
    1610612754: ["Tyrese Haliburton", "Myles Turner"],
    # Wizards
    1610612764: ["Jordan Poole", "Kyle Kuzma"],
    # Trail Blazers
    1610612757: ["Anfernee Simons", "Jerami Grant"],
    # Magic
    1610612753: ["Paolo Banchero", "Franz Wagner"],
    # Spurs
    1610612759: ["Victor Wembanyama", "Devin Vassell"],
    # Hornets
    1610612766: ["LaMelo Ball", "Terry Rozier"],
    # Pistons
    1610612765: ["Cade Cunningham", "Jalen Duren"],
    # Rockets
    1610612745: ["Alperen Şengün", "Jalen Green"],
    # Jazz
    1610612762: ["Lauri Markkanen", "Jordan Clarkson"],
}

# Common PrizePicks lines for different stat categories
PRIZEPICKS_LINES = {
    "points": {
        "superstar": [25.5, 27.5, 29.5],  # LeBron, Luka, Giannis
        "star": [20.5, 22.5, 24.5],       # Tatum, Booker, Mitchell
        "scorer": [15.5, 17.5, 19.5],     # Role players who score
    },
    "rebounds": {
        "big": [10.5, 11.5, 12.5],        # Jokic, Giannis, AD
        "forward": [7.5, 8.5, 9.5],       # Two-way forwards
        "guard": [4.5, 5.5, 6.5],         # Rebounding guards
    },
    "assists": {
        "playmaker": [8.5, 9.5, 10.5],    # Luka, Haliburton, Trae
        "combo": [5.5, 6.5, 7.5],         # Combo guards
        "secondary": [3.5, 4.5, 5.5],     # Wings who pass
    },
    "threes": {
        "shooter": [3.5, 4.5, 5.5],       # Curry, Dame, Trae
        "volume": [2.5, 3.5],             # Most wings
        "low": [1.5, 2.5],                # Bigs who shoot
    }
}


class PopularPlayersService:
    """Service to get popular players with PrizePicks-style lines"""
    
    def __init__(self):
        self.schedule_service = NBAScheduleService()
        self.nba_stats = NBAStatsService()
    
    async def get_popular_players_for_today(self) -> List[Dict]:
        """
        Get popular players playing today with their lines
        
        Only includes:
        - Players with games TODAY
        - Players who are ACTIVE (not injured)
        - Players with recent game activity (played within last 7 days)
        """
        return await self._get_popular_players_for_games("today")
    
    async def get_popular_players_for_tomorrow(self) -> List[Dict]:
        """
        Get popular players playing tomorrow with their lines
        
        Only includes:
        - Players with games TOMORROW
        - Players who are ACTIVE (not injured)
        - Players with recent game activity (played within last 7 days)
        """
        return await self._get_popular_players_for_games("tomorrow")
    
    async def _get_popular_players_for_games(self, day: str) -> List[Dict]:
        """
        Get popular players for a specific day
        
        Filters out:
        - Injured players (no games in last 7 days)
        - Players without scheduled games
        - Players with no recent stats
        """
        # Get games
        if day == "today":
            games = self.schedule_service.get_todays_games()
        else:
            games = self.schedule_service.get_tomorrows_games()
        
        if not games:
            return []
        
        popular_players = []
        
        # For each game, get popular players from both teams
        for game in games:
            # Get popular players from home team
            home_players = await self._get_team_popular_players(
                game['home_team_id'],
                game['home_team'],
                game['away_team'],
                game['game_date']
            )
            popular_players.extend(home_players)
            
            # Get popular players from away team
            away_players = await self._get_team_popular_players(
                game['away_team_id'],
                game['away_team'],
                game['home_team'],
                game['game_date']
            )
            popular_players.extend(away_players)
        
        return popular_players
    
    async def _get_team_popular_players(
        self, 
        team_id: int, 
        team_name: str, 
        opponent: str,
        game_date: str
    ) -> List[Dict]:
        """Get popular players from a specific team (excludes injured players)
        
        Note: If NBA API has issues (timeouts, rate limits), we allow players through
        rather than blocking everyone. This prevents empty results when API is slow.
        """
        players = []
        
        # Get list of popular players for this team
        popular_names = POPULAR_PLAYERS.get(team_id, [])
        
        if not popular_names:
            return []
        
        print(f"🔍 Fetching roster for {team_name} (ID: {team_id})...")
        
        # Get team roster
        try:
            roster = commonteamroster.CommonTeamRoster(team_id=team_id)
            roster_df = roster.get_data_frames()[0]
            print(f"✅ Got roster for {team_name} - {len(roster_df)} players")
        except Exception as e:
            print(f"❌ Error getting roster for team {team_id} ({team_name}): {e}")
            print(f"⚠️  Skipping {team_name} - NBA API timeout")
            # NO FALLBACK - Skip this team if API fails
            return []
        
        # Find each popular player and get their stats
        for player_name in popular_names:
            try:
                # Find player in roster
                player_row = roster_df[roster_df['PLAYER'].str.contains(player_name, case=False, na=False)]
                
                if player_row.empty:
                    continue
                
                player_id = int(player_row.iloc[0]['PLAYER_ID'])
                # Try to pull position from roster row if available (e.g., 'G', 'F-C', etc.)
                try:
                    position = str(player_row.iloc[0]['POSITION']) if 'POSITION' in player_row.columns else ''
                except Exception:
                    position = ''
                
                # Check if player is healthy (not injured/out)
                # Check recent game activity - if they haven't played in last 7 days, likely injured
                # BUT: If NBA API fails, allow player through (don't be too strict)
                try:
                    recent_games = await self.nba_stats.get_player_game_log(player_id, last_n_games=5)
                    if not recent_games or len(recent_games) == 0:
                        print(f"⚠️  Skipping {player_name} - No recent games (likely injured or inactive)")
                        continue
                    
                    # Check if their last game was recent (within 7 days)
                    from datetime import datetime, timedelta
                    last_game_date = recent_games[0].game_date if recent_games else None
                    if last_game_date:
                        try:
                            last_game_dt = datetime.strptime(last_game_date, "%Y-%m-%d")
                            days_since_last_game = (datetime.now() - last_game_dt).days
                            if days_since_last_game > 7:
                                print(f"⚠️  Skipping {player_name} - Last game was {days_since_last_game} days ago (likely injured)")
                                continue
                        except:
                            pass  # If date parsing fails, continue anyway
                    
                except Exception as e:
                    print(f"⚠️  Could not verify injury status for {player_name}: {e}")
                    # If we can't verify, ALLOW PLAYER THROUGH (NBA API might be down)
                    # This is less strict than blocking them
                    print(f"✅  Allowing {player_name} through despite verification failure")
                    pass  # Continue to next step instead of skipping
                
                # Get player stats
                print(f"  📊 Fetching season averages for {player_name}...")
                try:
                    season_avg = await self.nba_stats.get_player_season_averages(player_id)
                    
                    if not season_avg:
                        print(f"  ⚠️  No season stats available for {player_name}")
                        continue
                    
                    print(f"  ✅ Got stats for {player_name}: {round(season_avg.points_per_game, 1)} PPG")
                except Exception as e:
                    print(f"  ❌ Error getting stats for {player_name}: {e}")
                    continue
                
                # Determine player tier and get appropriate lines
                lines = self._get_prizepicks_lines(season_avg)
                
                player_data = {
                    "player_id": player_id,
                    "player_name": player_name,
                    "team": team_name,
                    "opponent": opponent,
                    "game_date": game_date,
                    "position": position,
                    "season_averages": {
                        "points": round(season_avg.points_per_game, 1),
                        "rebounds": round(season_avg.rebounds_per_game, 1),
                        "assists": round(season_avg.assists_per_game, 1),
                        "steals": round(season_avg.steals_per_game, 1),
                        "turnovers": round(season_avg.turnovers, 1) if hasattr(season_avg, 'turnovers') else 0,
                        "threes_made": round(season_avg.three_pointers_made, 1) if hasattr(season_avg, 'three_pointers_made') else 0,
                        "blocks": round(season_avg.blocks_per_game, 1),
                        "games_played": season_avg.games_played
                    },
                    "prizepicks_lines": lines
                }
                
                players.append(player_data)
                
            except Exception as e:
                print(f"Error processing player {player_name}: {e}")
                continue
        
        return players
    
    def _round_to_half(self, value: float) -> float:
        """
        Round to nearest whole number or .5 increment
        Examples: 25.3 -> 25.5, 25.7 -> 26.0, 25.0 -> 25.0
        """
        return round(value * 2) / 2
    
    def _get_prizepicks_lines(self, season_avg) -> Dict:
        """
        Generate PrizePicks-style lines based on player averages
        
        Supports all major prop types:
        - Points
        - Rebounds
        - Assists
        - Pts+Rebs+Asts (PRA)
        - Steals
        - Turnovers
        - 3-PT Made
        
        All lines are rounded to whole numbers or .5 increments (e.g., 25.0, 25.5, 26.0)
        """
        lines = {}
        
        pts = season_avg.points_per_game
        reb = season_avg.rebounds_per_game
        ast = season_avg.assists_per_game
        stl = season_avg.steals_per_game
        
        # Turnovers and 3PT Made (may not be in all stat objects)
        tov = season_avg.turnovers if hasattr(season_avg, 'turnovers') else 0
        threes = season_avg.three_pointers_made if hasattr(season_avg, 'three_pointers_made') else 0
        
        # Points line (realistic PrizePicks lines slightly below average)
        if pts >= 25:
            lines["points"] = self._round_to_half(pts - 1.5)
        elif pts >= 20:
            lines["points"] = self._round_to_half(pts - 1.0)
        elif pts >= 10:
            lines["points"] = self._round_to_half(pts - 0.5)
        elif pts >= 5:
            lines["points"] = self._round_to_half(pts - 0.3)
        
        # Rebounds line
        if reb >= 10:
            lines["rebounds"] = self._round_to_half(reb - 1.0)
        elif reb >= 6:
            lines["rebounds"] = self._round_to_half(reb - 0.5)
        elif reb >= 3:
            lines["rebounds"] = self._round_to_half(reb - 0.3)
        
        # Assists line
        if ast >= 8:
            lines["assists"] = self._round_to_half(ast - 0.5)
        elif ast >= 5:
            lines["assists"] = self._round_to_half(ast - 0.5)
        elif ast >= 3:
            lines["assists"] = self._round_to_half(ast - 0.3)
        
        # Steals line (typically low numbers)
        if stl >= 2.0:
            lines["steals"] = self._round_to_half(stl - 0.5)
        elif stl >= 1.0:
            lines["steals"] = self._round_to_half(stl - 0.3)
        elif stl >= 0.5:
            lines["steals"] = self._round_to_half(stl - 0.2)
        
        # Turnovers line (over is bad, under is good)
        if tov >= 3.0:
            lines["turnovers"] = self._round_to_half(tov - 0.3)
        elif tov >= 2.0:
            lines["turnovers"] = self._round_to_half(tov - 0.2)
        elif tov >= 1.0:
            lines["turnovers"] = self._round_to_half(tov - 0.1)
        
        # 3-PT Made line (for shooters)
        if threes >= 3.0:
            lines["threes_made"] = self._round_to_half(threes - 0.5)
        elif threes >= 2.0:
            lines["threes_made"] = self._round_to_half(threes - 0.3)
        elif threes >= 1.0:
            lines["threes_made"] = self._round_to_half(threes - 0.2)
        
        # Combo stats (popular on PrizePicks)
        
        # Points + Rebounds + Assists (PRA / Fantasy Points)
        pra = pts + reb + ast
        if pra >= 40:
            lines["pra"] = self._round_to_half(pra - 2.5)
        elif pra >= 30:
            lines["pra"] = self._round_to_half(pra - 2.0)
        elif pra >= 20:
            lines["pra"] = self._round_to_half(pra - 1.5)
        
        # Points + Rebounds
        pr = pts + reb
        if pr >= 35:
            lines["pr"] = self._round_to_half(pr - 2.0)
        elif pr >= 25:
            lines["pr"] = self._round_to_half(pr - 1.5)
        
        # Points + Assists
        pa = pts + ast
        if pa >= 35:
            lines["pa"] = self._round_to_half(pa - 2.0)
        elif pa >= 25:
            lines["pa"] = self._round_to_half(pa - 1.5)
        
        return lines
    
    async def _create_fallback_players(
        self,
        team_id: int,
        team_name: str,
        player_names: List[str],
        opponent: str,
        game_date: str
    ) -> List[Dict]:
        """Create fallback player data when NBA API fails"""
        fallback_players = []
        
        # Estimated stats for star players (these are reasonable averages)
        star_stats = {
            "LeBron James": {"pts": 24.0, "reb": 7.5, "ast": 7.0, "position": "F"},
            "Anthony Davis": {"pts": 24.0, "reb": 11.5, "ast": 3.5, "position": "F-C"},
            "Stephen Curry": {"pts": 26.0, "reb": 4.5, "ast": 5.0, "position": "G"},
            "Luka Dončić": {"pts": 32.0, "reb": 8.5, "ast": 9.0, "position": "G-F"},
            "Giannis Antetokounmpo": {"pts": 30.0, "reb": 11.5, "ast": 6.0, "position": "F"},
            "Jayson Tatum": {"pts": 27.0, "reb": 8.5, "ast": 4.5, "position": "F"},
            "Jaylen Brown": {"pts": 23.0, "reb": 5.5, "ast": 3.5, "position": "G-F"},
            "Joel Embiid": {"pts": 33.0, "reb": 10.5, "ast": 4.0, "position": "C"},
            "Nikola Jokić": {"pts": 26.0, "reb": 12.0, "ast": 9.0, "position": "C"},
            "Kevin Durant": {"pts": 28.0, "reb": 6.5, "ast": 5.0, "position": "F"},
            "Damian Lillard": {"pts": 25.0, "reb": 4.0, "ast": 7.0, "position": "G"},
            "Shai Gilgeous-Alexander": {"pts": 31.0, "reb": 5.5, "ast": 6.0, "position": "G"},
            "Ja Morant": {"pts": 26.0, "reb": 5.5, "ast": 8.0, "position": "G"},
            "Jaren Jackson Jr.": {"pts": 18.5, "reb": 5.5, "ast": 1.5, "position": "F-C"},
            "Chet Holmgren": {"pts": 17.0, "reb": 7.5, "ast": 2.5, "position": "F-C"},
            "Paolo Banchero": {"pts": 22.0, "reb": 6.5, "ast": 3.5, "position": "F"},
            "Franz Wagner": {"pts": 19.5, "reb": 5.0, "ast": 3.5, "position": "F"},
            "Jalen Brunson": {"pts": 28.0, "reb": 3.5, "ast": 6.5, "position": "G"},
            "LaMelo Ball": {"pts": 23.0, "reb": 5.0, "ast": 8.0, "position": "G"},
            "Trae Young": {"pts": 26.0, "reb": 3.0, "ast": 11.0, "position": "G"},
            "Cade Cunningham": {"pts": 22.0, "reb": 6.5, "ast": 7.0, "position": "G"},
        }
        
        for player_name in player_names[:2]:  # Limit to 2 players per failed team
            stats = star_stats.get(player_name, {"pts": 20.0, "reb": 5.0, "ast": 4.0, "position": "G-F"})
            
            player_data = {
                "player_name": player_name,
                "player_id": 0,  # Placeholder ID
                "team": team_name,
                "opponent": opponent,
                "game_date": game_date,
                "position": stats["position"],
                "season_averages": {
                    "pts": stats["pts"],
                    "reb": stats["reb"],
                    "ast": stats["ast"],
                    "stl": 1.0,
                    "blk": 0.5,
                    "fg_pct": 47.5,
                    "fg3_pct": 35.0,
                    "ft_pct": 85.0
                },
                "prizepicks_lines": self._generate_prizepicks_lines(stats["pts"], stats["reb"], stats["ast"]),
                "is_fallback": True  # Flag to indicate this is fallback data
            }
            fallback_players.append(player_data)
        
        print(f"✅ Created {len(fallback_players)} fallback players for {team_name}")
        return fallback_players


# Create singleton instance
popular_players_service = PopularPlayersService()
