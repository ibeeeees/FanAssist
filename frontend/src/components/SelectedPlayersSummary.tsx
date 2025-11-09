import React, { useState, useEffect } from 'react'
import { Activity, CircleSlash } from 'lucide-react'
import type { SelectedPlayer } from '../types'
import { BettingPanel } from './BettingPanel'

interface SelectedPlayersSummaryProps {
  selectedPlayers: SelectedPlayer[];
  setSelectedPlayers: React.Dispatch<React.SetStateAction<SelectedPlayer[]>>;
}

const SelectedPlayersSummary: React.FC<SelectedPlayersSummaryProps> = ({ selectedPlayers, setSelectedPlayers }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isDesktop, setIsDesktop] = useState(window.innerWidth >= 768);

  // Track screen size for responsive behavior
  useEffect(() => {
    const handleResize = () => {
      setIsDesktop(window.innerWidth >= 768);
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Auto-open when a player is selected (only if currently closed)
  useEffect(() => {
    if (selectedPlayers.length > 0 && !isOpen) {
      setIsOpen(true);
    }
  }, [selectedPlayers.length, isOpen]);

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
    <div className="relative z-10 w-full">
      {/* Toggle Button - Always visible on mobile/tablet */}
      <span className='absolute -top-2 -left-2 bg-accent2/50 rounded-full border border-accent2 w-2 h-2 flex items-center justify-center text-xs font-bold text-white z-20 md:hidden'>
        {selectedPlayers.length}
      </span>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`absolute -top-1 -left-1 z-10 bg-surface p-0.5 rounded-full border border-card-border flex items-center justify-center hover:bg-surface-hover transition-all md:hidden ${
          isOpen ? 'shadow-lg' : ''
        }`}
      >
          <Activity className="text-accent2" />
      </button>
    

      {/* Summary Panel - Responsive & Always visible on desktop */}
      {(isOpen || isDesktop) && (
        <div className="bg-surface/95 backdrop-blur-sm rounded-lg border border-card-border/50 shadow-2xl w-full">
          {/* Header - Responsive */}
          <div className="flex items-center justify-between px-3 py-2 border-b border-card-border/50">
            <div className="flex items-center gap-2">
              <h2 className="text-sm md:text-base font-bold text-text">Your Lineup</h2>
              <span className="text-xs font-bold text-white bg-accent1 px-2 py-0.5 rounded">
                {selectedPlayers.length}
              </span>
            </div>
            {selectedPlayers.length > 0 && (
              <button 
                onClick={handleClearAll}
                className="text-xs font-medium text-text-muted hover:text-red-500 transition-colors"
              >
                Clear
              </button>
            )}
          </div>

          {/* Player List - Responsive with bigger font */}
          {selectedPlayers.length > 0 ? (
            <div className="flex flex-col max-h-[50vh] md:max-h-[400px] overflow-y-auto">
              {selectedPlayers.map((sp, index) => (
                <div 
                  key={`${sp.playerId}-${index}`}
                  className="grid grid-cols-[auto_1fr_auto] items-center gap-2 md:gap-3 px-3 py-2 hover:bg-card-bg/20 transition-colors border-b border-card-border/20 last:border-b-0"
                >
                  {/* Headshot - Same size */}
                  <img src={sp.image} alt={sp.playerName} className="w-7 h-7 rounded-full flex-shrink-0 border border-card-border/50" />

                  {/* Info - Bigger font, more visible */}
                  <div className="min-w-0">
                    <div className="font-bold text-sm md:text-base text-text truncate leading-tight">{sp.playerName}</div>
                    <div className="flex items-center gap-1 text-xs md:text-sm leading-tight mt-0.5">
                      <span className={`font-bold ${sp.selection === 'more' ? 'text-green-500' : 'text-red-500'}`}>
                        {sp.selection === 'more' ? 'O' : 'U'} {sp.statValue.toFixed(1)}
                      </span>
                      <span className="text-text-muted/70 truncate">{sp.category}</span>
                    </div>
                  </div>
                  
                  {/* Toggle buttons - Same size but more visible */}
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
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center py-6 px-4 text-text-muted">
              <CircleSlash className="w-8 h-8 mb-2" />
              <span className='text-sm font-medium'>No Players Selected</span>
              <span className='text-xs text-text-muted/70 mt-1'>Choose players below</span>
            </div>
          )}

          {/* Betting Panel - Only show when players are selected */}
          {selectedPlayers.length > 0 && (
            <div className="mt-1">
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
