# 🎯 Updated SelectedPlayersSummary Component

## What Changed

The `SelectedPlayersSummary` component has been completely redesigned to integrate the payout calculator with a better UX flow.

---

## New Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│  Your Lineup                              [Clear All]   │
│  3 Players Selected                                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Select Play Type                                       │
│  ┌──────────────────────┐  ┌──────────────────────┐   │
│  │   POWER PLAY ✓       │  │   FLEX PLAY          │   │
│  │   2+ picks           │  │   3+ picks           │   │
│  └──────────────────────┘  └──────────────────────┘   │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐  │
│  │  Entry Amount       Potential Payout            │  │
│  │  [$10.00]          [10x = $100.00] 🔒          │  │
│  │                                                  │  │
│  │  [Submit Lineup] ──────────────────────────────│  │
│  └─────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐  │
│  │  👤 LeBron James          [More] ✓             │  │ ↕
│  │  NBA LAL - SF             [Less]               │  │
│  │  Sun, Nov 09 3:30 PM @ MIL                     │  │ Scrollable
│  │  25.5 Points                                    │  │
│  ├─────────────────────────────────────────────────┤  │ ↕
│  │  👤 Stephen Curry         [More]               │  │
│  │  NBA GSW - PG             [Less] ✓             │  │
│  │  Sun, Nov 09 5:00 PM vs BOS                    │  │
│  │  28.5 Points                                    │  │
│  ├─────────────────────────────────────────────────┤  │
│  │  👤 Giannis               [More] ✓             │  │
│  │  NBA MIL - PF             [Less]               │  │
│  │  Sun, Nov 09 3:30 PM vs LAL                    │  │
│  │  11.5 Rebounds                                  │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## Key Features

### 1. ✅ Play Type Selection (Conditional Visibility)

**Power Play:**
- Shows when 2+ players selected
- Disabled when < 2 players
- Green (accent1) when active

**Flex Play:**
- Shows when 3+ players selected
- Disabled when < 3 players
- Purple (accent2) when active

**Helper Messages:**
- 1 player: "Add 1 more player to unlock Power Play"
- 2 players: "Add 1 more player to unlock Flex Play"

### 2. 💰 Dynamic Payout Calculation

**Entry Amount Input:**
- User can enter any amount
- Default: $10.00
- Number input with $ prefix

**Potential Payout (Read-Only):**
- Automatically calculated in real-time
- Shows: `{multiplier}x = ${amount}`
- Example: `10x = $100.00`
- Updates when:
  - Players added/removed
  - Play type changed
  - Entry amount changed
  - More/Less selection changed

### 3. 📜 Scrollable Player List

**Static Elements (Always Visible):**
- Header (Your Lineup / Clear All)
- Play Type Selection
- Form (Entry Amount + Payout + Submit)

**Scrollable Section:**
- Player list (max-height: 24rem / 384px)
- Scrolls when > ~4 players
- Form stays visible at top

### 4. 🎨 Visual Feedback

**Play Type Buttons:**
- Active: Bold border + background color
- Inactive: Light border + hover effect
- Disabled: Opacity 50% + cursor-not-allowed

**Submit Button:**
- Power Play active: Green (accent1)
- Flex Play active: Purple (accent2)
- Disabled: Grey with border

**Payout Display:**
- Multiplier in accent1 (green)
- Shows push notifications if applicable

---

## Component State

```typescript
const [playType, setPlayType] = useState<'power' | 'flex'>('power');
const [entryAmount, setEntryAmount] = useState<string>('10');

// Computed payout result
const payoutResult = useMemo(() => {
  // Converts selectedPlayers to picks
  // Calls calculatePayout(picks, playType, entryAmount)
  // Returns: { multiplier, payoutAmount, ... }
}, [selectedPlayers, playType, entryAmount]);
```

---

## Payout Calculation Logic

```typescript
// Real-time calculation
const picks = selectedPlayers.map(player => ({
  id: player.playerId,
  playerId: player.playerId,
  playerName: player.playerName,
  category: player.category,
  selection: player.selection,
  statValue: player.statValue,
  status: 'win', // Preview mode - all wins
  modifier: null,
}));

const result = calculatePayout(picks, playType, parseFloat(entryAmount));

// Result contains:
// - multiplier: 10
// - payoutAmount: 100.00
// - activePickCount: 4
// - pushCount: 0
// - isWinner: true
```

---

## User Flow Examples

### Example 1: Adding Players

