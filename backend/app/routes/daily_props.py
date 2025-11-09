"""
Daily Props API - Get popular players with PrizePicks lines and bet with simulations
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, validator
from app.services.popular_players import popular_players_service
from app.services.paper_betting import PaperBettingService
from app.services.game_simulator import game_simulator
from app.services.nba_stats import NBAStatsService
from datetime import datetime

router = APIRouter(prefix="/api/daily-props", tags=["daily-props"])

# Initialize services
paper_betting_service = PaperBettingService()
nba_stats_service = NBAStatsService()


# ============================================================================
# ODDS AND PAYOUT CALCULATION SYSTEM
# ============================================================================

def calculate_realistic_odds(probability: float, bet_mode: str = "standard", power_multiplier: float = 1.0) -> float:
    """
    Calculate realistic odds based on win probability
    
    Args:
        probability: Win probability (0.0 to 1.0)
        bet_mode: "standard", "flex", or "power_play"
        power_multiplier: Multiplier for power play (2x, 3x, 5x, 10x)
    
    Returns:
        Payout multiplier (e.g., 1.91 means bet $100 to win $191)
    
    Examples:
        - 75% win probability → ~1.3x payout (low risk, low reward)
        - 50% win probability → ~2.0x payout (fair odds)
        - 30% win probability → ~3.3x payout (higher risk, higher reward)
        - Power Play 10x on 30% probability → Much lower effective probability
    """
    # Adjust probability for power play (reduces win chance)
    if bet_mode == "power_play" and power_multiplier > 1:
        # Power play reduces your effective win probability
        # 2x power = ~15% reduction, 10x power = ~40% reduction
        reduction_factor = 1.0 - (0.05 * (power_multiplier - 1))
        probability = max(0.1, probability * reduction_factor)
    
    # Calculate fair odds (inverse of probability)
    # Add house edge of ~10% (typical for sportsbooks)
    house_edge = 0.90
    fair_odds = (1.0 / probability) * house_edge
    
    # For power play, multiply the payout
    if bet_mode == "power_play":
        fair_odds *= power_multiplier
    
    # Floor at 1.01x (always some payout if you win)
    return max(1.01, round(fair_odds, 2))


def calculate_parlay_odds(probabilities: List[float], num_legs: int, bet_mode: str = "standard") -> dict:
    """
    Calculate parlay odds based on individual leg probabilities
    
    Args:
        probabilities: List of individual leg win probabilities
        num_legs: Number of legs in the parlay
        bet_mode: "standard", "flex", or "power_play"
    
    Returns:
        Dictionary with odds, combined_probability, and flex information
    """
    # Calculate combined probability for all legs winning
    combined_prob = 1.0
    for prob in probabilities:
        combined_prob *= prob
    
    result = {
        "combined_probability": round(combined_prob, 4),
        "num_legs": num_legs,
        "individual_probabilities": [round(p, 3) for p in probabilities]
    }
    
    if bet_mode == "flex":
        # Flex pick: Can miss one leg and still win reduced payout
        # Calculate probability of getting (n-1) correct
        if num_legs >= 3:
            # Probability of getting exactly (n-1) legs correct
            # This is more complex, but roughly: combined_prob / avg_leg_prob
            avg_prob = sum(probabilities) / len(probabilities)
            flex_prob = combined_prob + (combined_prob / avg_prob) * (1 - avg_prob) * num_legs
            flex_prob = min(0.95, flex_prob)  # Cap at 95%
            
            # Flex odds are lower than full parlay but higher than single bet
            flex_multiplier = calculate_realistic_odds(flex_prob, "standard", 1.0) * 0.7
            
            result["flex_mode"] = True
            result["flex_probability"] = round(flex_prob, 4)
            result["full_win_multiplier"] = calculate_realistic_odds(combined_prob, "standard", 1.0)
            result["flex_win_multiplier"] = round(flex_multiplier, 2)
            result["flex_rules"] = f"Win {num_legs-1} out of {num_legs} picks for reduced payout"
        else:
            # Need at least 3 legs for flex
            result["flex_mode"] = False
            result["flex_error"] = "Flex picks require at least 3 legs"
            result["standard_multiplier"] = calculate_realistic_odds(combined_prob, "standard", 1.0)
    else:
        # Standard parlay
        result["flex_mode"] = False
        result["standard_multiplier"] = calculate_realistic_odds(combined_prob, "standard", 1.0)
    
    return result


def calculate_power_play_adjusted_probability(base_prob: float, multiplier: float) -> float:
    """
    Power Play reduces your win probability but increases payout
    
    Power Play Tiers:
    - 2x: ~10% probability reduction
    - 3x: ~20% probability reduction  
    - 5x: ~30% probability reduction
    - 10x: ~40% probability reduction
    """
    reduction_map = {
        2.0: 0.90,
        3.0: 0.80,
        5.0: 0.70,
        10.0: 0.60
    }
    reduction = reduction_map.get(multiplier, 0.90)
    return max(0.05, base_prob * reduction)


class PropBetLeg(BaseModel):
    """
    A single leg in a parlay (no individual wager)
    
    Supported prop_types:
    - points: Player points scored
    - rebounds: Player rebounds
    - assists: Player assists
    - steals: Player steals
    - turnovers: Player turnovers (bet UNDER is good)
    - threes_made: 3-pointers made
    - pra: Points + Rebounds + Assists
    - pr: Points + Rebounds
    - pa: Points + Assists
    
    Lines must be whole numbers or .5 increments (e.g., 25.0, 25.5, 26.0)
    """
    player_name: str
    prop_type: str  # points, rebounds, assists, steals, turnovers, threes_made, pra, pr, pa
    line: float
    pick: str  # OVER or UNDER
    
    @validator('line')
    def validate_line(cls, v):
        """Ensure line is a whole number or .5 increment"""
        # Check if the line is a whole number or ends in .5
        decimal_part = v - int(v)
        if decimal_part not in [0.0, 0.5]:
            raise ValueError(f'Line must be a whole number or .5 increment (e.g., 25.0, 25.5, 26.0), got {v}')
        return v
    
    @validator('pick')
    def validate_pick(cls, v):
        """Ensure pick is OVER or UNDER"""
        if v.upper() not in ['OVER', 'UNDER']:
            raise ValueError('Pick must be either OVER or UNDER')
        return v.upper()


class PropBet(BaseModel):
    """
    A single prop bet (for individual bets)
    """
    player_name: str
    prop_type: str
    line: float
    pick: str  # OVER or UNDER
    wager: float
    bet_mode: Optional[str] = "standard"  # standard, power_play
    power_play_multiplier: Optional[float] = 1.0  # 2x, 3x, 5x, 10x
    
    @validator('line')
    def validate_line(cls, v):
        """Ensure line is a whole number or .5 increment"""
        decimal_part = v - int(v)
        if decimal_part not in [0.0, 0.5]:
            raise ValueError(f'Line must be a whole number or .5 increment (e.g., 25.0, 25.5, 26.0), got {v}')
        return v


class MultiPropBet(BaseModel):
    """Multiple props in a parlay - ONE total wager for the entire ticket"""
    username: str
    bets: List[PropBetLeg]  # Changed to PropBetLeg (no individual wagers)
    total_wager: float  # Single wager for the entire parlay
    bet_mode: Optional[str] = "standard"  # standard, flex, power_play
    power_play_multiplier: Optional[float] = 1.0  # For power play parlays


class SimulationResult(BaseModel):
    """Result of simulating a bet"""
    player_name: str
    prop_type: str
    line: float
    pick: str
    simulated_value: float
    won: bool
    probability: float


@router.get("/today")
async def get_todays_props():
    """
    Get popular players with PrizePicks-style prop lines for TODAY'S games
    
    ONLY includes players who:
    - Have a game scheduled TODAY
    - Are ACTIVE (not injured/out)
    - Have played within the last 7 days
    
    Returns:
        - List of popular players (LeBron, Curry, Giannis, etc.)
        - Season averages for each stat
        - Suggested betting lines for points, rebounds, assists, combos
        - Opponent and game info
    """
    try:
        players = await popular_players_service.get_popular_players_for_today()
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "count": len(players),
            "players": players
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching today's props: {str(e)}")


@router.get("/tomorrow")
async def get_tomorrows_props():
    """
    Get popular players with PrizePicks-style prop lines for TOMORROW'S games
    
    ONLY includes players who:
    - Have a game scheduled TOMORROW
    - Are ACTIVE (not injured/out)
    - Have played within the last 7 days
    
    Returns:
        - List of popular players
        - Season averages
        - Suggested betting lines
        - Opponent and game info
    """


@router.post("/simulate-bet")
async def simulate_single_bet(bet: PropBet):
    """
    Simulate a single prop bet using the game simulator (public endpoint)
    
    Returns:
    - Simulation results (30 runs)
    - Win/loss determination
    - Probability of hitting
    - Projected stats
    """
    return await _simulate_bet_leg(bet)


async def _simulate_bet_leg(bet):
    """
    Internal function to simulate a bet leg (works with both PropBet and PropBetLeg)
    
    Returns:
    - Simulation results (30 runs)
    - Win/loss determination
    - Probability of hitting
    - Projected stats
    """
    try:
        # Validate inputs
        if not bet.player_name:
            raise HTTPException(status_code=400, detail="Player name is required")
        if not bet.prop_type:
            raise HTTPException(status_code=400, detail="Prop type is required")
        if bet.line is None:
            raise HTTPException(status_code=400, detail="Line is required")
        if not bet.pick:
            raise HTTPException(status_code=400, detail="Pick (OVER/UNDER) is required")
        
        # Find player
        player_info = await nba_stats_service.get_player_info(bet.player_name)
        if not player_info:
            raise HTTPException(status_code=404, detail=f"Player not found: {bet.player_name}")
        
        # Get player stats
        season_avg = await nba_stats_service.get_player_season_averages(player_info.player_id)
        if not season_avg:
            raise HTTPException(status_code=404, detail=f"Stats not found for {bet.player_name}")
        
        recent_games = await nba_stats_service.get_player_game_log(player_info.player_id, last_n_games=5)
        
        # Run simulation
        simulation_result = game_simulator.simulate_player_game(
            player_info=player_info,
            season_averages=season_avg,
            recent_games=recent_games,
            opponent="Unknown",  # Could enhance this
            is_home=True
        )
        
        # Get the stat value based on prop type
        prop_map = {
            "points": "points",
            "rebounds": "rebounds",
            "assists": "assists",
            "steals": "steals",
            "turnovers": "turnovers",
            "threes": "three_pointers_made",
            "threes_made": "three_pointers_made",
            "pra": None,  # Need to calculate (Points + Rebounds + Assists)
            "pr": None,   # Need to calculate (Points + Rebounds)
            "pa": None    # Need to calculate (Points + Assists)
        }
        
        # Calculate simulated value
        try:
            if bet.prop_type in ["pra", "pr", "pa"]:
                # Combo stats - sum multiple stats
                simulated_value = 0
                if "p" in bet.prop_type:
                    simulated_value += getattr(simulation_result, "points", 0)
                if "r" in bet.prop_type:
                    simulated_value += getattr(simulation_result, "rebounds", 0)
                if "a" in bet.prop_type:
                    simulated_value += getattr(simulation_result, "assists", 0)
            else:
                # Single stat
                stat_key = prop_map.get(bet.prop_type)
                if not stat_key:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Invalid prop type: {bet.prop_type}. Supported: points, rebounds, assists, steals, turnovers, threes_made, pra, pr, pa"
                    )
                simulated_value = getattr(simulation_result, stat_key, 0)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error calculating simulated value for {bet.player_name} {bet.prop_type}: {str(e)}"
            )
        
        # Determine if bet won
        if bet.pick.upper() == "OVER":
            won = simulated_value > bet.line
        else:
            won = simulated_value < bet.line
        
        # Calculate probability (simplified - would need multiple sims for accuracy)
        # For now, use the margin
        margin = abs(simulated_value - bet.line)
        if margin >= 3:
            probability = 0.75 if won else 0.25
        elif margin >= 1.5:
            probability = 0.65 if won else 0.35
        else:
            probability = 0.55 if won else 0.45
        
        # Calculate season average for this prop type
        if bet.prop_type in ["pra", "pr", "pa"]:
            # Combo stats - calculate from individual averages
            season_avg_value = 0
            if "p" in bet.prop_type:
                season_avg_value += getattr(season_avg, "points_per_game", 0)
            if "r" in bet.prop_type:
                season_avg_value += getattr(season_avg, "rebounds_per_game", 0)
            if "a" in bet.prop_type:
                season_avg_value += getattr(season_avg, "assists_per_game", 0)
        else:
            # Single stat - get from season averages
            stat_key = prop_map.get(bet.prop_type)
            if stat_key:
                # Map simulation stat name to season average property name
                season_avg_map = {
                    "points": "points_per_game",
                    "rebounds": "rebounds_per_game",
                    "assists": "assists_per_game",
                    "steals": "steals_per_game",
                    "turnovers": "turnovers_per_game",
                    "three_pointers_made": "three_point_percentage"
                }
                season_stat_key = season_avg_map.get(stat_key, stat_key)
                season_avg_value = getattr(season_avg, season_stat_key, 0)
            else:
                season_avg_value = 0
        
        return {
            "player_name": bet.player_name,
            "prop_type": bet.prop_type,
            "line": bet.line,
            "pick": bet.pick,
            "simulated_value": round(simulated_value, 1),
            "won": won,
            "probability": probability,
            "season_average": round(season_avg_value, 1),
            "simulation_details": {
                "points": round(simulation_result.points, 1),
                "rebounds": round(simulation_result.rebounds, 1),
                "assists": round(simulation_result.assists, 1),
                "three_pointers_made": round(simulation_result.three_pointers_made, 1),
                "steals": round(simulation_result.steals, 1),
                "blocks": round(simulation_result.blocks, 1),
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error simulating bet for {bet.player_name}: {str(e)}")


@router.post("/place-bet")
async def place_bet_with_simulation(bet: PropBet):
    """
    Place a bet with paper money and simulate to see if you won
    
    Supports:
    - Standard bets: Realistic odds based on win probability
    - Power Play: Boosted payouts (2x, 3x, 5x, 10x) with reduced win probability
    
    Flow:
    1. Simulate the prop
    2. Calculate realistic odds based on probability
    3. Apply Power Play adjustments if selected
    4. Determine win/loss
    5. Update balance accordingly
    6. Return full results
    """
    try:
        # First, simulate the bet
        # Simulate the bet
        simulation = await _simulate_bet_leg(bet)
        
        # Adjust probability for power play
        win_probability = simulation["probability"]
        if bet.bet_mode == "power_play" and bet.power_play_multiplier > 1:
            adjusted_prob = calculate_power_play_adjusted_probability(
                win_probability, 
                bet.power_play_multiplier
            )
            # Re-determine win/loss with adjusted probability
            import random
            simulation["won"] = random.random() < adjusted_prob
            simulation["adjusted_probability"] = adjusted_prob
            simulation["original_probability"] = win_probability
        
        # Calculate realistic odds-based payout
        odds_multiplier = calculate_realistic_odds(
            simulation.get("adjusted_probability", win_probability),
            bet.bet_mode,
            bet.power_play_multiplier
        )
        
        # Create/get user account (for demo, we'll use a default user)
        username = "demo_user"
        user = await paper_betting_service.get_user_by_username(username)
        
        if not user:
            # Create demo account
            user = await paper_betting_service.create_user_account(
                username=username,
                email="demo@fanassist.com"
            )
        
        # Check if user has enough balance
        if user.virtual_balance < bet.wager:
            raise HTTPException(
                status_code=400, 
                detail=f"Insufficient balance. Current: ${user.virtual_balance:.2f}, Needed: ${bet.wager:.2f}"
            )
        
        # Calculate payout using realistic odds
        if simulation["won"]:
            payout = bet.wager * odds_multiplier
            profit = payout - bet.wager
            new_balance = user.virtual_balance + profit
        else:
            payout = 0
            profit = -bet.wager
            new_balance = user.virtual_balance - bet.wager
        
        # Update balance
        old_balance = user.virtual_balance
        user.virtual_balance = new_balance
        
        return {
            "bet_placed": True,
            "result": simulation,
            "odds_info": {
                "win_probability": round(win_probability * 100, 1),
                "odds_multiplier": odds_multiplier,
                "bet_mode": bet.bet_mode,
                "power_play_multiplier": bet.power_play_multiplier if bet.bet_mode == "power_play" else None,
                "house_edge": "10%"
            },
            "betting_summary": {
                "username": username,
                "old_balance": round(old_balance, 2),
                "wager": bet.wager,
                "payout": round(payout, 2),
                "profit": round(profit, 2),
                "new_balance": round(new_balance, 2),
                "won": simulation["won"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error placing bet: {str(e)}")


@router.post("/place-parlay")
async def place_parlay_with_simulation(parlay: MultiPropBet):
    """
    Place a multi-leg parlay and simulate all props
    
    Betting Modes:
    - Standard: All legs must win for payout (realistic odds based on combined probability)
    - Flex Pick: Can miss 1 leg and still win reduced payout (requires 3+ legs)
    - Power Play: Boosted payouts with reduced win probability
    
    Parlay Limits:
    - Minimum: 2 legs
    - Maximum: 6 legs
    
    Realistic Odds Examples:
    - 3-leg at 60% each: ~22% combined = ~4.5x payout
    - 4-leg at 50% each: ~6% combined = ~15x payout
    - Flex 4-pick (need 3/4): ~31% combined = ~3x payout
    """
    try:
        num_legs = len(parlay.bets)
        
        # Validate parlay size
        if num_legs < 2:
            raise HTTPException(
                status_code=400,
                detail="Parlays require at least 2 legs"
            )
        
        if num_legs > 6:
            raise HTTPException(
                status_code=400,
                detail="Parlays cannot have more than 6 legs. You submitted {} legs.".format(num_legs)
            )
        
        # Simulate each bet
        simulation_results = []
        probabilities = []
        wins = []
        
        for bet in parlay.bets:
            result = await _simulate_bet_leg(bet)
            simulation_results.append(result)
            probabilities.append(result["probability"])
            wins.append(result["won"])
        
        num_wins = sum(wins)
        all_won = num_wins == num_legs
        
        # Calculate parlay odds
        odds_info = calculate_parlay_odds(
            probabilities, 
            num_legs, 
            parlay.bet_mode
        )
        
        # Get or create user
        user = await paper_betting_service.get_user_by_username(parlay.username)
        if not user:
            user = await paper_betting_service.create_user_account(
                username=parlay.username,
                email=f"{parlay.username}@fanassist.com"
            )
        
        # Check balance
        if user.virtual_balance < parlay.total_wager:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient balance. Current: ${user.virtual_balance:.2f}, Needed: ${parlay.total_wager:.2f}"
            )
        
        # Determine payout based on bet mode
        payout = 0
        multiplier = 0
        bet_result = "loss"
        
        if parlay.bet_mode == "flex":
            # Flex pick: Can miss one leg
            if num_legs < 3:
                raise HTTPException(
                    status_code=400,
                    detail="Flex picks require at least 3 legs"
                )
            
            if all_won:
                # Full win: Use full multiplier
                multiplier = odds_info["full_win_multiplier"]
                payout = parlay.total_wager * multiplier
                bet_result = "full_win"
            elif num_wins >= (num_legs - 1):
                # Flex win: Won n-1 legs
                multiplier = odds_info["flex_win_multiplier"]
                payout = parlay.total_wager * multiplier
                bet_result = "flex_win"
            else:
                # Lost (missed more than 1)
                payout = 0
                bet_result = "loss"
                
        elif parlay.bet_mode == "power_play":
            # Power play: Higher multiplier but lower win chance
            if all_won:
                base_multiplier = odds_info["standard_multiplier"]
                multiplier = base_multiplier * parlay.power_play_multiplier
                payout = parlay.total_wager * multiplier
                bet_result = "win"
            else:
                payout = 0
                bet_result = "loss"
                
        else:
            # Standard: All legs must win
            if all_won:
                multiplier = odds_info["standard_multiplier"]
                payout = parlay.total_wager * multiplier
                bet_result = "win"
            else:
                payout = 0
                bet_result = "loss"
        
        # Calculate profit/loss
        profit = payout - parlay.total_wager if payout > 0 else -parlay.total_wager
        new_balance = user.virtual_balance + profit
        
        # Update balance
        old_balance = user.virtual_balance
        user.virtual_balance = new_balance
        
        # Build comprehensive response
        response = {
            "parlay_placed": True,
            "bet_mode": parlay.bet_mode,
            "bet_result": bet_result,
            "num_legs": num_legs,
            "num_wins": num_wins,
            "all_won": all_won,
            "total_wager": parlay.total_wager,
            "potential_payout": round(parlay.total_wager * odds_info.get("standard_multiplier", 0), 2),
            "odds_multiplier": round(odds_info.get("standard_multiplier", 0), 2),
            "legs": simulation_results,
            "bet_legs": simulation_results,  # Alias for compatibility
            "odds_info": {
                **odds_info,
                "actual_multiplier": round(multiplier, 2) if multiplier > 0 else 0
            },
            "betting_summary": {
                "username": parlay.username,
                "old_balance": round(old_balance, 2),
                "wager": parlay.total_wager,
                "payout": round(payout, 2),
                "profit": round(profit, 2),
                "new_balance": round(new_balance, 2),
                "won": payout > 0
            },
            "simulated_outcome": {
                "parlay_won": payout > 0,
                "is_flex_win": bet_result == "flex_win",
                "legs_hit": num_wins,
                "legs_needed": num_legs,
                "actual_payout": round(payout, 2),
                "new_balance": round(new_balance, 2)
            }
        }
        
        # Add mode-specific fields
        if parlay.bet_mode == "flex":
            response["flex_payout"] = round(parlay.total_wager * odds_info.get("flex_win_multiplier", 0), 2)
        
        if parlay.bet_mode == "power_play":
            response["power_play_multiplier"] = parlay.power_play_multiplier
            response["original_payout_before_power"] = round(odds_info.get("standard_multiplier", 0), 2)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error placing parlay: {str(e)}")


@router.get("/balance/{username}")
async def get_user_balance(username: str):
    """Get current paper money balance for a user"""
    try:
        user = await paper_betting_service.get_user_by_username(username)
        
        if not user:
            # Create new user
            user = await paper_betting_service.create_user_account(
                username=username,
                email=f"{username}@fanassist.com"
            )
        
        return {
            "username": user.username,
            "balance": round(user.virtual_balance, 2),
            "starting_balance": 10000.0,
            "profit_loss": round(user.virtual_balance - 10000.0, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting balance: {str(e)}")


@router.post("/reset-balance/{username}")
async def reset_user_balance(username: str):
    """Reset user's paper money balance to starting amount"""
    try:
        user = await paper_betting_service.get_user_by_username(username)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        old_balance = user.virtual_balance
        user.virtual_balance = 10000.0
        
        return {
            "username": username,
            "old_balance": round(old_balance, 2),
            "new_balance": 10000.0,
            "message": "Balance reset successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting balance: {str(e)}")
