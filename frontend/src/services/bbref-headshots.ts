/**
 * Basketball Reference Player Code Mapping
 * Format: {player_name}: {bbref_code}
 * 
 * Basketball Reference uses format: first 5 letters of last name + first 2 letters of first name + number
 * Example: Giannis Antetokounmpo = antetgi01 (antet + gi + 01)
 */

export const BBREF_PLAYER_CODES: Record<string, string> = {
  // Top Players
  'LeBron James': 'jamesle01',
  'Stephen Curry': 'curryst01',
  'Kevin Durant': 'duranke01',
  'Giannis Antetokounmpo': 'antetgi01',
  'Luka Dončić': 'doncilu01',
  'Luka Doncic': 'doncilu01', // Alt spelling
  'Nikola Jokić': 'jokicni01',
  'Nikola Jokic': 'jokicni01', // Alt spelling
  'Joel Embiid': 'embiijo01',
  'Jayson Tatum': 'tatumja01',
  'Damian Lillard': 'lillada01',
  'Anthony Davis': 'davisan02',
  'Jimmy Butler': 'butleji01',
  'Kawhi Leonard': 'leonaka01',
  'Paul George': 'georgpa01',
  'Kyrie Irving': 'irvinky01',
  'Devin Booker': 'bookede01',
  'Ja Morant': 'moranja01',
  'Trae Young': 'youngtr01',
  'Donovan Mitchell': 'mitchdo01',
  'Karl-Anthony Towns': 'townska01',
  'Anthony Edwards': 'edwaran01',
  'Shai Gilgeous-Alexander': 'gilgesh01',
  'Domantas Sabonis': 'sabondo01',
  'Tyrese Haliburton': 'halibty01',
  'Bam Adebayo': 'adebaba01',
  'Jaylen Brown': 'brownja02',
  'DeMar DeRozan': 'derozde01',
  'Zion Williamson': 'willizi01',
  'Paolo Banchero': 'banchpa01',
  'Franz Wagner': 'wagnefr01',
  'Cade Cunningham': 'cunniac01',
  'Scottie Barnes': 'barnesc01',
  'Jalen Brunson': 'brunsja01',
  'Julius Randle': 'randlju01',
  'Darius Garland': 'garlada01',
  'Evan Mobley': 'mobleep01',
  'Lauri Markkanen': 'markkla01',
  'De\'Aaron Fox': 'foxde01',
  'Alperen Sengun': 'sengual01',
  'Jaren Jackson Jr.': 'jacksja02',
  'Desmond Bane': 'banede01',
  'Brandon Ingram': 'ingrabr01',
  'CJ McCollum': 'mccolcj01',
  'Kristaps Porzingis': 'porzikr01',
  'Rudy Gobert': 'goberru01',
  'Mikal Bridges': 'bridgmi01',
  'OG Anunoby': 'anunoog01',
  'Jrue Holiday': 'holidjr01',
  'Tyler Herro': 'herroty01',
  'Jamal Murray': 'murreja01',
  'Michael Porter Jr.': 'portemi01',
  'Victor Wembanyama': 'wembavi01',
  'Chet Holmgren': 'holmgch01',
  'Deandre Ayton': 'aytonde01',
  'LaMelo Ball': 'ballla01',
  'Terry Rozier': 'roziete01',
  'Miles Bridges': 'bridgmi02',
  'Jalen Williams': 'willija06',
  'Josh Giddey': 'giddejo01',
  'Anfernee Simons': 'simonan01',
  'Jerami Grant': 'grantje01',
  'Pascal Siakam': 'siakapa01',
  'Myles Turner': 'turnemy01',
  'Buddy Hield': 'hieldbu01',
  'Tobias Harris': 'harrito02',
  'James Harden': 'hardeja01',
  'Russell Westbrook': 'westbru01',
  'Chris Paul': 'paulch01',
  'Klay Thompson': 'thompkl01',
  'Draymond Green': 'greendr01',
  'Fred VanVleet': 'vanvlfr01',
  'Jonas Valanciunas': 'valanjo01',
  'Clint Capela': 'capelca01',
  'Brook Lopez': 'lopezbr01',
  'Nikola Vucevic': 'vucevni01',
};

/**
 * Generate Basketball Reference player code from name
 * This is a fallback for players not in the mapping
 */
function generateBBRefCode(playerName: string): string {
  const parts = playerName.toLowerCase().replace(/[^a-z\s]/g, '').split(' ');
  
  if (parts.length < 2) {
    return '';
  }
  
  const firstName = parts[0];
  const lastName = parts[parts.length - 1];
  
  // Basketball Reference format: first 5 of last name + first 2 of first name + 01
  const lastPart = lastName.substring(0, 5).padEnd(5, lastName[0] || 'x');
  const firstPart = firstName.substring(0, 2);
  
  return `${lastPart}${firstPart}01`;
}

/**
 * Get Basketball Reference headshot URL for a player
 */
export function getBBRefHeadshotUrl(playerName: string): string {
  // Try to get from mapping first
  let code = BBREF_PLAYER_CODES[playerName];
  
  // If not found, try to generate it
  if (!code) {
    code = generateBBRefCode(playerName);
  }
  
  if (!code) {
    return ''; // Return empty if we can't generate a code
  }
  
  // Basketball Reference URL format
  return `https://www.basketball-reference.com/req/202106291/images/headshots/${code}.jpg`;
}

/**
 * Get player headshot with fallback chain
 */
export function getPlayerHeadshotUrl(playerId: string | number, playerName: string): string {
  // Priority 1: Basketball Reference
  const bbrefUrl = getBBRefHeadshotUrl(playerName);
  if (bbrefUrl) {
    return bbrefUrl;
  }
  
  // Priority 2: NBA CDN (if we have a valid player ID)
  if (playerId && playerId !== '1' && playerId !== 1) {
    return `https://cdn.nba.com/headshots/nba/latest/1040x760/${playerId}.png`;
  }
  
  // Priority 3: UI Avatars (always works)
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(playerName)}&size=100&background=10b981&color=fff&bold=true&rounded=true`;
}
