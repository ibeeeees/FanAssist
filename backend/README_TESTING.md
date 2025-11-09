# 🏀 NBA Player Simulation Testing - Complete Setup

## ✅ What You Now Have

You can now test **ANY active NBA player** using multiple methods!

## 📁 Test Files Created

1. **`test_menu.py`** - Interactive menu with 10 popular players
2. **`test_any_player.py`** - Full interactive test for any player
3. **`quick_test.sh`** - Fast command-line testing
4. **`test_giannis_simple.sh`** - Pre-made Giannis test
5. **`test_giannis_rockets.py`** - Full Python Giannis test

## 🚀 How to Use

### Method 1: Interactive Menu (Recommended for beginners)
```bash
cd /Users/ibe/WebstormProjects/ZokuAppWebsite/FanAssist/backend
python test_menu.py
```
- Pick from 10 popular NBA stars
- Or enter custom player
- Guided prompts for all inputs

### Method 2: Direct Player Test
```bash
python test_any_player.py "Stephen Curry"
```
- Interactive prompts for opponent and prop lines
- Full test suite runs automatically

### Method 3: Quick Command Line
```bash
./quick_test.sh "Player Name" OPPONENT PTS_LINE REB_LINE AST_LINE
```
- Fastest method
- All parameters in one command
- Great for scripting

## 🎯 Live Examples

### Example 1: Test Giannis (Interactive)
```bash
python test_any_player.py "Giannis Antetokounmpo"
# Then enter: HOU, y, 30.5, 11.5, 5.5
```

### Example 2: Test LeBron (Fast)
```bash
./quick_test.sh "LeBron James" LAL 25.5 7.5 7.5
```

### Example 3: Test from Menu
```bash
python test_menu.py
# Select: 3 (for Stephen Curry)
```

### Example 4: Test Any Player
```bash
# Try these:
python test_any_player.py "Damian Lillard"
python test_any_player.py "Ja Morant"
python test_any_player.py "Devin Booker"
python test_any_player.py "Kawhi Leonard"
```

## 📊 What Each Test Shows

### 1. Quick Odds (3 props)
- Best bet (OVER/UNDER)
- Win probability percentage
- Expected result
- Season average
- Recommendation

### 2. Single Game Simulation
- 10 simulated games
- Average stats across all games
- Sample game results

### 3. Bet Outcome Analysis
- 100 simulations per prop
- Win probability
- Expected value
- Median result
- Confidence level

### 4. Multi-Leg Parlay
- 3-leg ticket analysis
- Individual leg probabilities
- Combined win probability
- Difficulty rating

## 🏀 Pre-Configured Players

Just select from menu:
1. Giannis Antetokounmpo (30.5/11.5/5.5)
2. LeBron James (25.5/7.5/7.5)
3. Stephen Curry (28.5/5.5/6.5)
4. Kevin Durant (27.5/7.5/5.5)
5. Nikola Jokic (26.5/12.5/9.5)
6. Luka Doncic (32.5/8.5/8.5)
7. Joel Embiid (29.5/10.5/4.5)
8. Jayson Tatum (27.5/8.5/4.5)
9. Damian Lillard (25.5/4.5/7.5)
10. Anthony Davis (25.5/11.5/3.5)

## 🔧 Requirements

### Server Must Be Running
```bash
# In one terminal:
cd /Users/ibe/WebstormProjects/ZokuAppWebsite/FanAssist
python backend/run.py
```

### Then Test in Another Terminal
```bash
# In another terminal:
cd /Users/ibe/WebstormProjects/ZokuAppWebsite/FanAssist/backend
python test_menu.py
```

## 💡 Pro Tips

### Finding Players
- Use full names: "LeBron James" ✅
- First names often work: "Giannis" ✅
- Nicknames may not work: "King James" ❌

### Choosing Prop Lines
- Check PrizePicks/DraftKings for current lines
- Default lines provided in menu
- Can customize any line value

### Understanding Results
- **90%+ confidence**: Strong bet ⭐⭐⭐
- **60-89% confidence**: Good bet ⭐⭐
- **50-59% confidence**: Slight edge ⭐
- **Below 50%**: Avoid ❌

## 🎮 Quick Commands Reference

```bash
# Method 1: Interactive menu
python test_menu.py

# Method 2: Interactive any player
python test_any_player.py
python test_any_player.py "Player Name"

# Method 3: Quick test
./quick_test.sh "Player" TEAM PTS REB AST

# Examples
./quick_test.sh "Giannis" MIL 30.5 11.5 5.5
./quick_test.sh "LeBron James" LAL 25.5 7.5 7.5
./quick_test.sh "Stephen Curry" GSW 28.5 5.5 6.5
```

## 🚨 Troubleshooting

### "Player not found"
- Check spelling
- Use full name
- Try just first name

### "Connection refused"
- Start the server: `python backend/run.py`
- Check it's running: `curl http://localhost:8000/health`

### Timeout errors
- NBA API can be slow
- Wait 30 seconds and retry
- Server may need restart

## 📚 Documentation Files

- **`QUICK_START.md`** - Fast reference guide
- **`TESTING_GUIDE.md`** - Detailed testing guide
- **`README_TESTING.md`** - This comprehensive guide

## 🎉 You're All Set!

Start testing any NBA player right now:

```bash
python test_menu.py
```

Happy testing! 🏀🎯
