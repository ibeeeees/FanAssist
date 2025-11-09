# Player Photo and Layout Fixes

## Issues Fixed

### 1. 🖼️ Better Player Headshot API
**Problem**: NBA.com CDN images weren't loading reliably for all players.

**Solution**: Implemented multi-source image fallback system:
1. **Primary**: GitHub repo `GreenGuitar0/nba-players` (RealGM scraped images)
   - Format: `https://raw.githubusercontent.com/GreenGuitar0/nba-players/main/player_images/{lastname}-{firstname}.jpg`
   - Example: `antetokounmpo-giannis.jpg`
   - Best quality and most reliable

2. **Secondary**: NBA.com CDN
   - Format: `https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png`
   - Falls back if GitHub image not found

3. **Tertiary**: UI Avatars (always works)
   - Format: `https://ui-avatars.com/api/?name={name}&size=80&background=10b981&color=fff&bold=true`
   - Generates nice circular avatars with player initials

**Files Modified**:
- `frontend/src/services/api.ts` - Updated `getPlayerImageUrl()` function
- `frontend/src/components/PlayerCardComponent.tsx` - Added fallback chain logic

---

### 2. 📅 Restored Game Info Display
**Problem**: Large player photos (64x64px) were hiding the game day and time information.

**Solution**:
- Reduced photo size from 64px to 48px (w-16 → w-12)
- Added proper spacing and line height
- Restored gameDay display
- All info now visible:
  - Player photo (circular, 48x48px)
  - Position
  - Player name
  - Team vs Opponent
  - **Game Day** ✅
  - **Game Time** ✅

**Before**:
```
┌─────────────────┐
│  ╔═══════╗      │
│  ║ 📸    ║      │ ← Too big (64px)
│  ║PHOTO  ║      │
│  ╚═══════╝      │
│   G - F         │
│ Giannis A.      │
│ MIL vs BOS      │
│   (no day/time) │ ← Hidden!
└─────────────────┘
```

**After**:
```
┌─────────────────┐
│   ╔═════╗       │
│   ║ 📸  ║       │ ← Perfect size (48px)
│   ╚═════╝       │
│   G - F         │
│ Giannis A.      │
│ MIL vs BOS      │
│ Saturday        │ ← Visible!
│ 7:00 PM         │ ← Visible!
└─────────────────┘
```

---

## Technical Implementation

### Image Fallback Chain

```typescript
const getImageUrl = () => {
  const nameParts = player.name.split(' ');
  const firstName = nameParts[0]?.toLowerCase() || '';
  const lastName = nameParts[nameParts.length - 1]?.toLowerCase() || '';
  
  if (imageAttempt === 0) {
    // Attempt 1: GitHub repo (best quality)
    return `https://raw.githubusercontent.com/.../${lastName}-${firstName}.jpg`;
  } else if (imageAttempt === 1) {
    // Attempt 2: NBA CDN
    return `https://cdn.nba.com/headshots/nba/...//${player.id}.png`;
  } else {
    // Attempt 3: UI Avatars (always works)
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}...`;
  }
};

const handleImageError = () => {
  if (imageAttempt < 2) {
    setImageAttempt(prev => prev + 1); // Try next source
  } else {
    setImageError(true); // All attempts exhausted
  }
};
```

### Layout Adjustments

```tsx
{/* Player Photo - Optimized Size */}
<div className="w-12 h-12 rounded-full overflow-hidden bg-accent1/20 shrink-0 mb-1.5 flex items-center justify-center border-2 border-accent1/30">
  <img 
    src={getImageUrl()}
    alt={player.name}
    onError={handleImageError}
    className="w-full h-full object-cover"
  />
</div>

{/* Name - Better Line Height */}
<div className="font-light text-lg leading-tight">{name}</div>

{/* Game Info - Properly Spaced */}
<div className="flex flex-col text-center shrink-0 w-full align-center justify-center mt-1">
  <div className="text-xs text-text-muted leading-tight">
    {teamAbbr} {gameLocation === 'home' ? 'vs' : '@'} {opponentAbbr}
  </div>
  <div className="text-xs text-text-muted leading-tight">
    {gameDay} {/* ← Now visible! */}
  </div>
  <div className="text-xs text-text-muted leading-tight">
    {gameTime} {/* ← Now visible! */}
  </div>
</div>
```

---

## Examples

### Player Name Parsing
```
"Giannis Antetokounmpo" → lastName="antetokounmpo", firstName="giannis"
"LeBron James"          → lastName="james", firstName="lebron"
"Luka Doncic"           → lastName="doncic", firstName="luka"
```

### Image URLs Generated
```
1. https://raw.githubusercontent.com/GreenGuitar0/nba-players/main/player_images/antetokounmpo-giannis.jpg
   ↓ (if 404)
2. https://cdn.nba.com/headshots/nba/latest/1040x760/203507.png
   ↓ (if 404)
3. https://ui-avatars.com/api/?name=Giannis%20Antetokounmpo&size=80&background=10b981&color=fff&bold=true
```

---

## Benefits

### 1. Better Image Quality
- RealGM images from GitHub repo are high quality
- More players covered than NBA.com CDN
- Always have a fallback that works

### 2. Improved Layout
- All game information visible
- Better visual hierarchy
- Consistent spacing
- Professional appearance

### 3. Better Performance
- Images try fastest sources first
- Graceful degradation
- No broken image icons
- Smooth user experience

---

## Testing

### Manual Test Cases
- [x] Player with GitHub image available (e.g., Giannis)
- [x] Player with only NBA CDN image
- [x] Player with no photos (falls back to initials)
- [x] Game day displays correctly
- [x] Game time displays correctly
- [x] Opponent info displays correctly
- [x] All layouts responsive on mobile

### Edge Cases Handled
- Names with spaces (e.g., "LeBron James")
- Names with special characters (e.g., "Luka Dončić")
- Players without photos in any source
- Network errors during image loading

---

## Files Changed

### `frontend/src/services/api.ts`
- Updated `getPlayerImageUrl()` function
- Added GitHub repo as primary source
- Better name parsing (firstname/lastname)

### `frontend/src/components/PlayerCardComponent.tsx`
- Reduced photo size (64px → 48px)
- Added `imageAttempt` state for fallback chain
- Added `getImageUrl()` function
- Added `handleImageError()` function
- Restored `gameDay` in destructured props
- Improved layout spacing

---

## Known Limitations

1. **GitHub Repo Coverage**: Not all NBA players may be in the GitHub repo
   - Mitigation: Automatic fallback to NBA CDN → UI Avatars

2. **Name Parsing**: Complex names might not match exactly
   - Example: "Dennis Schröder" vs "schroder-dennis"
   - Mitigation: Multiple fallbacks ensure image always loads

3. **Image Caching**: Each fallback attempt triggers new request
   - Future: Could implement client-side cache of successful URLs

---

## Future Enhancements

1. **Image Preloading**: Preload images in background for faster display
2. **Local Cache**: Cache successful image URLs in localStorage
3. **WebP Support**: Use modern image formats for better performance
4. **Lazy Loading**: Only load images for visible cards

---

**Last Updated**: November 9, 2025  
**Version**: 2.1  
**Status**: ✅ Both issues fixed and tested
