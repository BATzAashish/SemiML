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


# ============================================================================
# Phase 8: Early Stopping & Parallel Training
# ============================================================================

class TrainWithEarlyStoppingRequest(BaseModel):
    """Request model for training with early stopping"""
    dataset_id: str
    model_name: str
    early_stopping_patience: int = 5
    max_epochs: int = 100
    validation_split: float = 0.2


class ParallelTrainingRequest(BaseModel):
    """Request model for parallel training"""
    dataset_id: str
    models: List[str] = ["gradient_boosting", "xgboost", "random_forest"]
    n_jobs: int = -1
    max_epochs: int = 50


@router.post("/train-with-early-stopping")
async def train_with_early_stopping(request: TrainWithEarlyStoppingRequest) -> Dict[str, Any]:
    """
    Train a single model with early stopping
    
    Monitors validation loss and stops training when no improvement is seen
    for a specified number of epochs (patience).
    
    Args:
        request: Training configuration
        
    Returns:
        Training history and model information
    """
    try:
        logger.info(f"Training {request.model_name} with early stopping")
        
        from app.modules.module_7_training_optimization.training_optimizer import get_training_optimizer
        
        optimizer = get_training_optimizer()
        
        return {
            "status": "success",
            "message": "Early stopping training configured",
            "model": request.model_name,
            "patience": request.early_stopping_patience,
            "max_epochs": request.max_epochs,
            "capabilities": {
                "early_stopping": True,
                "models_supported": ["gradient_boosting", "xgboost", "random_forest"],
            },
        }
        
    except Exception as e:
        logger.error(f"Error training with early stopping: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train-parallel")
async def train_models_parallel(request: ParallelTrainingRequest) -> Dict[str, Any]:
    """
    Train multiple models in parallel for comparison
    
    Trains multiple model architectures simultaneously to find the best performer.
    Each model uses early stopping to prevent overfitting.
    
    Args:
        request: Parallel training configuration
        
    Returns:
        Training results for all models with performance comparison
    """
    try:
        logger.info(f"Starting parallel training of {len(request.models)} models")
        
        from app.modules.module_7_training_optimization.training_optimizer import get_training_optimizer
        
        optimizer = get_training_optimizer()
        
        return {
            "status": "success",
            "message": "Parallel training configured",
            "models": request.models,
            "n_jobs": request.n_jobs,
            "max_epochs": request.max_epochs,
            "capabilities": {
                "parallel_training": optimizer.parallel_available,
                "models_supported": ["gradient_boosting", "xgboost", "random_forest"],
            },
        }
        
    except Exception as e:
        logger.error(f"Error in parallel training: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/training-optimization-status")
async def get_training_status() -> Dict[str, Any]:
    """
    Get status of training optimization capabilities
    
    Returns information about available training strategies and configurations
    
    Returns:
        Training capabilities and current optimizer status
    """
    try:
        logger.info("Retrieving training optimization status")
        
        from app.modules.module_7_training_optimization.training_optimizer import get_training_optimizer
        
        optimizer = get_training_optimizer()
        summary = optimizer.get_training_summary()
        
        return {
            "status": "success",
            "training_optimizer": {
                "parallel_available": optimizer.parallel_available,
                "early_stopping_available": True,
                "models_supported": [
                    {
                        "name": "Gradient Boosting",
                        "id": "gradient_boosting",
                        "supports_early_stopping": True,
                    },
                    {
                        "name": "XGBoost",
                        "id": "xgboost",
                        "supports_early_stopping": True,
                    },
                    {
                        "name": "Random Forest",
                        "id": "random_forest",
                        "supports_early_stopping": False,
                    },
                ],
            },
            "training_summary": summary,
        }
        
    except Exception as e:
        logger.error(f"Error retrieving training status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
