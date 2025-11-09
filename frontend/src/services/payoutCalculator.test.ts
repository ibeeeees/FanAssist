/**
 * Payout Calculator Test Examples
 * 
 * This file demonstrates the payout calculation logic with various scenarios
 * matching the PrizePicks rules.
 */

import {
  calculatePayout,
  PayoutCalculator,
  formatMultiplier,
  formatCurrency,
  getPayoutDescription,
  type Pick,
  type PayoutResult,
} from './payoutCalculator';

// ============================================================================
// Test Scenarios
// ============================================================================

console.log('='.repeat(70));
console.log('FANASSISTANT PAYOUT CALCULATOR - TEST SCENARIOS');
console.log('='.repeat(70));

// ----------------------------------------------------------------------------
// POWER PLAY TESTS
// ----------------------------------------------------------------------------

console.log('\n📊 POWER PLAY TESTS\n');

// Test 1: 6-pick Power Play - All Wins
console.log('Test 1: 6-pick Power Play - All Wins');
const powerPlay6AllWins: Pick[] = [
  { id: '1', playerId: 'p1', playerName: 'LeBron James', category: 'Points', selection: 'more', statValue: 25.5, status: 'win' },
  { id: '2', playerId: 'p2', playerName: 'Stephen Curry', category: 'Points', selection: 'more', statValue: 28.5, status: 'win' },
  { id: '3', playerId: 'p3', playerName: 'Kevin Durant', category: 'Points', selection: 'more', statValue: 27.5, status: 'win' },
  { id: '4', playerId: 'p4', playerName: 'Giannis', category: 'Rebounds', selection: 'more', statValue: 11.5, status: 'win' },
  { id: '5', playerId: 'p5', playerName: 'Luka Doncic', category: 'Assists', selection: 'more', statValue: 8.5, status: 'win' },
  { id: '6', playerId: 'p6', playerName: 'Nikola Jokic', category: 'Points', selection: 'more', statValue: 26.5, status: 'win' },
];

let result = calculatePayout(powerPlay6AllWins, 'power', 10);
console.log(`   Entry: $${10.00}`);
console.log(`   Result: ${result.winCount}/${result.activePickCount} wins`);
console.log(`   Multiplier: ${formatMultiplier(result.multiplier)}`);
console.log(`   Payout: ${formatCurrency(result.payoutAmount)}`);
console.log(`   Description: ${getPayoutDescription(result)}`);
console.log(`   ✅ Expected: 37.5x = $375.00\n`);

// Test 2: 6-pick Power Play - 1 Loss
console.log('Test 2: 6-pick Power Play - 1 Loss (Any loss = 0x)');
const powerPlay6OneLoss: Pick[] = [
  { id: '1', playerId: 'p1', playerName: 'LeBron James', category: 'Points', selection: 'more', statValue: 25.5, status: 'win' },
  { id: '2', playerId: 'p2', playerName: 'Stephen Curry', category: 'Points', selection: 'more', statValue: 28.5, status: 'win' },
  { id: '3', playerId: 'p3', playerName: 'Kevin Durant', category: 'Points', selection: 'more', statValue: 27.5, status: 'loss' },
  { id: '4', playerId: 'p4', playerName: 'Giannis', category: 'Rebounds', selection: 'more', statValue: 11.5, status: 'win' },
  { id: '5', playerId: 'p5', playerName: 'Luka Doncic', category: 'Assists', selection: 'more', statValue: 8.5, status: 'win' },
  { id: '6', playerId: 'p6', playerName: 'Nikola Jokic', category: 'Points', selection: 'more', statValue: 26.5, status: 'win' },
];

result = calculatePayout(powerPlay6OneLoss, 'power', 10);
console.log(`   Entry: $${10.00}`);
console.log(`   Result: ${result.winCount} wins, ${result.lossCount} loss`);
console.log(`   Multiplier: ${formatMultiplier(result.multiplier)}`);
console.log(`   Payout: ${formatCurrency(result.payoutAmount)}`);
console.log(`   Description: ${getPayoutDescription(result)}`);
console.log(`   ✅ Expected: 0x = $0.00\n`);

