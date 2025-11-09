# All Available Prop Types - User Guide

## 📊 Complete List of Supported Props

### ✅ Single Stat Props
1. **Points** (`points`)
   - Player's total points scored
   - Example line: 28.9 (OVER/UNDER)

2. **Rebounds** (`rebounds`)
   - Total rebounds (offensive + defensive)
   - Example line: 10.9 (OVER/UNDER)

3. **Assists** (`assists`)
   - Player's total assists
   - Example line: 6.0 (OVER/UNDER)

4. **Steals** (`steals`)
   - Player's total steals
   - Example line: 0.7 (OVER/UNDER)

5. **Turnovers** (`turnovers`)
   - Player's total turnovers
   - **Note**: UNDER is usually the good bet
   - Example line: 2.5 (OVER/UNDER)

6. **3-PT Made** (`threes_made` or `threes`)
   - Three-pointers made
   - Example line: 2.5 (OVER/UNDER)

### ✅ Combo Stats (PrizePicks Style)
7. **PRA** (`pra`)
   - Points + Rebounds + Assists
   - Example line: 46.3 (OVER/UNDER)

8. **PR** (`pr`)
   - Points + Rebounds
   - Example line: 40.3 (OVER/UNDER)

9. **PA** (`pa`)
   - Points + Assists
   - Example line: 34.9 (OVER/UNDER)

---

## 🎯 Example API Response

### GET /api/daily-props/today

```json
{
  "date": "2025-11-09",
  "count": 10,
  "players": [
    {
      "player_id": 203507,
      "player_name": "Giannis Antetokounmpo",
      "team": "MIL",
      "opponent": "HOU",
      "season_averages": {
        "points": 30.4,
        "rebounds": 11.9,
        "assists": 6.5,
        "steals": 0.9,
        "turnovers": 2.8,
        "threes_made": 0.5,
        "blocks": 1.2
      },
      "prizepicks_lines": {
        "points": 28.9,
        "rebounds": 10.9,
        "assists": 6.0,
        "steals": 0.7,
        "turnovers": 2.5,
        "threes_made": 0.3,
        "pra": 46.3,
        "pr": 40.3,
        "pa": 34.9
      }
    }
  ]
}
```

---

## 🎲 How to Build Your Own Parlay

### Step 1: Get Available Players
```bash
curl http://localhost:8000/api/daily-props/today
```

### Step 2: Choose Your Legs
Pick any combination of:
- Players (up to 6 different players OR same player multiple times)
- Prop types (points, rebounds, assists, steals, turnovers, threes_made, pra, pr, pa)
- Lines (use the suggested lines or create your own)
- Picks (OVER or UNDER)

### Step 3: Place Your Parlay
```bash
curl -X POST http://localhost:8000/api/daily-props/place-parlay \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "bets": [
      {
        "player_name": "Giannis Antetokounmpo",
        "prop_type": "points",
        "line": 28.9,
        "pick": "OVER",
        "wager": 10
      },
      {
        "player_name": "Giannis Antetokounmpo",
        "prop_type": "rebounds",
        "line": 10.9,
        "pick": "OVER",
        "wager": 10
      },
      {
        "player_name": "Stephen Curry",
        "prop_type": "threes_made",
        "line": 4.5,
        "pick": "OVER",
        "wager": 10
      },
      {
        "player_name": "Ja Morant",
        "prop_type": "assists",
        "line": 7.5,
        "pick": "OVER",
        "wager": 10
      },
      {
        "player_name": "Paolo Banchero",
        "prop_type": "pra",
        "line": 38.5,
        "pick": "OVER",
        "wager": 10
      },
      {
        "player_name": "Jalen Brunson",
        "prop_type": "steals",
        "line": 0.5,
        "pick": "OVER",
        "wager": 10
      }
    ],
    "total_wager": 60,
    "bet_mode": "standard"
  }'
```

---

## 💡 Popular Parlay Strategies

### Strategy 1: All Points (Scorers Parlay)
- 6 players, all on OVER points
- Higher risk (all must hit)
- Good for nights with weak defenses

