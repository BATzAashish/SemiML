"""
Module 11: Feedback & Learning Router
API endpoints for feedback submission and retrieval
"""
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.logging_config import logger
from app.modules.module_11_feedback_learning.service import feedback_learning_service

router = APIRouter(prefix="/api", tags=["Feedback & Learning"])


class FeedbackRequest(BaseModel):
    dataset_id: str
    pipeline_id: str
    model_id: str
    target_column: str
    performance_metrics: Dict[str, float]
    dataset_meta_features: Dict[str, Any]
    notes: Optional[str] = None
    accepted: bool = True


@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest) -> Dict[str, Any]:
    """
    Store feedback and optionally update experience store
    """
    try:
        logger.info("Submitting feedback")

        record = feedback_learning_service.submit_feedback(
            dataset_id=request.dataset_id,
            pipeline_id=request.pipeline_id,
            model_id=request.model_id,
            target_column=request.target_column,
            performance_metrics=request.performance_metrics,
            dataset_meta_features=request.dataset_meta_features,
            notes=request.notes,
            accepted=request.accepted,
        )

        return {
            "status": "success",
            "message": "Feedback recorded",
            "feedback": feedback_learning_service._to_dict(record),
        }

    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/feedback")
async def list_feedback(limit: int = 50) -> Dict[str, Any]:
    """
    List feedback records
    """
    try:
        records = feedback_learning_service.list_feedback(limit=limit)
        return {
            "status": "success",
            "count": len(records),
            "feedback": records,
        }
    except Exception as e:
        logger.error(f"Error listing feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
