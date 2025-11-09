# NBA Player Simulation Testing Guide

Test any NBA player's performance predictions and betting props!

## 🚀 Quick Start

### Method 1: Interactive Menu (Easiest)
```bash
python test_menu.py
```
Select from 10 popular NBA players or enter a custom player name.

### Method 2: Interactive Custom Player
```bash
python test_any_player.py
```
Or with a player name:
```bash
python test_any_player.py "Damian Lillard"
```

### Method 3: Quick Shell Script
```bash
./quick_test.sh "Player Name" [opponent] [pts_line] [reb_line] [ast_line]
```

## 📋 Examples

### Test Giannis Antetokounmpo
```bash
python test_any_player.py "Giannis Antetokounmpo"
# Or use the menu
python test_menu.py
# Select option 1
```

### Test Stephen Curry with custom lines
```bash
./quick_test.sh "Stephen Curry" GSW 28.5 5.5 6.5
```

### Test LeBron James
```bash
./quick_test.sh "LeBron James" LAL 25.5 7.5 7.5
```

### Test Luka Doncic
```bash
python test_any_player.py "Luka Doncic"
```

### Test Nikola Jokic
```bash
./quick_test.sh "Nikola Jokic" DEN 26.5 12.5 9.5
```

## 🎯 What Gets Tested

Each test runs:
1. **Quick Odds** - Instant probability calculations for 3 props
2. **Single Game Simulation** - 10 simulated games with full stats
3. **Bet Outcome Analysis** - 100 simulations per prop with win probability
4. **Multi-Leg Parlay** - 3-leg ticket analysis with combined odds

## 📊 Available Test Files

- `test_menu.py` - Interactive menu with 10 popular players
- `test_any_player.py` - Full interactive custom player test
- `quick_test.sh` - Fast command-line testing
- `test_giannis_simple.sh` - Pre-configured Giannis test
- `test_giannis_rockets.py` - Full Python test for Giannis

## 🏀 Popular Players (Pre-configured in Menu)

1. Giannis Antetokounmpo (MIL) - 30.5 PTS, 11.5 REB, 5.5 AST
2. LeBron James (LAL) - 25.5 PTS, 7.5 REB, 7.5 AST
3. Stephen Curry (GSW) - 28.5 PTS, 5.5 REB, 6.5 AST
4. Kevin Durant (PHX) - 27.5 PTS, 7.5 REB, 5.5 AST
5. Nikola Jokic (DEN) - 26.5 PTS, 12.5 REB, 9.5 AST
6. Luka Doncic (DAL) - 32.5 PTS, 8.5 REB, 8.5 AST
7. Joel Embiid (PHI) - 29.5 PTS, 10.5 REB, 4.5 AST
8. Jayson Tatum (BOS) - 27.5 PTS, 8.5 REB, 4.5 AST
9. Damian Lillard (MIL) - 25.5 PTS, 4.5 REB, 7.5 AST
10. Anthony Davis (LAL) - 25.5 PTS, 11.5 REB, 3.5 AST

## 💡 Tips

- **Make sure the server is running**: `python run.py` in another terminal
- **Use exact player names**: "LeBron James" not "Lebron" or "LBJ"
- **Common abbreviations work**: "Giannis" will find "Giannis Antetokounmpo"
- **Team abbreviations**: LAL, BOS, GSW, MIL, PHX, DEN, etc.

## 🔧 Troubleshooting

### Player not found?
- Try using full name: "LeBron James" instead of "LeBron"
- Check spelling
- Try just first name: "Giannis" works

### Server not responding?
```bash
# Check if server is running
curl http://localhost:8000/health

# Restart server if needed
pkill -f "python.*run.py"
python run.py &
```

### Timeout errors?
The NBA API sometimes has delays. Wait a few seconds and try again.

## 🎮 Advanced Usage

### Test multiple players in sequence
```bash
for player in "LeBron James" "Stephen Curry" "Giannis"; do
    ./quick_test.sh "$player"
    echo ""
done
```

### Custom props for specific matchup
```bash
# Test Curry with high assists line
./quick_test.sh "Stephen Curry" GSW 30.5 5.5 8.5

# Test Jokic triple-double watch
./quick_test.sh "Nikola Jokic" DEN 25.5 11.5 9.5
```

## 📈 Understanding Results

### Confidence Levels
- **90%+**: Strong bet ✅
- **60-89%**: Good bet ⭐
- **50-59%**: Slight edge ⚠️
- **Below 50%**: Avoid ❌

### Expected Value (EV)
- Positive EV: Projected result above the line
- Negative EV: Projected result below the line
- Higher EV = stronger conviction

### Recommendations
- ✅ TAKE IT: High confidence (70%+)
- ⚠️ CLOSE CALL: Toss-up (45-55%)
- ❌ AVOID: Low confidence (below 40%)

## 🚀 Quick Commands Summary

```bash
# Interactive menu (easiest)
python test_menu.py

# Test any player interactively
python test_any_player.py

# Quick test with defaults
./quick_test.sh "Player Name"

# Full custom test
./quick_test.sh "Player Name" OPPONENT PTS_LINE REB_LINE AST_LINE

# Pre-made test
./test_giannis_simple.sh
```

Happy testing! 🏀🎯
