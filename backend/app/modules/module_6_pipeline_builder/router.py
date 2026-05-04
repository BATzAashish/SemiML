"""
Module 6: Pipeline Builder Router
API endpoints for building sklearn pipelines
"""
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.logging_config import logger
from app.models.schemas import PipelineConfig
from app.modules.module_6_pipeline_builder.service import pipeline_builder

router = APIRouter(prefix="/api", tags=["Pipeline Builder"])


class PipelineBuildRequest(BaseModel):
    pipeline_config: PipelineConfig
    dataset_meta_features: Optional[Dict[str, Any]] = None


@router.post("/build-pipeline")
async def build_pipeline(request: PipelineBuildRequest) -> Dict[str, Any]:
    """
    Build a sklearn pipeline dynamically

    Returns pipeline_id and summary. The pipeline object is stored in memory.
    """
    try:
        logger.info("Building pipeline")

        config = request.pipeline_config
        feature_types = None
        if request.dataset_meta_features:
            feature_types = request.dataset_meta_features.get("feature_types")

        preprocessing_steps = [step.name for step in config.preprocessing]
        fe_steps = [step.name for step in config.feature_engineering]

        pipeline_id, _, summary = pipeline_builder.build_pipeline(
            problem_type=config.problem_type,
            preprocessing_steps=preprocessing_steps,
            model_name=config.model.name,
            model_params=config.model.parameters,
            feature_engineering_steps=fe_steps,
            feature_types=feature_types,
        )

        return {
            "status": "success",
            "message": "Pipeline built successfully",
            "pipeline_id": pipeline_id,
            "summary": summary,
        }

    except ValueError as e:
        logger.warning(f"Pipeline build failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error building pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
