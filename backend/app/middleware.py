"""
Middleware for SemiML Backend
Handles error responses, request logging, and common headers
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.exceptions import SemiMLException
from app.logging_config import logger
import time
import uuid


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle all exceptions and return structured error responses"""
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            return response
        except SemiMLException as e:
            logger.error(
                f"SemiML Exception in {request.method} {request.url.path}: {e.message}",
                extra={"error_code": e.error_code, "request_id": request_id}
            )
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "error": True,
                    "error_code": e.error_code,
                    "message": e.message,
                    "details": e.details,
                    "request_id": request_id
                },
                headers={"X-Request-ID": request_id}
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in {request.method} {request.url.path}: {str(e)}",
                exc_info=True,
                extra={"request_id": request_id}
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error": True,
                    "error_code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                    "request_id": request_id
                },
                headers={"X-Request-ID": request_id}
            )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all incoming requests and response times"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        logger.info(
            f"→ {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else "unknown"
            }
        )
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(
            f"← {request.method} {request.url.path} {response.status_code} ({process_time:.3f}s)",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(process_time * 1000)
            }
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response
