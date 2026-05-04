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

# Import and register routers
from app.routers import connection
from app.modules.module_2_data_processing.router import router as m2_router
from app.modules.module_3_meta_features.router import router as m3_router
from app.modules.module_4_experience_retrieval.router import router as m4_router
from app.modules.module_5_decision_engine.router import router as m5_router
from app.modules.module_6_pipeline_builder.router import router as m6_router
from app.modules.module_7_training_optimization.router import router as m7_router
from app.modules.module_8_validation.router import router as m8_router
from app.modules.module_9_explainability.router import router as m9_router
from app.modules.module_10_decision_trace.router import router as m10_router
from app.modules.module_11_feedback_learning.router import router as m11_router

app.include_router(connection.router)
app.include_router(m2_router)
app.include_router(m3_router)
app.include_router(m4_router)
app.include_router(m5_router)
app.include_router(m6_router)
app.include_router(m7_router)
app.include_router(m8_router)
app.include_router(m9_router)
app.include_router(m10_router)
app.include_router(m11_router)

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
