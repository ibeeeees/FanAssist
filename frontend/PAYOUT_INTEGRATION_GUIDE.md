# 🎯 Integrating Payout Calculator into SelectedPlayersSummary

## Quick Integration Guide

This guide shows how to add the payout calculator to your existing `SelectedPlayersSummary` component.

---

## Step 1: Update State

Add state for play type and entry amount:

```typescript
// In SelectedPlayersSummary.tsx

const [playType, setPlayType] = useState<'power' | 'flex'>('power');
const [entryAmount, setEntryAmount] = useState<number>(10);
```

---

## Step 2: Add Play Type Selector

Add a toggle between Power Play and Flex Play:

```tsx
{/* Play Type Selector */}
<div className="flex gap-2 mb-3">
  <button
    type="button"
    onClick={() => setPlayType('power')}
    className={`flex-1 px-3 py-2 rounded text-sm font-medium transition-colors ${
      playType === 'power'
        ? 'bg-accent1 text-black'
        : 'bg-surface border border-card-border text-text-primary hover:border-accent1'
    }`}
  >
    Power Play
  </button>
  <button
    type="button"
    onClick={() => setPlayType('flex')}
    className={`flex-1 px-3 py-2 rounded text-sm font-medium transition-colors ${
      playType === 'flex'
        ? 'bg-accent2 text-white'
        : 'bg-surface border border-card-border text-text-primary hover:border-accent2'
    }`}
  >
    Flex Play
  </button>
</div>
```

---

## Step 3: Import Payout Calculator

```typescript
import {
  calculatePayout,
  formatMultiplier,
  formatCurrency,
  getPayoutDescription,
} from '../services/payoutCalculator';
```

---

## Step 4: Calculate Payout

Add a useMemo hook to calculate the payout:

```typescript
const payoutResult = useMemo(() => {
  if (selectedPlayers.length === 0) {
    return null;
  }

  // Convert SelectedPlayer to Pick format
  const picks = selectedPlayers.map(player => ({
    id: player.playerId,
    playerId: player.playerId,
    playerName: player.playerName,
    category: player.category,
    selection: player.selection,
    statValue: player.statValue,
    status: player.status || 'win', // Default to 'win' for preview
    modifier: player.modifier || null,
  }));

  try {
    return calculatePayout(picks, playType, entryAmount);
  } catch (error) {
    console.error('Payout calculation error:', error);
    return null;
  }
}, [selectedPlayers, playType, entryAmount]);
```

---

## Step 5: Display Payout Information

Add the payout display to your component:

```tsx
{/* Payout Display */}
{payoutResult && (
  <div className="payout-section border-t border-card-border pt-3 mb-3">
    {/* Multiplier */}
    <div className="flex items-baseline justify-between mb-2">
      <span className="text-sm text-text-muted">Potential Payout</span>
      <div className="flex items-baseline gap-2">
        <span className="text-3xl font-bold text-accent1">
          {formatMultiplier(payoutResult.multiplier)}
        </span>
        <span className="text-lg text-text-primary">
          = {formatCurrency(payoutResult.payoutAmount)}
        </span>
      </div>
    </div>

    {/* Pick Count Info */}
    <div className="text-xs text-text-muted">
      {payoutResult.activePickCount} pick{payoutResult.activePickCount !== 1 ? 's' : ''}
      {payoutResult.pushCount > 0 && (
        <span className="text-accent2">
          {' '}({payoutResult.originalPickCount} - {payoutResult.pushCount} push
          {payoutResult.pushCount !== 1 ? 'es' : ''})
        </span>
      )}
    </div>

    {/* Description */}
    {payoutResult.pushCount > 0 && (
      <div className="mt-2 text-xs text-accent2 bg-surface p-2 rounded">
        💡 {getPayoutDescription(payoutResult)}
      </div>
    )}
  </div>
)}
```

---

## Step 6: Update Form Submission

Update the submit handler to include play type and payout info:

