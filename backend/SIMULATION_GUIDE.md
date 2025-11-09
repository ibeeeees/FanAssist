# 🎮 Game Simulation & Betting Features

## Overview

The FanAssist API now includes powerful game simulation features that allow users to:
- **Simulate NBA games** with realistic player performances
- **Test bet outcomes** before placing real money
- **Calculate win probabilities** for single and multi-leg tickets
- **Make data-driven betting decisions**

## 🎲 Simulation Endpoints

### 1. Single Game Simulation
**Endpoint:** `POST /api/simulation/single-game`

Simulate how a player might perform in their next game.

**Request:**
```json
{
  "player_name": "LeBron James",
  "opponent": "LAL",
  "is_home": true,
  "num_simulations": 100
}
```

**Response:**
```json
{
  "player_name": "LeBron James",
  "simulations": [
    {
      "points": 27,
      "rebounds": 8,
      "assists": 7,
      "steals": 1,
      "blocks": 1,
      "turnovers": 3,
      "three_pointers_made": 2,
      "fantasy_score": 45.6
    }
    // ... 99 more simulations
  ],
  "averages": {
    "points": 26.3,
    "rebounds": 7.8,
    "assists": 7.2,
    "steals": 1.1,
    "blocks": 0.8,
    "three_pointers_made": 1.9
  }
}
```

**Use Case:** See the range of possible outcomes for a player's next game.

---

### 2. Bet Outcome Simulation
**Endpoint:** `POST /api/simulation/bet-outcome`

Calculate your chances of winning a specific bet.

**Request:**
```json
{
  "player_name": "Stephen Curry",
  "prop_type": "points",
  "line": 27.5,
  "bet_type": "over",
  "num_simulations": 100
}
```

**Response:**
```json
{
  "player_name": "Stephen Curry",
  "prop_type": "points",
  "line": 27.5,
  "bet_type": "over",
  "win_probability": 0.58,
  "expected_value": 28.3,
  "median_result": 28.0,
  "standard_deviation": 6.2,
  "percentage_over": 58.0,
  "percentage_under": 42.0,
  "confidence_level": "Medium",
  "simulations_run": 100,
  "recommendation": "✔️ LEAN OVER - Slight edge (58% win rate)",
  "visualization_data": {
    "distribution": {
      "over_percentage": 58.0,
      "under_percentage": 42.0,
      "line": 27.5
    }
  }
}
```

**Use Case:** Determine if a bet is worth placing based on simulated probabilities.

---

### 3. Multi-Leg Ticket Simulation
**Endpoint:** `POST /api/simulation/multi-leg-ticket`

Simulate an entire parlay ticket with multiple player props.

**Request:**
```json
{
  "legs": [
    {
      "player_name": "LeBron James",
      "prop_type": "points",
      "line": 25.5,
      "bet_type": "over"
    },
    {
      "player_name": "Giannis Antetokounmpo",
      "prop_type": "rebounds",
      "line": 11.5,
      "bet_type": "over"
    },
    {
      "player_name": "Luka Doncic",
      "prop_type": "assists",
      "line": 8.5,
      "bet_type": "over"
    }
  ],
  "num_simulations": 100
}
```

**Response:**
```json
{
  "ticket_win_probability": 0.23,
  "ticket_hit_rate": "23.0%",
  "expected_wins_per_100": 23,
  "leg_probabilities": [
    {
      "leg_number": 1,
      "player": "LeBron James",
      "prop": "Points",
      "line": 25.5,
      "bet_type": "over",
      "win_probability": 0.62,
      "hit_rate": "62.0%"
    },
    {
      "leg_number": 2,
      "player": "Giannis Antetokounmpo",
      "prop": "Rebounds",
      "line": 11.5,
      "bet_type": "over",
      "win_probability": 0.58,
      "hit_rate": "58.0%"
    },
    {
      "leg_number": 3,
      "player": "Luka Doncic",
      "prop": "Assists",
      "line": 8.5,
      "bet_type": "over",
      "win_probability": 0.65,
      "hit_rate": "65.0%"
    }
  ],
  "total_legs": 3,
  "simulations_run": 100,
  "recommendation": "Good - Solid play",
  "visual_breakdown": {
    "difficulty_rating": "🟢 MODERATE - Reasonable shot"
  }
}
```