// Test 3: 6-pick Power Play - 1 Push (becomes 5-pick)
console.log('Test 3: 6-pick Power Play - 1 Push (graded as 5-pick, all wins)');
const powerPlay6OnePush: Pick[] = [
  { id: '1', playerId: 'p1', playerName: 'LeBron James', category: 'Points', selection: 'more', statValue: 25.5, status: 'win' },
  { id: '2', playerId: 'p2', playerName: 'Stephen Curry', category: 'Points', selection: 'more', statValue: 28.5, status: 'win' },
  { id: '3', playerId: 'p3', playerName: 'Kevin Durant', category: 'Points', selection: 'more', statValue: 27.5, status: 'push' },
  { id: '4', playerId: 'p4', playerName: 'Giannis', category: 'Rebounds', selection: 'more', statValue: 11.5, status: 'win' },
  { id: '5', playerId: 'p5', playerName: 'Luka Doncic', category: 'Assists', selection: 'more', statValue: 8.5, status: 'win' },
  { id: '6', playerId: 'p6', playerName: 'Nikola Jokic', category: 'Points', selection: 'more', statValue: 26.5, status: 'win' },
];

result = calculatePayout(powerPlay6OnePush, 'power', 10);
console.log(`   Entry: $${10.00}`);
console.log(`   Original Picks: ${result.originalPickCount}`);
console.log(`   Active Picks: ${result.activePickCount} (${result.pushCount} push removed)`);
console.log(`   Result: ${result.winCount}/${result.activePickCount} wins`);
console.log(`   Multiplier: ${formatMultiplier(result.multiplier)}`);
console.log(`   Payout: ${formatCurrency(result.payoutAmount)}`);
console.log(`   Description: ${getPayoutDescription(result)}`);
console.log(`   ✅ Expected: 20x = $200.00 (5-pick payout)\n`);

// Test 4: 2-pick Power Play - 1 Push (becomes 1-pick = no payout)
console.log('Test 4: 2-pick Power Play - 1 Push (becomes 1-pick, no payout)');
const powerPlay2OnePush: Pick[] = [
  { id: '1', playerId: 'p1', playerName: 'LeBron James', category: 'Points', selection: 'more', statValue: 25.5, status: 'win' },
  { id: '2', playerId: 'p2', playerName: 'Stephen Curry', category: 'Points', selection: 'more', statValue: 28.5, status: 'push' },
];

result = calculatePayout(powerPlay2OnePush, 'power', 10);
console.log(`   Entry: $${10.00}`);
console.log(`   Original Picks: ${result.originalPickCount}`);
console.log(`   Active Picks: ${result.activePickCount} (${result.pushCount} push removed)`);
console.log(`   Result: ${result.winCount}/${result.activePickCount} wins`);
console.log(`   Multiplier: ${formatMultiplier(result.multiplier)}`);
console.log(`   Payout: ${formatCurrency(result.payoutAmount)}`);
console.log(`   ✅ Expected: 0x = $0.00 (1-pick has no payout)\n`);

// ----------------------------------------------------------------------------
// FLEX PLAY TESTS
// ----------------------------------------------------------------------------

console.log('\n📊 FLEX PLAY TESTS\n');

