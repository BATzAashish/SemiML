# Playwright E2E Testing Guide for SemiML

## Overview
This directory contains comprehensive Playwright E2E tests for both frontend and backend integration testing.

## Created Test Files

### 1. `backend-api.spec.ts`
Tests for backend API endpoints:
- Health check endpoint verification
- System info endpoint
- Connection endpoint
- Meta-feature extraction
- Meta-decision making
- Monitoring endpoints
- LLM status
- OpenAPI documentation

### 2. `frontend-integration.spec.ts`
Tests for frontend UI and integration:
- Frontend page loads successfully
- Backend status indicators
- API connectivity from frontend
- Navigation elements
- Dashboard rendering
- Interactive elements
- Responsive design across viewports

### 3. `e2e-workflow.spec.ts`
End-to-end workflow tests:
- Complete backend + frontend integration
- Performance testing (response times)
- Concurrent request handling
- Error handling and validation
- System status verification

## Setup Instructions

### Prerequisites
- Node.js 16+ with npm/yarn/bun
- Python 3.11+
- Backend and frontend dependencies installed

### Step 1: Install Playwright Browsers
```bash
cd frontend
npx playwright install
```

### Step 2: Start Backend Server (Manual)

**Terminal 1: Backend**
```bash
cd backend
pip install -r requirements.txt  # if not already done
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Wait for the output:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Start Frontend Development Server (Manual)

**Terminal 2: Frontend**
```bash
cd frontend
npm run dev
```

Wait for the output:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://127.0.0.1:5173/
```

### Step 4: Run Playwright Tests

**Terminal 3: Test Runner**
```bash
cd frontend
npx playwright test
```

## Available Test Commands

```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test e2e/backend-api.spec.ts

# Run tests in headed mode (see browser)
npx playwright test --headed

# Run tests with specific browser
npx playwright test --project=chromium

# Run tests with debug mode
npx playwright test --debug

# Run tests with verbose output
npx playwright test --reporter=verbose

# Run tests and generate HTML report
npx playwright test --reporter=html
```

## Test Coverage

### Backend API Tests (11 tests)
- ✅ Health endpoint (status, message, version)
- ✅ Root endpoint (system info)
- ✅ Connection/system-ready endpoint
- ✅ Meta-feature extraction endpoint
- ✅ Meta-decision endpoint
- ✅ Monitoring endpoints (health/detailed, metrics, rate-limit)
- ✅ OpenAPI documentation availability
- ✅ Endpoint count validation (20+ endpoints)
- ✅ LLM status endpoint

### Frontend Integration Tests (9 tests)
- ✅ Frontend loads successfully
- ✅ Backend status indicator visible
- ✅ API reachability from frontend context
- ✅ Navigation elements present
- ✅ Dashboard rendering without crashes
- ✅ Content area displays
- ✅ Interactive elements available
- ✅ Responsive design (desktop, tablet, mobile)

### E2E Workflow Tests (4 tests)
- ✅ Complete integration workflow (10+ verification steps)
- ✅ Performance: health endpoint responds < 1s
- ✅ Concurrency: backend handles 10+ simultaneous requests
- ✅ Error handling: proper response for invalid requests

**Total: 24+ comprehensive integration tests**

## Expected Results

When all tests pass, you should see output similar to:
```
✓ [chromium] › backend-api.spec.ts (11 tests) 
✓ [chromium] › frontend-integration.spec.ts (9 tests)
✓ [chromium] › e2e-workflow.spec.ts (4 tests)

24 passed (45s)
```

## Troubleshooting

### Backend fails to start with middleware error
**Issue**: `ValueError: too many values to unpack (expected 2)` during middleware building

**Solution**: 
1. Update FastAPI and Starlette:
   ```bash
   pip install --upgrade fastapi uvicorn starlette
   ```

2. Or ensure versions in requirements.txt:
   ```
   fastapi>=0.115.13
   uvicorn>=0.34.3
   starlette>=0.37.0
   ```

3. Restart the backend server

### Frontend connection refused error
**Issue**: Tests fail with "Connection refused" to http://127.0.0.1:5173

**Solution**:
1. Verify frontend is running: `npm run dev`
2. Check port 5173 is not in use: `netstat -tulpn | grep 5173`
3. Kill any process using port 5173
4. Restart frontend server

### Backend API connection refused
**Issue**: Tests fail when connecting to backend (port 8000)

**Solution**:
1. Verify backend is running
2. Test manually: `curl http://127.0.0.1:8000/health`
3. Check firewall settings
4. Ensure port 8000 is not in use

### Tests timeout
**Issue**: Tests hang and eventually timeout

**Solution**:
1. Increase timeout in playwright.config.ts (default 60s)
2. Check if servers are responding slowly
3. Monitor CPU/memory usage
4. Run tests in debug mode: `npx playwright test --debug`

## Architecture

```
frontend/
├── e2e/                          # E2E test files
│   ├── backend-api.spec.ts      # API endpoint tests
│   ├── frontend-integration.spec.ts  # UI integration tests
│   └── e2e-workflow.spec.ts     # End-to-end workflows
├── playwright.config.ts          # Playwright configuration
└── ... (other frontend files)

backend/
├── app/
│   ├── main.py                  # FastAPI application
│   └── ... (routers, services)
└── requirements.txt             # Python dependencies
```

## CI/CD Integration

To run tests in CI/CD pipeline:

```yaml
# GitHub Actions example
- name: Install dependencies
  run: |
    cd backend && pip install -r requirements.txt
    cd ../frontend && npm install

- name: Start backend
  run: cd backend && python -m uvicorn app.main:app --port 8000 &

- name: Start frontend  
  run: cd frontend && npm run dev &

- name: Wait for servers
  run: sleep 5

- name: Run tests
  run: cd frontend && npx playwright test
```

## Performance Metrics

The test suite tracks:
- Backend response times (health endpoint < 1s)
- Concurrent request handling (10+ simultaneous)
- Frontend page load times
- API endpoint availability
- System stability

## Maintenance

### Adding New Tests
1. Create new `.spec.ts` file in `e2e/` directory
2. Follow naming pattern: `feature-name.spec.ts`
3. Import `test` and `expect` from `@playwright/test`
4. Run tests to verify

### Updating Test Data
- Modify request payloads in test files
- Update expected responses
- Run tests to validate changes

### Regular Maintenance
- Run full test suite after code changes
- Update test timeouts if needed
- Review failed tests for infrastructure issues
- Update documentation with new test coverage
