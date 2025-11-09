/**
 * Betting Panel Component - Integrates with backend for placing bets
 */

import React, { useState, useEffect } from 'react';
import { DollarSign, TrendingUp, AlertCircle, CheckCircle, RefreshCw } from 'lucide-react';
import { useBetting } from '../hooks/useBetting';
import type { SelectedPlayer } from '../types';

interface BettingPanelProps {
  selectedPlayers: SelectedPlayer[];
  onClearAll: () => void;
}

export const BettingPanel: React.FC<BettingPanelProps> = ({ selectedPlayers, onClearAll }) => {
  const { balance, isLoading, error, fetchBalance, submitParlay, resetUserBalance } = useBetting();
  const [wagerAmount, setWagerAmount] = useState<string>('50');
  const [betResult, setBetResult] = useState<any>(null);
  const [showResult, setShowResult] = useState(false);
  const [betMode, setBetMode] = useState<'standard' | 'flex'>('standard'); // Removed power_play

  // Fetch balance on mount
  useEffect(() => {
    fetchBalance();
  }, [fetchBalance]);

  const handlePlaceParlay = async () => {
    if (selectedPlayers.length < 2) {
      alert('You need at least 2 players for a parlay!');
      return;
    }

    if (selectedPlayers.length > 6) {
      alert('Maximum 6 players allowed in a parlay!');
      return;
    }

    const wager = parseFloat(wagerAmount);
    if (isNaN(wager) || wager <= 0) {
      alert('Please enter a valid wager amount');
      return;
    }

    if (balance && wager > balance) {
      alert(`Insufficient balance! You have $${balance.toFixed(2)}`);
      return;
    }

    try {
      // Map frontend prop names to backend prop types
      // Backend supports: points, rebounds, assists, steals, turnovers, threes_made, pra, pr, pa
      const propTypeMap: Record<string, string> = {
        'Popular': 'points',
        'Points': 'points',
        'Rebounds': 'rebounds',
        'Assists': 'assists',
        '3-PT Made': 'threes_made',
        'Pts+Asts': 'pa',
        'Pts+Rebs+Asts': 'pra',
        'Pts+Rebs': 'pr',
        'Steals': 'steals',
        'Turnovers': 'turnovers',
        'Blocked Shots': 'points', // Backend doesn't support blocks, fallback to points
        // Additional mappings for all frontend categories
        'Rebs+Asts': 'rebounds', // No direct backend support
        'Blks+Stls': 'steals', // Fallback to steals
        'FG Made': 'points', // No direct backend support
        'Defensive Rebounds': 'rebounds',
        'Offensive Rebounds': 'rebounds',
        'Fantasy Score': 'pra', // Fantasy score = PRA
        '3-PT Attempted': 'threes_made',
        'Points (Combo)': 'points',
        '3-PT Made (Combo)': 'threes_made',
        'Assists (Combo)': 'assists',
        'Rebounds (Combo)': 'rebounds',
        'Free Throws Made': 'points',
        'FG Attempted': 'points',
        'Dunks': 'points',
        'Free Throws Attempted': 'points',
        'Personal Fouls': 'turnovers', // Fouls similar to turnovers (negative stats)
        'Assists - 1st 3 Minutes': 'assists',
        'Points - 1st 3 Minutes': 'points',
        'Quarters with 3+ Points': 'points',
        'Rebounds - 1st 3 Minutes': 'rebounds',
        'Quarters with 5+ Points': 'points',
        'Two Pointers Attempted': 'points',
        'Two Pointers Made': 'points',
      };

      const parlayData = {
        bets: selectedPlayers.map(player => {
          const mappedPropType = propTypeMap[player.category];
          
          if (!mappedPropType) {
            console.warn(`Unknown category: ${player.category}, defaulting to 'points'`);
          }
          
          return {
            player_name: player.playerName,
            prop_type: mappedPropType || 'points',
            line: player.statValue,
            pick: player.selection === 'more' ? 'OVER' as const : 'UNDER' as const,
          };
        }),
        total_wager: wager,
        bet_mode: betMode,
      };

      console.log('Placing parlay:', JSON.stringify(parlayData, null, 2));
      const result = await submitParlay(parlayData);
      console.log('Parlay result:', result);
      
      setBetResult(result);
      setShowResult(true);
      
      // Refresh balance after bet
      await fetchBalance(true);
      
      // Clear selections after bet
      setTimeout(() => {
        setShowResult(false);
        onClearAll();
      }, 5000);
    } catch (err) {
      console.error('Error placing parlay:', err);
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      alert(`Failed to place bet: ${errorMessage}\n\nCheck console for details.`);
    }
  };

  const handleResetBalance = async () => {
    if (confirm('Are you sure you want to reset your balance to $10,000?')) {
      try {
        await resetUserBalance();
        alert('Balance reset successfully!');
      } catch (err) {
        alert('Failed to reset balance');
      }
    }
  };

  return (
    <div className="bg-surface/50 p-2 rounded-lg border border-card-border/50">
      {/* Balance Section - Compact */}
      <div className="mb-2 p-2 bg-card-bg/30 rounded-lg border border-card-border/30">
        <div className="flex items-center justify-between mb-1">
          <span className="text-[10px] font-semibold text-text-muted uppercase">Paper Money</span>
          <button
            onClick={() => fetchBalance(true)}
            disabled={isLoading}
            className="text-[10px] text-accent1 hover:text-accent2 disabled:opacity-50 transition-colors"
          >
            <RefreshCw className={`w-3 h-3 ${isLoading ? 'animate-spin' : ''}`} />
          </button>
        </div>
        <div className="flex items-center gap-1.5 mb-1">
          <div className="p-0.5 bg-green-500/20 rounded">
            <DollarSign className="w-3 h-3 text-green-500" />
          </div>
          <span className="text-lg font-bold text-green-500">
            {balance !== null ? `$${balance.toFixed(2)}` : '...'}
          </span>
        </div>
        <button
          onClick={handleResetBalance}
          className="text-[9px] text-text-muted hover:text-accent1 transition-colors"
        >
          Reset
        </button>
      </div>

      {/* Bet Mode Selection - Compact */}
      <div className="mb-2">
        <label className="block text-[10px] font-medium text-text mb-1">
          Mode
        </label>
        <div className="grid grid-cols-2 gap-1">
          <button
            onClick={() => setBetMode('standard')}
            className={`py-1 px-2 rounded text-[10px] font-bold transition-all ${
              betMode === 'standard'
                ? 'bg-gradient-to-r from-accent1 to-accent2 text-black'
                : 'bg-card-bg/50 text-text-muted hover:bg-card-bg border border-card-border/50'
            }`}
          >
            ⚡ Power
          </button>
          <button
            onClick={() => setBetMode('flex')}
            className={`py-1 px-2 rounded text-[10px] font-bold transition-all ${
              betMode === 'flex'
                ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white'
                : 'bg-card-bg/50 text-text-muted hover:bg-card-bg border border-card-border/50'
            }`}
          >
            🎯 Flex
          </button>
        </div>

        {/* Bet Mode Info - Compact */}
        <div className="mt-1 p-1 rounded bg-accent1/5 border border-accent1/10">
          <p className="text-[9px] text-text-muted leading-tight">
            {betMode === 'standard' && 'All legs must win'}
            {betMode === 'flex' && 'Win if 1 leg misses'}
          </p>
        </div>
      </div>

      {/* Wager Input - Compact */}
      <div className="mb-2">
        <label className="block text-[10px] font-medium text-text mb-1">
          Wager
        </label>
        <div className="relative">
          <div className="absolute left-1.5 top-1/2 transform -translate-y-1/2 p-0.5 bg-green-500/20 rounded">
            <DollarSign className="w-3 h-3 text-green-500" />
          </div>
          <input
            type="number"
            value={wagerAmount}
            onChange={(e) => setWagerAmount(e.target.value)}
            className="w-full pl-8 pr-2 py-1 bg-card-bg border border-card-border rounded text-text font-semibold text-sm focus:outline-none focus:ring-1 focus:ring-accent1 focus:border-accent1 transition-all"
            placeholder="50"
            min="1"
            step="1"
          />
        </div>
      </div>

      {/* Place Bet Button - Compact */}
      <button
        onClick={handlePlaceParlay}
        disabled={isLoading || selectedPlayers.length < 2}
        className={`w-full py-1.5 rounded text-xs font-bold text-white flex items-center justify-center gap-1 transition-all ${
          selectedPlayers.length < 2
            ? 'bg-gray-400 cursor-not-allowed opacity-50'
            : isLoading
            ? 'bg-blue-500 cursor-wait animate-pulse'
            : 'bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700'
        }`}
      >
        {isLoading ? (
          <>
            <RefreshCw className="w-3 h-3 animate-spin" />
            <span>Placing...</span>
          </>
        ) : (
          <>
            <TrendingUp className="w-3 h-3" />
            <span>Place {selectedPlayers.length}-Leg</span>
          </>
        )}
      </button>

      {/* Parlay Info - Compact */}
      {selectedPlayers.length > 0 && (
        <div className="mt-1 text-[9px] text-text-muted leading-tight">
          <p>Min 2, Max 6 legs • {selectedPlayers.length} selected</p>
        </div>
      )}

      {/* Error Message - Compact */}
      {error && (
        <div className="mt-2 p-1.5 bg-red-100 dark:bg-red-900 rounded flex items-start gap-1">
          <AlertCircle className="w-3 h-3 text-red-600 dark:text-red-300 flex-shrink-0 mt-0.5" />
          <span className="text-[10px] text-red-800 dark:text-red-200">{error}</span>
        </div>
      )}

      {/* Bet Result - Compact */}
      {showResult && betResult && (
        <div className={`mt-2 p-2 rounded ${
          betResult.betting_summary?.won 
            ? 'bg-green-100 dark:bg-green-900' 
            : 'bg-red-100 dark:bg-red-900'
        }`}>
          <div className="flex items-center gap-1 mb-1">
            {betResult.betting_summary?.won ? (
              <CheckCircle className="w-4 h-4 text-green-600 dark:text-green-300" />
            ) : (
              <AlertCircle className="w-4 h-4 text-red-600 dark:text-red-300" />
            )}
            <span className={`font-bold text-xs ${
              betResult.betting_summary?.won 
                ? 'text-green-800 dark:text-green-200'
                : 'text-red-800 dark:text-red-200'
            }`}>
              {betResult.betting_summary?.won ? 'WON! 🎉' : 'Lost'}
            </span>
          </div>
          
          <div className="text-[10px] space-y-0.5">
            <p className="text-gray-800 dark:text-gray-200">
              Payout: <strong>${betResult.betting_summary?.payout?.toFixed(2)}</strong>
            </p>
            <p className="text-gray-800 dark:text-gray-200">
              Profit: <strong>${betResult.betting_summary?.profit?.toFixed(2)}</strong>
            </p>
            <p className="text-gray-800 dark:text-gray-200">
              Balance: <strong>${betResult.betting_summary?.new_balance?.toFixed(2)}</strong>
            </p>
            <p className="text-[9px] text-gray-600 dark:text-gray-400 mt-1">
              {betResult.num_wins}/{betResult.num_legs} won
            </p>
            
            {/* Simulation Results - Compact */}
            {betResult.legs && betResult.legs.length > 0 && (
              <div className="mt-1.5 pt-1.5 border-t border-gray-200 dark:border-gray-700">
                <p className="text-[9px] font-semibold text-gray-700 dark:text-gray-300 mb-1">Results:</p>
                <div className="space-y-0.5">
                  {betResult.legs.map((leg: any, index: number) => {
                    const roundToHalf = (v: number) => Math.round(v * 2) / 2;
                    const simVal = leg.simulated_value !== undefined && leg.simulated_value !== null ? roundToHalf(leg.simulated_value) : null;
                    return (
                      <div key={index} className="text-[9px] leading-tight">
                        <span className="font-medium">{leg.player_name}</span>{' '}
                        <span className={leg.won ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}>
                          {leg.selection === 'more' ? 'O' : 'U'} {leg.line}: {simVal !== null ? simVal.toFixed(1) : 'N/A'} {leg.won ? '✓' : '✗'}
                        </span>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
