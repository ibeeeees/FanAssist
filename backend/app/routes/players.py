from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models import PlayerInfo
from app.services.nba_stats import nba_stats_service

router = APIRouter()

@router.get("/search", response_model=List[PlayerInfo])
async def search_players(
    query: str = Query(..., description="Player name to search for"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results")
):
    """Search for NBA players by name"""
    try:
        players = await nba_stats_service.search_players(query, limit)
        return players
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching players: {str(e)}")

@router.get("/{player_name}/info", response_model=PlayerInfo)
async def get_player_info(player_name: str):
    """Get detailed information about a specific player"""
    try:
        player = await nba_stats_service.get_player_info(player_name)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        return player
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching player info: {str(e)}")

@router.get("/{player_id}/stats/recent")
async def get_player_recent_stats(
    player_id: int,
    games: int = Query(10, ge=1, le=50, description="Number of recent games to retrieve")
):
    """Get recent game statistics for a player"""
    try:
        stats = await nba_stats_service.get_player_game_log(player_id, last_n_games=games)
        return {"player_id": player_id, "recent_games": stats, "games_count": len(stats)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recent stats: {str(e)}")

@router.get("/{player_id}/stats/season")
async def get_player_season_stats(
    player_id: int,
    season: str = Query("2023-24", description="NBA season (e.g., '2023-24')")
):
    """Get season averages for a player"""
    try:
        averages = await nba_stats_service.get_player_season_averages(player_id, season)
        if not averages:
            raise HTTPException(status_code=404, detail="Season averages not found")
        return averages
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching season stats: {str(e)}")