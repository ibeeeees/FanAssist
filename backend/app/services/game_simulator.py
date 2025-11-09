"""
Game Simulation Service - Simulates NBA games and player performances
"""
import random
import numpy as np
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime, timedelta
from app.models import (
    GameStats, SeasonAverages, PropType, BetType, PlayerInfo
)
import logging

logger = logging.getLogger(__name__)


class GameSimulator:
    """
    Simulates NBA games with realistic player performances based on:
    - Season averages
    - Recent form (last 5-10 games)
    - Variance and randomness
    - Position-based tendencies
    """
    
    def __init__(self):
        # Variance factors by stat type (standard deviation as % of average)
        self.stat_variance = {
            PropType.POINTS: 0.25,  # 25% variance
            PropType.REBOUNDS: 0.30,
            PropType.ASSISTS: 0.35,
            PropType.STEALS: 0.50,
            PropType.BLOCKS: 0.50,
            PropType.THREES_MADE: 0.40,
            PropType.TURNOVERS: 0.40,
            PropType.FREE_THROWS_MADE: 0.35,
        }
        
        # Hot/cold streak modifiers
        self.streak_modifiers = {
            "hot": 1.15,      # 15% boost
            "warm": 1.08,     # 8% boost
            "normal": 1.0,    # No change
            "cold": 0.92,     # 8% decrease
            "ice_cold": 0.85  # 15% decrease
        }
    
    def simulate_player_game(
        self,
        player_info: PlayerInfo,
        season_averages: SeasonAverages,
        recent_games: List[GameStats],
        opponent: Optional[str] = None,
        is_home: bool = True
    ) -> GameStats:
        """
        Simulate a single game for a player
        
        Returns a GameStats object with simulated performance
        """
        try:
            # Analyze recent form
            form_assessment = self._assess_player_form(recent_games)
            streak_modifier = self.streak_modifiers.get(form_assessment, 1.0)
            
            # Home court advantage (small boost)
            home_modifier = 1.05 if is_home else 0.98
            
            # Combined modifier
            total_modifier = streak_modifier * home_modifier
            
            # Simulate each stat
            simulated_stats = {
                "points": self._simulate_stat(
                    season_averages.points_per_game,
                    recent_games,
                    "points",
                    total_modifier,
                    PropType.POINTS
                ),
                "rebounds": self._simulate_stat(
                    season_averages.rebounds_per_game,
                    recent_games,
                    "rebounds",
                    total_modifier,
                    PropType.REBOUNDS
                ),
                "assists": self._simulate_stat(
                    season_averages.assists_per_game,
                    recent_games,
                    "assists",
                    total_modifier,
                    PropType.ASSISTS
                ),
                "steals": self._simulate_stat(
                    season_averages.steals_per_game,
                    recent_games,
                    "steals",
                    total_modifier,
                    PropType.STEALS
                ),
                "blocks": self._simulate_stat(
                    season_averages.blocks_per_game,
                    recent_games,
                    "blocks",
                    total_modifier,
                    PropType.BLOCKS
                ),
                "turnovers": self._simulate_stat(
                    season_averages.turnovers_per_game,
                    recent_games,
                    "turnovers",
                    total_modifier,
                    PropType.TURNOVERS
                ),
            }
            
            # Simulate shooting stats
            fg_pct = season_averages.field_goal_percentage
            three_pt_pct = season_averages.three_point_percentage
            ft_pct = season_averages.free_throw_percentage
            
            # Estimate attempts based on points and percentages
            points = simulated_stats["points"]
            
            # Rough estimation of shot distribution
            estimated_fta = max(0, int(random.gauss(points * 0.25, 2)))
            simulated_stats["free_throws_made"] = int(estimated_fta * ft_pct)
            simulated_stats["free_throws_attempted"] = estimated_fta
            
            # Points from free throws
            ft_points = simulated_stats["free_throws_made"]
            field_goal_points = points - ft_points
            
            # Estimate 3-pointers (varies by position/player style)
            avg_threes_per_game = self._estimate_threes_per_game(recent_games)
            three_pt_made = max(0, int(random.gauss(avg_threes_per_game * total_modifier, avg_threes_per_game * 0.4)))
            three_pt_attempted = int(three_pt_made / three_pt_pct) if three_pt_pct > 0 and three_pt_made > 0 else three_pt_made * 3
            
            simulated_stats["three_pointers_made"] = three_pt_made
            simulated_stats["three_pointers_attempted"] = three_pt_attempted
            
            # Calculate 2-pointers
            two_pt_points = field_goal_points - (three_pt_made * 3)
            two_pt_made = max(0, two_pt_points // 2)
            two_pt_attempted = int(two_pt_made / fg_pct) if fg_pct > 0 else two_pt_made * 2
            
            simulated_stats["field_goals_made"] = two_pt_made + three_pt_made
            simulated_stats["field_goals_attempted"] = two_pt_attempted + three_pt_attempted
            
            # Minutes played (usually between 28-38 for starters)
            simulated_stats["minutes_played"] = random.gauss(
                season_averages.minutes_per_game,
                3.0
            )
            
            # Plus/minus (somewhat random but correlated with good stats)
            performance_score = (
                simulated_stats["points"] * 0.5 +
                simulated_stats["rebounds"] * 0.3 +
                simulated_stats["assists"] * 0.3 +
                simulated_stats["steals"] * 0.5 +
                simulated_stats["blocks"] * 0.5 -
                simulated_stats["turnovers"] * 0.5
            )
            simulated_stats["plus_minus"] = int(random.gauss(performance_score * 0.3, 8))
            
            # Create simulated game
            game_date = datetime.now() + timedelta(days=1)  # Future game
            
            simulated_game = GameStats(
                game_id=f"SIM_{player_info.player_id}_{game_date.strftime('%Y%m%d')}",
                player_id=player_info.player_id,
                game_date=game_date,
                opponent=opponent or "TBD",
                is_home=is_home,
                **simulated_stats
            )
            
            # Calculate fantasy score
            simulated_game.fantasy_score = simulated_game.calculate_fantasy_score()
            
            logger.info(f"Simulated game for {player_info.full_name}: {simulated_stats['points']} pts, "
                       f"{simulated_stats['rebounds']} reb, {simulated_stats['assists']} ast")
            
            return simulated_game
            
        except Exception as e:
            logger.error(f"Error simulating game: {e}")
            raise
    
    def simulate_multiple_games(
        self,
        player_info: PlayerInfo,
        season_averages: SeasonAverages,
        recent_games: List[GameStats],
        num_simulations: int = 100,
        opponent: Optional[str] = None,
        is_home: bool = True
    ) -> List[GameStats]:
        """
        Run multiple simulations to get a distribution of outcomes
        """
        simulations = []
        for _ in range(num_simulations):
            sim_game = self.simulate_player_game(
                player_info,
                season_averages,
                recent_games,
                opponent,
                is_home
            )
            simulations.append(sim_game)
        
        return simulations
    
    def simulate_bet_outcome(
        self,
        player_info: PlayerInfo,
        season_averages: SeasonAverages,
        recent_games: List[GameStats],
        prop_type: PropType,
        line: float,
        bet_type: BetType,
        num_simulations: int = 100
    ) -> Dict[str, Any]:
        """
        Simulate bet outcomes and return win probability
        """
        simulations = self.simulate_multiple_games(
            player_info,
            season_averages,
            recent_games,
            num_simulations=num_simulations
        )
        
        # Extract the relevant stat from each simulation
        stat_values = []
        for sim in simulations:
            value = self._get_stat_value(sim, prop_type)
            if value is not None:
                stat_values.append(value)
        
        # Calculate win probability
        if bet_type == BetType.OVER:
            wins = sum(1 for v in stat_values if v > line)
        else:  # UNDER
            wins = sum(1 for v in stat_values if v < line)
        
        win_probability = wins / len(stat_values) if stat_values else 0
        
        # Calculate expected value
        avg_result = np.mean(stat_values) if stat_values else 0
        median_result = np.median(stat_values) if stat_values else 0
        std_dev = np.std(stat_values) if stat_values else 0
        
        return {
            "win_probability": round(win_probability, 3),
            "expected_value": round(avg_result, 2),
            "median_result": round(median_result, 2),
            "standard_deviation": round(std_dev, 2),
            "line": line,
            "bet_type": bet_type.value,
            "simulations_run": len(stat_values),
            "percentage_over": round(sum(1 for v in stat_values if v > line) / len(stat_values) * 100, 1) if stat_values else 0,
            "percentage_under": round(sum(1 for v in stat_values if v < line) / len(stat_values) * 100, 1) if stat_values else 0,
            "confidence_level": self._calculate_confidence(win_probability)
        }
    
    def simulate_multi_leg_ticket(
        self,
        legs: List[Dict[str, Any]],
        num_simulations: int = 100
    ) -> Dict[str, Any]:
        """
        Simulate a multi-leg parlay ticket
        
        Args:
            legs: List of dicts with player_info, season_averages, recent_games, prop_type, line, bet_type
            num_simulations: Number of times to simulate the entire ticket
        """
        ticket_wins = 0
        leg_results = {i: {"wins": 0, "losses": 0} for i in range(len(legs))}
        
        for _ in range(num_simulations):
            all_legs_hit = True
            
            for idx, leg in enumerate(legs):
                # Simulate one game for this leg
                sim_game = self.simulate_player_game(
                    leg["player_info"],
                    leg["season_averages"],
                    leg["recent_games"]
                )
                
                # Check if this leg hits
                actual_value = self._get_stat_value(sim_game, leg["prop_type"])
                
                if actual_value is None:
                    all_legs_hit = False
                    break
                
                if leg["bet_type"] == BetType.OVER:
                    leg_hits = actual_value > leg["line"]
                else:
                    leg_hits = actual_value < leg["line"]
                
                if leg_hits:
                    leg_results[idx]["wins"] += 1
                else:
                    leg_results[idx]["losses"] += 1
                    all_legs_hit = False
            
            if all_legs_hit:
                ticket_wins += 1
        
        # Calculate individual leg probabilities
        leg_probabilities = []
        for idx in range(len(legs)):
            win_prob = leg_results[idx]["wins"] / num_simulations
            leg_probabilities.append({
                "leg_number": idx + 1,
                "player": legs[idx]["player_info"].full_name,
                "prop": f"{legs[idx]['prop_type'].value.replace('_', ' ').title()}",
                "line": legs[idx]["line"],
                "bet_type": legs[idx]["bet_type"].value,
                "win_probability": round(win_prob, 3),
                "hit_rate": f"{round(win_prob * 100, 1)}%"
            })
        
        ticket_win_probability = ticket_wins / num_simulations
        
        return {
            "ticket_win_probability": round(ticket_win_probability, 3),
            "ticket_hit_rate": f"{round(ticket_win_probability * 100, 1)}%",
            "expected_wins_per_100": int(ticket_win_probability * 100),
            "leg_probabilities": leg_probabilities,
            "total_legs": len(legs),
            "simulations_run": num_simulations,
            "recommendation": self._get_ticket_recommendation(ticket_win_probability, len(legs))
        }
    
    def _simulate_stat(
        self,
        season_avg: float,
        recent_games: List[GameStats],
        stat_name: str,
        modifier: float,
        prop_type: PropType
    ) -> int:
        """Simulate a single stat with realistic variance"""
        # Get recent average
        recent_values = [
            getattr(game, stat_name) 
            for game in recent_games[-5:] 
            if getattr(game, stat_name) is not None
        ]
        
        # Weight recent performance more heavily
        if recent_values:
            recent_avg = np.mean(recent_values)
            # 60% recent, 40% season
            weighted_avg = (recent_avg * 0.6 + season_avg * 0.4)
        else:
            weighted_avg = season_avg
        
        # Apply modifier
        expected_value = weighted_avg * modifier
        
        # Handle edge case: if expected value is too low, return 0
        if expected_value < 0.1:
            return 0
        
        # Add variance
        variance = self.stat_variance.get(prop_type, 0.3)
        std_dev = expected_value * variance
        
        # Ensure std_dev is not too small to avoid division issues
        if std_dev < 0.01:
            std_dev = 0.01
        
        # Use gamma distribution for realistic positive skew
        # Protect against division by zero
        try:
            shape = (expected_value / std_dev) ** 2
            scale = std_dev ** 2 / expected_value
            
            # Validate shape and scale parameters
            if shape <= 0 or scale <= 0 or np.isnan(shape) or np.isnan(scale):
                # Fall back to simple rounding if parameters invalid
                return max(0, int(round(expected_value)))
            
            simulated_value = np.random.gamma(shape=shape, scale=scale)
        except (ValueError, FloatingPointError):
            # Fallback if gamma fails
            simulated_value = expected_value
        
        return max(0, int(round(simulated_value)))
    
    def _assess_player_form(self, recent_games: List[GameStats]) -> str:
        """Assess if player is hot, cold, or normal based on recent games"""
        if len(recent_games) < 3:
            return "normal"
        
        # Look at last 3-5 games
        last_games = recent_games[-5:]
        
        # Calculate trend in points (simplified form assessment)
        points = [g.points for g in last_games if g.points is not None]
        
        if len(points) < 3:
            return "normal"
        
        # Simple trend: compare first half to second half
        first_half = np.mean(points[:len(points)//2])
        second_half = np.mean(points[len(points)//2:])
        
        change_pct = (second_half - first_half) / first_half if first_half > 0 else 0
        
        if change_pct > 0.15:
            return "hot"
        elif change_pct > 0.05:
            return "warm"
        elif change_pct < -0.15:
            return "ice_cold"
        elif change_pct < -0.05:
            return "cold"
        else:
            return "normal"
    
    def _estimate_threes_per_game(self, recent_games: List[GameStats]) -> float:
        """Estimate 3-pointers per game from recent performance"""
        threes = [
            g.three_pointers_made 
            for g in recent_games[-10:] 
            if g.three_pointers_made is not None
        ]
        
        if threes:
            return np.mean(threes)
        return 2.0  # Default estimate
    
    def _get_stat_value(self, game: GameStats, prop_type: PropType) -> Optional[float]:
        """Extract the stat value for a given prop type"""
        stat_map = {
            PropType.POINTS: game.points,
            PropType.REBOUNDS: game.rebounds,
            PropType.ASSISTS: game.assists,
            PropType.STEALS: game.steals,
            PropType.BLOCKS: game.blocks,
            PropType.THREES_MADE: game.three_pointers_made,
            PropType.TURNOVERS: game.turnovers,
            PropType.FREE_THROWS_MADE: game.free_throws_made,
            PropType.FANTASY_SCORE: game.fantasy_score,
        }
        
        return stat_map.get(prop_type)
    
    def _calculate_confidence(self, win_probability: float) -> str:
        """Convert win probability to confidence level"""
        if win_probability >= 0.65:
            return "High"
        elif win_probability >= 0.55:
            return "Medium"
        elif win_probability >= 0.45:
            return "Low"
        else:
            return "Very Low"
    
    def _get_ticket_recommendation(self, win_prob: float, num_legs: int) -> str:
        """Get recommendation for multi-leg ticket"""
        if num_legs >= 5:
            if win_prob >= 0.08:
                return "Favorable - Good odds for a 5+ leg parlay"
            elif win_prob >= 0.05:
                return "Moderate - Decent chance but risky"
            else:
                return "Avoid - Low probability of hitting all legs"
        elif num_legs >= 3:
            if win_prob >= 0.20:
                return "Strong Play - Good value"
            elif win_prob >= 0.15:
                return "Moderate - Reasonable shot"
            else:
                return "Risky - Consider fewer legs"
        else:  # 2 legs
            if win_prob >= 0.35:
                return "Excellent - High confidence"
            elif win_prob >= 0.25:
                return "Good - Solid play"
            else:
                return "Risky - Low confidence"


# Singleton instance
game_simulator = GameSimulator()
