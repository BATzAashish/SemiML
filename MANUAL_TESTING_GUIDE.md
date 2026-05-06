# Manual API Endpoint Testing Guide

This guide shows how to test all SemiML endpoints manually using curl commands.

## Quick Start

1. **Start the backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

2. **In another terminal, run the tests below:**

## Foundation Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "timestamp": "..."}
```

### 2. System Info
```bash
curl http://localhost:8000/api/connect
# Expected: {"system_ready": true, "modules": {...}, ...}
```

### 3. OpenAPI Documentation
```bash
curl http://localhost:8000/openapi.json | head -50
# Expected: JSON schema with paths and components
```

## Data Processing Endpoints

### 4. Upload Dataset
```bash
# Create a test CSV file first
curl -X POST http://localhost:8000/api/upload-dataset \
  -F "file=@test_data.csv"
# Expected: {"dataset_id": "...", "filename": "test_data.csv", ...}
```

### 5. Get Datasets
```bash
curl http://localhost:8000/api/datasets
# Expected: Array of dataset objects
```

## Meta-Features Endpoints

### 6. Extract Meta-Features
```bash
curl -X POST http://localhost:8000/api/extract-meta-features \
  -H "Content-Type: application/json" \
  -d '{
    "data": [[1,2,3],[4,5,6],[7,8,9]],
    "feature_names": ["a", "b", "c"]
  }'
# Expected: {"outliers": {...}, "entropy": {...}, ...}
```

## Experience Retrieval Endpoints

### 7. Retrieve Knowledge (Semantic Search)
```bash
curl -X POST http://localhost:8000/api/retrieve-knowledge \
  -H "Content-Type: application/json" \
  -d '{"query": "feature engineering best practices"}'
# Expected: {"results": [...], "confidence": 0.85, ...}
```

### 8. Find Similar Datasets
```bash
curl -X POST http://localhost:8000/api/find-similar-datasets \
  -H "Content-Type: application/json" \
  -d '{"meta_features": {"num_samples": 1000, "num_features": 10}}'
# Expected: {"similar_datasets": [...]}
```

### 9. Get Best Practices
```bash
curl -X POST http://localhost:8000/api/get-best-practices \
  -H "Content-Type: application/json" \
  -d '{"meta_features": {"num_samples": 1000, "num_features": 10}}'
# Expected: {"recommendations": [...]}
```

### 10. Get Best Models
```bash
curl -X POST http://localhost:8000/api/get-best-models \
  -H "Content-Type: application/json" \
  -d '{"meta_features": {"num_samples": 1000, "num_features": 10}}'
# Expected: {"recommended_models": [...]}
```

## Unified Experience Retrieval

### 11. Retrieve All Experience Data
```bash
curl -X POST http://localhost:8000/api/retrieve-experience \
  -H "Content-Type: application/json" \
  -d '{"meta_features": {"num_samples": 1000, "num_features": 10}}'
# Expected: {
#   "similar_datasets": [...],
#   "recommended_models": [...],
#   "best_practices": [...],
#   "knowledge_base_insights": [...]
# }
```

## Meta-Learning Endpoints

### 12. Make Meta-Learning Decision
```bash
curl -X POST http://localhost:8000/api/meta-decision \
  -H "Content-Type: application/json" \
  -d '{
    "meta_features": {"num_samples": 1000, "num_features": 10},
    "available_models": ["random_forest", "svm", "neural_network"],
    "optimization_metric": "accuracy"
  }'
# Expected: {
#   "recommended_model": "...",
#   "confidence": 0.92,
#   "reasoning": "...",
#   "source": "META_LEARNING"
# }
```

### 13. Record Decision Outcome
```bash
curl -X POST http://localhost:8000/api/record-outcome \
  -H "Content-Type: application/json" \
  -d '{
    "decision_id": "dec_123",
    "actual_result": 0.95,
    "expected_result": 0.92
  }'
# Expected: {"status": "recorded", "learning_updated": true}
```

### 14. Get Meta-Learning Insights
```bash
curl http://localhost:8000/api/meta-insights
# Expected: {"insights": [...], "trend": "improving"}
```

### 15. Check LLM Status
```bash
curl http://localhost:8000/api/llm-status
# Expected: {
#   "available_llm": "huggingface" or "openai" or "google" or "anthropic",
#   "fallback_available": true
# }
```

## Training Optimization Endpoints

### 16. Train with Early Stopping
```bash
curl -X POST http://localhost:8000/api/train-with-early-stopping \
  -H "Content-Type: application/json" \
  -d '{
    "data": [[1,2,3],[4,5,6],[7,8,9]],
    "target": [0, 1, 0],
    "model_type": "random_forest",
    "early_stopping_config": {
      "monitor": "val_loss",
      "patience": 5,
      "min_delta": 0.001
    }
  }'
