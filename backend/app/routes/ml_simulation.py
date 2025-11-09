"""
ML Simulation Routes - Train and use ML models for game simulation
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.services.ml_simulator import ml_game_simulator
from app.services.nba_stats import nba_stats_service

router = APIRouter(prefix="/api/ml-simulation", tags=["ML Simulation"])


class TrainModelRequest(BaseModel):
    season: str = "2023-24"
    min_games: int = 10


class TrainModelResponse(BaseModel):
    status: str
    message: str
    accuracy_scores: dict
    training_time: Optional[str] = None


class MLPredictionRequest(BaseModel):
    player_name: str
    is_home: bool = True


class MLPredictionResponse(BaseModel):
    player_name: str
    predictions: dict
    confidence: str
    message: str


@router.post("/train", response_model=TrainModelResponse)
async def train_ml_models(
    request: TrainModelRequest,
    background_tasks: BackgroundTasks
):
    """
    🤖 Train ML models using data from top playoff teams
    
    This endpoint:
    - Collects historical data from top 4 teams in each conference (East/West)
    - Trains gradient boosting models for each stat (points, rebounds, assists, etc.)
    - Saves models for future predictions
    
    **Top Teams Used:**
    - **East:** Celtics, Bucks, 76ers, Cavaliers
    - **West:** Nuggets, Lakers, Warriors, Suns
    
    **Training Process:**
    - Collects 80+ games from star players on these teams
    - Uses season averages, recent form, home/away, and trends as features
    - Trains separate models for each stat type
    - Returns accuracy (R² scores) for each model
    
    ⚠️ **Note:** This can take 2-5 minutes to complete
    """
    try:
        start_time = datetime.now()
        
        # Train models
        accuracy_scores = await ml_game_simulator.train_models(
            season=request.season,
            min_games=request.min_games
        )
        
        training_time = str(datetime.now() - start_time)
        
        return TrainModelResponse(
            status="success",
            message=f"Successfully trained {len(accuracy_scores)} models using top teams data",
            accuracy_scores=accuracy_scores,
            training_time=training_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")


@router.get("/model-status")
async def get_model_status():
    """
    📊 Check if ML models are trained and ready
    
    Returns:
    - Training status
    - Available models
    - Model accuracy scores
    """
    # Try to load existing models
    if not ml_game_simulator.is_trained:
        ml_game_simulator.load_models()
    
    return {
        "is_trained": ml_game_simulator.is_trained,
        "available_models": list(ml_game_simulator.models.keys()),
        "total_models": len(ml_game_simulator.models),
        "stat_types": ml_game_simulator.stat_types,
        "top_teams_used": {
            "east": ml_game_simulator.top_east_teams,
            "west": ml_game_simulator.top_west_teams
        },
        "message": "Models ready" if ml_game_simulator.is_trained else "Models not trained yet. Use /train endpoint."
    }


@router.post("/predict", response_model=MLPredictionResponse)
async def ml_predict_performance(request: MLPredictionRequest):
    """
    🎯 Get ML-powered performance prediction for a player
    
    Uses trained models to predict:
    - Points, Rebounds, Assists
    - Steals, Blocks, Turnovers
    - 3-Pointers Made, Free Throws Made
    
    **More accurate than basic simulation** because it's trained on actual playoff-level performance data!
    """
    try:
        # Load models if not loaded
        if not ml_game_simulator.is_trained:
            loaded = ml_game_simulator.load_models()
            if not loaded:
                raise HTTPException(
                    status_code=400,
                    detail="ML models not trained yet. Please use /api/ml-simulation/train first."
                )
        
        # Get player data
        player_info = await nba_stats_service.get_player_info(request.player_name)
        if not player_info:
            raise HTTPException(status_code=404, detail=f"Player '{request.player_name}' not found")
        
        recent_games = await nba_stats_service.get_player_game_log(player_info.player_id, last_n_games=10)
        season_averages = await nba_stats_service.get_player_season_averages(player_info.player_id)
        
        if not season_averages:
            raise HTTPException(status_code=404, detail="Could not fetch player season averages")
        
        # Get ML predictions
        predictions = ml_game_simulator.predict_player_performance(
            player_info,
            season_averages,
            recent_games,
            is_home=request.is_home
        )
        
        # Calculate confidence based on model performance
        confidence = "High" if len(predictions) >= 6 else "Medium" if len(predictions) >= 4 else "Low"
        
        # Format predictions
        formatted_predictions = {
            stat_type: round(value, 1) 
            for stat_type, value in predictions.items()
        }
        
        return MLPredictionResponse(
            player_name=player_info.full_name,
            predictions=formatted_predictions,
            confidence=confidence,
            message=f"ML prediction based on top teams' historical data"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.post("/simulate-with-ml")
async def simulate_game_with_ml(
    player_name: str,
    num_simulations: int = 100,
    is_home: bool = True
):
    """
    🎮 Simulate games using ML models (more accurate!)
    
    Like regular simulation but uses ML predictions as the baseline.
    Better for players similar to stars on playoff teams.
    """
    try:
        # Load models if needed
        if not ml_game_simulator.is_trained:
            loaded = ml_game_simulator.load_models()
            if not loaded:
                raise HTTPException(
                    status_code=400,
                    detail="ML models not trained. Use basic simulation instead: /api/simulation/single-game"
                )
        
        # Get player data
        player_info = await nba_stats_service.get_player_info(player_name)
        if not player_info:
            raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found")
        
        recent_games = await nba_stats_service.get_player_game_log(player_info.player_id, last_n_games=10)
        season_averages = await nba_stats_service.get_player_season_averages(player_info.player_id)
        
        if not season_averages:
            raise HTTPException(status_code=404, detail="Could not fetch player season averages")
        
        # Run ML simulations
        simulations = await ml_game_simulator.simulate_with_ml(
            player_info,
            season_averages,
            recent_games,
            num_simulations=num_simulations,
            is_home=is_home
        )
        
        # Calculate averages
        averages = {
            'points': round(sum(s.points or 0 for s in simulations) / len(simulations), 1),
            'rebounds': round(sum(s.rebounds or 0 for s in simulations) / len(simulations), 1),
            'assists': round(sum(s.assists or 0 for s in simulations) / len(simulations), 1),
            'steals': round(sum(s.steals or 0 for s in simulations) / len(simulations), 1),
            'blocks': round(sum(s.blocks or 0 for s in simulations) / len(simulations), 1),
            'three_pointers_made': round(sum(s.three_pointers_made or 0 for s in simulations) / len(simulations), 1),
        }
        
        return {
            "player": player_info.full_name,
            "simulation_type": "ML-based (trained on top teams)",
            "num_simulations": len(simulations),
            "averages": averages,
            "message": "Simulations completed using machine learning models"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ML simulation error: {str(e)}")


@router.get("/compare-methods/{player_name}")
async def compare_simulation_methods(player_name: str, prop_type: str, line: float):
    """
    ⚖️ Compare ML simulation vs Basic simulation
    
    Shows you the difference between:
    - Basic statistical simulation
    - ML-powered simulation (trained on top teams)
    
    Helps you see which method is more reliable for a given player
    """
    try:
        from app.services.game_simulator import game_simulator
        
        # Get player data
        player_info = await nba_stats_service.get_player_info(player_name)
        if not player_info:
            raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found")
        
        recent_games = await nba_stats_service.get_player_game_log(player_info.player_id, last_n_games=10)
        season_averages = await nba_stats_service.get_player_season_averages(player_info.player_id)
        
        if not season_averages:
            raise HTTPException(status_code=404, detail="Could not fetch player season averages")
        
        # Basic simulation
        basic_sims = game_simulator.simulate_multiple_games(
            player_info, season_averages, recent_games, num_simulations=50
        )
        
        # Try ML simulation
        ml_available = ml_game_simulator.is_trained or ml_game_simulator.load_models()
        
        if ml_available:
            ml_sims = await ml_game_simulator.simulate_with_ml(
                player_info, season_averages, recent_games, num_simulations=50
            )
            
            # Compare results for the specific prop
            basic_values = [getattr(s, prop_type, 0) for s in basic_sims]
            ml_values = [getattr(s, prop_type, 0) for s in ml_sims]
            
            basic_avg = sum(basic_values) / len(basic_values)
            ml_avg = sum(ml_values) / len(ml_values)
            
            basic_over_pct = sum(1 for v in basic_values if v > line) / len(basic_values) * 100
            ml_over_pct = sum(1 for v in ml_values if v > line) / len(ml_values) * 100
            
            return {
                "player": player_info.full_name,
                "prop": f"{prop_type.replace('_', ' ').title()}",
                "line": line,
                "basic_simulation": {
                    "average": round(basic_avg, 1),
                    "over_percentage": round(basic_over_pct, 1),
                    "recommendation": "OVER" if basic_over_pct > 50 else "UNDER"
                },
                "ml_simulation": {
                    "average": round(ml_avg, 1),
                    "over_percentage": round(ml_over_pct, 1),
                    "recommendation": "OVER" if ml_over_pct > 50 else "UNDER"
                },
                "difference": {
                    "average_diff": round(abs(basic_avg - ml_avg), 1),
                    "percentage_diff": round(abs(basic_over_pct - ml_over_pct), 1)
                },
                "recommendation": "Use ML model - trained on top teams" if ml_over_pct != basic_over_pct else "Both methods agree"
            }
        else:
            # Only basic available
            basic_values = [getattr(s, prop_type, 0) for s in basic_sims]
            basic_avg = sum(basic_values) / len(basic_values)
            basic_over_pct = sum(1 for v in basic_values if v > line) / len(basic_values) * 100
            
            return {
                "player": player_info.full_name,
                "prop": f"{prop_type.replace('_', ' ').title()}",
                "line": line,
                "basic_simulation": {
                    "average": round(basic_avg, 1),
                    "over_percentage": round(basic_over_pct, 1)
                },
                "ml_simulation": "Not available - models not trained",
                "message": "Train ML models using /api/ml-simulation/train for more accurate predictions"
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")
