#!/bin/bash

# Quick Player Simulation Tester
# Usage: ./quick_test.sh "Player Name" [opponent] [points_line] [rebounds_line] [assists_line]

PLAYER_NAME="${1:-LeBron James}"
OPPONENT="${2:-LAL}"
POINTS_LINE="${3:-25.5}"
REBOUNDS_LINE="${4:-8.5}"
ASSISTS_LINE="${5:-5.5}"

echo "================================================================================"
echo "🏀 NBA PLAYER SIMULATION TEST"
echo "================================================================================"
echo ""
echo "Player: $PLAYER_NAME"
echo "Opponent: $OPPONENT"
echo "Props: PTS $POINTS_LINE | REB $REBOUNDS_LINE | AST $ASSISTS_LINE"
echo ""
echo "================================================================================"
echo ""

# Test 1: Quick Odds - Points
echo "📊 Quick Odds - Points (Over $POINTS_LINE)"
echo "--------------------------------------------------------------------------------"
curl -s "http://localhost:8000/api/simulation/quick-odds/${PLAYER_NAME// /%20}?prop_type=points&line=$POINTS_LINE" | python3 -m json.tool
echo ""
echo ""

# Test 2: Quick Odds - Rebounds
echo "📊 Quick Odds - Rebounds (Over $REBOUNDS_LINE)"
echo "--------------------------------------------------------------------------------"
curl -s "http://localhost:8000/api/simulation/quick-odds/${PLAYER_NAME// /%20}?prop_type=rebounds&line=$REBOUNDS_LINE" | python3 -m json.tool
echo ""
echo ""

# Test 3: Quick Odds - Assists
echo "📊 Quick Odds - Assists (Over $ASSISTS_LINE)"
echo "--------------------------------------------------------------------------------"
curl -s "http://localhost:8000/api/simulation/quick-odds/${PLAYER_NAME// /%20}?prop_type=assists&line=$ASSISTS_LINE" | python3 -m json.tool
echo ""
echo ""

# Test 4: Single Game Simulation
echo "🎮 Single Game Simulation (10 games)"
echo "--------------------------------------------------------------------------------"
curl -s -X POST "http://localhost:8000/api/simulation/single-game" \
  -H "Content-Type: application/json" \
  -d "{
    \"player_name\": \"$PLAYER_NAME\",
    \"opponent\": \"$OPPONENT\",
    \"is_home\": true,
    \"num_simulations\": 10
  }" | python3 -c "import sys, json; data=json.load(sys.stdin); print(json.dumps({'player': data['player_name'], 'averages': data['averages'], 'sample_games': data['simulations'][:3]}, indent=2))"
echo ""
echo ""

# Test 5: Bet Outcome
echo "🎲 Bet Outcome - Points Over $POINTS_LINE (100 simulations)"
echo "--------------------------------------------------------------------------------"
curl -s -X POST "http://localhost:8000/api/simulation/bet-outcome" \
  -H "Content-Type: application/json" \
  -d "{
    \"player_name\": \"$PLAYER_NAME\",
    \"prop_type\": \"points\",
    \"line\": $POINTS_LINE,
    \"bet_type\": \"over\",
    \"num_simulations\": 100
  }" | python3 -c "import sys, json; data=json.load(sys.stdin); print(json.dumps({'win_probability': data['win_probability'], 'expected_value': data['expected_value'], 'recommendation': data['recommendation']}, indent=2))"
echo ""
echo ""

echo "================================================================================"
echo "✅ Test Complete!"
echo ""
echo "Usage examples:"
echo "  ./quick_test.sh \"Stephen Curry\" GSW 28.5 5.5 6.5"
echo "  ./quick_test.sh \"Kevin Durant\" PHX 27.5 7.5 5.5"
echo "  ./quick_test.sh \"Nikola Jokic\" DEN 26.5 12.5 9.5"
echo "================================================================================"
