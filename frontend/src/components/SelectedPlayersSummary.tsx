import React, { useState, useEffect, useMemo } from 'react'
import { Activity, CircleSlash } from 'lucide-react'
import type { SelectedPlayer } from '../types'
import { calculatePayout } from '../services/payoutCalculator'
import { BettingPanel } from './BettingPanel'

interface SelectedPlayersSummaryProps {
  selectedPlayers: SelectedPlayer[];
  setSelectedPlayers: React.Dispatch<React.SetStateAction<SelectedPlayer[]>>;
  onCollapseChange?: (collapsed: boolean) => void;
}

const SelectedPlayersSummary: React.FC<SelectedPlayersSummaryProps> = ({ selectedPlayers, setSelectedPlayers, onCollapseChange }) => {
  const [isOpen, setIsOpen] = useState(true); // Always open by default
  const [isDesktop, setIsDesktop] = useState(window.innerWidth >= 768);
  const [isCollapsed, setIsCollapsed] = useState(false); // New: collapse state
  const [hasManuallyClosedWithPlayers, setHasManuallyClosedWithPlayers] = useState(false);

  // Notify parent when collapse state changes
  const handleCollapseToggle = () => {
    const newCollapsedState = !isCollapsed;
    setIsCollapsed(newCollapsedState);
    if (onCollapseChange) {
      onCollapseChange(newCollapsedState);
    }
  };

  // Track screen size for responsive behavior
  useEffect(() => {
    const handleResize = () => {
      setIsDesktop(window.innerWidth >= 768);
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Check if lineup contains any demon or goblin picks
  const hasDemonOrGoblin = useMemo(() => {
    return selectedPlayers.some(p => p.modifier === 'demon' || p.modifier === 'goblin');
  }, [selectedPlayers]);
  
  // Count demons and goblins
  const demonCount = useMemo(() => selectedPlayers.filter(p => p.modifier === 'demon').length, [selectedPlayers]);
  const goblinCount = useMemo(() => selectedPlayers.filter(p => p.modifier === 'goblin').length, [selectedPlayers]);
  // Auto-open when a player is selected for the first time (only if user hasn't manually closed it)
  useEffect(() => {
    if (selectedPlayers.length > 0 && !isOpen && !hasManuallyClosedWithPlayers) {
      setIsOpen(true);
    }
    // Reset the manual close flag when all players are removed
    if (selectedPlayers.length === 0) {
      setHasManuallyClosedWithPlayers(false);
    }
  }, [selectedPlayers.length, isOpen, hasManuallyClosedWithPlayers]);

  const handleToggle = () => {
    const newIsOpen = !isOpen;
    setIsOpen(newIsOpen);
    // Track if user manually closes while there are players selected
    if (!newIsOpen && selectedPlayers.length > 0) {
      setHasManuallyClosedWithPlayers(true);
    }
  };

  const handleClearAll = () => {
    setSelectedPlayers([]);
  };

  const handleToggleSelection = (index: number, newSelection: 'more' | 'less') => {
    setSelectedPlayers(prev => 
      prev.map((player, i) => 
        i === index ? { ...player, selection: newSelection } : player
      )
    );
  };

  return (
    <div className="relative z-10">
      {/* Toggle Button - Always visible */}
      <span className='absolute -top-2 -left-2 bg-accent2/50 rounded-full border border-accent2 w-2 h-2 flex items-center justify-center text-xs font-bold text-white z-20'>
        {selectedPlayers.length}
      </span>
      <button
        onClick={handleToggle}
        className={`absolute -top-1 -left-1 z-10 bg-surface p-0.5 rounded-full border border-card-border flex items-center justify-center hover:bg-surface-hover transition-all ${
          isOpen ? 'shadow-lg' : ''
        }`}
      >
          <Activity className="text-accent2" />
      </button>
    

      {/* Summary Panel */}
      {isOpen && (
        <div className="bg-surface rounded-lg border border-card-border max-w-md flex flex-col" style={{ maxHeight: '600px' }}>
          {/* Header */}
          <div className="flex items-center justify-between px-3 py-2 border-b border-card-border shrink-0">
            <div>
              <h2 className="text-lg font-semibold text-text">
                Your Lineup
              </h2>
              <h3 className="text-xs text-text-muted mt-0.5">
                {selectedPlayers.length} Player{selectedPlayers.length !== 1 ? 's' : ''} Selected
              </h3>
            </div>
            {selectedPlayers.length > 0 && (
              <button 
                onClick={handleClearAll}
                className="text-xs text-text-muted hover:text-accent1 transition-colors font-medium"
              >
                Clear All
              </button>
            )}
          </div>

          {/* Player List - Collapsible with compact height */}
          {!isCollapsed && selectedPlayers.length > 0 ? (
            <div className="flex flex-col max-h-[180px] overflow-y-auto flex-shrink-0">
              {selectedPlayers.map((sp, index) => (
                <div 
                  key={`${sp.playerId}-${index}`}
                  className="px-3 py-1.5 hover:bg-card-bg/20 transition-colors border-b border-card-border/20 last:border-b-0"
                >
                  {/* First Row: Headshot */}
                  <div className="flex items-center gap-2 mb-1">
                    <img src={sp.image} alt={sp.playerName} className="w-8 h-8 rounded-full flex-shrink-0 border-2 border-card-border/50" />
                    <div className="font-bold text-base md:text-lg text-text truncate leading-tight">{sp.playerName}</div>
                  </div>

                  {/* Second Row: Stat Info + Toggle Buttons */}
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-1 text-sm md:text-base leading-tight">
                      <span className={`font-bold ${sp.selection === 'more' ? 'text-green-500' : 'text-red-500'}`}>
                        {sp.selection === 'more' ? 'O' : 'U'} {sp.statValue.toFixed(1)}
                      </span>
                      <span className="text-text-muted/70 truncate">{sp.category}</span>
                    </div>
                    
                    {/* Toggle buttons */}
                    <div className="flex gap-1 flex-shrink-0">
                      <button
                        onClick={() => handleToggleSelection(index, 'more')}
                        className={`w-5 h-5 rounded text-[10px] font-bold transition-all ${
                          sp.selection === 'more'
                            ? 'bg-green-500 text-white shadow-md'
                            : 'bg-card-bg border border-card-border text-text-muted hover:bg-green-500/20 hover:border-green-500/50'
                        }`}
                      >
                        O
                      </button>
                      <button
                        onClick={() => handleToggleSelection(index, 'less')}
                        className={`w-5 h-5 rounded text-[10px] font-bold transition-all ${
                          sp.selection === 'less'
                            ? 'bg-red-500 text-white shadow-md'
                            : 'bg-card-bg border border-card-border text-text-muted hover:bg-red-500/20 hover:border-red-500/50'
                        }`}
                      >
                        U
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : !isCollapsed && selectedPlayers.length === 0 ? (
            <div className="flex flex-col items-center py-4 px-4 text-text-muted flex-shrink-0">
              <CircleSlash className="w-6 h-6 mb-1" />
              <span className='text-xs font-medium'>No Players Selected</span>
              <span className='text-[10px] text-text-muted/70 mt-0.5'>Choose players below</span>
            </div>
          ) : null}

          {/* Betting Panel - Only show when players are selected and not collapsed */}
          {!isCollapsed && selectedPlayers.length > 0 && (
            <div className="flex-shrink-0 border-t border-card-border/30">
              <BettingPanel 
                selectedPlayers={selectedPlayers}
                onClearAll={handleClearAll}
              />
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default SelectedPlayersSummary
