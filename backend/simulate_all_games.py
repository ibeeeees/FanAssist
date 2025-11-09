#!/usr/bin/env python3
"""
Simulate ALL players for ALL games today and tomorrow
Gets projections for every player on every team
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from datetime import datetime
from app.services.schedule import schedule_service
from app.services.nba_stats import nba_stats_service
from app.services.game_simulator import game_simulator
import json

async def simulate_player(player_name: str, player_id: int, opponent: str, is_home: bool, num_sims: int = 50):
    """Simulate a single player with robust error handling"""
    try:
        # Get player info with timeout handling
        try:
            player_info = await nba_stats_service.get_player_info(player_name)
            if not player_info:
                return None
        except Exception as e:
            if "timed out" in str(e).lower() or "timeout" in str(e).lower():
                print(f" ⏱️ TIMEOUT")
                return None
            raise
        
        # Get season averages with timeout handling
        try:
            season_avg = await nba_stats_service.get_player_season_averages(player_id)
            if not season_avg:
                return None
        except Exception as e:
            if "timed out" in str(e).lower() or "timeout" in str(e).lower():
                print(f" ⏱️ TIMEOUT")
                return None
            raise
        
        # Check for invalid season averages (rookies, injured players, etc.)
        if season_avg.points_per_game == 0 and season_avg.rebounds_per_game == 0 and season_avg.assists_per_game == 0:
            return None  # Skip players with no stats
        
        # Get recent games (optional, don't fail if timeout)
        recent_games = []
        try:
            recent_games = await nba_stats_service.get_player_game_log(player_id, last_n_games=5)
            if not recent_games:
                recent_games = []
        except Exception:
            recent_games = []  # Continue without recent games
        
        # Run simulation
        simulations = game_simulator.simulate_multiple_games(
            player_info=player_info,
            season_averages=season_avg,
            recent_games=recent_games,
            opponent=opponent,
            is_home=is_home,
            num_simulations=num_sims
        )
        
        if not simulations:
            return None
        
        # Calculate averages - access as objects, not dicts
        avg_stats = {
            'points': round(sum(s.points or 0 for s in simulations) / len(simulations), 2),
            'rebounds': round(sum(s.rebounds or 0 for s in simulations) / len(simulations), 2),
            'assists': round(sum(s.assists or 0 for s in simulations) / len(simulations), 2),
            'steals': round(sum(s.steals or 0 for s in simulations) / len(simulations), 2),
            'blocks': round(sum(s.blocks or 0 for s in simulations) / len(simulations), 2),
            'turnovers': round(sum(s.turnovers or 0 for s in simulations) / len(simulations), 2),
            'three_pointers_made': round(sum(s.three_pointers_made or 0 for s in simulations) / len(simulations), 2),
        }
        
        return {
            'player_name': player_name,
            'player_id': player_id,
            'projected_stats': avg_stats,
            'season_averages': {
                'points': season_avg.points_per_game,
                'rebounds': season_avg.rebounds_per_game,
                'assists': season_avg.assists_per_game,
                'steals': season_avg.steals_per_game,
                'blocks': season_avg.blocks_per_game
            },
            'status': 'success'
        }
    except Exception as e:
        error_msg = str(e)[:100]
        if "timed out" in error_msg.lower() or "timeout" in error_msg.lower():
            print(f" ⏱️ TIMEOUT")
        else:
            print(f" ❌ {error_msg}")
        return None

async def simulate_game(game: dict, num_sims: int = 30):
    """Simulate all players in a game with parallel processing"""
    print(f"\n{'='*80}")
    print(f"🏀 {game['matchup']} - {game['game_status']}")
    print(f"{'='*80}")
    
    # Get rosters
    print(f"\n📋 Getting rosters...")
    home_roster = schedule_service.get_team_roster(game['home_team_id'])
    away_roster = schedule_service.get_team_roster(game['away_team_id'])
    
    print(f"   Home ({game['home_team']}): {len(home_roster)} players")
    print(f"   Away ({game['away_team']}): {len(away_roster)} players")
    
    # Simulate all home team players IN PARALLEL (batches of 3 for stability)
    print(f"\n🔄 Simulating {game['home_team']} players...")
    home_simulations = []
    batch_size = 3
    
    for batch_start in range(0, len(home_roster), batch_size):
        batch = home_roster[batch_start:batch_start + batch_size]
        tasks = []
        
        for player in batch:
            task = simulate_player(
                player['player_name'],
                player['player_id'],
                game['away_team'],
                True,
                num_sims
            )
            tasks.append(task)
        
        # Run batch in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, (player, result) in enumerate(zip(batch, results), start=batch_start + 1):
            print(f"   {i}/{len(home_roster)} {player['player_name']}...", end='', flush=True)
            if isinstance(result, Exception):
                print(f" ❌ {str(result)[:50]}")
            elif result and result.get('status') == 'success':
                stats = result['projected_stats']
                print(f" ✅ {stats['points']} PTS | {stats['rebounds']} REB | {stats['assists']} AST | {stats['three_pointers_made']} 3PM | {stats['steals']} STL | {stats['blocks']} BLK")
                home_simulations.append(result)
            else:
                print()
        
        # Small delay between batches to avoid overwhelming API
        if batch_start + batch_size < len(home_roster):
            await asyncio.sleep(0.5)
    
    # Simulate all away team players IN PARALLEL (batches of 3 for stability)
    print(f"\n🔄 Simulating {game['away_team']} players...")
    away_simulations = []
    
    for batch_start in range(0, len(away_roster), batch_size):
        batch = away_roster[batch_start:batch_start + batch_size]
        tasks = []
        
        for player in batch:
            task = simulate_player(
                player['player_name'],
                player['player_id'],
                game['home_team'],
                False,
                num_sims
            )
            tasks.append(task)
        
        # Run batch in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, (player, result) in enumerate(zip(batch, results), start=batch_start + 1):
            print(f"   {i}/{len(away_roster)} {player['player_name']}...", end='', flush=True)
            if isinstance(result, Exception):
                print(f" ❌ {str(result)[:50]}")
            elif result and result.get('status') == 'success':
                stats = result['projected_stats']
                print(f" ✅ {stats['points']} PTS | {stats['rebounds']} REB | {stats['assists']} AST | {stats['three_pointers_made']} 3PM | {stats['steals']} STL | {stats['blocks']} BLK")
                away_simulations.append(result)
            else:
                print()
        
        # Small delay between batches to avoid overwhelming API
        if batch_start + batch_size < len(away_roster):
            await asyncio.sleep(0.5)
    
    # Calculate team totals
    home_total_pts = sum(p['projected_stats']['points'] for p in home_simulations)
    away_total_pts = sum(p['projected_stats']['points'] for p in away_simulations)
    
    print(f"\n📊 RESULTS:")
    print(f"   {game['home_team']}: {len(home_simulations)} players simulated, {round(home_total_pts, 1)} projected points")
    print(f"   {game['away_team']}: {len(away_simulations)} players simulated, {round(away_total_pts, 1)} projected points")
    print(f"   🏆 Projected Winner: {game['home_team'] if home_total_pts > away_total_pts else game['away_team']}")
    
    return {
        'game_id': game['game_id'],
        'game_date': game['game_date_str'],
        'matchup': game['matchup'],
        'game_status': game['game_status'],
        'home_team': game['home_team'],
        'away_team': game['away_team'],
        'home_players': home_simulations,
        'away_players': away_simulations,
        'summary': {
            'home_players_simulated': len(home_simulations),
            'away_players_simulated': len(away_simulations),
            'total_players_simulated': len(home_simulations) + len(away_simulations),
            'home_projected_points': round(home_total_pts, 1),
            'away_projected_points': round(away_total_pts, 1),
            'projected_winner': game['home_team'] if home_total_pts > away_total_pts else game['away_team'],
            'point_differential': abs(round(home_total_pts - away_total_pts, 1))
        }
    }

async def main():
    print("\n" + "="*80)
    print("🏀 NBA COMPLETE GAME SIMULATOR")
    print("   Simulating ALL players for today's and tomorrow's games")
    print("="*80)
    
    # Get games
    print("\n📅 Fetching games...")
    today_games = schedule_service.get_todays_games()
    tomorrow_games = schedule_service.get_tomorrows_games()
    
    print(f"\n   Today ({datetime.now().strftime('%Y-%m-%d')}): {len(today_games)} games")
    print(f"   Tomorrow: {len(tomorrow_games)} games")
    print(f"   Total: {len(today_games) + len(tomorrow_games)} games")
    
    if not today_games and not tomorrow_games:
        print("\n❌ No games found!")
        return
    
    # Show games
    print("\n📋 GAMES TO SIMULATE:")
    print("\nTODAY:")
    for i, game in enumerate(today_games, 1):
        print(f"   {i}. {game['matchup']} - {game['game_status']}")
    
    if tomorrow_games:
        print("\nTOMORROW:")
        for i, game in enumerate(tomorrow_games, len(today_games) + 1):
            print(f"   {i}. {game['matchup']} - {game['game_status']}")
    
    # Ask user what to simulate
    print("\n" + "="*80)
    print("OPTIONS:")
    print("   1. Simulate ALL games (will take a while)")
    print("   2. Simulate only TODAY's games")
    print("   3. Simulate only TOMORROW's games")
    print("   4. Simulate specific game by number")
    print("="*80)
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    games_to_simulate = []
    if choice == '1':
        games_to_simulate = today_games + tomorrow_games
    elif choice == '2':
        games_to_simulate = today_games
    elif choice == '3':
        games_to_simulate = tomorrow_games
    elif choice == '4':
        game_num = int(input("Enter game number: ")) - 1
        all_games = today_games + tomorrow_games
        if 0 <= game_num < len(all_games):
            games_to_simulate = [all_games[game_num]]
        else:
            print("Invalid game number!")
            return
    else:
        print("Invalid choice!")
        return
    
    if not games_to_simulate:
        print("\n❌ No games to simulate!")
        return
    
    # Simulate games
    print(f"\n🔄 Starting simulation of {len(games_to_simulate)} game(s)...")
    print(f"⏱️  Estimated time: {len(games_to_simulate) * 2-3} minutes")
    
    all_results = []
    start_time = datetime.now()
    
    for i, game in enumerate(games_to_simulate, 1):
        print(f"\n\n{'#'*80}")
        print(f"# GAME {i}/{len(games_to_simulate)}")
        print(f"{'#'*80}")
        
        result = await simulate_game(game, num_sims=50)
        all_results.append(result)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"simulation_results_{timestamp}.json"
    
    output = {
        'simulation_info': {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_games': len(all_results),
            'total_players': sum(r['summary']['total_players_simulated'] for r in all_results),
            'duration_seconds': round(duration, 2),
            'simulations_per_player': 50
        },
        'games': all_results
    }
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    # Print summary
    print("\n\n" + "="*80)
    print("📊 SIMULATION COMPLETE!")
    print("="*80)
    print(f"⏱️  Time: {duration:.1f} seconds")
    print(f"🏀 Games simulated: {len(all_results)}")
    print(f"👥 Total players simulated: {sum(r['summary']['total_players_simulated'] for r in all_results)}")
    print(f"💾 Results saved to: {filename}")
    
    # Collect all players with full stats
    print("\n" + "="*80)
    print("🏆 TOP PERFORMERS BY CATEGORY")
    print("="*80)
    
    all_players = []
    for game in all_results:
        for player in game['home_players'] + game['away_players']:
            if player.get('status') == 'success':
                stats = player['projected_stats']
                all_players.append({
                    'name': player['player_name'],
                    'game': game['matchup'],
                    'points': stats['points'],
                    'rebounds': stats['rebounds'],
                    'assists': stats['assists'],
                    'three_pointers': stats.get('three_pointers_made', 0),
                    'steals': stats['steals'],
                    'blocks': stats['blocks']
                })
    
    if all_players:
        # Top Scorers
        print("\n🔥 TOP 5 SCORERS:")
        top_scorers = sorted(all_players, key=lambda x: x['points'], reverse=True)[:5]
        for i, player in enumerate(top_scorers, 1):
            print(f"   {i}. {player['name']}: {player['points']} PTS ({player['game']})")
        
        # Top Rebounders
        print("\n🏀 TOP 5 REBOUNDERS:")
        top_rebounders = sorted(all_players, key=lambda x: x['rebounds'], reverse=True)[:5]
        for i, player in enumerate(top_rebounders, 1):
            print(f"   {i}. {player['name']}: {player['rebounds']} REB ({player['game']})")
        
        # Top Assist Leaders
        print("\n🎯 TOP 5 ASSIST LEADERS:")
        top_assists = sorted(all_players, key=lambda x: x['assists'], reverse=True)[:5]
        for i, player in enumerate(top_assists, 1):
            print(f"   {i}. {player['name']}: {player['assists']} AST ({player['game']})")
        
        # Top 3-Point Shooters
        print("\n🎯 TOP 5 THREE-POINT SHOOTERS:")
        top_threes = sorted(all_players, key=lambda x: x['three_pointers'], reverse=True)[:5]
        for i, player in enumerate(top_threes, 1):
            print(f"   {i}. {player['name']}: {player['three_pointers']} 3PM ({player['game']})")
        
        # Top Defenders (Steals)
        print("\n🛡️  TOP 5 STEALS LEADERS:")
        top_steals = sorted(all_players, key=lambda x: x['steals'], reverse=True)[:5]
        for i, player in enumerate(top_steals, 1):
            print(f"   {i}. {player['name']}: {player['steals']} STL ({player['game']})")
        
        # Top Shot Blockers
        print("\n🚫 TOP 5 SHOT BLOCKERS:")
        top_blocks = sorted(all_players, key=lambda x: x['blocks'], reverse=True)[:5]
        for i, player in enumerate(top_blocks, 1):
            print(f"   {i}. {player['name']}: {player['blocks']} BLK ({player['game']})")
    
    print("\n✅ Done!")

if __name__ == "__main__":
    asyncio.run(main())
