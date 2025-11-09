/**
 * API Service for FanAssist Backend
 * Connects frontend to FastAPI backend at localhost:8000
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface BackendPlayer {
  player_id: number;
  player_name: string;
  team: string;
  opponent: string;
  game_date: string;
  position?: string;
  season_averages: {
    points: number;
    rebounds: number;
    assists: number;
    steals: number;
    turnovers: number;
    threes_made: number;
    blocks: number;
    games_played: number;
  };
  prizepicks_lines: {
    points?: number;
    rebounds?: number;
    assists?: number;
    steals?: number;
    turnovers?: number;
    threes_made?: number;
    pra?: number;
    pr?: number;
    pa?: number;
  };
}

export interface DailyPropsResponse {
  date: string;
  count: number;
  players: BackendPlayer[];
}

export interface BetRequest {
  player_name: string;
  prop_type: string;
  line: number;
  pick: 'OVER' | 'UNDER';
  wager: number;
  bet_mode?: 'standard' | 'power_play';
  power_play_multiplier?: number;
}

export interface ParlayLeg {
  player_name: string;
  prop_type: string;
  line: number;
  pick: 'OVER' | 'UNDER';
}

export interface ParlayRequest {
  username: string;
  bets: ParlayLeg[];
  total_wager: number;
  bet_mode?: 'standard' | 'flex' | 'power_play';
  power_play_multiplier?: number;
}

export interface BetResult {
  bet_placed: boolean;
  result: {
    player_name: string;
    prop_type: string;
    line: number;
    pick: string;
    simulated_value: number;
    won: boolean;
    probability: number;
    season_average: number;
  };
  odds_info: {
    win_probability: number;
    odds_multiplier: number;
    bet_mode: string;
    power_play_multiplier?: number;
  };
  betting_summary: {
    username: string;
    old_balance: number;
    wager: number;
    payout: number;
    profit: number;
    new_balance: number;
    won: boolean;
  };
}

export interface BalanceResponse {
  username: string;
  balance: number;
  starting_balance: number;
  profit_loss: number;
}

/**
 * Fetch today's popular players with betting lines
 */
export async function getTodaysPlayers(): Promise<DailyPropsResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/daily-props/today`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching today\'s players:', error);
    throw error;
  }
}

/**
 * Fetch tomorrow's popular players with betting lines
 */
export async function getTomorrowsPlayers(): Promise<DailyPropsResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/daily-props/tomorrow`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching tomorrow\'s players:', error);
    throw error;
  }
}

/**
 * Place a single bet
 */
export async function placeBet(betData: BetRequest): Promise<BetResult> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/daily-props/place-bet`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(betData),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error placing bet:', error);
    throw error;
  }
}

/**
 * Place a parlay bet
 */
export async function placeParlay(parlayData: ParlayRequest): Promise<any> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/daily-props/place-parlay`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(parlayData),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error placing parlay:', error);
    throw error;
  }
}

/**
 * Get user balance
 */
export async function getBalance(username: string): Promise<BalanceResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/daily-props/balance/${username}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching balance:', error);
    throw error;
  }
}

/**
 * Reset user balance
 */
export async function resetBalance(username: string): Promise<any> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/daily-props/reset-balance/${username}`, {
      method: 'POST',
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error resetting balance:', error);
    throw error;
  }
}

/**
 * Get NBA player headshot image URL with multiple fallbacks
 */
function getPlayerImageUrl(playerId: number, _playerName: string): string {
  // Priority 1: NBA CDN - Official source
  // Format: Player ID with path
  // Source: Official NBA.com headshots
  const nbaCdnUrl = `https://cdn.nba.com/headshots/nba/latest/1040x760/${playerId}.png`;
  
  // Component will handle fallbacks in order:
  // 1. NBA CDN (official, most current players)
  // 2. UI Avatars (always works as final fallback)
  
  return nbaCdnUrl;
}

