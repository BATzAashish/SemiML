"""
Module 3: Meta-Features Extraction Router
Provides endpoints for extracting and analyzing dataset meta-features
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import pandas as pd
from pathlib import Path

from app.modules.module_2_data_processing.service import data_processor
from app.modules.module_3_meta_features.service import meta_features_extractor
from app.logging_config import logger
from app.config import UPLOAD_DIR

router = APIRouter(prefix="/api", tags=["Meta-Features Extraction"])


@router.post("/extract-meta-features/{dataset_id}")
async def extract_meta_features(dataset_id: str) -> Dict[str, Any]:
    """
    Extract meta-features from a dataset
    
    Args:
        dataset_id: The UUID of the dataset
        
    Returns:
        Dictionary containing all meta-features
    """
    try:
        logger.info(f"Extracting meta-features for dataset {dataset_id}")
        
        # Get dataset info
        dataset_info = data_processor.get_dataset_info(dataset_id)
        if not dataset_info:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
        
        # Load the dataset
        file_path = dataset_info.get("file_path")
        df, _ = data_processor.load_and_validate_data(file_path)
        
        # Extract meta-features
        meta_features = meta_features_extractor.extract_meta_features(df, dataset_id)
        
        return {
            "status": "success",
            "message": "Meta-features extracted successfully",
            "meta_features": meta_features,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting meta-features: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error extracting meta-features: {str(e)}")


@router.get("/meta-features/{dataset_id}")
async def get_meta_features(dataset_id: str) -> Dict[str, Any]:
    """
    Get previously extracted meta-features for a dataset
    
    Args:
        dataset_id: The UUID of the dataset
        
    Returns:
        Meta-features dictionary
    """
    try:
        logger.info(f"Fetching meta-features for dataset {dataset_id}")
        
        # Get dataset info
        dataset_info = data_processor.get_dataset_info(dataset_id)
        if not dataset_info:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
        
        # Load the dataset
        file_path = dataset_info.get("file_path")
        df, _ = data_processor.load_and_validate_data(file_path)
        
        # Extract meta-features
        meta_features = meta_features_extractor.extract_meta_features(df, dataset_id)
        
        return {
            "status": "success",
            "data": meta_features,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching meta-features: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching meta-features: {str(e)}")


@router.get("/data-preview/{dataset_id}")
async def get_data_preview(dataset_id: str, rows: int = 10) -> Dict[str, Any]:
    """
    Get a preview of the dataset (first N rows)
    
    Args:
        dataset_id: The UUID of the dataset
        rows: Number of rows to preview (default 10)
        
    Returns:
        DataFrame preview as JSON
    """
    try:
        logger.info(f"Fetching data preview for dataset {dataset_id}")
        
        if rows > 100:
            rows = 100  # Limit to 100 rows for performance
        
        # Get dataset info
        dataset_info = data_processor.get_dataset_info(dataset_id)
        if not dataset_info:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
        
        # Load the dataset
        file_path = dataset_info.get("file_path")
        df, _ = data_processor.load_and_validate_data(file_path)
        
        # Get preview
        preview_df = df.head(rows)
        preview_data = preview_df.to_dict(orient="records")
        
        return {
            "status": "success",
            "dataset_id": dataset_id,
            "rows_shown": len(preview_data),
            "total_rows": len(df),
            "columns": list(df.columns),
            "data": preview_data,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting data preview: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting data preview: {str(e)}")


@router.get("/dataset-summary/{dataset_id}")
async def get_dataset_summary(dataset_id: str) -> Dict[str, Any]:
    """
    Get comprehensive dataset summary (metadata + meta-features)
    
    Args:
        dataset_id: The UUID of the dataset
        
    Returns:
        Complete dataset summary
    """
    try:
        logger.info(f"Fetching comprehensive summary for dataset {dataset_id}")
        
        # Get dataset info
        dataset_info = data_processor.get_dataset_info(dataset_id)
        if not dataset_info:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
        
        # Load the dataset
        file_path = dataset_info.get("file_path")
        df, _ = data_processor.load_and_validate_data(file_path)
        
        # Extract meta-features
        meta_features = meta_features_extractor.extract_meta_features(df, dataset_id)
        
        # Check if ready for modeling
        is_ready_for_modeling = meta_features_extractor.extract_feature_importance_ready(df)
        
        return {
            "status": "success",
            "summary": {
                "dataset_id": dataset_id,
                "filename": dataset_info.get("filename"),
                "file_size_mb": dataset_info.get("file_size", 0) / (1024 * 1024),
                "metadata": dataset_info.get("data_metadata", {}),
                "meta_features": meta_features,
                "ready_for_modeling": is_ready_for_modeling,
                "recommendations": [
                    "Handle missing values before modeling" if meta_features["missing_data_analysis"]["has_missing_values"] else "No missing values detected",
                    "Consider feature engineering" if meta_features["feature_analysis"]["numeric_columns"] > 5 else "Feature set is manageable",
                    "Normalize numerical features" if meta_features["feature_analysis"]["numeric_columns"] > 0 else "No numerical features",
                ],
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting dataset summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting dataset summary: {str(e)}")


@router.post("/compare-datasets")
async def compare_datasets(dataset_1_id: str, dataset_2_id: str) -> Dict[str, Any]:
    """
    Compare meta-features of two datasets
    
    Args:
        dataset_1_id: First dataset UUID
        dataset_2_id: Second dataset UUID
        
    Returns:
        Comparison analysis
    """
    try:
        logger.info(f"Comparing datasets {dataset_1_id} and {dataset_2_id}")
        
        # Get dataset 1
        dataset_info_1 = data_processor.get_dataset_info(dataset_1_id)
        if not dataset_info_1:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_1_id} not found")
        
        # Get dataset 2
        dataset_info_2 = data_processor.get_dataset_info(dataset_2_id)
        if not dataset_info_2:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_2_id} not found")
        
        # Load datasets
        file_path_1 = dataset_info_1.get("file_path")
        df_1, _ = data_processor.load_and_validate_data(file_path_1)
        
        file_path_2 = dataset_info_2.get("file_path")
        df_2, _ = data_processor.load_and_validate_data(file_path_2)
        
        # Extract meta-features
        meta_features_1 = meta_features_extractor.extract_meta_features(df_1, dataset_1_id)
        meta_features_2 = meta_features_extractor.extract_meta_features(df_2, dataset_2_id)
        
        # Compare
        comparison = meta_features_extractor.compare_datasets(meta_features_1, meta_features_2)
        
        return {
            "status": "success",
            "message": "Datasets compared successfully",
            "comparison": comparison,
            "meta_features_1": meta_features_1,
            "meta_features_2": meta_features_2,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error comparing datasets: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error comparing datasets: {str(e)}")
