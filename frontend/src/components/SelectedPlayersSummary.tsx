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
    <div className="relative z-10">
      {/* Toggle Button - Always visible */}
      <span className='absolute -top-2 -left-2 bg-accent2/50 rounded-full border border-accent2 w-2 h-2 flex items-center justify-center text-xs font-bold text-white z-20'>
        {selectedPlayers.length}
      </span>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`absolute -top-1 -left-1 z-10 bg-surface p-0.5 rounded-full border border-card-border flex items-center justify-center hover:bg-surface-hover transition-all ${
          isOpen ? 'shadow-lg' : ''
        }`}
      >
          <Activity className="text-accent2" />
      </button>
    

      {/* Summary Panel - Ultra Minimal */}
      {isOpen && (
        <div className="bg-surface/95 backdrop-blur-sm rounded-lg border border-card-border/50 shadow-2xl w-56">
          {/* Minimal Header */}
          <div className="flex items-center justify-between px-2.5 py-1.5 border-b border-card-border/50">
            <div className="flex items-center gap-1.5">
              <h2 className="text-xs font-bold text-text">Lineup</h2>
              <span className="text-[10px] font-bold text-white bg-accent1 px-1 py-0.5 rounded-sm">
                {selectedPlayers.length}
              </span>
            </div>
            {selectedPlayers.length > 0 && (
              <button 
                onClick={handleClearAll}
                className="text-[10px] font-medium text-text-muted hover:text-red-500 transition-colors"
              >
                Clear
              </button>
            )}
          </div>

          {/* Ultra Compact Player List */}
          {selectedPlayers.length > 0 ? (
            <div className="flex flex-col max-h-[280px] overflow-y-auto">
              {selectedPlayers.map((sp, index) => (
                <div 
                  key={`${sp.playerId}-${index}`}
                  className="grid grid-cols-[auto_1fr_auto] items-center gap-1.5 px-2.5 py-1.5 hover:bg-card-bg/20 transition-colors border-b border-card-border/20 last:border-b-0"
                >
                  {/* Headshot */}
                  <img src={sp.image} alt={sp.playerName} className="w-7 h-7 rounded-full flex-shrink-0" />

                  {/* Info - Super Compact */}
                  <div className="min-w-0">
                    <div className="font-semibold text-[11px] text-text truncate leading-tight">{sp.playerName}</div>
                    <div className="flex items-center gap-0.5 text-[9px] leading-tight">
                      <span className={`font-bold ${sp.selection === 'more' ? 'text-green-500' : 'text-red-500'}`}>
                        {sp.selection === 'more' ? 'O' : 'U'} {sp.statValue.toFixed(1)}
                      </span>
                      <span className="text-text-muted/60">{sp.category}</span>
                    </div>
                  </div>
                  
                  {/* Micro Toggle */}
                  <div className="flex gap-0.5 flex-shrink-0">
                    <button
                      onClick={() => handleToggleSelection(index, 'more')}
                      className={`w-5 h-5 rounded text-[9px] font-bold transition-all ${
                        sp.selection === 'more'
                          ? 'bg-green-500 text-white'
                          : 'bg-card-bg/50 text-text-muted hover:bg-green-500/20'
                      }`}
                    >
                      O
                    </button>
                    <button
                      onClick={() => handleToggleSelection(index, 'less')}
                      className={`w-5 h-5 rounded text-[9px] font-bold transition-all ${
                        sp.selection === 'less'
                          ? 'bg-red-500 text-white'
                          : 'bg-card-bg/50 text-text-muted hover:bg-red-500/20'
                      }`}
                    >
                      U
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center py-3 px-2 text-text-muted">
              <CircleSlash className="w-5 h-5 mb-1" />
              <span className='text-[10px] font-medium'>No Players</span>
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
