"""
Module 11: Feedback & Learning Service
Stores validated experiments and updates experience store
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import uuid

from app.config import UPLOAD_DIR
from app.logging_config import logger
from app.modules.module_4_experience_retrieval.service import experience_retriever


FEEDBACK_DIR = Path(UPLOAD_DIR) / "feedback"
FEEDBACK_DIR.mkdir(exist_ok=True)
FEEDBACK_FILE = FEEDBACK_DIR / "feedback.json"


@dataclass
class FeedbackRecord:
    feedback_id: str
    dataset_id: str
    pipeline_id: str
    model_id: str
    target_column: str
    performance_metrics: Dict[str, float]
    notes: Optional[str]
    accepted: bool
    submitted_at: str


class FeedbackLearningService:
    """Stores feedback and updates experience store"""

    def __init__(self):
        self._records: List[FeedbackRecord] = []
        self._load_feedback()
        logger.info("FeedbackLearningService initialized")

    def submit_feedback(
        self,
        dataset_id: str,
        pipeline_id: str,
        model_id: str,
        target_column: str,
        performance_metrics: Dict[str, float],
        dataset_meta_features: Dict[str, Any],
        notes: Optional[str],
        accepted: bool,
    ) -> FeedbackRecord:
        record = FeedbackRecord(
            feedback_id=str(uuid.uuid4()),
            dataset_id=dataset_id,
            pipeline_id=pipeline_id,
            model_id=model_id,
            target_column=target_column,
            performance_metrics=performance_metrics,
            notes=notes,
            accepted=accepted,
            submitted_at=datetime.utcnow().isoformat(),
        )

        self._records.append(record)
        self._save_feedback()

        if accepted:
            experience_retriever.store_pipeline_experience(
                dataset_id=dataset_id,
                pipeline_type=self._infer_pipeline_type(performance_metrics),
                model_name=self._infer_model_name(model_id),
                hyperparameters={},
                performance_metrics=performance_metrics,
                dataset_meta_features=dataset_meta_features,
                notes=notes,
            )

        logger.info(f"Feedback recorded: {record.feedback_id}")
        return record

    def list_feedback(self, limit: int = 50) -> List[Dict[str, Any]]:
        return [self._to_dict(r) for r in self._records[-limit:]]

    def _load_feedback(self) -> None:
        if not FEEDBACK_FILE.exists():
            return
        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            self._records = [FeedbackRecord(**item) for item in data]
        except Exception as exc:
            logger.error(f"Failed to load feedback: {exc}")
            self._records = []

    def _save_feedback(self) -> None:
        try:
            with open(FEEDBACK_FILE, "w", encoding="utf-8") as handle:
                json.dump([self._to_dict(r) for r in self._records], handle, indent=2)
        except Exception as exc:
            logger.error(f"Failed to save feedback: {exc}")

    @staticmethod
    def _infer_pipeline_type(performance_metrics: Dict[str, float]) -> str:
        if "accuracy" in performance_metrics or "f1_macro" in performance_metrics:
            return "classification"
        if "r2" in performance_metrics or "rmse" in performance_metrics:
            return "regression"
        return "unknown"

    @staticmethod
    def _infer_model_name(model_id: str) -> str:
        return f"model_{model_id[:8]}"

    @staticmethod
    def _to_dict(record: FeedbackRecord) -> Dict[str, Any]:
        return {
            "feedback_id": record.feedback_id,
            "dataset_id": record.dataset_id,
            "pipeline_id": record.pipeline_id,
            "model_id": record.model_id,
            "target_column": record.target_column,
            "performance_metrics": record.performance_metrics,
            "notes": record.notes,
            "accepted": record.accepted,
            "submitted_at": record.submitted_at,
        }


feedback_learning_service = FeedbackLearningService()
