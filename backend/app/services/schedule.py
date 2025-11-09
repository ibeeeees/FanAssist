"""
NBA Schedule Service - Get today's and upcoming games
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from nba_api.stats.endpoints import scoreboardv2
import pandas as pd

class NBAScheduleService:
    """Service to get NBA game schedules"""
    
    def __init__(self):
        # Add simple in-memory cache with timestamps
        self._cache = {}
        self._cache_ttl = 600  # Cache for 10 minutes (600 seconds) - games don't change often
        
    def _get_from_cache(self, cache_key: str):
        """Get value from cache if not expired"""
        import time
        if cache_key in self._cache:
            value, timestamp = self._cache[cache_key]
            if time.time() - timestamp < self._cache_ttl:
                print(f"  ✅ Using cached games for {cache_key}")
                return value
            else:
                # Expired, remove from cache
                del self._cache[cache_key]
        return None
    
    def _set_cache(self, cache_key: str, value):
        """Store value in cache with timestamp"""
        import time
        self._cache[cache_key] = (value, time.time())
    
    def get_games_for_date(self, date: datetime) -> List[Dict]:
        """
        Get all NBA games for a specific date (with caching)
        
        Returns list of games with:
        - game_id
        - game_date
        - home_team
        - away_team
        - home_team_id
        - away_team_id
        - game_status
        """
        try:
            # Format date for NBA API (YYYY-MM-DD format works)
            date_str = date.strftime('%Y-%m-%d')
            
            # Check cache first
            cache_key = f"games_{date_str}"
            cached_result = self._get_from_cache(cache_key)
            if cached_result is not None:
                return cached_result
            
            print(f"Fetching games for date: {date_str}")
            
            # Get scoreboard for the date with timeout
            import time
            time.sleep(0.5)  # Add delay before API call
            scoreboard = scoreboardv2.ScoreboardV2(game_date=date_str, timeout=30)
            games_df = scoreboard.get_data_frames()[0]  # GameHeader
            line_score_df = scoreboard.get_data_frames()[1]  # LineScore
            
            print(f"Found {len(games_df)} games in API response")
            
            if games_df.empty:
                return []
            
            games = []
            for idx, game in games_df.iterrows():
                try:
                    game_id = str(game['GAME_ID'])
                    home_team_id = int(game['HOME_TEAM_ID'])
                    visitor_team_id = int(game['VISITOR_TEAM_ID'])
                    
                    # Parse GAMECODE for team abbreviations (format: YYYYMMDD/AWAYINHOME)
                    gamecode = str(game.get('GAMECODE', ''))
                    if '/' in gamecode:
                        teams_part = gamecode.split('/')[1]  # Gets "DALWAS" from "20251108/DALWAS"
                        # First 3 chars = away team, last 3 chars = home team
                        away_abbrev = teams_part[:3]
                        home_abbrev = teams_part[3:6]
                    else:
                        # Fallback if GAMECODE format is different
                        away_abbrev = f"TEAM{visitor_team_id}"
                        home_abbrev = f"TEAM{home_team_id}"
                    
                    game_data = {
                        'game_id': game_id,
                        'game_date': date,
                        'game_date_str': date_str,
                        'home_team': home_abbrev,
                        'away_team': away_abbrev,
                        'home_team_id': home_team_id,
                        'away_team_id': visitor_team_id,
                        'home_team_name': home_abbrev,  # We'll use abbreviations as names for now
                        'away_team_name': away_abbrev,
                        'game_status': str(game['GAME_STATUS_TEXT']),
                        'matchup': f"{away_abbrev} @ {home_abbrev}",
                        'arena': str(game.get('ARENA_NAME', ''))
                    }
                    
                    games.append(game_data)
                    print(f"Added game: {game_data['matchup']} at {game_data['arena']}")
                except Exception as e:
                    print(f"Error processing game {game.get('GAME_ID', 'unknown')}: {e}")
                    continue
            
            print(f"Returning {len(games)} games")
            
            # Cache the result
            self._set_cache(cache_key, games)
            return games
            
        except Exception as e:
            print(f"Error fetching games for {date}: {e}")
            return []
    
    def get_todays_games(self) -> List[Dict]:
        """Get all games scheduled for today"""
        today = datetime.now()
        return self.get_games_for_date(today)
    
    def get_tomorrows_games(self) -> List[Dict]:
        """Get all games scheduled for tomorrow"""
        tomorrow = datetime.now() + timedelta(days=1)
        return self.get_games_for_date(tomorrow)
    
    def get_upcoming_games(self, days: int = 2) -> Dict[str, List[Dict]]:
        """
        Get games for the next N days
        
        Returns dict with date strings as keys and game lists as values
        """
        games_by_date = {}
        
        for i in range(days):
            date = datetime.now() + timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            games = self.get_games_for_date(date)
            
            if games:
                games_by_date[date_str] = games
        
        return games_by_date
    
    def get_team_roster(self, team_id: int, season: str = "2024-25") -> List[Dict]:
        """
        Get roster for a team
        Note: This is a simplified version - in production, use commonteamroster endpoint
        """
        try:
            from nba_api.stats.endpoints import commonteamroster
            
            roster = commonteamroster.CommonTeamRoster(
                team_id=team_id,
                season=season
            )
            
            roster_df = roster.get_data_frames()[0]
            
            players = []
            for _, player in roster_df.iterrows():
                players.append({
                    'player_id': int(player['PLAYER_ID']),
                    'player_name': player['PLAYER'],
                    'position': player['POSITION'],
                    'jersey_number': player['NUM'],
                    'age': player.get('AGE', 0),
                    'height': player.get('HEIGHT', ''),
                    'weight': player.get('WEIGHT', '')
                })
            
            return players
            
        except Exception as e:
            print(f"Error fetching roster for team {team_id}: {e}")
            return []
    
    def find_game_by_team(self, team_abbrev: str, date: Optional[datetime] = None) -> Optional[Dict]:
        """
        Find a game for a specific team on a specific date
        If no date provided, search today and tomorrow
        """
        if date is None:
            # Search today and tomorrow
            for i in range(2):
                search_date = datetime.now() + timedelta(days=i)
                games = self.get_games_for_date(search_date)
                
                for game in games:
                    if game['home_team'].upper() == team_abbrev.upper() or \
                       game['away_team'].upper() == team_abbrev.upper():
                        return game
            return None
        else:
            games = self.get_games_for_date(date)
            for game in games:
                if game['home_team'].upper() == team_abbrev.upper() or \
                   game['away_team'].upper() == team_abbrev.upper():
                    return game
            return None
    
    def find_player_game_today(self, player_name: str) -> Optional[Dict]:
        """
        Find if a player has a game today or tomorrow
        Returns game info with player's team marked
        """
        from nba_api.stats.static import players as nba_players
        
        # Find player
        all_players = nba_players.get_active_players()
        found_players = [p for p in all_players if player_name.lower() in p['full_name'].lower()]
        
        if not found_players:
            return None
        
        player = found_players[0]
        
        # Get player's current team (simplified - in production, use commonplayerinfo)
        try:
            from nba_api.stats.endpoints import commonplayerinfo
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=player['id'])
            player_data = player_info.get_data_frames()[0]
            
            if player_data.empty:
                return None
            
            team_abbrev = str(player_data['TEAM_ABBREVIATION'].iloc[0])
            
            # Find game for this team
            game = self.find_game_by_team(team_abbrev)
            
            if game:
                game['player_name'] = player['full_name']
                game['player_id'] = player['id']
                game['player_team'] = team_abbrev
                game['is_home'] = game['home_team'] == team_abbrev
                
            return game
            
        except Exception as e:
            print(f"Error finding player game: {e}")
            return None

# Create a singleton instance
schedule_service = NBAScheduleService()