// Test 5: 6-pick Flex Play - All Wins
console.log('Test 5: 6-pick Flex Play - 6/6 Wins');
const flexPlay6AllWins: Pick[] = [
  { id: '1', playerId: 'p1', playerName: 'LeBron James', category: 'Points', selection: 'more', statValue: 25.5, status: 'win' },
  { id: '2', playerId: 'p2', playerName: 'Stephen Curry', category: 'Points', selection: 'more', statValue: 28.5, status: 'win' },
  { id: '3', playerId: 'p3', playerName: 'Kevin Durant', category: 'Points', selection: 'more', statValue: 27.5, status: 'win' },
  { id: '4', playerId: 'p4', playerName: 'Giannis', category: 'Rebounds', selection: 'more', statValue: 11.5, status: 'win' },
  { id: '5', playerId: 'p5', playerName: 'Luka Doncic', category: 'Assists', selection: 'more', statValue: 8.5, status: 'win' },
  { id: '6', playerId: 'p6', playerName: 'Nikola Jokic', category: 'Points', selection: 'more', statValue: 26.5, status: 'win' },
];

result = calculatePayout(flexPlay6AllWins, 'flex', 10);
console.log(`   Entry: $${10.00}`);
console.log(`   Result: ${result.winCount}/${result.activePickCount} wins`);
console.log(`   Multiplier: ${formatMultiplier(result.multiplier)}`);
console.log(`   Payout: ${formatCurrency(result.payoutAmount)}`);
console.log(`   Description: ${getPayoutDescription(result)}`);
console.log(`   ✅ Expected: 25x = $250.00\n`);

// Test 6: 6-pick Flex Play - 5/6 Wins
console.log('Test 6: 6-pick Flex Play - 5/6 Wins (1 loss)');
const flexPlay6FiveWins: Pick[] = [
  { id: '1', playerId: 'p1', playerName: 'LeBron James', category: 'Points', selection: 'more', statValue: 25.5, status: 'win' },
  { id: '2', playerId: 'p2', playerName: 'Stephen Curry', category: 'Points', selection: 'more', statValue: 28.5, status: 'win' },
  { id: '3', playerId: 'p3', playerName: 'Kevin Durant', category: 'Points', selection: 'more', statValue: 27.5, status: 'loss' },
  { id: '4', playerId: 'p4', playerName: 'Giannis', category: 'Rebounds', selection: 'more', statValue: 11.5, status: 'win' },
  { id: '5', playerId: 'p5', playerName: 'Luka Doncic', category: 'Assists', selection: 'more', statValue: 8.5, status: 'win' },
  { id: '6', playerId: 'p6', playerName: 'Nikola Jokic', category: 'Points', selection: 'more', statValue: 26.5, status: 'win' },
];

result = calculatePayout(flexPlay6FiveWins, 'flex', 10);
console.log(`   Entry: $${10.00}`);
console.log(`   Result: ${result.winCount}/${result.activePickCount} wins, ${result.lossCount} loss`);
console.log(`   Multiplier: ${formatMultiplier(result.multiplier)}`);
console.log(`   Payout: ${formatCurrency(result.payoutAmount)}`);
console.log(`   Description: ${getPayoutDescription(result)}`);
console.log(`   ✅ Expected: 2x = $20.00\n`);

// Test 7: 6-pick Flex Play - 4/6 Wins
console.log('Test 7: 6-pick Flex Play - 4/6 Wins (2 losses)');
const flexPlay6FourWins: Pick[] = [
  { id: '1', playerId: 'p1', playerName: 'LeBron James', category: 'Points', selection: 'more', statValue: 25.5, status: 'win' },
  { id: '2', playerId: 'p2', playerName: 'Stephen Curry', category: 'Points', selection: 'more', statValue: 28.5, status: 'win' },
  { id: '3', playerId: 'p3', playerName: 'Kevin Durant', category: 'Points', selection: 'more', statValue: 27.5, status: 'loss' },
  { id: '4', playerId: 'p4', playerName: 'Giannis', category: 'Rebounds', selection: 'more', statValue: 11.5, status: 'win' },
  { id: '5', playerId: 'p5', playerName: 'Luka Doncic', category: 'Assists', selection: 'more', statValue: 8.5, status: 'loss' },
  { id: '6', playerId: 'p6', playerName: 'Nikola Jokic', category: 'Points', selection: 'more', statValue: 26.5, status: 'win' },
];

