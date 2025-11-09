from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes import players, props, analysis, betting, beginner, simulation, ml_simulation, schedule
from app.config import settings

app = FastAPI(
    title="FanAssist NBA Props & Paper Betting API",
    description="Beginner-friendly NBA prop betting analysis with AI insights and virtual money betting",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(players.router, prefix="/api/players", tags=["players"])
app.include_router(props.router, prefix="/api/props", tags=["props"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(betting.router, prefix="/api/betting", tags=["betting"])
app.include_router(beginner.router, prefix="/api/beginner", tags=["beginner"])
app.include_router(simulation.router)
app.include_router(ml_simulation.router)
app.include_router(schedule.router)

@app.get("/")
async def root():
    return {
        "message": "FanAssist NBA Props & Paper Betting API", 
        "version": "1.0.0",
        "features": [
            "NBA player stats and last 5 games analysis",
            "AI-powered prop recommendations", 
            "Paper betting with virtual money ($10,000 start)",
            "PrizePicks-style betting system",
            "Beginner-friendly analysis",
            "Game simulation",
            "Simulate games and bets to see win probabilities",
            "Leaderboards and analytics"
        ],
        "simulation_endpoints": [
            "POST /api/simulation/single-game",
            "POST /api/simulation/bet-outcome",
            "POST /api/simulation/multi-leg-ticket",
            "GET /api/simulation/quick-odds/{player_name}"
        ],
        "beginner_endpoints": [
            "GET /api/beginner/players/{player_name}/beginner-analysis",
            "POST /api/beginner/analyze-prop/beginner",
            "POST /api/beginner/analyze-ticket/beginner"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