```typescript
const handleSubmit = (e: React.FormEvent) => {
  e.preventDefault();

  if (selectedPlayers.length === 0) {
    return;
  }

  // Submit lineup with payout info
  const lineupData = {
    players: selectedPlayers,
    playType: playType,
    entryFee: parseFloat(formData.entryFee) || 0,
    email: formData.email,
    potentialPayout: payoutResult?.payoutAmount || 0,
    multiplier: payoutResult?.multiplier || 0,
  };

  console.log('Submitting lineup:', lineupData);

  // TODO: Send to backend API
  // fetch('/api/submit-lineup', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify(lineupData),
  // });
};
```

---

## Full Component Structure

Here's how the complete component should be structured:

```tsx
function SelectedPlayersSummary({ selectedPlayers, setSelectedPlayers }) {
  // State
  const [isOpen, setIsOpen] = useState(false);
  const [hasManuallyClosedWithPlayers, setHasManuallyClosedWithPlayers] = useState(false);
  const [playType, setPlayType] = useState<'power' | 'flex'>('power');
  const [formData, setFormData] = useState({ entryFee: '', email: '' });

  // Calculate payout
  const payoutResult = useMemo(() => { /* ... */ }, [selectedPlayers, playType, formData.entryFee]);

  // Handlers
  const handleToggle = () => { /* ... */ };
  const handleSubmit = (e) => { /* ... */ };

  return (
    <>
      {/* Toggle Button */}
      
      {/* Summary Panel */}
      <div className={`summary-panel ${isOpen ? 'open' : ''}`}>
        {/* Header */}
        
        {/* Play Type Selector */}
        
        {/* Payout Display */}
        
        {/* Player List */}
        
        {/* Form */}
      </div>
    </>
  );
}
```

---

## Visual Layout

```
┌─────────────────────────────────────────┐
│  Selected Players (3)             [X]   │
├─────────────────────────────────────────┤
│  [Power Play]  [Flex Play]              │  ← Play Type Selector
├─────────────────────────────────────────┤
│  Potential Payout        37.5x = $37.50 │  ← Payout Display
│  3 picks                                │
├─────────────────────────────────────────┤
│  Player 1...                            │  ← Player List
│  Player 2...                            │
│  Player 3...                            │
├─────────────────────────────────────────┤
│  [Clear All]                            │
├─────────────────────────────────────────┤
│  Entry Fee:  [$10.00]                   │  ← Form
│  Email:      [user@email.com]           │
│  [Submit Lineup]                        │
└─────────────────────────────────────────┘
```

---

## Styling Tips

### Power Play vs Flex Play Colors

```css
/* Power Play - Accent1 (Green) */
.power-play-active {
  background-color: var(--accent1);
  color: #000;
}

/* Flex Play - Accent2 (Purple) */
.flex-play-active {
  background-color: var(--accent2);
  color: #fff;
}

/* Payout Multiplier */
.payout-multiplier {
  color: var(--accent1);
  font-size: 2rem;
  font-weight: 700;
}
```

---

## Testing Checklist

- [ ] Switch between Power Play and Flex Play
- [ ] Verify payout changes based on number of picks
- [ ] Test with 2, 3, 4, 5, 6 picks
- [ ] Verify multiplier displays correctly
- [ ] Check that entry fee affects payout amount
- [ ] Ensure form submission includes payout data
- [ ] Test edge cases (0 picks, invalid entry amount)

---

## Next Steps

1. **Backend Integration**: Create API endpoint to receive lineup submissions
2. **Result Tracking**: Store picks with actual results (win/loss/push)
3. **Payout Calculation**: Calculate actual payouts after games complete
4. **User Balance**: Track user winnings and losses
5. **History**: Show user's previous lineups and results

---

## Example API Endpoint

```typescript
// backend/routes/lineups.py

@app.route('/api/submit-lineup', methods=['POST'])
def submit_lineup():
    data = request.json
    
    lineup = {
        'user_email': data['email'],
        'play_type': data['playType'],
        'entry_fee': data['entryFee'],
        'picks': data['players'],
        'potential_payout': data['potentialPayout'],
        'status': 'pending',
        'created_at': datetime.now()
    }
    
    # Save to database
    db.lineups.insert_one(lineup)
    
    return jsonify({
        'success': True,
        'lineup_id': str(lineup['_id'])
    })
```

---

**Need help?** Refer to `PAYOUT_CALCULATOR.md` for detailed API documentation.
