# FanAssist Paper Betting API Examples

This document provides examples of how to use the FanAssist Paper Betting API that simulates PrizePicks-style NBA prop betting with virtual money.

## 🚀 Getting Started

### 1. Start the API Server
```bash
cd backend
python run.py
```

### 2. Access the API Documentation
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 👤 User Management

### Create a New User Account
```python
import requests

# Create new user
user_data = {
    "username": "nba_bettor_123",
    "email": "user@example.com"
}

response = requests.post("http://localhost:8000/api/betting/users", json=user_data)
user = response.json()
print(f"Created user: {user['username']} with ${user['virtual_balance']}")
```

### Get User Account
```python
# Get user by ID
user_id = "your-user-id-here"
response = requests.get(f"http://localhost:8000/api/betting/users/{user_id}")
user = response.json()

# Or get user by username
username = "nba_bettor_123"
response = requests.get(f"http://localhost:8000/api/betting/users/username/{username}")
user = response.json()
```

## 🎯 Placing Bets

### Place a Single Prop Bet
```python
# Place bet on LeBron James points over 25.5
bet_data = {
    "player_name": "LeBron James",
    "prop_type": "points",
    "line_value": 25.5,
    "bet_type": "over",
    "wager_amount": 100.0,
    "game_date": "2024-01-15T20:00:00Z"
}

response = requests.post(
    f"http://localhost:8000/api/betting/users/{user_id}/bets",
    json=bet_data
)
bet = response.json()
print(f"Placed bet: {bet['bet_id']} for ${bet['wager_amount']}")
```

### Place Multiple Bets (Different Prop Types)
```python
# Multiple prop bets
bets = [
    {
        "player_name": "Stephen Curry",
        "prop_type": "threes_made",
        "line_value": 4.5,
        "bet_type": "over",
        "wager_amount": 50.0
    },
    {
        "player_name": "Giannis Antetokounmpo",
        "prop_type": "rebounds",
        "line_value": 11.5,
        "bet_type": "under",
        "wager_amount": 75.0
    },
    {
        "player_name": "Luka Dončić",
        "prop_type": "assists",
        "line_value": 8.5,
        "bet_type": "over",
        "wager_amount": 60.0
    },
    {
        "player_name": "Anthony Davis",
        "prop_type": "fantasy_score",
        "line_value": 45.5,
        "bet_type": "over",
        "wager_amount": 80.0
    }
]

placed_bets = []
for bet_data in bets:
    response = requests.post(
        f"http://localhost:8000/api/betting/users/{user_id}/bets",
        json=bet_data
    )
    placed_bets.append(response.json())
```

## 📊 Available PrizePicks Prop Types

### Get All Available Props
```python
response = requests.get("http://localhost:8000/api/betting/prop-types/prizepicks")
prop_types = response.json()

for prop in prop_types['prop_types']:
    print(f"{prop['display_name']}: {prop['description']}")
```

### PrizePicks Prop Types:
- **Points (Pts)**: Total points scored by the player
- **Rebounds (Reb)**: Total rebounds (offensive + defensive)
- **Assists (Asts)**: Total assists by the player
- **3-PT Made**: Three-point field goals made
- **Steals (Stls)**: Steals by the player
- **Blocked Shots (Blks)**: Blocked shots by the player
- **Turnovers**: Turnovers committed by the player
- **Fantasy Score**: PrizePicks fantasy points (1pt=1, 1reb=1.2, 1ast=1.5, 1stl=3, 1blk=3, 1to=-1)
- **Free Throws Made**: Free throw field goals made
- **Quarters/Halves with [x] Achievements**: Number of quarters/halves achieving a milestone

## 🎮 Simulating Bet Results

### Simulate Bet Settlement (For Testing)
```python
# Simulate bet with 70% win probability
bet_id = "your-bet-id-here"
response = requests.post(
    f"http://localhost:8000/api/betting/bets/{bet_id}/simulate",
    params={"win_probability": 0.7}
)
settled_bet = response.json()
print(f"Bet {settled_bet['status']}: {settled_bet['actual_result']}")
```

### Settle Bet with Actual Result
```python
# Settle bet with actual game result
actual_result_data = {"actual_result": 28.0}  # LeBron scored 28 points

response = requests.post(
    f"http://localhost:8000/api/betting/bets/{bet_id}/settle",
    json=actual_result_data
)
settled_bet = response.json()
```

## 📈 Portfolio & Analytics

### Get User Portfolio
```python
response = requests.get(f"http://localhost:8000/api/betting/users/{user_id}/portfolio")
portfolio = response.json()

print(f"Active Bets: {len(portfolio['active_bets'])}")
print(f"Pending Payout: ${portfolio['pending_payout']}")
print(f"At Risk: ${portfolio['at_risk_amount']}")
```

### Get Betting Statistics
```python
response = requests.get(f"http://localhost:8000/api/betting/users/{user_id}/stats")
stats = response.json()

print(f"Current Balance: ${stats['current_balance']}")
print(f"Win Rate: {stats['win_rate']:.1%}")
print(f"Net Profit: ${stats['net_profit']}")
print(f"Best Prop Type: {stats['best_prop_type']}")
```

