from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models import PropAnalysisRequest, PropAnalysisResponse, PropType, BetType
from app.services.beginner_analysis import beginner_analysis_service
from app.services.aws_bedrock import aws_bedrock_service
from pydantic import BaseModel

router = APIRouter()

class BeginnerPropRequest(BaseModel):
    player_name: str
    prop_type: PropType
    line_value: float
    bet_type: BetType = BetType.OVER

class BeginnerTicketRequest(BaseModel):
    legs: List[BeginnerPropRequest]
    wager_amount: float = 10.0

class BeginnerAnalysisResponse(BaseModel):
    player_analysis: dict
    ai_predictions: List[dict]
    simulation_result: Optional[dict] = None
    beginner_summary: dict
    educational_content: dict

@router.get("/players/{player_name}/beginner-analysis")
async def get_beginner_player_analysis(player_name: str):
    """
    Get comprehensive beginner-friendly analysis of a player's last 5 games
    with detailed pros/cons and basketball explanations
    """
    try:
        analysis = await beginner_analysis_service.analyze_last_5_games(player_name)
        
        return {
            "player_info": analysis["player_info"],
            "last_5_games": analysis["last_5_games"],
            "performance_summary": {
                "last_5_averages": analysis["last_5_averages"],
                "season_averages": analysis["season_averages"],
                "overall_form": analysis["overall_form"]
            },
            "detailed_analysis": analysis["stat_analysis"],
            "beginner_tips": analysis["beginner_tips"],
            "basketball_education": {
                "position_explanation": _get_position_explanation(analysis["player_info"]),
                "stat_explanations": _get_stat_explanations(),
                "betting_basics": _get_betting_basics()
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing player: {str(e)}")

@router.post("/analyze-prop/beginner")
async def analyze_single_prop_beginner(request: BeginnerPropRequest):
    """
    Analyze a single prop bet with beginner-friendly explanations
    """
    try:
        # Get detailed player analysis
        player_analysis = await beginner_analysis_service.analyze_last_5_games(request.player_name)
        
        # Create prop lines for AI analysis
        prop_lines = {request.prop_type: request.line_value}
        
        # Get AI analysis with beginner focus
        ai_predictions = await aws_bedrock_service.analyze_player_props_for_beginners(
            player_info=player_analysis["player_info"],
            recent_games=player_analysis["last_5_games"],
            season_averages=player_analysis["season_averages"],
            prop_lines=prop_lines,
            detailed_analysis=player_analysis
        )
        
        if not ai_predictions:
            raise HTTPException(status_code=500, detail="Failed to generate AI analysis")
        
        prediction = ai_predictions[0]
        
        # Generate simulation
        simulation = await aws_bedrock_service.simulate_game_outcome([prediction], request.player_name)
        
        # Create beginner summary
        beginner_summary = _create_prop_summary(
            request, prediction, player_analysis["stat_analysis"].get(request.prop_type.value, {})
        )
        
        return BeginnerAnalysisResponse(
            player_analysis=player_analysis,
            ai_predictions=[{
                "prop_type": prediction.prop_type.value,
                "recommendation": prediction.recommendation,
                "confidence": prediction.confidence,
                "reasoning": prediction.reasoning,
                "beginner_details": getattr(prediction, 'beginner_details', {}),
                "line_value": prediction.line_value,
                "predicted_value": prediction.predicted_value
            }],
            simulation_result=simulation,
            beginner_summary=beginner_summary,
            educational_content=_get_educational_content(request.prop_type)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing prop: {str(e)}")

@router.post("/analyze-ticket/beginner")
async def analyze_ticket_beginner(request: BeginnerTicketRequest):
    """
    Analyze a multi-leg ticket with beginner-friendly breakdown of each leg
    """
    try:
        if len(request.legs) > 6:
            raise HTTPException(status_code=400, detail="Maximum 6 legs per ticket for beginners")
        
        if request.wager_amount > 100:
            raise HTTPException(status_code=400, detail="Maximum $100 wager recommended for beginners")
        
        ticket_analysis = {
            "legs": [],
            "overall_assessment": {},
            "risk_analysis": {},
            "educational_insights": []
        }
        
        all_predictions = []
        
        # Analyze each leg
        for i, leg in enumerate(request.legs, 1):
            try:
                # Get player analysis
                player_analysis = await beginner_analysis_service.analyze_last_5_games(leg.player_name)
                
                # Get AI prediction
                prop_lines = {leg.prop_type: leg.line_value}
                ai_predictions = await aws_bedrock_service.analyze_player_props_for_beginners(
                    player_info=player_analysis["player_info"],
                    recent_games=player_analysis["last_5_games"],
                    season_averages=player_analysis["season_averages"],
                    prop_lines=prop_lines,
                    detailed_analysis=player_analysis
                )
                
                if ai_predictions:
                    prediction = ai_predictions[0]
                    all_predictions.append(prediction)
                    
                    leg_analysis = {
                        "leg_number": i,
                        "player_name": leg.player_name,
                        "prop": f"{leg.prop_type.value} {leg.bet_type.value} {leg.line_value}",
                        "recommendation": prediction.recommendation,
                        "confidence": prediction.confidence,
                        "risk_level": getattr(prediction, 'beginner_details', {}).get('risk_level', 'medium'),
                        "key_points": _extract_key_points(prediction),
                        "stat_context": player_analysis["stat_analysis"].get(leg.prop_type.value, {}),
                        "why_this_pick": getattr(prediction, 'beginner_details', {}).get('beginner_explanation', prediction.reasoning[:100])
                    }
                    
                    ticket_analysis["legs"].append(leg_analysis)
                
            except Exception as e:
                ticket_analysis["legs"].append({
                    "leg_number": i,
                    "player_name": leg.player_name,
                    "error": f"Analysis failed: {str(e)}"
                })
        
        # Overall ticket assessment
        if all_predictions:
            # Simulate the entire ticket
            ticket_simulation = await aws_bedrock_service.simulate_game_outcome(
                all_predictions, 
                f"Multi-leg ticket ({len(request.legs)} legs)"
            )
            
            # Calculate overall risk and recommendation
            avg_confidence = sum(p.confidence for p in all_predictions) / len(all_predictions)
            high_risk_legs = len([p for p in all_predictions if p.confidence < 0.7])
            
            ticket_analysis["overall_assessment"] = {
                "average_confidence": avg_confidence,
                "high_risk_legs": high_risk_legs,
                "recommendation": _get_ticket_recommendation(avg_confidence, high_risk_legs, len(request.legs)),
                "estimated_hit_probability": _estimate_ticket_probability(all_predictions),
                "potential_payout": request.wager_amount * (1.9 ** len(request.legs))  # PrizePicks-style
            }
            
            ticket_analysis["simulation"] = ticket_simulation
            
            # Educational insights
            ticket_analysis["educational_insights"] = _generate_ticket_insights(
                request.legs, all_predictions, avg_confidence
            )
        
        return ticket_analysis
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing ticket: {str(e)}")

@router.get("/education/basketball-terms")
async def get_basketball_education():
    """
    Get educational content about basketball terms and concepts
    """
    return {
        "basic_stats": {
            "points": {
                "definition": "Points scored by making field goals, three-pointers, and free throws",
                "typical_ranges": "10-15 (role player), 15-20 (solid scorer), 20-25 (star), 25+ (superstar)",
                "betting_tips": "Look at shot attempts, efficiency, and role in offense"
            },
            "rebounds": {
                "definition": "Gaining possession after a missed shot (offensive or defensive)",
                "typical_ranges": "4-6 (guards), 6-8 (forwards), 8-12 (centers)",
                "betting_tips": "Consider height, playing time, and opponent pace"
            },
            "assists": {
                "definition": "Passes that directly lead to a teammate's made shot",
                "typical_ranges": "2-4 (non-guards), 4-6 (guards), 6+ (playmakers)",
                "betting_tips": "Look at ball-handling role and teammate shooting"
            },
            "steals": {
                "definition": "Taking possession away from opponent through defensive play",
                "typical_ranges": "0.5-1 (average), 1-1.5 (active), 1.5+ (elite)",
                "betting_tips": "Harder to predict, consider defensive style and pace"
            }
        },
        "betting_concepts": {
            "over_under": "Bet whether player will go OVER or UNDER the set line",
            "line": "The number you're betting over or under (e.g., 25.5 points)",
            "juice": "The cost of placing the bet (PrizePicks is typically -110)",
            "push": "When player hits exactly the line (rare with .5 lines)"
        },
        "beginner_tips": [
            "Start with small bets to learn",
            "Focus on players you follow closely",  
            "Compare recent form to season averages",
            "Avoid betting on injured or resting players",
            "Don't chase losses with bigger bets"
        ]
    }

@router.post("/education/explain/{concept}")
async def explain_concept(concept: str):
    """
    Get AI explanation of any basketball or betting concept
    """
    try:
        explanation = await aws_bedrock_service.explain_betting_concepts(concept)
        return {
            "concept": concept,
            "explanation": explanation,
            "related_topics": _get_related_concepts(concept)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error explaining concept: {str(e)}")

# Helper functions
def _get_position_explanation(player_info):
    """Get explanation of player's position"""
    position = getattr(player_info, 'position', 'Unknown')
    explanations = {
        'PG': 'Point Guard - Usually the shortest player, handles the ball and runs plays',
        'SG': 'Shooting Guard - Focuses on scoring, especially from outside',
        'SF': 'Small Forward - Versatile player who can score, rebound, and defend',
        'PF': 'Power Forward - Strong player who works near the basket',
        'C': 'Center - Usually the tallest, focuses on rebounds, blocks, and close shots'
    }
    return explanations.get(position, f'Position: {position}')

def _get_stat_explanations():
    """Get explanations of all basketball stats"""
    return {
        "points": "Total points from all types of shots and free throws",
        "rebounds": "Getting the ball after missed shots", 
        "assists": "Passes that lead directly to teammates scoring",
        "steals": "Taking the ball away from opponents",
        "blocks": "Preventing opponent shots from going in",
        "turnovers": "Giving the ball to the other team (bad)",
        "3pt_made": "Successful shots from beyond the three-point line",
        "free_throws": "Uncontested 1-point shots after fouls"
    }

def _get_betting_basics():
    """Get basic betting concepts"""
    return {
        "over_bet": "Betting the player will exceed the line (get MORE than the number)",
        "under_bet": "Betting the player will stay below the line (get LESS than the number)", 
        "line": "The target number you're betting over or under",
        "confidence": "How sure you are about the bet (higher = more likely to hit)",
        "bankroll": "Total amount of money you have for betting",
        "unit": "Standard bet size (usually 1-2% of your bankroll)"
    }

def _create_prop_summary(request, prediction, stat_analysis):
    """Create a summary for a single prop bet"""
    return {
        "bet_description": f"{request.player_name} {request.prop_type.value} {request.bet_type.value} {request.line_value}",
        "ai_recommendation": prediction.recommendation,
        "confidence_level": _convert_confidence_to_words(prediction.confidence),
        "key_reason": prediction.reasoning.split('.')[0] if prediction.reasoning else "No reason provided",
        "recent_average": stat_analysis.get('last_5_average', 0),
        "season_average": stat_analysis.get('season_average', 0),
        "trend": stat_analysis.get('trend', 'stable'),
        "risk_assessment": _assess_risk_level(prediction.confidence, stat_analysis.get('consistency', 'consistent'))
    }

def _convert_confidence_to_words(confidence):
    """Convert confidence number to words"""
    if confidence >= 0.85:
        return "Very High"
    elif confidence >= 0.75:
        return "High" 
    elif confidence >= 0.65:
        return "Medium"
    elif confidence >= 0.55:
        return "Low"
    else:
        return "Very Low"

def _assess_risk_level(confidence, consistency):
    """Assess overall risk level"""
    if confidence >= 0.8 and consistency in ['very_consistent', 'consistent']:
        return "Low Risk"
    elif confidence >= 0.7:
        return "Medium Risk"
    else:
        return "High Risk"

def _extract_key_points(prediction):
    """Extract key points from prediction"""
    reasoning = prediction.reasoning
    # Extract first 2 sentences as key points
    sentences = reasoning.split('.')[:2]
    return [s.strip() for s in sentences if s.strip()]

def _get_ticket_recommendation(avg_confidence, high_risk_legs, total_legs):
    """Get recommendation for entire ticket"""
    if avg_confidence >= 0.8 and high_risk_legs == 0:
        return "RECOMMENDED - Strong confidence across all legs"
    elif avg_confidence >= 0.7 and high_risk_legs <= 1:
        return "CONSIDER - Good overall confidence with minor concerns"
    elif high_risk_legs >= total_legs // 2:
        return "AVOID - Too many uncertain legs for beginners"
    else:
        return "PROCEED WITH CAUTION - Mixed confidence levels"

def _estimate_ticket_probability(predictions):
    """Estimate probability of hitting entire ticket"""
    # Simplified calculation: multiply individual confidence levels
    overall_prob = 1.0
    for pred in predictions:
        overall_prob *= pred.confidence
    return overall_prob

def _generate_ticket_insights(legs, predictions, avg_confidence):
    """Generate educational insights about the ticket"""
    insights = []
    
    if len(legs) > 4:
        insights.append("🚨 Large tickets (5+ legs) are very hard to hit - consider smaller tickets as a beginner")
    
    if avg_confidence < 0.7:
        insights.append("⚠️ Low average confidence - this ticket has significant risk")
    
    # Count prop types
    prop_counts = {}
    for leg in legs:
        prop_type = leg.prop_type.value
        prop_counts[prop_type] = prop_counts.get(prop_type, 0) + 1
    
    if any(count > 1 for count in prop_counts.values()):
        insights.append("📊 You have multiple bets on the same stat type - consider diversifying")
    
    high_confidence_legs = [p for p in predictions if p.confidence >= 0.8]
    if high_confidence_legs:
        insights.append(f"✅ {len(high_confidence_legs)} legs have high confidence - these are your strongest picks")
    
    return insights

def _get_educational_content(prop_type):
    """Get educational content specific to prop type"""
    content_map = {
        PropType.POINTS: {
            "what_affects_it": ["Shot attempts", "Field goal percentage", "Free throws", "Playing time"],
            "beginner_tip": "Points are usually the most predictable prop - start here!",
            "red_flags": ["Player listed as questionable", "Back-to-back games", "Blowout potential"]
        },
        PropType.REBOUNDS: {
            "what_affects_it": ["Height advantage", "Opponent pace", "Team rebounding", "Playing time"],
            "beginner_tip": "Rebounds can be volatile - look for consistent rebounders",
            "red_flags": ["Facing tall teams", "Team has other good rebounders", "Player in foul trouble"]
        },
        PropType.ASSISTS: {
            "what_affects_it": ["Ball-handling role", "Teammate shooting", "Game pace", "Team offense"],
            "beginner_tip": "Assists depend on teammates making shots - consider team shooting",
            "red_flags": ["Key teammates injured", "Slow-paced game expected", "Player not primary ball-handler"]
        }
    }
    
    return content_map.get(prop_type, {
        "what_affects_it": ["Playing time", "Role in team", "Game situation"],
        "beginner_tip": "Research this stat type more before betting",
        "red_flags": ["Limited data available", "Inconsistent performance"]
    })

def _get_related_concepts(concept):
    """Get related concepts to explore"""
    related_map = {
        "points": ["field_goal_percentage", "three_pointers", "free_throws"],
        "rebounds": ["offensive_rebounds", "defensive_rebounds", "double_double"],
        "assists": ["turnovers", "assist_to_turnover_ratio", "usage_rate"],
        "over_under": ["line", "juice", "push", "bankroll_management"],
        "confidence": ["risk_management", "unit_sizing", "variance"]
    }
    
    return related_map.get(concept.lower(), ["betting_basics", "bankroll_management", "statistics"])