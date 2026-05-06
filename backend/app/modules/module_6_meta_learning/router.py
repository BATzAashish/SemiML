"""
Module 6: Meta-Learning & LLM Integration Router
Provides endpoints for meta-learning decisions and LLM-powered reasoning
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from app.modules.module_6_meta_learning.meta_learning import get_meta_learning_engine
from app.logging_config import logger

router = APIRouter(prefix="/api", tags=["Meta-Learning"])


# ============================================================================
# Request Models
# ============================================================================

class MetaDecisionRequest(BaseModel):
    """Request model for meta-learning decision"""
    dataset_features: Dict[str, Any]
    rule_based_decision: Optional[Dict[str, Any]] = None
    experience_based_decision: Optional[Dict[str, Any]] = None
    model_recommendations: List[Dict[str, Any]] = []


class DecisionOutcomeRequest(BaseModel):
    """Request model for recording decision outcome"""
    decision: Dict[str, Any]
    outcome: Dict[str, Any]
    actual_performance: float


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/meta-decision")
async def generate_meta_decision(request: MetaDecisionRequest) -> Dict[str, Any]:
    """
    Generate a meta-learning decision by combining multiple reasoning sources
    
    Uses rule-based reasoning, past experience, and LLM reasoning to make
    the best possible recommendation for the given dataset.
    
    Args:
        request: Dataset features and decision inputs from different sources
        
    Returns:
        Final meta-learning decision with confidence scores and recommendations
    """
    try:
        logger.info("Generating meta-learning decision")
        
        engine = get_meta_learning_engine()
        decision = engine.generate_meta_decision(
            dataset_features=request.dataset_features,
            rule_based_decision=request.rule_based_decision,
            experience_based_decision=request.experience_based_decision,
            model_recommendations=request.model_recommendations,
        )
        
        return decision
        
    except Exception as e:
        logger.error(f"Error generating meta decision: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/record-outcome")
async def record_decision_outcome(request: DecisionOutcomeRequest) -> Dict[str, Any]:
    """
    Record the outcome of a decision for meta-learning
    
    This helps the system learn from past decisions and improve future recommendations.
    
    Args:
        request: Decision, outcome, and actual performance
        
    Returns:
        Confirmation of outcome recording
    """
    try:
        logger.info("Recording decision outcome for meta-learning")
        
        engine = get_meta_learning_engine()
        success = engine.record_decision_outcome(
            decision=request.decision,
            outcome=request.outcome,
            actual_performance=request.actual_performance,
        )
        
        return {
            "status": "success" if success else "failed",
            "message": "Decision outcome recorded successfully" if success else "Failed to record outcome",
            "performance": request.actual_performance,
        }
        
    except Exception as e:
        logger.error(f"Error recording outcome: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/meta-insights")
async def get_meta_insights() -> Dict[str, Any]:
    """
    Get meta-learning insights from accumulated decision history
    
    Returns insights about system performance, trends, and recommendations
    based on historical decision outcomes.
    
    Returns:
        Meta-learning insights and performance trends
    """
    try:
        logger.info("Retrieving meta-insights")
        
        engine = get_meta_learning_engine()
        insights = engine.get_meta_insights()
        
        return {
            "status": "success",
            "insights": insights,
        }
        
    except Exception as e:
        logger.error(f"Error retrieving insights: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/llm-status")
async def get_llm_status() -> Dict[str, Any]:
    """
    Get status of LLM integration
    
    Returns whether LLM reasoning is available and which provider is active
    
    Returns:
        LLM status and available providers
    """
    try:
        logger.info("Retrieving LLM status")
        
        engine = get_meta_learning_engine()
        
        import os
        providers_available = {
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "google_gemini": bool(os.getenv("GOOGLE_API_KEY")),
            "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
        }
        
        active_provider = None
        if providers_available["openai"]:
            active_provider = "OpenAI"
        elif providers_available["google_gemini"]:
            active_provider = "Google Gemini"
        elif providers_available["anthropic"]:
            active_provider = "Anthropic Claude"
        
        return {
            "status": "success",
            "llm_enabled": engine.llm_available,
            "active_provider": active_provider,
            "available_providers": providers_available,
            "message": "LLM reasoning enabled" if engine.llm_available else "LLM reasoning disabled - using fallback reasoning",
        }
        
    except Exception as e:
        logger.error(f"Error getting LLM status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
