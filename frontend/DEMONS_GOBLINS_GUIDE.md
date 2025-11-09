# 😈🤢 Demons and Goblins Feature Guide

## Overview

The **Demons and Goblins** feature allows users to select alternate, modified player projections in exchange for different payout multipliers. This adds a new strategic layer to lineup building where users can choose between:

- **Normal picks** - Standard projections with standard payouts
- **Demon picks** (😈) - Harder to win (higher lines) but significantly boosted payouts (up to 2000x)
- **Goblin picks** (🤢) - Easier to win (lower lines) but reduced payouts

---

## Core Mechanics

### Player Card States

Each player projection card can exist in **one of three mutually exclusive states**:

1. **Normal** - Default state with standard projection line
2. **Demon** - Modified state with a higher projection line (harder to hit)
3. **Goblin** - Modified state with a lower projection line (easier to hit)

**Important**: A card cannot be both Demon and Goblin simultaneously.

### Selection Constraints

- **Normal picks**: Can select either "MORE" or "LESS"
- **Demon picks**: Can **only** select "MORE" (LESS is disabled)
- **Goblin picks**: Can **only** select "MORE" (LESS is disabled)

---

## UI/UX Implementation

### Visual Indicators

#### Player Cards

**Demon State:**
- Red border (2px, `border-red-600`)
- Red glow shadow effect
- Red demon emoji badge (😈)
- Stat value displayed in red (`text-red-500`)
- Toggle button shows: `😈 +X.X` (difference from normal)

**Goblin State:**
- Green border (2px, `border-green-600`)
- Green glow shadow effect
- Green goblin emoji badge (🤢)
- Stat value displayed in green (`text-green-500`)
- Toggle button shows: `🤢 -X.X` (difference from normal)

#### Lineup Summary

Each selected player with a modifier shows:
- Left border accent (red for demon, green for goblin)
- Small emoji badge next to player name
- Colored stat value

#### Form Section

When demons or goblins are present, a banner displays:
```
😈 2 Demons    🤢 1 Goblin
⚠️ Promotions cannot be applied to lineups with Demons or Goblins
```

### Toggle Buttons

When available, small toggle buttons appear on the player card:

**Demon Button:**
```
😈 +4.0
```
Shows the additional points compared to normal line.

**Goblin Button:**
```
🤢 -3.0
```
Shows the reduction in points compared to normal line.

Clicking the active modifier toggles it off (returns to normal state).

---

## Payout Calculations

### Demon Multiplier Boost

Demons add a **fixed boost** to the base payout multiplier based on lineup size:

| Picks | Boost per Demon |
|-------|----------------|
| 2     | +10x          |
| 3     | +25x          |
| 4     | +100x         |
| 5     | +400x         |
| 6     | +2000x        |

**Example:**
- 6-pick Power Play normally pays **37.5x**
- With 1 Demon: **37.5x + 2000x = 2037.5x**
- With 2 Demons: **37.5x + 4000x = 4037.5x**

Demons **stack additively** - each additional demon adds another boost.

### Goblin Multiplier Reduction

Goblins apply a **reduction factor** to the payout multiplier:

| Picks | Reduction Factor |
|-------|-----------------|
| 2     | 0.5× (50%)     |
| 3     | 0.4× (40%)     |
| 4     | 0.3× (30%)     |
| 5     | 0.25× (25%)    |
| 6     | 0.2× (20%)     |

**Example:**
- 4-pick Power Play normally pays **10x**
- With 1 Goblin: **10x × 0.3 = 3x**
- With 2 Goblins: **10x × 0.3 × 0.3 = 0.9x**

Goblins **stack multiplicatively** - each additional goblin compounds the reduction.

### Mixed Lineups

You can combine Normal, Demon, and Goblin picks in the same lineup!

**Calculation Order:**
1. Calculate base payout (Power/Flex Play rules)
2. Apply Demon boosts (additive)
3. Apply Goblin reductions (multiplicative)

**Example - Mixed 6-pick:**
- Base Power Play: 37.5x
- 2 Demons: +4000x boost → 4037.5x
- 1 Goblin: ×0.2 reduction → **807.5x**

---

## Data Structure

### Type Definitions

