"""
Data Processing Router - API endpoints for dataset upload and management
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.logging_config import logger
from app.services.data_processor import data_processor
from app.models.schemas import DatasetMetadata

router = APIRouter(prefix="/api", tags=["Data Processing"])


@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...), description: str = ""):
    """
    Upload and process a dataset
    Accepts: CSV, XLSX, JSON, Parquet files
    Returns: dataset_id and file information
    """
    try:
        logger.info(f"Dataset upload started: {file.filename}")

        # Read file content
        content = await file.read()

        # Validate file
        is_valid, error_msg = data_processor.validate_file(file.filename, content)
        if not is_valid:
            logger.warning(f"File validation failed: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)

        # Save file
        dataset_id, file_path = data_processor.save_file(file.filename, content)

        # Load and validate data
        df, metadata = data_processor.load_and_validate_data(file_path)

        logger.info(f"Dataset uploaded successfully: {dataset_id}")

        return {
            "status": "success",
            "dataset_id": dataset_id,
            "filename": file.filename,
            "file_path": file_path,
            "file_size": len(content),
            "description": description,
            "data_summary": {
                "num_rows": metadata["num_rows"],
                "num_columns": metadata["num_columns"],
                "columns": metadata["columns"],
                "missing_values": metadata["missing_values"],
                "duplicates": metadata["duplicates"],
            },
            "message": f"Dataset uploaded successfully. ID: {dataset_id}",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading dataset: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading dataset: {str(e)}")


@router.get("/dataset/{dataset_id}")
async def get_dataset_info(dataset_id: str):
    """
    Get information about a specific dataset
    """
    try:
        logger.info(f"Fetching dataset info: {dataset_id}")
        info = data_processor.get_dataset_info(dataset_id)
        return {
            "status": "success",
            "data": info,
        }
    except FileNotFoundError as e:
        logger.warning(f"Dataset not found: {dataset_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching dataset info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/datasets")
async def list_datasets():
    """
    List all uploaded datasets
    """
    try:
        logger.info("Fetching all datasets")
        datasets = data_processor.list_datasets()
        return {
            "status": "success",
            "count": len(datasets),
            "datasets": datasets,
        }
    except Exception as e:
        logger.error(f"Error listing datasets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/dataset/{dataset_id}")
async def delete_dataset(dataset_id: str):
    """
    Delete a dataset and all its files
    """
    try:
        logger.info(f"Deleting dataset: {dataset_id}")
        success = data_processor.delete_dataset(dataset_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
        return {
            "status": "success",
            "message": f"Dataset {dataset_id} deleted successfully",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting dataset: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
