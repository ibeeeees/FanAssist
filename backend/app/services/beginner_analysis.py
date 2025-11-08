from typing import List, Dict, Optional, Any
from datetime import datetime
from app.models import PlayerInfo, GameStats, SeasonAverages, PropType
from app.services.nba_stats import nba_stats_service
import statistics

class BeginnerAnalysisService:
    """
    Service to provide beginner-friendly basketball analysis with detailed explanations
    """
    
    def __init__(self):
        self.basketball_terms = {
            "points": {
                "description": "Total points scored by shooting field goals, three-pointers, and free throws",
                "good_range": "15+ points per game is solid, 20+ is very good, 25+ is elite",
                "factors": ["Shot attempts", "Field goal %", "Free throw attempts", "Playing time"]
            },
            "rebounds": {
                "description": "Grabbing the ball after a missed shot (offensive or defensive)",
                "good_range": "6+ rebounds is solid for guards, 8+ for forwards, 10+ for centers",
                "factors": ["Height advantage", "Playing time", "Team pace", "Opponent missed shots"]
            },
            "assists": {
                "description": "Passes that directly lead to a teammate scoring",
                "good_range": "3+ assists is good for non-guards, 5+ for guards, 8+ is elite",
                "factors": ["Ball handling role", "Team offense", "Teammate shooting", "Playing time"]
            },
            "steals": {
                "description": "Taking the ball away from the opponent",
                "good_range": "1+ steal per game is solid, 1.5+ is very good, 2+ is elite",
                "factors": ["Defensive pressure", "Opponent turnovers", "Playing style", "Game pace"]
            },
            "blocks": {
                "description": "Preventing an opponent's shot from going in by deflecting it",
                "good_range": "0.5+ blocks for guards, 1+ for forwards, 1.5+ for centers is good",
                "factors": ["Height", "Defensive positioning", "Opponent shot attempts", "Playing time"]
            },
            "turnovers": {
                "description": "Losing possession of the ball to the opponent (bad for player)",
                "good_range": "Under 3 turnovers is good, under 2 is excellent",
                "factors": ["Ball handling", "Pressure defense", "Usage rate", "Playing style"]
            },
            "threes_made": {
                "description": "Successful shots from beyond the three-point line",
                "good_range": "1+ three-pointers is decent, 2+ is good, 3+ is excellent",
                "factors": ["Three-point attempts", "Shooting %", "Role in offense", "Game situation"]
            },
            "free_throws_made": {
                "description": "Uncontested shots worth 1 point each after fouls",
                "good_range": "2+ free throws is decent, 4+ is good, depends on playing style",
                "factors": ["Aggressive play", "Foul calls", "Free throw %", "Game situation"]
            },
            "fantasy_score": {
                "description": "Composite score: 1pt=1, 1reb=1.2, 1ast=1.5, 1stl=3, 1blk=3, 1to=-1",
                "good_range": "25+ fantasy points is decent, 35+ is good, 45+ is excellent",
                "factors": ["All-around production", "Playing time", "Team role", "Game flow"]
            }
        }
    
    async def analyze_last_5_games(self, player_name: str) -> Dict[str, Any]:
        """
        Analyze player's last 5 games with beginner-friendly explanations
        """
        # Get player info
        player_info = await nba_stats_service.get_player_info(player_name)
        if not player_info:
            raise ValueError(f"Player '{player_name}' not found")
        
        # Get last 5 games
        recent_games = await nba_stats_service.get_player_game_log(player_info.player_id, last_n_games=5)
        if not recent_games:
            raise ValueError(f"No recent games found for {player_name}")
        
        # Get season averages for comparison
        season_averages = await nba_stats_service.get_player_season_averages(player_info.player_id)
        
        # Calculate last 5 averages
        last_5_stats = self._calculate_last_5_averages(recent_games)
        
        # Generate analysis for each stat category
        stat_analysis = {}
        for prop_type in PropType:
            if prop_type == PropType.QUARTERS_WITH_STAT:
                continue  # Skip this complex prop for now
            
            analysis = self._analyze_stat_performance(
                prop_type, last_5_stats, season_averages, recent_games
            )
            stat_analysis[prop_type.value] = analysis
        
        return {
            "player_info": player_info,
            "last_5_games": recent_games,
            "last_5_averages": last_5_stats,
            "season_averages": season_averages,
            "stat_analysis": stat_analysis,
            "overall_form": self._assess_overall_form(last_5_stats, season_averages),
            "beginner_tips": self._generate_beginner_tips(player_info, last_5_stats, season_averages)
        }
    
    def _calculate_last_5_averages(self, games: List[GameStats]) -> Dict[str, float]:
        """Calculate averages for last 5 games"""
        if not games:
            return {}
        
        stats = {
            "games": len(games),
            "minutes": self._safe_average([g.minutes_played for g in games]),
            "points": self._safe_average([g.points for g in games]),
            "rebounds": self._safe_average([g.rebounds for g in games]),
            "assists": self._safe_average([g.assists for g in games]),
            "steals": self._safe_average([g.steals for g in games]),
            "blocks": self._safe_average([g.blocks for g in games]),
            "turnovers": self._safe_average([g.turnovers for g in games]),
            "threes_made": self._safe_average([g.three_pointers_made for g in games]),
            "free_throws_made": self._safe_average([g.free_throws_made for g in games]),
            "field_goal_pct": self._calculate_fg_percentage(games),
            "fantasy_score": self._safe_average([g.fantasy_score for g in games if g.fantasy_score])
        }
        
        return stats
    
    def _safe_average(self, values: List[Optional[float]]) -> float:
        """Calculate average safely handling None values"""
        valid_values = [v for v in values if v is not None]
        return statistics.mean(valid_values) if valid_values else 0.0
    
    def _calculate_fg_percentage(self, games: List[GameStats]) -> float:
        """Calculate field goal percentage over last games"""
        total_made = sum(g.field_goals_made or 0 for g in games)
        total_attempted = sum(g.field_goals_attempted or 0 for g in games)
        return (total_made / total_attempted * 100) if total_attempted > 0 else 0.0
    
    def _analyze_stat_performance(
        self, 
        prop_type: PropType, 
        last_5_stats: Dict[str, float], 
        season_averages: Optional[SeasonAverages],
        recent_games: List[GameStats]
    ) -> Dict[str, Any]:
        """Analyze performance for a specific stat with pros/cons"""
        
        stat_key = self._get_stat_key(prop_type)
        last_5_avg = last_5_stats.get(stat_key, 0)
        season_avg = self._get_season_stat(prop_type, season_averages) if season_averages else 0
        
        # Get individual game values for trend analysis
        game_values = self._get_game_values(prop_type, recent_games)
        
        # Calculate trend
        trend = self._calculate_trend(game_values)
        consistency = self._calculate_consistency(game_values)
        
        # Generate pros and cons
        pros, cons = self._generate_pros_cons(
            prop_type, last_5_avg, season_avg, game_values, trend, consistency
        )
        
        # Get basketball context
        basketball_info = self.basketball_terms.get(prop_type.value, {})
        
        return {
            "stat_name": prop_type.value.replace("_", " ").title(),
            "last_5_average": round(last_5_avg, 1),
            "season_average": round(season_avg, 1),
            "recent_games_values": game_values,
            "trend": trend,  # "improving", "declining", "stable"
            "consistency": consistency,  # "very_consistent", "consistent", "inconsistent"
            "pros": pros,
            "cons": cons,
            "basketball_explanation": basketball_info.get("description", ""),
            "good_performance_range": basketball_info.get("good_range", ""),
            "key_factors": basketball_info.get("factors", []),
            "form_vs_season": self._compare_form_to_season(last_5_avg, season_avg)
        }
    
    def _get_stat_key(self, prop_type: PropType) -> str:
        """Map PropType to stat key"""
        mapping = {
            PropType.POINTS: "points",
            PropType.REBOUNDS: "rebounds", 
            PropType.ASSISTS: "assists",
            PropType.STEALS: "steals",
            PropType.BLOCKS: "blocks",
            PropType.TURNOVERS: "turnovers",
            PropType.THREES_MADE: "threes_made",
            PropType.FREE_THROWS_MADE: "free_throws_made",
            PropType.FANTASY_SCORE: "fantasy_score"
        }
        return mapping.get(prop_type, prop_type.value)
    
    def _get_season_stat(self, prop_type: PropType, season_averages: SeasonAverages) -> float:
        """Get season average for specific stat"""
        mapping = {
            PropType.POINTS: season_averages.points_per_game,
            PropType.REBOUNDS: season_averages.rebounds_per_game,
            PropType.ASSISTS: season_averages.assists_per_game,
            PropType.STEALS: season_averages.steals_per_game,
            PropType.BLOCKS: season_averages.blocks_per_game,
            PropType.TURNOVERS: season_averages.turnovers_per_game,
            PropType.THREES_MADE: season_averages.three_point_percentage * 3,  # Rough estimate
            PropType.FREE_THROWS_MADE: 2.0,  # Default estimate
            PropType.FANTASY_SCORE: 30.0  # Default estimate
        }
        return mapping.get(prop_type, 0.0)
    
    def _get_game_values(self, prop_type: PropType, games: List[GameStats]) -> List[float]:
        """Get stat values from recent games"""
        mapping = {
            PropType.POINTS: [g.points or 0 for g in games],
            PropType.REBOUNDS: [g.rebounds or 0 for g in games],
            PropType.ASSISTS: [g.assists or 0 for g in games],
            PropType.STEALS: [g.steals or 0 for g in games],
            PropType.BLOCKS: [g.blocks or 0 for g in games],
            PropType.TURNOVERS: [g.turnovers or 0 for g in games],
            PropType.THREES_MADE: [g.three_pointers_made or 0 for g in games],
            PropType.FREE_THROWS_MADE: [g.free_throws_made or 0 for g in games],
            PropType.FANTASY_SCORE: [g.fantasy_score or 0 for g in games]
        }
        return mapping.get(prop_type, [])
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate if player is trending up, down, or stable"""
        if len(values) < 3:
            return "insufficient_data"
        
        # Compare first half vs second half of recent games
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        if second_avg > first_avg * 1.1:
            return "improving"
        elif second_avg < first_avg * 0.9:
            return "declining"
        else:
            return "stable"
    
    def _calculate_consistency(self, values: List[float]) -> str:
        """Calculate how consistent the player's performance is"""
        if len(values) < 3:
            return "insufficient_data"
        
        if not values or all(v == 0 for v in values):
            return "consistently_low"
        
        avg = statistics.mean(values)
        if avg == 0:
            return "consistently_low"
        
        # Calculate coefficient of variation
        std_dev = statistics.stdev(values) if len(values) > 1 else 0
        cv = (std_dev / avg) if avg > 0 else 0
        
        if cv < 0.2:
            return "very_consistent"
        elif cv < 0.4:
            return "consistent"
        else:
            return "inconsistent"
    
    def _generate_pros_cons(
        self, 
        prop_type: PropType, 
        last_5_avg: float, 
        season_avg: float, 
        game_values: List[float],
        trend: str,
        consistency: str
    ) -> tuple[List[str], List[str]]:
        """Generate pros and cons with basketball context"""
        
        pros = []
        cons = []
        
        stat_name = prop_type.value.replace("_", " ")
        
        # Trend analysis
        if trend == "improving":
            pros.append(f"📈 Trending UP in {stat_name} - recent games better than earlier ones")
        elif trend == "declining":
            cons.append(f"📉 Trending DOWN in {stat_name} - recent games worse than earlier ones")
        
        # Form vs season comparison
        if last_5_avg > season_avg * 1.1:
            pros.append(f"🔥 Hot streak! Recent {stat_name} ({last_5_avg:.1f}) well above season average ({season_avg:.1f})")
        elif last_5_avg < season_avg * 0.9:
            cons.append(f"❄️ Cold stretch. Recent {stat_name} ({last_5_avg:.1f}) below season average ({season_avg:.1f})")
        
        # Consistency analysis
        if consistency == "very_consistent":
            pros.append(f"⚡ Very reliable in {stat_name} - consistent performance across recent games")
        elif consistency == "inconsistent":
            cons.append(f"🎲 Unpredictable {stat_name} - big ups and downs in recent games")
        
        # Specific stat analysis
        if prop_type == PropType.POINTS:
            self._add_points_specific_analysis(last_5_avg, game_values, pros, cons)
        elif prop_type == PropType.REBOUNDS:
            self._add_rebounds_specific_analysis(last_5_avg, game_values, pros, cons)
        elif prop_type == PropType.ASSISTS:
            self._add_assists_specific_analysis(last_5_avg, game_values, pros, cons)
        elif prop_type == PropType.TURNOVERS:
            self._add_turnovers_specific_analysis(last_5_avg, game_values, pros, cons)
        
        # Add game-by-game context
        if game_values:
            high_game = max(game_values)
            low_game = min(game_values)
            pros.append(f"🏀 Recent high: {high_game:.0f} {stat_name}")
            if low_game < last_5_avg * 0.5:
                cons.append(f"⚠️ Recent low: {low_game:.0f} {stat_name} (concerning floor)")
        
        return pros, cons
    
    def _add_points_specific_analysis(self, avg: float, values: List[float], pros: List[str], cons: List[str]):
        """Add points-specific analysis"""
        if avg >= 20:
            pros.append("🎯 Elite scorer - consistently puts up big numbers")
        elif avg >= 15:
            pros.append("✅ Solid scorer - reliable for double digits")
        elif avg < 10:
            cons.append("⬇️ Low scoring role - limited offensive opportunities")
        
        # Check for 20+ point games
        big_games = [v for v in values if v >= 20]
        if len(big_games) >= 3:
            pros.append(f"💪 Multiple 20+ point games ({len(big_games)} of {len(values)})")
    
    def _add_rebounds_specific_analysis(self, avg: float, values: List[float], pros: List[str], cons: List[str]):
        """Add rebounds-specific analysis"""
        if avg >= 10:
            pros.append("🏀 Double-digit rebounder - dominates the boards")
        elif avg >= 7:
            pros.append("📦 Solid rebounder - good glass work")
        elif avg < 4:
            cons.append("⬇️ Limited rebounding - not a factor on the boards")
        
        double_doubles = [v for v in values if v >= 10]
        if len(double_doubles) >= 2:
            pros.append(f"💥 Multiple double-digit rebounding games ({len(double_doubles)} of {len(values)})")
    
    def _add_assists_specific_analysis(self, avg: float, values: List[float], pros: List[str], cons: List[str]):
        """Add assists-specific analysis"""
        if avg >= 7:
            pros.append("🎯 Elite playmaker - sets up teammates consistently")
        elif avg >= 4:
            pros.append("✅ Good facilitator - creates opportunities for others")
        elif avg < 2:
            cons.append("⬇️ Limited playmaking role - doesn't handle the ball much")
        
        big_assist_games = [v for v in values if v >= 7]
        if len(big_assist_games) >= 2:
            pros.append(f"🎪 Multiple high-assist games ({len(big_assist_games)} of {len(values)})")
    
    def _add_turnovers_specific_analysis(self, avg: float, values: List[float], pros: List[str], cons: List[str]):
        """Add turnovers-specific analysis (note: lower is better)"""
        if avg <= 2:
            pros.append("✅ Takes care of the ball well - low turnover rate")
        elif avg >= 4:
            cons.append("⚠️ High turnovers - gives the ball away too much")
        
        # For turnovers, high games are bad
        bad_games = [v for v in values if v >= 4]
        if len(bad_games) >= 2:
            cons.append(f"😬 Multiple high-turnover games ({len(bad_games)} of {len(values)})")
    
    def _compare_form_to_season(self, recent_avg: float, season_avg: float) -> str:
        """Compare recent form to season average"""
        if recent_avg > season_avg * 1.15:
            return "much_better"
        elif recent_avg > season_avg * 1.05:
            return "slightly_better"
        elif recent_avg < season_avg * 0.85:
            return "much_worse"
        elif recent_avg < season_avg * 0.95:
            return "slightly_worse"
        else:
            return "about_same"
    
    def _assess_overall_form(self, last_5_stats: Dict[str, float], season_averages: Optional[SeasonAverages]) -> Dict[str, Any]:
        """Assess player's overall current form"""
        if not season_averages:
            return {"assessment": "insufficient_data", "explanation": "Need season averages for comparison"}
        
        # Compare key stats
        comparisons = {
            "points": (last_5_stats.get("points", 0), season_averages.points_per_game),
            "rebounds": (last_5_stats.get("rebounds", 0), season_averages.rebounds_per_game),
            "assists": (last_5_stats.get("assists", 0), season_averages.assists_per_game)
        }
        
        better_count = sum(1 for recent, season in comparisons.values() if recent > season * 1.05)
        worse_count = sum(1 for recent, season in comparisons.values() if recent < season * 0.95)
        
        if better_count >= 2:
            assessment = "hot_streak"
            explanation = "Playing above season averages in multiple categories"
        elif worse_count >= 2:
            assessment = "cold_streak"
            explanation = "Playing below season averages in multiple categories"
        else:
            assessment = "normal_form"
            explanation = "Playing close to season averages"
        
        return {
            "assessment": assessment,
            "explanation": explanation,
            "better_stats": better_count,
            "worse_stats": worse_count,
            "advice": self._get_form_advice(assessment)
        }
    
    def _get_form_advice(self, assessment: str) -> str:
        """Get betting advice based on form"""
        advice_map = {
            "hot_streak": "🔥 Player is in great form! Consider OVER bets on their strong categories",
            "cold_streak": "❄️ Player struggling recently. Consider UNDER bets or avoid betting on them",
            "normal_form": "⚖️ Player performing normally. Use season averages as your guide"
        }
        return advice_map.get(assessment, "Analyze each stat individually")
    
    def _generate_beginner_tips(
        self, 
        player_info: PlayerInfo, 
        last_5_stats: Dict[str, float], 
        season_averages: Optional[SeasonAverages]
    ) -> List[str]:
        """Generate helpful tips for beginners"""
        tips = []
        
        # Position-based tips
        position = getattr(player_info, 'position', 'Unknown')
        if 'G' in position:  # Guard
            tips.append("🏀 Guards typically get more assists and steals, fewer rebounds")
            if last_5_stats.get("assists", 0) >= 5:
                tips.append("💡 This guard is a good playmaker - assists props might be valuable")
        elif 'F' in position:  # Forward  
            tips.append("🏀 Forwards usually balance scoring, rebounding, and some assists")
            if last_5_stats.get("rebounds", 0) >= 8:
                tips.append("💡 This forward hits the boards well - rebounds props to consider")
        elif 'C' in position:  # Center
            tips.append("🏀 Centers focus on rebounds, blocks, and close-range scoring")
            if last_5_stats.get("blocks", 0) >= 1:
                tips.append("💡 This center protects the rim - blocks props might hit")
        
        # General tips
        tips.extend([
            "📊 Compare recent averages to season averages to spot trends",
            "🎯 Look for consistent performers for safer bets",
            "📈 Players on hot streaks often continue good form short-term",
            "⚖️ Mix high-confidence picks with one riskier prop for bigger payouts"
        ])
        
        return tips

# Create singleton instance
beginner_analysis_service = BeginnerAnalysisService()