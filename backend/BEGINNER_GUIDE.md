# 🏀 FanAssist Beginner's Guide to NBA Prop Betting

Welcome to FanAssist! This guide will help you understand NBA prop betting and use our AI-powered analysis system. Don't worry - we'll explain everything in simple terms with real examples.

## 🎯 What Are Prop Bets?

**Prop bets** (proposition bets) let you bet on individual player statistics instead of who wins the game. For example:
- "Will LeBron James score OVER 25.5 points?"
- "Will Stephen Curry make UNDER 3.5 three-pointers?"

### Key Terms:
- **Line**: The target number (e.g., 25.5 points)
- **Over**: Player will exceed the line 
- **Under**: Player will stay below the line
- **Leg**: One bet in a multi-bet ticket

## 📊 Understanding Basketball Stats

### Basic Stats Explained:

#### 🏀 **Points**
- **What it is**: Total points from field goals, 3-pointers, and free throws
- **Good numbers**: 15+ (solid), 20+ (very good), 25+ (elite)
- **What affects it**: Shot attempts, shooting %, playing time, role in offense

#### 📦 **Rebounds**  
- **What it is**: Grabbing the ball after missed shots
- **Good numbers**: 6+ (guards), 8+ (forwards), 10+ (centers)
- **What affects it**: Height, opponent pace, team rebounding, playing time

#### 🎯 **Assists**
- **What it is**: Passes that directly lead to teammate scores
- **Good numbers**: 3+ (non-guards), 5+ (guards), 8+ (elite playmakers)
- **What affects it**: Ball-handling role, teammate shooting, game pace

#### 🛡️ **Steals**
- **What it is**: Taking the ball away from opponents
- **Good numbers**: 1+ (solid), 1.5+ (very good), 2+ (elite)
- **What affects it**: Defensive pressure, opponent turnovers, playing style

#### 🚫 **Blocks**
- **What it is**: Preventing opponent shots by deflecting them
- **Good numbers**: 0.5+ (guards), 1+ (forwards), 1.5+ (centers)
- **What affects it**: Height, defensive positioning, opponent shot attempts

## 🚀 Getting Started with FanAssist

### Step 1: Analyze a Player
```bash
GET /api/beginner/players/LeBron James/beginner-analysis
```

**What you get:**
- ✅ Last 5 games breakdown with pros/cons
- ✅ Basketball explanations for each stat
- ✅ Trend analysis (improving/declining/stable)
- ✅ Beginner tips for that player
- ✅ Position and role explanations

### Step 2: Analyze a Single Prop
```bash
POST /api/beginner/analyze-prop/beginner
{
  "player_name": "LeBron James",
  "prop_type": "points", 
  "line_value": 25.5,
  "bet_type": "over"
}
```

**What you get:**
- 🤖 AI recommendation with confidence level
- 📊 Recent vs season average comparison
- 🎮 Game simulation showing how bet could hit/miss
- 📚 Basketball education about the stat
- ⚠️ Risk assessment and betting tips

### Step 3: Analyze a Full Ticket
```bash
POST /api/beginner/analyze-ticket/beginner
{
  "legs": [
    {"player_name": "LeBron James", "prop_type": "points", "line_value": 25.5, "bet_type": "over"},
    {"player_name": "Stephen Curry", "prop_type": "threes_made", "line_value": 3.5, "bet_type": "over"},
    {"player_name": "Giannis Antetokounmpo", "prop_type": "rebounds", "line_value": 11.5, "bet_type": "under"}
  ],
  "wager_amount": 10.0
}
```

**What you get:**
- 🎯 Analysis of each individual leg
- 🎲 Simulation of entire ticket outcome
- 📈 Overall probability and recommendation
- 📚 Educational insights about multi-leg betting
- ⚠️ Risk warnings and beginner tips

## 💡 Reading the Analysis

### Confidence Levels:
- **90-100%**: Very High Confidence 🟢 (Almost certain)
- **80-89%**: High Confidence 🟢 (Strong evidence)  
- **70-79%**: Medium Confidence 🟡 (Good chance)
- **60-69%**: Low Confidence 🟡 (Uncertain)
- **Below 60%**: Very Low 🔴 (Avoid for beginners)

### Trend Analysis:
- **📈 Improving**: Player getting better in recent games
- **📉 Declining**: Player struggling lately
- **⚖️ Stable**: Consistent performance

### Form vs Season:
- **🔥 Hot Streak**: Recent games much better than season average
- **❄️ Cold Stretch**: Recent games worse than season average  
- **➡️ Normal Form**: Playing close to season averages

## 🎮 Practice with Paper Betting

Start with virtual money to learn without risk!

### Create Account:
```bash
POST /api/betting/users
{
  "username": "nba_beginner",
  "email": "beginner@example.com"
}
```
*You get $10,000 virtual money to start!*

