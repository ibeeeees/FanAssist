/**
 * FanAssistant Payout Calculation Engine
 * 
 * This module handles payout calculations for Power Play and Flex Play game modes
 * based on PrizePicks rules.
 */

// ============================================================================
// Types and Interfaces
// ============================================================================

export type PickStatus = 'win' | 'loss' | 'push';
export type PlayType = 'power' | 'flex';
export type PickModifier = 'demon' | 'goblin' | null;

export interface Pick {
  id: string;
  playerId: string;
  playerName: string;
  category: string;
  selection: 'more' | 'less';
  statValue: number;
  status?: PickStatus;
  modifier?: PickModifier;
}

export interface PayoutResult {
  multiplier: number;
  originalPickCount: number;
  activePickCount: number;
  winCount: number;
  lossCount: number;
  pushCount: number;
  isWinner: boolean;
  payoutAmount: number;
}

// ============================================================================
// Payout Data Structures
// ============================================================================

/**
 * Power Play Payout Multipliers
 * Key: Number of picks
 * Value: Payout multiplier
 */
const POWER_PLAY_PAYOUTS: Record<number, number> = {
  6: 37.5,
  5: 20,
  4: 10,
  3: 6,
  2: 3,
};

/**
 * Demon Multiplier Boost Table
 * Based on total number of picks in lineup (after pushes removed)
 * Demons make picks harder to win but increase payout significantly
 */
const DEMON_MULTIPLIER_BOOST: Record<number, number> = {
  2: 10,    // 2-pick with demon: up to 10x boost
  3: 25,    // 3-pick with demon: up to 25x boost
  4: 100,   // 4-pick with demon: up to 100x boost
  5: 400,   // 5-pick with demon: up to 400x boost
  6: 2000,  // 6-pick with demon: up to 2000x boost
};

/**
 * Goblin Multiplier Reduction Table
 * Goblins make picks easier to win but reduce payout
 * Values are reduction factors (multiplied against base payout)
 */
const GOBLIN_MULTIPLIER_REDUCTION: Record<number, number> = {
  2: 0.5,   // 2-pick with goblin: 50% of normal payout
  3: 0.4,   // 3-pick with goblin: 40% of normal payout
  4: 0.3,   // 4-pick with goblin: 30% of normal payout
  5: 0.25,  // 5-pick with goblin: 25% of normal payout
  6: 0.2,   // 6-pick with goblin: 20% of normal payout
};

/**
 * Flex Play Payout Multipliers
 * First key: Total number of picks
 * Second key: Number of correct picks
 * Value: Payout multiplier
 */
const FLEX_PLAY_PAYOUTS: Record<number, Record<number, number>> = {
  6: { 6: 25, 5: 2, 4: 0.4 },
  5: { 5: 10, 4: 2, 3: 0.4 },
  4: { 4: 6, 3: 1.5 },
  3: { 3: 3, 2: 1 },
};

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Filters out pushes and returns active picks
 */
function getActivePicks(picks: Pick[]): Pick[] {
  return picks.filter(pick => pick.status !== 'push');
}

/**
 * Counts picks by status
 */
function countPicksByStatus(picks: Pick[]) {
  return {
    total: picks.length,
    wins: picks.filter(p => p.status === 'win').length,
    losses: picks.filter(p => p.status === 'loss').length,
    pushes: picks.filter(p => p.status === 'push').length,
  };
}

/**
 * Applies modifiers to the base payout multiplier
 * Implements Demon and Goblin logic:
 * - Demons: Boost multiplier significantly (up to 2000x for 6-pick)
 * - Goblins: Reduce multiplier proportionally
 * - Mixed lineups: Apply both modifiers in sequence
 */
function applyModifiers(
  baseMultiplier: number,
  picks: Pick[]
): number {
  // If base multiplier is 0 (losing lineup), no modifiers apply
  if (baseMultiplier === 0) {
    return 0;
  }

  const demonPicks = picks.filter(p => p.modifier === 'demon');
  const goblinPicks = picks.filter(p => p.modifier === 'goblin');
  const totalPicks = picks.length;
  
  let modifiedMultiplier = baseMultiplier;
  
  // Apply demon boost
  // Each demon in the lineup adds to the multiplier boost
  // The boost scales with total number of picks
  if (demonPicks.length > 0) {
    const boostPerDemon = DEMON_MULTIPLIER_BOOST[totalPicks] ?? 1;
    // For multiple demons, boost stacks additively
    const totalDemonBoost = boostPerDemon * demonPicks.length;
    modifiedMultiplier = baseMultiplier + totalDemonBoost;
  }
  
  // Apply goblin reduction
  // Each goblin reduces the multiplier
  if (goblinPicks.length > 0) {
    const reductionFactor = GOBLIN_MULTIPLIER_REDUCTION[totalPicks] ?? 1;
    // For multiple goblins, reduction compounds multiplicatively
    const totalReduction = Math.pow(reductionFactor, goblinPicks.length);
    modifiedMultiplier = modifiedMultiplier * totalReduction;
  }
  
  // Ensure multiplier doesn't go below 0
  return Math.max(0, modifiedMultiplier);
}

// ============================================================================
// Core Payout Calculation Logic
// ============================================================================

/**
 * Calculate Power Play payout
 * 
 * Power Play is all-or-nothing:
 * - Any loss = 0x payout
 * - Pushes are removed, payout adjusts to next tier down
 * - All wins = payout based on remaining pick count
 */
