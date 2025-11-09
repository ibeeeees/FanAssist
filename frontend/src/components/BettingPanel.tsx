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
    <div className="bg-surface p-4 rounded-lg border border-card-border">
      {/* Balance Section - Enhanced */}
      <div className="mb-4 p-4 bg-gradient-to-br from-card-bg via-card-bg to-surface rounded-xl border border-card-border shadow-lg">
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm font-semibold text-text-muted uppercase tracking-wide">Paper Money</span>
          <button
            onClick={() => fetchBalance(true)}
            disabled={isLoading}
            className="text-xs text-accent1 hover:text-accent2 disabled:opacity-50 transition-colors p-1.5 hover:bg-accent1/10 rounded-lg"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          </button>
        </div>
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2 bg-gradient-to-br from-green-500/20 to-green-600/10 rounded-lg">
            <DollarSign className="w-6 h-6 text-green-500 drop-shadow-md" />
          </div>
          <span className="text-3xl font-bold bg-gradient-to-r from-green-500 to-green-600 bg-clip-text text-transparent">
            {balance !== null ? `$${balance.toFixed(2)}` : 'Loading...'}
          </span>
        </div>
        <button
          onClick={handleResetBalance}
          className="mt-2 text-xs text-text-muted hover:text-accent1 transition-colors font-medium"
        >
          Reset Balance
        </button>
      </div>

      {/* Bet Mode Selection */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-text mb-2">
          Bet Mode
        </label>
        <div className="grid grid-cols-2 gap-2">
          <button
            onClick={() => setBetMode('standard')}
            className={`py-3 px-4 rounded-xl text-sm font-bold transition-all duration-300 ${
              betMode === 'standard'
                ? 'bg-gradient-to-br from-accent1 to-accent2 text-black shadow-lg shadow-accent1/30 scale-105'
                : 'bg-card-bg text-text-muted hover:bg-surface border border-card-border hover:border-accent1/30'
            }`}
          >
            ⚡ Power
          </button>
          <button
            onClick={() => setBetMode('flex')}
            className={`py-3 px-4 rounded-xl text-sm font-bold transition-all duration-300 ${
              betMode === 'flex'
                ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white shadow-lg shadow-blue-500/30 scale-105'
                : 'bg-card-bg text-text-muted hover:bg-surface border border-card-border hover:border-blue-500/30'
            }`}
          >
            🎯 Flex
          </button>
        </div>

        {/* Bet Mode Info - Enhanced */}
        <div className="mt-3 p-2.5 rounded-lg bg-gradient-to-r from-accent1/5 to-accent2/5 border border-accent1/10">
          <p className="text-xs text-text-muted font-medium">
            {betMode === 'standard' && '⚡ Power Play - All legs must win for maximum payout'}
            {betMode === 'flex' && '🎯 Flex Play - Win even if 1 leg misses (reduced payout)'}
          </p>
        </div>
      </div>

      {/* Wager Input - Enhanced */}
      <div className="mb-4">
        <label className="block text-sm font-semibold text-text mb-3 uppercase tracking-wide">
          Wager Amount
        </label>
        <div className="relative">
          <div className="absolute left-3 top-1/2 transform -translate-y-1/2 p-1.5 bg-gradient-to-br from-green-500/20 to-green-600/10 rounded-lg">
            <DollarSign className="w-4 h-4 text-green-500" />
          </div>
          <input
            type="number"
            value={wagerAmount}
            onChange={(e) => setWagerAmount(e.target.value)}
            className="w-full pl-14 pr-4 py-3 bg-card-bg border-2 border-card-border rounded-xl text-text font-semibold text-lg focus:outline-none focus:ring-2 focus:ring-accent1 focus:border-accent1 transition-all shadow-sm hover:shadow-md"
            placeholder="50"
            min="1"
            step="1"
          />
        </div>
      </div>

      {/* Place Bet Button - Enhanced */}
      <button
        onClick={handlePlaceParlay}
        disabled={isLoading || selectedPlayers.length < 2}
        className={`w-full py-4 rounded-xl font-bold text-white flex items-center justify-center gap-2 transition-all duration-300 shadow-lg ${
          selectedPlayers.length < 2
            ? 'bg-gray-400 cursor-not-allowed opacity-50'
            : isLoading
            ? 'bg-gradient-to-r from-blue-400 to-blue-500 cursor-wait animate-pulse'
            : 'bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]'
        }`}
      >
        {isLoading ? (
          <>
            <RefreshCw className="w-5 h-5 animate-spin" />
            <span>Placing Bet...</span>
          </>
        ) : (
          <>
            <TrendingUp className="w-5 h-5" />
            <span>Place {selectedPlayers.length}-Leg Parlay</span>
          </>
        )}
      </button>

      {/* Parlay Info */}
      {selectedPlayers.length > 0 && (
        <div className="mt-3 text-xs text-text-muted">
          <p>• Minimum 2 legs, Maximum 6 legs</p>
          <p>• All legs must win for payout</p>
          <p>• {selectedPlayers.length} leg{selectedPlayers.length > 1 ? 's' : ''} selected</p>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mt-4 p-3 bg-red-100 dark:bg-red-900 rounded-lg flex items-start gap-2">
          <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-300 flex-shrink-0 mt-0.5" />
          <span className="text-sm text-red-800 dark:text-red-200">{error}</span>
        </div>
      )}

      {/* Bet Result */}
      {showResult && betResult && (
        <div className={`mt-4 p-4 rounded-lg ${
          betResult.betting_summary?.won 
            ? 'bg-green-100 dark:bg-green-900' 
            : 'bg-red-100 dark:bg-red-900'
        }`}>
          <div className="flex items-center gap-2 mb-2">
            {betResult.betting_summary?.won ? (
              <CheckCircle className="w-6 h-6 text-green-600 dark:text-green-300" />
            ) : (
              <AlertCircle className="w-6 h-6 text-red-600 dark:text-red-300" />
            )}
            <span className={`font-bold text-lg ${
              betResult.betting_summary?.won 
                ? 'text-green-800 dark:text-green-200'
                : 'text-red-800 dark:text-red-200'
            }`}>
              {betResult.betting_summary?.won ? 'YOU WON! 🎉' : 'Bet Lost'}
            </span>
          </div>
          
          <div className="text-sm space-y-1">
            <p className="text-gray-800 dark:text-gray-200">
              Payout: <strong>${betResult.betting_summary?.payout?.toFixed(2)}</strong>
            </p>
            <p className="text-gray-800 dark:text-gray-200">
              Profit: <strong>${betResult.betting_summary?.profit?.toFixed(2)}</strong>
            </p>
            <p className="text-gray-800 dark:text-gray-200">
              New Balance: <strong>${betResult.betting_summary?.new_balance?.toFixed(2)}</strong>
            </p>
            <p className="text-xs text-gray-600 dark:text-gray-400 mt-2">
              {betResult.num_wins}/{betResult.num_legs} legs won
            </p>
            
            {/* Simulation Results for Each Leg */}
            {betResult.legs && betResult.legs.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                <p className="text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2">Simulation Results:</p>
                <div className="space-y-1">
                  {betResult.legs.map((leg: any, index: number) => {
                    const roundToHalf = (v: number) => Math.round(v * 2) / 2;
                    const simVal = leg.simulated_value !== undefined && leg.simulated_value !== null ? roundToHalf(leg.simulated_value) : null;
                    return (
                      <div key={index} className="text-xs">
                        <span className="font-medium">{leg.player_name}</span> - {leg.prop_type}{' '}
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
