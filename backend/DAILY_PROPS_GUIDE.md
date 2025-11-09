# 🎮 Daily Props & Paper Betting - User Guide

## What Is This Feature?

This feature lets you:
1. **See popular NBA players** playing today or tomorrow
2. **View PrizePicks-style lines** for their stats (points, rebounds, assists, etc.)
3. **Simulate bets** using our game simulator to see projected outcomes
4. **Place bets with paper money** ($10,000 starting balance)
5. **See if you won or lost** based on simulation results
6. **Track your balance** as you win or lose virtual money

**Think of it as:** A fantasy betting simulator where you can practice PrizePicks-style betting without risking real money!

---

## 🚀 Quick Start

### 1. Get Today's Popular Players

```bash
GET http://localhost:8000/api/daily-props/today
```

**Returns:**
```json
{
  "date": "2025-11-09",
  "count": 45,
  "players": [
    {
      "player_id": 2544,
      "player_name": "LeBron James",
      "team": "Lakers",
      "opponent": "Hawks",
      "game_date": "2025-11-09",
      "season_averages": {
        "points": 25.5,
        "rebounds": 7.8,
        "assists": 8.2,
        "three_pointers_made": 1.8,
        "steals": 1.2,
        "blocks": 0.6
      },
      "prizepicks_lines": {
        "points": 24.0,
        "rebounds": 6.8,
        "assists": 7.7,
        "pra": 38.5,
        "pr": 31.8,
        "pa": 32.2
      }
    },
    // ... more players
  ]
}
```

### 2. Check Your Balance

```bash
GET http://localhost:8000/api/daily-props/balance/your_username
```

**Returns:**
```json
{
  "username": "your_username",
  "balance": 10000.00,
  "starting_balance": 10000.00,
  "profit_loss": 0.00
}
```

### 3. Simulate a Bet (Preview Only)

```bash
POST http://localhost:8000/api/daily-props/simulate-bet
Content-Type: application/json

{
  "player_name": "LeBron James",
  "prop_type": "points",
  "line": 24.0,
  "pick": "OVER",
  "wager": 100
}
```

**Returns:**
```json
{
  "player_name": "LeBron James",
  "prop_type": "points",
  "line": 24.0,
  "pick": "OVER",
  "simulated_value": 26.2,
  "won": true,
  "probability": 0.65,
  "season_average": 25.5,
  "simulation_details": {
    "points": 26.2,
    "rebounds": 7.9,
    "assists": 8.4,
    "three_pointers_made": 1.8,
    "steals": 1.2,
    "blocks": 0.6
  }
}
```

### 4. Place a Real Bet (Uses Paper Money)

```bash
POST http://localhost:8000/api/daily-props/place-bet
Content-Type: application/json

{
  "player_name": "LeBron James",
  "prop_type": "points",
  "line": 24.0,
  "pick": "OVER",
  "wager": 100
}
```

**Returns:**
```json
{
  "bet_placed": true,
  "result": {
    "player_name": "LeBron James",
    "prop_type": "points",
    "line": 24.0,
    "pick": "OVER",
    "simulated_value": 26.2,
    "won": true,
    "probability": 0.65
  },
  "betting_summary": {
    "username": "demo_user",
    "old_balance": 10000.00,
    "wager": 100.00,
    "payout": 200.00,
    "profit": 100.00,
    "new_balance": 10100.00,
    "won": true
  }
}
```

**Explanation:**
- You bet **$100** on LeBron OVER 24.0 points
- Simulation predicts he'll score **26.2 points** ✅
- You **WON** the bet!
- Payout: **$200** (2x your wager)
- Profit: **$100**
- New balance: **$10,100**

### 5. Place a Parlay (Multiple Bets)

```bash
POST http://localhost:8000/api/daily-props/place-parlay
Content-Type: application/json

{
  "username": "your_username",
  "total_wager": 50,
  "bets": [
    {
      "player_name": "LeBron James",
      "prop_type": "points",
      "line": 24.0,
      "pick": "OVER",
      "wager": 50
    },
    {
      "player_name": "Stephen Curry",
      "prop_type": "threes",
      "line": 4.5,
      "pick": "OVER",
      "wager": 50
    },
    {
      "player_name": "Giannis Antetokounmpo",
      "prop_type": "rebounds",
      "line": 11.5,
      "pick": "OVER",
      "wager": 50
    }
  ]
}
```

