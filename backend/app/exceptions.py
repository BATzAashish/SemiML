"""
Custom Exception Classes for SemiML Backend
Provides structured error handling and logging
"""
from typing import Any, Dict, Optional


class SemiMLException(Exception):
    """Base exception for all SemiML errors"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "SEMIML_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(SemiMLException):
    """Raised when input validation fails"""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            details=details
        )


class DataProcessingError(SemiMLException):
    """Raised when data processing fails"""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_code="DATA_PROCESSING_ERROR",
            status_code=400,
            details=details
        )


class FileNotFoundError_(SemiMLException):
    """Raised when a required file is not found"""
    
    def __init__(self, message: str, file_path: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="FILE_NOT_FOUND",
            status_code=404,
            details={"file_path": file_path} if file_path else {}
        )


class ModelNotFoundError(SemiMLException):
    """Raised when a model is not found"""
    
    def __init__(self, model_id: str):
        super().__init__(
            message=f"Model with ID {model_id} not found",
            error_code="MODEL_NOT_FOUND",
            status_code=404,
            details={"model_id": model_id}
        )


class DatasetNotFoundError(SemiMLException):
    """Raised when a dataset is not found"""
    
    def __init__(self, dataset_id: str):
        super().__init__(
            message=f"Dataset with ID {dataset_id} not found",
            error_code="DATASET_NOT_FOUND",
            status_code=404,
            details={"dataset_id": dataset_id}
        )


class PipelineError(SemiMLException):
    """Raised when pipeline operations fail"""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_code="PIPELINE_ERROR",
            status_code=500,
            details=details
        )


class TrainingError(SemiMLException):
    """Raised when model training fails"""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_code="TRAINING_ERROR",
            status_code=500,
            details=details
        )


class ValidationError_(SemiMLException):
    """Raised when model validation fails"""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_code="MODEL_VALIDATION_ERROR",
            status_code=400,
            details=details
        )


class ExplainabilityError(SemiMLException):
    """Raised when explanation generation fails"""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_code="EXPLAINABILITY_ERROR",
            status_code=500,
            details=details
        )


class ConfigurationError(SemiMLException):
    """Raised when configuration is invalid"""
    
    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            status_code=500,
            details={"config_key": config_key} if config_key else {}
        )
