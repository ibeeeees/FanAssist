# 💰 Payout Calculator - FanAssistant

## Overview

The **Payout Calculator** is the core engine for calculating winnings in FanAssistant, based on PrizePicks rules. It supports two game modes: **Power Play** and **Flex Play**, each with distinct payout structures and rules.

---

## 📋 Table of Contents

- [Game Modes](#game-modes)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Payout Tables](#payout-tables)
- [Rules & Logic](#rules--logic)
- [Examples](#examples)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)

---

## 🎮 Game Modes

### Power Play (All-or-Nothing)

- **Win Condition**: ALL picks must be correct
- **Loss Condition**: ANY single loss = 0x payout
- **Push Rule**: Pushes are removed, payout adjusts to next tier down
- **Payout Range**: 3x - 37.5x

### Flex Play (Partial Wins Allowed)

- **Win Condition**: Varies by number of picks
- **Loss Condition**: Based on minimum correct picks required
- **Push Rule**: Pushes removed, graded as smaller lineup
- **Payout Range**: 0.4x - 25x

---

## 📦 Installation

The payout calculator is located in:
```
frontend/src/services/payoutCalculator.ts
```

No additional dependencies required beyond TypeScript.

---

## 🚀 Usage

### Basic Function Call

```typescript
import { calculatePayout } from '../services/payoutCalculator';

const picks = [
  { id: '1', playerId: 'p1', playerName: 'LeBron James', category: 'Points', 
    selection: 'more', statValue: 25.5, status: 'win' },
  { id: '2', playerId: 'p2', playerName: 'Stephen Curry', category: 'Points', 
    selection: 'more', statValue: 28.5, status: 'win' },
  // ... more picks
];

const result = calculatePayout(picks, 'power', 10);

console.log(result.multiplier);      // e.g., 3
console.log(result.payoutAmount);    // e.g., 30
console.log(result.isWinner);        // true/false
```

### Using the Class Approach

```typescript
import { PayoutCalculator } from '../services/payoutCalculator';

const calculator = new PayoutCalculator(picks, 'flex', 25);

console.log(calculator.isWinner());          // true/false
console.log(calculator.getMultiplier());     // e.g., 10
console.log(calculator.getPayoutAmount());   // e.g., 250
```

### React Component Integration

```typescript
import PayoutDisplay from '../components/PayoutDisplay';

function MyComponent() {
  const [selectedPlayers, setSelectedPlayers] = useState<SelectedPlayer[]>([]);
  const [playType, setPlayType] = useState<'power' | 'flex'>('power');
  const [entryAmount, setEntryAmount] = useState(10);

  return (
    <PayoutDisplay
      selectedPlayers={selectedPlayers}
      playType={playType}
      entryAmount={entryAmount}
    />
  );
}
```

---

## 📚 API Reference

### Main Function

#### `calculatePayout(picks, playType, entryAmount)`

**Parameters:**
- `picks` (Pick[]): Array of pick objects
- `playType` ('power' | 'flex'): Game mode
- `entryAmount` (number): Amount wagered (default: 1)

**Returns:** `PayoutResult`
```typescript
{
  multiplier: number;           // Payout multiplier (e.g., 37.5)
  originalPickCount: number;    // Original number of picks
  activePickCount: number;      // Picks after removing pushes
  winCount: number;             // Number of wins
  lossCount: number;            // Number of losses
  pushCount: number;            // Number of pushes
  isWinner: boolean;            // True if payout > 0
  payoutAmount: number;         // Final payout (entry × multiplier)
}
```

### Pick Object Structure

```typescript
interface Pick {
  id: string;
  playerId: string;
  playerName: string;
  category: string;
  selection: 'more' | 'less';
  statValue: number;
  status?: 'win' | 'loss' | 'push';
  modifier?: 'demon' | 'goblin' | null;
}
```

### Utility Functions

#### `formatMultiplier(multiplier: number): string`
Formats multiplier for display (e.g., `3` → `"3x"`)

#### `formatCurrency(amount: number): string`
Formats amount as currency (e.g., `30` → `"$30.00"`)

#### `getPayoutDescription(result: PayoutResult): string`
Returns human-readable description of payout result

---

## 📊 Payout Tables

### Power Play Payouts

| Picks | Multiplier |
|-------|-----------|
| 6     | 37.5x     |
| 5     | 20x       |
| 4     | 10x       |
| 3     | 6x        |
| 2     | 3x        |
| 1     | No payout |

### Flex Play Payouts

| Total Picks | Correct Picks | Multiplier |
|------------|--------------|-----------|
| 6          | 6            | 25x       |
| 6          | 5            | 2x        |
| 6          | 4            | 0.4x      |
| 5          | 5            | 10x       |
| 5          | 4            | 2x        |
| 5          | 3            | 0.4x      |
| 4          | 4            | 6x        |
| 4          | 3            | 1.5x      |
| 3          | 3            | 3x        |
| 3          | 2            | 1x        |

---

## ⚖️ Rules & Logic

### Push Handling (Critical)

**What is a Push?**
- A pick that results in a tie (exact stat value)
- A pick for a player who doesn't play (DNP)

**How Pushes Work:**

1. **Power Play:**
   - Push is removed from lineup
   - Payout adjusts to next tier down
   - Example: 6-pick with 1 push → graded as 5-pick

2. **Flex Play:**
   - Push is removed from lineup
   - Entry graded as smaller lineup
   - Example: 6-pick with 1 push, 4 wins, 1 loss → graded as 5-pick with 4/5 correct

**Important Edge Cases:**

```typescript
// Power Play: 2-pick with 1 push → 1-pick (no payout)
picks = [
  { status: 'win' },
  { status: 'push' }
];
// Result: 0x (1-pick has no payout table entry)

// Flex Play: 6-pick with 1 push, 4 wins → 5-pick, 4/5 correct = 2x
picks = [
  { status: 'win' },
  { status: 'win' },
  { status: 'win' },
  { status: 'win' },
  { status: 'loss' },
  { status: 'push' }
];
// Result: 2x (from 5-pick table, 4/5 row)
```

### Power Play Logic

```
1. Remove all pushes from picks
2. Count remaining active picks
3. IF any active pick is a loss:
     RETURN 0x
4. ELSE IF all active picks are wins:
     LOOKUP payout from POWER_PLAY_PAYOUTS[activeCount]
5. ELSE:
     RETURN 0x (no payout defined)
```

### Flex Play Logic

```
1. Remove all pushes from picks
2. Count remaining active picks
3. Count number of wins in active picks
4. LOOKUP payout from FLEX_PLAY_PAYOUTS[activeCount][winCount]
5. IF no payout defined:
     RETURN 0x
6. ELSE:
     RETURN payout multiplier
```

---

## 💡 Examples

### Example 1: Power Play - Perfect 6-Pick

```typescript
const picks = [
  { id: '1', playerName: 'LeBron James', status: 'win' },
  { id: '2', playerName: 'Stephen Curry', status: 'win' },
  { id: '3', playerName: 'Kevin Durant', status: 'win' },
  { id: '4', playerName: 'Giannis', status: 'win' },
  { id: '5', playerName: 'Luka Doncic', status: 'win' },
  { id: '6', playerName: 'Nikola Jokic', status: 'win' },
];

const result = calculatePayout(picks, 'power', 10);
// result.multiplier = 37.5
// result.payoutAmount = $375.00
```

### Example 2: Power Play - 1 Push

```typescript
const picks = [
  { id: '1', playerName: 'LeBron James', status: 'win' },
  { id: '2', playerName: 'Stephen Curry', status: 'win' },
  { id: '3', playerName: 'Kevin Durant', status: 'push' }, // DNP
  { id: '4', playerName: 'Giannis', status: 'win' },
  { id: '5', playerName: 'Luka Doncic', status: 'win' },
  { id: '6', playerName: 'Nikola Jokic', status: 'win' },
];

const result = calculatePayout(picks, 'power', 10);
// result.originalPickCount = 6
// result.activePickCount = 5 (1 push removed)
// result.multiplier = 20 (5-pick payout)
// result.payoutAmount = $200.00
```

### Example 3: Flex Play - Mixed Results

```typescript
const picks = [
  { id: '1', playerName: 'LeBron James', status: 'win' },
  { id: '2', playerName: 'Stephen Curry', status: 'win' },
  { id: '3', playerName: 'Kevin Durant', status: 'loss' },
  { id: '4', playerName: 'Giannis', status: 'win' },
  { id: '5', playerName: 'Luka Doncic', status: 'win' },
  { id: '6', playerName: 'Nikola Jokic', status: 'win' },
];

const result = calculatePayout(picks, 'flex', 10);
// result.winCount = 5
// result.activePickCount = 6
// result.multiplier = 2 (6-pick, 5/6 correct)
// result.payoutAmount = $20.00
```

### Example 4: Flex Play - Push Adjustment

```typescript
const picks = [
  { id: '1', playerName: 'LeBron James', status: 'win' },
  { id: '2', playerName: 'Stephen Curry', status: 'push' },
  { id: '3', playerName: 'Kevin Durant', status: 'win' },
  { id: '4', playerName: 'Giannis', status: 'push' },
  { id: '5', playerName: 'Luka Doncic', status: 'win' },
];

const result = calculatePayout(picks, 'flex', 10);
// result.originalPickCount = 5
// result.activePickCount = 3 (2 pushes removed)
// result.winCount = 3
// result.multiplier = 3 (3-pick, 3/3 correct)
// result.payoutAmount = $30.00
```

---

## 🧪 Testing

### Run Test File

```bash
# Using ts-node
npx ts-node src/services/payoutCalculator.test.ts

# Or compile and run
tsc src/services/payoutCalculator.test.ts
node src/services/payoutCalculator.test.js
```

### Test Coverage

The test file (`payoutCalculator.test.ts`) includes:

- ✅ 6-pick Power Play - all wins (37.5x)
- ✅ 6-pick Power Play - 1 loss (0x)
- ✅ 6-pick Power Play - 1 push (20x as 5-pick)
- ✅ 2-pick Power Play - 1 push (0x as 1-pick)
- ✅ 6-pick Flex Play - all wins (25x)
- ✅ 6-pick Flex Play - 5/6 wins (2x)
- ✅ 6-pick Flex Play - 4/6 wins (0.4x)
- ✅ 6-pick Flex Play - 1 push, 4 wins (2x as 5-pick, 4/5)
- ✅ 5-pick Flex Play - 2 pushes, 3 wins (3x as 3-pick, 3/3)
- ✅ 6-pick Flex Play - 3/6 wins (0x)
- ✅ Class approach validation

---

## 🔮 Future Enhancements

### Demon & Goblin Picks

**Planned Implementation:**

```typescript
// Demon Pick: Reduces overall payout but easier to hit
const demonPick: Pick = {
  id: '1',
  playerName: 'LeBron James',
  modifier: 'demon',
  status: 'win'
};

// Goblin Pick: Increases payout but harder to hit
const goblinPick: Pick = {
  id: '2',
  playerName: 'Stephen Curry',
  modifier: 'goblin',
  status: 'win'
};
```

**Modifier Logic (To Be Implemented):**

The `applyModifiers()` function is already scaffolded for future use:

```typescript
function applyModifiers(
  baseMultiplier: number,
  picks: Pick[],
  playType: PlayType
): number {
  const demonPicks = picks.filter(p => p.modifier === 'demon');
  const goblinPicks = picks.filter(p => p.modifier === 'goblin');
  
  let adjustedMultiplier = baseMultiplier;
  
  // Apply demon reduction
  demonPicks.forEach(() => {
    adjustedMultiplier *= 0.75; // 25% reduction per demon
  });
  
  // Apply goblin boost
  goblinPicks.forEach(() => {
    adjustedMultiplier *= 1.5; // 50% boost per goblin
  });
  
  return adjustedMultiplier;
}
```

### Additional Enhancements

- [ ] Insurance picks (get money back on 1 loss)
- [ ] Progressive parlays (varying payouts based on combo)
- [ ] Live betting adjustments (mid-game changes)
- [ ] Historical payout tracking
- [ ] Odds calculator integration
- [ ] Expected value (EV) calculations

---

## 📝 Notes

### Design Decisions

1. **Immutable Calculations**: The calculator never modifies input data
2. **Type Safety**: Full TypeScript coverage prevents runtime errors
3. **Extensibility**: Class-based approach allows easy feature additions
4. **Separation of Concerns**: Display formatting separate from calculation logic

### Performance Considerations

- Time Complexity: O(n) where n = number of picks
- Space Complexity: O(1) (no additional data structures created)
- All calculations happen synchronously (no async overhead)

### Edge Cases Handled

- ✅ Empty picks array (throws error)
- ✅ All pushes (returns 0x)
- ✅ Invalid play type (throws error)
- ✅ Pushes reducing to invalid tier (returns 0x)
- ✅ Too few wins for Flex Play (returns 0x)

---

## 👥 Contributing

When adding new features to the payout calculator:

1. Update the payout tables if needed
2. Add tests to `payoutCalculator.test.ts`
3. Update this README with new examples
4. Ensure TypeScript types are up to date
5. Test edge cases thoroughly

---

## 📄 License

Part of FanAssistant project. See main project LICENSE.

---

**Questions?** Contact the development team or create an issue in the repository.
