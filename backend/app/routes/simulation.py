"""
Simulation Routes - API endpoints for game and bet simulation
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.services.game_simulator import game_simulator
from app.services.nba_stats import nba_stats_service
from app.models import PropType, BetType, PlayerInfo

router = APIRouter(prefix="/api/simulation", tags=["Simulation"])


# Request/Response Models
class SimulationRequest(BaseModel):
    player_name: str = Field(..., description="Full player name")
    opponent: Optional[str] = Field(None, description="Opponent team abbreviation")
    is_home: bool = Field(True, description="Is this a home game?")
    num_simulations: int = Field(1, description="Number of simulations to run", ge=1, le=1000)


class SingleGameSimulation(BaseModel):
    player_name: str
    game_date: datetime
    opponent: str
    is_home: bool
    points: int
    rebounds: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    three_pointers_made: int
    free_throws_made: int
    fantasy_score: Optional[float]
    minutes_played: float
    plus_minus: int


class SimulationResponse(BaseModel):
    player_name: str
    simulations: List[SingleGameSimulation]
    averages: dict
    message: str


class BetSimulationRequest(BaseModel):
    player_name: str = Field(..., description="Full player name")
    prop_type: PropType = Field(..., description="Type of prop to simulate")
    line: float = Field(..., description="The line/over-under value")
    bet_type: BetType = Field(..., description="Over or Under")
    num_simulations: int = Field(100, description="Number of simulations", ge=10, le=1000)
    opponent: Optional[str] = None
    is_home: bool = True


class BetSimulationResponse(BaseModel):
    player_name: str
    prop_type: str
    line: float
    bet_type: str
    win_probability: float
    expected_value: float
    median_result: float
    standard_deviation: float
    percentage_over: float
    percentage_under: float
    confidence_level: str
    simulations_run: int
    recommendation: str
    visualization_data: dict


class MultiLegRequest(BaseModel):
    class LegInfo(BaseModel):
        player_name: str
        prop_type: PropType
        line: float
        bet_type: BetType
    
    legs: List[LegInfo] = Field(..., description="List of bet legs", min_length=2, max_length=10)
    num_simulations: int = Field(100, description="Number of simulations", ge=10, le=500)


class MultiLegResponse(BaseModel):
    ticket_win_probability: float
    ticket_hit_rate: str
    expected_wins_per_100: int
    leg_probabilities: List[dict]
    total_legs: int
    simulations_run: int
    recommendation: str
    visual_breakdown: dict


@router.post("/single-game", response_model=SimulationResponse)
async def simulate_single_game(request: SimulationRequest):
    """
    🎮 Simulate a game for a player
    
    This endpoint simulates how a player might perform in their next game based on:
    - Season averages
    - Recent form (last 5-10 games)
    - Home/away status
    - Random variance (because basketball is unpredictable!)
    
    Perfect for:
    - Seeing different possible outcomes
    - Understanding performance ranges
    - Visualizing "what if" scenarios
    """
    try:
        # Get player info
        player_info = await nba_stats_service.get_player_info(request.player_name)
        if not player_info:
            raise HTTPException(status_code=404, detail=f"Player '{request.player_name}' not found")
        
        # Get player stats
        recent_games = await nba_stats_service.get_player_game_log(player_info.player_id, last_n_games=10)
        season_averages = await nba_stats_service.get_player_season_averages(player_info.player_id)
        
        if not season_averages:
            raise HTTPException(status_code=404, detail="Could not fetch player season averages")
        
        # Run simulations
        simulations = game_simulator.simulate_multiple_games(
            player_info=player_info,
            season_averages=season_averages,
            recent_games=recent_games,
            num_simulations=request.num_simulations,
            opponent=request.opponent,
            is_home=request.is_home
        )
        
        # Convert to response format
        sim_results = [
            SingleGameSimulation(
                player_name=player_info.full_name,
                game_date=sim.game_date,
                opponent=sim.opponent,
                is_home=sim.is_home,
                points=sim.points or 0,
                rebounds=sim.rebounds or 0,
                assists=sim.assists or 0,
                steals=sim.steals or 0,
                blocks=sim.blocks or 0,
                turnovers=sim.turnovers or 0,
                three_pointers_made=sim.three_pointers_made or 0,
                free_throws_made=sim.free_throws_made or 0,
                fantasy_score=sim.fantasy_score,
                minutes_played=sim.minutes_played or 0,
                plus_minus=sim.plus_minus or 0
            )
            for sim in simulations
        ]
        
        # Calculate averages
        averages = {
            "points": round(sum(s.points for s in sim_results) / len(sim_results), 1),
            "rebounds": round(sum(s.rebounds for s in sim_results) / len(sim_results), 1),
            "assists": round(sum(s.assists for s in sim_results) / len(sim_results), 1),
            "steals": round(sum(s.steals for s in sim_results) / len(sim_results), 1),
            "blocks": round(sum(s.blocks for s in sim_results) / len(sim_results), 1),
            "three_pointers_made": round(sum(s.three_pointers_made for s in sim_results) / len(sim_results), 1),
        }
        
        return SimulationResponse(
            player_name=player_info.full_name,
            simulations=sim_results,
            averages=averages,
            message=f"Successfully simulated {len(sim_results)} games for {player_info.full_name}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")


@router.post("/bet-outcome", response_model=BetSimulationResponse)
async def simulate_bet_outcome(request: BetSimulationRequest):
    """
    🎲 Simulate a bet to see your winning chances
    
    This shows you:
    - Win probability (% chance of hitting)
    - Expected outcome (average result)
    - How often it goes over vs under
    - Confidence level
    
    Example: If you bet LeBron OVER 25.5 points, this will simulate 100 games
    and tell you what % of the time he scores over 25.5
    """
    try:
        # Get player data
        player_info = await nba_stats_service.get_player_info(request.player_name)
        if not player_info:
            raise HTTPException(status_code=404, detail=f"Player '{request.player_name}' not found")
        
        recent_games = await nba_stats_service.get_player_game_log(player_info.player_id, last_n_games=10)
        season_averages = await nba_stats_service.get_player_season_averages(player_info.player_id)
        
        if not season_averages:
            raise HTTPException(status_code=404, detail="Could not fetch player season averages")
        
        # Run bet simulation
        result = game_simulator.simulate_bet_outcome(
            player_info=player_info,
            season_averages=season_averages,
            recent_games=recent_games,
            prop_type=request.prop_type,
            line=request.line,
            bet_type=request.bet_type,
            num_simulations=request.num_simulations
        )
        
        # Generate recommendation
        win_prob = result["win_probability"]
        if win_prob >= 0.60:
            recommendation = f"✅ STRONG {request.bet_type.value.upper()} - High confidence ({int(win_prob*100)}% win rate)"
        elif win_prob >= 0.52:
            recommendation = f"✔️ LEAN {request.bet_type.value.upper()} - Slight edge ({int(win_prob*100)}% win rate)"
        elif win_prob >= 0.48:
            recommendation = f"⚠️ COIN FLIP - Very close to 50/50, avoid or small stake"
        else:
            opposite = "UNDER" if request.bet_type == BetType.OVER else "OVER"
            recommendation = f"❌ AVOID - Better to bet {opposite} ({int((1-win_prob)*100)}% win rate)"
        
        # Create visualization data
        viz_data = {
            "distribution": {
                "over_percentage": result["percentage_over"],
                "under_percentage": result["percentage_under"],
                "line": request.line
            },
            "comparison": {
                "season_average": getattr(season_averages, f"{request.prop_type.value}_per_game", 0),
                "expected_simulation": result["expected_value"],
                "line": request.line
            }
        }
        
        return BetSimulationResponse(
            player_name=player_info.full_name,
            prop_type=request.prop_type.value,
            line=request.line,
            bet_type=request.bet_type.value,
            win_probability=result["win_probability"],
            expected_value=result["expected_value"],
            median_result=result["median_result"],
            standard_deviation=result["standard_deviation"],
            percentage_over=result["percentage_over"],
            percentage_under=result["percentage_under"],
            confidence_level=result["confidence_level"],
            simulations_run=result["simulations_run"],
            recommendation=recommendation,
            visualization_data=viz_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bet simulation error: {str(e)}")


@router.post("/multi-leg-ticket", response_model=MultiLegResponse)
async def simulate_multi_leg_ticket(request: MultiLegRequest):
    """
    🎟️ Simulate a multi-leg parlay ticket
    
    This is SUPER useful for:
    - Seeing how likely your entire ticket is to hit
    - Finding which leg is the weakest
    - Understanding parlay difficulty (more legs = much harder!)
    
    Example: If you have a 4-leg ticket, this shows:
    - Individual win probability for each leg
    - Overall ticket win probability
    - How many times per 100 the full ticket would hit
    """
    try:
        # Gather data for all legs
        legs_data = []
        
        for leg in request.legs:
            player_info = await nba_stats_service.get_player_info(leg.player_name)
            if not player_info:
                raise HTTPException(status_code=404, detail=f"Player '{leg.player_name}' not found")
            
            recent_games = await nba_stats_service.get_player_game_log(player_info.player_id, last_n_games=10)
            season_averages = await nba_stats_service.get_player_season_averages(player_info.player_id)
            
            if not season_averages:
                raise HTTPException(status_code=404, detail=f"Could not fetch season averages for {leg.player_name}")
            
            legs_data.append({
                "player_info": player_info,
                "season_averages": season_averages,
                "recent_games": recent_games,
                "prop_type": leg.prop_type,
                "line": leg.line,
                "bet_type": leg.bet_type
            })
        
        # Run multi-leg simulation
        result = game_simulator.simulate_multi_leg_ticket(
            legs=legs_data,
            num_simulations=request.num_simulations
        )
        
        # Create visual breakdown
        visual = {
            "legs_summary": [
                {
                    "leg": idx + 1,
                    "player": leg["player_info"].full_name,
                    "bet": f"{leg['bet_type'].value.upper()} {leg['line']} {leg['prop_type'].value}",
                    "hit_rate": result["leg_probabilities"][idx]["hit_rate"]
                }
                for idx, leg in enumerate(legs_data)
            ],
            "difficulty_rating": _calculate_difficulty_rating(
                result["ticket_win_probability"],
                len(request.legs)
            )
        }
        
        return MultiLegResponse(
            ticket_win_probability=result["ticket_win_probability"],
            ticket_hit_rate=result["ticket_hit_rate"],
            expected_wins_per_100=result["expected_wins_per_100"],
            leg_probabilities=result["leg_probabilities"],
            total_legs=result["total_legs"],
            simulations_run=result["simulations_run"],
            recommendation=result["recommendation"],
            visual_breakdown=visual
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multi-leg simulation error: {str(e)}")


@router.get("/quick-odds/{player_name}")
async def quick_odds_check(
    player_name: str,
    prop_type: PropType = Query(..., description="Stat to check"),
    line: float = Query(..., description="Line value"),
):
    """
    ⚡ Quick odds check for a single prop
    
    Fast simulation (50 iterations) for quick decision making
    """
    try:
        player_info = await nba_stats_service.get_player_info(player_name)
        if not player_info:
            raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found")
        
        recent_games = await nba_stats_service.get_player_game_log(player_info.player_id, last_n_games=10)
        season_averages = await nba_stats_service.get_player_season_averages(player_info.player_id)
        
        if not season_averages:
            raise HTTPException(status_code=404, detail="Could not fetch player season averages")
        
        # Quick simulation for both OVER and UNDER
        over_result = game_simulator.simulate_bet_outcome(
            player_info, season_averages, recent_games,
            prop_type, line, BetType.OVER, num_simulations=50
        )
        
        under_result = game_simulator.simulate_bet_outcome(
            player_info, season_averages, recent_games,
            prop_type, line, BetType.UNDER, num_simulations=50
        )
        
        # Determine best bet
        if over_result["win_probability"] > under_result["win_probability"]:
            best_bet = "OVER"
            confidence = over_result["win_probability"]
        else:
            best_bet = "UNDER"
            confidence = under_result["win_probability"]
        
        return {
            "player": player_info.full_name,
            "prop": f"{prop_type.value.replace('_', ' ').title()}",
            "line": line,
            "best_bet": best_bet,
            "confidence": f"{int(confidence * 100)}%",
            "over_probability": f"{int(over_result['win_probability'] * 100)}%",
            "under_probability": f"{int(under_result['win_probability'] * 100)}%",
            "expected_result": over_result["expected_value"],
            "season_average": getattr(season_averages, f"{prop_type.value}_per_game", 0),
            "recommendation": "✅ TAKE IT" if confidence >= 0.58 else "⚠️ CLOSE CALL" if confidence >= 0.52 else "❌ PASS"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quick odds check error: {str(e)}")


def _calculate_difficulty_rating(win_prob: float, num_legs: int) -> str:
    """Calculate how difficult a ticket is to hit"""
    if num_legs >= 6:
        return "🔴 EXTREMELY HARD - 6+ leg parlays rarely hit"
    elif num_legs >= 4:
        if win_prob >= 0.10:
            return "🟡 HARD - But better odds than average"
        else:
            return "🔴 VERY HARD - Low probability"
    elif num_legs >= 3:
        if win_prob >= 0.20:
            return "🟢 MODERATE - Reasonable shot"
        else:
            return "🟡 MODERATE-HARD - Challenging"
    else:
        if win_prob >= 0.40:
            return "🟢 EASY - Good odds"
        else:
            return "🟡 MODERATE - Doable"
