import React, { useState } from 'react'

interface PlayerProjections {
  points: number;
  rebounds: number;
  assists: number;
  threePointersMade: number;
  pointsPlusAssists: number;
  pointsPlusReboundsPlusAssists: number;
  fgMade: number;
  defensiveRebounds: number;
  fantasyScore: number;
  offensiveRebounds: number;
  reboundsPlusAssists: number;
  threePointersAttempted: number;
  pointsCombo: number;
  threePointersMadeCombo: number;
  assistsCombo: number;
  reboundsCombo: number;
  freeThrowsMade: number;
  fgAttempted: number;
  dunks: number;
  pointsPlusRebounds: number;
  blockedShots: number;
  steals: number;
  freeThrowsAttempted: number;
  personalFouls: number;
  blocksPlusSteals: number;
  turnovers: number;
  assistsFirst3Minutes: number;
  pointsFirst3Minutes: number;
  reboundsFirst3Minutes: number;
  quartersWith3PlusPoints: number;
  quartersWith5PlusPoints: number;
  twoPointersAttempted: number;
  twoPointersMade: number;
}

interface Player {
  id: string;
  name: string;
  image: string;
  team: string;
  teamAbbr: string;
  position: string[];
  gameLocation: string;
  opponent: string;
  opponentAbbr: string;
  gameDay: string;
  gameTime: string;
  gameDate: string;
  projections: PlayerProjections;
  isInjured: boolean;
  injuryStatus: string | null;
}

interface PlayerCardProps {
  player: Player;
  selectedCategory?: string;
}

const categoryMap: Record<string, { key: keyof PlayerProjections; label: string }> = {
  'Popular': { key: 'points', label: 'Points' },
  'Points': { key: 'points', label: 'Points' },
  'Rebounds': { key: 'rebounds', label: 'Rebounds' },
  '3-PT Made': { key: 'threePointersMade', label: '3-PT Made' },
  'Assists': { key: 'assists', label: 'Assists' },
  'Pts+Asts': { key: 'pointsPlusAssists', label: 'Pts+Asts' },
  'Pts+Rebs+Asts': { key: 'pointsPlusReboundsPlusAssists', label: 'Pts+Rebs+Asts' },
  'FG Made': { key: 'fgMade', label: 'FG Made' },
  'Defensive Rebounds': { key: 'defensiveRebounds', label: 'Def Rebounds' },
  'Fantasy Score': { key: 'fantasyScore', label: 'Fantasy Pts' },
  'Offensive Rebounds': { key: 'offensiveRebounds', label: 'Off Rebounds' },
  'Rebs+Asts': { key: 'reboundsPlusAssists', label: 'Rebs+Asts' },
  '3-PT Attempted': { key: 'threePointersAttempted', label: '3-PT Att' },
  'Points (Combo)': { key: 'pointsCombo', label: 'Points' },
  '3-PT Made (Combo)': { key: 'threePointersMadeCombo', label: '3-PT Made' },
  'Assists (Combo)': { key: 'assistsCombo', label: 'Assists' },
  'Rebounds (Combo)': { key: 'reboundsCombo', label: 'Rebounds' },
  'Free Throws Made': { key: 'freeThrowsMade', label: 'FT Made' },
  'FG Attempted': { key: 'fgAttempted', label: 'FG Att' },
  'Dunks': { key: 'dunks', label: 'Dunks' },
  'Pts+Rebs': { key: 'pointsPlusRebounds', label: 'Pts+Rebs' },
  'Blocked Shots': { key: 'blockedShots', label: 'Blocks' },
  'Steals': { key: 'steals', label: 'Steals' },
  'Free Throws Attempted': { key: 'freeThrowsAttempted', label: 'FT Att' },
  'Personal Fouls': { key: 'personalFouls', label: 'Fouls' },
  'Blks+Stls': { key: 'blocksPlusSteals', label: 'Blks+Stls' },
  'Turnovers': { key: 'turnovers', label: 'Turnovers' },
  'Assists - 1st 3 Minutes': { key: 'assistsFirst3Minutes', label: 'Asts 1st 3min' },
  'Points - 1st 3 Minutes': { key: 'pointsFirst3Minutes', label: 'Pts 1st 3min' },
  'Quarters with 3+ Points': { key: 'quartersWith3PlusPoints', label: 'Q w/ 3+ Pts' },
  'Rebounds - 1st 3 Minutes': { key: 'reboundsFirst3Minutes', label: 'Rebs 1st 3min' },
  'Quarters with 5+ Points': { key: 'quartersWith5PlusPoints', label: 'Q w/ 5+ Pts' },
  'Two Pointers Attempted': { key: 'twoPointersAttempted', label: '2-PT Att' },
  'Two Pointers Made': { key: 'twoPointersMade', label: '2-PT Made' },
};

