"""
Module 8: Validation Router
API endpoints for model validation
"""
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.logging_config import logger
from app.modules.module_8_validation.service import validation_service

router = APIRouter(prefix="/api", tags=["Validation"])


class ValidationRequest(BaseModel):
    dataset_id: str
    pipeline_id: str
    target_column: str
    cv_folds: int = Field(default=5, ge=2, le=10)


@router.post("/validate-model")
async def validate_model(request: ValidationRequest) -> Dict[str, Any]:
    """
    Validate a pipeline using cross-validation and leakage checks
    """
    try:
        logger.info("Validating model")

        result = validation_service.validate_model(
            dataset_id=request.dataset_id,
            pipeline_id=request.pipeline_id,
            target_column=request.target_column,
            cv_folds=request.cv_folds,
        )

        return {
            "status": "success",
            "message": "Validation complete",
            "validation": validation_service._to_dict(result),
        }

    except ValueError as e:
        logger.warning(f"Validation failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        logger.warning(f"Validation failed: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error validating model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/validation-runs")
async def list_validations(limit: int = 20) -> Dict[str, Any]:
    """
    List recent validation runs
    """
    try:
        runs = validation_service.list_validations(limit=limit)
        return {
            "status": "success",
            "count": len(runs),
            "runs": runs,
        }
    except Exception as e:
        logger.error(f"Error listing validation runs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
