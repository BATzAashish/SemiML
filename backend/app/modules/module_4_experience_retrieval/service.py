"""
Module 4: Experience Retrieval Service
Stores and retrieves past pipeline experiences and similar datasets
Implements RAG (Retrieval-Augmented Generation) knowledge base for ML pipelines
"""
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
from app.logging_config import logger
from app.config import UPLOAD_DIR

# Experience storage directory
EXPERIENCES_DIR = Path(UPLOAD_DIR) / "experiences"
EXPERIENCES_DIR.mkdir(exist_ok=True)


class ExperienceRetriever:
    """
    Manages and retrieves past ML pipeline experiences and best practices
    """

    def __init__(self):
        self.experiences: List[Dict[str, Any]] = []
        self.best_practices: Dict[str, List[str]] = {}
        self._load_experiences_from_disk()
        logger.info("ExperienceRetriever initialized")

    def _load_experiences_from_disk(self):
        """Load existing experiences from disk"""
        try:
            experiences_file = EXPERIENCES_DIR / "experiences.json"
            if experiences_file.exists():
                with open(experiences_file, 'r') as f:
                    self.experiences = json.load(f)
                logger.info(f"Loaded {len(self.experiences)} experiences from disk")
            else:
                self.experiences = []
        except Exception as e:
            logger.error(f"Error loading experiences: {str(e)}")
            self.experiences = []

    def _save_experiences_to_disk(self):
        """Save experiences to disk"""
        try:
            experiences_file = EXPERIENCES_DIR / "experiences.json"
            with open(experiences_file, 'w') as f:
                json.dump(self.experiences, f, indent=2, default=str)
            logger.info("Experiences saved to disk")
        except Exception as e:
            logger.error(f"Error saving experiences: {str(e)}")

    def store_pipeline_experience(
        self,
        dataset_id: str,
        pipeline_type: str,
        model_name: str,
        hyperparameters: Dict[str, Any],
        performance_metrics: Dict[str, float],
        dataset_meta_features: Dict[str, Any],
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Store a completed pipeline experience
        
        Args:
            dataset_id: Dataset used for training
            pipeline_type: Type of pipeline (classification, regression, clustering)
            model_name: Name of the model used
            hyperparameters: Model hyperparameters
            performance_metrics: Performance metrics (accuracy, rmse, etc.)
            dataset_meta_features: Meta-features of the dataset
            notes: Additional notes about the experience
            
        Returns:
            Experience record with unique experience_id
        """
        try:
            experience_id = f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            experience = {
                "experience_id": experience_id,
                "dataset_id": dataset_id,
                "pipeline_type": pipeline_type,
                "model_name": model_name,
                "hyperparameters": hyperparameters,
                "performance_metrics": performance_metrics,
                "dataset_meta_features": dataset_meta_features,
                "notes": notes,
                "timestamp": datetime.now().isoformat(),
            }
            
            self.experiences.append(experience)
            self._save_experiences_to_disk()
            
            logger.info(f"Stored pipeline experience {experience_id}")
            return experience
            
        except Exception as e:
            logger.error(f"Error storing pipeline experience: {str(e)}")
            raise

    def find_similar_datasets(
        self,
        query_meta_features: Dict[str, Any],
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Find similar datasets from past experiences
        
        Args:
            query_meta_features: Meta-features of query dataset
            top_k: Number of similar datasets to return
            
        Returns:
            List of similar experiences ranked by similarity score
        """
        try:
            logger.info(f"Searching for {top_k} similar datasets")
            
            similarities = []
            
            for experience in self.experiences:
                similarity = self._compute_similarity(
                    query_meta_features,
                    experience["dataset_meta_features"]
                )
                similarities.append({
                    "experience": experience,
                    "similarity_score": similarity,
                })
            
            # Sort by similarity score (descending)
            similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            return [s["experience"] for s in similarities[:top_k]]
            
        except Exception as e:
            logger.error(f"Error finding similar datasets: {str(e)}")
            raise

    def get_best_practices(self, dataset_meta_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get best practices and recommendations for dataset characteristics
        
        Args:
            dataset_meta_features: Meta-features of the dataset
            
        Returns:
            Dictionary with best practices and recommendations
        """
        try:
            logger.info("Generating best practices")
            
            recommendations = {
                "preprocessing": [],
                "model_suggestions": [],
                "hyperparameter_tips": [],
            }
            
            num_rows = dataset_meta_features.get("basic_info", {}).get("num_rows", 0)
            num_cols = dataset_meta_features.get("basic_info", {}).get("num_columns", 0)
            numeric_cols = dataset_meta_features.get("feature_analysis", {}).get("numeric_columns", 0)
            
            # Size-based recommendations
            if num_rows < 1000:
                recommendations["preprocessing"].append("Small dataset - use cross-validation to maximize data usage")
                recommendations["model_suggestions"].append("Consider simple models to avoid overfitting")
            elif num_rows > 100000:
                recommendations["preprocessing"].append("Large dataset - consider stratified sampling")
                recommendations["model_suggestions"].append("Gradient boosting methods may be efficient")
            
            # Feature-based recommendations
            if numeric_cols > 50:
                recommendations["preprocessing"].append("High dimensionality - consider feature selection or PCA")
                recommendations["hyperparameter_tips"].append("Use regularization (L1/L2) to prevent overfitting")
            elif numeric_cols < 5:
                recommendations["preprocessing"].append("Low feature count - focus on feature engineering")
            
            # Data quality recommendations
            missing_pct = dataset_meta_features.get("missing_data_analysis", {}).get("missing_percentage_total", 0)
            if missing_pct > 10:
                recommendations["preprocessing"].append("Handle missing values - consider imputation or removal")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating best practices: {str(e)}")
            raise

    def get_best_models_for_dataset(
        self,
        dataset_meta_features: Dict[str, Any],
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Get best performing models for similar datasets
        
        Args:
            dataset_meta_features: Meta-features of the dataset
            top_k: Number of top models to return
            
        Returns:
            List of best performing models for similar datasets
        """
        try:
            logger.info(f"Finding best models for dataset")
            
            similar_exps = self.find_similar_datasets(dataset_meta_features, top_k=10)
            
            # Rank by performance
            ranked = sorted(
                similar_exps,
                key=lambda x: x["performance_metrics"].get("accuracy", 0) or 
                             x["performance_metrics"].get("r2_score", 0) or
                             x["performance_metrics"].get("silhouette_score", 0),
                reverse=True
            )
            
            best_models = []
            for exp in ranked[:top_k]:
                best_models.append({
                    "model_name": exp["model_name"],
                    "pipeline_type": exp["pipeline_type"],
                    "hyperparameters": exp["hyperparameters"],
                    "performance_metrics": exp["performance_metrics"],
                    "similarity_score": self._compute_similarity(
                        dataset_meta_features,
                        exp["dataset_meta_features"]
                    ),
                })
            
            return best_models
            
        except Exception as e:
            logger.error(f"Error getting best models: {str(e)}")
            raise

    def search_experiences(
        self,
        pipeline_type: Optional[str] = None,
        model_name: Optional[str] = None,
        min_performance: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search experiences with filters
        
        Args:
            pipeline_type: Filter by pipeline type (classification, regression, etc.)
            model_name: Filter by model name
            min_performance: Minimum performance threshold
            
        Returns:
            Filtered list of experiences
        """
        try:
            logger.info("Searching experiences with filters")
            
            results = self.experiences.copy()
            
            if pipeline_type:
                results = [e for e in results if e["pipeline_type"] == pipeline_type]
            
            if model_name:
                results = [e for e in results if e["model_name"] == model_name]
            
            if min_performance is not None:
                results = [
                    e for e in results 
                    if max(e["performance_metrics"].values()) >= min_performance
                ]
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching experiences: {str(e)}")
            raise

    def get_experience_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about stored experiences
        
        Returns:
            Dictionary with experience statistics
        """
        try:
            logger.info("Computing experience statistics")
            
            if not self.experiences:
                return {
                    "total_experiences": 0,
                    "models_count": 0,
                    "pipeline_types": [],
                    "avg_best_accuracy": 0,
                }
            
            # Collect statistics
            models = set()
            pipeline_types = set()
            accuracies = []
            
            for exp in self.experiences:
                models.add(exp["model_name"])
                pipeline_types.add(exp["pipeline_type"])
                
                # Get best metric value
                perf = exp["performance_metrics"]
                if "accuracy" in perf:
                    accuracies.append(perf["accuracy"])
                elif "r2_score" in perf:
                    accuracies.append(perf["r2_score"])
            
            avg_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0
            
            return {
                "total_experiences": len(self.experiences),
                "unique_models": len(models),
                "unique_pipeline_types": len(pipeline_types),
                "pipeline_types": list(pipeline_types),
                "models_used": list(models),
                "avg_best_accuracy": round(avg_accuracy, 4),
                "total_datasets_trained_on": len(set(e["dataset_id"] for e in self.experiences)),
            }
            
        except Exception as e:
            logger.error(f"Error computing statistics: {str(e)}")
            raise

    @staticmethod
    def _compute_similarity(features_1: Dict[str, Any], features_2: Dict[str, Any]) -> float:
        """
        Compute similarity between two datasets based on meta-features
        
        Uses Euclidean distance on normalized numeric features
        
        Returns:
            Similarity score between 0 and 1 (1 = identical)
        """
        try:
            # Extract basic info for comparison
            basic_1 = features_1.get("basic_info", {})
            basic_2 = features_2.get("basic_info", {})
            
            if not basic_1 or not basic_2:
                return 0.0
            
            # Normalize dimensions for comparison
            rows_1, rows_2 = basic_1.get("num_rows", 1), basic_2.get("num_rows", 1)
            cols_1, cols_2 = basic_1.get("num_columns", 1), basic_2.get("num_columns", 1)
            
            # Normalize to 0-1 range
            max_rows = max(rows_1, rows_2, 1000)
            max_cols = max(cols_1, cols_2, 100)
            
            row_sim = 1 - (abs(rows_1 - rows_2) / max_rows)
            col_sim = 1 - (abs(cols_1 - cols_2) / max_cols)
            
            # Also compare numeric column counts
            num_1 = features_1.get("feature_analysis", {}).get("numeric_columns", 0)
            num_2 = features_2.get("feature_analysis", {}).get("numeric_columns", 0)
            max_numeric = max(num_1, num_2, 1)
            numeric_sim = 1 - (abs(num_1 - num_2) / max_numeric)
            
            # Average similarity
            similarity = (row_sim + col_sim + numeric_sim) / 3
            return round(max(0.0, similarity), 4)
            
        except Exception:
            return 0.0


# Initialize global instance
experience_retriever = ExperienceRetriever()
