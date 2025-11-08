from fastapi import APIRouter, HTTPException
from typing import List
from app.models import PropAnalysisRequest, PropAnalysisResponse, PropPrediction, PropType
from app.services.prizepicks import prizepicks_service

router = APIRouter()

@router.post("/analyze", response_model=PropAnalysisResponse)
async def analyze_props(request: PropAnalysisRequest):
    """
    Analyze multiple PrizePicks props and get AI-powered recommendations
    """
    try:
        if not request.props:
            raise HTTPException(status_code=400, detail="No props provided for analysis")
        
        analysis = await prizepicks_service.analyze_props(request)
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing props: {str(e)}")

@router.get("/quick/{player_name}")
async def quick_prop_analysis(
    player_name: str,
    prop_type: PropType,
    line: float
):
    """
    Get quick analysis for a single player prop
    """
    try:
        prediction = await prizepicks_service.get_player_quick_analysis(player_name, prop_type, line)
        if not prediction:
            raise HTTPException(status_code=404, detail="Unable to analyze prop")
        return prediction
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in quick analysis: {str(e)}")

@router.get("/trending")
async def get_trending_props(limit: int = 10):
    """
    Get trending props based on recent player performance
    """
    try:
        trending = await prizepicks_service.get_trending_props(limit)
        return {"trending_props": trending}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trending props: {str(e)}")

@router.get("/prop-types")
async def get_available_prop_types():
    """
    Get list of available prop types for analysis
    """
    return {
        "prop_types": [
            {"value": prop.value, "display_name": prop.value.replace("_", " ").title()}
            for prop in PropType
        ]
    }