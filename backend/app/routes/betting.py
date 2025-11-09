from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from app.models import (
    UserAccount, Bet, BetSlip, BetType, PropType, 
    Leaderboard, BettingStats, Portfolio, BetStatus
)
from app.services.paper_betting import paper_betting_service
from pydantic import BaseModel

router = APIRouter()

# Request/Response Models
class CreateUserRequest(BaseModel):
    username: str
    email: str

class PlaceBetRequest(BaseModel):
    player_name: str
    prop_type: PropType
    line_value: float
    bet_type: BetType
    wager_amount: float
    game_date: Optional[datetime] = None

class SettleBetRequest(BaseModel):
    actual_result: float

# User Management Endpoints
@router.post("/users", response_model=UserAccount)
async def create_user(request: CreateUserRequest):
    """Create a new user account with starting virtual money"""
    try:
        user = await paper_betting_service.create_user_account(
            username=request.username,
            email=request.email
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@router.get("/users/{user_id}", response_model=UserAccount)
async def get_user(user_id: str):
    """Get user account details"""
    user = await paper_betting_service.get_user_account(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/username/{username}", response_model=UserAccount)
async def get_user_by_username(username: str):
    """Get user account by username"""
    user = await paper_betting_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/{user_id}/reset", response_model=UserAccount)
async def reset_user_balance(user_id: str):
    """Reset user balance to starting amount (for demo purposes)"""
    try:
        user = await paper_betting_service.reset_user_balance(user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting balance: {str(e)}")

# Betting Endpoints
@router.post("/users/{user_id}/bets", response_model=Bet)
async def place_bet(user_id: str, bet_request: PlaceBetRequest):
    """Place a new bet"""
    try:
        bet = await paper_betting_service.place_bet(
            user_id=user_id,
            player_name=bet_request.player_name,
            prop_type=bet_request.prop_type,
            line_value=bet_request.line_value,
            bet_type=bet_request.bet_type,
            wager_amount=bet_request.wager_amount,
            game_date=bet_request.game_date
        )
        return bet
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error placing bet: {str(e)}")

@router.get("/users/{user_id}/bets")
async def get_user_bets(
    user_id: str,
    status: Optional[BetStatus] = None,
    limit: int = 50
):
    """Get user's betting history"""
    try:
        portfolio = await paper_betting_service.get_user_portfolio(user_id)
        
        if status == BetStatus.PENDING:
            bets = portfolio.active_bets[:limit]
        elif status:
            all_bets = portfolio.recent_bets + portfolio.active_bets
            bets = [bet for bet in all_bets if bet.status == status][:limit]
        else:
            bets = (portfolio.active_bets + portfolio.recent_bets)[:limit]
        
        return {
            "bets": bets,
            "total_count": len(bets)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bets: {str(e)}")

@router.post("/bets/{bet_id}/settle", response_model=Bet)
async def settle_bet(bet_id: str, settle_request: SettleBetRequest):
    """Settle a bet with actual game result"""
    try:
        bet = await paper_betting_service.settle_bet(bet_id, settle_request.actual_result)
        return bet
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error settling bet: {str(e)}")

@router.post("/bets/{bet_id}/simulate", response_model=Bet)
async def simulate_bet_settlement(bet_id: str, win_probability: float = 0.5):
    """Simulate bet settlement for testing (randomly determine outcome)"""
    try:
        if win_probability < 0 or win_probability > 1:
            raise ValueError("Win probability must be between 0 and 1")
        
        bet = await paper_betting_service.simulate_bet_settlement(bet_id, win_probability)
        return bet
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error simulating bet: {str(e)}")

# Portfolio and Analytics Endpoints
@router.get("/users/{user_id}/portfolio", response_model=Portfolio)
async def get_user_portfolio(user_id: str):
    """Get user's complete betting portfolio"""
    try:
        portfolio = await paper_betting_service.get_user_portfolio(user_id)
        return portfolio
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching portfolio: {str(e)}")

@router.get("/users/{user_id}/stats", response_model=BettingStats)
async def get_user_betting_stats(user_id: str):
    """Get comprehensive betting statistics for a user"""
    try:
        stats = await paper_betting_service.get_betting_stats(user_id)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

@router.get("/leaderboard", response_model=List[Leaderboard])
async def get_leaderboard(
    limit: int = 10,
    sort_by: str = "total_winnings"  # total_winnings, win_rate, roi
):
    """Get leaderboard of top performers"""
    try:
        valid_sorts = ["total_winnings", "win_rate", "roi"]
        if sort_by not in valid_sorts:
            raise HTTPException(status_code=400, detail=f"sort_by must be one of: {valid_sorts}")
        
        leaderboard = await paper_betting_service.get_leaderboard(limit, sort_by)
        return leaderboard
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching leaderboard: {str(e)}")

# Utility Endpoints
@router.get("/prop-types/prizepicks")
async def get_prizepicks_prop_types():
    """Get all available PrizePicks prop types with descriptions"""
    return {
        "prop_types": [
            {
                "value": PropType.POINTS.value,
                "display_name": "Points (Pts)",
                "description": "Total points scored by the player"
            },
            {
                "value": PropType.REBOUNDS.value,
                "display_name": "Rebounds (Reb)",
                "description": "Total rebounds (offensive + defensive)"
            },
            {
                "value": PropType.ASSISTS.value,
                "display_name": "Assists (Asts)",
                "description": "Total assists by the player"
            },
            {
                "value": PropType.THREES_MADE.value,
                "display_name": "3-PT Made",
                "description": "Three-point field goals made"
            },
            {
                "value": PropType.STEALS.value,
                "display_name": "Steals (Stls)",
                "description": "Steals by the player"
            },
            {
                "value": PropType.BLOCKS.value,
                "display_name": "Blocked Shots (Blks)",
                "description": "Blocked shots by the player"
            },
            {
                "value": PropType.TURNOVERS.value,
                "display_name": "Turnovers",
                "description": "Turnovers committed by the player"
            },
            {
                "value": PropType.FANTASY_SCORE.value,
                "display_name": "Fantasy Score",
                "description": "PrizePicks fantasy points (1pt=1, 1reb=1.2, 1ast=1.5, 1stl=3, 1blk=3, 1to=-1)"
            },
            {
                "value": PropType.FREE_THROWS_MADE.value,
                "display_name": "Free Throws Made",
                "description": "Free throw field goals made"
            },
            {
                "value": PropType.QUARTERS_WITH_STAT.value,
                "display_name": "Quarters/Halves with [x] Achievements",
                "description": "Number of quarters/halves achieving a statistical milestone"
            }
        ]
    }

@router.get("/betting-config")
async def get_betting_configuration():
    """Get current betting system configuration"""
    return {
        "starting_balance": 10000.0,
        "default_odds": 1.9,
        "max_bet_amount": 1000.0,
        "min_bet_amount": 1.0,
        "currency": "USD",
        "bet_types": [
            {"value": BetType.OVER.value, "display_name": "Over"},
            {"value": BetType.UNDER.value, "display_name": "Under"}
        ],
        "fantasy_scoring": {
            "points": 1.0,
            "rebounds": 1.2,
            "assists": 1.5,
            "steals": 3.0,
            "blocks": 3.0,
            "turnovers": -1.0
        }
    }


@router.post("/users/{user_id}/bets/preview-with-simulation")
async def preview_bet_with_simulation(user_id: str, bet_request: PlaceBetRequest):
    """
    🎲 Preview a bet before placing it - WITH SIMULATION
    
    This endpoint:
    1. Checks if you have enough balance
    2. Simulates the bet 50 times to show your chances
    3. Gives you win probability and expected value
    4. Recommends whether to place the bet
    
    Perfect for making informed decisions!
    """
    from app.services.nba_stats import nba_stats_service
    from app.services.game_simulator import game_simulator
    
    try:
        # Check user account
        user = await paper_betting_service.get_user_account(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check balance
        if user.virtual_balance < bet_request.wager_amount:
            return {
                "can_place": False,
                "reason": f"Insufficient balance. You have ${user.virtual_balance:.2f}, need ${bet_request.wager_amount:.2f}",
                "current_balance": user.virtual_balance
            }
        
        # Get player data for simulation
        player_info = await nba_stats_service.get_player_info(bet_request.player_name)
        if not player_info:
            raise HTTPException(status_code=404, detail=f"Player '{bet_request.player_name}' not found")
        
        recent_games = await nba_stats_service.get_player_game_log(player_info.player_id, last_n_games=10)
        season_averages = await nba_stats_service.get_player_season_averages(player_info.player_id)
        
        if not season_averages:
            raise HTTPException(status_code=404, detail="Could not fetch player season averages")
        
        # Run simulation
        sim_result = game_simulator.simulate_bet_outcome(
            player_info=player_info,
            season_averages=season_averages,
            recent_games=recent_games,
            prop_type=bet_request.prop_type,
            line=bet_request.line_value,
            bet_type=bet_request.bet_type,
            num_simulations=50  # Quick simulation
        )
        
        # Calculate potential payout
        potential_payout = bet_request.wager_amount * 1.9  # Default odds
        profit = potential_payout - bet_request.wager_amount
        
        # Calculate expected value (EV)
        win_prob = sim_result["win_probability"]
        expected_value = (win_prob * profit) - ((1 - win_prob) * bet_request.wager_amount)
        
        # Generate recommendation
        if win_prob >= 0.60:
            recommendation = "✅ STRONG PLAY - High confidence bet"
            should_place = True
        elif win_prob >= 0.55:
            recommendation = "✔️ GOOD BET - Slight edge in your favor"
            should_place = True
        elif win_prob >= 0.48:
            recommendation = "⚠️ COIN FLIP - Very close, proceed with caution"
            should_place = False
        else:
            recommendation = "❌ AVOID - Better opportunities elsewhere"
            should_place = False
        
        return {
            "can_place": True,
            "should_place": should_place,
            "bet_details": {
                "player": player_info.full_name,
                "prop": f"{bet_request.prop_type.value.replace('_', ' ').title()}",
                "line": bet_request.line_value,
                "bet_type": bet_request.bet_type.value.upper(),
                "wager": bet_request.wager_amount,
                "potential_payout": round(potential_payout, 2),
                "potential_profit": round(profit, 2)
            },
            "simulation_results": {
                "win_probability": f"{int(win_prob * 100)}%",
                "expected_value": round(expected_value, 2),
                "expected_result": sim_result["expected_value"],
                "confidence_level": sim_result["confidence_level"],
                "percentage_over": sim_result["percentage_over"],
                "percentage_under": sim_result["percentage_under"]
            },
            "recommendation": recommendation,
            "balance_after_win": round(user.virtual_balance + profit, 2),
            "balance_after_loss": round(user.virtual_balance - bet_request.wager_amount, 2),
            "current_balance": user.virtual_balance
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error previewing bet: {str(e)}")