"""
Schedule and Team Simulation Routes
Get today's games and simulate all players
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.services.schedule import schedule_service
from app.services.game_simulator import game_simulator
from app.services.nba_stats import nba_stats_service

router = APIRouter(prefix="/api/schedule", tags=["schedule"])

class GameInfo(BaseModel):
    game_id: str
    game_date: str
    home_team: str
    away_team: str
    home_team_name: str
    away_team_name: str
    matchup: str
    game_status: str

class PlayerSimulation(BaseModel):
    player_name: str
    player_id: int
    position: str
    team: str
    is_home: bool
    projected_stats: dict
    season_averages: dict

class TeamGameSimulation(BaseModel):
    game_info: GameInfo
    home_team_players: List[PlayerSimulation]
    away_team_players: List[PlayerSimulation]
    simulation_summary: dict

class PrizePickLeg(BaseModel):
    player_name: str
    prop_type: str  # "points", "rebounds", "assists", "pts+rebs+asts"
    line: float
    pick: str  # "OVER" or "UNDER"

class PrizePickTicket(BaseModel):
    legs: List[PrizePickLeg]
    num_simulations: int = 100

@router.get("/today", response_model=List[GameInfo])
async def get_todays_games():
    """Get all NBA games scheduled for today"""
    try:
        games = schedule_service.get_todays_games()
        
        if not games:
            return []
        
        return [
            GameInfo(
                game_id=game['game_id'],
                game_date=game['game_date_str'],
                home_team=game['home_team'],
                away_team=game['away_team'],
                home_team_name=game['home_team_name'],
                away_team_name=game['away_team_name'],
                matchup=game['matchup'],
                game_status=game['game_status']
            )
            for game in games
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching today's games: {str(e)}")

@router.get("/tomorrow", response_model=List[GameInfo])
async def get_tomorrows_games():
    """Get all NBA games scheduled for tomorrow"""
    try:
        games = schedule_service.get_tomorrows_games()
        
        if not games:
            return []
        
        return [
            GameInfo(
                game_id=game['game_id'],
                game_date=game['game_date_str'],
                home_team=game['home_team'],
                away_team=game['away_team'],
                home_team_name=game['home_team_name'],
                away_team_name=game['away_team_name'],
                matchup=game['matchup'],
                game_status=game['game_status']
            )
            for game in games
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tomorrow's games: {str(e)}")

@router.get("/upcoming")
async def get_upcoming_games(days: int = Query(default=2, ge=1, le=7)):
    """Get all NBA games for the next N days"""
    try:
        games_by_date = schedule_service.get_upcoming_games(days=days)
        return games_by_date
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching upcoming games: {str(e)}")

@router.get("/player/{player_name}/next-game")
async def get_player_next_game(player_name: str):
    """Find a player's next game (today or tomorrow)"""
    try:
        game = schedule_service.find_player_game_today(player_name)
        
        if not game:
            raise HTTPException(
                status_code=404,
                detail=f"No game found for player '{player_name}' in the next 2 days"
            )
        
        return game
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding player game: {str(e)}")

