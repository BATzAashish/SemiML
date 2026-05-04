"""
Module 7: Training & Optimization Router
API endpoints for model training and tuning
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.logging_config import logger
from app.modules.module_7_training_optimization.service import training_service

router = APIRouter(prefix="/api", tags=["Training & Optimization"])


class TrainPipelineRequest(BaseModel):
    dataset_id: str
    pipeline_id: str
    target_column: str
    test_size: float = Field(default=0.2, ge=0.05, le=0.5)
    random_state: int = 42
    tune_hyperparameters: bool = False
    param_grid: Optional[Dict[str, List[Any]]] = None
    cv_folds: int = Field(default=5, ge=2, le=10)


@router.post("/train-pipeline")
async def train_pipeline(request: TrainPipelineRequest) -> Dict[str, Any]:
    """
    Train a pipeline and return metrics and model artifact path
    """
    try:
        logger.info("Training pipeline")

        result = training_service.train_pipeline(
            dataset_id=request.dataset_id,
            pipeline_id=request.pipeline_id,
            target_column=request.target_column,
            test_size=request.test_size,
            random_state=request.random_state,
            tune_hyperparameters=request.tune_hyperparameters,
            param_grid=request.param_grid,
            cv_folds=request.cv_folds,
        )

        return {
            "status": "success",
            "message": "Pipeline trained successfully",
            "training": training_service._to_dict(result),
        }

    except ValueError as e:
        logger.warning(f"Training failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        logger.warning(f"Training failed: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error training pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/training-runs")
async def list_training_runs(limit: int = 20) -> Dict[str, Any]:
    """
    List recent training runs
    """
    try:
        runs = training_service.list_training_runs(limit=limit)
        return {
            "status": "success",
            "count": len(runs),
            "runs": runs,
        }
    except Exception as e:
        logger.error(f"Error listing training runs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
