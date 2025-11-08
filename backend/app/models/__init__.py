from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PropType(str, Enum):
    POINTS = "points"  # Points (Pts)
    REBOUNDS = "rebounds"  # Rebounds (Reb)
    ASSISTS = "assists"  # Assists (Asts)
    THREES_MADE = "threes_made"  # 3-PT Made
    STEALS = "steals"  # Steals (Stls)
    BLOCKS = "blocks"  # Blocked Shots (Blks)
    TURNOVERS = "turnovers"  # Turnovers
    FANTASY_SCORE = "fantasy_score"  # Fantasy Score
    FREE_THROWS_MADE = "free_throws_made"  # Free Throws Made
    QUARTERS_WITH_STAT = "quarters_with_stat"  # Quarters/Halves with [x] Statistical Achievements

class PlayerInfo(BaseModel):
    player_id: int
    full_name: str
    first_name: str
    last_name: str
    team_id: int
    team_name: str
    team_abbreviation: str
    position: str
    height: Optional[str] = None
    weight: Optional[str] = None
    years_pro: Optional[int] = None

class GameStats(BaseModel):
    game_id: str
    player_id: int
    game_date: datetime
    opponent: str
    is_home: bool
    minutes_played: Optional[float] = None
    points: Optional[int] = None
    rebounds: Optional[int] = None
    assists: Optional[int] = None
    steals: Optional[int] = None
    blocks: Optional[int] = None
    turnovers: Optional[int] = None
    field_goals_made: Optional[int] = None
    field_goals_attempted: Optional[int] = None
    three_pointers_made: Optional[int] = None
    three_pointers_attempted: Optional[int] = None
    free_throws_made: Optional[int] = None
    free_throws_attempted: Optional[int] = None
    plus_minus: Optional[int] = None
    fantasy_score: Optional[float] = None
    
    def calculate_fantasy_score(self) -> Optional[float]:
        """Calculate PrizePicks-style fantasy score"""
        if not all([self.points, self.rebounds, self.assists, self.steals, self.blocks]):
            return None
        
        # PrizePicks fantasy scoring: 1pt = 1, 1reb = 1.2, 1ast = 1.5, 1stl = 3, 1blk = 3, 1to = -1
        score = (
            (self.points or 0) * 1.0 +
            (self.rebounds or 0) * 1.2 +
            (self.assists or 0) * 1.5 +
            (self.steals or 0) * 3.0 +
            (self.blocks or 0) * 3.0 -
            (self.turnovers or 0) * 1.0
        )
        return round(score, 1)

class SeasonAverages(BaseModel):
    player_id: int
    season: str
    games_played: int
    minutes_per_game: float
    points_per_game: float
    rebounds_per_game: float
    assists_per_game: float
    steals_per_game: float
    blocks_per_game: float
    turnovers_per_game: float
    field_goal_percentage: float
    three_point_percentage: float
    free_throw_percentage: float

class PropPrediction(BaseModel):
    prop_type: PropType
    predicted_value: float
    confidence: float  # 0-1 scale
    line_value: Optional[float] = None
    recommendation: str  # "over", "under", or "avoid"
    reasoning: str

class PlayerAnalysis(BaseModel):
    player_info: PlayerInfo
    recent_stats: List[GameStats]
    season_averages: SeasonAverages
    prop_predictions: List[PropPrediction]
    injury_status: Optional[str] = None
    matchup_analysis: Optional[str] = None
    confidence_score: float  # Overall confidence in predictions

class PrizePicksProp(BaseModel):
    player_name: str
    prop_type: PropType
    line: float
    odds: Optional[str] = None
    
class PropAnalysisRequest(BaseModel):
    props: List[PrizePicksProp]
    analysis_depth: str = "standard"  # "quick", "standard", "deep"

class PropAnalysisResponse(BaseModel):
    analyses: List[PlayerAnalysis]
    overall_recommendation: str
    confidence_score: float
    generated_at: datetime

# Paper Betting System Models

class UserAccount(BaseModel):
    user_id: str
    username: str
    email: str
    virtual_balance: float = 10000.0  # Starting with $10,000 fake money
    total_winnings: float = 0.0
    total_losses: float = 0.0
    total_bets: int = 0
    win_rate: float = 0.0
    created_at: datetime
    last_active: datetime

class BetStatus(str, Enum):
    PENDING = "pending"
    WON = "won"
    LOST = "lost"
    PUSHED = "pushed"  # Tie/exact hit
    CANCELLED = "cancelled"

class BetType(str, Enum):
    OVER = "over"
    UNDER = "under"

class Bet(BaseModel):
    bet_id: str
    user_id: str
    player_name: str
    prop_type: PropType
    line_value: float
    bet_type: BetType  # over/under
    wager_amount: float
    potential_payout: float
    odds: float = 1.9  # Default PrizePicks-style odds
    status: BetStatus = BetStatus.PENDING
    placed_at: datetime
    settled_at: Optional[datetime] = None
    actual_result: Optional[float] = None
    game_id: Optional[str] = None
    game_date: Optional[datetime] = None

class BetSlip(BaseModel):
    user_id: str
    bets: List[Dict[str, Any]]  # List of bet selections before placement
    total_wager: float
    potential_total_payout: float
    estimated_odds: float

class Leaderboard(BaseModel):
    rank: int
    username: str
    total_winnings: float
    win_rate: float
    total_bets: int
    roi: float  # Return on Investment

class BettingStats(BaseModel):
    user_id: str
    current_balance: float
    total_wagered: float
    total_winnings: float
    net_profit: float
    win_rate: float
    average_bet_size: float
    biggest_win: float
    biggest_loss: float
    favorite_prop_type: Optional[PropType] = None
    best_prop_type: Optional[PropType] = None  # Best performing prop type
    
class Portfolio(BaseModel):
    user_id: str
    active_bets: List[Bet]
    recent_bets: List[Bet]
    pending_payout: float
    at_risk_amount: float