### Place Your First Bet:
```bash
POST /api/betting/users/{user_id}/bets
{
  "player_name": "LeBron James",
  "prop_type": "points",
  "line_value": 25.5, 
  "bet_type": "over",
  "wager_amount": 10.0
}
```

### Track Your Progress:
```bash
GET /api/betting/users/{user_id}/portfolio  # See all your bets
GET /api/betting/users/{user_id}/stats      # Your win rate and profit
GET /api/betting/leaderboard               # Compare with others
```

## 📚 Learn Basketball Concepts

### Get Explanations:
```bash
GET /api/beginner/education/basketball-terms    # All basketball terms
POST /api/beginner/education/explain/rebounds   # AI explains any concept
```

## 🎯 Example Walkthrough

Let's analyze **LeBron James Points Over 25.5**:

### 1. Get Player Analysis
```json
{
  "last_5_averages": {
    "points": 28.2,
    "minutes": 36.5
  },
  "season_averages": {
    "points": 26.1
  },
  "stat_analysis": {
    "points": {
      "trend": "improving",
      "consistency": "very_consistent", 
      "pros": [
        "📈 Trending UP in points - recent games better than earlier ones",
        "🔥 Hot streak! Recent points (28.2) well above season average (26.1)",
        "⚡ Very reliable in points - consistent performance across recent games"
      ],
      "cons": [],
      "form_vs_season": "much_better"
    }
  }
}
```

### 2. AI Analysis
```json
{
  "recommendation": "over",
  "confidence": 0.87,
  "reasoning": "LeBron is in excellent form, averaging 28.2 points over his last 5 games compared to his 26.1 season average. He's been very consistent and trending upward...",
  "beginner_details": {
    "beginner_explanation": "LeBron has been scoring really well lately. He's averaged 28.2 points in his last 5 games, which is higher than the 25.5 line we need to beat.",
    "confidence_explanation": "I'm quite confident (87%) because LeBron has been very consistent and is clearly in good scoring form right now.",
    "risk_level": "low",
    "betting_tip": "This is a good beginner bet - LeBron is reliable and in great form"
  }
}
```

### 3. Game Simulation
```json
{
  "simulation": {
    "game_scenario": "Close game against a good team where LeBron stays aggressive throughout",
    "final_stats": {
      "points": 27
    },
    "leg_results": [{
      "bet_result": "won",
      "explanation": "LeBron scored 27 points, beating the 25.5 line by 1.5 points",
      "lesson_learned": "When elite players are in good form, they often maintain their level against any opponent"
    }]
  }
}
```

**Result**: ✅ **BET HITS!** LeBron scored 27 points, beating our 25.5 line.

## ⚠️ Beginner Tips

### DO:
✅ **Start Small**: Begin with $5-10 bets  
✅ **Use Analysis**: Always check our AI recommendations  
✅ **Learn Gradually**: Focus on 1-2 stat types at first  
✅ **Track Performance**: Monitor your win rate and learn  
✅ **Compare Form**: Recent games vs season averages  

### DON'T:  
❌ **Chase Losses**: Don't increase bet size after losing  
❌ **Bet Injured Players**: Always check injury reports  
❌ **Ignore Consistency**: Avoid unpredictable players  
❌ **Overbet**: Never risk more than you can afford  
❌ **Rush**: Take time to understand the analysis  

## 🏆 Success Strategies

### 1. **The Conservative Approach**
- Bet only high confidence picks (85%+)  
- Small bet sizes ($5-20)
- Focus on consistent players
- 2-3 leg tickets maximum

### 2. **The Learning Approach**  
- Try different prop types to learn
- Use simulation feature extensively
- Read all pros/cons carefully
- Track which strategies work for you

### 3. **The Gradual Growth**
- Start with single props
- Move to 2-leg tickets
- Slowly increase bet sizes as you improve
- Always use bankroll management

## 📱 Quick Reference

### Key Endpoints:
- **Player Analysis**: `/api/beginner/players/{name}/beginner-analysis`
- **Single Prop**: `/api/beginner/analyze-prop/beginner`  
- **Full Ticket**: `/api/beginner/analyze-ticket/beginner`
- **Learn Terms**: `/api/beginner/education/basketball-terms`
- **Paper Betting**: `/api/betting/*`

### Response Features:
- 🎯 AI recommendations with confidence
- 📊 Last 5 games vs season stats
- 🏀 Basketball term explanations
- 🎮 Game outcome simulations
- 📚 Educational content
- ⚠️ Risk assessments
- 💡 Specific beginner tips

## 🎉 Ready to Start!

1. **Explore a player** you know well
2. **Read the full analysis** - don't skip the explanations!
3. **Start with high-confidence, single props**
4. **Use paper betting** to practice risk-free
5. **Learn from simulations** to understand game flow
6. **Gradually build complexity** as you improve

Remember: The goal is to **learn and have fun** while developing your understanding of basketball and betting. Take your time, use the analysis tools, and don't rush into big bets!

🏀 **Good luck, and welcome to the world of NBA prop betting!** 🏀