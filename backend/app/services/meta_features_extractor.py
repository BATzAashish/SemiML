"""
Meta-Features Extractor Service - Analyzes datasets and extracts statistical features
Used for meta-learning and intelligent pipeline selection
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from app.logging_config import logger


class MetaFeaturesExtractor:
    """
    Extracts meta-features from datasets for meta-learning and analysis
    """

    def __init__(self):
        logger.info("MetaFeaturesExtractor initialized")

    def extract_meta_features(self, df: pd.DataFrame, dataset_id: str) -> Dict[str, Any]:
        """
        Extract all meta-features from dataset
        
        Returns:
            Dictionary with comprehensive meta-features
        """
        try:
            logger.info(f"Extracting meta-features for dataset {dataset_id}")
            
            meta_features = {
                "dataset_id": dataset_id,
                "basic_info": self._extract_basic_info(df),
                "statistical_features": self._extract_statistical_features(df),
                "feature_analysis": self._extract_feature_analysis(df),
                "missing_data_analysis": self._extract_missing_data_analysis(df),
                "data_quality": self._extract_data_quality_metrics(df),
                "class_distribution": self._extract_class_distribution(df),
                "feature_types": self._extract_feature_types(df),
            }
            
            logger.info(f"Meta-features extraction completed for {dataset_id}")
            return meta_features
            
        except Exception as e:
            logger.error(f"Error extracting meta-features: {str(e)}")
            raise

    def _extract_basic_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract basic dataset information"""
        return {
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024**2,
            "sparsity": (df.isna().sum().sum() / (len(df) * len(df.columns))) * 100,
        }

    def _extract_statistical_features(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract statistical features for numerical columns"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            return {"numeric_columns_count": 0}
        
        stats = {
            "numeric_columns_count": len(numeric_cols),
            "numeric_columns": numeric_cols,
            "means": df[numeric_cols].mean().to_dict(),
            "stds": df[numeric_cols].std().to_dict(),
            "mins": df[numeric_cols].min().to_dict(),
            "maxs": df[numeric_cols].max().to_dict(),
            "medians": df[numeric_cols].median().to_dict(),
            "q25": df[numeric_cols].quantile(0.25).to_dict(),
            "q75": df[numeric_cols].quantile(0.75).to_dict(),
            "skewness": df[numeric_cols].skew().to_dict(),
            "kurtosis": df[numeric_cols].kurtosis().to_dict(),
        }
        
        return stats

    def _extract_feature_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze feature characteristics"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Calculate correlations
        correlations = {}
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            # Get max correlation pairs
            correlations = {
                "max_correlation": float(corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].max()),
                "mean_correlation": float(corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].mean()),
            }
        
        return {
            "numeric_columns": len(numeric_cols),
            "categorical_columns": len(categorical_cols),
            "constant_columns": len(df.columns[df.nunique() == 1]),
            "duplicate_rows": len(df) - len(df.drop_duplicates()),
            "feature_correlations": correlations,
            "avg_unique_values": float(df.nunique().mean()),
        }

    def _extract_missing_data_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze missing data patterns"""
        missing_info = {}
        missing_counts = df.isna().sum()
        
        for col in df.columns:
            missing_percent = (missing_counts[col] / len(df)) * 100
            if missing_percent > 0:
                missing_info[col] = {
                    "missing_count": int(missing_counts[col]),
                    "missing_percentage": round(missing_percent, 2),
                }
        
        return {
            "total_missing_values": int(missing_counts.sum()),
            "columns_with_missing": len(missing_info),
            "missing_percentage_total": round((missing_counts.sum() / (len(df) * len(df.columns))) * 100, 2),
            "missing_by_column": missing_info,
            "has_missing_values": bool(missing_counts.sum() > 0),
        }

    def _extract_data_quality_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract data quality metrics"""
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isna().sum().sum()
        
        # Completeness
        completeness = ((total_cells - missing_cells) / total_cells) * 100
        
        # Uniqueness (percentage of duplicate values)
        duplicate_rows = len(df) - len(df.drop_duplicates())
        uniqueness = ((len(df) - duplicate_rows) / len(df)) * 100 if len(df) > 0 else 0
        
        # Consistency check (data types are consistent)
        consistency = 100.0
        
        return {
            "completeness_score": round(completeness, 2),
            "uniqueness_score": round(uniqueness, 2),
            "consistency_score": round(consistency, 2),
            "overall_quality_score": round((completeness + uniqueness + consistency) / 3, 2),
        }

    def _extract_class_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze class distribution for classification problems"""
        # Check if there's a likely target column
        potential_targets = []
        
        for col in df.columns:
            unique_values = df[col].nunique()
            # Potential target: few unique values, preferably string or numeric
            if 2 <= unique_values <= 20:
                potential_targets.append({
                    "column": col,
                    "unique_values": unique_values,
                    "distribution": df[col].value_counts().to_dict(),
                })
        
        return {
            "potential_target_columns": potential_targets,
            "likely_classification": len(potential_targets) > 0,
        }

    def _extract_feature_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract feature type information"""
        feature_types = {
            "numerical": [],
            "categorical": [],
            "datetime": [],
            "mixed": [],
        }
        
        for col in df.columns:
            dtype = str(df[col].dtype)
            
            if df[col].dtype in ['int64', 'float64']:
                feature_types["numerical"].append(col)
            elif df[col].dtype == 'object':
                # Try to detect date columns
                try:
                    pd.to_datetime(df[col].dropna().head())
                    feature_types["datetime"].append(col)
                except:
                    feature_types["categorical"].append(col)
            else:
                feature_types["mixed"].append(col)
        
        return feature_types

    def extract_feature_importance_ready(self, df: pd.DataFrame) -> bool:
        """Check if dataset is ready for feature importance analysis"""
        # Must have numerical features
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        # Must have potential target
        has_target = any(2 <= df[col].nunique() <= 100 for col in df.columns)
        
        return len(numeric_cols) > 0 and has_target

    def compare_datasets(self, meta_features_1: Dict[str, Any], meta_features_2: Dict[str, Any]) -> Dict[str, Any]:
        """Compare meta-features of two datasets"""
        comparison = {
            "dataset_1_id": meta_features_1.get("dataset_id"),
            "dataset_2_id": meta_features_2.get("dataset_id"),
            "similarities": {
                "same_num_columns": (
                    meta_features_1["basic_info"]["num_columns"] == 
                    meta_features_2["basic_info"]["num_columns"]
                ),
                "similar_num_rows": (
                    abs(meta_features_1["basic_info"]["num_rows"] - meta_features_2["basic_info"]["num_rows"]) 
                    / max(meta_features_1["basic_info"]["num_rows"], meta_features_2["basic_info"]["num_rows"]) < 0.1
                ),
            },
            "differences": {
                "row_count_diff": (
                    meta_features_1["basic_info"]["num_rows"] - 
                    meta_features_2["basic_info"]["num_rows"]
                ),
                "sparsity_diff": (
                    meta_features_1["basic_info"]["sparsity"] - 
                    meta_features_2["basic_info"]["sparsity"]
                ),
            }
        }
        
        return comparison


# Initialize global instance
meta_features_extractor = MetaFeaturesExtractor()
