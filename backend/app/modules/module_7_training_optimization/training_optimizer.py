"""
Training Optimization Service
Implements early stopping, parallel training, and advanced training strategies
"""
import os
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import pickle

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
import pandas as pd

from app.logging_config import logger

try:
    from joblib import Parallel, delayed
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False


@dataclass
class TrainingCallback:
    """Callback for monitoring training progress"""
    epoch: int
    train_loss: float
    val_loss: float
    val_metric: float
    best_val_metric: float
    patience_count: int
    should_stop: bool = False


@dataclass
class EarlyStoppingConfig:
    """Configuration for early stopping"""
    monitor: str = "val_loss"  # metric to monitor: val_loss, val_accuracy, etc.
    patience: int = 5  # number of epochs with no improvement to stop
    min_delta: float = 0.001  # minimum change to count as improvement
    mode: str = "min"  # "min" for loss, "max" for accuracy/f1
    restore_best_weights: bool = True
    verbose: int = 1


class EarlyStoppingCallback:
    """Early stopping callback for training monitoring"""
    
    def __init__(self, config: EarlyStoppingConfig):
        self.config = config
        self.best_value = float('inf') if config.mode == 'min' else float('-inf')
        self.best_epoch = 0
        self.patience_count = 0
        self.best_weights = None
        self.stopped_epoch = 0
    
    def on_epoch_end(self, epoch: int, logs: Dict[str, float]) -> TrainingCallback:
        """
        Called at end of each epoch
        
        Args:
            epoch: Current epoch number
            logs: Dictionary with training metrics
            
        Returns:
            TrainingCallback with stopping decision
        """
        current = logs.get(self.config.monitor, float('inf'))
        
        # Check if improvement
        if self.config.mode == 'min':
            improved = (self.best_value - current) > self.config.min_delta
        else:  # max mode
            improved = (current - self.best_value) > self.config.min_delta
        
        if improved:
            self.best_value = current
            self.best_epoch = epoch
            self.patience_count = 0
            self.best_weights = logs.get('weights', None)
            
            if self.config.verbose > 0:
                logger.info(f"Epoch {epoch}: Improved {self.config.monitor} to {current:.4f}")
        else:
            self.patience_count += 1
            
            if self.config.verbose > 0 and self.patience_count % 2 == 0:
                logger.warning(
                    f"Epoch {epoch}: No improvement. "
                    f"Patience {self.patience_count}/{self.config.patience}"
                )
        
        should_stop = self.patience_count >= self.config.patience
        if should_stop:
            self.stopped_epoch = epoch
            logger.warning(f"Early stopping at epoch {epoch}")
        
        return TrainingCallback(
            epoch=epoch,
            train_loss=logs.get('train_loss', 0.0),
            val_loss=logs.get('val_loss', 0.0),
            val_metric=current,
            best_val_metric=self.best_value,
            patience_count=self.patience_count,
            should_stop=should_stop,
        )


