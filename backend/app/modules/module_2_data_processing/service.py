"""
Module 2: Data Processing Service
Handles dataset upload, validation, and storage
"""
import os
import uuid
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, Any
from app.config import UPLOAD_DIR
from app.logging_config import logger
from app.models.schemas import DatasetMetadata


class DataProcessor:
    """
    Processes and validates uploaded datasets
    """

    # Allowed file types
    ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".json", ".parquet"}
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

    def __init__(self):
        self.upload_dir = Path(UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"DataProcessor initialized with upload dir: {self.upload_dir}")

    def validate_file(self, filename: str, file_content: bytes) -> Tuple[bool, str]:
        """
        Validate uploaded file
        Returns: (is_valid, error_message)
        """
        # Check file extension
        file_ext = Path(filename).suffix.lower()
        if file_ext not in self.ALLOWED_EXTENSIONS:
            return False, f"File type {file_ext} not allowed. Allowed: {self.ALLOWED_EXTENSIONS}"

        # Check file size
        file_size = len(file_content)
        if file_size > self.MAX_FILE_SIZE:
            return False, f"File size {file_size} exceeds maximum {self.MAX_FILE_SIZE}"

        # Check file is not empty
        if file_size == 0:
            return False, "File is empty"

        return True, ""

    def save_file(self, filename: str, file_content: bytes) -> Tuple[str, str]:
        """
        Save uploaded file to disk
        Returns: (dataset_id, file_path)
        """
        # Generate unique dataset ID
        dataset_id = str(uuid.uuid4())

        # Create dataset directory
        dataset_dir = self.upload_dir / dataset_id
        dataset_dir.mkdir(parents=True, exist_ok=True)

        # Save file
        file_path = dataset_dir / filename
        with open(file_path, "wb") as f:
            f.write(file_content)

        logger.info(f"File saved: {file_path} (Dataset ID: {dataset_id})")
        return dataset_id, str(file_path)

    def load_and_validate_data(self, file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Load dataset and extract basic info
        Returns: (dataframe, metadata_dict)
        """
        file_ext = Path(file_path).suffix.lower()

        try:
            # Load based on file type
            if file_ext == ".csv":
                df = pd.read_csv(file_path)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file_path)
            elif file_ext == ".json":
                df = pd.read_json(file_path)
            elif file_ext == ".parquet":
                df = pd.read_parquet(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")

            # Extract metadata
            metadata = {
                "num_rows": len(df),
                "num_columns": len(df.columns),
                "columns": list(df.columns),
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "missing_values": df.isnull().sum().to_dict(),
                "duplicates": len(df[df.duplicated()]),
            }

            logger.info(f"Data loaded successfully: {metadata['num_rows']} rows, {metadata['num_columns']} columns")
            return df, metadata

        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            raise

    def get_dataset_info(self, dataset_id: str) -> Dict[str, Any]:
        """
        Get information about a stored dataset
        """
        dataset_dir = self.upload_dir / dataset_id
        if not dataset_dir.exists():
            raise FileNotFoundError(f"Dataset {dataset_id} not found")

        # Get files in directory
        files = list(dataset_dir.glob("*"))
        if not files:
            raise FileNotFoundError(f"No files found in dataset {dataset_id}")

        file_path = files[0]
        df, metadata = self.load_and_validate_data(str(file_path))

        return {
            "dataset_id": dataset_id,
            "filename": file_path.name,
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size,
            "upload_time": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            "data_metadata": metadata,
        }

    def delete_dataset(self, dataset_id: str) -> bool:
        """
        Delete a dataset and all its files
        """
        import shutil

        dataset_dir = self.upload_dir / dataset_id
        if not dataset_dir.exists():
            logger.warning(f"Dataset {dataset_id} not found for deletion")
            return False

        try:
            shutil.rmtree(dataset_dir)
            logger.info(f"Dataset {dataset_id} deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting dataset {dataset_id}: {str(e)}")
            return False

    def list_datasets(self) -> list:
        """
        List all uploaded datasets
        """
        datasets = []
        for dataset_dir in self.upload_dir.iterdir():
            if dataset_dir.is_dir():
                try:
                    info = self.get_dataset_info(dataset_dir.name)
                    datasets.append(info)
                except Exception as e:
                    logger.warning(f"Error getting info for dataset {dataset_dir.name}: {str(e)}")

        return datasets


# Global instance
data_processor = DataProcessor()