**Use Case:** Understand how difficult it is to hit an entire parlay and identify weak legs.

---

### 4. Quick Odds Check
**Endpoint:** `GET /api/simulation/quick-odds/{player_name}`

Fast odds check for instant decision-making.

**Request:**
```
GET /api/simulation/quick-odds/LeBron%20James?prop_type=points&line=25.5
```

**Response:**
```json
{
  "player": "LeBron James",
  "prop": "Points",
  "line": 25.5,
  "best_bet": "OVER",
  "confidence": "58%",
  "over_probability": "58%",
  "under_probability": "42%",
  "expected_result": 26.8,
  "season_average": 25.4,
  "recommendation": "✅ TAKE IT"
}
```

**Use Case:** Quick check before placing a bet.

---

## 💰 Integrated Betting Preview

### Preview Bet With Simulation
**Endpoint:** `POST /api/betting/users/{user_id}/bets/preview-with-simulation`

Preview a bet with full simulation before placing it.

**Request:**
```json
{
  "player_name": "Kevin Durant",
  "prop_type": "points",
  "line_value": 28.5,
  "bet_type": "over",
  "wager_amount": 100.0
}
```

**Response:**
```json
{
  "can_place": true,
  "should_place": true,
  "bet_details": {
    "player": "Kevin Durant",
    "prop": "Points",
    "line": 28.5,
    "bet_type": "OVER",
    "wager": 100.0,
    "potential_payout": 190.0,
    "potential_profit": 90.0
  },
  "simulation_results": {
    "win_probability": "62%",
    "expected_value": 11.80,
    "expected_result": 29.3,
    "confidence_level": "High",
    "percentage_over": 62.0,
    "percentage_under": 38.0
  },
  "recommendation": "✅ STRONG PLAY - High confidence bet",
  "balance_after_win": 10090.0,
  "balance_after_loss": 9900.0,
  "current_balance": 10000.0
}
```

**Use Case:** Get full analysis before committing your money.

---

## 🎯 How the Simulation Works

### Statistical Model

The simulation uses a sophisticated model based on:

1. **Season Averages** (40% weight)
   - Player's full season statistics
   
2. **Recent Form** (60% weight)
   - Last 5-10 games performance
   - Trend analysis (hot/cold streaks)

3. **Variance Factors**
   - Points: 25% standard deviation
   - Rebounds: 30% standard deviation
   - Assists: 35% standard deviation
   - Steals/Blocks: 50% standard deviation

4. **Modifiers**
   - Hot streak: +15% boost
   - Warm: +8% boost
   - Normal: No change
   - Cold: -8% decrease
   - Ice cold: -15% decrease
   - Home court: +5% boost
   - Away: -2% decrease

