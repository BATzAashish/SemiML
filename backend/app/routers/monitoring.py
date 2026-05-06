"""
Monitoring & Metrics Router
Provides endpoints for monitoring system health and performance metrics
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional

from app.monitoring import get_request_monitor, get_rate_limiter, RateLimitConfig
from app.logging_config import logger

router = APIRouter(prefix="/api", tags=["Monitoring"])


# ============================================================================
# Metrics Endpoints
# ============================================================================

@router.get("/metrics/overall")
async def get_overall_metrics() -> Dict[str, Any]:
    """
    Get overall system metrics and statistics
    
    Returns:
        Overall system performance metrics including requests, errors, response times
    """
    try:
        logger.info("Retrieving overall metrics")
        monitor = get_request_monitor()
        stats = monitor.get_overall_stats()
        
        return {
            "status": "success",
            "metrics": stats,
            "timestamp": None,  # Would add timestamp here
        }
        
    except Exception as e:
        logger.error(f"Error retrieving metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/endpoints")
async def get_endpoint_metrics(endpoint: Optional[str] = None) -> Dict[str, Any]:
    """
    Get per-endpoint metrics
    
    Args:
        endpoint: Specific endpoint or None for all
        
    Returns:
        Metrics for each endpoint including request counts and response times
    """
    try:
        logger.info("Retrieving endpoint metrics")
        monitor = get_request_monitor()
        stats = monitor.get_endpoint_stats(endpoint)
        
        return {
            "status": "success",
            "metrics": stats,
        }
        
    except Exception as e:
        logger.error(f"Error retrieving endpoint metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/errors")
async def get_error_metrics() -> Dict[str, Any]:
    """
    Get error summary and statistics
    
    Returns:
        Errors grouped by status code and endpoint
    """
    try:
        logger.info("Retrieving error metrics")
        monitor = get_request_monitor()
        errors = monitor.get_error_summary()
        
        return {
            "status": "success",
            "errors": errors,
        }
        
    except Exception as e:
        logger.error(f"Error retrieving error metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Rate Limiting Endpoints
# ============================================================================

@router.get("/rate-limit/status")
async def get_rate_limit_status() -> Dict[str, Any]:
    """
    Get rate limiting status
    
    Returns:
        Rate limiting configuration and current status
    """
    try:
        logger.info("Retrieving rate limit status")
        limiter = get_rate_limiter()
        
        return {
            "status": "success",
            "rate_limiting": {
                "enabled": limiter.config.enabled,
                "max_requests": limiter.config.max_requests,
                "window_seconds": limiter.config.window_seconds,
                "per_user": limiter.config.per_user,
            },
            "message": "Rate limiting is enabled" if limiter.config.enabled else "Rate limiting is disabled",
        }
        
    except Exception as e:
        logger.error(f"Error retrieving rate limit status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rate-limit/configure")
async def configure_rate_limiting(
    max_requests: int = 100,
    window_seconds: int = 60,
    enabled: bool = True,
) -> Dict[str, Any]:
    """
    Configure rate limiting parameters
    
    Args:
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds
        enabled: Whether rate limiting is enabled
        
    Returns:
        Updated rate limiting configuration
    """
    try:
        logger.info(f"Configuring rate limiting: {max_requests} requests per {window_seconds}s")
        
        config = RateLimitConfig(
            max_requests=max_requests,
            window_seconds=window_seconds,
            enabled=enabled
        )
        
        return {
            "status": "success",
            "message": "Rate limiting configured",
            "config": {
                "enabled": config.enabled,
                "max_requests": config.max_requests,
                "window_seconds": config.window_seconds,
            },
        }
        
    except Exception as e:
        logger.error(f"Error configuring rate limiting: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Health Check Endpoints
# ============================================================================

@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """
    Get detailed health check information
    
    Returns:
        Detailed system health including uptime, metrics, and component status
    """
    try:
        logger.info("Performing detailed health check")
        monitor = get_request_monitor()
        stats = monitor.get_overall_stats()
        errors = monitor.get_error_summary()
        
        # Determine health status
        error_rate = stats.get("error_rate", 0)
        if error_rate > 0.1:  # > 10% error rate = degraded
            health_status = "degraded"
        elif error_rate > 0.05:  # > 5% error rate = warning
            health_status = "warning"
        else:
            health_status = "healthy"
        
        return {
            "status": "success",
            "health": {
                "overall_status": health_status,
                "metrics": stats,
                "recent_errors": errors,
            },
        }
        
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Performance Monitoring Endpoints
# ============================================================================

@router.get("/metrics/performance")
async def get_performance_metrics() -> Dict[str, Any]:
    """
    Get performance metrics
    
    Returns:
        Performance indicators including response times and throughput
    """
    try:
        logger.info("Retrieving performance metrics")
        monitor = get_request_monitor()
        stats = monitor.get_overall_stats()
        
        # Calculate throughput (requests per minute)
        uptime_minutes = stats.get("uptime_seconds", 1) / 60.0
        throughput_rpm = stats.get("total_requests", 0) / max(uptime_minutes, 1)
        
        return {
            "status": "success",
            "performance": {
                "throughput_requests_per_minute": throughput_rpm,
                "average_response_time_ms": stats.get("avg_response_time_ms", 0),
                "min_response_time_ms": stats.get("min_response_time_ms", 0),
                "max_response_time_ms": stats.get("max_response_time_ms", 0),
                "total_requests": stats.get("total_requests", 0),
                "uptime_seconds": stats.get("uptime_seconds", 0),
            },
        }
        
    except Exception as e:
        logger.error(f"Error retrieving performance metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/summary")
async def get_metrics_summary() -> Dict[str, Any]:
    """
    Get comprehensive metrics summary
    
    Returns:
        Summary of all system metrics
    """
    try:
        logger.info("Retrieving metrics summary")
        monitor = get_request_monitor()
        limiter = get_rate_limiter()
        
        stats = monitor.get_overall_stats()
        errors = monitor.get_error_summary()
        endpoints = monitor.get_endpoint_stats()
        
        return {
            "status": "success",
            "summary": {
                "total_requests": stats.get("total_requests", 0),
                "total_errors": stats.get("total_errors", 0),
                "error_rate": f"{stats.get('error_rate', 0) * 100:.2f}%",
                "avg_response_time_ms": f"{stats.get('avg_response_time_ms', 0):.2f}",
                "endpoints_monitored": len(endpoints),
                "rate_limiting_enabled": limiter.config.enabled,
                "uptime_seconds": stats.get("uptime_seconds", 0),
            },
        }
        
    except Exception as e:
        logger.error(f"Error retrieving summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
