import React, { useState, useEffect } from 'react'
import { ArrowUp, ArrowDown } from 'lucide-react'
import type { SelectedPlayer } from '../types'

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
  specialModifier?: 'demon' | 'goblin'; // Fixed modifier type (either demon OR goblin)
  modifierMultiplier?: number; // How much to add/subtract from projections
  isInjured: boolean;
  injuryStatus: string | null;
}

interface PlayerCardProps {
  player: Player;
  selectedCategory?: string;
  selectedPlayers: SelectedPlayer[];
  setSelectedPlayers: React.Dispatch<React.SetStateAction<SelectedPlayer[]>>;
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

const PlayerCardComponent: React.FC<PlayerCardProps> = ({ player, selectedCategory = 'Popular', selectedPlayers, setSelectedPlayers }) => {
  const [selection, setSelection] = useState<'more' | 'less' | null>(null);
  const [imageAttempt, setImageAttempt] = useState(0);

  // Sync selection state with selectedPlayers array
  useEffect(() => {
    const selectedPlayer = selectedPlayers.find(p => p.playerId === player.id);
    if (selectedPlayer) {
      setSelection(selectedPlayer.selection);
    } else {
      setSelection(null);
    }
  }, [selectedPlayers, player.id]);

  // Get image URL with fallbacks
  const getImageUrl = () => {
    let url = '';
    if (imageAttempt === 0) {
      // Special cases mapping for players with non-standard names
      const specialCases: { [key: string]: string } = {
        'Luka Doncic': 'doncilu01',
        'Luka Dončić': 'doncilu01',
        'Nikola Jokic': 'jokicni01',
        'Nikola Jokić': 'jokicni01',
        'Anthony Davis': 'davisan02',
        'Giannis Antetokounmpo': 'antetgi01',
        'Nikola Vucevic': 'vucevni01',
        'Nikola Vučević': 'vucevni01',
        'Bogdan Bogdanovic': 'bogdabo01',
        'Bogdan Bogdanović': 'bogdabo01',
        'Bojan Bogdanovic': 'bogdabo02',
        'Bojan Bogdanović': 'bogdabo02',
        'Jaylen Brown': 'brownja02',  // Using 02 for correct Jaylen Brown (Celtics)
      };

      // Check if player has a special case mapping
      let bbrefCode = specialCases[player.name];
      
      if (!bbrefCode) {
        // Generate code algorithmically
        const nameParts = player.name.split(' ');
        const firstName = nameParts[0]?.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '') || '';
        const lastName = nameParts[nameParts.length - 1]?.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z]/g, '') || '';
        
        const lastPart = lastName.substring(0, 5).padEnd(5, lastName[0] || 'x');
        const firstPart = firstName.substring(0, 2);
        bbrefCode = `${lastPart}${firstPart}01`;
      }
      
      url = `https://www.basketball-reference.com/req/202106291/images/headshots/${bbrefCode}.jpg`;
    } else if (imageAttempt === 1) {
      // Secondary: Try NBA CDN
      url = `https://cdn.nba.com/headshots/nba/latest/1040x760/${player.id}.png`;
    } else {
      // Final fallback to UI Avatars
      url = `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&size=100&background=10b981&color=fff&bold=true&rounded=true`;
    }
    
    console.log(`[${player.name}] Attempt ${imageAttempt}: ${url}`);
    return url;
  };

  const handleImageError = () => {
    console.log(`[${player.name}] Image failed at attempt ${imageAttempt}`);
    if (imageAttempt < 2) {
      setImageAttempt(prev => prev + 1);
    }
  };

  const {
    name,
    teamAbbr,
    position,
    gameLocation,
    opponentAbbr,
    gameTime,
    gameDay,
    projections,
  } = player;

  const category = categoryMap[selectedCategory] || categoryMap['Popular'];
  const statValue = projections[category.key] ?? projections.points ?? 0;
  // Round to nearest 0.5 for display
  const roundToHalf = (v: number) => Math.round(v * 2) / 2;
  const baseStatValue = roundToHalf(statValue);
  
  // Simple stat display - no modifiers
  const displayStatValue = baseStatValue;

  const handleButtonClick = (type: 'more' | 'less') => {
    // If clicking the same button, deselect it
    if (selection === type) {
      setSelection(null);
      // Remove player from selectedPlayers
      setSelectedPlayers(prev => prev.filter(p => p.playerId !== player.id));
    } else {
      // Otherwise, select the clicked button
      setSelection(type);
      // Add or update player in selectedPlayers
      setSelectedPlayers(prev => {
        // Remove existing entry if it exists
        const filtered = prev.filter(p => p.playerId !== player.id);
        // Add new entry
        return [...filtered, {
          playerId: player.id,
          image: player.image,
          playerName: name,
          teamAbbr: player.teamAbbr,
          position: player.position,
          gameLocation: player.gameLocation,
          opponentAbbr: player.opponentAbbr,
          gameDay: player.gameDay,
          gameTime: player.gameTime,
          category: selectedCategory,
          selection: type,
          statValue: displayStatValue,
          originalStatValue: baseStatValue
        }];
      });
    }
  };

  return (
    <>
      <div className={`player-card ${selection ? 'active' : ''}`}>
        {/* Main Content Area */}
        <div className="flex flex-col items-center justify-center p-1.5 overflow-hidden grow">
            {/* Player Photo */}
            <div 
              className="w-5 h-5 rounded-full overflow-hidden bg-accent1/20 shrink-0 mb-1 flex items-center justify-center border border-accent1/40"
            >
              <img 
                src={getImageUrl()}
                alt={player.name}
                onError={handleImageError}
                className="w-full h-full object-cover"
                loading="lazy"
              />
            </div>

            {/* Position */}
            <div className="text-[9px] font-semibold text-text-muted shrink-0 mb-0.5">
                {position && position.length > 0 ? position.join(' - ') : '—'}
            </div>

            {/* Name - Compact */}
            <div className="font-light text-sm leading-tight mb-0.5 text-center px-1">{name}</div>

            {/* Game Info - Condensed */}
            <div className="flex flex-col text-center shrink-0 w-full items-center justify-center mb-0.5">
                <div className="text-[10px] text-text-muted leading-tight">
                    {teamAbbr || 'TBD'} {gameLocation === 'home' ? 'vs' : '@'} {opponentAbbr || 'TBD'}
                </div>
                <div className="text-[10px] text-text-muted leading-tight">
                    {gameDay || 'Today'} • {gameTime || 'TBD'}
                </div>
            </div>

            {/* Stat Projection - Compact */}
            <div className="flex flex-row items-baseline text-center shrink-0 gap-1">
                <div className="text-xl font-normal">
                  {displayStatValue.toFixed(1)}
                </div>
                <div className="text-[10px] text-text-muted">{category.label}</div>
            </div>
        </div>

        {/* Bottom Buttons */}
        <div className="flex mt-auto">
          <button 
            onClick={() => handleButtonClick('less')}
            className={`selection-button selection-button-left ${selection === 'less' ? 'active' : ''}`}
          >
            <ArrowDown size={16} className="inline-block mr-[5px]" /> Less
          </button>
          <button 
            onClick={() => handleButtonClick('more')}
            className={`selection-button ${selection === 'more' ? 'active' : ''}`}
          >
            <ArrowUp size={16} className="inline-block mr-[5px]" /> More
          </button>
        </div>
      </div>
    </>
  )
}


export default PlayerCardComponent
