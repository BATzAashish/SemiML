"""
Module 9: Explainability Router
API endpoints for SHAP explanations
"""
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.logging_config import logger
from app.modules.module_9_explainability.service import explainability_service

router = APIRouter(prefix="/api", tags=["Explainability"])


class ExplainModelRequest(BaseModel):
    model_id: str
    dataset_id: str
    target_column: str
    max_rows: int = Field(default=200, ge=50, le=1000)


@router.post("/explain-model")
async def explain_model(request: ExplainModelRequest) -> Dict[str, Any]:
    """
    Generate SHAP explanations for a trained model
    """
    try:
        logger.info("Generating model explanations")

        result = explainability_service.explain_model(
            model_id=request.model_id,
            dataset_id=request.dataset_id,
            target_column=request.target_column,
            max_rows=request.max_rows,
        )

        return {
            "status": "success",
            "message": "Explanation generated successfully",
            "explanation": explainability_service._to_dict(result),
        }

    except FileNotFoundError as e:
        logger.warning(f"Explanation failed: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        logger.warning(f"Explanation failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating explanation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/explanations")
async def list_explanations(limit: int = 20) -> Dict[str, Any]:
    """
    List recent explanations
    """
    try:
        runs = explainability_service.list_explanations(limit=limit)
        return {
            "status": "success",
            "count": len(runs),
            "explanations": runs,
        }
    except Exception as e:
        logger.error(f"Error listing explanations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