function calculatePowerPlayPayout(picks: Pick[]): number {
  // Remove pushes - they don't count
  const activePicks = getActivePicks(picks);
  const activeCount = activePicks.length;
  
  // If no active picks remain (all were pushes), no payout
  if (activeCount === 0) {
    return 0;
  }
  
  // Check if any pick is a loss - Power Play is all-or-nothing
  const hasLoss = activePicks.some(pick => pick.status === 'loss');
  if (hasLoss) {
    return 0;
  }
  
  // All remaining picks must be wins
  // Look up payout in the Power Play table
  const payout = POWER_PLAY_PAYOUTS[activeCount];
  
  // If no payout defined for this count (e.g., 1 pick), return 0
  return payout ?? 0;
}

/**
 * Calculate Flex Play payout
 * 
 * Flex Play allows some losses:
 * - Pushes are removed, entry graded as smaller lineup
 * - Payout based on active picks and number of wins
 */
function calculateFlexPlayPayout(picks: Pick[]): number {
  // Remove pushes - grade as a smaller entry
  const activePicks = getActivePicks(picks);
  const activeCount = activePicks.length;
  
  // If no active picks remain (all were pushes), no payout
  if (activeCount < 2) {
    return 0;
  }
  
  // Count the number of wins
  const winCount = activePicks.filter(pick => pick.status === 'win').length;
  
  // Get the payout map for the active pick count
  const payoutMap = FLEX_PLAY_PAYOUTS[activeCount];
  
  // If no payout map exists for this count, no payout
  if (!payoutMap) {
    return 0;
  }
  
  // Look up the payout for the number of wins
  const payout = payoutMap[winCount];
  
  // If no payout defined (e.g., too few wins), return 0
  return payout ?? 0;
}

// ============================================================================
// Main Payout Calculator
// ============================================================================

/**
 * Main payout calculation function
 * 
 * @param picks - Array of pick objects with status
 * @param playType - 'power' or 'flex'
 * @param entryAmount - Amount wagered (default 1)
 * @returns PayoutResult with detailed breakdown
 */
export function calculatePayout(
  picks: Pick[],
  playType: PlayType,
  entryAmount: number = 1
): PayoutResult {
  // Validate input
  if (!picks || picks.length === 0) {
    throw new Error('Picks array cannot be empty');
  }
  
  if (!['power', 'flex'].includes(playType)) {
    throw new Error('Play type must be "power" or "flex"');
  }
  
  // Count picks by status
  const counts = countPicksByStatus(picks);
  const activePicks = getActivePicks(picks);
  
  // Calculate base multiplier based on play type
  let baseMultiplier: number;
  
  if (playType === 'power') {
    baseMultiplier = calculatePowerPlayPayout(picks);
  } else {
    baseMultiplier = calculateFlexPlayPayout(picks);
  }
  
  // Apply modifiers (Demon/Goblin)
  const finalMultiplier = applyModifiers(baseMultiplier, activePicks);
  
  // Calculate final payout amount
  const payoutAmount = entryAmount * finalMultiplier;
  
  // Return detailed result
  return {
    multiplier: finalMultiplier,
    originalPickCount: counts.total,
    activePickCount: activePicks.length,
    winCount: counts.wins,
    lossCount: counts.losses,
    pushCount: counts.pushes,
    isWinner: finalMultiplier > 0,
    payoutAmount: payoutAmount,
  };
}

// ============================================================================
// Payout Calculator Class (Alternative OOP Approach)
// ============================================================================

/**
 * Object-oriented payout calculator for easier extensibility
 */
export class PayoutCalculator {
  private picks: Pick[];
  private playType: PlayType;
  private entryAmount: number;
  
  constructor(picks: Pick[], playType: PlayType, entryAmount: number = 1) {
    this.picks = picks;
    this.playType = playType;
    this.entryAmount = entryAmount;
  }
  
  /**
   * Calculate and return payout result
   */
  calculate(): PayoutResult {
    return calculatePayout(this.picks, this.playType, this.entryAmount);
  }
  
  /**
   * Get active picks (excluding pushes)
   */
  getActivePicks(): Pick[] {
    return getActivePicks(this.picks);
  }
  
  /**
   * Get pick counts by status
   */
  getCounts() {
    return countPicksByStatus(this.picks);
  }
  
  /**
   * Check if entry is a winner
   */
  isWinner(): boolean {
    const result = this.calculate();
    return result.isWinner;
  }
  
  /**
   * Get payout multiplier only
   */
  getMultiplier(): number {
    const result = this.calculate();
    return result.multiplier;
  }
  
  /**
   * Get total payout amount
   */
  getPayoutAmount(): number {
    const result = this.calculate();
    return result.payoutAmount;
  }
}

// ============================================================================
// Utility Functions for Display
// ============================================================================

/**
 * Format payout multiplier for display
 */
export function formatMultiplier(multiplier: number): string {
  return `${multiplier}x`;
}

/**
 * Format payout amount as currency
 */
export function formatCurrency(amount: number): string {
  return `$${amount.toFixed(2)}`;
}

/**
 * Get payout description for UI
 */
export function getPayoutDescription(result: PayoutResult): string {
  if (result.pushCount > 0) {
    return `${result.pushCount} push${result.pushCount > 1 ? 'es' : ''} removed. ` +
           `Entry graded as ${result.activePickCount}-pick with ${result.winCount} win${result.winCount !== 1 ? 's' : ''}.`;
  }
  
  if (result.isWinner) {
    return `${result.winCount}/${result.activePickCount} correct picks!`;
  }
  
  return `${result.lossCount} loss${result.lossCount !== 1 ? 'es' : ''}. Better luck next time!`;
}

// ============================================================================
// Export Default
// ============================================================================

export default {
  calculatePayout,
  PayoutCalculator,
  formatMultiplier,
  formatCurrency,
  getPayoutDescription,
};
