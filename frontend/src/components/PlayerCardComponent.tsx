import React, { useState, useEffect } from 'react'
import { ArrowUp, ArrowDown, ArrowLeftRight } from 'lucide-react'
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
  const [modifierActive, setModifierActive] = useState<boolean>(false);

  // Sync selection state with selectedPlayers array
  useEffect(() => {
    const selectedPlayer = selectedPlayers.find(p => p.playerId === player.id);
    if (selectedPlayer) {
      setSelection(selectedPlayer.selection);
      setModifierActive(selectedPlayer.modifier === player.specialModifier);
    } else {
      setSelection(null);
      setModifierActive(false);
    }
  }, [selectedPlayers, player.id, player.specialModifier]);

  const {
    name,
    teamAbbr,
    position,
    gameLocation,
    opponentAbbr,
    gameTime,
    projections,
    specialModifier,
    modifierMultiplier,
  } = player;

  const category = categoryMap[selectedCategory] || categoryMap['Popular'];
  const baseStatValue = projections[category.key] ?? projections.points ?? 0;
  
  // Calculate modified stat value if modifier is active
  const statValue = modifierActive && modifierMultiplier !== undefined
    ? baseStatValue + modifierMultiplier
    : baseStatValue;
  
  // Check if this player has a special modifier available
  const hasSpecialModifier = specialModifier !== undefined && modifierMultiplier !== undefined;

  const handleModifierToggle = () => {
    // Toggle modifier on/off
    const newModifierActive = !modifierActive;
    setModifierActive(newModifierActive);
    
    // Update selectedPlayers if player is already selected
    if (selection) {
      const newStatValue = newModifierActive && modifierMultiplier !== undefined
        ? baseStatValue + modifierMultiplier
        : baseStatValue;
      
      setSelectedPlayers(prev => {
        const filtered = prev.filter(p => p.playerId !== player.id);
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
          selection: selection,
          statValue: newStatValue,
          originalStatValue: baseStatValue,
          modifier: newModifierActive ? specialModifier || null : null,
        }];
      });
    }
  };

  const handleButtonClick = (type: 'more' | 'less') => {
    // Modifier picks can only be "MORE"
    if (modifierActive && type === 'less') {
      return; // Don't allow "less" for modifier picks
    }
    
    // If clicking the same button, deselect it
    if (selection === type) {
      setSelection(null);
      setModifierActive(false); // Also clear modifier when deselecting
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
          statValue: statValue,
          originalStatValue: baseStatValue,
          modifier: modifierActive ? specialModifier || null : null,
        }];
      });
    }
  };

  return (
    <div className={`player-card ${selection ? 'active' : ''} ${modifierActive && specialModifier === 'demon' ? 'demon-active' : modifierActive && specialModifier === 'goblin' ? 'goblin-active' : ''}`}>
        {/* Main Content Area */}
        <div className="flex flex-col items-center justify-center p-1 overflow-hidden grow">

          {/* Icon */}
          <div className={`w-2 h-2 rounded-full shrink-0 mb-1 ${
            modifierActive && specialModifier === 'demon' 
              ? 'bg-red-600' 
              : modifierActive && specialModifier === 'goblin' 
              ? 'bg-green-600' 
              : 'bg-accent1'
          }`}></div>

          {/* Position */}
          <div className="text-xs font-semibold text-text-muted shrink-0">
              {position.join(' - ')}
          </div>

          {/* Name */}
          <div className="font-light text-lg">{name}</div>

          {/* Game Info */}
          <div className="flex flex-col text-center shrink-0 w-full align-center justify-center">
              <div className="text-xs text-text-muted leading-tight">
                  {teamAbbr} {gameLocation === 'home' ? 'vs' : '@'} {opponentAbbr}
              </div>
              <div className="text-xs text-text-muted">
                  {gameTime}
              </div>
          </div>

          {/* Stat Projection */}
          <div className="flex flex-row items-baseline text-center shrink-0 gap-0.5">

              {/* Special Modifier Toggle Button */}
              {hasSpecialModifier && (
                <button
                  onClick={handleModifierToggle}
                  className={`flex items-center gap-1 text-[9px] p-0.5 mt-1 rounded-full font-bold transition-all ${
                    modifierActive
                      ? specialModifier === 'demon'
                        ? 'bg-red-600 text-white shadow-sm border border-red-600'
                        : 'bg-green-600 text-white shadow-sm border border-green-600'
                      : specialModifier === 'demon'
                      ? 'bg-card-bg text-text-muted border border-card-border hover:bg-red-600/10 hover:border-red-600 hover:text-red-600'
                      : 'bg-card-bg text-text-muted border border-card-border hover:bg-green-600/10 hover:border-green-600 hover:text-green-600'
                  }`}
                  title={`Toggle ${specialModifier?.toUpperCase()}: ${modifierMultiplier && modifierMultiplier > 0 ? '+' : ''}${modifierMultiplier?.toFixed(1)} ${modifierActive ? '(Active)' : '(Inactive)'}`}
                >
                  <ArrowLeftRight size={12} />
                </button>
              )}
              <div className={`text-2xl font-normal ${
                modifierActive && specialModifier === 'demon' 
                  ? 'text-red-500' 
                  : modifierActive && specialModifier === 'goblin' 
                  ? 'text-green-500' 
                  : ''
              }`}>
                  {statValue.toFixed(1)}
              </div>
              <div className="text-xs text-text-muted">{category.label}</div>
          </div>
        </div>

        {/* Bottom Buttons */}
        <div className="flex mt-auto">
          <button 
            onClick={() => handleButtonClick('less')}
            disabled={modifierActive}
            className={`selection-button selection-button-left ${selection === 'less' ? 'active' : ''} ${
              modifierActive ? 'opacity-40 cursor-not-allowed' : ''
            }`}
          >
            <ArrowDown size={16} className="inline-block mr-[5px]" /> Less
          </button>
          <button 
            onClick={() => handleButtonClick('more')}
            className={`selection-button ${
              selection === 'more' && modifierActive && specialModifier === 'demon'
                ? 'bg-red-600 text-white border-red-600'
                : selection === 'more' && modifierActive && specialModifier === 'goblin'
                ? 'bg-green-600 text-white border-green-600'
                : selection === 'more'
                ? 'active'
                : ''
            }`}
            style={
              selection === 'more' && modifierActive
                ? specialModifier === 'demon'
                  ? { backgroundColor: 'rgb(220, 38, 38)', color: 'white' }
                  : { backgroundColor: 'rgb(22, 163, 74)', color: 'white' }
                : undefined
            }
          >
            <ArrowUp size={16} className="inline-block mr-[5px]" /> More
          </button>
        </div>
    </div>
  )
}


export default PlayerCardComponent
