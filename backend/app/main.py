from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes import players, props, analysis, betting, beginner
from app.config import settings

app = FastAPI(
    title="FanAssist NBA Props & Paper Betting API",
    description="Beginner-friendly NBA prop betting analysis with AI insights and virtual money betting",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
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

@app.get("/")
async def root():
    return {
        "message": "FanAssist NBA Props & Paper Betting API", 
        "version": "1.0.0",
        "features": [
            "🏀 NBA player stats and last 5 games analysis",
            "🤖 AI-powered prop recommendations with explanations", 
            "💰 Paper betting with virtual money ($10,000 start)",
            "🎯 PrizePicks-style betting system",
            "📚 Beginner-friendly analysis with basketball education",
            "🎮 Game simulation and leg-by-leg feedback",
            "🏆 Leaderboards and detailed analytics",
            "📊 Pros/cons analysis with basketball terminology"
        ],
        "beginner_endpoints": [
            "GET /api/beginner/players/{player_name}/beginner-analysis - Full player breakdown",
            "POST /api/beginner/analyze-prop/beginner - Single prop with explanations", 
            "POST /api/beginner/analyze-ticket/beginner - Multi-leg ticket analysis",
            "GET /api/beginner/education/basketball-terms - Learn basketball concepts",
            "POST /api/beginner/education/explain/{concept} - AI concept explanations"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)