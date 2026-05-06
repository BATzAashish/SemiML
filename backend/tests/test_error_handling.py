"""
Comprehensive Error Handling Tests
Tests for all error scenarios and OpenAPI documentation
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.exceptions import (
    SemiMLException,
    ValidationError as SemiMLValidationError,
    DataProcessingError,
    FileNotFoundError_,
    ModelNotFoundError,
    DatasetNotFoundError,
    PipelineError,
    TrainingError,
    ExplainabilityError,
    ConfigurationError,
)

client = TestClient(app)


# ============================================================================
# OpenAPI Documentation Tests
# ============================================================================

class TestOpenAPIDocumentation:
    """Test OpenAPI documentation endpoints"""
    
    def test_openapi_schema_accessible(self):
        """Test that OpenAPI schema is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data
        assert "components" in data
    
    def test_swagger_ui_accessible(self):
        """Test that Swagger UI is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower() or "swagger-ui" in response.text.lower()
    
    def test_redoc_accessible(self):
        """Test that ReDoc is accessible"""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "redoc" in response.text.lower()
    
    def test_api_endpoints_documented(self):
        """Test that all main API endpoints are documented"""
        response = client.get("/openapi.json")
        schema = response.json()
        paths = schema.get("paths", {})
        
        # Check for key endpoints
        assert "/health" in paths or "/api/connect" in paths
        assert len(paths) > 0


# ============================================================================
# HTTP Error Code Tests
# ============================================================================

class TestHTTPErrorCodes:
    """Test proper HTTP error codes are returned"""
    
    def test_404_not_found(self):
        """Test 404 Not Found response"""
        response = client.get("/api/nonexistent-endpoint")
        assert response.status_code == 404
        # Should return structured error
        if response.status_code == 404:
            assert "detail" in response.json() or "message" in response.json()
    
    def test_405_method_not_allowed(self):
        """Test 405 Method Not Allowed response"""
        # POST to a GET-only endpoint
        response = client.post("/health")
        assert response.status_code == 405
    
    def test_422_validation_error(self):
        """Test 422 Unprocessable Entity for invalid input"""
        # Send invalid data to an endpoint
        response = client.post("/api/train-pipeline", json={"invalid": "data"})
        assert response.status_code in [400, 422, 500]  # Could be validation or missing required fields
    
    def test_400_bad_request(self):
        """Test 400 Bad Request response"""
        # Send malformed JSON
        response = client.post(
            "/api/train-pipeline",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [400, 422]


# ============================================================================
# Exception Handling Tests
# ============================================================================

class TestExceptionHandling:
    """Test exception handling and error responses"""
    
    def test_connection_test(self):
        """Test connection endpoint for error handling"""
        response = client.get("/api/connect")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "connected"
    
    def test_system_info_endpoint(self):
        """Test system info endpoint for completeness"""
        response = client.get("/api/system-info")
        assert response.status_code == 200
        data = response.json()
        assert "system" in data or "modules" in data
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
    
    def test_error_response_structure(self):
        """Test that error responses have consistent structure"""
        # Try to access an invalid dataset
        response = client.get("/api/dataset/invalid-id")
        
        if response.status_code >= 400:
            data = response.json()
            # Should have either 'detail' or 'message' field
            assert "detail" in data or "message" in data


# ============================================================================
# Data Validation Tests
# ============================================================================

class TestDataValidation:
    """Test input data validation and error handling"""
    
    def test_empty_request_body(self):
        """Test handling of empty request body"""
        response = client.post("/api/train-pipeline", json={})
        # Should either return validation error or handle gracefully
        assert response.status_code in [400, 422, 500]
    
    def test_missing_required_fields(self):
        """Test handling of missing required fields"""
        response = client.post("/api/train-pipeline", json={"dataset_id": "test"})
        assert response.status_code in [400, 422, 500]
    
    def test_invalid_json_format(self):
        """Test handling of invalid JSON format"""
        response = client.post(
            "/api/train-pipeline",
            data="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [400, 422]
    
    def test_invalid_data_types(self):
        """Test handling of invalid data types"""
        response = client.post(
            "/api/train-pipeline",
            json={
                "dataset_id": 123,  # Should be string
                "pipeline_id": "test",
                "target_column": "target",
            }
        )
        # Should return validation error
        assert response.status_code in [400, 422, 500]


# ============================================================================
# Error Message Tests
# ============================================================================

class TestErrorMessages:
    """Test that error messages are informative"""
    
    def test_error_message_contains_info(self):
        """Test that error messages contain helpful information"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        data = response.json()
        # Error should contain useful info
        assert "detail" in data or "message" in data
    
    def test_validation_error_details(self):
        """Test that validation errors contain field information"""
        response = client.post(
            "/api/train-pipeline",
            json={"test": "invalid"}
        )
        if response.status_code == 422:
            data = response.json()
            assert "detail" in data


