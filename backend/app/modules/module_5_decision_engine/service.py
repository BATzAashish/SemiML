"""
Module 5: Decision Engine Service
Rule-based pipeline selection and decision making for ML workflows
Selects optimal pipeline based on dataset characteristics and problem type
"""
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from app.logging_config import logger


class ProblemType(str, Enum):
    """Supported problem types"""
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"
    ANOMALY_DETECTION = "anomaly_detection"
    UNDEFINED = "undefined"


class DecisionEngine:
    """
    Rule-based decision engine for selecting ML pipelines
    Makes decisions based on dataset characteristics, problem type, and constraints
    """

    def __init__(self):
        logger.info("DecisionEngine initialized")
        self.decision_history: List[Dict[str, Any]] = []

    def decide_pipeline(
        self,
        dataset_meta_features: Dict[str, Any],
        problem_type: Optional[str] = None,
        constraints: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a decision on the best pipeline for the dataset
        
        Args:
            dataset_meta_features: Meta-features of the dataset
            problem_type: Classification, regression, clustering, etc.
            constraints: Optional constraints (max_time, max_memory, interpretability, etc.)
            
        Returns:
            Decision with recommended pipeline, models, and reasoning
        """
        try:
            logger.info("Making pipeline decision")
            
            # Determine problem type if not provided
            if not problem_type:
                problem_type = self._detect_problem_type(dataset_meta_features)
            
            # Extract dataset characteristics
            characteristics = self._analyze_dataset_characteristics(dataset_meta_features)
            
            # Get pipeline recommendations
            pipelines = self._recommend_pipelines(characteristics, problem_type, constraints)
            
            # Select best pipeline
            best_pipeline = pipelines[0] if pipelines else {}
            
            # Generate reasoning
            reasoning = self._generate_reasoning(characteristics, problem_type, best_pipeline)
            
            decision = {
                "problem_type": problem_type,
                "dataset_characteristics": characteristics,
                "recommended_pipelines": pipelines,
                "best_pipeline": best_pipeline,
                "reasoning": reasoning,
            }
            
            self.decision_history.append(decision)
            logger.info(f"Pipeline decision: {best_pipeline.get('name', 'Unknown')}")
            
            return decision
            
        except Exception as e:
            logger.error(f"Error making pipeline decision: {str(e)}")
            raise

    def _detect_problem_type(self, meta_features: Dict[str, Any]) -> str:
        """
        Detect problem type based on dataset characteristics
        
        Returns:
            Problem type: classification, regression, clustering, or anomaly_detection
        """
        try:
            # Get potential target columns
            potential_targets = meta_features.get("class_distribution", {}).get("potential_target_columns", [])
            
            if not potential_targets:
                return ProblemType.CLUSTERING.value
            
            target = potential_targets[0]
            unique_values = target.get("unique_values", 0)
            
            # Classification: 2-20 unique values
            if 2 <= unique_values <= 20:
                return ProblemType.CLASSIFICATION.value
            # Regression: >20 unique values or continuous data
            elif unique_values > 20:
                return ProblemType.REGRESSION.value
            
            return ProblemType.UNDEFINED.value
            
        except Exception as e:
            logger.warning(f"Could not detect problem type: {str(e)}")
            return ProblemType.UNDEFINED.value

    def _analyze_dataset_characteristics(self, meta_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze key characteristics of the dataset
        
        Returns:
            Dictionary with dataset analysis
        """
        try:
            basic_info = meta_features.get("basic_info", {})
            feature_analysis = meta_features.get("feature_analysis", {})
            data_quality = meta_features.get("data_quality", {})
            
            num_rows = basic_info.get("num_rows", 0)
            num_cols = basic_info.get("num_columns", 0)
            numeric_cols = feature_analysis.get("numeric_columns", 0)
            categorical_cols = feature_analysis.get("categorical_columns", 0)
            
            return {
                "dataset_size": self._categorize_size(num_rows),
                "num_rows": num_rows,
                "num_columns": num_cols,
                "dimensionality": self._categorize_dimensionality(num_cols),
                "feature_types": {
                    "numeric": numeric_cols,
                    "categorical": categorical_cols,
                },
                "data_quality": data_quality.get("overall_quality_score", 0),
                "missing_data": not data_quality.get("completeness_score", 100) < 100,
                "has_imbalance": False,  # Could be detected from class_distribution
            }
            
        except Exception as e:
            logger.error(f"Error analyzing characteristics: {str(e)}")
            return {}

    def _categorize_size(self, num_rows: int) -> str:
        """Categorize dataset size"""
        if num_rows < 1000:
            return "small"
        elif num_rows < 100000:
            return "medium"
        elif num_rows < 1000000:
            return "large"
        else:
            return "very_large"

    def _categorize_dimensionality(self, num_cols: int) -> str:
        """Categorize feature dimensionality"""
        if num_cols < 10:
            return "low"
        elif num_cols < 50:
            return "medium"
        elif num_cols < 200:
            return "high"
        else:
            return "very_high"

    def _recommend_pipelines(
        self,
        characteristics: Dict[str, Any],
        problem_type: str,
        constraints: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Recommend pipelines based on characteristics and problem type
        
        Returns:
            List of recommended pipelines ranked by score
        """
        try:
            pipelines = []
            dataset_size = characteristics.get("dataset_size", "medium")
            dimensionality = characteristics.get("dimensionality", "medium")
            data_quality = characteristics.get("data_quality", 80)
            
            if problem_type == ProblemType.CLASSIFICATION.value:
                pipelines = self._get_classification_pipelines(dataset_size, dimensionality)
            elif problem_type == ProblemType.REGRESSION.value:
                pipelines = self._get_regression_pipelines(dataset_size, dimensionality)
            elif problem_type == ProblemType.CLUSTERING.value:
                pipelines = self._get_clustering_pipelines(dataset_size, dimensionality)
            
            # Score and sort pipelines
            for pipeline in pipelines:
                score = self._score_pipeline(pipeline, characteristics, constraints)
                pipeline["score"] = score
            
            pipelines.sort(key=lambda x: x["score"], reverse=True)
            return pipelines
            
        except Exception as e:
            logger.error(f"Error recommending pipelines: {str(e)}")
            return []

    def _get_classification_pipelines(self, dataset_size: str, dimensionality: str) -> List[Dict[str, Any]]:
        """Get classification pipeline recommendations"""
        pipelines = [
            {
                "name": "Random Forest",
                "type": "tree-based",
                "models": ["RandomForest"],
                "preprocessing": ["handle_missing", "encode_categorical"],
                "best_for": ["medium_data", "mixed_features"],
                "interpretability": "medium",
                "training_time": "fast",
                "hyperparameters": {
                    "n_estimators": 100,
                    "max_depth": 10,
                    "min_samples_split": 2,
                },
            },
            {
                "name": "Gradient Boosting (XGBoost)",
                "type": "boosting",
                "models": ["XGBoost"],
                "preprocessing": ["handle_missing", "scale_features"],
                "best_for": ["any_size", "high_performance"],
                "interpretability": "low",
                "training_time": "medium",
                "hyperparameters": {
                    "learning_rate": 0.1,
                    "max_depth": 5,
                    "n_estimators": 100,
                },
            },
            {
                "name": "Logistic Regression",
                "type": "linear",
                "models": ["LogisticRegression"],
                "preprocessing": ["normalize_features", "encode_categorical"],
                "best_for": ["small_data", "interpretability"],
                "interpretability": "high",
                "training_time": "very_fast",
                "hyperparameters": {
                    "C": 1.0,
                    "solver": "lbfgs",
                    "max_iter": 1000,
                },
            },
            {
                "name": "SVM (Support Vector Machine)",
                "type": "kernel",
                "models": ["SVM"],
                "preprocessing": ["normalize_features", "encode_categorical"],
                "best_for": ["small_to_medium", "high_accuracy"],
                "interpretability": "low",
                "training_time": "slow",
                "hyperparameters": {
                    "kernel": "rbf",
                    "C": 1.0,
                    "gamma": "scale",
                },
            },
        ]
        
        if dataset_size == "small":
            return [p for p in pipelines if p["interpretability"] in ["high", "medium"]]
        elif dataset_size == "very_large":
            return [p for p in pipelines if p["training_time"] in ["fast", "very_fast"]]
        
        return pipelines

    def _get_regression_pipelines(self, dataset_size: str, dimensionality: str) -> List[Dict[str, Any]]:
        """Get regression pipeline recommendations"""
        pipelines = [
            {
                "name": "Linear Regression",
                "type": "linear",
                "models": ["LinearRegression"],
                "preprocessing": ["normalize_features", "handle_missing"],
                "best_for": ["small_to_medium", "interpretability"],
                "interpretability": "high",
                "training_time": "very_fast",
                "hyperparameters": {},
            },
            {
                "name": "Random Forest Regression",
                "type": "tree-based",
                "models": ["RandomForestRegressor"],
                "preprocessing": ["handle_missing"],
                "best_for": ["medium_data", "non_linear"],
                "interpretability": "medium",
                "training_time": "fast",
                "hyperparameters": {
                    "n_estimators": 100,
                    "max_depth": 10,
                },
            },
            {
                "name": "Gradient Boosting Regression",
                "type": "boosting",
                "models": ["XGBRegressor"],
                "preprocessing": ["handle_missing", "normalize_features"],
                "best_for": ["any_size", "high_performance"],
                "interpretability": "low",
                "training_time": "medium",
                "hyperparameters": {
                    "learning_rate": 0.1,
                    "max_depth": 5,
                    "n_estimators": 100,
                },
            },
            {
                "name": "Support Vector Regression",
                "type": "kernel",
                "models": ["SVR"],
                "preprocessing": ["normalize_features"],
                "best_for": ["high_accuracy", "small_to_medium"],
                "interpretability": "low",
                "training_time": "slow",
                "hyperparameters": {
                    "kernel": "rbf",
                    "C": 1.0,
                },
            },
        ]
        
        if dataset_size == "small":
            return pipelines[:2]
        elif dataset_size == "very_large":
            return [p for p in pipelines if p["training_time"] in ["fast", "very_fast"]]
        
        return pipelines

    def _get_clustering_pipelines(self, dataset_size: str, dimensionality: str) -> List[Dict[str, Any]]:
        """Get clustering pipeline recommendations"""
        pipelines = [
            {
                "name": "K-Means Clustering",
                "type": "center-based",
                "models": ["KMeans"],
                "preprocessing": ["normalize_features", "handle_missing"],
                "best_for": ["any_size", "interpretability"],
                "interpretability": "high",
                "training_time": "fast",
                "hyperparameters": {
                    "n_clusters": 3,
                    "init": "k-means++",
                    "n_init": 10,
                },
            },
            {
                "name": "DBSCAN Clustering",
                "type": "density-based",
                "models": ["DBSCAN"],
                "preprocessing": ["normalize_features"],
                "best_for": ["outlier_detection", "arbitrary_shapes"],
                "interpretability": "medium",
                "training_time": "medium",
                "hyperparameters": {
                    "eps": 0.5,
                    "min_samples": 5,
                },
            },
            {
                "name": "Hierarchical Clustering",
                "type": "hierarchical",
                "models": ["AgglomerativeClustering"],
                "preprocessing": ["normalize_features"],
                "best_for": ["dendrograms", "hierarchical_structure"],
                "interpretability": "high",
                "training_time": "medium",
                "hyperparameters": {
                    "n_clusters": 3,
                    "linkage": "ward",
                },
            },
        ]
        
        if dimensionality == "very_high":
            return [p for p in pipelines if p["type"] != "density-based"]
        
        return pipelines

    def _score_pipeline(
        self,
        pipeline: Dict[str, Any],
        characteristics: Dict[str, Any],
        constraints: Optional[Dict[str, Any]] = None,
    ) -> float:
        """
        Score a pipeline based on dataset characteristics and constraints
        
        Returns:
            Score between 0 and 100
        """
        try:
            score = 70.0  # Base score
            
            # Adjust for dataset size
            dataset_size = characteristics.get("dataset_size", "medium")
            if "very_large" in dataset_size and pipeline["training_time"] == "very_fast":
                score += 15
            elif "small" in dataset_size and pipeline["interpretability"] == "high":
                score += 10
            
            # Data quality bonus
            data_quality = characteristics.get("data_quality", 80)
            score += (data_quality - 80) * 0.1
            
            # Apply constraints
            if constraints:
                if constraints.get("interpretability_required") and pipeline["interpretability"] == "high":
                    score += 10
                if constraints.get("speed_required") and pipeline["training_time"] == "very_fast":
                    score += 10
            
            return round(min(100.0, max(0.0, score)), 2)
            
        except Exception as e:
            logger.error(f"Error scoring pipeline: {str(e)}")
            return 50.0

    def _generate_reasoning(
        self,
        characteristics: Dict[str, Any],
        problem_type: str,
        best_pipeline: Dict[str, Any],
    ) -> List[str]:
        """
        Generate human-readable reasoning for the decision
        
        Returns:
            List of reasoning statements
        """
        try:
            reasoning = []
            
            dataset_size = characteristics.get("dataset_size", "medium")
            dimensionality = characteristics.get("dimensionality", "medium")
            data_quality = characteristics.get("data_quality", 80)
            
            # Dataset size reasoning
            if dataset_size == "small":
                reasoning.append("Dataset is small - avoiding complex models to prevent overfitting")
            elif dataset_size == "very_large":
                reasoning.append("Large dataset - selected fast, scalable algorithm")
            
            # Problem type reasoning
            reasoning.append(f"Problem detected as {problem_type} task")
            
            # Pipeline selection reasoning
            if best_pipeline:
                reasoning.append(f"Selected {best_pipeline.get('name', 'Unknown')} for {problem_type}")
                reasoning.append(f"This pipeline offers {best_pipeline.get('interpretability', 'medium')} interpretability")
            
            # Data quality reasoning
            if data_quality < 80:
                reasoning.append("Lower data quality - recommend preprocessing and feature engineering")
            else:
                reasoning.append("High data quality - ready for model training")
            
            return reasoning
            
        except Exception as e:
            logger.error(f"Error generating reasoning: {str(e)}")
            return ["Unable to generate reasoning"]

    def get_decision_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent decision history"""
        return self.decision_history[-limit:]


# Initialize global instance
decision_engine = DecisionEngine()
