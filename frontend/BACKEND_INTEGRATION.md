# FanAssist Frontend - Backend Integration

This frontend is now fully integrated with the FastAPI backend for real-time NBA player data and betting functionality.

## Features

### 🎯 Live Data Integration
- **Real-time player data** from backend API
- **Auto-refresh** every 5 minutes
- **Manual refresh** button for instant updates
- **Fallback to static data** if backend is unavailable
- **Toggle between live and static data**

### 💰 Paper Money Betting
- **Place parlays** with 2-6 legs
- **Real-time balance tracking** ($10,000 starting balance)
- **Bet simulation** using actual NBA stats
- **Instant results** with win/loss notification
- **Balance reset** functionality

### 📊 Supported Prop Types
- Points
- Rebounds
- Assists
- 3-PT Made
- Steals
- Turnovers
- Points + Assists (PA)
- Points + Rebounds + Assists (PRA)
- Points + Rebounds (PR)
- Blocks

## Setup Instructions

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Environment Configuration
The `.env` file is already configured:
```
VITE_API_URL=http://localhost:8000
VITE_DEFAULT_USERNAME=demo_user
```

### 3. Start Backend Server
Make sure your backend is running on port 8000:
```bash
cd backend
source ../.venv/bin/activate  # Activate virtual environment
python run.py
```

### 4. Start Frontend Development Server
```bash
cd frontend
npm run dev
```

Frontend will be available at: **http://localhost:5173**

## How It Works

### Data Flow
```
Frontend (React) ←→ API Service (api.ts) ←→ Backend (FastAPI:8000)
                          ↓
                  Transform Data
                          ↓
                  Display in UI
```

### Key Files

#### API Integration
- **`src/services/api.ts`** - All backend API calls
- **`src/hooks/useBetting.ts`** - Custom hook for betting operations
- **`.env`** - Environment configuration

#### Components
- **`src/App.tsx`** - Main app with live data fetching
- **`src/components/BettingPanel.tsx`** - Betting interface
- **`src/components/PlayerCardComponent.tsx`** - Player cards
- **`src/components/SelectedPlayersSummary.tsx`** - Selected players + betting

### API Endpoints Used

#### Get Today's Players
```typescript
GET /api/daily-props/today
Returns: { date, count, players[] }
```

#### Place Parlay Bet
```typescript
POST /api/daily-props/place-parlay
Body: {
  username: string,
  bets: [{ player_name, prop_type, line, pick }],
  total_wager: number,
  bet_mode: 'standard' | 'flex' | 'power_play'
}
```

#### Get Balance
```typescript
GET /api/daily-props/balance/{username}
Returns: { username, balance, profit_loss }
```

## Usage

### Viewing Live Player Data
1. Click the **"🟢 Live"** button in the header (green = live data)
2. Click **"Refresh"** to manually update player data
3. Toggle to **"⚫ Static"** to use cached data

### Placing a Bet
1. **Select players** by clicking on their cards
2. Choose **"More"** (OVER) or **"Less"** (UNDER) for each player
3. **Open the sidebar** (Activity icon) if not already open
4. **Enter wager amount** in the betting panel
5. Click **"Place Parlay"** button
6. **View results** instantly with updated balance

### Example Parlay
```
Player 1: LeBron James - Points OVER 25.5
Player 2: Stephen Curry - Assists OVER 6.5
Player 3: Giannis - PRA OVER 43.0
Total Wager: $50
```

## Features in Detail

### Live Data Toggle
- **Green "Live"** = Using backend API
- **Gray "Static"** = Using local JSON file
- Automatically falls back to static if API fails

### Auto-Refresh
- Fetches new data every 5 minutes
- Shows last update time in header
- Manual refresh available anytime

### Error Handling
- **Yellow warning banner** for API errors
- **Fallback to static data** on failure
- **Retry logic** in API service

### Betting Panel
- **Balance display** with refresh button
- **Wager input** with validation
- **Parlay validation** (2-6 legs)
- **Real-time results** with 5-second display
- **Auto-clear** selections after bet

## Development

### Adding New Prop Types
1. Update `propTypeMap` in `BettingPanel.tsx`
2. Add to backend prop type support
3. Update `PlayerProjections` interface

### Customizing API URL
Update `.env` file:
```
VITE_API_URL=https://your-production-api.com
```

### Debugging
```bash
# Check API connectivity
curl http://localhost:8000/api/daily-props/today

# View console logs
Open browser DevTools → Console

# Check network requests
Open browser DevTools → Network tab
```

## Common Issues

### "Failed to load live data"
- **Check backend is running**: `curl http://localhost:8000/health`
- **Check CORS settings**: Should allow `localhost:5173`
- **Check firewall**: Both ports 8000 and 5173 should be accessible

### "Insufficient balance"
- **Check current balance**: Click refresh icon in betting panel
- **Reset balance**: Click "Reset Balance" button

### Players not updating
- **Manual refresh**: Click "Refresh" button
- **Check backend logs**: `tail -f backend/server.log`
- **Toggle live mode**: Turn off and on again

## Production Deployment

### Build for Production
```bash
npm run build
```

### Update API URL
```bash
# In .env
VITE_API_URL=https://your-api-domain.com
```

### Serve Built Files
```bash
npm run preview
# Or deploy dist/ folder to hosting service
```

## Tech Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **Motion** - Animations

## Support

For issues or questions:
1. Check browser console for errors
2. Verify backend is running and accessible
3. Check network tab for failed requests
4. Review backend logs for API errors

---

**Made with ❤️ by FanAssist Team**