```typescript
// SelectedPlayer interface (updated)
export interface SelectedPlayer {
  playerId: string;
  // ... other fields ...
  statValue: number;
  originalStatValue?: number; // Original before demon/goblin
  modifier?: 'demon' | 'goblin' | null;
}

// New interface for alternate projections
export interface AlternateProjection {
  demon?: number;  // Harder line (higher value)
  goblin?: number; // Easier line (lower value)
}
```

### Player Data Structure

```json
{
  "id": "1",
  "name": "LeBron James",
  "projections": {
    "points": 26.5,
    "rebounds": 7.5,
    "assists": 9.0
  },
  "alternateProjections": {
    "points": { 
      "demon": 30.5,   // +4.0 points harder
      "goblin": 23.5   // -3.0 points easier
    },
    "rebounds": { 
      "demon": 9.5,    // +2.0 rebounds harder
      "goblin": 6.5    // -1.0 rebounds easier
    },
    "assists": { 
      "demon": 11.0,   // +2.0 assists harder
      "goblin": 7.5    // -1.5 assists easier
    }
  }
}
```

Not every stat needs demon/goblin variants - only add where appropriate.

---

## Code Implementation

### Key Functions

#### `applyModifiers()` (payoutCalculator.ts)

```typescript
function applyModifiers(
  baseMultiplier: number,
  picks: Pick[]
): number {
  if (baseMultiplier === 0) return 0;

  const demonPicks = picks.filter(p => p.modifier === 'demon');
  const goblinPicks = picks.filter(p => p.modifier === 'goblin');
  const totalPicks = picks.length;
  
  let modifiedMultiplier = baseMultiplier;
  
  // Apply demon boost (additive)
  if (demonPicks.length > 0) {
    const boostPerDemon = DEMON_MULTIPLIER_BOOST[totalPicks] ?? 1;
    const totalDemonBoost = boostPerDemon * demonPicks.length;
    modifiedMultiplier = baseMultiplier + totalDemonBoost;
  }
  
  // Apply goblin reduction (multiplicative)
  if (goblinPicks.length > 0) {
    const reductionFactor = GOBLIN_MULTIPLIER_REDUCTION[totalPicks] ?? 1;
    const totalReduction = Math.pow(reductionFactor, goblinPicks.length);
    modifiedMultiplier = modifiedMultiplier * totalReduction;
  }
  
  return Math.max(0, modifiedMultiplier);
}
```

#### `handleModifierToggle()` (PlayerCardComponent.tsx)

```typescript
const handleModifierToggle = (newModifier: 'demon' | 'goblin') => {
  // Toggle: if already set to this modifier, clear it
  const toggledModifier = modifier === newModifier ? null : newModifier;
  setModifier(toggledModifier);
  
  // Calculate new stat value
  const newStatValue = toggledModifier === 'demon' && demonValue !== undefined
    ? demonValue
    : toggledModifier === 'goblin' && goblinValue !== undefined
    ? goblinValue
    : baseStatValue;
  
  // Update selectedPlayers if player is already selected
  if (selection) {
    setSelectedPlayers(prev => {
      const filtered = prev.filter(p => p.playerId !== player.id);
      return [...filtered, {
        // ... player data ...
        statValue: newStatValue,
        originalStatValue: baseStatValue,
        modifier: toggledModifier,
      }];
    });
  }
};
```

---

## Business Rules

### Promotions

**Critical Rule**: Promotions **cannot** be applied to any lineup containing at least one Demon or Goblin pick, unless the promotion explicitly states otherwise.

The UI displays this warning when demons/goblins are present:
```
⚠️ Promotions cannot be applied to lineups with Demons or Goblins
```

### Lineup Construction

- ✅ Can mix Normal, Demon, and Goblin picks freely
- ✅ Can have multiple Demons in one lineup
- ✅ Can have multiple Goblins in one lineup
- ✅ Can have both Demons and Goblins in same lineup
- ✅ Power Play and Flex Play both support modifiers
- ❌ Cannot select "LESS" on Demon or Goblin picks
- ❌ Cannot apply standard promotions to modified lineups

---

## User Stories

### ✅ Implemented

1. **As a user**, I want to see a visual indicator on a player card if a "Demon" or "Goblin" alternate line is available.
   - ✅ Toggle buttons appear when `alternateProjections` exist

