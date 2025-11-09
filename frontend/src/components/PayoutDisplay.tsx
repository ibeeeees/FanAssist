/**
 * PayoutDisplay Component
 * 
 * Displays payout information for the current lineup
 */

import React, { useMemo } from 'react';
import { calculatePayout, formatMultiplier, formatCurrency, getPayoutDescription } from '../services/payoutCalculator';
import type { SelectedPlayer } from '../types';

interface PayoutDisplayProps {
  selectedPlayers: SelectedPlayer[];
  playType: 'power' | 'flex';
  entryAmount: number;
}

const PayoutDisplay: React.FC<PayoutDisplayProps> = ({
  selectedPlayers,
  playType,
  entryAmount,
}) => {
  // Convert SelectedPlayer to Pick format for calculator
  const picks = useMemo(() => {
    return selectedPlayers.map(player => ({
      id: player.playerId,
      playerId: player.playerId,
      playerName: player.playerName,
      category: player.category,
      selection: player.selection,
      statValue: player.statValue,
      status: player.status || 'win', // Default to 'win' for simulation
      modifier: null,
    }));
  }, [selectedPlayers]);

  // Calculate payout
  const payoutResult = useMemo(() => {
    if (picks.length === 0) {
      return null;
    }

    try {
      return calculatePayout(picks, playType, entryAmount);
    } catch (error) {
      console.error('Payout calculation error:', error);
      return null;
    }
  }, [picks, playType, entryAmount]);

  // Don't render if no picks
  if (!payoutResult || picks.length === 0) {
    return null;
  }

  return (
    <div className="payout-display">
      {/* Payout Multiplier */}
      <div className="payout-multiplier">
        <span className="text-2xl font-bold text-accent1">
          {formatMultiplier(payoutResult.multiplier)}
        </span>
        <span className="text-xs text-text-muted ml-2">
          {playType === 'power' ? 'Power Play' : 'Flex Play'}
        </span>
      </div>

      {/* Potential Winnings */}
      <div className="potential-winnings mt-2">
        <div className="text-xs text-text-muted">Potential Payout</div>
        <div className="text-xl font-semibold text-text-primary">
          {formatCurrency(payoutResult.payoutAmount)}
        </div>
      </div>

      {/* Pick Breakdown */}
      <div className="pick-breakdown mt-3 text-xs">
        <div className="flex justify-between">
          <span className="text-text-muted">Picks:</span>
          <span className="text-text-primary">
            {payoutResult.activePickCount}
            {payoutResult.pushCount > 0 && (
              <span className="text-text-muted ml-1">
                ({payoutResult.originalPickCount} - {payoutResult.pushCount} push)
              </span>
            )}
          </span>
        </div>
      </div>

      {/* Description */}
      {payoutResult.pushCount > 0 && (
        <div className="mt-2 text-xs text-accent2 bg-surface p-2 rounded">
          {getPayoutDescription(payoutResult)}
        </div>
      )}
    </div>
  );
};

export default PayoutDisplay;
