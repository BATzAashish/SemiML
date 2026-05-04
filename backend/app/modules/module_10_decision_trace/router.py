"""
Module 10: Decision Trace Router
API endpoints for decision trace logging and retrieval
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.logging_config import logger
from app.modules.module_10_decision_trace.service import decision_trace_service

router = APIRouter(prefix="/api", tags=["Decision Trace"])


class DecisionTraceRequest(BaseModel):
    decision: str
    reasoning: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    sources: Optional[List[str]] = None
    alternatives: Optional[List[Dict[str, Any]]] = None


@router.post("/decision-trace")
async def create_decision_trace(request: DecisionTraceRequest) -> Dict[str, Any]:
    """
    Store a decision trace record
    """
    try:
        logger.info("Recording decision trace")
        trace = decision_trace_service.add_trace(
            decision=request.decision,
            reasoning=request.reasoning,
            confidence=request.confidence,
            sources=request.sources,
            alternatives=request.alternatives,
        )
        return {
            "status": "success",
            "message": "Decision trace recorded",
            "trace": decision_trace_service._to_dict(trace),
        }
    except Exception as e:
        logger.error(f"Error recording decision trace: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/decision-trace")
async def list_decision_traces(limit: int = 50) -> Dict[str, Any]:
    """
    List decision trace records
    """
    try:
        traces = decision_trace_service.list_traces(limit=limit)
        return {
            "status": "success",
            "count": len(traces),
            "traces": traces,
        }
    except Exception as e:
        logger.error(f"Error listing decision traces: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/decision-trace/{trace_id}")
async def get_decision_trace(trace_id: str) -> Dict[str, Any]:
    """
    Get a decision trace by ID
    """
    try:
        trace = decision_trace_service.get_trace(trace_id)
        return {
            "status": "success",
            "trace": trace,
        }
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching decision trace: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
