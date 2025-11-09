# Demons & Goblins - Quick Implementation Reference

## Files Modified

### 1. Type Definitions
**File**: `src/types/index.ts`
- Added `originalStatValue?: number` to `SelectedPlayer`
- Added `AlternateProjection` interface with `demon?` and `goblin?` properties

### 2. Payout Calculator
**File**: `src/services/payoutCalculator.ts`
- Added `DEMON_MULTIPLIER_BOOST` table (10x to 2000x)
- Added `GOBLIN_MULTIPLIER_REDUCTION` table (0.5x to 0.2x)
- Implemented `applyModifiers()` function with demon boost (additive) and goblin reduction (multiplicative)

### 3. Player Card Component
**File**: `src/components/PlayerCardComponent.tsx`
- Added `AlternateProjections` interface to Player type
- Added `modifier` state tracking ('demon' | 'goblin' | null)
- Added `handleModifierToggle()` function
- Updated stat value calculation based on active modifier
- Added demon/goblin toggle buttons (show +/- difference from normal)
- Disabled LESS button when modifier is active
- Added visual indicators (border colors, emoji badges, colored stat values)

### 4. Selected Players Summary
**File**: `src/components/SelectedPlayersSummary.tsx`
- Added `hasDemonOrGoblin`, `demonCount`, `goblinCount` calculations
- Updated player list to show modifier badges and colored borders
- Added demon/goblin info banner above form
- Added promotion warning when modifiers present

### 5. Styles
**File**: `src/index.css`
- Added `.player-card.demon-active` with red border and glow
- Added `.player-card.goblin-active` with green border and glow

### 6. Sample Data
**File**: `src/data/players.json`
- Added `alternateProjections` to LeBron James (id: 1)
- Added `alternateProjections` to Stephen Curry (id: 2)

---

## Key Features Implemented

✅ Visual toggles on player cards for demon/goblin  
✅ Demon = red theme (😈), harder to win, higher payouts  
✅ Goblin = green theme (🤢), easier to win, lower payouts  
✅ "LESS" disabled for demon/goblin picks (MORE only)  
✅ Real-time payout calculation with modifiers  
✅ Mixed lineups (normal + demon + goblin combinations)  
✅ Promotion warning for modified lineups  
✅ Visual indicators in lineup summary  
✅ Additive demon boosts (stack linearly)  
✅ Multiplicative goblin reductions (compound)  

---

## Usage Examples

### Player Card with Demon/Goblin Available
```tsx
// When alternateProjections exist:
{
  "projections": { "points": 26.5 },
  "alternateProjections": {
    "points": { 
      "demon": 30.5,   // +4.0 harder
      "goblin": 23.5   // -3.0 easier
    }
  }
}

// Shows toggle buttons:
[😈 +4.0]  [🤢 -3.0]
```

### Payout Calculation Example
```typescript
// 4-pick Power Play with 1 Demon
Base: 10x
Demon boost: +100x
Result: 110x multiplier

// With $10 entry = $1,100 payout
```

### Mixed Lineup Example
```typescript
// 6-pick with 2 Demons, 1 Goblin
Base: 37.5x
Demons: +4000x → 4037.5x
Goblin: ×0.2 → 807.5x final
```

---

## Testing Checklist

- [ ] Toggle demon on/off on player card
- [ ] Toggle goblin on/off on player card
- [ ] Cannot select LESS with demon active
- [ ] Cannot select LESS with goblin active
- [ ] Stat value updates when toggling modifiers
- [ ] Border color changes (red/green)
- [ ] Emoji badges appear
- [ ] Lineup summary shows modifiers
- [ ] Payout increases with demons
- [ ] Payout decreases with goblins
- [ ] Warning banner appears
- [ ] Demon/goblin counts correct
- [ ] Mix of all three types works
- [ ] Deselecting clears modifier

---

## Next Steps (Optional Enhancements)

1. Add more players with alternate projections
2. Create demon/goblin-specific promotions
3. Add analytics tracking for modifier usage
4. Implement seasonal theming
5. Add tooltips explaining modifier mechanics
6. Create demo mode showcasing feature
7. Add achievements for hitting demon lineups
8. Optimize payout algorithm for edge cases
