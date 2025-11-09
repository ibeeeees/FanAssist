/**
 * Result Evaluator
 * 
 * Evaluates picks after games complete to determine win/loss/push status
 */

import type { SelectedPlayer } from '../types';
import type { Pick, PickStatus } from './payoutCalculator';

// ============================================================================
// Types
// ============================================================================

interface GameResult {
  playerId: string;
  playerName: string;
  category: string;
  actualValue: number;
  gameCompleted: boolean;
}

interface EvaluationResult {
  playerId: string;
  playerName: string;
  category: string;
  selection: 'more' | 'less';
  projectedValue: number;
  actualValue: number;
  status: PickStatus;
  difference: number;
}

// ============================================================================
// Core Evaluation Logic
// ============================================================================

/**
 * Evaluates a single pick to determine if it's a win, loss, or push
 * 
 * Rules:
 * - Push: Actual value EXACTLY equals projected value
 * - Win (More): Actual value > projected value
 * - Win (Less): Actual value < projected value
 * - Loss: Opposite of win conditions
 */
export function evaluatePick(
  pick: SelectedPlayer,
  actualValue: number
): PickStatus {
  const { selection, statValue: projectedValue } = pick;

  // Push: Exact match (tie)
  if (actualValue === projectedValue) {
    return 'push';
  }

  // More selection
  if (selection === 'more') {
    return actualValue > projectedValue ? 'win' : 'loss';
  }

  // Less selection
  return actualValue < projectedValue ? 'win' : 'loss';
}

/**
 * Evaluates all picks in a lineup
 */
export function evaluateLineup(
  picks: SelectedPlayer[],
  gameResults: GameResult[]
): EvaluationResult[] {
  return picks.map(pick => {
    // Find matching game result
    const result = gameResults.find(
      r => r.playerId === pick.playerId && r.category === pick.category
    );

    if (!result) {
      throw new Error(
        `No game result found for ${pick.playerName} - ${pick.category}`
      );
    }

    if (!result.gameCompleted) {
      throw new Error(
        `Game not completed for ${pick.playerName}`
      );
    }

    // Evaluate the pick
    const status = evaluatePick(pick, result.actualValue);
    const difference = result.actualValue - pick.statValue;

    return {
      playerId: pick.playerId,
      playerName: pick.playerName,
      category: pick.category,
      selection: pick.selection,
      projectedValue: pick.statValue,
      actualValue: result.actualValue,
      status,
      difference,
    };
  });
}

/**
 * Converts SelectedPlayer to Pick with evaluated status
 */
export function convertToPicksWithStatus(
  players: SelectedPlayer[],
  gameResults: GameResult[]
): Pick[] {
  const evaluations = evaluateLineup(players, gameResults);

  return players.map((player, index) => ({
    id: player.playerId,
    playerId: player.playerId,
    playerName: player.playerName,
    category: player.category,
    selection: player.selection,
    statValue: player.statValue,
    status: evaluations[index].status,
    modifier: player.modifier || null,
  }));
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Formats the result for display
 */
export function formatEvaluationResult(result: EvaluationResult): string {
  const { playerName, category, selection, projectedValue, actualValue, status } = result;
  
  const selectionText = selection.toUpperCase();
  const statusEmoji = status === 'win' ? '✅' : status === 'loss' ? '❌' : '➖';
  
  return `${statusEmoji} ${playerName} - ${category} ${selectionText} ${projectedValue} (Actual: ${actualValue})`;
}

/**
 * Gets summary statistics for a lineup evaluation
 */
export function getLineupSummary(evaluations: EvaluationResult[]) {
  const wins = evaluations.filter(e => e.status === 'win').length;
  const losses = evaluations.filter(e => e.status === 'loss').length;
  const pushes = evaluations.filter(e => e.status === 'push').length;

  return {
    total: evaluations.length,
    wins,
    losses,
    pushes,
    winPercentage: (wins / evaluations.length) * 100,
  };
}

/**
 * Checks if a game is completed (helper for API integration)
 */
export function isGameCompleted(gameId: string): Promise<boolean> {
  // TODO: Implement actual API call to check game status
  // This would call your NBA stats service
  return Promise.resolve(true);
}

/**
 * Fetches actual stats for a player from a completed game
 */
export async function fetchPlayerGameStats(
  playerId: string,
  gameId: string,
  category: string
): Promise<number> {
  // TODO: Implement actual API call to fetch player stats
  // This would call your NBA stats service
  
  // Example implementation:
  // const response = await fetch(`/api/player-stats/${playerId}/${gameId}`);
  // const data = await response.json();
  // return data.stats[category];
  
  // Placeholder return
  return 0;
}

/**
 * Batch fetch game results for all picks
 */
export async function fetchGameResultsForLineup(
  picks: SelectedPlayer[]
): Promise<GameResult[]> {
  // TODO: Implement batch API call
  // This would fetch all game results in one request
  
  // Example implementation:
  // const playerIds = picks.map(p => p.playerId);
  // const response = await fetch('/api/game-results', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ playerIds }),
  // });
  // return await response.json();
  
  // Placeholder return
  return [];
}

// ============================================================================
// Example Usage
// ============================================================================

/**
 * Complete workflow: Evaluate lineup and calculate payout
 */
export async function evaluateAndCalculatePayout(
  lineup: {
    picks: SelectedPlayer[];
    playType: 'power' | 'flex';
    entryAmount: number;
  }
) {
  // 1. Fetch game results
  const gameResults = await fetchGameResultsForLineup(lineup.picks);

  // 2. Evaluate picks
  const evaluations = evaluateLineup(lineup.picks, gameResults);

  // 3. Convert to Pick objects with status
  const picksWithStatus = convertToPicksWithStatus(lineup.picks, gameResults);

  // 4. Calculate payout (import from payoutCalculator)
  // const payoutResult = calculatePayout(picksWithStatus, lineup.playType, lineup.entryAmount);

  // 5. Return combined result
  return {
    evaluations,
    summary: getLineupSummary(evaluations),
    // payout: payoutResult,
  };
}

// ============================================================================
// Export
// ============================================================================

export default {
  evaluatePick,
  evaluateLineup,
  convertToPicksWithStatus,
  formatEvaluationResult,
  getLineupSummary,
  fetchGameResultsForLineup,
  evaluateAndCalculatePayout,
};