2. **As a user**, I want to be able to toggle a player card between its "Normal" state and its "Demon" or "Goblin" state.
   - ✅ Click toggle button to activate/deactivate modifier

3. **As a user**, when I select a "Demon" or "Goblin" projection, I want to be forced to select "MORE" and understand that "LESS" is not an option.
   - ✅ LESS button disabled when modifier active

4. **As a user**, I want to see my lineup's potential payout multiplier increase when I add a "Demon" and decrease when I add a "Goblin."
   - ✅ Real-time payout calculation with modifiers

5. **As a user**, I want to be able to mix and match Normal, Demon, and Goblin picks in the same lineup.
   - ✅ All combinations supported

6. **As an admin**, I want to disable standard promotions for any lineup that includes at least one Demon or Goblin pick.
   - ✅ Warning message displayed when modifiers present

---

## Testing Examples

### Test Case 1: Single Demon Boost
```typescript
// 3-pick Power Play with 1 Demon
picks = [
  { modifier: 'demon', status: 'win' },
  { modifier: null, status: 'win' },
  { modifier: null, status: 'win' }
]
// Base: 6x
// Demon boost: +25x
// Result: 31x
```

### Test Case 2: Multiple Goblins
```typescript
// 4-pick Power Play with 2 Goblins
picks = [
  { modifier: 'goblin', status: 'win' },
  { modifier: 'goblin', status: 'win' },
  { modifier: null, status: 'win' },
  { modifier: null, status: 'win' }
]
// Base: 10x
// Goblin reduction: 0.3 × 0.3 = 0.09
// Result: 0.9x
```

### Test Case 3: Mixed Lineup
```typescript
// 6-pick Power Play: 2 Demons, 1 Goblin
picks = [
  { modifier: 'demon', status: 'win' },
  { modifier: 'demon', status: 'win' },
  { modifier: 'goblin', status: 'win' },
  { modifier: null, status: 'win' },
  { modifier: null, status: 'win' },
  { modifier: null, status: 'win' }
]
// Base: 37.5x
// Demon boost: +4000x → 4037.5x
// Goblin reduction: ×0.2 → 807.5x
```

---

## Future Enhancements

### Potential Features
- [ ] Seasonal demon/goblin themes (Halloween, Christmas, etc.)
- [ ] Special demon/goblin-only promotions
- [ ] Demon/goblin leaderboards
- [ ] Achievement system for hitting demon lineups
- [ ] AI-suggested demon/goblin combinations
- [ ] Historical demon/goblin win rates

### Analytics to Track
- Demon pick success rate vs normal
- Goblin pick success rate vs normal
- Average payout with demons
- User adoption rate of feature
- Most popular demon/goblin categories

---

## FAQ

**Q: Can I toggle between Demon and Goblin on the same pick?**  
A: Yes! Clicking a demon button when goblin is active will switch to demon (and vice versa).

**Q: What happens if I deselect MORE/LESS while a modifier is active?**  
A: The modifier is also cleared, returning the card to normal state.

**Q: Do demons/goblins work with Flex Play?**  
A: Yes! All modifier logic applies to both Power Play and Flex Play.

**Q: What if a player only has a Demon line but no Goblin (or vice versa)?**  
A: Only the available toggle button will show. Not all stats need both options.

**Q: Can I see the original line after activating a modifier?**  
A: Yes - the toggle button shows the difference (e.g., `+4.0` or `-3.0`), and the `originalStatValue` field stores the base projection.

**Q: What happens to modifiers when a pick pushes?**  
A: The pick is removed entirely (standard push behavior), and modifiers are recalculated on the remaining active picks.

---

## Summary

The Demons and Goblins feature adds exciting strategic depth to FanAssist:

- 😈 **Demons**: High risk, high reward (up to 2000x boosts)
- 🤢 **Goblins**: Low risk, low reward (reduced payouts)
- 🎯 **Strategy**: Mix and match for optimal risk/reward balance
- 🎨 **UX**: Clear visual indicators and real-time payout updates
- ⚠️ **Trade-off**: Cannot use standard promotions

This creates a more engaging, dynamic lineup-building experience while maintaining the core Power Play and Flex Play mechanics!
