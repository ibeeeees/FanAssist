# Quick Reference - Test Any NBA Player

## 🚀 Three Ways to Test

### 1️⃣ Menu (Pick from 10 stars)
```bash
python test_menu.py
```

### 2️⃣ Interactive (Any player)
```bash
python test_any_player.py "Player Name"
```

### 3️⃣ Command Line (Fast)
```bash
./quick_test.sh "Player Name" TEAM PTS REB AST
```

## ⚡ Examples

```bash
# Test Giannis
./quick_test.sh "Giannis Antetokounmpo" MIL 30.5 11.5 5.5

# Test LeBron
./quick_test.sh "LeBron James" LAL 25.5 7.5 7.5

# Test Curry
./quick_test.sh "Stephen Curry" GSW 28.5 5.5 6.5

# Test any player interactively
python test_any_player.py "Damian Lillard"

# Use the menu
python test_menu.py
```

## 📊 What You Get

✅ Quick odds with win probabilities
✅ 10 game simulations with averages
✅ 100-simulation bet analysis
✅ Multi-leg parlay recommendations

## 🏀 Popular Players in Menu

1. Giannis Antetokounmpo
2. LeBron James
3. Stephen Curry
4. Kevin Durant
5. Nikola Jokic
6. Luka Doncic
7. Joel Embiid
8. Jayson Tatum
9. Damian Lillard
10. Anthony Davis

**Or enter any active NBA player!**

## 💡 Tips

- Server must be running: `python run.py`
- Use full names: "LeBron James" not "LeBron"
- First names often work: "Giannis" finds full name
- Check spelling if player not found

## 🎯 That's it!

Pick your method and start testing! 🏀
