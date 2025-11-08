import uuid
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.models import (
    UserAccount, Bet, BetSlip, BetStatus, BetType, PropType, 
    Leaderboard, BettingStats, Portfolio
)
import json
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class PaperBettingService:
    """
    Paper betting service for virtual money NBA props betting
    This simulates PrizePicks-style betting with fake money
    """
    
    def __init__(self):
        # In-memory storage (in production, this would be a database)
        self.users: Dict[str, UserAccount] = {}
        self.bets: Dict[str, Bet] = {}
        self.bet_slips: Dict[str, BetSlip] = {}
        
        # PrizePicks-style configuration
        self.starting_balance = 10000.0
        self.default_odds = 1.9  # PrizePicks standard odds
        self.max_bet_amount = 1000.0
        self.min_bet_amount = 1.0
        
    async def create_user_account(self, username: str, email: str) -> UserAccount:
        """Create a new user account with starting virtual money"""
        user_id = str(uuid.uuid4())
        
        if any(user.username == username for user in self.users.values()):
            raise ValueError("Username already exists")
        
        if any(user.email == email for user in self.users.values()):
            raise ValueError("Email already exists")
        
        user = UserAccount(
            user_id=user_id,
            username=username,
            email=email,
            virtual_balance=self.starting_balance,
            created_at=datetime.now(),
            last_active=datetime.now()
        )
        
        self.users[user_id] = user
        logger.info(f"Created new user account: {username} with $${self.starting_balance}")
        return user
    
    async def get_user_account(self, user_id: str) -> Optional[UserAccount]:
        """Get user account by ID"""
        return self.users.get(user_id)
    
    async def get_user_by_username(self, username: str) -> Optional[UserAccount]:
        """Get user account by username"""
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    async def place_bet(
        self, 
        user_id: str, 
        player_name: str,
        prop_type: PropType,
        line_value: float,
        bet_type: BetType,
        wager_amount: float,
        game_date: Optional[datetime] = None
    ) -> Bet:
        """Place a single prop bet"""
        
        # Validate user
        user = await self.get_user_account(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Validate bet amount
        if wager_amount < self.min_bet_amount:
            raise ValueError(f"Minimum bet is ${self.min_bet_amount}")
        
        if wager_amount > self.max_bet_amount:
            raise ValueError(f"Maximum bet is ${self.max_bet_amount}")
        
        if wager_amount > user.virtual_balance:
            raise ValueError("Insufficient balance")
        
        # Calculate payout
        potential_payout = wager_amount * self.default_odds
        
        # Create bet
        bet_id = str(uuid.uuid4())
        bet = Bet(
            bet_id=bet_id,
            user_id=user_id,
            player_name=player_name,
            prop_type=prop_type,
            line_value=line_value,
            bet_type=bet_type,
            wager_amount=wager_amount,
            potential_payout=potential_payout,
            odds=self.default_odds,
            placed_at=datetime.now(),
            game_date=game_date or datetime.now() + timedelta(hours=2)  # Default to 2 hours from now
        )
        
        # Deduct from user balance
        user.virtual_balance -= wager_amount
        user.total_bets += 1
        user.last_active = datetime.now()
        
        # Store bet
        self.bets[bet_id] = bet
        self.users[user_id] = user
        
        logger.info(f"Placed bet: {player_name} {prop_type.value} {bet_type.value} {line_value} for ${wager_amount}")
        return bet
    
    async def settle_bet(self, bet_id: str, actual_result: float) -> Bet:
        """Settle a bet based on actual game result"""
        bet = self.bets.get(bet_id)
        if not bet:
            raise ValueError("Bet not found")
        
        if bet.status != BetStatus.PENDING:
            raise ValueError("Bet already settled")
        
        user = self.users.get(bet.user_id)
        if not user:
            raise ValueError("User not found")
        
        # Determine bet result
        if actual_result == bet.line_value:
            # Push - return original wager
            bet.status = BetStatus.PUSHED
            user.virtual_balance += bet.wager_amount
            logger.info(f"Bet pushed: {bet_id}")
        elif (bet.bet_type == BetType.OVER and actual_result > bet.line_value) or \
             (bet.bet_type == BetType.UNDER and actual_result < bet.line_value):
            # Win
            bet.status = BetStatus.WON
            user.virtual_balance += bet.potential_payout
            user.total_winnings += (bet.potential_payout - bet.wager_amount)
            logger.info(f"Bet won: {bet_id} - Payout: ${bet.potential_payout}")
        else:
            # Loss
            bet.status = BetStatus.LOST
            user.total_losses += bet.wager_amount
            logger.info(f"Bet lost: {bet_id}")
        
        # Update bet
        bet.actual_result = actual_result
        bet.settled_at = datetime.now()
        
        # Update user stats
        wins = sum(1 for b in self.bets.values() if b.user_id == bet.user_id and b.status == BetStatus.WON)
        total_settled = sum(1 for b in self.bets.values() if b.user_id == bet.user_id and b.status in [BetStatus.WON, BetStatus.LOST])
        user.win_rate = (wins / total_settled) if total_settled > 0 else 0.0
        
        # Store updates
        self.bets[bet_id] = bet
        self.users[bet.user_id] = user
        
        return bet
    
    async def get_user_portfolio(self, user_id: str) -> Portfolio:
        """Get user's betting portfolio"""
        user_bets = [bet for bet in self.bets.values() if bet.user_id == user_id]
        
        active_bets = [bet for bet in user_bets if bet.status == BetStatus.PENDING]
        recent_bets = sorted(
            [bet for bet in user_bets if bet.status != BetStatus.PENDING],
            key=lambda x: x.settled_at or x.placed_at,
            reverse=True
        )[:20]  # Last 20 settled bets
        
        pending_payout = sum(bet.potential_payout for bet in active_bets)
        at_risk_amount = sum(bet.wager_amount for bet in active_bets)
        
        return Portfolio(
            user_id=user_id,
            active_bets=active_bets,
            recent_bets=recent_bets,
            pending_payout=pending_payout,
            at_risk_amount=at_risk_amount
        )
    
    async def get_betting_stats(self, user_id: str) -> BettingStats:
        """Get comprehensive betting statistics for a user"""
        user = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        user_bets = [bet for bet in self.bets.values() if bet.user_id == user_id]
        settled_bets = [bet for bet in user_bets if bet.status in [BetStatus.WON, BetStatus.LOST]]
        won_bets = [bet for bet in settled_bets if bet.status == BetStatus.WON]
        
        total_wagered = sum(bet.wager_amount for bet in user_bets)
        total_winnings = sum(bet.potential_payout for bet in won_bets)
        net_profit = user.virtual_balance - self.starting_balance
        
        # Analyze prop type performance
        prop_counts = defaultdict(int)
        prop_wins = defaultdict(int)
        
        for bet in user_bets:
            prop_counts[bet.prop_type] += 1
            if bet.status == BetStatus.WON:
                prop_wins[bet.prop_type] += 1
        
        favorite_prop = max(prop_counts.items(), key=lambda x: x[1])[0] if prop_counts else None
        best_prop = None
        if prop_wins:
            best_win_rate = 0
            for prop_type, wins in prop_wins.items():
                total = prop_counts[prop_type]
                win_rate = wins / total if total > 0 else 0
                if win_rate > best_win_rate and total >= 3:  # Minimum 3 bets
                    best_win_rate = win_rate
                    best_prop = prop_type
        
        return BettingStats(
            user_id=user_id,
            current_balance=user.virtual_balance,
            total_wagered=total_wagered,
            total_winnings=user.total_winnings,
            net_profit=net_profit,
            win_rate=user.win_rate,
            average_bet_size=total_wagered / len(user_bets) if user_bets else 0,
            biggest_win=max((bet.potential_payout - bet.wager_amount for bet in won_bets), default=0),
            biggest_loss=max((bet.wager_amount for bet in settled_bets if bet.status == BetStatus.LOST), default=0),
            favorite_prop_type=favorite_prop,
            best_prop_type=best_prop
        )
    
    async def get_leaderboard(self, limit: int = 10, sort_by: str = "total_winnings") -> List[Leaderboard]:
        """Get leaderboard of top performers"""
        users_list = list(self.users.values())
        
        # Calculate ROI for each user
        leaderboard_entries = []
        for user in users_list:
            total_wagered = sum(bet.wager_amount for bet in self.bets.values() if bet.user_id == user.user_id)
            roi = ((user.virtual_balance - self.starting_balance) / self.starting_balance * 100) if self.starting_balance > 0 else 0
            
            leaderboard_entries.append(Leaderboard(
                rank=0,  # Will be set after sorting
                username=user.username,
                total_winnings=user.total_winnings,
                win_rate=user.win_rate,
                total_bets=user.total_bets,
                roi=roi
            ))
        
        # Sort based on criteria
        if sort_by == "win_rate":
            leaderboard_entries.sort(key=lambda x: (x.win_rate, x.total_bets), reverse=True)
        elif sort_by == "roi":
            leaderboard_entries.sort(key=lambda x: x.roi, reverse=True)
        else:  # total_winnings
            leaderboard_entries.sort(key=lambda x: x.total_winnings, reverse=True)
        
        # Set ranks
        for i, entry in enumerate(leaderboard_entries[:limit], 1):
            entry.rank = i
        
        return leaderboard_entries[:limit]
    
    async def simulate_bet_settlement(self, bet_id: str, win_probability: float = 0.5) -> Bet:
        """Simulate bet settlement for testing (randomly determine outcome)"""
        import random
        
        bet = self.bets.get(bet_id)
        if not bet:
            raise ValueError("Bet not found")
        
        # Simulate a result based on the line and bet type
        if random.random() < win_probability:
            # Make it a winning bet
            if bet.bet_type == BetType.OVER:
                actual_result = bet.line_value + random.uniform(0.5, 5.0)
            else:  # UNDER
                actual_result = bet.line_value - random.uniform(0.5, 5.0)
        else:
            # Make it a losing bet
            if bet.bet_type == BetType.OVER:
                actual_result = bet.line_value - random.uniform(0.5, 5.0)
            else:  # UNDER
                actual_result = bet.line_value + random.uniform(0.5, 5.0)
        
        return await self.settle_bet(bet_id, max(0, actual_result))  # Ensure non-negative
    
    async def reset_user_balance(self, user_id: str) -> UserAccount:
        """Reset user balance to starting amount (for testing/demo purposes)"""
        user = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        user.virtual_balance = self.starting_balance
        user.total_winnings = 0.0
        user.total_losses = 0.0
        user.total_bets = 0
        user.win_rate = 0.0
        
        # Remove all user's bets
        user_bet_ids = [bet_id for bet_id, bet in self.bets.items() if bet.user_id == user_id]
        for bet_id in user_bet_ids:
            del self.bets[bet_id]
        
        self.users[user_id] = user
        logger.info(f"Reset balance for user {user.username}")
        return user

# Create singleton instance
paper_betting_service = PaperBettingService()