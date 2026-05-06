# SemiML Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Setup Environment (30 seconds)

```bash
cd backend
cp .env.example .env
# Edit .env and add your API keys (optional - system works without them)
```

### Step 2: Install Dependencies (1 minute)

```bash
python -m pip install -r requirements.txt
```

### Step 3: Start Backend (30 seconds)

```bash
python -m uvicorn app.main:app --reload --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 4: Test It Works!

In another terminal:
```bash
# Health check
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","message":"SemiML Backend is running","version":"1.0.0"}
```

## 🔑 API Keys (Optional)

### Completely Free Option ✅
```bash
# Just run without keys - system uses rule-based reasoning
python -m uvicorn app.main:app --reload
```

### Using Gemini (Recommended) 🎯
```bash
export GEMINI_API_KEY=your_key
export LLM_PROVIDER=gemini
python -m uvicorn app.main:app --reload
```

### Using Groq (Also Free) ⚡
```bash
export GROQ_API_KEY=your_key
export LLM_PROVIDER=groq
python -m uvicorn app.main:app --reload
```

## 📊 Test All Endpoints

### Option A: Using curl (Easiest)

```bash
# Foundation
curl http://localhost:8000/health
curl http://localhost:8000/

# Data Processing
curl -X POST http://localhost:8000/api/upload-dataset \
  -F "file=@test_data.csv"

# Meta-Features
curl -X POST http://localhost:8000/api/extract-meta-features \
  -H "Content-Type: application/json" \
  -d '{"data": [[1,2],[3,4]], "feature_names": ["a", "b"]}'

# Meta-Learning
curl -X POST http://localhost:8000/api/meta-decision \
  -H "Content-Type: application/json" \
  -d '{
    "meta_features": {"num_samples": 1000, "num_features": 10},
    "available_models": ["random_forest", "svm"],
    "optimization_metric": "accuracy"
  }'

# Monitoring
curl http://localhost:8000/api/metrics/overall
curl http://localhost:8000/api/health/detailed
```

See [MANUAL_TESTING_GUIDE.md](./MANUAL_TESTING_GUIDE.md) for 24+ examples.

### Option B: Using Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Test health
r = requests.get(f"{BASE_URL}/health")
print(r.json())  # {"status": "healthy", ...}

# Test meta-learning
r = requests.post(
    f"{BASE_URL}/api/meta-decision",
    json={
        "meta_features": {"num_samples": 1000, "num_features": 10},
        "available_models": ["random_forest", "svm"],
        "optimization_metric": "accuracy"
    }
)
print(r.json())  # {"recommended_model": "...", "confidence": 0.92, ...}
```

### Option C: Browser

Open http://localhost:8000/docs for interactive API documentation (Swagger UI)

## 🖥️ Frontend Setup

```bash
cd frontend
npm install
npm run dev

# Open http://localhost:5173 in browser
```

## 🐳 Docker Deployment

```bash
# Option 1: Build and run backend
docker build -f Dockerfile.backend -t semiml-backend .
docker run -p 8000:8000 semiml-backend

# Option 2: Full stack with compose
docker-compose up

# Access:
# - Backend API: http://localhost:8000
# - Frontend: http://localhost:5173
# - Nginx proxy: http://localhost/
```

## 📋 What's Included

✅ **Complete Backend**
- 11 ML modules + monitoring
- FastAPI + Uvicorn server
- SQLite database + FAISS vector store
- Optional LLM integration (OpenAI/Gemini/Groq/Anthropic)
- Request logging + rate limiting
- Error handling + validation

✅ **Frontend**
- React 18 + Vite
- Dashboard with charts
- Dataset upload
- Meta-features analysis
- Decision tracing

✅ **DevOps**
- Docker multi-stage builds
- Docker Compose setup
- Nginx reverse proxy
- Production-ready config

## 🧪 Running Tests

### All Endpoints Are Functional ✅

Tests work via direct HTTP calls (no pytest needed):

```bash
# Terminal 1: Start server
python -m uvicorn app.main:app --reload

# Terminal 2: Run test suite
python tests/test_all_endpoints_manual.py
# or use curl commands in MANUAL_TESTING_GUIDE.md
```

### 43 Test Cases Cover

- Foundation endpoints (health, connection, system info)
- Data processing (upload, retrieval)
- Meta-features extraction & analysis
- Experience retrieval & knowledge search
- Meta-learning decisions
- Training optimization
- Monitoring & metrics
- Error handling
- End-to-end integration

## 📚 Documentation

- [API_KEYS_REQUIRED.md](./API_KEYS_REQUIRED.md) - LLM setup guide
- [MANUAL_TESTING_GUIDE.md](./MANUAL_TESTING_GUIDE.md) - 24+ endpoint examples
- [TESTING_SUMMARY.md](./TESTING_SUMMARY.md) - Test suite overview
- [TESTING_DEPLOYMENT_GUIDE.md](./TESTING_DEPLOYMENT_GUIDE.md) - Comprehensive guide
- http://localhost:8000/docs - Interactive API docs (Swagger)

## 🎯 Next Steps

1. **Validate Locally**: Start server → curl test 5 endpoints
2. **Add API Keys**: Configure GEMINI_API_KEY or GROQ_API_KEY (optional)
3. **Deploy**: Use Docker or uvicorn on your server
4. **Monitor**: Check /api/metrics/* endpoints for health

## ❓ Troubleshooting

**Port 8000 already in use?**
```bash
python -m uvicorn app.main:app --reload --port 8001
# Or kill the process: lsof -ti:8000 | xargs kill -9
```

**Dependencies missing?**
```bash
python -m pip install -r requirements.txt --upgrade
```

**Database error?**
```bash
rm decisions.db  # Recreated on next run
```

**FAISS warning?**
```
# Just a performance note, not an error
# System works fine with standard FAISS
```

## ✨ You're All Set!

The system is **production-ready** with all 14 architectural phases implemented. Happy testing! 🎉

Need help? Check the docs or start the server and access http://localhost:8000/docs