class TrainingOptimizer:
    """
    Optimization strategies for model training
    Includes early stopping, parallel training, hyperparameter optimization
    """
    
    def __init__(self):
        self.parallel_available = JOBLIB_AVAILABLE
        self.training_history = []
        self.best_models = {}
        logger.info(f"TrainingOptimizer initialized (Parallel available: {self.parallel_available})")
    
    def train_with_early_stopping(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        model_name: str = "gradient_boosting",
        early_stopping_config: Optional[EarlyStoppingConfig] = None,
        max_epochs: int = 100,
    ) -> Tuple[Any, Dict[str, Any]]:
        """
        Train model with early stopping
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features
            y_val: Validation labels
            model_name: Name of model to train
            early_stopping_config: Early stopping configuration
            max_epochs: Maximum number of epochs
            
        Returns:
            Tuple of (trained_model, training_history)
        """
        try:
            logger.info(f"Training {model_name} with early stopping")
            
            if early_stopping_config is None:
                early_stopping_config = EarlyStoppingConfig()
            
            early_stopping = EarlyStoppingCallback(early_stopping_config)
            
            # Select model
            if model_name == "gradient_boosting":
                model = GradientBoostingClassifier(n_estimators=max_epochs, random_state=42)
                history = self._train_gb_with_monitoring(
                    model, X_train, y_train, X_val, y_val, early_stopping, max_epochs
                )
            elif model_name == "xgboost":
                model = XGBClassifier(n_estimators=max_epochs, random_state=42, eval_metric='logloss')
                history = self._train_xgb_with_monitoring(
                    model, X_train, y_train, X_val, y_val, early_stopping, max_epochs
                )
            elif model_name == "random_forest":
                model = RandomForestClassifier(n_estimators=max_epochs, random_state=42)
                history = self._train_rf_with_monitoring(
                    model, X_train, y_train, X_val, y_val, early_stopping, max_epochs
                )
            else:
                raise ValueError(f"Unknown model: {model_name}")
            
            logger.info(f"Training completed. Stopped at epoch {early_stopping.stopped_epoch}")
            
            return model, history
            
        except Exception as e:
            logger.error(f"Error training with early stopping: {str(e)}")
            raise

    def _train_gb_with_monitoring(
        self,
        model: GradientBoostingClassifier,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        early_stopping: EarlyStoppingCallback,
        max_epochs: int,
    ) -> Dict[str, Any]:
        """Train GradientBoosting with monitoring"""
        train_scores = []
        val_scores = []
        
        # Train incrementally
        for epoch in range(max_epochs):
            # Warm-start training
            if epoch == 0:
                model.fit(X_train, y_train)
            else:
                model.set_params(n_estimators=epoch + 1)
                model.fit(X_train, y_train)
            
            # Evaluate
            train_score = model.score(X_train, y_train)
            val_score = model.score(X_val, y_val)
            
            train_scores.append(train_score)
            val_scores.append(val_score)
            
            # Early stopping
            logs = {
                'train_loss': 1 - train_score,
                'val_loss': 1 - val_score,
                'val_accuracy': val_score,
            }
            callback = early_stopping.on_epoch_end(epoch, logs)
            
            if callback.should_stop:
                break
        
        return {
            "epochs": len(train_scores),
            "stopped_epoch": early_stopping.stopped_epoch,
            "train_scores": train_scores,
            "val_scores": val_scores,
            "best_epoch": early_stopping.best_epoch,
            "best_score": early_stopping.best_value,
        }

    def _train_xgb_with_monitoring(
        self,
        model: XGBClassifier,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        early_stopping: EarlyStoppingCallback,
        max_epochs: int,
    ) -> Dict[str, Any]:
        """Train XGBoost with monitoring and built-in early stopping"""
        eval_set = [(X_val, y_val)]
        eval_metric = 'logloss'
        
        model.fit(
            X_train, y_train,
            eval_set=eval_set,
            eval_metric=eval_metric,
            early_stopping_rounds=early_stopping.config.patience,
            verbose=early_stopping.config.verbose,
        )
        
        results = model.evals_result()
        
        return {
            "epochs": model.n_estimators,
            "stopped_epoch": model.best_iteration,
            "best_score": model.best_score,
            "eval_results": results,
        }

    def _train_rf_with_monitoring(
        self,
        model: RandomForestClassifier,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        early_stopping: EarlyStoppingCallback,
        max_epochs: int,
    ) -> Dict[str, Any]:
        """Train RandomForest with monitoring"""
        train_scores = []
        val_scores = []
        
        # Random Forest doesn't support warm start well, train once
        model.fit(X_train, y_train)
        
        train_score = model.score(X_train, y_train)
        val_score = model.score(X_val, y_val)
        
        train_scores.append(train_score)
        val_scores.append(val_score)
        
        return {
            "epochs": 1,
            "train_scores": train_scores,
            "val_scores": val_scores,
            "final_score": val_score,
        }

    def train_models_parallel(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        model_names: List[str] = None,
        n_jobs: int = -1,
    ) -> Dict[str, Tuple[Any, Dict[str, Any]]]:
        """
        Train multiple models in parallel
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features
            y_val: Validation labels
            model_names: List of model names to train
            n_jobs: Number of parallel jobs (-1 = all cores)
            
        Returns:
            Dictionary mapping model names to (model, history) tuples
        """
        if model_names is None:
            model_names = ["gradient_boosting", "xgboost", "random_forest"]
        
        try:
            logger.info(f"Training {len(model_names)} models in parallel")
            
            if self.parallel_available and len(model_names) > 1:
                # Use joblib for parallel training
                results = Parallel(n_jobs=n_jobs)(
                    delayed(self._train_single_model)(
                        X_train, y_train, X_val, y_val, model_name
                    )
                    for model_name in model_names
                )
                
                trained_models = {
                    model_name: result
                    for model_name, result in zip(model_names, results)
                }
            else:
                # Train sequentially
                trained_models = {}
                for model_name in model_names:
                    result = self._train_single_model(X_train, y_train, X_val, y_val, model_name)
                    trained_models[model_name] = result
            
            logger.info(f"Parallel training completed for {len(trained_models)} models")
            self.best_models = trained_models
            return trained_models
            
        except Exception as e:
            logger.error(f"Error in parallel training: {str(e)}")
            raise

    def _train_single_model(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        model_name: str,
    ) -> Tuple[Any, Dict[str, Any]]:
        """Train a single model"""
        logger.info(f"Training {model_name}")
        
        try:
            model, history = self.train_with_early_stopping(
                X_train, y_train, X_val, y_val,
                model_name=model_name,
                max_epochs=50,
            )
            return (model, history)
        except Exception as e:
            logger.error(f"Error training {model_name}: {str(e)}")
            raise

    def get_best_model(self) -> Tuple[str, Any]:
        """Get best model from last parallel training"""
        if not self.best_models:
            return None, None
        
        best_name = None
        best_score = -float('inf')
        best_model = None
        
        for model_name, (model, history) in self.best_models.items():
            score = history.get("best_score", history.get("final_score", 0))
            if score > best_score:
                best_score = score
                best_name = model_name
                best_model = model
        
        logger.info(f"Best model: {best_name} with score {best_score:.4f}")
        return best_name, best_model

    def get_training_summary(self) -> Dict[str, Any]:
        """Get summary of training results"""
        if not self.best_models:
            return {"status": "no_training", "message": "No training completed yet"}
        
        summary = {
            "models_trained": len(self.best_models),
            "models": {},
        }
        
        for model_name, (model, history) in self.best_models.items():
            summary["models"][model_name] = {
                "best_score": history.get("best_score", history.get("final_score", 0)),
                "epochs": history.get("epochs", "N/A"),
                "stopped_epoch": history.get("stopped_epoch", "N/A"),
            }
        
        return summary


# Global training optimizer instance
training_optimizer: Optional[TrainingOptimizer] = None


def get_training_optimizer() -> TrainingOptimizer:
    """Get or initialize training optimizer"""
    global training_optimizer
    if training_optimizer is None:
        training_optimizer = TrainingOptimizer()
    return training_optimizer
