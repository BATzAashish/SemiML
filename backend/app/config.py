import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_TITLE = "Hybrid Explainable ML Decision System"
API_VERSION = "1.0.0"
API_DESCRIPTION = "Backend for intelligent ML pipeline selection and explanation"

# Paths
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
MODELS_DIR = os.getenv("MODELS_DIR", "./models")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./decisions.db")

# MLflow Configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MLFLOW_EXPERIMENT_NAME = "semiml-experiments"

# LangChain & FAISS Configuration
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "./faiss_index")

# LLM Configuration (for reasoning)
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "./logs/semiml.log")

# Validation thresholds
MIN_CROSS_VAL_SCORE = float(os.getenv("MIN_CROSS_VAL_SCORE", "0.7"))
MAX_OVERFITTING_THRESHOLD = float(os.getenv("MAX_OVERFITTING_THRESHOLD", "0.15"))

# Create directories if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
