# 🔄 Demons & Goblins - Toggle Model Implementation

## Summary of Changes

The Demons and Goblins feature has been redesigned with a **simplified toggle model** where each player has a fixed modifier type (demon OR goblin).

---

## Data Structure Changes

### Before (Multiple Options)
```json
"alternateProjections": {
  "points": { 
    "demon": 30.5, 
    "goblin": 23.5 
  }
}
```

### After (Single Toggle)
```json
"specialModifier": "demon",
"modifierMultiplier": 4.0
```

---

## UI Changes

### Toggle Button

**Single two-way button** with `↔️` (ArrowLeftRight) icon:

- **Inactive**: Shows "↔️ 😈 DEMON" or "↔️ 🤢 GOBLIN"
- **Active**: Shows "↔️ 😈 +4.0" or "↔️ 🤢 -3.0"

### Sample Players

1. **LeBron James** - Demon (+4.0 points)
2. **Stephen Curry** - Goblin (-3.0 points)  
3. **Giannis** - Demon (+5.5 points)

---

## Component Changes

### PlayerCardComponent.tsx

```typescript
// New state
const [modifierActive, setModifierActive] = useState<boolean>(false);

// New props from player data
specialModifier?: 'demon' | 'goblin'
modifierMultiplier?: number

// Simplified calculation
const statValue = modifierActive && modifierMultiplier !== undefined
  ? baseStatValue + modifierMultiplier
  : baseStatValue;

// Single toggle handler
const handleModifierToggle = () => {
  setModifierActive(!modifierActive);
  // Update lineup
};
```

---

## How It Works

1. **Load Player** - Check if `specialModifier` exists
2. **Show Toggle** - Display ↔️ button if modifier available
3. **Activate** - Click to add modifier value to projection
4. **Select** - Choose MORE (LESS disabled when active)
5. **Deactivate** - Click toggle again to return to normal
6. **Deselect** - Removing pick also clears modifier

---

## Key Features

✅ One button per player (not two)  
✅ Clear on/off state  
✅ Shows exact modifier value  
✅ LESS disabled when active  
✅ Visual feedback (colors, badges, borders)  
✅ Works with existing payout calculator  

---

## Testing

Try these scenarios:

1. **Toggle Demon** - LeBron: 26.5 → 30.5 points
2. **Toggle Goblin** - Curry: 30.5 → 27.5 points
3. **Select MORE** - Only option when modifier active
4. **Deselect** - Clears both selection and modifier
5. **Mixed Lineup** - Combine normal + demon + goblin picks

---

## Files Modified

1. `src/data/players.json` - Added specialModifier fields
2. `src/components/PlayerCardComponent.tsx` - Toggle button logic
3. `src/types/index.ts` - Updated SelectedPlayer interface
4. `src/services/payoutCalculator.ts` - Existing modifier support

---

This simpler model makes the feature easier to understand and use!
