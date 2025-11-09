"""
Advanced ML-based Game Simulation using Top Teams Data
Uses historical performance of playoff-caliber teams to build better models
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import pickle
import logging
from pathlib import Path

from app.models import GameStats, SeasonAverages, PlayerInfo, PropType
from app.services.nba_stats import nba_stats_service

logger = logging.getLogger(__name__)


class MLGameSimulator:
    """
    ML-based game simulator trained on top teams' historical data
    """
    
    def __init__(self):
        self.models = {}  # Store models for each stat type
        self.scalers = {}  # Store scalers for each stat type
        self.is_trained = False
        self.model_path = Path("models")
        self.model_path.mkdir(exist_ok=True)
        
        # Top teams from each conference (can be updated each season)
        self.top_east_teams = ["BOS", "MIL", "PHI", "CLE"]  # Top 4 East
        self.top_west_teams = ["DEN", "LAL", "GSW", "PHX"]  # Top 4 West
        self.top_teams = self.top_east_teams + self.top_west_teams
        
        # Stats to predict
        self.stat_types = [
            'points', 'rebounds', 'assists', 'steals', 
            'blocks', 'turnovers', 'three_pointers_made', 'free_throws_made'
        ]
    
    async def train_models(
        self, 
        season: str = "2023-24",
        min_games: int = 10
    ) -> Dict[str, float]:
        """
        Train ML models using historical data from top teams
        
        Returns accuracy scores for each stat type
        """
        logger.info("Starting model training with top teams data...")
        
        # Collect training data
        training_data = await self._collect_training_data(season, min_games)
        
        if len(training_data) < 100:
            raise ValueError(f"Insufficient training data: only {len(training_data)} samples")
        
        # Train models for each stat type
        accuracy_scores = {}
        
        for stat_type in self.stat_types:
            logger.info(f"Training model for {stat_type}...")
            
            # Prepare features and target
            X, y = self._prepare_features(training_data, stat_type)
            
            if len(X) == 0:
                logger.warning(f"No data for {stat_type}, skipping")
                continue
            
            # Split train/test
            split_idx = int(len(X) * 0.8)
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model (using Gradient Boosting for better accuracy)
            model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
            model.fit(X_train_scaled, y_train)
            
            # Evaluate
            train_score = model.score(X_train_scaled, y_train)
            test_score = model.score(X_test_scaled, y_test)
            
            # Store model and scaler
            self.models[stat_type] = model
            self.scalers[stat_type] = scaler
            
            accuracy_scores[stat_type] = {
                'train_r2': round(train_score, 3),
                'test_r2': round(test_score, 3),
                'samples': len(X)
            }
            
            logger.info(f"{stat_type}: Train R² = {train_score:.3f}, Test R² = {test_score:.3f}")
        
        self.is_trained = True
        
        # Save models
        self._save_models()
        
        return accuracy_scores
    
    async def _collect_training_data(
        self, 
        season: str,
        min_games: int
    ) -> List[Dict]:
        """
        Collect historical game data from top teams
        """
        training_data = []
        
        # Get all players from top teams
        logger.info(f"Collecting data from top teams: {self.top_teams}")
        
        # For each top team, get their roster and game logs
        for team_abbr in self.top_teams:
            try:
                # Get team's players (this would need nba_api integration)
                # For now, we'll use a placeholder approach
                # In production, you'd query team rosters
                
                # Placeholder: Get games against these teams from player histories
                logger.info(f"Processing team: {team_abbr}")
                
            except Exception as e:
                logger.error(f"Error collecting data for {team_abbr}: {e}")
                continue
        
        # Alternative approach: Collect from specific star players we know
        star_players = [
            "LeBron James", "Stephen Curry", "Giannis Antetokounmpo",
            "Nikola Jokic", "Joel Embiid", "Luka Doncic",
            "Jayson Tatum", "Kevin Durant", "Damian Lillard",
            "Anthony Davis", "Kawhi Leonard", "Jimmy Butler"
        ]
        
        for player_name in star_players:
            try:
                player_info = await nba_stats_service.get_player_info(player_name)
                if not player_info:
                    continue
                
                # Get extensive game log (full season)
                game_log = await nba_stats_service.get_player_game_log(
                    player_info.player_id,
                    season=season,
                    last_n_games=82  # Full season
                )
                
                season_avg = await nba_stats_service.get_player_season_averages(
                    player_info.player_id,
                    season=season
                )
                
                if not season_avg or len(game_log) < min_games:
                    continue
                
                # Process each game as a training sample
                for i, game in enumerate(game_log):
                    # Get recent form (last 5 games before this one)
                    recent_games = game_log[max(0, i-5):i] if i > 0 else []
                    
                    training_sample = {
                        'player_id': player_info.player_id,
                        'player_name': player_info.full_name,
                        'game': game,
                        'season_avg': season_avg,
                        'recent_games': recent_games,
                        'game_number': i + 1
                    }
                    
                    training_data.append(training_sample)
                
                logger.info(f"Collected {len(game_log)} games from {player_name}")
                
            except Exception as e:
                logger.error(f"Error collecting data for {player_name}: {e}")
                continue
        
        logger.info(f"Total training samples collected: {len(training_data)}")
        return training_data
    
    def _prepare_features(
        self, 
        training_data: List[Dict],
        stat_type: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare feature matrix and target vector for a specific stat
        """
        features = []
        targets = []
        
        for sample in training_data:
            game = sample['game']
            season_avg = sample['season_avg']
            recent_games = sample['recent_games']
            
            # Get target value
            target_value = getattr(game, stat_type, None)
            if target_value is None:
                continue
            
            # Build feature vector
            feature_vector = []
            
            # Season averages
            feature_vector.append(getattr(season_avg, f"{stat_type}_per_game", 0))
            feature_vector.append(season_avg.minutes_per_game)
            feature_vector.append(season_avg.games_played)
            
            # Recent form (last 5 games)
            if recent_games:
                recent_values = [getattr(g, stat_type, 0) for g in recent_games]
                feature_vector.append(np.mean(recent_values))  # Recent average
                feature_vector.append(np.std(recent_values))   # Recent variance
                feature_vector.append(len(recent_values))      # Number of recent games
                
                # Trend (difference between last 2 and first 2 games)
                if len(recent_values) >= 4:
                    recent_trend = np.mean(recent_values[-2:]) - np.mean(recent_values[:2])
                    feature_vector.append(recent_trend)
                else:
                    feature_vector.append(0)
            else:
                feature_vector.extend([0, 0, 0, 0])  # No recent data
            
            # Game context
            feature_vector.append(1 if game.is_home else 0)  # Home/away
            feature_vector.append(game.minutes_played or 0)  # Minutes played
            feature_vector.append(sample['game_number'])     # Season progression
            
            # Related stats (correlations)
            if stat_type == 'points':
                feature_vector.append(season_avg.field_goal_percentage)
                feature_vector.append(season_avg.free_throw_percentage)
            elif stat_type == 'assists':
                feature_vector.append(season_avg.points_per_game)
            elif stat_type == 'rebounds':
                feature_vector.append(season_avg.blocks_per_game)
            else:
                feature_vector.append(0)  # Placeholder
            
            features.append(feature_vector)
            targets.append(target_value)
        
        return np.array(features), np.array(targets)
    
    def predict_player_performance(
        self,
        player_info: PlayerInfo,
        season_averages: SeasonAverages,
        recent_games: List[GameStats],
        is_home: bool = True,
        minutes_projection: float = None
    ) -> Dict[str, float]:
        """
        Predict player's performance using trained ML models
        """
        if not self.is_trained:
            raise ValueError("Models not trained yet. Call train_models() first.")
        
        predictions = {}
        
        # Estimate minutes if not provided
        if minutes_projection is None:
            minutes_projection = season_averages.minutes_per_game
        
        for stat_type in self.stat_types:
            if stat_type not in self.models:
                continue
            
            # Build feature vector (same structure as training)
            feature_vector = []
            
            # Season averages
            feature_vector.append(getattr(season_averages, f"{stat_type}_per_game", 0))
            feature_vector.append(season_averages.minutes_per_game)
            feature_vector.append(season_averages.games_played)
            
            # Recent form
            if recent_games:
                recent_values = [getattr(g, stat_type, 0) for g in recent_games[-5:]]
                feature_vector.append(np.mean(recent_values))
                feature_vector.append(np.std(recent_values))
                feature_vector.append(len(recent_values))
                
                if len(recent_values) >= 4:
                    recent_trend = np.mean(recent_values[-2:]) - np.mean(recent_values[:2])
                    feature_vector.append(recent_trend)
                else:
                    feature_vector.append(0)
            else:
                feature_vector.extend([0, 0, 0, 0])
            
            # Game context
            feature_vector.append(1 if is_home else 0)
            feature_vector.append(minutes_projection)
            feature_vector.append(season_averages.games_played + 1)  # Next game
            
            # Related stats
            if stat_type == 'points':
                feature_vector.append(season_averages.field_goal_percentage)
                feature_vector.append(season_averages.free_throw_percentage)
            elif stat_type == 'assists':
                feature_vector.append(season_averages.points_per_game)
            elif stat_type == 'rebounds':
                feature_vector.append(season_averages.blocks_per_game)
            else:
                feature_vector.append(0)
            
            # Scale and predict
            X = np.array([feature_vector])
            X_scaled = self.scalers[stat_type].transform(X)
            prediction = self.models[stat_type].predict(X_scaled)[0]
            
            # Ensure non-negative
            predictions[stat_type] = max(0, prediction)
        
        return predictions
    
    def _save_models(self):
        """Save trained models to disk"""
        try:
            for stat_type in self.models:
                model_file = self.model_path / f"{stat_type}_model.pkl"
                scaler_file = self.model_path / f"{stat_type}_scaler.pkl"
                
                with open(model_file, 'wb') as f:
                    pickle.dump(self.models[stat_type], f)
                
                with open(scaler_file, 'wb') as f:
                    pickle.dump(self.scalers[stat_type], f)
            
            logger.info(f"Models saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def load_models(self):
        """Load pre-trained models from disk"""
        try:
            for stat_type in self.stat_types:
                model_file = self.model_path / f"{stat_type}_model.pkl"
                scaler_file = self.model_path / f"{stat_type}_scaler.pkl"
                
                if model_file.exists() and scaler_file.exists():
                    with open(model_file, 'rb') as f:
                        self.models[stat_type] = pickle.load(f)
                    
                    with open(scaler_file, 'rb') as f:
                        self.scalers[stat_type] = pickle.load(f)
            
            self.is_trained = len(self.models) > 0
            logger.info(f"Loaded {len(self.models)} pre-trained models")
            return True
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False
    
    async def simulate_with_ml(
        self,
        player_info: PlayerInfo,
        season_averages: SeasonAverages,
        recent_games: List[GameStats],
        num_simulations: int = 100,
        is_home: bool = True
    ) -> List[GameStats]:
        """
        Simulate games using ML predictions with realistic variance
        """
        if not self.is_trained:
            # Try to load pre-trained models
            if not self.load_models():
                raise ValueError("No trained models available. Train models first.")
        
        # Get ML predictions
        ml_predictions = self.predict_player_performance(
            player_info,
            season_averages,
            recent_games,
            is_home
        )
        
        simulations = []
        
        for _ in range(num_simulations):
            # Add realistic variance to ML predictions
            simulated_stats = {}
            
            for stat_type, predicted_value in ml_predictions.items():
                # Add Gaussian noise (15-25% std dev based on stat type)
                if stat_type in ['steals', 'blocks']:
                    std_dev = predicted_value * 0.40  # Higher variance for defensive stats
                elif stat_type in ['assists', 'rebounds']:
                    std_dev = predicted_value * 0.25
                else:
                    std_dev = predicted_value * 0.20
                
                simulated_value = np.random.normal(predicted_value, std_dev)
                simulated_stats[stat_type] = max(0, int(round(simulated_value)))
            
            # Create GameStats object
            game_date = datetime.now() + timedelta(days=1)
            
            sim_game = GameStats(
                game_id=f"ML_SIM_{player_info.player_id}_{game_date.strftime('%Y%m%d')}_{_}",
                player_id=player_info.player_id,
                game_date=game_date,
                opponent="TBD",
                is_home=is_home,
                **simulated_stats
            )
            
            sim_game.fantasy_score = sim_game.calculate_fantasy_score()
            simulations.append(sim_game)
        
        return simulations


# Singleton instance
ml_game_simulator = MLGameSimulator()
