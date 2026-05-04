"""
Module 4: Experience Retrieval Router
Provides endpoints for storing and retrieving ML pipeline experiences
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel

from app.modules.module_4_experience_retrieval.service import experience_retriever
from app.logging_config import logger

router = APIRouter(prefix="/api", tags=["Experience Retrieval"])


# ============================================================================
# Request Models
# ============================================================================

class PipelineExperienceRequest(BaseModel):
    """Request model for storing pipeline experience"""
    dataset_id: str
    pipeline_type: str
    model_name: str
    hyperparameters: Dict[str, Any]
    performance_metrics: Dict[str, float]
    dataset_meta_features: Dict[str, Any]
    notes: Optional[str] = None


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/store-experience")
async def store_pipeline_experience(request: PipelineExperienceRequest) -> Dict[str, Any]:
    """
    Store a completed ML pipeline experience
    
    This endpoint saves information about a trained model and its performance
    for later retrieval and comparison with similar datasets.
    
    Args:
        request: Pipeline experience details
        
    Returns:
        Stored experience record with experience_id
    """
    try:
        logger.info(f"Storing pipeline experience for dataset {request.dataset_id}")
        
        experience = experience_retriever.store_pipeline_experience(
            dataset_id=request.dataset_id,
            pipeline_type=request.pipeline_type,
            model_name=request.model_name,
            hyperparameters=request.hyperparameters,
            performance_metrics=request.performance_metrics,
            dataset_meta_features=request.dataset_meta_features,
            notes=request.notes,
        )
        
        return {
            "status": "success",
            "message": "Pipeline experience stored successfully",
            "experience": experience,
        }
        
    except Exception as e:
        logger.error(f"Error storing pipeline experience: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/find-similar-datasets")
async def find_similar_datasets(
    meta_features: Dict[str, Any],
    top_k: int = 5,
) -> Dict[str, Any]:
    """
    Find similar datasets from past experiences
    
    Args:
        meta_features: Meta-features of query dataset
        top_k: Number of similar datasets to return (default: 5)
        
    Returns:
        List of similar experiences ranked by similarity score
    """
    try:
        logger.info(f"Finding {top_k} similar datasets")
        
        similar_datasets = experience_retriever.find_similar_datasets(
            meta_features,
            top_k=top_k,
        )
        
        return {
            "status": "success",
            "count": len(similar_datasets),
            "similar_datasets": similar_datasets,
        }
        
    except Exception as e:
        logger.error(f"Error finding similar datasets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-best-practices")
async def get_best_practices(meta_features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get best practices and recommendations for dataset
    
    Based on dataset characteristics, returns preprocessing recommendations,
    model suggestions, and hyperparameter tips.
    
    Args:
        meta_features: Meta-features of the dataset
        
    Returns:
        Best practices and recommendations
    """
    try:
        logger.info("Generating best practices")
        
        recommendations = experience_retriever.get_best_practices(meta_features)
        
        return {
            "status": "success",
            "recommendations": recommendations,
        }
        
    except Exception as e:
        logger.error(f"Error generating best practices: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-best-models")
async def get_best_models(
    meta_features: Dict[str, Any],
    top_k: int = 3,
) -> Dict[str, Any]:
    """
    Get best performing models for similar datasets
    
    Returns models that performed well on datasets similar to the input.
    
    Args:
        meta_features: Meta-features of the dataset
        top_k: Number of top models to return (default: 3)
        
    Returns:
        List of best performing models with hyperparameters and performance
    """
    try:
        logger.info(f"Finding best models for dataset (top {top_k})")
        
        best_models = experience_retriever.get_best_models_for_dataset(
            meta_features,
            top_k=top_k,
        )
        
        return {
            "status": "success",
            "count": len(best_models),
            "best_models": best_models,
        }
        
    except Exception as e:
        logger.error(f"Error getting best models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search-experiences")
async def search_experiences(
    pipeline_type: Optional[str] = None,
    model_name: Optional[str] = None,
    min_performance: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Search stored experiences with filters
    
    Args:
        pipeline_type: Filter by pipeline type (classification, regression, clustering)
        model_name: Filter by model name
        min_performance: Minimum performance threshold
        
    Returns:
        Filtered list of experiences
    """
    try:
        logger.info("Searching experiences with filters")
        
        results = experience_retriever.search_experiences(
            pipeline_type=pipeline_type,
            model_name=model_name,
            min_performance=min_performance,
        )
        
        return {
            "status": "success",
            "count": len(results),
            "experiences": results,
        }
        
    except Exception as e:
        logger.error(f"Error searching experiences: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/experience-statistics")
async def get_experience_statistics() -> Dict[str, Any]:
    """
    Get statistics about stored pipeline experiences
    
    Returns:
        Statistics including total experiences, unique models, pipeline types, etc.
    """
    try:
        logger.info("Computing experience statistics")
        
        stats = experience_retriever.get_experience_statistics()
        
        return {
            "status": "success",
            "statistics": stats,
        }
        
    except Exception as e:
        logger.error(f"Error computing statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
