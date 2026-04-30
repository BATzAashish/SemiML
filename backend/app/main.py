from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import API_TITLE, API_VERSION, API_DESCRIPTION
from app.logging_config import logger

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# CORS Configuration (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify backend is running"""
    return {
        "status": "healthy",
        "message": "SemiML Backend is running",
        "version": API_VERSION
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Hybrid Explainable ML Decision System",
        "version": API_VERSION,
        "description": API_DESCRIPTION,
        "docs": "/docs",
        "status": "operational"
    }


# Import and register routers (will be added as modules are built)
# from app.routers import upload, meta_features, rag, experience, decision, etc.

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting SemiML Backend...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
