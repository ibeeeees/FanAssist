# Working with Live Backend Data + Demons & Goblins

## 📡 Data Flow Overview

```
Backend API → transformBackendPlayer() → Player Object → PlayerCardComponent → SelectedPlayer → BettingPanel → Backend
```

---

## 🔄 How Live Data Works

### 1. Fetching Players from Backend

**File**: `frontend/src/App.tsx`

```typescript
// Fetch live data on mount and every 5 minutes
const fetchPlayersFromBackend = async () => {
  const response = await getTodaysPlayers(); // Calls /api/daily-props/today
  const transformedPlayers = response.players.map((player, index) => 
    transformBackendPlayer(player, index)
  );
  setPlayers(transformedPlayers);
};
```

**Backend Endpoint**: `GET /api/daily-props/today`

### 2. Transforming Backend Data

**File**: `frontend/src/services/api.ts`

The `transformBackendPlayer()` function converts backend data to frontend format:

```typescript
export function transformBackendPlayer(backendPlayer: any, index: number) {
  return {
    id: backendPlayer.player_id || `player-${index}`,
    name: backendPlayer.player_name,
    image: backendPlayer.image_url || generateHeadshotUrl(backendPlayer.player_name),
    team: backendPlayer.team || 'Unknown',
    teamAbbr: backendPlayer.team || 'UNK',
    position: [backendPlayer.position || 'G'],
    gameLocation: backendPlayer.game_info?.location || 'home',
    opponent: backendPlayer.opponent || 'TBD',
    opponentAbbr: backendPlayer.opponent || 'TBD',
    gameDay: backendPlayer.game_info?.day || 'Today',
    gameTime: backendPlayer.game_info?.time || 'TBD',
    gameDate: backendPlayer.game_date || new Date().toISOString(),
    projections: {
      points: backendPlayer.lines?.points || 0,
      rebounds: backendPlayer.lines?.rebounds || 0,
      assists: backendPlayer.lines?.assists || 0,
      threePointersMade: backendPlayer.lines?.threes_made || 0,
      // ... all other stat categories
    },
    specialModifier: undefined, // TODO: Add to backend response
    modifierMultiplier: undefined, // TODO: Add to backend response
    isInjured: backendPlayer.is_injured || false,
    injuryStatus: backendPlayer.injury_status || null,
  };
}
```

---

## 🎲 Adding Demons & Goblins to Live Data

### Option 1: Backend Response (Recommended)

**Update backend to return modifiers**:

```python
# backend/app/routes/daily_props.py

def get_todays_players():
    players = []
    for player in popular_players:
        player_data = {
            "player_name": player["name"],
            "player_id": player["id"],
            "lines": get_lines(player),
            # Add modifier fields
            "special_modifier": player.get("special_modifier"),  # 'demon' or 'goblin'
            "modifier_multiplier": player.get("modifier_multiplier"),  # +4.0, -3.0, etc.
        }
        players.append(player_data)
    return players
```

Then update `transformBackendPlayer()`:

```typescript
export function transformBackendPlayer(backendPlayer: any, index: number) {
  return {
    // ... other fields
    specialModifier: backendPlayer.special_modifier as 'demon' | 'goblin' | undefined,
    modifierMultiplier: backendPlayer.modifier_multiplier,
  };
}
```

### Option 2: Frontend Hardcoding (Temporary)

**Add modifiers in transformation**:

```typescript
export function transformBackendPlayer(backendPlayer: any, index: number) {
  // Hardcode specific players as demons/goblins
  const demonPlayers = {
    'LeBron James': { modifier: 'demon' as const, multiplier: 4.0 },
    'Giannis Antetokounmpo': { modifier: 'demon' as const, multiplier: 5.5 },
  };
  
  const goblinPlayers = {
    'Stephen Curry': { modifier: 'goblin' as const, multiplier: -3.0 },
  };
  
  const playerName = backendPlayer.player_name;
  const demonData = demonPlayers[playerName];
  const goblinData = goblinPlayers[playerName];
  
  return {
    // ... other fields
    specialModifier: demonData?.modifier || goblinData?.modifier,
    modifierMultiplier: demonData?.multiplier || goblinData?.multiplier,
  };
}
```

