# 🚀 Payout Calculator - Quick Reference

## 30-Second Quickstart

```typescript
import { calculatePayout } from './services/payoutCalculator';

const picks = [
  { id: '1', playerName: 'LeBron', category: 'Points', 
    selection: 'more', statValue: 25.5, status: 'win' },
  // ... more picks
];

const result = calculatePayout(picks, 'power', 10);
console.log(result.payoutAmount); // $375.00
```

---

## Cheat Sheet

### Payout Tables

| **Power Play** | **Multiplier** |
|---------------|---------------|
| 6 picks       | 37.5x         |
| 5 picks       | 20x           |
| 4 picks       | 10x           |
| 3 picks       | 6x            |
| 2 picks       | 3x            |

| **Flex Play** | **6/6** | **5/6** | **4/6** | **3/6** |
|--------------|---------|---------|---------|---------|
| Multiplier   | 25x     | 2x      | 0.4x    | 0x      |

---

## Common Code Snippets

### 1. Basic Calculation
```typescript
const result = calculatePayout(picks, 'power', 10);
```

### 2. React Integration
```tsx
const payoutResult = useMemo(() => {
  const picks = selectedPlayers.map(p => ({
    ...p,
    id: p.playerId,
    status: 'win',
  }));
  return calculatePayout(picks, playType, entryAmount);
}, [selectedPlayers, playType, entryAmount]);
```

### 3. Format for Display
```typescript
import { formatMultiplier, formatCurrency } from './services/payoutCalculator';

<div>{formatMultiplier(result.multiplier)}</div>  // "37.5x"
<div>{formatCurrency(result.payoutAmount)}</div>  // "$375.00"
```

### 4. Class Approach
```typescript
const calculator = new PayoutCalculator(picks, 'flex', 25);
console.log(calculator.isWinner());
console.log(calculator.getPayoutAmount());
```

---

## Pick Status Rules

```typescript
// Win (More): actualValue > projectedValue
{ selection: 'more', statValue: 25.5, actualValue: 28.0 } // WIN ✅

// Win (Less): actualValue < projectedValue
{ selection: 'less', statValue: 8.5, actualValue: 7.0 } // WIN ✅

// Loss (More): actualValue <= projectedValue
{ selection: 'more', statValue: 25.5, actualValue: 24.0 } // LOSS ❌

// Push: actualValue === projectedValue OR DNP
{ selection: 'more', statValue: 25.5, actualValue: 25.5 } // PUSH ➖
```

---

## Push Handling

### Power Play
```
6 picks + 1 push = graded as 5-pick (20x)
2 picks + 1 push = graded as 1-pick (0x - no payout)
```

### Flex Play
```
6 picks, 4 wins, 1 loss, 1 push = graded as 5-pick with 4/5 (2x)
5 picks, 3 wins, 2 pushes = graded as 3-pick with 3/3 (3x)
```

---

## TypeScript Types

```typescript
type PlayType = 'power' | 'flex';
type PickStatus = 'win' | 'loss' | 'push';
type PickModifier = 'demon' | 'goblin' | null;

interface Pick {
  id: string;
  playerId: string;
  playerName: string;
  category: string;
  selection: 'more' | 'less';
  statValue: number;
  status?: PickStatus;
  modifier?: PickModifier;
}

interface PayoutResult {
  multiplier: number;
  payoutAmount: number;
  originalPickCount: number;
  activePickCount: number;
  winCount: number;
  lossCount: number;
  pushCount: number;
  isWinner: boolean;
}
```

---

## API Methods

### Main Function
```typescript
calculatePayout(picks, playType, entryAmount)
// Returns: PayoutResult
```

### Class Methods
```typescript
new PayoutCalculator(picks, playType, entryAmount)
.calculate()           // Full PayoutResult
.isWinner()           // boolean
.getMultiplier()      // number
.getPayoutAmount()    // number
.getActivePicks()     // Pick[]
.getCounts()          // { total, wins, losses, pushes }
```

### Utility Functions
```typescript
formatMultiplier(37.5)              // "37.5x"
formatCurrency(375)                 // "$375.00"
getPayoutDescription(result)        // Human-readable string
```

---

## Testing Scenarios

```bash
# Run tests
npx ts-node src/services/payoutCalculator.test.ts
```

