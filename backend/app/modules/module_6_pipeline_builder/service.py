"""
Module 6: Pipeline Builder Service
Builds scikit-learn pipelines dynamically from configuration
"""
from typing import Any, Dict, List, Optional, Tuple
import uuid

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.decomposition import PCA

from app.logging_config import logger


class PipelineBuilder:
    """Builds and stores sklearn pipelines"""

    def __init__(self):
        self._pipelines: Dict[str, Pipeline] = {}
        logger.info("PipelineBuilder initialized")

    def build_pipeline(
        self,
        problem_type: str,
        preprocessing_steps: List[str],
        model_name: str,
        model_params: Dict[str, Any],
        feature_engineering_steps: Optional[List[str]] = None,
        feature_types: Optional[Dict[str, List[str]]] = None,
    ) -> Tuple[str, Pipeline, Dict[str, Any]]:
        """
        Build a sklearn pipeline based on steps and feature types

        Returns:
            pipeline_id, pipeline, summary
        """
        numeric_features = (feature_types or {}).get("numerical", [])
        categorical_features = (feature_types or {}).get("categorical", [])

        preprocessor = self._build_preprocessor(
            preprocessing_steps,
            numeric_features,
            categorical_features,
        )

        fe_steps = self._build_feature_engineering(feature_engineering_steps or [])
        model = self._build_model(model_name, model_params)

        steps = [("preprocessor", preprocessor)]
        steps.extend(fe_steps)
        steps.append(("model", model))

        pipeline = Pipeline(steps=steps)
        pipeline_id = str(uuid.uuid4())
        self._pipelines[pipeline_id] = pipeline

        summary = {
            "problem_type": problem_type,
            "preprocessing": preprocessing_steps,
            "feature_engineering": feature_engineering_steps or [],
            "model": model_name,
            "model_params": model_params,
            "numeric_features": numeric_features,
            "categorical_features": categorical_features,
        }

        logger.info(f"Pipeline built: {pipeline_id} ({model_name})")
        return pipeline_id, pipeline, summary

    def get_pipeline(self, pipeline_id: str) -> Pipeline:
        if pipeline_id not in self._pipelines:
            raise KeyError(f"Pipeline {pipeline_id} not found")
        return self._pipelines[pipeline_id]

    def _build_preprocessor(
        self,
        preprocessing_steps: List[str],
        numeric_features: List[str],
        categorical_features: List[str],
    ) -> ColumnTransformer:
        transformers = []

        if numeric_features:
            numeric_pipeline_steps = []
            if "handle_missing" in preprocessing_steps:
                numeric_pipeline_steps.append(("imputer", SimpleImputer(strategy="median")))
            if "scale_features" in preprocessing_steps or "normalize_features" in preprocessing_steps:
                numeric_pipeline_steps.append(("scaler", StandardScaler()))
            if not numeric_pipeline_steps:
                numeric_pipeline_steps.append(("identity", "passthrough"))
            transformers.append((
                "numeric",
                Pipeline(steps=numeric_pipeline_steps),
                numeric_features,
            ))

        if categorical_features:
            categorical_pipeline_steps = []
            if "handle_missing" in preprocessing_steps:
                categorical_pipeline_steps.append(("imputer", SimpleImputer(strategy="most_frequent")))
            if "encode_categorical" in preprocessing_steps:
                categorical_pipeline_steps.append((
                    "encoder",
                    OneHotEncoder(handle_unknown="ignore"),
                ))
            if not categorical_pipeline_steps:
                categorical_pipeline_steps.append(("identity", "passthrough"))
            transformers.append((
                "categorical",
                Pipeline(steps=categorical_pipeline_steps),
                categorical_features,
            ))

        if not transformers:
            transformers.append(("all", "passthrough", slice(0, None)))

        return ColumnTransformer(transformers=transformers, remainder="drop")

    def _build_feature_engineering(self, steps: List[str]) -> List[tuple]:
        fe_steps = []
        if "pca" in steps:
            fe_steps.append(("pca", PCA(n_components=0.95)))
        return fe_steps

    def _build_model(self, model_name: str, params: Dict[str, Any]):
        model_name_lower = model_name.lower()

        if model_name_lower in ["logistic_regression", "logisticregression"]:
            from sklearn.linear_model import LogisticRegression
            return LogisticRegression(**params)

        if model_name_lower in ["random_forest", "randomforest"]:
            from sklearn.ensemble import RandomForestClassifier
            return RandomForestClassifier(**params)

        if model_name_lower in ["random_forest_regressor", "randomforestregressor"]:
            from sklearn.ensemble import RandomForestRegressor
            return RandomForestRegressor(**params)

        if model_name_lower in ["linear_regression", "linearregression"]:
            from sklearn.linear_model import LinearRegression
            return LinearRegression(**params)

        if model_name_lower in ["svm", "svc"]:
            from sklearn.svm import SVC
            return SVC(**params)

        if model_name_lower in ["svr"]:
            from sklearn.svm import SVR
            return SVR(**params)

        raise ValueError(f"Unsupported model: {model_name}")


pipeline_builder = PipelineBuilder()