@router.get("/game/{game_id}/simulate-all-players")
async def simulate_game_all_players(
    game_id: str,
    num_simulations: int = Query(default=5, ge=1, le=20),
    top_n_players: int = Query(default=5, ge=3, le=10)
):
    """
    Simulate top players in a specific game
    Returns projections for key rotation players on both teams
    Reduced defaults for faster performance: 5 simulations, 5 players per team
    """
    try:
        # First, get the game info
        today_games = schedule_service.get_todays_games()
        tomorrow_games = schedule_service.get_tomorrows_games()
        all_games = today_games + tomorrow_games
        
        game = next((g for g in all_games if g['game_id'] == game_id), None)
        
        if not game:
            raise HTTPException(status_code=404, detail=f"Game {game_id} not found")
        
        # Get rosters for both teams
        home_roster = schedule_service.get_team_roster(game['home_team_id'])
        away_roster = schedule_service.get_team_roster(game['away_team_id'])
        
        # Simulate all players
        home_simulations = []
        away_simulations = []
        
        # Simulate home team
        for player in home_roster[:10]:  # Top 10 players (rotation players)
            try:
                # Get player season averages
                player_info = await nba_stats_service.get_player_info(player['player_name'])
                if not player_info:
                    continue
                
                season_avg = await nba_stats_service.get_player_season_averages(player_info.player_id)
                if not season_avg:
                    continue
                
                # Get recent games for better simulation
                recent_games = await nba_stats_service.get_player_game_log(player_info.player_id, last_n_games=5)
                if not recent_games:
                    recent_games = []
                
                # Simulate games
                simulations = game_simulator.simulate_multiple_games(
                    player_info=player_info,
                    season_averages=season_avg,
                    recent_games=recent_games,
                    opponent=game['away_team'],
                    is_home=True,
                    num_simulations=num_simulations
                )
                
                # Calculate averages
                avg_stats = {
                    'points': sum(s.points for s in simulations) / len(simulations),
                    'rebounds': sum(s.rebounds for s in simulations) / len(simulations),
                    'assists': sum(s.assists for s in simulations) / len(simulations),
                    'steals': sum(s.steals for s in simulations) / len(simulations),
                    'blocks': sum(s.blocks for s in simulations) / len(simulations),
                }
                
                home_simulations.append({
                    'player_name': player['player_name'],
                    'player_id': player['player_id'],
                    'position': player['position'],
                    'team': game['home_team'],
                    'is_home': True,
                    'projected_stats': avg_stats,
                    'season_averages': {
                        'points': season_avg.points_per_game,
                        'rebounds': season_avg.rebounds_per_game,
                        'assists': season_avg.assists_per_game,
                        'steals': season_avg.steals_per_game,
                        'blocks': season_avg.blocks_per_game
                    }
                })
            except Exception as e:
                print(f"Error simulating {player['player_name']}: {e}")
                continue
        
        # Simulate away team
        for player in away_roster[:10]:  # Top 10 players
            try:
                player_info = await nba_stats_service.get_player_info(player['player_name'])
                if not player_info:
                    continue
                
                season_avg = await nba_stats_service.get_player_season_averages(player_info.player_id)
                if not season_avg:
                    continue
                
                # Get recent games for better simulation
                recent_games = await nba_stats_service.get_player_game_log(player_info.player_id, last_n_games=5)
                if not recent_games:
                    recent_games = []
                
                simulations = game_simulator.simulate_multiple_games(
                    player_info=player_info,
                    season_averages=season_avg,
                    recent_games=recent_games,
                    opponent=game['home_team'],
                    is_home=False,
                    num_simulations=num_simulations
                )
                
                avg_stats = {
                    'points': sum(s.points for s in simulations) / len(simulations),
                    'rebounds': sum(s.rebounds for s in simulations) / len(simulations),
                    'assists': sum(s.assists for s in simulations) / len(simulations),
                    'steals': sum(s.steals for s in simulations) / len(simulations),
                    'blocks': sum(s.blocks for s in simulations) / len(simulations),
                }
                
                away_simulations.append({
                    'player_name': player['player_name'],
                    'player_id': player['player_id'],
                    'position': player['position'],
                    'team': game['away_team'],
                    'is_home': False,
                    'projected_stats': avg_stats,
                    'season_averages': {
                        'points': season_avg.points_per_game,
                        'rebounds': season_avg.rebounds_per_game,
                        'assists': season_avg.assists_per_game,
                        'steals': season_avg.steals_per_game,
                        'blocks': season_avg.blocks_per_game
                    }
                })
            except Exception as e:
                print(f"Error simulating {player['player_name']}: {e}")
                continue
        
        # Calculate team totals
        home_total_pts = sum(p['projected_stats']['points'] for p in home_simulations)
        away_total_pts = sum(p['projected_stats']['points'] for p in away_simulations)
        
        return {
            'game_info': {
                'game_id': game['game_id'],
                'game_date': game['game_date_str'],
                'home_team': game['home_team'],
                'away_team': game['away_team'],
                'home_team_name': game['home_team_name'],
                'away_team_name': game['away_team_name'],
                'matchup': game['matchup'],
                'game_status': game['game_status']
            },
            'home_team_players': home_simulations,
            'away_team_players': away_simulations,
            'simulation_summary': {
                'num_simulations': num_simulations,
                'home_team_projected_points': round(home_total_pts, 1),
                'away_team_projected_points': round(away_total_pts, 1),
                'projected_winner': game['home_team'] if home_total_pts > away_total_pts else game['away_team'],
                'point_differential': abs(round(home_total_pts - away_total_pts, 1)),
                'total_players_simulated': len(home_simulations) + len(away_simulations)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error simulating game: {str(e)}")

@router.post("/simulate-todays-games")
async def simulate_all_todays_games(
    num_simulations: int = Query(default=10, ge=1, le=50)
):
    """
    Simulate ALL games happening today with all players on both teams
    WARNING: This can take several minutes!
    """
    try:
        games = schedule_service.get_todays_games()
        
        if not games:
            return {
                "message": "No games scheduled for today",
                "games": []
            }
        
        all_simulations = []
        
        for game in games:
            try:
                # Simulate this game
                game_sim = await simulate_game_all_players(game['game_id'], num_simulations)
                all_simulations.append(game_sim)
            except Exception as e:
                print(f"Error simulating game {game['game_id']}: {e}")
                continue
        
        return {
            "message": f"Successfully simulated {len(all_simulations)} games",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "total_games": len(games),
            "simulated_games": len(all_simulations),
            "games": all_simulations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error simulating today's games: {str(e)}")

@router.post("/simulate-prizepicks-ticket")
async def simulate_prizepicks_ticket(ticket: PrizePickTicket):
    """
    Simulate a PrizePicks-style ticket with multiple player props
    Returns detailed game context and simulation results for each leg
    
    Example:
    {
        "legs": [
            {"player_name": "LeBron James", "prop_type": "points", "line": 25.5, "pick": "OVER"},
            {"player_name": "Luka Doncic", "prop_type": "assists", "line": 8.5, "pick": "OVER"},
            {"player_name": "Giannis Antetokounmpo", "prop_type": "rebounds", "line": 11.5, "pick": "UNDER"}
        ],
        "num_simulations": 100
    }
    """
    try:
        # Get today's and tomorrow's games
        today_games = schedule_service.get_todays_games()
        tomorrow_games = schedule_service.get_tomorrows_games()
        all_games = today_games + tomorrow_games
        
        if not all_games:
            raise HTTPException(status_code=404, detail="No games scheduled for today or tomorrow")
        
        results = []
        
        for leg in ticket.legs:
            try:
                # Find the player's game
                player_game = None
                for game in all_games:
                    # Get rosters for both teams
                    home_roster = schedule_service.get_team_roster(game['home_team_id'])
                    away_roster = schedule_service.get_team_roster(game['away_team_id'])
                    
                    # Check if player is in either roster
                    player_in_home = any(p['player_name'].lower() == leg.player_name.lower() for p in home_roster)
                    player_in_away = any(p['player_name'].lower() == leg.player_name.lower() for p in away_roster)
                    
                    if player_in_home or player_in_away:
                        player_game = game
                        is_home = player_in_home
                        player_team = game['home_team'] if is_home else game['away_team']
                        opponent_team = game['away_team'] if is_home else game['home_team']
                        break
                
                if not player_game:
                    results.append({
                        "player_name": leg.player_name,
                        "prop_type": leg.prop_type,
                        "line": leg.line,
                        "pick": leg.pick,
                        "status": "error",
                        "error": f"Player {leg.player_name} not found in today's or tomorrow's games",
                        "win_probability": 0
                    })
                    continue
                
                # Get player info
                player_info = await nba_stats_service.get_player_info(leg.player_name)
                if not player_info:
                    results.append({
                        "player_name": leg.player_name,
                        "prop_type": leg.prop_type,
                        "line": leg.line,
                        "pick": leg.pick,
                        "status": "error",
                        "error": f"Could not find player info for {leg.player_name}",
                        "win_probability": 0
                    })
                    continue
                
                # Get season averages and recent games
                season_avg = await nba_stats_service.get_player_season_averages(player_info.player_id)
                recent_games = await nba_stats_service.get_player_game_log(player_info.player_id, last_n_games=5)
                
                if not season_avg:
                    results.append({
                        "player_name": leg.player_name,
                        "prop_type": leg.prop_type,
                        "line": leg.line,
                        "pick": leg.pick,
                        "status": "error",
                        "error": f"No season averages found for {leg.player_name}",
                        "win_probability": 0
                    })
                    continue
                
                # Run simulations
                simulations = game_simulator.simulate_multiple_games(
                    player_info=player_info,
                    season_averages=season_avg,
                    recent_games=recent_games if recent_games else [],
                    opponent=opponent_team,
                    is_home=is_home,
                    num_simulations=ticket.num_simulations
                )
                
                # Calculate win probability based on prop type and pick
                wins = 0
                stat_values = []
                
                for sim in simulations:
                    if leg.prop_type == "points":
                        value = sim.points
                    elif leg.prop_type == "rebounds":
                        value = sim.rebounds
                    elif leg.prop_type == "assists":
                        value = sim.assists
                    elif leg.prop_type == "pts+rebs+asts":
                        value = sim.points + sim.rebounds + sim.assists
                    elif leg.prop_type == "pts+rebs":
                        value = sim.points + sim.rebounds
                    elif leg.prop_type == "pts+asts":
                        value = sim.points + sim.assists
                    elif leg.prop_type == "rebs+asts":
                        value = sim.rebounds + sim.assists
                    else:
                        value = getattr(sim, leg.prop_type, 0)
                    
                    stat_values.append(value)
                    
                    if leg.pick.upper() == "OVER":
                        if value > leg.line:
                            wins += 1
                    else:  # UNDER
                        if value < leg.line:
                            wins += 1
                
                win_probability = (wins / len(simulations)) * 100
                avg_value = sum(stat_values) / len(stat_values)
                
                results.append({
                    "player_name": leg.player_name,
                    "prop_type": leg.prop_type,
                    "line": leg.line,
                    "pick": leg.pick,
                    "status": "success",
                    "game_info": {
                        "game_id": player_game['game_id'],
                        "matchup": player_game['matchup'],
                        "game_date": player_game['game_date_str'],
                        "game_status": player_game['game_status'],
                        "player_team": player_team,
                        "opponent": opponent_team,
                        "is_home": is_home
                    },
                    "season_averages": {
                        "points": season_avg.points_per_game,
                        "rebounds": season_avg.rebounds_per_game,
                        "assists": season_avg.assists_per_game
                    },
                    "simulation_results": {
                        "win_probability": round(win_probability, 2),
                        "projected_value": round(avg_value, 2),
                        "line": leg.line,
                        "difference": round(avg_value - leg.line, 2),
                        "wins": wins,
                        "losses": len(simulations) - wins,
                        "total_simulations": len(simulations)
                    }
                })
                
            except Exception as e:
                print(f"Error simulating {leg.player_name}: {e}")
                results.append({
                    "player_name": leg.player_name,
                    "prop_type": leg.prop_type,
                    "line": leg.line,
                    "pick": leg.pick,
                    "status": "error",
                    "error": str(e),
                    "win_probability": 0
                })
        
        # Calculate overall ticket probability (all legs must win)
        successful_legs = [r for r in results if r['status'] == 'success']
        if successful_legs:
            # Probability all legs win = product of individual probabilities
            overall_probability = 1.0
            for leg in successful_legs:
                overall_probability *= (leg['simulation_results']['win_probability'] / 100)
            overall_probability *= 100
        else:
            overall_probability = 0
        
        return {
            "ticket_summary": {
                "total_legs": len(ticket.legs),
                "successful_simulations": len(successful_legs),
                "failed_simulations": len(ticket.legs) - len(successful_legs),
                "overall_win_probability": round(overall_probability, 2),
                "num_simulations_per_player": ticket.num_simulations
            },
            "legs": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error simulating PrizePicks ticket: {str(e)}")
