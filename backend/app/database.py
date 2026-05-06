"""
Database and Storage Module for SemiML
Handles persistent storage for models, datasets, and metadata
Uses SQLite for simplicity; can be extended to PostgreSQL
"""
from sqlalchemy import create_engine, Column, String, DateTime, Float, Integer, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import Optional, Dict, Any
import os
from app.config import DATABASE_URL
from app.logging_config import logger

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ===== DATABASE MODELS =====

class Dataset(Base):
    """Persisted dataset metadata"""
    __tablename__ = "datasets"
    
    dataset_id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    num_rows = Column(Integer)
    num_columns = Column(Integer)
    columns = Column(JSON)  # List of column names
    metadata = Column(JSON)  # Additional metadata


class Model(Base):
    """Persisted model metadata"""
    __tablename__ = "models"
    
    model_id = Column(String, primary_key=True, index=True)
    pipeline_id = Column(String, nullable=False, index=True)
    dataset_id = Column(String, nullable=False, index=True)
    model_type = Column(String, nullable=False)
    model_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    accuracy = Column(Float)
    f1_score = Column(Float)
    metadata = Column(JSON)


class TrainingRun(Base):
    """Persisted training run history"""
    __tablename__ = "training_runs"
    
    run_id = Column(String, primary_key=True, index=True)
    model_id = Column(String, nullable=False, index=True)
    dataset_id = Column(String, nullable=False, index=True)
    status = Column(String)  # "completed", "failed", "running"
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    duration_seconds = Column(Float)
    hyperparameters = Column(JSON)
    metrics = Column(JSON)
    error_message = Column(Text)


class ValidationRun(Base):
    """Persisted validation run history"""
    __tablename__ = "validation_runs"
    
    validation_id = Column(String, primary_key=True, index=True)
    model_id = Column(String, nullable=False, index=True)
    dataset_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    cross_val_score = Column(Float)
    overfitting_detected = Column(Integer)  # Boolean as int
    data_leakage_risk = Column(Integer)  # Boolean as int
    issues = Column(JSON)
    status = Column(String)  # "passed", "failed", "warning"


class DecisionLog(Base):
    """Persisted decision trace and reasoning"""
    __tablename__ = "decision_logs"
    
    trace_id = Column(String, primary_key=True, index=True)
    dataset_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    decision = Column(String, nullable=False)
    reasoning = Column(Text)
    confidence_score = Column(Float)
    source = Column(String)  # "rules", "meta-learning", "experience", "llm"
    metadata = Column(JSON)


# ===== DATABASE OPERATIONS =====

class DatabaseManager:
    """Manager for database operations"""
    
    @staticmethod
    def init_db():
        """Initialize database tables"""
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise
    
    @staticmethod
    def get_session() -> Session:
        """Get database session"""
        return SessionLocal()
    
    @staticmethod
    def save_dataset(
        dataset_id: str,
        filename: str,
        file_path: str,
        num_rows: int,
        num_columns: int,
        columns: list,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dataset:
        """Save dataset metadata to database"""
        session = DatabaseManager.get_session()
        try:
            dataset = Dataset(
                dataset_id=dataset_id,
                filename=filename,
                file_path=file_path,
                num_rows=num_rows,
                num_columns=num_columns,
                columns=columns,
                metadata=metadata or {}
            )
            session.add(dataset)
            session.commit()
            session.refresh(dataset)
            logger.info(f"Dataset {dataset_id} saved to database")
            return dataset
        finally:
            session.close()
    
    @staticmethod
    def get_dataset(dataset_id: str) -> Optional[Dataset]:
        """Retrieve dataset metadata"""
        session = DatabaseManager.get_session()
        try:
            return session.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
        finally:
            session.close()
    
    @staticmethod
    def save_model(
        model_id: str,
        pipeline_id: str,
        dataset_id: str,
        model_type: str,
        model_path: str,
        accuracy: float,
        f1_score: float,
        metadata: Optional[Dict] = None
    ) -> Model:
        """Save model metadata to database"""
        session = DatabaseManager.get_session()
        try:
            model = Model(
                model_id=model_id,
                pipeline_id=pipeline_id,
                dataset_id=dataset_id,
                model_type=model_type,
                model_path=model_path,
                accuracy=accuracy,
                f1_score=f1_score,
                metadata=metadata or {}
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            logger.info(f"Model {model_id} saved to database")
            return model
        finally:
            session.close()
    
    @staticmethod
    def save_training_run(
        run_id: str,
        model_id: str,
        dataset_id: str,
        status: str,
        duration_seconds: float,
        hyperparameters: Dict,
        metrics: Dict,
        error_message: Optional[str] = None
    ) -> TrainingRun:
        """Save training run to database"""
        session = DatabaseManager.get_session()
        try:
            run = TrainingRun(
                run_id=run_id,
                model_id=model_id,
                dataset_id=dataset_id,
                status=status,
                duration_seconds=duration_seconds,
                hyperparameters=hyperparameters,
                metrics=metrics,
                error_message=error_message,
                completed_at=datetime.utcnow() if status in ["completed", "failed"] else None
            )
            session.add(run)
            session.commit()
            session.refresh(run)
            logger.info(f"Training run {run_id} saved to database")
            return run
        finally:
            session.close()
    
    @staticmethod
    def save_decision_log(
        trace_id: str,
        dataset_id: str,
        decision: str,
        reasoning: str,
        confidence_score: float,
        source: str,
        metadata: Optional[Dict] = None
    ) -> DecisionLog:
        """Save decision trace to database"""
        session = DatabaseManager.get_session()
        try:
            log = DecisionLog(
                trace_id=trace_id,
                dataset_id=dataset_id,
                decision=decision,
                reasoning=reasoning,
                confidence_score=confidence_score,
                source=source,
                metadata=metadata or {}
            )
            session.add(log)
            session.commit()
            session.refresh(log)
            logger.info(f"Decision log {trace_id} saved to database")
            return log
        finally:
            session.close()


# Initialize database on module load
try:
    DatabaseManager.init_db()
except Exception as e:
    logger.warning(f"Database initialization warning: {str(e)}")