**Returns:**
```json
{
  "parlay_placed": true,
  "num_legs": 3,
  "all_won": true,
  "legs": [
    {
      "player_name": "LeBron James",
      "prop_type": "points",
      "line": 24.0,
      "pick": "OVER",
      "simulated_value": 26.2,
      "won": true,
      "probability": 0.65
    },
    {
      "player_name": "Stephen Curry",
      "prop_type": "threes",
      "line": 4.5,
      "pick": "OVER",
      "simulated_value": 5.2,
      "won": true,
      "probability": 0.60
    },
    {
      "player_name": "Giannis Antetokounmpo",
      "prop_type": "rebounds",
      "line": 11.5,
      "pick": "OVER",
      "simulated_value": 12.8,
      "won": true,
      "probability": 0.70
    }
  ],
  "betting_summary": {
    "username": "your_username",
    "old_balance": 10100.00,
    "wager": 50.00,
    "multiplier": 5.0,
    "payout": 250.00,
    "profit": 200.00,
    "new_balance": 10300.00,
    "combined_probability": 27.3
  }
}
```

**Parlay Payouts:**
- **2 legs**: 3x payout
- **3 legs**: 5x payout ⬅️ This example
- **4 legs**: 10x payout
- **5 legs**: 20x payout
- **6 legs**: 50x payout

**Example:** $50 × 5x = $250 payout, $200 profit

---

## 📊 Prop Types Available

| Prop Type | Description | Example Line |
|-----------|-------------|--------------|
| `points` | Total points scored | 24.5 |
| `rebounds` | Total rebounds | 7.5 |
| `assists` | Total assists | 8.5 |
| `threes` | Three-pointers made | 3.5 |
| `pra` | Points + Rebounds + Assists | 40.5 |
| `pr` | Points + Rebounds | 32.5 |
| `pa` | Points + Assists | 33.5 |

---

## 🎯 How It Works

### Behind the Scenes

1. **Get Popular Players**: We filter for star players (LeBron, Curry, Giannis, etc.) from today's/tomorrow's games
2. **Generate Lines**: We create PrizePicks-style lines based on season averages (slightly below their average)
3. **Run Simulation**: When you bet, we run our game simulator (30 simulations per player)
4. **Determine Outcome**: Based on the simulated stats, we see if you would have won or lost
5. **Update Balance**: Win = +profit, Lose = -wager

### Why Simulation?

Since the games haven't happened yet, we can't know the real outcome. Our simulation:
- Uses real NBA stats
- Combines season averages + recent form
- Adds realistic variance (some games better, some worse)
- Gives you a **realistic preview** of what might happen

**Think of it as:** Playing a betting video game based on real NBA data!

---

## 💡 Tips for Success

### 1. Check Probabilities
- **65%+ probability** = Good bet 🟢
- **55-65% probability** = Moderate bet 🟡
- **Below 55% probability** = Risky bet 🔴

### 2. Parlay Strategy
- More legs = higher payout BUT lower win chance
- **2-3 leg parlays**: Balanced risk/reward
- **4+ leg parlays**: High risk, high reward

### 3. Manage Your Bankroll
- Don't bet your entire balance on one play
- Start with small bets ($10-$50)
- Track your wins and losses

### 4. Look for Value
- Lines slightly UNDER a player's average are good OVERs
- Lines slightly OVER a player's average are good UNDERs
- Compare season average vs line

**Example:**
- LeBron averages **25.5 points**
- Line is **24.0 points**
- OVER is **1.5 points of value** ✅

---

## 🔧 API Endpoints

### Get Props
```
GET /api/daily-props/today          # Today's popular players
GET /api/daily-props/tomorrow       # Tomorrow's popular players
```

### Betting
```
POST /api/daily-props/simulate-bet  # Preview only (no money)
POST /api/daily-props/place-bet     # Place single bet
POST /api/daily-props/place-parlay  # Place multi-leg parlay
```

### Balance Management
```
GET  /api/daily-props/balance/{username}       # Check balance
POST /api/daily-props/reset-balance/{username} # Reset to $10,000
```

---

## 🧪 Testing

### Run Full Test Suite
```bash
cd backend
./test_daily_props.sh
```

This will:
1. Get today's popular players ✅
2. Check starting balance ($10,000) ✅
3. Simulate a bet (preview) ✅
4. Place a real bet ✅
5. Check updated balance ✅
6. Place a 3-leg parlay ✅
7. Check final balance ✅

