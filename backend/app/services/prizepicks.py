from typing import List, Dict, Optional
import asyncio
from datetime import datetime
from app.models import (
    PlayerInfo, GameStats, SeasonAverages, PropPrediction, 
    PlayerAnalysis, PrizePicksProp, PropAnalysisRequest, 
    PropAnalysisResponse, PropType
)
from app.services.nba_stats import nba_stats_service
from app.services.aws_bedrock import aws_bedrock_service
import logging

logger = logging.getLogger(__name__)

class PrizePicksAnalysisService:
    def __init__(self):
        self.nba_service = nba_stats_service
        self.llm_service = aws_bedrock_service
    
    async def analyze_props(self, request: PropAnalysisRequest) -> PropAnalysisResponse:
        """
        Analyze multiple PrizePicks props and return comprehensive analysis
        """
        try:
            analyses = []
            
            # Group props by player for efficient processing
            player_props = self._group_props_by_player(request.props)
            
            # Process each player's props
            for player_name, props in player_props.items():
                analysis = await self._analyze_player_props(player_name, props, request.analysis_depth)
                if analysis:
                    analyses.append(analysis)
            
            # Generate overall recommendation
            overall_recommendation = self._generate_overall_recommendation(analyses)
            overall_confidence = self._calculate_overall_confidence(analyses)
            
            return PropAnalysisResponse(
                analyses=analyses,
                overall_recommendation=overall_recommendation,
                confidence_score=overall_confidence,
                generated_at=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error analyzing props: {e}")
            raise
    
    async def _analyze_player_props(
        self, 
        player_name: str, 
        props: List[PrizePicksProp], 
        analysis_depth: str
    ) -> Optional[PlayerAnalysis]:
        """Analyze props for a single player"""
        try:
            # Get player information
            player_info = await self.nba_service.get_player_info(player_name)
            if not player_info:
                logger.warning(f"Player not found: {player_name}")
                return None
            
            # Get player stats based on analysis depth
            if analysis_depth == "quick":
                recent_games = await self.nba_service.get_player_game_log(player_info.player_id, last_n_games=5)
            elif analysis_depth == "deep":
                recent_games = await self.nba_service.get_player_game_log(player_info.player_id, last_n_games=15)
            else:  # standard
                recent_games = await self.nba_service.get_player_game_log(player_info.player_id, last_n_games=10)
            
            # Get season averages
            season_averages = await self.nba_service.get_player_season_averages(player_info.player_id)
            if not season_averages:
                logger.warning(f"No season averages found for {player_name}")
                return None
            
            # Prepare prop lines for LLM analysis
            prop_lines = {prop.prop_type: prop.line for prop in props}
            
            # Get injury status and matchup info (placeholder for now)
            injury_status = await self._get_injury_status(player_info.player_id)
            matchup_info = await self._get_matchup_analysis(player_info.team_id)
            
            # Analyze props using LLM
            prop_predictions = await self.llm_service.analyze_player_props(
                player_info=player_info,
                recent_games=recent_games,
                season_averages=season_averages,
                prop_lines=prop_lines,
                opponent_info=matchup_info,
                injury_report=injury_status
            )
            
            # Calculate overall confidence for this player
            player_confidence = self._calculate_player_confidence(prop_predictions)
            
            return PlayerAnalysis(
                player_info=player_info,
                recent_stats=recent_games,
                season_averages=season_averages,
                prop_predictions=prop_predictions,
                injury_status=injury_status,
                matchup_analysis=self._format_matchup_analysis(matchup_info),
                confidence_score=player_confidence
            )
            
        except Exception as e:
            logger.error(f"Error analyzing player {player_name}: {e}")
            return None
    
    def _group_props_by_player(self, props: List[PrizePicksProp]) -> Dict[str, List[PrizePicksProp]]:
        """Group props by player name"""
        player_props = {}
        for prop in props:
            if prop.player_name not in player_props:
                player_props[prop.player_name] = []
            player_props[prop.player_name].append(prop)
        return player_props
    
    async def _get_injury_status(self, player_id: int) -> Optional[str]:
        """Get injury status for a player (placeholder - would integrate with injury API)"""
        # This would integrate with an injury reporting API
        # For now, return None
        return None
    
    async def _get_matchup_analysis(self, team_id: int) -> Optional[Dict]:
        """Get matchup analysis for a team (placeholder - would integrate with matchup data)"""
        # This would integrate with team stats and matchup APIs
        # For now, return basic info
        return {
            "opponent_ranking": "Unknown",
            "pace": "Unknown",
            "defensive_rating": "Unknown"
        }
    
    def _format_matchup_analysis(self, matchup_info: Optional[Dict]) -> Optional[str]:
        """Format matchup analysis for display"""
        if not matchup_info:
            return None
        
        return f"Opponent ranking: {matchup_info.get('opponent_ranking', 'Unknown')}, " \
               f"Pace: {matchup_info.get('pace', 'Unknown')}, " \
               f"Defensive rating: {matchup_info.get('defensive_rating', 'Unknown')}"
    
    def _calculate_player_confidence(self, predictions: List[PropPrediction]) -> float:
        """Calculate overall confidence score for a player's predictions"""
        if not predictions:
            return 0.0
        
        # Average confidence weighted by prediction confidence
        total_confidence = sum(pred.confidence for pred in predictions)
        return total_confidence / len(predictions)
    
    def _calculate_overall_confidence(self, analyses: List[PlayerAnalysis]) -> float:
        """Calculate overall confidence across all analyses"""
        if not analyses:
            return 0.0
        
        total_confidence = sum(analysis.confidence_score for analysis in analyses)
        return total_confidence / len(analyses)
    
    def _generate_overall_recommendation(self, analyses: List[PlayerAnalysis]) -> str:
        """Generate an overall recommendation based on all analyses"""
        if not analyses:
            return "No analysis available"
        
        # Count recommendations
        over_count = 0
        under_count = 0
        avoid_count = 0
        high_confidence_plays = []
        
        for analysis in analyses:
            for prediction in analysis.prop_predictions:
                if prediction.recommendation == "over":
                    over_count += 1
                    if prediction.confidence >= 0.8:
                        high_confidence_plays.append(f"{analysis.player_info.full_name} {prediction.prop_type.value} OVER")
                elif prediction.recommendation == "under":
                    under_count += 1
                    if prediction.confidence >= 0.8:
                        high_confidence_plays.append(f"{analysis.player_info.full_name} {prediction.prop_type.value} UNDER")
                else:
                    avoid_count += 1
        
        # Generate recommendation summary
        total_props = over_count + under_count + avoid_count
        
        if not high_confidence_plays:
            return f"Analyzed {total_props} props. No high-confidence plays identified. Consider avoiding these props."
        
        recommendation = f"Analyzed {total_props} props. "
        recommendation += f"High-confidence plays ({len(high_confidence_plays)}): "
        recommendation += ", ".join(high_confidence_plays[:5])  # Limit to top 5
        
        if len(high_confidence_plays) > 5:
            recommendation += f" and {len(high_confidence_plays) - 5} others."
        
        if avoid_count > 0:
            recommendation += f" Recommend avoiding {avoid_count} props due to low confidence."
        
        return recommendation
    
    async def get_player_quick_analysis(self, player_name: str, prop_type: PropType, line: float) -> Optional[PropPrediction]:
        """Get quick analysis for a single player prop"""
        try:
            # Create a single prop request
            props = [PrizePicksProp(
                player_name=player_name,
                prop_type=prop_type,
                line=line
            )]
            
            request = PropAnalysisRequest(props=props, analysis_depth="quick")
            response = await self.analyze_props(request)
            
            if response.analyses and response.analyses[0].prop_predictions:
                return response.analyses[0].prop_predictions[0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error in quick analysis for {player_name}: {e}")
            return None
    
    async def get_trending_props(self, limit: int = 10) -> List[Dict]:
        """Get trending props based on recent performance (placeholder)"""
        # This would analyze recent player performance trends
        # and suggest props that might have value
        return [
            {
                "player_name": "Example Player",
                "prop_type": "points",
                "trend": "trending_up",
                "reason": "Averaging 5+ points above season average in last 5 games"
            }
        ]

# Create singleton instance
prizepicks_service = PrizePicksAnalysisService()