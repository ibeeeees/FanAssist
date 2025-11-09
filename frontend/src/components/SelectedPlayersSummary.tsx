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
    

      {/* Summary Panel - Compact Minimal */}
      {isOpen && (
        <div className="bg-surface rounded-lg border border-card-border shadow-xl w-64">
          {/* Compact Header */}
          <div className="flex items-center justify-between px-3 py-2 border-b border-card-border">
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-bold text-text">Lineup</h2>
              <span className="text-xs font-bold text-white bg-accent1 px-1.5 py-0.5 rounded">
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

          {/* Compact Player List - Scrollable */}
          {selectedPlayers.length > 0 ? (
            <div className="flex flex-col max-h-[300px] overflow-y-auto divide-y divide-card-border/30">
              {selectedPlayers.map((sp, index) => (
                <div 
                  key={`${sp.playerId}-${index}`}
                  className="grid grid-cols-[auto_1fr_auto] items-center gap-2 px-3 py-2 hover:bg-card-bg/30 transition-colors"
                >
                  {/* Column 1: Headshot FIRST */}
                  <img src={sp.image} alt={sp.playerName} className="w-10 h-10 rounded-full flex-shrink-0 border-2 border-card-border" />

                  {/* Column 2: Name and Stats */}
                  <div className="min-w-0 flex flex-col">
                    <div className="flex items-center gap-1.5">
                      <span className="font-semibold text-xs text-text truncate">{sp.playerName}</span>
                    </div>
                    <div className="flex items-center gap-1 text-[10px] mt-0.5">
                      <span className={`font-bold ${sp.selection === 'more' ? 'text-green-500' : 'text-red-500'}`}>
                        {sp.selection === 'more' ? 'O' : 'U'} {sp.statValue.toFixed(1)}
                      </span>
                      <span className="text-text-muted/70 truncate">{sp.category}</span>
                    </div>
                  </div>
                  
                  {/* Column 3: O/U Toggle Buttons */}
                  <div className="flex gap-1 flex-shrink-0">
                    <button
                      onClick={() => handleToggleSelection(index, 'more')}
                      className={`w-6 h-6 rounded text-[10px] font-bold transition-all ${
                        sp.selection === 'more'
                          ? 'bg-green-500 text-white'
                          : 'bg-card-bg text-text-muted hover:bg-green-500/20'
                      }`}
                    >
                      O
                    </button>
                    <button
                      onClick={() => handleToggleSelection(index, 'less')}
                      className={`w-6 h-6 rounded text-[10px] font-bold transition-all ${
                        sp.selection === 'less'
                          ? 'bg-red-500 text-white'
                          : 'bg-card-bg text-text-muted hover:bg-red-500/20'
                      }`}
                    >
                      U
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center p-4 text-text-muted">
              <CircleSlash className="w-6 h-6 mb-1.5" />
              <span className='text-xs font-medium'>No Players Selected</span>
              <p className='text-[10px] font-light'>Build your lineup!</p>
            </div>
          )}

          {/* Betting Panel - Only show when players are selected */}
          {selectedPlayers.length > 0 && (
            <div className="mt-2">
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