/**
 * Transform backend player data to frontend format
 */
export function transformBackendPlayer(backendPlayer: BackendPlayer, _index: number): any {
  const { player_id, player_name, team, opponent, game_date, season_averages, prizepicks_lines } = backendPlayer;
  
  // Debug: Log the actual player_id from backend
  console.log(`[Transform] ${player_name}: player_id from backend = ${player_id} (type: ${typeof player_id})`);
  
  return {
  id: player_id.toString(),
    name: player_name,
    image: getPlayerImageUrl(player_id, player_name),
    team: team,
    teamAbbr: team,
  // If backend provides a position string (e.g. "G", "G-F", "F-C"), split into parts for display
  position: backendPlayer.position ? backendPlayer.position.split(/[\-\/ ]+/).map((p: string) => p.trim()) : ['G'],
    gameLocation: 'home',
    opponent: opponent,
    opponentAbbr: opponent,
    gameDay: new Date(game_date).toLocaleDateString('en-US', { weekday: 'long' }),
    gameTime: '7:00 PM',
    gameDate: game_date,
    projections: {
      // Round everything to nearest 0.5 for consistent display
      points: Math.round((prizepicks_lines.points || season_averages.points) * 2) / 2,
      rebounds: Math.round((prizepicks_lines.rebounds || season_averages.rebounds) * 2) / 2,
      assists: Math.round((prizepicks_lines.assists || season_averages.assists) * 2) / 2,
      threePointersMade: Math.round((prizepicks_lines.threes_made || season_averages.threes_made) * 2) / 2,
      pointsPlusAssists: Math.round((prizepicks_lines.pa || (season_averages.points + season_averages.assists)) * 2) / 2,
      pointsPlusReboundsPlusAssists: Math.round((prizepicks_lines.pra || (season_averages.points + season_averages.rebounds + season_averages.assists)) * 2) / 2,
      fgMade: 0,
      defensiveRebounds: Math.round((season_averages.rebounds * 0.7) * 2) / 2,
      fantasyScore: Math.round((season_averages.points + season_averages.rebounds * 1.2 + season_averages.assists * 1.5) * 2) / 2,
      offensiveRebounds: Math.round((season_averages.rebounds * 0.3) * 2) / 2,
      reboundsPlusAssists: Math.round((season_averages.rebounds + season_averages.assists) * 2) / 2,
      threePointersAttempted: 0,
      pointsCombo: Math.round((prizepicks_lines.points || season_averages.points) * 2) / 2,
      threePointersMadeCombo: Math.round((prizepicks_lines.threes_made || season_averages.threes_made) * 2) / 2,
      assistsCombo: Math.round((prizepicks_lines.assists || season_averages.assists) * 2) / 2,
      reboundsCombo: Math.round((prizepicks_lines.rebounds || season_averages.rebounds) * 2) / 2,
      freeThrowsMade: 0,
      fgAttempted: 0,
      dunks: 0,
      pointsPlusRebounds: Math.round((prizepicks_lines.pr || (season_averages.points + season_averages.rebounds)) * 2) / 2,
      blockedShots: Math.round((season_averages.blocks) * 2) / 2,
      steals: Math.round((prizepicks_lines.steals || season_averages.steals) * 2) / 2,
      freeThrowsAttempted: 0,
      personalFouls: 0,
      blocksPlusSteals: Math.round((season_averages.blocks + season_averages.steals) * 2) / 2,
      turnovers: Math.round((prizepicks_lines.turnovers || season_averages.turnovers) * 2) / 2,
      assistsFirst3Minutes: 0,
      pointsFirst3Minutes: 0,
      reboundsFirst3Minutes: 0,
      quartersWith3PlusPoints: 0,
      quartersWith5PlusPoints: 0,
      twoPointersAttempted: 0,
      twoPointersMade: 0,
    },
    isInjured: false,
    injuryStatus: null,
  };
}