### Strategy 2: Mixed Stats (Balanced Parlay)
- 2 points, 2 rebounds, 2 assists
- Diversified across stat types
- More balanced approach

### Strategy 3: Same Player Multi-Leg
- Same player, multiple props (points + rebounds + assists)
- If player has big game, you win multiple legs
- "Stack" strategy

### Strategy 4: Combo Stats Only
- Use PRA, PR, PA props
- Safer lines (combined stats more consistent)
- Lower payouts but higher win probability

### Strategy 5: Defensive Stats
- Focus on steals, blocks
- Lower lines = easier to hit
- Great for defensive-minded players

### Strategy 6: Shooter's Special
- All threes_made props
- Pick the best shooters (Curry, Dame, Trae)
- High variance but fun

---

## 📈 Prop Type Difficulty Rankings

### Easiest to Hit (Most Consistent)
1. **PRA** - Combined stats, most consistent
2. **Points** - Star players score reliably
3. **PR / PA** - Combo stats
4. **Rebounds** - Bigs are consistent
5. **Assists** - Guards are fairly consistent

### Moderate Difficulty
6. **Threes Made** - Depends on shot attempts
7. **Steals** - Moderate variance
8. **Turnovers** - Varies by game pace

### Hardest to Hit (Most Variance)
9. **Blocks** - Very game-dependent
10. **Specific low-usage players** - Bench players

---

## 🎯 Line Generation Logic

All lines are generated **slightly below** season averages to match PrizePicks style:

| Stat | Season Avg | Line Formula |
|------|------------|--------------|
| Points (25+) | 30.4 | avg - 1.5 = 28.9 |
| Points (20-25) | 22.0 | avg - 1.0 = 21.0 |
| Points (10-20) | 15.0 | avg - 0.5 = 14.5 |
| Rebounds (10+) | 11.9 | avg - 1.0 = 10.9 |
| Rebounds (6-10) | 8.0 | avg - 0.5 = 7.5 |
| Assists (8+) | 9.0 | avg - 0.5 = 8.5 |
| Assists (5-8) | 6.5 | avg - 0.5 = 6.0 |
| Steals (2+) | 2.2 | avg - 0.5 = 1.7 |
| Steals (1-2) | 1.5 | avg - 0.3 = 1.2 |
| Threes (3+) | 3.5 | avg - 0.5 = 3.0 |
| Threes (2-3) | 2.5 | avg - 0.3 = 2.2 |
| PRA (40+) | 46.8 | avg - 2.5 = 44.3 |
| PRA (30-40) | 35.0 | avg - 2.0 = 33.0 |

---

## 🚀 Testing Your Parlay

### Quick Test Script
```bash
# 1. See today's players
curl http://localhost:8000/api/daily-props/today | jq '.players[] | {player_name, prizepicks_lines}'

# 2. Place a 6-leg parlay
curl -X POST http://localhost:8000/api/daily-props/place-parlay \
  -H "Content-Type: application/json" \
  -d @your_parlay.json

# 3. Check your balance
curl http://localhost:8000/api/daily-props/balance/your_username
```

---

## ⚠️ Important Notes

1. **Turnovers**: Betting UNDER is usually the "good" bet (fewer turnovers is better)
2. **Same Player Multi-Leg**: Allowed! You can bet on same player multiple times
3. **Combo Stats**: PRA, PR, PA are often safer than individual stats
4. **Flex Pick**: Available on 3-6 leg parlays (insurance against 1 loss)
5. **Power Play**: Available on all parlays (boost payout, reduce win chance)
6. **Realistic Lines**: All lines are slightly below averages (PrizePicks style)

---

## 📝 Complete Prop Type Reference

```
Single Stats:
- points
- rebounds
- assists
- steals
- turnovers
- threes_made (or "threes")

Combo Stats:
- pra (points + rebounds + assists)
- pr (points + rebounds)
- pa (points + assists)
```

All prop types work with:
- Standard bets
- Flex Pick parlays
- Power Play parlays
- Realistic odds calculation
- Simulation-based outcomes

---

**You now have complete freedom to build any parlay combination you want!** 🎉
