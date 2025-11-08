import httpx
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import pandas as pd
from app.models import PlayerInfo, GameStats, SeasonAverages
from app.config import settings
import json

class NBAStatsService:
    def __init__(self):
        self.base_url = settings.nba_stats_base_url
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.nba.com/',
            'Connection': 'keep-alive',
        }
        
    async def get_player_info(self, player_name: str) -> Optional[PlayerInfo]:
        """Get player information by name"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/commonallplayers"
                params = {
                    'IsOnlyCurrentSeason': '1',
                    'LeagueID': '00',
                    'Season': '2023-24'
                }
                
                response = await client.get(url, params=params, headers=self.headers)
                response.raise_for_status()
                
                data = response.json()
                players = data['resultSets'][0]['rowSet']
                
                # Find player by name (case insensitive)
                for player in players:
                    if player_name.lower() in player[2].lower():  # DISPLAY_FIRST_LAST
                        return PlayerInfo(
                            player_id=player[0],
                            full_name=player[2],
                            first_name=player[1].split()[0] if player[1] else "",
                            last_name=player[1].split()[-1] if player[1] else "",
                            team_id=player[7] if len(player) > 7 else 0,
                            team_name="",  # Will be filled by team service
                            team_abbreviation="",
                            position=""
                        )
                return None
                
        except Exception as e:
            print(f"Error fetching player info: {e}")
            return None
    
    async def get_player_game_log(self, player_id: int, season: str = "2023-24", last_n_games: int = 10) -> List[GameStats]:
        """Get recent game logs for a player"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/playergamelog"
                params = {
                    'PlayerID': str(player_id),
                    'Season': season,
                    'SeasonType': 'Regular Season'
                }
                
                response = await client.get(url, params=params, headers=self.headers)
                response.raise_for_status()
                
                data = response.json()
                games = data['resultSets'][0]['rowSet'][:last_n_games]
                
                game_stats = []
                for game in games:
                    try:
                        game_date = datetime.strptime(game[3], '%b %d, %Y')
                    except:
                        game_date = datetime.now()
                    
                    game_stat = GameStats(
                        game_id=game[2],
                        player_id=player_id,
                        game_date=game_date,
                        opponent=game[4].replace('vs. ', '').replace('@ ', ''),
                        is_home='vs.' in game[4],
                        minutes_played=self._parse_minutes(game[8]) if len(game) > 8 else None,
                        points=game[26] if len(game) > 26 else None,
                        rebounds=game[20] if len(game) > 20 else None,
                        assists=game[21] if len(game) > 21 else None,
                        steals=game[22] if len(game) > 22 else None,
                        blocks=game[23] if len(game) > 23 else None,
                        turnovers=game[24] if len(game) > 24 else None,
                        field_goals_made=game[9] if len(game) > 9 else None,
                        field_goals_attempted=game[10] if len(game) > 10 else None,
                        three_pointers_made=game[12] if len(game) > 12 else None,
                        three_pointers_attempted=game[13] if len(game) > 13 else None,
                        free_throws_made=game[15] if len(game) > 15 else None,
                        free_throws_attempted=game[16] if len(game) > 16 else None,
                        plus_minus=game[25] if len(game) > 25 else None
                    )
                    
                    # Calculate fantasy score
                    game_stat.fantasy_score = game_stat.calculate_fantasy_score()
                    game_stats.append(game_stat)
                
                return game_stats
                
        except Exception as e:
            print(f"Error fetching game log: {e}")
            return []
    
    async def get_player_season_averages(self, player_id: int, season: str = "2023-24") -> Optional[SeasonAverages]:
        """Get season averages for a player"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/playerdashboardbyyearoveryear"
                params = {
                    'PlayerID': str(player_id),
                    'Season': season,
                    'SeasonType': 'Regular Season'
                }
                
                response = await client.get(url, params=params, headers=self.headers)
                response.raise_for_status()
                
                data = response.json()
                season_stats = data['resultSets'][1]['rowSet']  # OverallPlayerDashboard
                
                if not season_stats:
                    return None
                
                stats = season_stats[0]  # Current season stats
                
                return SeasonAverages(
                    player_id=player_id,
                    season=season,
                    games_played=stats[3],
                    minutes_per_game=stats[8],
                    points_per_game=stats[26],
                    rebounds_per_game=stats[20],
                    assists_per_game=stats[21],
                    steals_per_game=stats[22],
                    blocks_per_game=stats[23],
                    turnovers_per_game=stats[24],
                    field_goal_percentage=stats[11],
                    three_point_percentage=stats[14],
                    free_throw_percentage=stats[17]
                )
                
        except Exception as e:
            print(f"Error fetching season averages: {e}")
            return None
    
    def _parse_minutes(self, minutes_str: str) -> Optional[float]:
        """Parse minutes string (e.g., '32:15') to float"""
        try:
            if not minutes_str or minutes_str == 'None':
                return None
            parts = minutes_str.split(':')
            return float(parts[0]) + float(parts[1]) / 60
        except:
            return None
    
    async def search_players(self, query: str, limit: int = 10) -> List[PlayerInfo]:
        """Search for players by name"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/commonallplayers"
                params = {
                    'IsOnlyCurrentSeason': '1',
                    'LeagueID': '00',
                    'Season': '2023-24'
                }
                
                response = await client.get(url, params=params, headers=self.headers)
                response.raise_for_status()
                
                data = response.json()
                players = data['resultSets'][0]['rowSet']
                
                # Filter and search players
                matching_players = []
                for player in players:
                    if query.lower() in player[2].lower() and len(matching_players) < limit:
                        matching_players.append(PlayerInfo(
                            player_id=player[0],
                            full_name=player[2],
                            first_name=player[1].split()[0] if player[1] else "",
                            last_name=player[1].split()[-1] if player[1] else "",
                            team_id=player[7] if len(player) > 7 else 0,
                            team_name="",
                            team_abbreviation="",
                            position=""
                        ))
                
                return matching_players
                
        except Exception as e:
            print(f"Error searching players: {e}")
            return []

# Create a singleton instance
nba_stats_service = NBAStatsService()