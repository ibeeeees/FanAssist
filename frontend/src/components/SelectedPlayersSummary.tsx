import React, { useState, useEffect } from 'react'
import { Activity, CircleSlash } from 'lucide-react'
import type { SelectedPlayer } from '../types'

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
    

      {/* Summary Panel */}
      {isOpen && (
        <div className="bg-surface p-1 rounded-lg border border-card-border">
          {/* Top Section */}
          <div className="flex items-center justify-start">
            <h2 className="text-2xl font-medium text-text m-1 whitespace-nowrap">
              {selectedPlayers.length > 0
               ? 'Your Lineup'
               : ''}
            </h2>
            <h3 className="text-sm text-text-muted m-1">
              {selectedPlayers.length > 0 
                ? `${selectedPlayers.length} Selected Player${selectedPlayers.length > 1 ? 's' : ''}`
                : ''
              }
            </h3>
            {selectedPlayers.length > 0 && (
              <button 
                onClick={handleClearAll}
                className="text-sm text-text-muted hover:text-text ml-auto mr-2"
              >
                Clear
              </button>
            )}
          </div>

          {/* Player List or Empty State */}
          {selectedPlayers.length > 0 ? (
            <div className="flex flex-col">
              {selectedPlayers.map((sp, index) => (
                <div 
                  key={`${sp.playerId}-${index}`}
                  className="flex flex-row items-start justify-between py-2 px-2 bg-card-bg border-b border-card-border gap-2"
                >
                  {/* Player Details */}
                  <div className="flex items-center gap-2 flex-1">
                    <img src={sp.image} alt={sp.playerName} className="w-5 h-5" />

                    <div className="flex flex-col items-start">
                      <span className="font-medium text-text text-left">{sp.playerName}</span>
                      <span className="text-xs text-text-muted text-left">
                        <span className="bg-surface text-[10px] mr-1">NBA</span>
                        {sp.teamAbbr} - {sp.position.join('/')}
                      </span>
                      <span className="text-xs text-text-muted mt-0.5 text-left">
                        {sp.gameDay}, {sp.gameTime} {sp.gameLocation === 'home' ? 'vs' : '@'} {sp.opponentAbbr}
                      </span>
                      <span className="text-sm text-text mt-0.5 text-left">
                        <span className='font-bold text-text'>{sp.statValue.toFixed(1)}</span>
                        <span className='text-text-muted'>{sp.category}</span>
                      </span>
                    </div>
                  </div>
                  
                  {/* More/Less Buttons */}
                  <div className="flex flex-col">
                    <button
                      onClick={() => handleToggleSelection(index, 'more')}
                      className={`px-4 py-1 rounded-t text-sm font-semibold transition-all ${
                        sp.selection === 'more'
                          ? 'bg-accent1 text-black'
                          : 'bg-surface hover:bg-surface-hover text-text border border-card-border'
                      }`}
                    >
                      More
                    </button>
                    <button
                      onClick={() => handleToggleSelection(index, 'less')}
                      className={`px-4 py-1 rounded-b text-sm font-semibold transition-all ${
                        sp.selection === 'less'
                          ? 'bg-accent1 text-black'
                          : 'bg-surface hover:bg-surface-hover text-text border border-card-border'
                      }`}
                    >
                      Less
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col p-5 w-full text-text-muted">
              <CircleSlash className="w-8 h-8 mx-auto mb-2" />
              <span className='mb-2 font-medium whitespace-nowrap'>No Players Selected</span>
              <p className='font-light whitespace-nowrap'>Start building your lineup!</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default SelectedPlayersSummary
