"""
Monitoring & Rate Limiting Module
Implements request monitoring, metrics collection, and rate limiting
"""
import time
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
from functools import wraps
import threading

from app.logging_config import logger

try:
    from prometheus_client import Counter, Histogram, Gauge
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False


@dataclass
class RequestMetrics:
    """Metrics for a single request"""
    method: str
    path: str
    status_code: int
    duration_ms: float
    timestamp: datetime = field(default_factory=datetime.now)
    error: Optional[str] = None


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    max_requests: int = 100
    window_seconds: int = 60
    per_user: bool = False
    enabled: bool = True


class RateLimiter:
    """
    Simple rate limiter implementation
    Tracks requests per endpoint or user
    """
    
    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.request_log: Dict[str, list] = defaultdict(list)
        self.lock = threading.Lock()
    
    def is_allowed(self, identifier: str = "global") -> bool:
        """
        Check if request is allowed
        
        Args:
            identifier: User ID or "global" for endpoint rate limit
            
        Returns:
            True if request is allowed, False if rate limited
        """
        if not self.config.enabled:
            return True
        
        with self.lock:
            now = datetime.now()
            window_start = now - timedelta(seconds=self.config.window_seconds)
            
            # Clean old requests
            self.request_log[identifier] = [
                ts for ts in self.request_log[identifier]
                if ts > window_start
            ]
            
            # Check if limit exceeded
            if len(self.request_log[identifier]) >= self.config.max_requests:
                return False
            
            # Record request
            self.request_log[identifier].append(now)
            return True
    
    def get_remaining_requests(self, identifier: str = "global") -> int:
        """Get remaining requests in current window"""
        with self.lock:
            return max(0, self.config.max_requests - len(self.request_log[identifier]))