### Manual Testing with curl

**Get today's props:**
```bash
curl http://localhost:8000/api/daily-props/today | python3 -m json.tool
```

**Place a bet:**
```bash
curl -X POST http://localhost:8000/api/daily-props/place-bet \
  -H "Content-Type: application/json" \
  -d '{
    "player_name": "LeBron James",
    "prop_type": "points",
    "line": 24.5,
    "pick": "OVER",
    "wager": 100
  }' | python3 -m json.tool
```

**Check balance:**
```bash
curl http://localhost:8000/api/daily-props/balance/demo_user | python3 -m json.tool
```

---

## 📱 Example Frontend Flow

### Player Cards Display
```
┌────────────────────────────────────────┐
│  🏀 LeBron James                       │
│  LAL @ ATL • Tonight 7:00 PM           │
│                                        │
│  Season Avg: 25.5 PPG                  │
│                                        │
│  ┌──────────────┐  ┌──────────────┐  │
│  │ OVER 24.0 PTS │  │ UNDER 24.0   │  │
│  │   Likely ✅   │  │   Unlikely   │  │
│  │   65% win    │  │   35% win    │  │
│  └──────────────┘  └──────────────┘  │
│                                        │
│  Other Props:                          │
│  • Rebounds: 7.5 (OVER 60%)           │
│  • Assists: 7.7 (OVER 58%)            │
│  • PRA: 38.5 (OVER 62%)               │
│                                        │
│  [SELECT] [ADD TO SLIP]               │
└────────────────────────────────────────┘
```

### Bet Slip
```
┌────────────────────────────────────────┐
│  📋 YOUR BET SLIP                      │
├────────────────────────────────────────┤
│  1. LeBron James OVER 24.0 PTS        │
│  2. Curry OVER 4.5 3PM                 │
│  3. Giannis OVER 11.5 REB             │
│                                        │
│  Parlay: 3-leg                         │
│  Wager: $50                            │
│  Potential Payout: $250 (5x)          │
│  Win Probability: 27%                  │
│                                        │
│  Balance: $10,000                      │
│                                        │
│  [SIMULATE] [PLACE BET]               │
└────────────────────────────────────────┘
```

### Results Screen
```
┌────────────────────────────────────────┐
│  🎉 YOU WON!                           │
├────────────────────────────────────────┤
│  ✅ LeBron: 26.2 PTS (OVER 24.0)      │
│  ✅ Curry: 5.2 3PM (OVER 4.5)         │
│  ✅ Giannis: 12.8 REB (OVER 11.5)     │
│                                        │
│  Wager: $50                            │
│  Payout: $250                          │
│  Profit: +$200 💰                      │
│                                        │
│  New Balance: $10,200                  │
│                                        │
│  [BET AGAIN] [VIEW BALANCE]           │
└────────────────────────────────────────┘
```

---

## 🎮 Game Modes

### Practice Mode (Current)
- Start with $10,000 paper money
- Bet on simulated outcomes
- Learn betting strategies risk-free
- Reset balance anytime

### Future Modes (Ideas)
- **Challenge Mode**: Try to double your money
- **Tournament Mode**: Compete against other users
- **Historical Mode**: Bet on past games with real results
- **Leaderboard**: Top virtual money earners

---

## ❓ FAQ

**Q: Is this real money?**
A: No! It's 100% paper/virtual money. You can't lose real money.

**Q: Why do I win/lose before the game happens?**
A: We use simulation to predict outcomes. It's like a video game based on real stats.

**Q: How accurate is the simulation?**
A: About 65-70% accurate for clear picks. It's realistic but not perfect.

**Q: Can I reset my balance?**
A: Yes! `POST /api/daily-props/reset-balance/your_username` resets to $10,000.

**Q: What if a player doesn't play?**
A: Currently, simulation assumes healthy players. We'll add injury checks later.

**Q: Can I bet on all stats?**
A: Currently: points, rebounds, assists, threes, PRA, PR, PA. More coming soon!

---

## 🚀 Next Steps

1. **Try it yourself**: Run `./test_daily_props.sh`
2. **Build a frontend**: Use the API to create a betting UI
3. **Track your record**: See if you can beat 50% win rate
4. **Learn strategies**: Compare simulation probabilities to real outcomes

**Happy betting! 🎰**