**Test Coverage:**
- ✅ 6-pick Power Play (37.5x)
- ✅ Power Play with loss (0x)
- ✅ Power Play with push (20x as 5-pick)
- ✅ 6-pick Flex Play (25x)
- ✅ Flex Play 5/6 (2x)
- ✅ Flex Play with push adjustment
- ✅ Edge cases

---

## Common Mistakes to Avoid

❌ **Wrong:** Setting status after calculation
```typescript
const result = calculatePayout(picks, 'power', 10);
picks[0].status = 'win'; // Too late!
```

✅ **Right:** Set status before calculation
```typescript
picks[0].status = 'win';
const result = calculatePayout(picks, 'power', 10);
```

---

❌ **Wrong:** Forgetting to handle pushes
```typescript
// Assuming 6 picks always = 6 active picks
```

✅ **Right:** Use activePickCount from result
```typescript
console.log(result.activePickCount); // Accounts for pushes
```

---

❌ **Wrong:** Hardcoding multipliers
```typescript
const payout = entryFee * 37.5; // What if there's a push?
```

✅ **Right:** Use calculator
```typescript
const result = calculatePayout(picks, 'power', entryFee);
const payout = result.payoutAmount; // Handles all cases
```

---

## Environment Setup

### Required Files
```
src/
├── services/
│   ├── payoutCalculator.ts       ← Core
│   ├── payoutCalculator.test.ts  ← Tests
│   └── resultEvaluator.ts        ← Result eval
└── types/
    └── index.ts                   ← Types
```

### No Dependencies
- Pure TypeScript
- No npm packages required
- Works with React, Vue, Angular, vanilla JS

---

## Integration Checklist

- [ ] Import `calculatePayout` from `./services/payoutCalculator`
- [ ] Add `status?: PickStatus` to your Pick/Player type
- [ ] Create state for `playType: 'power' | 'flex'`
- [ ] Create state for `entryAmount: number`
- [ ] Use `useMemo` for real-time calculation
- [ ] Display `result.multiplier` and `result.payoutAmount`
- [ ] Handle pushes in UI (show `activePickCount` vs `originalPickCount`)
- [ ] Test with various pick combinations
- [ ] Add error handling for edge cases

---

## Troubleshooting

### "Picks array cannot be empty"
```typescript
// Check for empty array before calling
if (picks.length === 0) return null;
const result = calculatePayout(picks, playType, entryAmount);
```

### "Play type must be 'power' or 'flex'"
```typescript
// Ensure playType is typed correctly
const playType: 'power' | 'flex' = 'power';
```

### Multiplier is 0x (unexpected)
```typescript
// Check pick statuses
console.log(picks.map(p => p.status));

// Power Play: Any loss = 0x
// Flex Play: Too few wins = 0x
// Check payout tables for minimum wins required
```

### Push not being removed
```typescript
// Ensure status is exactly 'push' (case-sensitive)
{ status: 'push' } // ✅ Correct
{ status: 'Push' } // ❌ Wrong
{ status: 'PUSH' } // ❌ Wrong
```

---

## Performance Tips

- ✅ Use `useMemo` in React to prevent recalculations
- ✅ Calculations are O(n) - very fast even with many picks
- ✅ No async operations - instant results
- ✅ Type safety prevents runtime errors

---

## Support

- 📖 **Full Docs:** `PAYOUT_CALCULATOR.md`
- 🔧 **Integration Guide:** `PAYOUT_INTEGRATION_GUIDE.md`
- 📊 **Flow Diagram:** `PAYOUT_FLOW_DIAGRAM.md`
- 📝 **Summary:** `IMPLEMENTATION_SUMMARY.md`

---

## Example: Complete React Component

```tsx
import React, { useState, useMemo } from 'react';
import { calculatePayout, formatMultiplier, formatCurrency } from './services/payoutCalculator';

function QuickPayout() {
  const [picks, setPicks] = useState([]);
  const [playType, setPlayType] = useState<'power' | 'flex'>('power');
  const [entry, setEntry] = useState(10);

  const result = useMemo(() => {
    if (picks.length === 0) return null;
    return calculatePayout(picks, playType, entry);
  }, [picks, playType, entry]);

  if (!result) return <div>Select picks to see payout</div>;

  return (
    <div>
      <h2>{formatMultiplier(result.multiplier)}</h2>
      <p>Potential: {formatCurrency(result.payoutAmount)}</p>
      <p>{result.activePickCount} picks</p>
    </div>
  );
}
```

---

**That's it! You're ready to calculate payouts! 🎯**