class RequestMonitor:
    """
    Monitors and tracks request metrics
    Collects metrics for monitoring and debugging
    """
    
    def __init__(self):
        self.metrics_history: list[RequestMetrics] = []
        self.endpoint_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "count": 0,
            "errors": 0,
            "total_duration_ms": 0.0,
            "min_duration_ms": float('inf'),
            "max_duration_ms": 0.0,
            "status_codes": defaultdict(int),
        })
        self.lock = threading.Lock()
        
        # Prometheus metrics (if available)
        if PROMETHEUS_AVAILABLE:
            self._init_prometheus()
    
    def _init_prometheus(self):
        """Initialize Prometheus metrics"""
        try:
            self.request_count = Counter(
                'semiml_requests_total',
                'Total HTTP requests',
                ['method', 'endpoint', 'status']
            )
            self.request_duration = Histogram(
                'semiml_request_duration_seconds',
                'HTTP request duration in seconds',
                ['method', 'endpoint']
            )
            self.request_errors = Counter(
                'semiml_errors_total',
                'Total errors',
                ['endpoint', 'error_type']
            )
            logger.info("Prometheus metrics initialized")
        except Exception as e:
            logger.warning(f"Could not initialize Prometheus: {str(e)}")
    
    def record_request(self, metrics: RequestMetrics):
        """
        Record a request
        
        Args:
            metrics: RequestMetrics object with request details
        """
        with self.lock:
            self.metrics_history.append(metrics)
            
            # Update endpoint stats
            endpoint = f"{metrics.method} {metrics.path}"
            stats = self.endpoint_stats[endpoint]
            
            stats["count"] += 1
            stats["total_duration_ms"] += metrics.duration_ms
            stats["min_duration_ms"] = min(stats["min_duration_ms"], metrics.duration_ms)
            stats["max_duration_ms"] = max(stats["max_duration_ms"], metrics.duration_ms)
            stats["status_codes"][metrics.status_code] += 1
            
            if metrics.status_code >= 400:
                stats["errors"] += 1
            
            # Record in Prometheus if available
            if PROMETHEUS_AVAILABLE:
                try:
                    self.request_count.labels(
                        method=metrics.method,
                        endpoint=metrics.path,
                        status=metrics.status_code
                    ).inc()
                    self.request_duration.labels(
                        method=metrics.method,
                        endpoint=metrics.path
                    ).observe(metrics.duration_ms / 1000.0)
                    
                    if metrics.status_code >= 400:
                        error_type = f"{metrics.status_code}"
                        self.request_errors.labels(
                            endpoint=metrics.path,
                            error_type=error_type
                        ).inc()
                except Exception as e:
                    logger.debug(f"Error recording Prometheus metric: {str(e)}")
    
    def get_endpoint_stats(self, endpoint: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics for endpoint(s)
        
        Args:
            endpoint: Specific endpoint or None for all
            
        Returns:
            Statistics dictionary
        """
        with self.lock:
            if endpoint:
                if endpoint not in self.endpoint_stats:
                    return {}
                
                stats = self.endpoint_stats[endpoint]
                return {
                    "endpoint": endpoint,
                    "requests": stats["count"],
                    "errors": stats["errors"],
                    "error_rate": stats["errors"] / stats["count"] if stats["count"] > 0 else 0,
                    "avg_duration_ms": stats["total_duration_ms"] / stats["count"] if stats["count"] > 0 else 0,
                    "min_duration_ms": stats["min_duration_ms"],
                    "max_duration_ms": stats["max_duration_ms"],
                    "status_codes": dict(stats["status_codes"]),
                }
            else:
                # Return all endpoint stats
                all_stats = {}
                for ep, stats in self.endpoint_stats.items():
                    all_stats[ep] = {
                        "requests": stats["count"],
                        "errors": stats["errors"],
                        "error_rate": stats["errors"] / stats["count"] if stats["count"] > 0 else 0,
                        "avg_duration_ms": stats["total_duration_ms"] / stats["count"] if stats["count"] > 0 else 0,
                    }
                return all_stats
    
    def get_overall_stats(self) -> Dict[str, Any]:
        """Get overall system statistics"""
        with self.lock:
            if not self.metrics_history:
                return {
                    "total_requests": 0,
                    "total_errors": 0,
                    "uptime_seconds": 0,
                }
            
            total_requests = len(self.metrics_history)
            total_errors = sum(1 for m in self.metrics_history if m.status_code >= 400)
            durations = [m.duration_ms for m in self.metrics_history]
            
            # Calculate uptime (from first request to now)
            if self.metrics_history:
                uptime = (datetime.now() - self.metrics_history[0].timestamp).total_seconds()
            else:
                uptime = 0
            
            return {
                "total_requests": total_requests,
                "total_errors": total_errors,
                "error_rate": total_errors / total_requests if total_requests > 0 else 0,
                "avg_response_time_ms": sum(durations) / len(durations) if durations else 0,
                "min_response_time_ms": min(durations) if durations else 0,
                "max_response_time_ms": max(durations) if durations else 0,
                "uptime_seconds": uptime,
                "endpoints_tracked": len(self.endpoint_stats),
            }
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors"""
        with self.lock:
            errors_by_code = defaultdict(int)
            errors_by_endpoint = defaultdict(int)
            
            for metric in self.metrics_history:
                if metric.status_code >= 400:
                    errors_by_code[metric.status_code] += 1
                    endpoint = f"{metric.method} {metric.path}"
                    errors_by_endpoint[endpoint] += 1
            
            return {
                "errors_by_status_code": dict(errors_by_code),
                "errors_by_endpoint": dict(errors_by_endpoint),
                "total_errors": sum(errors_by_code.values()),
            }


# Global instances
rate_limiter: Optional[RateLimiter] = None
request_monitor: Optional[RequestMonitor] = None


def get_rate_limiter(config: Optional[RateLimitConfig] = None) -> RateLimiter:
    """Get or initialize rate limiter"""
    global rate_limiter
    if rate_limiter is None:
        if config is None:
            config = RateLimitConfig()
        rate_limiter = RateLimiter(config)
    return rate_limiter


def get_request_monitor() -> RequestMonitor:
    """Get or initialize request monitor"""
    global request_monitor
    if request_monitor is None:
        request_monitor = RequestMonitor()
    return request_monitor


def rate_limit(max_requests: int = 100, window_seconds: int = 60):
    """
    Decorator for rate limiting
    
    Usage:
        @rate_limit(max_requests=10, window_seconds=60)
        async def my_endpoint():
            pass
    """
    def decorator(func: Callable) -> Callable:
        limiter = get_rate_limiter(RateLimitConfig(
            max_requests=max_requests,
            window_seconds=window_seconds
        ))
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get client identifier (could be IP, user ID, etc.)
            identifier = "global"  # In production, use request.client.host or user_id
            
            if not limiter.is_allowed(identifier):
                from fastapi import HTTPException
                remaining = limiter.get_remaining_requests(identifier)
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Requests remaining: {remaining}"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def monitor_request(func: Callable) -> Callable:
    """
    Decorator for request monitoring
    
    Usage:
        @monitor_request
        async def my_endpoint():
            pass
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        monitor = get_request_monitor()
        
        # Would need request context to get method/path
        # This is a simplified version
        method = "GET"
        path = func.__name__
        
        try:
            result = await func(*args, **kwargs)
            status_code = 200
            duration_ms = (time.time() - start_time) * 1000
            
            metrics = RequestMetrics(
                method=method,
                path=path,
                status_code=status_code,
                duration_ms=duration_ms
            )
            monitor.record_request(metrics)
            
            return result
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            metrics = RequestMetrics(
                method=method,
                path=path,
                status_code=500,
                duration_ms=duration_ms,
                error=str(e)
            )
            monitor.record_request(metrics)
            raise
    
    return wrapper