# Expected: {"training_complete": true, "final_accuracy": 0.85, ...}
```

### 17. Parallel Model Training
```bash
curl -X POST http://localhost:8000/api/train-parallel \
  -H "Content-Type: application/json" \
  -d '{
    "data": [[1,2,3],[4,5,6],[7,8,9]],
    "target": [0, 1, 0],
    "model_types": ["random_forest", "svm", "logistic_regression"],
    "n_jobs": 3
  }'
# Expected: {
#   "training_complete": true,
#   "models": [
#     {"model": "random_forest", "accuracy": 0.85},
#     {"model": "svm", "accuracy": 0.88},
#     ...
#   ]
# }
```

## Monitoring Endpoints

### 18. Get Overall Metrics
```bash
curl http://localhost:8000/api/metrics/overall
# Expected: {
#   "total_requests": 150,
#   "total_errors": 2,
#   "avg_response_time_ms": 45.2
# }
```

### 19. Get Per-Endpoint Metrics
```bash
curl http://localhost:8000/api/metrics/endpoints
# Expected: {
#   "/health": {"count": 50, "avg_time_ms": 2.1},
#   "/api/upload-dataset": {"count": 10, "avg_time_ms": 250},
#   ...
# }
```

### 20. Get Error Metrics
```bash
curl http://localhost:8000/api/metrics/errors
# Expected: {
#   "total_errors": 2,
#   "by_status_code": {"422": 1, "500": 1},
#   "by_endpoint": {...}
# }
```

### 21. Get Rate Limit Status
```bash
curl http://localhost:8000/api/rate-limit/status
# Expected: {
#   "is_limited": false,
#   "remaining_requests": 5000,
#   "reset_at": "..."
# }
```

### 22. Configure Rate Limiting
```bash
curl -X POST http://localhost:8000/api/rate-limit/configure \
  -H "Content-Type: application/json" \
  -d '{
    "max_requests": 1000,
    "window_seconds": 60
  }'
# Expected: {"status": "configured", "max_requests": 1000}
```

### 23. Detailed Health Check
```bash
curl http://localhost:8000/api/health/detailed
# Expected: {
#   "status": "healthy",
#   "database": "connected",
#   "faiss": "ready",
#   "modules": {...}
# }
```

### 24. Performance Metrics
```bash
curl http://localhost:8000/api/metrics/performance
# Expected: {
#   "p50_response_time_ms": 25,
#   "p95_response_time_ms": 100,
#   "p99_response_time_ms": 200
# }
```

## Error Handling Tests

### 25. Missing Required Field
```bash
curl -X POST http://localhost:8000/api/meta-decision \
  -H "Content-Type: application/json" \
  -d '{}'
# Expected: 422 Unprocessable Entity with validation errors
```

### 26. Invalid Data Type
```bash
curl -X POST http://localhost:8000/api/extract-meta-features \
  -H "Content-Type: application/json" \
  -d '{
    "data": "not an array",
    "feature_names": ["a"]
  }'
# Expected: 422 Unprocessable Entity
```

### 27. Internal Server Error (Intentional)
```bash
curl -X POST http://localhost:8000/api/train-with-early-stopping \
  -H "Content-Type: application/json" \
  -d '{
    "data": [],
    "target": [],
    "model_type": "invalid_model"
  }'
# Expected: 500 Internal Server Error with error_code and status_code
```

## Automation Script

### Run All Tests with Python

```python
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
RESULTS = []

def test_endpoint(name, method, url, data=None, expected_status=200):
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{url}")
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{url}", json=data)
        else:
            response = requests.request(method, f"{BASE_URL}{url}", json=data)
        
        passed = response.status_code == expected_status
        RESULTS.append({
            "test": name,
            "status": "PASS" if passed else "FAIL",
            "expected": expected_status,
            "actual": response.status_code,
            "time": datetime.now().isoformat()
        })
        print(f"{'✓' if passed else '✗'} {name}: {response.status_code}")
    except Exception as e:
        RESULTS.append({
            "test": name,
            "status": "ERROR",
            "error": str(e)
        })
        print(f"✗ {name}: {e}")

# Run tests
test_endpoint("Health Check", "GET", "/health")
test_endpoint("System Info", "GET", "/api/connect")
test_endpoint("LLM Status", "GET", "/api/llm-status")
test_endpoint("Metrics Overall", "GET", "/api/metrics/overall")
test_endpoint("Rate Limit Status", "GET", "/api/rate-limit/status")

# Print results
print(f"\nResults: {sum(1 for r in RESULTS if r['status'] == 'PASS')}/{len(RESULTS)} passed")
```

## Playwright E2E Testing

```bash
# Install Playwright (if not done)
npm install -D @playwright/test

# Run E2E tests
npm run test:e2e

# Or from repo root
cd frontend && npm run test:e2e
```

## Performance Testing

```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:8000/health

# Using wrk (if installed)
wrk -t4 -c100 -d30s http://localhost:8000/health
```

## Continuous Testing

```bash
# Watch for changes and re-run tests
pytest-watch tests/test_all_endpoints.py

# Or with live reload
python -m pytest tests/test_all_endpoints.py --looponfail
```
