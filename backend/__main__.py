"""
Entry point for running the backend
"""
if __name__ == "__main__":
    import uvicorn
    from app.logging_config import logger
    
    logger.info("Starting SemiML Backend...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
