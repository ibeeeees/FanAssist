from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.services.aws_bedrock import aws_bedrock_service

router = APIRouter()

@router.post("/betting-insights")
async def get_betting_insights(context: Dict[str, Any]):
    """
    Get general betting insights and recommendations based on provided context
    """
    try:
        context_str = str(context.get("query", ""))
        if not context_str:
            raise HTTPException(status_code=400, detail="Context query is required")
        
        insights = await aws_bedrock_service.get_general_betting_insights(context_str)
        return {"insights": insights, "context": context_str}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")

@router.get("/market-overview")
async def get_market_overview():
    """
    Get general NBA betting market overview
    """
    try:
        # This could be enhanced to provide real market data
        overview_context = """
        Provide a general overview of the current NBA betting market, 
        including key trends, popular prop types, and general advice for PrizePicks betting.
        """
        
        insights = await aws_bedrock_service.get_general_betting_insights(overview_context)
        return {
            "market_overview": insights,
            "generated_at": "2024-01-01T00:00:00Z",  # This would be current time
            "disclaimer": "This is AI-generated analysis for entertainment purposes only. Always gamble responsibly."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating market overview: {str(e)}")

@router.get("/recommendations/general")
async def get_general_recommendations():
    """
    Get general betting recommendations and strategies
    """
    return {
        "recommendations": [
            {
                "category": "Bankroll Management",
                "advice": "Never bet more than 1-2% of your total bankroll on a single prop"
            },
            {
                "category": "Research",
                "advice": "Always check injury reports and recent player performance trends"
            },
            {
                "category": "Value Betting",
                "advice": "Look for props where your predicted probability is significantly higher than implied odds"
            },
            {
                "category": "Prop Selection",
                "advice": "Focus on props for players with consistent usage and predictable roles"
            },
            {
                "category": "Timing",
                "advice": "Line shopping and early analysis can provide better value before public betting moves lines"
            }
        ],
        "disclaimer": "These are general guidelines. Always do your own research and bet responsibly."
    }