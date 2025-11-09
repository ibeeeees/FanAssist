export interface SelectedPlayer {
  playerId: string;
  image: string;
  playerName: string;
  teamAbbr: string;
  position: string[];
  gameLocation: string;
  opponentAbbr: string;
  gameDay: string;
  gameTime: string;
  category: string;
  selection: 'more' | 'less';
  statValue: number;
  status?: 'win' | 'loss' | 'push'; // Payout calculation status
  modifier?: 'demon' | 'goblin' | null; // Special pick modifiers for enhanced payouts
  originalStatValue?: number; // Original stat value before demon/goblin modifier
}

export interface AlternateProjection {
  demon?: number; // Harder to win (higher line)
  goblin?: number; // Easier to win (lower line)
}