### Get User Betting History
```python
# Get all bets
response = requests.get(f"http://localhost:8000/api/betting/users/{user_id}/bets")
all_bets = response.json()

# Get only pending bets
response = requests.get(
    f"http://localhost:8000/api/betting/users/{user_id}/bets",
    params={"status": "pending"}
)
pending_bets = response.json()

# Get only won bets
response = requests.get(
    f"http://localhost:8000/api/betting/users/{user_id}/bets",
    params={"status": "won"}
)
won_bets = response.json()
```

## 🏆 Leaderboards

### Get Top Winners Leaderboard
```python
# Top winners by total winnings
response = requests.get(
    "http://localhost:8000/api/betting/leaderboard",
    params={"limit": 10, "sort_by": "total_winnings"}
)
leaderboard = response.json()

print("Top Winners:")
for entry in leaderboard:
    print(f"{entry['rank']}. {entry['username']} - ${entry['total_winnings']}")
```

### Get Best Win Rate Leaderboard
```python
# Top performers by win rate
response = requests.get(
    "http://localhost:8000/api/betting/leaderboard",
    params={"limit": 10, "sort_by": "win_rate"}
)
leaderboard = response.json()

print("Best Win Rates:")
for entry in leaderboard:
    print(f"{entry['rank']}. {entry['username']} - {entry['win_rate']:.1%} ({entry['total_bets']} bets)")
```

### Get Best ROI Leaderboard
```python
# Top performers by ROI
response = requests.get(
    "http://localhost:8000/api/betting/leaderboard",
    params={"limit": 10, "sort_by": "roi"}
)
leaderboard = response.json()

print("Best ROI:")
for entry in leaderboard:
    print(f"{entry['rank']}. {entry['username']} - {entry['roi']:.1f}% ROI")
```

## 🔄 Combined NBA Analysis + Betting Workflow

### Full Workflow Example
```python
import requests

# 1. Search for a player
response = requests.get(
    "http://localhost:8000/api/players/search",
    params={"query": "LeBron James"}
)
players = response.json()
player = players[0] if players else None

if player:
    # 2. Get player's recent stats
    response = requests.get(
        f"http://localhost:8000/api/players/{player['player_id']}/stats/recent",
        params={"games": 5}
    )
    recent_stats = response.json()
    
    # 3. Analyze prop using AI
    props_analysis = {
        "props": [
            {
                "player_name": player['full_name'],
                "prop_type": "points",
                "line": 25.5
            }
        ],
        "analysis_depth": "standard"
    }
    
    response = requests.post(
        "http://localhost:8000/api/props/analyze",
        json=props_analysis
    )
    analysis = response.json()
    
    # 4. Get recommendation
    recommendation = analysis['analyses'][0]['prop_predictions'][0]
    
    print(f"AI Recommendation: {recommendation['recommendation']}")
    print(f"Confidence: {recommendation['confidence']:.1%}")
    print(f"Reasoning: {recommendation['reasoning']}")
    
    # 5. Place bet based on recommendation
    if recommendation['confidence'] > 0.7:  # Only bet if confident
        bet_data = {
            "player_name": player['full_name'],
            "prop_type": "points",
            "line_value": 25.5,
            "bet_type": recommendation['recommendation'],
            "wager_amount": min(100.0, recommendation['confidence'] * 100)  # Scale bet size by confidence
        }
        
        response = requests.post(
            f"http://localhost:8000/api/betting/users/{user_id}/bets",
            json=bet_data
        )
        bet = response.json()
        print(f"Placed ${bet['wager_amount']} bet: {bet['player_name']} {bet['prop_type']} {bet['bet_type']} {bet['line_value']}")
```

## 🎲 Demo Features

### Reset User Balance (For Testing)
```python
# Reset user balance back to $10,000 starting amount
response = requests.post(f"http://localhost:8000/api/betting/users/{user_id}/reset")
user = response.json()
print(f"Reset balance to ${user['virtual_balance']}")
```

### Get Betting Configuration
```python
response = requests.get("http://localhost:8000/api/betting/betting-config")
config = response.json()

print(f"Starting Balance: ${config['starting_balance']}")
print(f"Default Odds: {config['default_odds']}")
print(f"Max Bet: ${config['max_bet_amount']}")
print(f"Fantasy Scoring: {config['fantasy_scoring']}")
```

## 💡 Tips for Using the Paper Betting System

1. **Start Small**: Begin with small bets to learn the system
2. **Use AI Analysis**: Leverage the prop analysis endpoints for insights
3. **Track Performance**: Regularly check your stats and portfolio
4. **Diversify Props**: Try different prop types to find your strengths
5. **Bankroll Management**: Don't bet more than you can afford to lose (even with fake money!)

## 🔧 Error Handling

```python
def place_bet_safely(user_id, bet_data):
    try:
        response = requests.post(
            f"http://localhost:8000/api/betting/users/{user_id}/bets",
            json=bet_data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print(f"Invalid bet: {response.json()['detail']}")
        elif response.status_code == 404:
            print("User not found")
        else:
            print(f"Error placing bet: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

This paper betting system provides a full PrizePicks-style experience with virtual money, allowing users to practice their betting strategies risk-free!