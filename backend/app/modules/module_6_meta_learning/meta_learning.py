"""
Meta-Learning & LLM Integration Service
Uses meta-learning to improve decision confidence and integrates LLM reasoning
"""
import os
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from enum import Enum

from app.logging_config import logger

# Try to import LLM libraries
try:
    from langchain.llms import OpenAI, Anthropic
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

try:
    import google.generativeai as genai
    GOOGLE_GENAI_AVAILABLE = True
except ImportError:
    GOOGLE_GENAI_AVAILABLE = False


class ReasoningSource(str, Enum):
    """Enum for decision reasoning sources"""
    RULE_BASED = "rule_based"
    EXPERIENCE_BASED = "experience_based"
    LLM_BASED = "llm_based"
    META_LEARNING = "meta_learning"


@dataclass
class DecisionReasoning:
    """Structured decision reasoning from different sources"""
    source: ReasoningSource
    confidence: float
    reasoning: str
    supporting_data: Dict[str, Any]
    recommendation: str
    priority: int  # 1-5, higher = more important


class MetaLearningEngine:
    """
    Meta-learning engine that learns from past decisions and improves recommendations
    Also integrates LLM reasoning for complex decision scenarios
    """

    def __init__(self):
        """Initialize meta-learning engine"""
        self.decision_history = []
        self.model_performance_cache = {}
        self.llm_available = self._initialize_llm()
        logger.info(f"MetaLearningEngine initialized (LLM available: {self.llm_available})")

    def _initialize_llm(self) -> bool:
        """Initialize LLM integration"""
        try:
            # Check for available LLM providers
            if os.getenv("OPENAI_API_KEY"):
                logger.info("OpenAI API key found - LLM reasoning enabled")
                return True
            elif os.getenv("GOOGLE_API_KEY"):
                logger.info("Google API key found - LLM reasoning enabled via Gemini")
                genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                return True
            elif os.getenv("ANTHROPIC_API_KEY"):
                logger.info("Anthropic API key found - LLM reasoning enabled via Claude")
                return True
            else:
                logger.warning("No LLM API keys configured - using fallback reasoning")
                return False
        except Exception as e:
            logger.error(f"Error initializing LLM: {str(e)}")
            return False

    def generate_meta_decision(
        self,
        dataset_features: Dict[str, Any],
        rule_based_decision: Dict[str, Any],
        experience_based_decision: Dict[str, Any],
        model_recommendations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate final decision by combining multiple reasoning sources
        
        Args:
            dataset_features: Meta-features of the dataset
            rule_based_decision: Decision from rule-based system
            experience_based_decision: Decision from experience retrieval
            model_recommendations: List of recommended models
            
        Returns:
            Final meta-learning decision with confidence scores
        """
        try:
            logger.info("Generating meta-learning decision")
            
            # Collect reasoning from different sources
            reasonings = []
            
            # Rule-based reasoning
            rule_reasoning = self._extract_rule_based_reasoning(rule_based_decision)
            if rule_reasoning:
                reasonings.append(rule_reasoning)
            
            # Experience-based reasoning
            exp_reasoning = self._extract_experience_reasoning(experience_based_decision, model_recommendations)
            if exp_reasoning:
                reasonings.append(exp_reasoning)
            
            # LLM-based reasoning
            if self.llm_available:
                llm_reasoning = self._get_llm_reasoning(dataset_features, model_recommendations)
                if llm_reasoning:
                    reasonings.append(llm_reasoning)
            
            # Aggregate reasonings
            final_decision = self._aggregate_decisions(reasonings, model_recommendations)
            
            return {
                "status": "success",
                "final_decision": final_decision,
                "reasoning_sources": len(reasonings),
                "confidence_score": final_decision.get("overall_confidence", 0.0),
                "recommendations": final_decision.get("recommended_models", []),
            }
            
        except Exception as e:
            logger.error(f"Error generating meta decision: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "fallback": rule_based_decision,
            }

    def _extract_rule_based_reasoning(self, rule_decision: Dict[str, Any]) -> Optional[DecisionReasoning]:
        """Extract reasoning from rule-based system"""
        try:
            if not rule_decision:
                return None
            
            return DecisionReasoning(
                source=ReasoningSource.RULE_BASED,
                confidence=rule_decision.get("confidence", 0.7),
                reasoning=rule_decision.get("reasoning", ""),
                supporting_data=rule_decision.get("data", {}),
                recommendation=rule_decision.get("recommendation", ""),
                priority=3,
            )
        except Exception as e:
            logger.error(f"Error extracting rule-based reasoning: {str(e)}")
            return None

    def _extract_experience_reasoning(
        self,
        exp_decision: Dict[str, Any],
        model_recommendations: List[Dict[str, Any]]
    ) -> Optional[DecisionReasoning]:
        """Extract reasoning from past experiences"""
        try:
            if not model_recommendations:
                return None
            
            top_model = model_recommendations[0] if model_recommendations else {}
            
            return DecisionReasoning(
                source=ReasoningSource.EXPERIENCE_BASED,
                confidence=top_model.get("performance_score", 0.75),
                reasoning=f"Based on {len(model_recommendations)} similar past projects",
                supporting_data={"top_model": top_model},
                recommendation=f"Use {top_model.get('model_name', 'recommended model')} based on past performance",
                priority=4,
            )
        except Exception as e:
            logger.error(f"Error extracting experience reasoning: {str(e)}")
            return None

    def _get_llm_reasoning(
        self,
        dataset_features: Dict[str, Any],
        model_recommendations: List[Dict[str, Any]]
    ) -> Optional[DecisionReasoning]:
        """Get reasoning from LLM"""
        try:
            if not self.llm_available:
                return None
            
            # Build prompt for LLM
            prompt = self._build_llm_prompt(dataset_features, model_recommendations)
            
            # Get LLM response
            response = self._call_llm(prompt)
            
            if response:
                return DecisionReasoning(
                    source=ReasoningSource.LLM_BASED,
                    confidence=0.85,
                    reasoning="LLM analysis of data characteristics and model suitability",
                    supporting_data={"llm_response": response},
                    recommendation=response.get("recommendation", ""),
                    priority=5,  # Highest priority for LLM reasoning
                )
            return None
            
        except Exception as e:
            logger.error(f"Error getting LLM reasoning: {str(e)}")
            return None

    def _build_llm_prompt(self, dataset_features: Dict[str, Any], models: List[Dict[str, Any]]) -> str:
        """Build prompt for LLM reasoning"""
        models_str = "\n".join([
            f"- {m.get('model_name', 'Unknown')}: Accuracy {m.get('accuracy', 'N/A')}, Score {m.get('performance_score', 'N/A')}"
            for m in models[:3]
        ])
        
        prompt = f"""
        Analyze this ML dataset and recommend the best approach:
        
        Dataset characteristics:
        - Rows: {dataset_features.get('num_rows', 'Unknown')}
        - Columns: {dataset_features.get('num_columns', 'Unknown')}
        - Missing values: {dataset_features.get('missing_percentage', 'Unknown')}%
        - Data quality score: {dataset_features.get('data_quality_score', 'Unknown')}
        
        Top performing models from similar datasets:
        {models_str}
        
        Provide:
        1. Recommended model and why
        2. Key preprocessing steps
        3. Potential challenges
        4. Confidence in recommendation (0-1)
        """
        return prompt

    def _call_llm(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Call LLM with prompt"""
        try:
            if os.getenv("GOOGLE_API_KEY") and GOOGLE_GENAI_AVAILABLE:
                return self._call_google_gemini(prompt)
            elif os.getenv("OPENAI_API_KEY") and LANGCHAIN_AVAILABLE:
                return self._call_openai(prompt)
            else:
                return None
        except Exception as e:
            logger.error(f"Error calling LLM: {str(e)}")
            return None

    def _call_google_gemini(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Call Google Gemini LLM"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            
            return {
                "provider": "Google Gemini",
                "recommendation": response.text,
                "raw_response": response.text,
            }
        except Exception as e:
            logger.error(f"Error calling Gemini: {str(e)}")
            return None

    def _call_openai(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Call OpenAI LLM"""
        try:
            from langchain.llms import OpenAI
            llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = llm.predict(prompt)
            
            return {
                "provider": "OpenAI",
                "recommendation": response,
                "raw_response": response,
            }
        except Exception as e:
            logger.error(f"Error calling OpenAI: {str(e)}")
            return None

    def _aggregate_decisions(
        self,
        reasonings: List[DecisionReasoning],
        model_recommendations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Aggregate multiple reasoning sources into final decision"""
        if not reasonings:
            return {
                "status": "no_reasoning_available",
                "fallback_model": model_recommendations[0] if model_recommendations else None,
                "overall_confidence": 0.5,
            }
        
        # Sort by priority
        reasonings.sort(key=lambda r: r.priority, reverse=True)
        
        # Calculate weighted confidence
        weights = {
            ReasoningSource.LLM_BASED: 0.4,
            ReasoningSource.EXPERIENCE_BASED: 0.35,
            ReasoningSource.RULE_BASED: 0.25,
            ReasoningSource.META_LEARNING: 0.3,
        }
        
        weighted_confidence = sum(
            r.confidence * weights.get(r.source, 0.25) for r in reasonings
        ) / len(reasonings) if reasonings else 0.5
        
        # Combine recommendations
        recommendations = [r.recommendation for r in reasonings if r.recommendation]
        
        # Combine reasoning explanations
        combined_reasoning = " | ".join([
            f"{r.source.value}: {r.reasoning}" for r in reasonings[:3]
        ])
        
        return {
            "status": "success",
            "overall_confidence": float(weighted_confidence),
            "reasoning_summary": combined_reasoning,
            "recommended_models": model_recommendations[:3],
            "reasoning_sources": [r.source.value for r in reasonings],
            "primary_recommendation": reasonings[0].recommendation if reasonings else "Use recommended model",
        }

    def record_decision_outcome(
        self,
        decision: Dict[str, Any],
        outcome: Dict[str, Any],
        actual_performance: float
    ) -> bool:
        """
        Record decision outcome for meta-learning
        
        Args:
            decision: The decision made
            outcome: The outcome of the decision
            actual_performance: Actual model performance achieved
            
        Returns:
            True if recorded successfully
        """
        try:
            record = {
                "decision": decision,
                "outcome": outcome,
                "actual_performance": actual_performance,
                "timestamp": str(np.datetime64('now')),
            }
            self.decision_history.append(record)
            logger.info(f"Decision outcome recorded. Performance: {actual_performance}")
            return True
        except Exception as e:
            logger.error(f"Error recording decision outcome: {str(e)}")
            return False

    def get_meta_insights(self) -> Dict[str, Any]:
        """Get insights from accumulated meta-learning history"""
        if not self.decision_history:
            return {
                "status": "no_history",
                "message": "Not enough decision history for meta-insights",
            }
        
        performances = [d.get("actual_performance", 0) for d in self.decision_history]
        
        return {
            "status": "success",
            "total_decisions": len(self.decision_history),
            "average_performance": float(np.mean(performances)),
            "best_performance": float(np.max(performances)),
            "worst_performance": float(np.min(performances)),
            "performance_std": float(np.std(performances)),
            "improvement_trend": self._calculate_trend(performances),
        }

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend from performance values"""
        if len(values) < 2:
            return "insufficient_data"
        
        recent = np.mean(values[-5:])
        historical = np.mean(values[:-5]) if len(values) > 5 else recent
        
        if recent > historical * 1.05:
            return "improving"
        elif recent < historical * 0.95:
            return "declining"
        else:
            return "stable"


# Global meta-learning engine instance
meta_engine: Optional[MetaLearningEngine] = None


def get_meta_learning_engine() -> MetaLearningEngine:
    """Get or initialize meta-learning engine"""
    global meta_engine
    if meta_engine is None:
        meta_engine = MetaLearningEngine()
    return meta_engine
