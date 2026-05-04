"""
Module 8: Validation Service
Validates trained models for generalization, leakage, and overfitting
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
from sklearn.model_selection import cross_val_score

from app.config import MIN_CROSS_VAL_SCORE, MAX_OVERFITTING_THRESHOLD
from app.logging_config import logger
from app.modules.module_2_data_processing.service import data_processor
from app.modules.module_6_pipeline_builder.service import pipeline_builder


@dataclass
class ValidationResult:
    validation_id: str
    dataset_id: str
    pipeline_id: str
    target_column: str
    problem_type: str
    cv_scores: List[float]
    cv_mean: float
    cv_std: float
    overfitting_gap: float
    leakage_flags: List[str]
    accepted: bool
    validated_at: str


class ValidationService:
    """Validates models and datasets for common risks"""

    def __init__(self):
        self._history: List[ValidationResult] = []
        logger.info("ValidationService initialized")

    def validate_model(
        self,
        dataset_id: str,
        pipeline_id: str,
        target_column: str,
        cv_folds: int = 5,
    ) -> ValidationResult:
        dataset_info = data_processor.get_dataset_info(dataset_id)
        file_path = dataset_info.get("file_path")
        df, _ = data_processor.load_and_validate_data(file_path)

        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset")

        X = df.drop(columns=[target_column])
        y = df[target_column]

        problem_type = self._infer_problem_type(y)
        pipeline = pipeline_builder.get_pipeline(pipeline_id)

        scoring = "accuracy" if problem_type == "classification" else "r2"
        cv_scores = cross_val_score(pipeline, X, y, cv=cv_folds, scoring=scoring).tolist()

        cv_mean = float(np.mean(cv_scores))
        cv_std = float(np.std(cv_scores))

        overfitting_gap = self._estimate_overfitting_gap(cv_scores)
        leakage_flags = self._detect_leakage(df, target_column)

        accepted = (
            cv_mean >= MIN_CROSS_VAL_SCORE
            and overfitting_gap <= MAX_OVERFITTING_THRESHOLD
            and len(leakage_flags) == 0
        )

        result = ValidationResult(
            validation_id=self._generate_id(),
            dataset_id=dataset_id,
            pipeline_id=pipeline_id,
            target_column=target_column,
            problem_type=problem_type,
            cv_scores=cv_scores,
            cv_mean=cv_mean,
            cv_std=cv_std,
            overfitting_gap=overfitting_gap,
            leakage_flags=leakage_flags,
            accepted=accepted,
            validated_at=datetime.utcnow().isoformat(),
        )

        self._history.append(result)
        logger.info(f"Validation complete: {result.validation_id} accepted={accepted}")
        return result

    def list_validations(self, limit: int = 20) -> List[Dict[str, Any]]:
        return [self._to_dict(v) for v in self._history[-limit:]]

    @staticmethod
    def _infer_problem_type(y) -> str:
        unique_values = y.nunique()
        if y.dtype == "object" or unique_values <= 20:
            return "classification"
        return "regression"

    @staticmethod
    def _estimate_overfitting_gap(cv_scores: List[float]) -> float:
        if not cv_scores:
            return 0.0
        return float(max(cv_scores) - min(cv_scores))

    @staticmethod
    def _detect_leakage(df, target_column: str) -> List[str]:
        flags: List[str] = []
        if target_column.lower() in ["target", "label", "outcome"]:
            flags.append("Target column has generic label name; verify leakage")

        if df[target_column].nunique() == len(df):
            flags.append("Target column appears to be an identifier")

        return flags

    @staticmethod
    def _generate_id() -> str:
        import uuid

        return str(uuid.uuid4())

    @staticmethod
    def _to_dict(result: ValidationResult) -> Dict[str, Any]:
        return {
            "validation_id": result.validation_id,
            "dataset_id": result.dataset_id,
            "pipeline_id": result.pipeline_id,
            "target_column": result.target_column,
            "problem_type": result.problem_type,
            "cv_scores": result.cv_scores,
            "cv_mean": result.cv_mean,
            "cv_std": result.cv_std,
            "overfitting_gap": result.overfitting_gap,
            "leakage_flags": result.leakage_flags,
            "accepted": result.accepted,
            "validated_at": result.validated_at,
        }


validation_service = ValidationService()