result = calculatePayout(flexPlay6FourWins, 'flex', 10);
console.log(`   Entry: $${10.00}`);
console.log(`   Result: ${result.winCount}/${result.activePickCount} wins, ${result.lossCount} losses`);
console.log(`   Multiplier: ${formatMultiplier(result.multiplier)}`);
console.log(`   Payout: ${formatCurrency(result.payoutAmount)}`);
console.log(`   Description: ${getPayoutDescription(result)}`);
console.log(`   ✅ Expected: 0.4x = $4.00\n`);

// Test 8: 6-pick Flex Play - 1 Push, 4 Wins, 1 Loss (becomes 5-pick with 4/5)
console.log('Test 8: 6-pick Flex Play - 1 Push, 4 Wins, 1 Loss');
console.log('   (Graded as 5-pick with 4/5 correct)');
const flexPlay6OnePushFourWins: Pick[] = [
  { id: '1', playerId: 'p1', playerName: 'LeBron James', category: 'Points', selection: 'more', statValue: 25.5, status: 'win' },
  { id: '2', playerId: 'p2', playerName: 'Stephen Curry', category: 'Points', selection: 'more', statValue: 28.5, status: 'win' },
  { id: '3', playerId: 'p3', playerName: 'Kevin Durant', category: 'Points', selection: 'more', statValue: 27.5, status: 'push' },
  { id: '4', playerId: 'p4', playerName: 'Giannis', category: 'Rebounds', selection: 'more', statValue: 11.5, status: 'win' },
  { id: '5', playerId: 'p5', playerName: 'Luka Doncic', category: 'Assists', selection: 'more', statValue: 8.5, status: 'loss' },
  { id: '6', playerId: 'p6', playerName: 'Nikola Jokic', category: 'Points', selection: 'more', statValue: 26.5, status: 'win' },
];

result = calculatePayout(flexPlay6OnePushFourWins, 'flex', 10);
console.log(`   Entry: $${10.00}`);
console.log(`   Original Picks: ${result.originalPickCount}`);
console.log(`   Active Picks: ${result.activePickCount} (${result.pushCount} push removed)`);
console.log(`   Result: ${result.winCount}/${result.activePickCount} wins, ${result.lossCount} loss`);
console.log(`   Multiplier: ${formatMultiplier(result.multiplier)}`);
console.log(`   Payout: ${formatCurrency(result.payoutAmount)}`);
console.log(`   Description: ${getPayoutDescription(result)}`);
console.log(`   ✅ Expected: 2x = $20.00 (5-pick, 4/5 correct)\n`);

// Test 9: 5-pick Flex Play - 2 Pushes, 3 Wins (becomes 3-pick with 3/3)
console.log('Test 9: 5-pick Flex Play - 2 Pushes, 3 Wins');
console.log('   (Graded as 3-pick with 3/3 correct)');
const flexPlay5TwoPushesThreeWins: Pick[] = [
  { id: '1', playerId: 'p1', playerName: 'LeBron James', category: 'Points', selection: 'more', statValue: 25.5, status: 'win' },
  { id: '2', playerId: 'p2', playerName: 'Stephen Curry', category: 'Points', selection: 'more', statValue: 28.5, status: 'push' },
  { id: '3', playerId: 'p3', playerName: 'Kevin Durant', category: 'Points', selection: 'more', statValue: 27.5, status: 'win' },
  { id: '4', playerId: 'p4', playerName: 'Giannis', category: 'Rebounds', selection: 'more', statValue: 11.5, status: 'push' },
  { id: '5', playerId: 'p5', playerName: 'Luka Doncic', category: 'Assists', selection: 'more', statValue: 8.5, status: 'win' },
];