### Option 3: Static + Live Hybrid

**Merge static player data with live data**:

```typescript
// In App.tsx
const fetchPlayersFromBackend = async () => {
  const response = await getTodaysPlayers();
  const transformedPlayers = response.players.map((livePlayer, index) => {
    // Find matching static player from players.json
    const staticPlayer = playersData.players.find(
      p => p.name === livePlayer.player_name
    );
    
    return transformBackendPlayer(livePlayer, index, staticPlayer);
  });
  setPlayers(transformedPlayers);
};

// Update transformBackendPlayer signature
export function transformBackendPlayer(
  backendPlayer: any, 
  index: number,
  staticPlayer?: any
) {
  return {
    // ... other fields
    specialModifier: staticPlayer?.specialModifier,
    modifierMultiplier: staticPlayer?.modifierMultiplier,
  };
}
```

---

## 🎯 Backend Integration for Betting

### Submitting Bets with Modifiers

**File**: `frontend/src/components/BettingPanel.tsx`

```typescript
const parlayData = {
  bets: selectedPlayers.map(player => ({
    player_name: player.playerName,
    prop_type: propTypeMap[player.category] || 'points',
    line: player.statValue,  // This is the MODIFIED value
    pick: player.selection === 'more' ? 'OVER' : 'UNDER',
    // Add modifier info
    modifier: player.modifier,
    original_line: player.originalStatValue,  // Base value before modifier
  })),
  total_wager: wager,
  bet_mode: betMode,
};
```

### Backend Handling

**Update backend to process modifiers**:

```python
# backend/app/routes/daily_props.py

@router.post("/place-parlay")
def place_parlay(parlay: ParlayRequest):
    results = []
    for bet in parlay.bets:
        # Simulate the game
        simulated_value = simulate_player_performance(bet.player_name, bet.prop_type)
        
        # Apply modifier to simulation if present
        if bet.modifier == 'demon':
            # Demon boosts are already in the line, so simulate normally
            # But could add variance or special logic
            pass
        elif bet.modifier == 'goblin':
            # Goblin reductions are in the line
            pass
        
        # Check if bet won
        if bet.pick == 'OVER':
            won = simulated_value > bet.line
        else:
            won = simulated_value < bet.line
        
        results.append({
            "player_name": bet.player_name,
            "simulated_value": simulated_value,
            "line": bet.line,
            "original_line": bet.original_line,
            "modifier": bet.modifier,
            "won": won
        })
    
    # Calculate payout with demon/goblin multipliers
    payout = calculate_payout_with_modifiers(results, parlay.bet_mode, parlay.total_wager)
    
    return {
        "legs": results,
        "payout": payout,
        "won": all(r["won"] for r in results)
    }
```

---

## 🧮 Payout Calculation with Modifiers

### Frontend Payout Calculator

**File**: `frontend/src/services/payoutCalculator.ts`