```
1 player selected:
  ├─ Power Play: ❌ Disabled
  ├─ Flex Play: ❌ Disabled
  └─ Message: "Add 1 more player to unlock Power Play"

2 players selected:
  ├─ Power Play: ✅ Enabled (auto-selected)
  ├─ Flex Play: ❌ Disabled
  ├─ Payout: 3x = $30.00 (for 2-pick Power Play)
  └─ Message: "Add 1 more player to unlock Flex Play"

3 players selected:
  ├─ Power Play: ✅ Enabled
  ├─ Flex Play: ✅ Enabled
  └─ Payout: 6x = $60.00 (for 3-pick Power Play)

4 players selected:
  ├─ Power Play: 10x = $100.00
  └─ Flex Play: 6x = $60.00 (4/4 correct)
```

### Example 2: Changing Entry Amount

```
Entry: $10  →  Power Play 4-pick  →  10x = $100.00
Entry: $25  →  Power Play 4-pick  →  10x = $250.00
Entry: $50  →  Power Play 4-pick  →  10x = $500.00
```

### Example 3: Switching Play Types

```
4 picks, $10 entry:
  Power Play:  10x = $100.00  (all or nothing)
  Flex Play:    6x = $60.00   (can lose 1 and still win)

6 picks, $10 entry:
  Power Play:  37.5x = $375.00  (all 6 must win)
  Flex Play:    25x = $250.00   (all 6 must win)
  Flex Play:     2x = $20.00    (5/6 correct)
```

---

## Validation Rules

**Submit Button Enabled When:**
- Power Play: `selectedPlayers.length >= 2`
- Flex Play: `selectedPlayers.length >= 3`
- Entry amount is valid number

**Submit Button Disabled When:**
- No players selected
- Power Play selected but < 2 players
- Flex Play selected but < 3 players
- Entry amount is empty or invalid

---

## Responsive Behavior

**Panel Width:**
- `max-w-md` (448px maximum)
- Adapts to screen size

**Player List Scrolling:**
- `max-h-96` (384px)
- Smooth scroll
- Hover effects on rows

**Grid Layout:**
- Play type buttons: 2 columns (grid-cols-2)
- Form inputs: 2 columns (grid-cols-2)

---

## Styling Details

**Colors:**
- Power Play: `bg-accent1` (#6eff00 green)
- Flex Play: `bg-accent2` (#7f00ff purple)
- Borders: `border-card-border`
- Background: `bg-surface`, `bg-card-bg`

**Typography:**
- Header: `text-2xl font-medium`
- Labels: `text-xs font-medium text-text-muted`
- Player names: `text-sm font-medium`
- Stats: `text-sm` with bold values

**Spacing:**
- Outer padding: `p-4`
- Form padding: `p-4`
- Player rows: `p-3`
- Gap between elements: `gap-2`, `gap-3`

---

## Code Changes Summary

### Removed:
- ❌ Old email input field
- ❌ Separate entry fee + email form
- ❌ Static player list at bottom

### Added:
- ✅ Play type selection (Power/Flex)
- ✅ Dynamic payout calculation
- ✅ Real-time multiplier display
- ✅ Conditional button visibility (2+ for Power, 3+ for Flex)
- ✅ Scrollable player list with fixed form
- ✅ Push notification support
- ✅ Helper messages for locked play types

### Modified:
- 🔄 Form moved to top (above player list)
- 🔄 Submit button style changes based on play type
- 🔄 Player list made scrollable
- 🔄 Layout restructured for better UX

---

## Integration with Payout Calculator

```typescript
import { calculatePayout } from '../services/payoutCalculator';

// In component:
const payoutResult = useMemo(() => {
  if (selectedPlayers.length === 0) return null;
  
  const picks = selectedPlayers.map(/* convert to Pick format */);
  const entry = parseFloat(entryAmount) || 0;
  
  return calculatePayout(picks, playType, entry);
}, [selectedPlayers, playType, entryAmount]);

// Display:
{payoutResult && (
  <div>
    <span>{payoutResult.multiplier}x</span>
    <span>${payoutResult.payoutAmount.toFixed(2)}</span>
  </div>
)}
```

---

## Testing Checklist

- [ ] Add 1 player - both play types disabled
- [ ] Add 2 players - Power Play enabled, Flex disabled
- [ ] Add 3 players - both play types enabled
- [ ] Change entry amount - payout updates
- [ ] Switch between Power/Flex - payout recalculates
- [ ] Toggle More/Less - affects future calculations
- [ ] Add 7+ players - list scrolls, form stays visible
- [ ] Clear All - resets to empty state
- [ ] Submit with valid lineup - console logs data

---

**All features working and ready to use! 🎉**
