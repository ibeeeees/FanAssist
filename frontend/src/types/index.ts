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
  modifier?: 'demon' | 'goblin' | null; // Future: special pick modifiers
}
