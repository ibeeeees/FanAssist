import httpx
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import pandas as pd
from app.models import PlayerInfo, GameStats, SeasonAverages
from app.config import settings
import json
import time
from functools import wraps
from nba_api.stats.static import players as nba_players
from nba_api.stats.endpoints import playergamelog, commonplayerinfo, playercareerstats

def retry_with_backoff(max_retries=3, initial_delay=1):
    """Decorator to retry API calls with exponential backoff"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    error_str = str(e).lower()
                    
                    # If it's a timeout or connection error, retry
                    if any(x in error_str for x in ['timeout', 'timed out', 'connection', 'read timed']):
                        if attempt < max_retries - 1:
                            print(f"   ⏳ Retry {attempt + 1}/{max_retries} after {delay}s...")
                            await asyncio.sleep(delay) if asyncio.iscoroutinefunction(func) else time.sleep(delay)
                            delay *= 2  # Exponential backoff
                            continue
                    # For other errors, don't retry
                    raise
            
            # If all retries failed, raise the last exception
            raise last_exception
        return wrapper
    return decorator

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
        self._last_request_time = 0
        self._min_request_interval = 0.6  # Increased to 600ms between requests to avoid rate limiting
        
        # Add simple in-memory cache with timestamps
        self._cache = {}
        self._cache_ttl = 300  # Cache for 5 minutes (300 seconds)
        
    async def _rate_limit(self):
        """Enforce rate limiting between API calls"""
        current_time = time.time()
        time_since_last = current_time - self._last_request_time
        if time_since_last < self._min_request_interval:
            await asyncio.sleep(self._min_request_interval - time_since_last)
        self._last_request_time = time.time()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if cache_key in self._cache:
            value, timestamp = self._cache[cache_key]
            if time.time() - timestamp < self._cache_ttl:
                print(f"  ✅ Using cached data for {cache_key}")
                return value
            else:
                # Expired, remove from cache
                del self._cache[cache_key]
        return None
    
    def _set_cache(self, cache_key: str, value: Any):
        """Store value in cache with timestamp"""
        self._cache[cache_key] = (value, time.time())
    
    async def get_player_info(self, player_name: str) -> Optional[PlayerInfo]:
        """Get player information by name using nba_api - searches both active and inactive players"""
        try:
            await self._rate_limit()
            
            # Search active players first
            all_players = nba_players.get_active_players()
            
            # Find player by name (case insensitive)
            found_players = [p for p in all_players if player_name.lower() in p['full_name'].lower()]
            
            # If not found in active, search inactive (for injured/traded players)
            if not found_players:
                all_players = nba_players.get_inactive_players()
                found_players = [p for p in all_players if player_name.lower() in p['full_name'].lower()]
            
            if not found_players:
                print(f"Player not found: {player_name}")
                return None
            
            player = found_players[0]
            
            # Get additional player info
            try:
                player_info = commonplayerinfo.CommonPlayerInfo(player_id=player['id'])
                player_data = player_info.get_data_frames()[0]
                
                return PlayerInfo(
                    player_id=player['id'],
                    full_name=player['full_name'],
                    first_name=player['first_name'],
                    last_name=player['last_name'],
                    team_id=int(player_data['TEAM_ID'].iloc[0]) if not player_data.empty else 0,
                    team_name=str(player_data['TEAM_NAME'].iloc[0]) if not player_data.empty else "",
                    team_abbreviation=str(player_data['TEAM_ABBREVIATION'].iloc[0]) if not player_data.empty else "",
                    position=str(player_data['POSITION'].iloc[0]) if not player_data.empty else ""
                )
            except:
                # Fallback if additional info fails
                return PlayerInfo(
                    player_id=player['id'],
                    full_name=player['full_name'],
                    first_name=player['first_name'],
                    last_name=player['last_name'],
                    team_id=0,
                    team_name="",
                    team_abbreviation="",
                    position=""
                )
                
        except Exception as e:
            print(f"Error fetching player info: {e}")
            return None
    
    @retry_with_backoff(max_retries=2, initial_delay=2)
    async def get_player_game_log(self, player_id: int, season: str = "2024-25", last_n_games: int = 10) -> List[GameStats]:
        """Get recent game logs for a player using nba_api with retry logic and caching"""
        try:
            # Check cache first
            cache_key = f"gamelog_{player_id}_{season}_{last_n_games}"
            cached_result = self._get_from_cache(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Add delay to avoid rate limiting
            await self._rate_limit()
            
            # Use nba_api library to get game log with increased timeout
            gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season, timeout=60)
            df = gamelog.get_data_frames()[0]
            
            if df.empty:
                return []
            
            # Limit to last N games
            df = df.head(last_n_games)
            
            game_stats = []
            for _, row in df.iterrows():
                try:
                    game_date = pd.to_datetime(row['GAME_DATE'])
                except:
                    game_date = datetime.now()
                
                # Parse matchup to determine opponent and home/away
                matchup = str(row['MATCHUP'])
                is_home = 'vs.' in matchup
                # Extract opponent abbreviation
                opponent = matchup.split()[-1] if matchup else ""
                
                game_stat = GameStats(
                    game_id=str(row['Game_ID']),
                    player_id=player_id,
                    game_date=game_date,
                    opponent=opponent,
                    is_home=is_home,
                    minutes_played=self._parse_minutes(str(row.get('MIN', ''))) if pd.notna(row.get('MIN')) else None,
                    points=int(row['PTS']) if pd.notna(row.get('PTS')) else None,
                    rebounds=int(row['REB']) if pd.notna(row.get('REB')) else None,
                    assists=int(row['AST']) if pd.notna(row.get('AST')) else None,
                    steals=int(row['STL']) if pd.notna(row.get('STL')) else None,
                    blocks=int(row['BLK']) if pd.notna(row.get('BLK')) else None,
                    turnovers=int(row['TOV']) if pd.notna(row.get('TOV')) else None,
                    field_goals_made=int(row['FGM']) if pd.notna(row.get('FGM')) else None,
                    field_goals_attempted=int(row['FGA']) if pd.notna(row.get('FGA')) else None,
                    three_pointers_made=int(row['FG3M']) if pd.notna(row.get('FG3M')) else None,
                    three_pointers_attempted=int(row['FG3A']) if pd.notna(row.get('FG3A')) else None,
                    free_throws_made=int(row['FTM']) if pd.notna(row.get('FTM')) else None,
                    free_throws_attempted=int(row['FTA']) if pd.notna(row.get('FTA')) else None,
                    plus_minus=int(row['PLUS_MINUS']) if pd.notna(row.get('PLUS_MINUS')) else None
                )
                
                # Calculate fantasy score
                game_stat.fantasy_score = game_stat.calculate_fantasy_score()
                game_stats.append(game_stat)
            
            # Cache the result
            self._set_cache(cache_key, game_stats)
            return game_stats
            
        except Exception as e:
            print(f"Error fetching game log: {e}")
            return []
    
    @retry_with_backoff(max_retries=3, initial_delay=2)
    async def get_player_season_averages(self, player_id: int, season: str = "2024-25") -> Optional[SeasonAverages]:
        """Get season averages for a player using nba_api with retry logic and caching"""
        try:
            # Check cache first
            cache_key = f"season_avg_{player_id}_{season}"
            cached_result = self._get_from_cache(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Add delay to avoid rate limiting
            await self._rate_limit()
            
            # Use career stats endpoint to get season averages
            career_stats = playercareerstats.PlayerCareerStats(player_id=player_id, timeout=60)
            df = career_stats.get_data_frames()[0]  # SeasonTotalsRegularSeason
            
            if df.empty:
                return None
            
            # Get the specified season stats
            season_data = df[df['SEASON_ID'] == season]
            
            if season_data.empty:
                # If exact season not found, get the most recent season
                season_data = df.iloc[[-1]]
            
            row = season_data.iloc[0]
            games_played = int(row['GP']) if pd.notna(row.get('GP')) else 0
            
            if games_played == 0:
                return None
            
            # Calculate per-game averages
            season_avg = SeasonAverages(
                player_id=player_id,
                season=season,
                games_played=games_played,
                minutes_per_game=float(row['MIN']) / games_played if pd.notna(row.get('MIN')) and games_played > 0 else 0.0,
                points_per_game=float(row['PTS']) / games_played if pd.notna(row.get('PTS')) and games_played > 0 else 0.0,
                rebounds_per_game=float(row['REB']) / games_played if pd.notna(row.get('REB')) and games_played > 0 else 0.0,
                assists_per_game=float(row['AST']) / games_played if pd.notna(row.get('AST')) and games_played > 0 else 0.0,
                steals_per_game=float(row['STL']) / games_played if pd.notna(row.get('STL')) and games_played > 0 else 0.0,
                blocks_per_game=float(row['BLK']) / games_played if pd.notna(row.get('BLK')) and games_played > 0 else 0.0,
                turnovers_per_game=float(row['TOV']) / games_played if pd.notna(row.get('TOV')) and games_played > 0 else 0.0,
                field_goal_percentage=float(row['FG_PCT']) if pd.notna(row.get('FG_PCT')) else 0.0,
                three_point_percentage=float(row['FG3_PCT']) if pd.notna(row.get('FG3_PCT')) else 0.0,
                free_throw_percentage=float(row['FT_PCT']) if pd.notna(row.get('FT_PCT')) else 0.0
            )
            
            # Cache the result
            self._set_cache(cache_key, season_avg)
            return season_avg
                
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