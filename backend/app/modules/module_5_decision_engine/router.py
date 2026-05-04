"""
Module 5: Decision Engine Router
Provides endpoints for ML pipeline decision making and recommendations
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel

from app.modules.module_5_decision_engine.service import decision_engine
from app.logging_config import logger

router = APIRouter(prefix="/api", tags=["Decision Engine"])


# ============================================================================
# Request Models
# ============================================================================

class DecisionRequest(BaseModel):
    """Request model for making pipeline decisions"""
    dataset_meta_features: Dict[str, Any]
    problem_type: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/decide-pipeline")
async def decide_pipeline(request: DecisionRequest) -> Dict[str, Any]:
    """
    Make a decision on the best ML pipeline for the dataset
    
    This endpoint uses rule-based logic to analyze dataset characteristics
    and recommend the optimal pipeline, models, and preprocessing steps.
    
    Args:
        request: Dataset meta-features and optional problem type/constraints
        
    Returns:
        Decision with recommended pipelines and reasoning
    """
    try:
        logger.info("Making pipeline decision")
        
        decision = decision_engine.decide_pipeline(
            dataset_meta_features=request.dataset_meta_features,
            problem_type=request.problem_type,
            constraints=request.constraints,
        )
        
        return {
            "status": "success",
            "message": "Pipeline decision made successfully",
            "decision": decision,
        }
        
    except Exception as e:
        logger.error(f"Error making pipeline decision: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect-problem-type")
async def detect_problem_type(meta_features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detect the problem type (classification, regression, clustering, etc.)
    
    Args:
        meta_features: Dataset meta-features
        
    Returns:
        Detected problem type with confidence
    """
    try:
        logger.info("Detecting problem type")
        
        problem_type = decision_engine._detect_problem_type(meta_features)
        
        return {
            "status": "success",
            "problem_type": problem_type,
            "confidence": 0.85,  # Rule-based detection
        }
        
    except Exception as e:
        logger.error(f"Error detecting problem type: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-characteristics")
async def analyze_characteristics(meta_features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze and categorize dataset characteristics
    
    Args:
        meta_features: Dataset meta-features
        
    Returns:
        Categorized dataset characteristics
    """
    try:
        logger.info("Analyzing dataset characteristics")
        
        characteristics = decision_engine._analyze_dataset_characteristics(meta_features)
        
        return {
            "status": "success",
            "characteristics": characteristics,
        }
        
    except Exception as e:
        logger.error(f"Error analyzing characteristics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-pipeline-recommendations")
async def get_pipeline_recommendations(
    meta_features: Dict[str, Any],
    problem_type: str,
    constraints: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Get recommended pipelines for specific problem type
    
    Args:
        meta_features: Dataset meta-features
        problem_type: Classification, regression, clustering, etc.
        constraints: Optional constraints (interpretability, speed, etc.)
        
    Returns:
        Ranked list of recommended pipelines with scores
    """
    try:
        logger.info(f"Getting pipeline recommendations for {problem_type}")
        
        characteristics = decision_engine._analyze_dataset_characteristics(meta_features)
        pipelines = decision_engine._recommend_pipelines(characteristics, problem_type, constraints)
        
        return {
            "status": "success",
            "problem_type": problem_type,
            "count": len(pipelines),
            "pipelines": pipelines,
        }
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/decision-history")
async def get_decision_history(limit: int = 10) -> Dict[str, Any]:
    """
    Get recent decision history
    
    Args:
        limit: Number of recent decisions to retrieve (default: 10)
        
    Returns:
        List of recent decisions made
    """
    try:
        logger.info("Retrieving decision history")
        
        history = decision_engine.get_decision_history(limit=limit)
        
        return {
            "status": "success",
            "count": len(history),
            "decisions": history,
        }
        
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
