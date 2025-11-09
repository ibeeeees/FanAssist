# Player Filtering & Injury Protection System

## Overview
The Daily Props system automatically filters out injured and inactive players to ensure you're only betting on players who are **actually playing**.

## Filtering Rules

### 1. Game Schedule Filter
✅ **Players MUST have a game today or tomorrow**
- Only shows players from teams with scheduled games
- Automatically updates based on NBA schedule
- No players from teams on off-days

### 2. Injury/Inactive Filter
✅ **Players MUST have recent game activity**
- Checks if player has played in the last **7 days**
- If no games in 7+ days → Player is filtered out (likely injured)
- If unable to verify recent games → Player is filtered out (safety)

### 3. Stats Availability Filter
✅ **Players MUST have current season stats**
- Requires valid season averages
- Requires recent game log data
- No rookies or players without enough games

## How It Works

### Backend Implementation
```python
# In popular_players.py
async def _get_team_popular_players():
    # 1. Get team roster
    roster = get_team_roster(team_id)
    
    # 2. For each popular player on the team
    for player_name in POPULAR_PLAYERS[team_id]:
        
        # 3. Check recent game activity (injury filter)
        recent_games = get_player_game_log(player_id, last_n_games=5)
        
        if not recent_games or len(recent_games) == 0:
            skip_player()  # No recent games = likely injured
            continue
        
        # 4. Check if last game was within 7 days
        last_game_date = recent_games[0].game_date
        days_since_last_game = (today - last_game_date).days
        
        if days_since_last_game > 7:
            skip_player()  # Haven't played in 7+ days = likely injured
            continue
        
        # 5. If passes all checks, include in results
        add_player_to_results()
```

## Player Status Examples

### ✅ INCLUDED (Active Players)
- **LeBron James**: Played 2 days ago, playing tonight
- **Stephen Curry**: Played yesterday, playing tomorrow
- **Giannis Antetokounmpo**: Played 3 days ago, playing today

### ❌ EXCLUDED (Filtered Out)
- **Joel Embiid**: Last game 10 days ago → **FILTERED** (likely injured)
- **Kawhi Leonard**: No games in 14 days → **FILTERED** (load management/injury)
- **Zion Williamson**: Last game 21 days ago → **FILTERED** (injured reserve)

## API Behavior

### GET /api/daily-props/today
```json
{
  "date": "2025-11-09",
  "count": 16,
  "players": [
    // ONLY includes:
    // - Players with games TODAY
    // - Players who played within last 7 days
    // - Players with valid season stats
  ]
}
```

### GET /api/daily-props/tomorrow
```json
{
  "date": "2025-11-10",
  "count": 18,
  "players": [
    // ONLY includes:
    // - Players with games TOMORROW
    // - Players who played within last 7 days
    // - Players with valid season stats
  ]
}
```

## Benefits

### 1. No Wasted Bets
- Can't accidentally bet on injured players
- No surprise "Player DNP - Injury" situations
- Only see players who are likely to play

### 2. Up-to-Date Information
- Automatically updates based on game logs
- Checks recent activity every request
- No manual injury report checking needed

### 3. Accurate Predictions
- Simulations only run on active players
- Season averages are from actual playing time
- More reliable betting outcomes

## Edge Cases

### Late Scratches
⚠️ **The system checks recent activity, not real-time injury reports**
- If a player is scratched **day-of** due to sudden injury, they may still appear
- NBA injury reports are updated closer to game time
- Consider checking official injury reports for day-of games

### Load Management
⚠️ **Players on load management may be filtered**
- If a star player rests frequently (every 3-4 games)
- If their last game was 8+ days ago
- They will be filtered out until they play again

### Season Start / Long Breaks
⚠️ **Players returning from extended breaks**
- First 1-2 games after All-Star break
- Season opener adjustments
- May need to reduce the 7-day threshold during breaks

## Console Output

When running the API, you'll see filtering messages:

```
✅ Added Giannis Antetokounmpo (MIL vs HOU)
✅ Added Stephen Curry (GSW vs IND)
⚠️  Skipping Joel Embiid - Last game was 12 days ago (likely injured)
⚠️  Skipping Kawhi Leonard - No recent games (likely injured or inactive)
✅ Added Ja Morant (MEM vs OKC)
```

## Configuration

### Adjust Injury Detection Threshold
Currently set to **7 days**. To change:

```python
# In popular_players.py, line ~178
if days_since_last_game > 7:  # Change this number
    skip_player()
```

**Recommendations:**
- **5 days**: More strict (filters out 2-game absences)
- **7 days**: Balanced (current setting)
- **10 days**: More lenient (allows longer breaks)
- **14 days**: Very lenient (only filters serious injuries)

## Testing

### Test Today's Players (With Injury Filter)
```bash
curl http://localhost:8000/api/daily-props/today
```

### Test Tomorrow's Players (With Injury Filter)
```bash
curl http://localhost:8000/api/daily-props/tomorrow
```

### Verify Filtering in Logs
```bash
tail -f /tmp/server.log | grep "Skipping"
```

## Summary

✅ **Automatic injury filtering**
- No injured players in results
- Only players with games today/tomorrow
- Only players who played within 7 days

✅ **Safe betting environment**
- Reduced risk of betting on inactive players
- Up-to-date game schedules
- Recent activity verification

✅ **Transparent logging**
- See which players are filtered and why
- Console output shows filtering decisions
- Easy to debug and verify

## Future Enhancements

### Potential Improvements:
1. **Real-time injury API integration**
   - Connect to official NBA injury reports
   - Check game-day status (Probable/Questionable/Out)
   - More accurate day-of filtering

2. **Injury history tracking**
   - Track which players are frequently injured
   - Adjust betting recommendations based on injury risk
   - Show injury history in player profiles

3. **Starting lineup verification**
   - Check if player is in starting lineup
   - Filter out benchwarming stars
   - Adjust lines based on expected minutes

4. **Load management predictions**
   - Predict which players will rest
   - Back-to-back game alerts
   - Rest day probability scores
