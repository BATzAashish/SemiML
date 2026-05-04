"""
Module 10: Decision Trace Service
Stores and retrieves decision traces for explainability and auditing
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import uuid

from app.config import UPLOAD_DIR
from app.logging_config import logger


TRACE_DIR = Path(UPLOAD_DIR) / "decision_traces"
TRACE_DIR.mkdir(exist_ok=True)
TRACE_FILE = TRACE_DIR / "traces.json"


@dataclass
class TraceRecord:
    trace_id: str
    timestamp: str
    decision: str
    reasoning: List[str]
    confidence: float
    sources: List[str]
    alternatives: List[Dict[str, Any]]


class DecisionTraceService:
    """Manages decision trace records"""

    def __init__(self):
        self._traces: List[TraceRecord] = []
        self._load_traces()
        logger.info("DecisionTraceService initialized")

    def add_trace(
        self,
        decision: str,
        reasoning: List[str],
        confidence: float,
        sources: Optional[List[str]] = None,
        alternatives: Optional[List[Dict[str, Any]]] = None,
    ) -> TraceRecord:
        trace = TraceRecord(
            trace_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            sources=sources or [],
            alternatives=alternatives or [],
        )

        self._traces.append(trace)
        self._save_traces()
        logger.info(f"Decision trace recorded: {trace.trace_id}")
        return trace

    def list_traces(self, limit: int = 50) -> List[Dict[str, Any]]:
        traces = self._traces[-limit:]
        return [self._to_dict(t) for t in traces]

    def get_trace(self, trace_id: str) -> Dict[str, Any]:
        for trace in self._traces:
            if trace.trace_id == trace_id:
                return self._to_dict(trace)
        raise KeyError(f"Trace {trace_id} not found")

    def _load_traces(self) -> None:
        if not TRACE_FILE.exists():
            return
        try:
            with open(TRACE_FILE, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            self._traces = [TraceRecord(**item) for item in data]
        except Exception as exc:
            logger.error(f"Failed to load traces: {exc}")
            self._traces = []

    def _save_traces(self) -> None:
        try:
            with open(TRACE_FILE, "w", encoding="utf-8") as handle:
                json.dump([self._to_dict(t) for t in self._traces], handle, indent=2)
        except Exception as exc:
            logger.error(f"Failed to save traces: {exc}")

    @staticmethod
    def _to_dict(record: TraceRecord) -> Dict[str, Any]:
        return {
            "trace_id": record.trace_id,
            "timestamp": record.timestamp,
            "decision": record.decision,
            "reasoning": record.reasoning,
            "confidence": record.confidence,
            "sources": record.sources,
            "alternatives": record.alternatives,
        }


decision_trace_service = DecisionTraceService()