result = calculatePayout(flexPlay5TwoPushesThreeWins, 'flex', 10);
console.log(`   Entry: $${10.00}`);
console.log(`   Original Picks: ${result.originalPickCount}`);
console.log(`   Active Picks: ${result.activePickCount} (${result.pushCount} pushes removed)`);
console.log(`   Result: ${result.winCount}/${result.activePickCount} wins`);
console.log(`   Multiplier: ${formatMultiplier(result.multiplier)}`);
console.log(`   Payout: ${formatCurrency(result.payoutAmount)}`);
console.log(`   Description: ${getPayoutDescription(result)}`);
console.log(`   ✅ Expected: 3x = $30.00 (3-pick, 3/3 correct)\n`);

// Test 10: 6-pick Flex Play - 3 Wins, 3 Losses (no payout)
console.log('Test 10: 6-pick Flex Play - 3/6 Wins (too few wins)');
const flexPlay6ThreeWins: Pick[] = [
  { id: '1', playerId: 'p1', playerName: 'LeBron James', category: 'Points', selection: 'more', statValue: 25.5, status: 'win' },
  { id: '2', playerId: 'p2', playerName: 'Stephen Curry', category: 'Points', selection: 'more', statValue: 28.5, status: 'loss' },
  { id: '3', playerId: 'p3', playerName: 'Kevin Durant', category: 'Points', selection: 'more', statValue: 27.5, status: 'win' },
  { id: '4', playerId: 'p4', playerName: 'Giannis', category: 'Rebounds', selection: 'more', statValue: 11.5, status: 'loss' },
  { id: '5', playerId: 'p5', playerName: 'Luka Doncic', category: 'Assists', selection: 'more', statValue: 8.5, status: 'loss' },
  { id: '6', playerId: 'p6', playerName: 'Nikola Jokic', category: 'Points', selection: 'more', statValue: 26.5, status: 'win' },
];

result = calculatePayout(flexPlay6ThreeWins, 'flex', 10);
console.log(`   Entry: $${10.00}`);
console.log(`   Result: ${result.winCount}/${result.activePickCount} wins, ${result.lossCount} losses`);
console.log(`   Multiplier: ${formatMultiplier(result.multiplier)}`);
console.log(`   Payout: ${formatCurrency(result.payoutAmount)}`);
console.log(`   Description: ${getPayoutDescription(result)}`);
console.log(`   ✅ Expected: 0x = $0.00 (need at least 4/6)\n`);

// ----------------------------------------------------------------------------
// USING THE CLASS APPROACH
// ----------------------------------------------------------------------------

console.log('\n📊 USING PayoutCalculator CLASS\n');

console.log('Test 11: Using OOP approach with PayoutCalculator class');
const picks: Pick[] = [
  { id: '1', playerId: 'p1', playerName: 'LeBron James', category: 'Points', selection: 'more', statValue: 25.5, status: 'win' },
  { id: '2', playerId: 'p2', playerName: 'Stephen Curry', category: 'Points', selection: 'more', statValue: 28.5, status: 'win' },
  { id: '3', playerId: 'p3', playerName: 'Kevin Durant', category: 'Points', selection: 'more', statValue: 27.5, status: 'win' },
  { id: '4', playerId: 'p4', playerName: 'Giannis', category: 'Rebounds', selection: 'more', statValue: 11.5, status: 'win' },
];

const calculator = new PayoutCalculator(picks, 'power', 10);

console.log(`   Entry: $10.00`);
console.log(`   Play Type: Power Play`);
console.log(`   Pick Count: ${calculator.getCounts().total}`);
console.log(`   Is Winner: ${calculator.isWinner()}`);
console.log(`   Multiplier: ${formatMultiplier(calculator.getMultiplier())}`);
console.log(`   Payout: ${formatCurrency(calculator.getPayoutAmount())}`);
console.log(`   ✅ Expected: 10x = $100.00 (4-pick Power Play)\n`);

console.log('='.repeat(70));
console.log('ALL TESTS COMPLETE');
console.log('='.repeat(70));