const PlayerCardComponent: React.FC<PlayerCardProps> = ({ player, selectedCategory = 'Popular' }) => {
  const [selection, setSelection] = useState<'more' | 'less' | null>(null);

  const {
    name,
    teamAbbr,
    position,
    gameLocation,
    opponentAbbr,
    gameTime,
    projections,
  } = player;

  const category = categoryMap[selectedCategory] || categoryMap['Popular'];
  const statValue = projections[category.key] ?? projections.points ?? 0;

  const handleButtonClick = (type: 'more' | 'less') => {
    // If clicking the same button, deselect it
    if (selection === type) {
      setSelection(null);
    } else {
      // Otherwise, select the clicked button
      setSelection(type);
    }
  };

  return (
    <div className="bg-card-bg border border-card-border rounded-lg overflow-hidden hover:border-card-border-hover hover:shadow-card-shadow-hover transition-all duration-200 flex flex-col h-[250px] w-[250px] justify-center">
      {/* Main Content Area */}
        <div className="flex-1 flex flex-col items-center justify-center p-4 gap-1 overflow-hidden">
            {/* Icon */}
            <div className="w-2 h-2 rounded-full bg-accent1 shrink-0"></div>

            {/* Position */}
            <div className="text-xs font-semibold text-text-muted shrink-0">
                {position.join(', ')}
            </div>

            {/* Name, Game Info */}
            <div className="flex flex-row text-center shrink-0 max-w-full px-2 align-center justify-center">
                <div className="font-semibold text-text text-sm mb-1 truncate">{name}</div>
                <div className="text-xs text-text-muted leading-tight">
                    {teamAbbr} {gameLocation === 'home' ? 'vs' : '@'} {opponentAbbr}
                </div>
                <div className="text-xs text-text-muted">
                    {gameTime}
                </div>
            </div>

            {/* Stat Projection */}
            <div className="text-center shrink-0">
            <div className="text-4xl font-bold leading-none" style={{ color: 'var(--color-accent1)' }}>
                {statValue.toFixed(1)}
            </div>
            <div className="text-xs text-text-muted mt-1 leading-tight">{category.label}</div>
            </div>
        </div>

        {/* Bottom Buttons */}
        <div className="flex shrink-0">
            <button 
                onClick={() => handleButtonClick('less')}
                className={`selection-button selection-button-left ${selection === 'less' ? 'active' : ''}`}
            >
                Less
            </button>
            <button 
                onClick={() => handleButtonClick('more')}
                className={`selection-button ${selection === 'more' ? 'active' : ''}`}
            >
                More
            </button>
        </div>
    </div>
  )
}

// Helper component for stat items
const StatItem: React.FC<{ label: string; value: number }> = ({ label, value }) => (
  <div className="text-center p-2 rounded bg-surface-hover">
    <div className="text-xs text-text-muted mb-1">{label}</div>
    <div className="text-xl font-bold" style={{ color: 'var(--color-accent1)' }}>
      {value.toFixed(1)}
    </div>
  </div>
);

export default PlayerCardComponent