```typescript
export function calculatePayout(
  picks: Pick[],
  playType: 'power' | 'flex',
  entryAmount: number
) {
  const numPicks = picks.length;
  
  // Get base multiplier
  let multiplier = POWER_PLAY_MULTIPLIERS[numPicks] || 1;
  
  if (playType === 'flex') {
    multiplier = FLEX_PLAY_MULTIPLIERS[numPicks] || 1;
  }
  
  // Apply demon/goblin modifiers
  const { demonBoost, goblinReduction } = applyModifiers(picks);
  
  // Demons: Additive boost
  multiplier += demonBoost;
  
  // Goblins: Multiplicative reduction (compounds)
  multiplier *= goblinReduction;
  
  return {
    multiplier,
    payoutAmount: entryAmount * multiplier,
    entryAmount,
  };
}

function applyModifiers(picks: Pick[]) {
  const numPicks = picks.length;
  const demonPicks = picks.filter(p => p.modifier === 'demon');
  const goblinPicks = picks.filter(p => p.modifier === 'goblin');
  
  // Demon boost (additive)
  const demonBoostTable = DEMON_MULTIPLIER_BOOST[numPicks] || 0;
  const demonBoost = demonPicks.length > 0 ? demonBoostTable : 0;
  
  // Goblin reduction (multiplicative)
  const goblinReductionTable = GOBLIN_MULTIPLIER_REDUCTION[numPicks] || 1;
  const goblinReduction = Math.pow(goblinReductionTable, goblinPicks.length);
  
  return { demonBoost, goblinReduction };
}
```

### Example Calculation

**3-leg parlay with 1 demon, 1 goblin, 1 normal**:

```
Base Power Play (3 picks): 3.0x
Demon Boost (3 picks):    +25x   (additive)
Goblin Reduction (3 picks): 0.65x (multiplicative)

Total Multiplier = (3.0 + 25) × 0.65 = 28 × 0.65 = 18.2x

$10 entry → $182 payout
```

---

## 🎨 UI States with Live Data

### Player Card States

1. **No Selection** - Gray border, normal stat
2. **MORE Selected** - Green border, normal stat
3. **LESS Selected** - Red border, normal stat
4. **Modifier Available** - Toggle button visible (top-right)
5. **Modifier Active + MORE** - Colored border (red/green), modified stat, colored MORE button
6. **Modifier Disabled** - Toggle greyed out (when LESS selected or no selection)

### Visual Indicators

```tsx
{/* Card border */}
<div className={`player-card ${
  modifierActive && specialModifier === 'demon' ? 'demon-active' : 
  modifierActive && specialModifier === 'goblin' ? 'goblin-active' : 
  selection ? 'active' : ''
}`}>

{/* Stat value color */}
<div className={`text-xl font-normal ${
  modifierActive 
    ? specialModifier === 'demon' ? 'text-red-600' : 'text-green-600'
    : ''
}`}>
  {displayStatValue.toFixed(1)}
</div>

{/* Modifier indicator dot */}
{modifierActive && specialModifier && (
  <div className={`w-1 h-1 rounded-full ${
    specialModifier === 'demon' ? 'bg-red-600' : 'bg-green-600'
  }`}></div>
)}
```

---

## 🔧 Debugging Tips

### Check Live Data Structure

```typescript
// In App.tsx after fetching
console.log('Live players:', players);
console.log('First player:', players[0]);
console.log('Modifiers:', players.filter(p => p.specialModifier));
```

### Verify Modifier Activation

```typescript
// In PlayerCardComponent
console.log('Modifier state:', {
  specialModifier,
  modifierMultiplier,
  modifierActive,
  baseStatValue,
  displayStatValue,
});
```

### Test Betting Submission

```typescript
// In BettingPanel before submission
console.log('Parlay data:', JSON.stringify(parlayData, null, 2));
```

---

## ✅ Implementation Checklist

- [ ] Backend returns `special_modifier` and `modifier_multiplier`
- [ ] `transformBackendPlayer()` maps modifier fields
- [ ] Modifier toggle button appears for eligible players
- [ ] Stat value updates when modifier activated
- [ ] Card border changes color (red/green)
- [ ] MORE button changes color when modifier active
- [ ] LESS button disabled when modifier active
- [ ] Modifier state persists in selectedPlayers
- [ ] BettingPanel sends modifier info to backend
- [ ] Backend applies modifier logic in simulation
- [ ] Payout calculator accounts for demons/goblins
- [ ] Results display shows modifier effects

---

**Remember**: The demo branch brought live data, but **you need to ensure demons & goblins work with that live data** by implementing one of the three options above!