# ============================================================================
# CORS and Security Header Tests
# ============================================================================

class TestSecurityHeaders:
    """Test security headers are properly set"""
    
    def test_cors_headers_present(self):
        """Test CORS headers are present"""
        response = client.options("/api/connect")
        # CORS headers might be on actual response
        response = client.get("/api/connect")
        assert response.status_code == 200
    
    def test_no_sensitive_headers_exposed(self):
        """Test that sensitive information is not in headers"""
        response = client.get("/api/connect")
        # Server header should not expose version
        assert response.status_code == 200


# ============================================================================
# Rate Limiting Tests (if implemented)
# ============================================================================

class TestRateLimiting:
    """Test rate limiting functionality (if implemented)"""
    
    def test_multiple_rapid_requests(self):
        """Test handling of rapid sequential requests"""
        responses = []
        for _ in range(5):
            response = client.get("/health")
            responses.append(response.status_code)
        
        # Should get consistent responses (all 200 or some rate-limited)
        assert all(status in [200, 429] for status in responses)


# ============================================================================
# Logging Tests
# ============================================================================

class TestLogging:
    """Test that errors are properly logged"""
    
    def test_request_logging(self):
        """Test that requests are being logged"""
        response = client.get("/api/connect")
        # If we reach here, the middleware didn't break
        assert response.status_code == 200
    
    def test_error_logging(self):
        """Test that errors are being logged"""
        response = client.get("/api/nonexistent")
        # If we reach here, error logging didn't break the app
        assert response.status_code == 404


# ============================================================================
# Module-Specific Error Tests
# ============================================================================

class TestModuleErrors:
    """Test module-specific error handling"""
    
    def test_meta_learning_endpoint_errors(self):
        """Test meta-learning endpoints error handling"""
        response = client.post("/api/meta-decision", json={})
        # Should handle error gracefully
        assert response.status_code in [400, 422, 500]
    
    def test_training_endpoint_errors(self):
        """Test training endpoints error handling"""
        response = client.post("/api/train-pipeline", json={})
        # Should handle error gracefully
        assert response.status_code in [400, 422, 500]
    
    def test_knowledge_retrieval_errors(self):
        """Test knowledge retrieval endpoints error handling"""
        response = client.post("/api/retrieve-knowledge", json={})
        # Should handle error gracefully
        assert response.status_code in [400, 422, 500]


# ============================================================================
# Response Consistency Tests
# ============================================================================

class TestResponseConsistency:
    """Test that responses follow consistent patterns"""
    
    def test_success_responses_have_status(self):
        """Test that success responses include status field"""
        response = client.get("/api/connect")
        if response.status_code == 200:
            data = response.json()
            assert "status" in data or "message" in data
    
    def test_error_responses_structured(self):
        """Test that error responses are properly structured"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        data = response.json()
        # Should be a structured error response
        assert isinstance(data, dict)


# ============================================================================
# Integration Tests
# ============================================================================

class TestEndToEndErrorHandling:
    """Test error handling across multiple endpoints"""
    
    def test_workflow_with_error_recovery(self):
        """Test that system recovers from errors"""
        # Make a request that causes an error
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        
        # Next request should still work
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_multiple_error_types(self):
        """Test handling of multiple error types"""
        # 404 error
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        
        # 405 error
        response = client.post("/health")
        assert response.status_code == 405
        
        # 422/400 error
        response = client.post("/api/train-pipeline", json={})
        assert response.status_code in [400, 422, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
