"""
Module 7: Training & Optimization Service
Trains sklearn pipelines and optionally performs hyperparameter tuning
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import uuid

from joblib import dump
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score

from app.config import MODELS_DIR
from app.logging_config import logger
from app.modules.module_2_data_processing.service import data_processor
from app.modules.module_6_pipeline_builder.service import pipeline_builder


@dataclass
class TrainingResult:
    model_id: str
    pipeline_id: str
    dataset_id: str
    target_column: str
    problem_type: str
    metrics: Dict[str, float]
    cv_scores: Optional[List[float]]
    trained_at: str
    artifact_path: str
    best_params: Optional[Dict[str, Any]] = None


class TrainingService:
    """Handles model training and tuning"""

    def __init__(self):
        self._history: List[TrainingResult] = []
        logger.info("TrainingService initialized")

    def train_pipeline(
        self,
        dataset_id: str,
        pipeline_id: str,
        target_column: str,
        test_size: float = 0.2,
        random_state: int = 42,
        tune_hyperparameters: bool = False,
        param_grid: Optional[Dict[str, List[Any]]] = None,
        cv_folds: int = 5,
    ) -> TrainingResult:
        """
        Train a pipeline on a dataset and return metrics and artifact path
        """
        dataset_info = data_processor.get_dataset_info(dataset_id)
        file_path = dataset_info.get("file_path")
        df, _ = data_processor.load_and_validate_data(file_path)

        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset")

        X = df.drop(columns=[target_column])
        y = df[target_column]

        problem_type = self._infer_problem_type(y)
        pipeline = pipeline_builder.get_pipeline(pipeline_id)
        self._prune_pipeline_columns(pipeline, list(X.columns))

        stratify = y if problem_type == "classification" else None
        if stratify is not None:
            num_classes = y.nunique()
            test_count = max(1, int(len(y) * test_size))
            if test_count < num_classes:
                stratify = None
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=random_state,
            stratify=stratify,
        )

        best_params = None
        if tune_hyperparameters:
            if not param_grid:
                raise ValueError("param_grid is required when tune_hyperparameters is true")
            scoring = "accuracy" if problem_type == "classification" else "r2"
            tuner = GridSearchCV(
                pipeline,
                param_grid=param_grid,
                cv=cv_folds,
                n_jobs=-1,
                scoring=scoring,
            )
            tuner.fit(X_train, y_train)
            pipeline = tuner.best_estimator_
            best_params = tuner.best_params_
        else:
            pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_test)
        metrics = self._compute_metrics(problem_type, y_test, predictions)

        cv_scores = None
        if not tune_hyperparameters and cv_folds > 1:
            scoring = "accuracy" if problem_type == "classification" else "r2"
            cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv_folds, scoring=scoring).tolist()

        model_id = str(uuid.uuid4())
        artifact_path = f"{MODELS_DIR}/{model_id}.joblib"
        dump(pipeline, artifact_path)

        result = TrainingResult(
            model_id=model_id,
            pipeline_id=pipeline_id,
            dataset_id=dataset_id,
            target_column=target_column,
            problem_type=problem_type,
            metrics=metrics,
            cv_scores=cv_scores,
            trained_at=datetime.utcnow().isoformat(),
            artifact_path=artifact_path,
            best_params=best_params,
        )

        self._history.append(result)
        logger.info(f"Training complete: {model_id} ({problem_type})")
        return result

    def list_training_runs(self, limit: int = 20) -> List[Dict[str, Any]]:
        runs = self._history[-limit:]
        return [self._to_dict(r) for r in runs]

    @staticmethod
    def _infer_problem_type(y) -> str:
        unique_values = y.nunique()
        if y.dtype == "object" or unique_values <= 20:
            return "classification"
        return "regression"

    @staticmethod
    def _compute_metrics(problem_type: str, y_true, y_pred) -> Dict[str, float]:
        if problem_type == "classification":
            return {
                "accuracy": float(accuracy_score(y_true, y_pred)),
                "f1_macro": float(f1_score(y_true, y_pred, average="macro")),
            }
        return {
            "r2": float(r2_score(y_true, y_pred)),
            "rmse": float(mean_squared_error(y_true, y_pred, squared=False)),
        }

    @staticmethod
    def _prune_pipeline_columns(pipeline, columns: List[str]) -> None:
        if not hasattr(pipeline, "named_steps"):
            return
        preprocessor = pipeline.named_steps.get("preprocessor")
        if not preprocessor or not hasattr(preprocessor, "transformers"):
            return

        new_transformers = []
        for name, transformer, cols in preprocessor.transformers:
            if isinstance(cols, list):
                filtered = [col for col in cols if col in columns]
                if not filtered:
                    continue
                new_transformers.append((name, transformer, filtered))
            else:
                new_transformers.append((name, transformer, cols))

        if not new_transformers:
            new_transformers = [("all", "passthrough", columns)]

        preprocessor.transformers = new_transformers

    @staticmethod
    def _to_dict(result: TrainingResult) -> Dict[str, Any]:
        return {
            "model_id": result.model_id,
            "pipeline_id": result.pipeline_id,
            "dataset_id": result.dataset_id,
            "target_column": result.target_column,
            "problem_type": result.problem_type,
            "metrics": result.metrics,
            "cv_scores": result.cv_scores,
            "trained_at": result.trained_at,
            "artifact_path": result.artifact_path,
            "best_params": result.best_params,
        }


training_service = TrainingService()
