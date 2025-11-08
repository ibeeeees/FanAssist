import boto3
import json
from typing import List, Dict, Any, Optional
from app.models import PlayerInfo, GameStats, SeasonAverages, PropPrediction, PropType
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class AWSBedrockService:
    def __init__(self):
        self.client = boto3.client(
            'bedrock-runtime',
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key
        )
        self.model_id = settings.aws_bedrock_model_id
        
    async def analyze_player_props_for_beginners(
        self,
        player_info: PlayerInfo,
        recent_games: List[GameStats],
        season_averages: SeasonAverages,
        prop_lines: Dict[PropType, float],
        detailed_analysis: Dict[str, Any],
        opponent_info: Optional[Dict[str, Any]] = None,
        injury_report: Optional[str] = None
    ) -> List[PropPrediction]:
        """
        Analyze player props with beginner-friendly explanations and game simulation
        """
        try:
            # Create enhanced prompt for beginners
            prompt = self._create_beginner_analysis_prompt(
                player_info, recent_games, season_averages, prop_lines, 
                detailed_analysis, opponent_info, injury_report
            )
            
            # Call AWS Bedrock
            response = await self._call_bedrock(prompt)
            
            # Parse the response and create PropPrediction objects
            predictions = self._parse_beginner_predictions(response, prop_lines)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error analyzing player props for beginners: {e}")
            return []
    
    def _create_beginner_analysis_prompt(
        self,
        player_info: PlayerInfo,
        recent_games: List[GameStats],
        season_averages: SeasonAverages,
        prop_lines: Dict[PropType, float],
        detailed_analysis: Dict[str, Any],
        opponent_info: Optional[Dict[str, Any]],
        injury_report: Optional[str]
    ) -> str:
        """Create a comprehensive prompt for beginner-friendly LLM analysis"""
        
        # Extract key insights from detailed analysis
        stat_insights = []
        for stat_name, analysis in detailed_analysis.get('stat_analysis', {}).items():
            pros = analysis.get('pros', [])
            cons = analysis.get('cons', [])
            stat_insights.append({
                "stat": stat_name,
                "last_5_avg": analysis.get('last_5_average', 0),
                "season_avg": analysis.get('season_average', 0),
                "trend": analysis.get('trend', 'stable'),
                "consistency": analysis.get('consistency', 'consistent'),
                "pros": pros,
                "cons": cons
            })
        
        overall_form = detailed_analysis.get('overall_form', {})
        
        prompt = f"""
You are an expert NBA betting analyst who specializes in explaining complex basketball statistics and betting concepts to BEGINNERS. Your job is to analyze player props and provide easy-to-understand explanations that help new bettors learn.

PLAYER INFORMATION:
- Name: {player_info.full_name}
- Team: {player_info.team_name} ({player_info.team_abbreviation})
- Position: {player_info.position}

CURRENT FORM ASSESSMENT:
- Overall Form: {overall_form.get('assessment', 'normal_form')}
- Explanation: {overall_form.get('explanation', 'Playing at normal levels')}
- Advice: {overall_form.get('advice', 'Use standard analysis')}

DETAILED LAST 5 GAMES ANALYSIS:
{self._format_stat_insights(stat_insights)}

SEASON CONTEXT:
- Games Played: {season_averages.games_played}
- Season Averages: {season_averages.points_per_game:.1f} pts, {season_averages.rebounds_per_game:.1f} reb, {season_averages.assists_per_game:.1f} ast

BETTING LINES TO ANALYZE:
{json.dumps({prop.value: line for prop, line in prop_lines.items()}, indent=2)}

RECENT GAMES PERFORMANCE:
{self._format_recent_games_for_beginners(recent_games)}

{f"OPPONENT INFORMATION: {json.dumps(opponent_info, indent=2)}" if opponent_info else ""}
{f"INJURY REPORT: {injury_report}" if injury_report else ""}

ANALYSIS REQUIREMENTS FOR BEGINNERS:

For each prop line, provide analysis in this JSON format:

{{
  "predictions": [
    {{
      "prop_type": "points",
      "predicted_value": 24.5,
      "confidence": 0.85,
      "recommendation": "over",
      "reasoning": "DETAILED explanation including: 1) What this stat means in basketball, 2) Why you expect this outcome, 3) Key factors supporting your pick, 4) What could go wrong",
      "beginner_explanation": "Simple explanation of the bet and why it makes sense",
      "game_simulation": "Describe a realistic game scenario where this bet hits/misses",
      "confidence_explanation": "Explain why you're confident/uncertain in simple terms",
      "key_stats": "Highlight the 2-3 most important numbers from recent games",
      "risk_level": "low/medium/high with explanation",
      "betting_tip": "Specific advice for beginners betting this prop"
    }}
  ]
}}

IMPORTANT GUIDELINES FOR BEGINNERS:
1. Always explain basketball terms (what rebounds, assists, etc. actually mean)
2. Use the detailed analysis provided to support your reasoning
3. Give specific examples from recent games
4. Explain confidence levels in simple terms (why you're sure/unsure)
5. Simulate realistic game scenarios 
6. Highlight risk factors that beginners should know
7. Use encouraging language but be honest about risks
8. Compare recent form to season averages and explain what that means
9. Give practical betting advice (bet sizing, when to avoid, etc.)
10. Use emojis and formatting to make it engaging

CONFIDENCE SCALE FOR BEGINNERS:
- 0.9-1.0: "Very confident" (explain why this is almost certain)
- 0.8-0.89: "Confident" (good evidence supporting this pick)
- 0.7-0.79: "Somewhat confident" (decent chance but some concerns)  
- 0.6-0.69: "Uncertain" (could go either way)
- Below 0.6: "Not recommended" (too risky for beginners)

Focus on education while providing actionable betting insights!
"""
        
        return prompt
    
    def _format_stat_insights(self, insights: List[Dict]) -> str:
        """Format statistical insights for the prompt"""
        formatted = []
        for insight in insights:
            formatted.append(f"""
{insight['stat'].title()}:
- Last 5 games: {insight['last_5_avg']:.1f} (vs season: {insight['season_avg']:.1f})
- Trend: {insight['trend']} | Consistency: {insight['consistency']}
- Pros: {'; '.join(insight['pros'][:3])}  
- Cons: {'; '.join(insight['cons'][:3])}
""")
        return '\n'.join(formatted)
    
    def _format_recent_games_for_beginners(self, games: List[GameStats]) -> str:
        """Format recent games in a beginner-friendly way"""
        if not games:
            return "No recent games available"
        
        formatted_games = []
        for i, game in enumerate(games[:5], 1):
            formatted_games.append(f"""
Game {i} vs {game.opponent} ({'Home' if game.is_home else 'Away'}):
- Points: {game.points or 0} | Rebounds: {game.rebounds or 0} | Assists: {game.assists or 0}
- 3-Pointers: {game.three_pointers_made or 0} | Steals: {game.steals or 0} | Blocks: {game.blocks or 0}
- Turnovers: {game.turnovers or 0} | Fantasy: {game.fantasy_score or 0:.1f}
""")
        return '\n'.join(formatted_games)
    
    def _parse_beginner_predictions(self, response: str, prop_lines: Dict[PropType, float]) -> List[PropPrediction]:
        """Parse LLM response into detailed PropPrediction objects for beginners"""
        try:
            # Try to extract JSON from the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[start_idx:end_idx]
            data = json.loads(json_str)
            
            predictions = []
            for pred_data in data.get('predictions', []):
                prop_type_str = pred_data.get('prop_type')
                
                # Convert string to PropType enum
                try:
                    prop_type = PropType(prop_type_str)
                except ValueError:
                    continue  # Skip invalid prop types
                
                # Create enhanced PropPrediction with beginner fields
                prediction = PropPrediction(
                    prop_type=prop_type,
                    predicted_value=float(pred_data.get('predicted_value', 0)),
                    confidence=float(pred_data.get('confidence', 0)),
                    line_value=prop_lines.get(prop_type),
                    recommendation=pred_data.get('recommendation', 'avoid'),
                    reasoning=pred_data.get('reasoning', 'No reasoning provided')
                )
                
                # Add beginner-specific fields as a custom attribute
                prediction.beginner_details = {
                    "beginner_explanation": pred_data.get('beginner_explanation', ''),
                    "game_simulation": pred_data.get('game_simulation', ''),
                    "confidence_explanation": pred_data.get('confidence_explanation', ''),
                    "key_stats": pred_data.get('key_stats', ''),
                    "risk_level": pred_data.get('risk_level', 'medium'),
                    "betting_tip": pred_data.get('betting_tip', '')
                }
                
                predictions.append(prediction)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error parsing beginner predictions: {e}")
            # Return simplified predictions if parsing fails
            return [
                PropPrediction(
                    prop_type=prop_type,
                    predicted_value=line_value,
                    confidence=0.5,
                    line_value=line_value,
                    recommendation="avoid",
                    reasoning="Analysis failed - please try again"
                )
                for prop_type, line_value in prop_lines.items()
            ]
    
    async def simulate_game_outcome(
        self,
        predictions: List[PropPrediction],
        player_name: str
    ) -> Dict[str, Any]:
        """
        Simulate a game outcome and provide feedback on each betting leg
        """
        try:
            prompt = f"""
You are simulating a realistic NBA game outcome for {player_name} based on the following prop bets:

PROP BETS TO SIMULATE:
{json.dumps([{
    "prop": pred.prop_type.value,
    "line": pred.line_value,
    "bet": pred.recommendation,
    "confidence": pred.confidence
} for pred in predictions], indent=2)}

Simulate a realistic game performance and provide feedback on each leg:

{{
  "simulation": {{
    "game_scenario": "Describe the type of game that occurred (blowout, close game, high-scoring, defensive battle, etc.)",
    "player_performance": "Overall description of how the player performed",
    "final_stats": {{
      "points": 25,
      "rebounds": 8,
      "assists": 6,
      "steals": 2,
      "blocks": 1,
      "turnovers": 3,
      "threes_made": 2,
      "free_throws_made": 4,
      "fantasy_score": 42.5
    }},
    "leg_results": [
      {{
        "prop_type": "points",
        "line": 22.5,
        "bet_type": "over", 
        "actual_result": 25,
        "bet_result": "won",
        "explanation": "Why this leg won/lost in this game scenario",
        "lesson_learned": "What this teaches beginners about this type of bet"
      }}
    ],
    "overall_ticket": {{
      "total_legs": 4,
      "winning_legs": 3,
      "losing_legs": 1,
      "ticket_result": "lost",
      "payout": 0,
      "explanation": "Why the overall ticket won/lost and what beginners can learn"
    }},
    "beginner_insights": [
      "Key lesson from this simulation",
      "What to watch for in real games",
      "How this affects future betting strategy"
    ]
  }}
}}

Make the simulation realistic and educational for beginners. Show how game flow affects different props.
"""
            
            response = await self._call_bedrock(prompt)
            
            # Parse simulation response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                simulation_data = json.loads(json_str)
                return simulation_data
            
            return {"error": "Failed to parse simulation response"}
            
        except Exception as e:
            logger.error(f"Error simulating game outcome: {e}")
            return {"error": f"Simulation failed: {str(e)}"}
            
    async def explain_betting_concepts(self, concept: str) -> str:
        """Explain betting concepts for beginners"""
        try:
            prompt = f"""
You are a patient teacher explaining NBA betting concepts to complete beginners. 
Explain the concept of "{concept}" in simple terms with examples.

Use this structure:
1. Simple definition
2. Why it matters in betting
3. Real example with NBA player
4. Common beginner mistakes to avoid
5. Practical tips

Make it encouraging and easy to understand!
"""
            
            response = await self._call_bedrock(prompt)
            return response
            
        except Exception as e:
            logger.error(f"Error explaining concept: {e}")
            return f"Sorry, couldn't explain {concept} right now. Please try again."
    
    def _create_analysis_prompt(
        self,
        player_info: PlayerInfo,
        recent_games: List[GameStats],
        season_averages: SeasonAverages,
        prop_lines: Dict[PropType, float],
        opponent_info: Optional[Dict[str, Any]],
        injury_report: Optional[str]
    ) -> str:
        """Create a comprehensive prompt for LLM analysis"""
        
        # Format recent games data
        recent_stats = []
        for game in recent_games[:10]:  # Last 10 games
            recent_stats.append({
                "date": game.game_date.strftime("%Y-%m-%d"),
                "opponent": game.opponent,
                "home": game.is_home,
                "minutes": game.minutes_played,
                "points": game.points,
                "rebounds": game.rebounds,
                "assists": game.assists,
                "steals": game.steals,
                "blocks": game.blocks,
                "turnovers": game.turnovers,
                "threes_made": game.three_pointers_made
            })
        
        # Calculate recent averages (last 5 games)
        recent_5_stats = self._calculate_recent_averages(recent_games[:5])
        recent_10_stats = self._calculate_recent_averages(recent_games[:10])
        
        prompt = f"""
You are an expert NBA betting analyst specializing in player prop predictions for PrizePicks. 
Analyze the following player data and provide detailed predictions for each prop line.

PLAYER INFORMATION:
- Name: {player_info.full_name}
- Team: {player_info.team_name} ({player_info.team_abbreviation})
- Position: {player_info.position}

SEASON AVERAGES (2023-24):
- Games Played: {season_averages.games_played}
- Minutes: {season_averages.minutes_per_game:.1f}
- Points: {season_averages.points_per_game:.1f}
- Rebounds: {season_averages.rebounds_per_game:.1f}
- Assists: {season_averages.assists_per_game:.1f}
- Steals: {season_averages.steals_per_game:.1f}
- Blocks: {season_averages.blocks_per_game:.1f}
- Turnovers: {season_averages.turnovers_per_game:.1f}
- FG%: {season_averages.field_goal_percentage:.1%}
- 3P%: {season_averages.three_point_percentage:.1%}
- FT%: {season_averages.free_throw_percentage:.1%}

RECENT PERFORMANCE (Last 5 games):
{self._format_recent_averages(recent_5_stats)}

RECENT PERFORMANCE (Last 10 games):
{self._format_recent_averages(recent_10_stats)}

LAST 10 GAMES DETAIL:
{json.dumps(recent_stats, indent=2)}

PROP LINES TO ANALYZE:
{json.dumps({prop.value: line for prop, line in prop_lines.items()}, indent=2)}

{f"OPPONENT INFORMATION: {json.dumps(opponent_info, indent=2)}" if opponent_info else ""}

{f"INJURY REPORT: {injury_report}" if injury_report else ""}

ANALYSIS REQUIREMENTS:
For each prop line, provide your analysis in the following JSON format:

{{
  "predictions": [
    {{
      "prop_type": "points",
      "predicted_value": 24.5,
      "confidence": 0.85,
      "recommendation": "over",
      "reasoning": "Detailed explanation of your analysis including trends, matchup factors, and key statistics"
    }}
  ]
}}

Consider the following factors in your analysis:
1. Recent form vs season averages
2. Home/away performance
3. Matchup advantages/disadvantages
4. Injury status and playing time
5. Historical performance against similar opponents
6. Game pace and style considerations
7. Rest days and schedule density
8. Weather/external factors (if applicable)

Provide confidence scores from 0.0 to 1.0 where:
- 0.9-1.0: Extremely confident
- 0.8-0.89: Very confident  
- 0.7-0.79: Confident
- 0.6-0.69: Moderate confidence
- Below 0.6: Low confidence (recommend avoid)

Give specific reasoning for each prediction focusing on the most relevant statistical trends and factors.
"""
        
        return prompt
    
    def _calculate_recent_averages(self, games: List[GameStats]) -> Dict[str, float]:
        """Calculate averages for recent games"""
        if not games:
            return {}
        
        stats = {
            "games": len(games),
            "minutes": sum(g.minutes_played or 0 for g in games) / len(games),
            "points": sum(g.points or 0 for g in games) / len(games),
            "rebounds": sum(g.rebounds or 0 for g in games) / len(games),
            "assists": sum(g.assists or 0 for g in games) / len(games),
            "steals": sum(g.steals or 0 for g in games) / len(games),
            "blocks": sum(g.blocks or 0 for g in games) / len(games),
            "turnovers": sum(g.turnovers or 0 for g in games) / len(games),
            "threes_made": sum(g.three_pointers_made or 0 for g in games) / len(games),
        }
        
        return stats
    
    def _format_recent_averages(self, stats: Dict[str, float]) -> str:
        """Format recent averages for prompt"""
        if not stats:
            return "No recent games available"
        
        return f"""
- Games: {stats.get('games', 0)}
- Minutes: {stats.get('minutes', 0):.1f}
- Points: {stats.get('points', 0):.1f}
- Rebounds: {stats.get('rebounds', 0):.1f}
- Assists: {stats.get('assists', 0):.1f}
- Steals: {stats.get('steals', 0):.1f}
- Blocks: {stats.get('blocks', 0):.1f}
- Turnovers: {stats.get('turnovers', 0):.1f}
- 3-Pointers Made: {stats.get('threes_made', 0):.1f}
"""
    
    async def _call_bedrock(self, prompt: str) -> str:
        """Make a call to AWS Bedrock"""
        try:
            # Format request for Claude (Anthropic) model
            if "anthropic.claude" in self.model_id:
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4000,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.1,
                    "top_p": 0.9
                }
            # Format for other models (Titan, etc.)
            else:
                body = {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 4000,
                        "temperature": 0.1,
                        "topP": 0.9
                    }
                }
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            
            # Extract text based on model type
            if "anthropic.claude" in self.model_id:
                return response_body['content'][0]['text']
            else:
                return response_body['results'][0]['outputText']
                
        except Exception as e:
            logger.error(f"Error calling Bedrock: {e}")
            raise
    
    def _parse_predictions(self, response: str, prop_lines: Dict[PropType, float]) -> List[PropPrediction]:
        """Parse LLM response into PropPrediction objects"""
        try:
            # Try to extract JSON from the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[start_idx:end_idx]
            data = json.loads(json_str)
            
            predictions = []
            for pred_data in data.get('predictions', []):
                prop_type_str = pred_data.get('prop_type')
                
                # Convert string to PropType enum
                try:
                    prop_type = PropType(prop_type_str)
                except ValueError:
                    continue  # Skip invalid prop types
                
                prediction = PropPrediction(
                    prop_type=prop_type,
                    predicted_value=float(pred_data.get('predicted_value', 0)),
                    confidence=float(pred_data.get('confidence', 0)),
                    line_value=prop_lines.get(prop_type),
                    recommendation=pred_data.get('recommendation', 'avoid'),
                    reasoning=pred_data.get('reasoning', 'No reasoning provided')
                )
                predictions.append(prediction)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error parsing predictions: {e}")
            # Return default predictions if parsing fails
            return [
                PropPrediction(
                    prop_type=prop_type,
                    predicted_value=line_value,
                    confidence=0.5,
                    line_value=line_value,
                    recommendation="avoid",
                    reasoning="Analysis failed - insufficient data"
                )
                for prop_type, line_value in prop_lines.items()
            ]
    
    async def get_general_betting_insights(self, context: str) -> str:
        """Get general betting insights for a given context"""
        try:
            prompt = f"""
You are an expert NBA betting analyst. Provide insights and recommendations for the following context:

{context}

Please provide:
1. Key factors to consider
2. Potential value opportunities
3. Risk assessment
4. General recommendations

Keep your response concise but informative.
"""
            
            response = await self._call_bedrock(prompt)
            return response
            
        except Exception as e:
            logger.error(f"Error getting betting insights: {e}")
            return "Unable to provide insights at this time."

# Create singleton instance
aws_bedrock_service = AWSBedrockService()