import React, { useState, useEffect, useMemo } from 'react'
import { Activity, CircleSlash } from 'lucide-react'
import type { SelectedPlayer } from '../types'
import { calculatePayout } from '../services/payoutCalculator'

interface SelectedPlayersSummaryProps {
  selectedPlayers: SelectedPlayer[];
  setSelectedPlayers: React.Dispatch<React.SetStateAction<SelectedPlayer[]>>;
}

const SelectedPlayersSummary: React.FC<SelectedPlayersSummaryProps> = ({ selectedPlayers, setSelectedPlayers }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [hasManuallyClosedWithPlayers, setHasManuallyClosedWithPlayers] = useState(false);
  const [playType, setPlayType] = useState<'power' | 'flex'>('power');
  const [entryAmount, setEntryAmount] = useState<string>('10');

  // Calculate payout dynamically
  const payoutResult = useMemo(() => {
    if (selectedPlayers.length === 0) {
      return null;
    }

    // Convert SelectedPlayer to Pick format
    const picks = selectedPlayers.map(player => ({
      id: player.playerId,
      playerId: player.playerId,
      playerName: player.playerName,
      category: player.category,
      selection: player.selection,
      statValue: player.statValue,
      status: 'win' as const, // Default to 'win' for preview
      modifier: player.modifier || null,
    }));

    try {
      const entry = parseFloat(entryAmount) || 0;
      return calculatePayout(picks, playType, entry);
    } catch (error) {
      console.error('Payout calculation error:', error);
      return null;
    }
  }, [selectedPlayers, playType, entryAmount]);

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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedPlayers.length === 0) {
      return;
    }
    console.log('Submitting lineup:', {
      players: selectedPlayers,
      playType: playType,
      entryAmount: parseFloat(entryAmount) || 0,
      potentialPayout: payoutResult?.payoutAmount || 0,
      multiplier: payoutResult?.multiplier || 0,
    });
    // Add your submission logic here
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

          {selectedPlayers.length === 0 ? (
            /* Empty State */
            <div className="flex flex-row items-center justify-center py-12 text-text-muted flex-1">
              <CircleSlash className="w-12 h-12 mb-3 opacity-50" />
              <span className="mb-1 font-medium text-sm">No Players Selected</span>
              <p className="font-light text-xs">Start building your lineup!</p>
            </div>
          ) : (
            <>
              {/* Scrollable Content Area */}
              <div className="flex-1 overflow-y-auto">
                {/* Player List */}
                <div className="divide-y divide-card-border">
                  {selectedPlayers.map((sp, index) => (
                    <div 
                      key={`${sp.playerId}-${index}`}
                      className={`flex items-start justify-between px-2.5 py-2 hover:bg-card-bg transition-colors gap-2 ${
                        sp.modifier === 'demon' ? 'border-l-2 border-l-red-600' : 
                        sp.modifier === 'goblin' ? 'border-l-2 border-l-green-600' : ''
                      }`}
                    >
                      {/* Player Details */}
                      <div className="flex w-auto items-start gap-2 flex-1 min-w-0 whitespace-nowrap overflow-hidden">
                        <img src={sp.image} alt={sp.playerName} className="w-5 h-5 shrink-0" />

                        <div className="flex flex-col items-start flex-1 min-w-0">
                          <div className="flex items-center gap-1">
                            <span className="text-left font-semibold text-text text-xs leading-tight">{sp.playerName}</span>
                            {sp.modifier && (
                              <span className={`text-[8px] px-1 py-0.5 rounded font-bold ${
                                sp.modifier === 'demon' 
                                  ? 'bg-red-600 text-white' 
                                  : 'bg-green-600 text-white'
                              }`}>
                                {sp.modifier === 'demon' ? '😈' : '🤢'}
                              </span>
                            )}
                          </div>
                          <span className="text-left text-[10px] text-text-muted mt-0.5">
                            <span className="text-left bg-card-bg rounded text-[9px] font-medium">NBA</span>
                            {sp.teamAbbr} - {sp.position.join('/')}
                          </span>
                          <span className="text-left text-[10px] text-text-muted mt-0.5">
                            {sp.gameDay}, {sp.gameTime} {sp.gameLocation === 'home' ? 'vs' : '@'} {sp.opponentAbbr}
                          </span>
                          <div className="flex text-xs text-text gap-0.5 font-medium">
                            <span className={`text-left font-bold ${
                              sp.modifier === 'demon' ? 'text-red-500' : 
                              sp.modifier === 'goblin' ? 'text-green-500' : ''
                            }`}>
                              {sp.statValue.toFixed(1)}
                            </span>
                            <span className="text-left text-text-muted"> {sp.category}</span>
                          </div>
                        </div>
                      </div>
                      
                      {/* More/Less Buttons */}
                      <div className="flex flex-col shrink-0">
                        <button
                          type="button"
                          onClick={() => handleToggleSelection(index, 'more')}
                          className={`px-2 py-0.5 rounded-t text-[10px] font-bold transition-all ${
                            sp.selection === 'more'
                              ? 'bg-accent1 text-black shadow-sm'
                              : 'bg-card-bg hover:bg-surface text-text border border-card-border'
                          }`}
                        >
                          More
                        </button>
                        <button
                          type="button"
                          onClick={() => handleToggleSelection(index, 'less')}
                          className={`px-2 py-0.5 rounded-b text-[10px] font-bold transition-all ${
                            sp.selection === 'less'
                              ? 'bg-accent1 text-black shadow-sm'
                              : 'bg-card-bg hover:bg-surface text-text border border-card-border'
                          }`}
                        >
                          Less
                        </button>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Play Type Selection */}
                <div className="px-3 py-2 border-t border-card-border">
                  <label className="block text-[10px] font-semibold text-text-muted mb-1.5">
                    Select Play Type
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {/* Power Play */}
                    <button
                      type="button"
                      onClick={() => setPlayType('power')}
                      disabled={selectedPlayers.length < 2}
                      className={`px-2 py-2 rounded-lg text-xs font-bold transition-all ${
                        playType === 'power' && selectedPlayers.length >= 2
                          ? 'bg-accent1 text-black border-2 border-accent1 shadow-md'
                          : selectedPlayers.length >= 2
                          ? 'bg-card-bg border border-card-border text-text hover:border-accent1 hover:bg-surface'
                          : 'bg-card-bg border border-card-border text-text-muted cursor-not-allowed opacity-40'
                      }`}
                    >
                      <div className="flex flex-col items-center gap-0.5">
                        <span>Power Play</span>
                        <span className={`text-[9px] font-medium ${playType === 'power' && selectedPlayers.length >= 2 ? 'opacity-80' : 'opacity-60'}`}>
                          2+ picks
                        </span>
                      </div>
                    </button>

                    {/* Flex Play */}
                    <button
                      type="button"
                      onClick={() => setPlayType('flex')}
                      disabled={selectedPlayers.length < 3}
                      className={`px-2 py-2 rounded-lg text-xs font-bold transition-all ${
                        playType === 'flex' && selectedPlayers.length >= 3
                          ? 'bg-accent2 text-white border-2 border-accent2 shadow-md'
                          : selectedPlayers.length >= 3
                          ? 'bg-card-bg border border-card-border text-text hover:border-accent2 hover:bg-surface'
                          : 'bg-card-bg border border-card-border text-text-muted cursor-not-allowed opacity-40'
                      }`}
                    >
                      <div className="flex flex-col items-center gap-0.5">
                        <span>Flex Play</span>
                        <span className={`text-[9px] font-medium ${playType === 'flex' && selectedPlayers.length >= 3 ? 'opacity-80' : 'opacity-60'}`}>
                          3+ picks
                        </span>
                      </div>
                    </button>
                  </div>

                  {/* Helper text */}
                  {selectedPlayers.length === 1 && (
                    <p className="text-[10px] text-text-muted mt-1.5 text-center italic">
                      Add 1 more player to unlock Power Play
                    </p>
                  )}
                  {selectedPlayers.length === 2 && (
                    <p className="text-[10px] text-text-muted mt-1.5 text-center italic">
                      Add 1 more player to unlock Flex Play
                    </p>
                  )}
                </div>
              </div>

              {/* Fixed Form Section at Bottom */}
              <div className="border-t border-card-border bg-card-bg shrink-0">
                <form onSubmit={handleSubmit} className="p-3">
                  {/* Entry Amount and Potential Payout */}
                  <div className="grid grid-cols-2 gap-2 mb-1">
                    {/* Entry Amount */}
                    <div className="flex flex-co l">
                      <label htmlFor="entryAmount" className="text-left block text-[10px] font-semibold text-text-muted mb-1">
                        Entry Amount
                      </label>
                      <div className="relative px-1 py-1">
                        <span className="absolute left-2 top-1/2 -translate-y-1/2 text-text-muted font-medium text-xs">$</span>
                        <input
                          id="entryAmount"
                          type="number"
                          step="0.01"
                          min="0"
                          placeholder="10.00"
                          value={entryAmount}
                          onChange={(e) => setEntryAmount(e.target.value)}
                          className="w-full pl-5 pr-2 py-1.5 text-xs bg-surface text-text border border-card-border rounded-lg focus:outline-none focus:border-accent1 focus:ring-1 focus:ring-accent1/20 font-medium"
                        />
                      </div>
                    </div>

                    {/* Potential Payout - Read-only */}
                    <div className="flex flex-col">
                      <label className="text-left block text-[10px] font-semibold text-text-muted mb-1">
                        Potential Payout
                      </label>
                      <div className="w-full px-1 py-1 text-xs bg-surface text-text border border-card-border rounded-lg">
                        {payoutResult ? (
                          <div className="flex items-baseline gap-0.5">
                            <span className="font-bold text-accent1 text-sm">
                              {payoutResult.multiplier}x
                            </span>
                            <span className="text-[10px] text-text-muted">=</span>
                            <span className="font-bold text-text text-xs">
                              ${payoutResult.payoutAmount.toFixed(2)}
                            </span>
                          </div>
                        ) : (
                          <span className="text-text-muted font-medium">$0.00</span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Payout Info */}
                  {payoutResult && payoutResult.pushCount > 0 && (
                    <div className="text-[10px] text-accent2 bg-surface px-2 py-1.5 rounded-lg border border-accent2/20">
                      ℹ️ {payoutResult.pushCount} push{payoutResult.pushCount !== 1 ? 'es' : ''} removed. 
                      Graded as {payoutResult.activePickCount}-pick.
                    </div>
                  )}

                  {/* Submit Button */}
                  <button
                    type="submit"
                    disabled={selectedPlayers.length === 0 || (playType === 'power' && selectedPlayers.length < 2) || (playType === 'flex' && selectedPlayers.length < 3)}
                    className={`w-full p-1 rounded-lg font-bold text-xs transition-all ${
                      selectedPlayers.length > 0 && 
                      ((playType === 'power' && selectedPlayers.length >= 2) || (playType === 'flex' && selectedPlayers.length >= 3))
                        ? 'bg-accent2 text-white hover:bg-accent2/90 shadow-md hover:shadow-lg'
                        : 'bg-surface text-text-muted cursor-not-allowed border border-card-border opacity-50'
                    }`}
                  >
                    Submit Lineup
                  </button>
                </form>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  )
}

export default SelectedPlayersSummary
