"""
Knowledge Ingestion & Retrieval Service
Integrates LangChain + FAISS for semantic search and knowledge retrieval
"""
import os
import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.docstore.document import Document
    from langchain.chains import RetrievalQA
    from langchain.llms import OpenAI
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

from app.logging_config import logger


class KnowledgeBase:
    """
    Manages knowledge base ingestion, indexing, and retrieval using FAISS + LangChain
    """

    def __init__(self, knowledge_dir: str = "backend/knowledge"):
        """
        Initialize knowledge base
        Args:
            knowledge_dir: Directory to store FAISS indices and documents
        """
        self.knowledge_dir = Path(knowledge_dir)
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        self.vectorstore = None
        self.embeddings = None
        self.documents = []
        
        logger.info("KnowledgeBase initialized")
        
        # Try to initialize embeddings
        if LANGCHAIN_AVAILABLE:
            self._initialize_embeddings()
            self._load_knowledge_base()

    def _initialize_embeddings(self):
        """Initialize embedding model - use HuggingFace if OpenAI key not available"""
        try:
            if os.getenv("OPENAI_API_KEY"):
                self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
                logger.info("Using OpenAI embeddings")
            else:
                # Use HuggingFace embeddings as fallback
                self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                logger.info("Using HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2)")
        except Exception as e:
            logger.warning(f"Error initializing embeddings: {str(e)}")
            self.embeddings = None

    def ingest_documents(self, documents: List[Dict[str, str]]) -> bool:
        """
        Ingest documents into the knowledge base
        Args:
            documents: List of dicts with 'content' and optional 'metadata' keys
        Returns:
            True if successful
        """
        if not LANGCHAIN_AVAILABLE or not FAISS_AVAILABLE:
            logger.warning("LangChain or FAISS not available - skipping ingestion")
            return False

        try:
            # Convert documents to LangChain format
            docs = []
            for doc in documents:
                content = doc.get("content", "")
                metadata = doc.get("metadata", {})
                docs.append(Document(page_content=content, metadata=metadata))

            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            split_docs = text_splitter.split_documents(docs)
            self.documents.extend(split_docs)

            # Create FAISS index
            if self.embeddings:
                self.vectorstore = FAISS.from_documents(split_docs, self.embeddings)
                self._save_knowledge_base()
                logger.info(f"Ingested {len(split_docs)} document chunks")
                return True
            else:
                logger.warning("Embeddings not available - cannot create vectorstore")
                return False

        except Exception as e:
            logger.error(f"Error ingesting documents: {str(e)}")
            return False

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        Args:
            query: Search query
            top_k: Number of results to return
        Returns:
            List of relevant documents with scores
        """
        if not self.vectorstore:
            logger.warning("Vector store not initialized")
            return []

        try:
            # Perform similarity search with score
            results_with_score = self.vectorstore.similarity_search_with_score(query, k=top_k)
            
            retrieved = []
            for doc, score in results_with_score:
                retrieved.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": float(score),
                })
            
            return retrieved

        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []

    def _load_knowledge_base(self):
        """Load existing FAISS index from disk"""
        try:
            index_path = self.knowledge_dir / "faiss_index"
            if index_path.exists():
                self.vectorstore = FAISS.load_local(
                    str(index_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("Loaded existing FAISS index")
        except Exception as e:
            logger.warning(f"Could not load existing FAISS index: {str(e)}")

    def _save_knowledge_base(self):
        """Save FAISS index to disk"""
        try:
            if self.vectorstore:
                index_path = self.knowledge_dir / "faiss_index"
                self.vectorstore.save_local(str(index_path))
                logger.info(f"Saved FAISS index to {index_path}")
        except Exception as e:
            logger.error(f"Error saving FAISS index: {str(e)}")

    def add_ml_best_practices(self) -> bool:
        """
        Add ML best practices to knowledge base
        Returns:
            True if successful
        """
        best_practices = [
            {
                "content": """Machine Learning Data Preprocessing Best Practices:
                1. Handle missing values: Use mean/median imputation for numerical, mode for categorical
                2. Scale numerical features: Use StandardScaler or MinMaxScaler to normalize
                3. Encode categorical features: Use one-hot encoding for nominal, ordinal encoding for ordinal
                4. Handle outliers: Use IQR or Z-score method, consider log transformation
                5. Feature engineering: Create interactions, polynomial features, domain-specific features
                6. Data split: Use 70-20-10 or 80-10-10 for train-validation-test
                7. Check for data leakage: Ensure target information not in features
                8. Balance classes: Use SMOTE or class weights for imbalanced data""",
                "metadata": {"source": "ml_best_practices", "category": "preprocessing"}
            },
            {
                "content": """Feature Selection and Engineering Strategies:
                1. Statistical methods: Correlation analysis, mutual information, chi-square test
                2. Model-based selection: Feature importance from tree models, permutation importance
                3. Recursive feature elimination: Remove least important features iteratively
                4. Domain expertise: Use domain knowledge to create meaningful features
                5. Dimensionality reduction: PCA, UMAP for high-dimensional data
                6. Feature interactions: Create polynomial and interaction features
                7. Time-series features: Lag features, rolling statistics for temporal data
                8. Autoencoder features: Learn latent representations for complex patterns""",
                "metadata": {"source": "ml_best_practices", "category": "feature_engineering"}
            },
            {
                "content": """Model Selection and Hyperparameter Tuning:
                1. Classification: Logistic Regression, Random Forest, SVM, Gradient Boosting (XGBoost, LightGBM)
                2. Regression: Linear Regression, Ridge/Lasso, Random Forest, Gradient Boosting
                3. Hyperparameter tuning: Grid search, random search, Bayesian optimization
                4. Cross-validation: K-fold (5-10), stratified for imbalanced data
                5. Model ensemble: Voting, stacking, blending for better predictions
                6. Early stopping: Monitor validation metric to prevent overfitting
                7. Learning curves: Plot train/validation loss to diagnose bias/variance
                8. Model comparison: Use appropriate metrics (accuracy, F1, AUC, RMSE, R²)""",
                "metadata": {"source": "ml_best_practices", "category": "modeling"}
            },
            {
                "content": """Evaluation Metrics and Validation:
                Classification metrics: Accuracy (overall), Precision (false positive cost), Recall (false negative cost),
                F1-score (balance precision-recall), AUC-ROC (threshold-independent), Confusion matrix
                Regression metrics: MAE (average error), MSE/RMSE (penalize large errors), R² (variance explained),
                MAPE (percentage error), Residual analysis (check for patterns)
                Always use: Cross-validation, hold-out test set, stratified splits for imbalanced data,
                Domain-specific metrics, Confidence intervals for estimates""",
                "metadata": {"source": "ml_best_practices", "category": "evaluation"}
            },
        ]
        
        return self.ingest_documents(best_practices)

    def add_experience_data(self, experiences: List[Dict[str, Any]]) -> bool:
        """
        Add past project experiences to knowledge base
        Args:
            experiences: List of experience dictionaries
        Returns:
            True if successful
        """
        documents = []
        for exp in experiences:
            content = f"""
            Dataset: {exp.get('dataset_name', 'Unknown')}
            Problem type: {exp.get('problem_type', 'Unknown')}
            Best model: {exp.get('best_model', 'Unknown')}
            Accuracy: {exp.get('accuracy', 'Unknown')}
            Features used: {', '.join(exp.get('features', []))}
            Preprocessing: {exp.get('preprocessing_steps', 'Unknown')}
            Key insights: {exp.get('insights', 'Unknown')}
            """
            documents.append({
                "content": content,
                "metadata": {
                    "source": "experience",
                    "dataset_id": exp.get("dataset_id"),
                    "accuracy": exp.get("accuracy")
                }
            })
        
        return self.ingest_documents(documents)

    def search_similar_approaches(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for similar approaches and best practices
        Args:
            query: Problem description or question
            top_k: Number of results
        Returns:
            List of relevant approaches
        """
        return self.retrieve(query, top_k=top_k)


# Global knowledge base instance
knowledge_base: Optional[KnowledgeBase] = None


def get_knowledge_base() -> Optional[KnowledgeBase]:
    """Get or initialize knowledge base"""
    global knowledge_base
    if knowledge_base is None:
        knowledge_base = KnowledgeBase()
    return knowledge_base


def initialize_default_knowledge():
    """Initialize with default ML best practices"""
    kb = get_knowledge_base()
    if kb and LANGCHAIN_AVAILABLE:
        kb.add_ml_best_practices()
        logger.info("Default ML knowledge base initialized")
