"""
Module 9: Explainability Service
Generates SHAP-based explanations for trained models
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
from joblib import load

try:
    import shap
except ImportError:
    shap = None

from app.config import MODELS_DIR
from app.logging_config import logger
from app.modules.module_2_data_processing.service import data_processor


@dataclass
class ExplainabilityResult:
    explanation_id: str
    model_id: str
    dataset_id: str
    target_column: str
    problem_type: str
    feature_importance: Dict[str, float]
    base_value: Optional[float]
    shap_values_summary: List[Dict[str, Any]]
    explained_at: str


class ExplainabilityService:
    """Generates SHAP explanations for trained pipelines"""

    def __init__(self):
        self._history: List[ExplainabilityResult] = []
        logger.info("ExplainabilityService initialized")

    def explain_model(
        self,
        model_id: str,
        dataset_id: str,
        target_column: str,
        max_rows: int = 200,
    ) -> ExplainabilityResult:
        dataset_info = data_processor.get_dataset_info(dataset_id)
        file_path = dataset_info.get("file_path")
        df, _ = data_processor.load_and_validate_data(file_path)

        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset")

        X = df.drop(columns=[target_column])
        if len(X) > max_rows:
            X = X.sample(n=max_rows, random_state=42)

        model_path = f"{MODELS_DIR}/{model_id}.joblib"
        pipeline = load(model_path)

        problem_type = self._infer_problem_type(df[target_column])

        explainer = self._build_explainer(pipeline, X)
        shap_values = explainer(X)

        feature_importance = self._summarize_feature_importance(shap_values, X)
        shap_values_summary = self._summarize_shap_values(shap_values, X)

        result = ExplainabilityResult(
            explanation_id=self._generate_id(),
            model_id=model_id,
            dataset_id=dataset_id,
            target_column=target_column,
            problem_type=problem_type,
            feature_importance=feature_importance,
            base_value=self._safe_base_value(shap_values),
            shap_values_summary=shap_values_summary,
            explained_at=datetime.utcnow().isoformat(),
        )

        self._history.append(result)
        logger.info(f"Explainability complete: {result.explanation_id}")
        return result

    def list_explanations(self, limit: int = 20) -> List[Dict[str, Any]]:
        return [self._to_dict(r) for r in self._history[-limit:]]

    @staticmethod
    def _build_explainer(pipeline, X):
        model = pipeline
        if hasattr(pipeline, "named_steps"):
            model = pipeline.named_steps.get("model", pipeline)
        if hasattr(model, "predict_proba") or "Forest" in model.__class__.__name__:
            return shap.TreeExplainer(model)
        if "Linear" in model.__class__.__name__:
            return shap.LinearExplainer(model, X, feature_perturbation="interventional")
        return shap.KernelExplainer(model.predict, X)

    @staticmethod
    def _summarize_feature_importance(shap_values, X) -> Dict[str, float]:
        values = shap_values.values
        if isinstance(values, list):
            values = values[0]
        importance = np.abs(values).mean(axis=0)
        return {col: float(score) for col, score in zip(X.columns, importance)}

    @staticmethod
    def _summarize_shap_values(shap_values, X) -> List[Dict[str, Any]]:
        values = shap_values.values
        if isinstance(values, list):
            values = values[0]
        summary = []
        for idx, row in enumerate(values[: min(len(values), 20)]):
            summary.append({
                "row_index": int(idx),
                "contributions": {col: float(val) for col, val in zip(X.columns, row)},
            })
        return summary

    @staticmethod
    def _safe_base_value(shap_values) -> Optional[float]:
        base = getattr(shap_values, "base_values", None)
        if base is None:
            return None
        if isinstance(base, (list, np.ndarray)):
            return float(np.array(base).mean())
        return float(base)

    @staticmethod
    def _infer_problem_type(y) -> str:
        unique_values = y.nunique()
        if y.dtype == "object" or unique_values <= 20:
            return "classification"
        return "regression"

    @staticmethod
    def _generate_id() -> str:
        import uuid

        return str(uuid.uuid4())

    @staticmethod
    def _to_dict(result: ExplainabilityResult) -> Dict[str, Any]:
        return {
            "explanation_id": result.explanation_id,
            "model_id": result.model_id,
            "dataset_id": result.dataset_id,
            "target_column": result.target_column,
            "problem_type": result.problem_type,
            "feature_importance": result.feature_importance,
            "base_value": result.base_value,
            "shap_values_summary": result.shap_values_summary,
            "explained_at": result.explained_at,
        }


explainability_service = ExplainabilityService()