5. **Distribution**
   - Uses Gamma distribution for realistic positive skew
   - No negative values (basketball stats can't be negative)

### Simulation Process

For each simulation:
1. Assess player's recent form (hot/cold streak)
2. Calculate expected value with modifiers
3. Apply statistical variance
4. Generate realistic stat line
5. Check if bet would win or lose

After N simulations:
- Calculate win percentage
- Determine confidence level
- Generate recommendation
- Show expected value

---

## 📊 Understanding Results

### Win Probability Levels

| Probability | Confidence | Action |
|-------------|-----------|--------|
| 65%+ | High | Strong bet |
| 55-65% | Medium | Good bet |
| 48-55% | Low | Risky |
| <48% | Very Low | Avoid |

### Expected Value (EV)

- **Positive EV** = Good bet (you'll profit long-term)
- **Negative EV** = Bad bet (you'll lose long-term)
- **Zero EV** = Break even

Formula: `EV = (Win% × Profit) - (Loss% × Stake)`

### Multi-Leg Difficulty

| Legs | 20% Each Leg | Ticket Win% |
|------|--------------|-------------|
| 2 legs | 60% | 36% |
| 3 legs | 60% | 22% |
| 4 legs | 60% | 13% |
| 5 legs | 60% | 8% |
| 6 legs | 60% | 5% |

**Key Insight:** Adding more legs dramatically reduces your chance of winning!

---

## 🔥 Example Workflows

### Workflow 1: Single Bet Decision
1. Check quick odds: `/api/simulation/quick-odds/LeBron%20James?prop_type=points&line=25.5`
2. If promising, get full simulation: `POST /api/simulation/bet-outcome`
3. Preview with balance: `POST /api/betting/users/{user_id}/bets/preview-with-simulation`
4. Place bet: `POST /api/betting/users/{user_id}/bets`

### Workflow 2: Building a Parlay
1. Simulate each individual leg first
2. Check individual win probabilities (aim for 60%+ each)
3. Simulate the full ticket: `POST /api/simulation/multi-leg-ticket`
4. If ticket probability > 20% (for 3+ legs), consider placing

### Workflow 3: Player Research
1. Simulate 100 games: `POST /api/simulation/single-game`
2. Review averages and range
3. Compare to current prop lines
4. Find value opportunities

---

## ⚠️ Important Notes

### Simulation Limits
- Single game: 1-1000 simulations
- Bet outcome: 10-1000 simulations
- Multi-leg: 10-500 simulations
- Quick odds: Fixed at 50 simulations

### Accuracy
- Simulations are based on historical data
- Cannot predict injuries, rest days, or lineup changes
- Should be used as a guide, not a guarantee
- Past performance doesn't guarantee future results

### Best Practices
1. Run at least 100 simulations for accuracy
2. Check player's recent form before trusting results
3. Consider external factors (matchup, rest, motivation)
4. Don't bet more than you can afford to lose
5. Use simulations to find value, not certainty

---

## 🚀 Quick Start Examples

### cURL Examples

```bash
# Quick odds check
curl "http://localhost:8000/api/simulation/quick-odds/LeBron%20James?prop_type=points&line=25.5"

# Single game simulation
curl -X POST "http://localhost:8000/api/simulation/single-game" \
  -H "Content-Type: application/json" \
  -d '{
    "player_name": "Stephen Curry",
    "num_simulations": 100,
    "is_home": true
  }'

# Bet outcome simulation
curl -X POST "http://localhost:8000/api/simulation/bet-outcome" \
  -H "Content-Type: application/json" \
  -d '{
    "player_name": "Giannis Antetokounmpo",
    "prop_type": "rebounds",
    "line": 11.5,
    "bet_type": "over",
    "num_simulations": 100
  }'
```

### Python Examples

```python
import requests

# Quick odds check
response = requests.get(
    "http://localhost:8000/api/simulation/quick-odds/LeBron James",
    params={"prop_type": "points", "line": 25.5}
)
print(response.json())

# Multi-leg simulation
response = requests.post(
    "http://localhost:8000/api/simulation/multi-leg-ticket",
    json={
        "legs": [
            {"player_name": "LeBron James", "prop_type": "points", "line": 25.5, "bet_type": "over"},
            {"player_name": "Giannis Antetokounmpo", "prop_type": "rebounds", "line": 11.5, "bet_type": "over"}
        ],
        "num_simulations": 100
    }
)
print(response.json())
```

---

## 📖 Additional Resources

- Full API documentation: `http://localhost:8000/docs`
- Betting system: See `BETTING_EXAMPLES.md`
- Beginner guide: See `BEGINNER_GUIDE.md`

---

## 🎓 Understanding Basketball Stats

For beginners unfamiliar with basketball statistics:
- **Points (Pts)**: Baskets scored
- **Rebounds (Reb)**: Balls grabbed after missed shots
- **Assists (Ast)**: Passes that lead to baskets
- **Steals (Stl)**: Taking the ball from opponent
- **Blocks (Blk)**: Blocking opponent's shot
- **Turnovers (TO)**: Losing possession
- **3-Pointers Made**: Three-point shots made
- **Fantasy Score**: Weighted combination of all stats

Good luck and bet responsibly! 🍀
