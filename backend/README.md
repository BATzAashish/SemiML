# SemiML Backend - Hybrid Explainable ML Decision System

This is the backend for the Hybrid Explainable ML Decision System, a semi-autonomous decision engine that intelligently selects, evaluates, and explains machine learning workflows.

## Project Structure

```
backend/
├── app/
│   ├── models/
│   │   └── schemas.py           # Pydantic data models
│   ├── routers/                 # API endpoints (will be added)
│   ├── services/                # Business logic (will be added)
│   ├── database/                # Database utilities (will be added)
│   ├── utils/                   # Helper functions (will be added)
│   ├── main.py                  # FastAPI application
│   ├── config.py                # Configuration management
│   └── logging_config.py        # Logging setup
├── uploads/                     # Uploaded datasets
├── logs/                        # Application logs
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
└── README.md                    # This file
```

## Installation

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Update `.env` file with your configuration:
```env
LOG_LEVEL=INFO
LLM_API_KEY=your_api_key_here
# ... other settings
```

## Running the Backend

### Development Mode
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Health Check
```bash
curl http://localhost:8000/health
```

## System Architecture

### Core Modules (To Be Built)
1. **Data Processing Layer** - Handle dataset upload and validation
2. **Meta-Feature Extraction** - Extract dataset characteristics
3. **Knowledge Retrieval (RAG)** - Retrieve ML best practices
4. **Experience Retrieval** - Query past experiments from MLflow
5. **Hybrid Decision Engine** - Intelligently select ML pipelines
6. **Pipeline Builder** - Construct scikit-learn pipelines
7. **Training & Optimization** - Train and tune models
8. **Validation Layer** - Cross-validate and detect issues
9. **Explainability Engine** - Generate model explanations
10. **Decision Trace System** - Log all decisions
11. **Feedback & Learning** - Store and learn from experiences

## Current Status

✅ Module 1: Project Foundation
- [x] Directory structure created
- [x] Pydantic schemas defined
- [x] Configuration management set up
- [x] Logging configured
- [x] FastAPI app initialized
- [x] Health check endpoint ready

⏳ Module 2-11: To be built

## API Endpoints (Planned)

| Module | Endpoint | Method | Purpose |
|--------|----------|--------|---------|
| Data Processing | `/upload-dataset` | POST | Upload dataset |
| Meta-Features | `/extract-meta-features` | POST | Extract dataset features |
| RAG | `/retrieve-knowledge` | POST | Retrieve ML best practices |
| Experience | `/retrieve-experience` | POST | Get similar past experiments |
| Decision | `/decide-pipeline` | POST | Select optimal pipeline |
| Pipeline | `/build-pipeline` | POST | Build ML pipeline |
| Training | `/train-pipeline` | POST | Train selected pipeline |
| Validation | `/validate-model` | POST | Validate trained model |
| Explainability | `/explain-model` | POST | Generate explanations |
| Feedback | `/feedback` | POST | Submit feedback |
| Trace | `/decision-trace` | GET | Retrieve decision logs |

## Development Guidelines

1. **Modularity**: Each feature is independent and testable
2. **Explainability**: Every decision must be logged with reasoning
3. **Clean Code**: Follow PEP 8 standards
4. **Testing**: Write unit tests for each module
5. **Documentation**: Keep docstrings and comments updated

## Next Steps

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Start development on Module 2: Data Processing Layer
- [ ] Set up MLflow tracking server
- [ ] Configure LangChain and FAISS for RAG
- [ ] Implement decision engine logic
- [ ] Create router endpoints
- [ ] Write unit tests
- [ ] Deploy to production

## Contributing

Follow the modular architecture when adding new features. Ensure all decisions are logged and explainable.

## License

TBD
