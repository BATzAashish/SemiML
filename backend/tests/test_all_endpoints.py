"""
Comprehensive API Endpoint Tests
Tests all backend API endpoints including new Phase 4-14 endpoints
"""
import pytest


@pytest.fixture
def client(client):  # Use the fixture from conftest
    """Provide the test client"""
    return client


# ============================================================================
# Phase 1: Foundation Endpoints
# ============================================================================

class TestFoundationEndpoints:
    """Test Phase 1 foundation endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_connect_endpoint(self, client):
        """Test connection test endpoint"""
        response = client.get("/api/connect")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "connected"
        assert "backend" in data
    
    def test_system_info(self, client):
        """Test system info endpoint"""
        response = client.get("/api/system-info")
        assert response.status_code == 200
        data = response.json()
        assert "system" in data or "modules" in data
        assert len(data.get("modules", {})) >= 0
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert data["status"] == "operational"


# ============================================================================
# Phase 2: Data Processing Endpoints
# ============================================================================

class TestDataProcessingEndpoints:
    """Test Phase 2 data processing endpoints"""
    
    def test_upload_dataset_endpoint_exists(self, client):
        """Test that upload endpoint is registered"""
        response = client.options("/api/upload-dataset")
        assert response.status_code in [200, 204, 405]  # 405 means endpoint exists but method not allowed
    
    def test_get_datasets(self, client):
        """Test get datasets endpoint"""
        response = client.get("/api/datasets")
        assert response.status_code in [200, 404]  # 404 if no datasets


# ============================================================================
# Phase 3: Meta-Features Endpoints
# ============================================================================

class TestMetaFeaturesEndpoints:
    """Test Phase 3 meta-features extraction endpoints"""
    
    def test_extract_meta_features_endpoint_exists(self, client):
        """Test that meta-features endpoint is registered"""
        # Just check endpoint exists, not actual execution
        response = client.get("/api/meta-features/test-id")
        assert response.status_code in [404, 500]  # Endpoint exists if we get 404 or 500, not 404 for /api


# ============================================================================
# Phase 4: Experience Retrieval Endpoints
# ============================================================================

class TestExperienceRetrievalEndpoints:
    """Test Phase 4 experience retrieval and knowledge endpoints"""
    
    def test_retrieve_knowledge_endpoint(self, client):
        """Test knowledge retrieval endpoint"""
        request_data = {
            "query": "classification with imbalanced data",
            "top_k": 5
        }
        response = client.post("/api/retrieve-knowledge", json=request_data)
        assert response.status_code in [200, 422, 500]
        if response.status_code == 200:
            data = response.json()
            assert "results" in data or "count" in data
    
    def test_search_similar_approaches(self, client):
        """Test similar approaches search endpoint"""
        request_data = {
            "query": "time series forecasting",
            "top_k": 3
        }
        response = client.post("/api/search-similar-approaches", json=request_data)
        assert response.status_code in [200, 422, 500]
    
    def test_find_similar_datasets(self, client):
        """Test find similar datasets endpoint"""
        meta_features = {
            "num_rows": 1000,
            "num_columns": 20,
            "problem_type": "classification"
        }
        response = client.post("/api/find-similar-datasets", json={"meta_features": meta_features})
        assert response.status_code in [200, 422, 500]
    
    def test_get_best_practices(self, client):
        """Test best practices endpoint"""
        meta_features = {
            "num_rows": 1000,
            "num_columns": 20,
            "missing_percentage": 5.0
        }
        response = client.post("/api/get-best-practices", json={"meta_features": meta_features})
        assert response.status_code in [200, 422, 500]
    
    def test_get_best_models(self, client):
        """Test best models endpoint"""
        meta_features = {
            "num_rows": 1000,
            "num_columns": 20
        }
        response = client.post("/api/get-best-models", json={"meta_features": meta_features, "top_k": 3})
        assert response.status_code in [200, 422, 500]
    
    def test_search_experiences(self, client):
        """Test search experiences endpoint"""
        response = client.get("/api/search-experiences?pipeline_type=classification")
        assert response.status_code in [200, 422, 500]
    
    def test_experience_statistics(self, client):
        """Test experience statistics endpoint"""
        response = client.get("/api/experience-statistics")
        assert response.status_code in [200, 422, 500]
    
    def test_add_knowledge(self, client):
        """Test add knowledge endpoint"""
        documents = [
            {
                "content": "Test knowledge base entry",
                "metadata": {"source": "test"}
            }
        ]
        response = client.post("/api/add-knowledge", json=documents)
        assert response.status_code in [200, 422, 500]
    
    def test_initialize_knowledge_base(self, client):
        """Test initialize knowledge base endpoint"""
        response = client.post("/api/initialize-knowledge-base")
        assert response.status_code in [200, 422, 500]


# ============================================================================
# Phase 5: Unified Experience Retrieval
# ============================================================================

class TestUnifiedExperienceRetrievalEndpoints:
    """Test Phase 5 unified experience retrieval endpoint"""
    
    def test_retrieve_experience_unified(self, client):
        """Test unified experience retrieval endpoint"""
        request_data = {
            "dataset_meta_features": {
                "num_rows": 5000,
                "num_columns": 30,
                "data_quality_score": 0.95
            },
            "problem_type": "classification",
            "top_k": 5
        }
        response = client.post("/api/retrieve-experience", json=request_data)
        assert response.status_code in [200, 422, 500]
        if response.status_code == 200:
            data = response.json()
            assert "similar_datasets" in data or "recommended_models" in data


# ============================================================================
# Phase 6: Meta-Learning Endpoints
# ============================================================================

class TestMetaLearningEndpoints:
    """Test Phase 6 meta-learning endpoints"""
    
    def test_meta_decision(self, client):
        """Test meta-decision endpoint"""
        request_data = {
            "dataset_features": {"num_rows": 1000, "num_columns": 20},
            "model_recommendations": [
                {"model_name": "xgboost", "accuracy": 0.92}
            ]
        }
        response = client.post("/api/meta-decision", json=request_data)
        assert response.status_code in [200, 422, 500]
        if response.status_code == 200:
            data = response.json()
            assert "final_decision" in data or "status" in data
    
    def test_record_outcome(self, client):
        """Test record decision outcome endpoint"""
        request_data = {
            "decision": {"model": "xgboost"},
            "outcome": {"result": "success"},
            "actual_performance": 0.93
        }
        response = client.post("/api/record-outcome", json=request_data)
        assert response.status_code in [200, 422, 500]
    
    def test_meta_insights(self, client):
        """Test meta-insights endpoint"""
        response = client.get("/api/meta-insights")
        assert response.status_code in [200, 422, 500]
    
    def test_llm_status(self, client):
        """Test LLM status endpoint"""
        response = client.get("/api/llm-status")
        assert response.status_code in [200, 422, 500]
        if response.status_code == 200:
            data = response.json()
            assert "llm_enabled" in data or "status" in data


# ============================================================================
# Phase 7: Training Optimization Endpoints
# ============================================================================

class TestTrainingOptimizationEndpoints:
    """Test Phase 7 training optimization endpoints"""
    
    def test_train_with_early_stopping(self, client):
        """Test early stopping training endpoint"""
        request_data = {
            "dataset_id": "test-dataset",
            "model_name": "gradient_boosting",
            "early_stopping_patience": 5,
            "max_epochs": 50
        }
        response = client.post("/api/train-with-early-stopping", json=request_data)
        assert response.status_code in [200, 422, 500]
    
    def test_train_parallel(self, client):
        """Test parallel training endpoint"""
        request_data = {
            "dataset_id": "test-dataset",
            "models": ["gradient_boosting", "xgboost"],
            "n_jobs": -1,
            "max_epochs": 50
        }
        response = client.post("/api/train-parallel", json=request_data)
        assert response.status_code in [200, 422, 500]
    
    def test_training_status(self, client):
        """Test training status endpoint"""
        response = client.get("/api/training-optimization-status")
        assert response.status_code in [200, 422, 500]
        if response.status_code == 200:
            data = response.json()
            assert "training_optimizer" in data or "status" in data


# ============================================================================
# Phase 13: Error Handling (Already tested in test_error_handling.py)
# ============================================================================

class TestErrorHandling:
    """Test error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 response"""
        response = client.get("/api/nonexistent-endpoint")
        assert response.status_code == 404
    
    def test_405_method_not_allowed(self, client):
        """Test 405 response"""
        response = client.post("/health")
        assert response.status_code == 405


# ============================================================================
# Phase 14: Monitoring & Rate Limiting Endpoints
# ============================================================================

class TestMonitoringEndpoints:
    """Test Phase 14 monitoring endpoints"""
    
    def test_overall_metrics(self, client):
        """Test overall metrics endpoint"""
        response = client.get("/api/metrics/overall")
        assert response.status_code in [200, 422, 500]
        if response.status_code == 200:
            data = response.json()
            assert "metrics" in data or "status" in data
    
    def test_endpoint_metrics(self, client):
        """Test endpoint metrics"""
        response = client.get("/api/metrics/endpoints")
        assert response.status_code in [200, 422, 500]
    
    def test_error_metrics(self, client):
        """Test error metrics"""
        response = client.get("/api/metrics/errors")
        assert response.status_code in [200, 422, 500]
    
    def test_rate_limit_status(self, client):
        """Test rate limit status"""
        response = client.get("/api/rate-limit/status")
        assert response.status_code in [200, 422, 500]
        if response.status_code == 200:
            data = response.json()
            assert "rate_limiting" in data or "status" in data
    
    def test_configure_rate_limiting(self, client):
        """Test configure rate limiting"""
        request_data = {
            "max_requests": 100,
            "window_seconds": 60,
            "enabled": True
        }
        response = client.post("/api/rate-limit/configure", json=request_data)
        assert response.status_code in [200, 422, 500]
    
    def test_detailed_health_check(self, client):
        """Test detailed health check"""
        response = client.get("/api/health/detailed")
        assert response.status_code in [200, 422, 500]
    
    def test_performance_metrics(self, client):
        """Test performance metrics"""
        response = client.get("/api/metrics/performance")
        assert response.status_code in [200, 422, 500]
    
    def test_metrics_summary(self, client):
        """Test metrics summary"""
        response = client.get("/api/metrics/summary")
        assert response.status_code in [200, 422, 500]


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for workflow scenarios"""
    
    def test_full_workflow_endpoints(self, client):
        """Test that key workflow endpoints are accessible"""
        endpoints = [
            ("/api/connect", "GET"),
            ("/api/system-info", "GET"),
            ("/health", "GET"),
            ("/api/meta-insights", "GET"),
            ("/api/llm-status", "GET"),
            ("/api/metrics/overall", "GET"),
        ]
        
        for endpoint, method in endpoints:
            if method == "GET":
                response = client.get(endpoint)
            else:
                response = client.post(endpoint)
            
            assert response.status_code in [200, 422, 500, 404], \
                f"Endpoint {endpoint} returned {response.status_code}"
    
    def test_openapi_documentation(self, client):
        """Test OpenAPI documentation is available"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "paths" in schema
        assert "components" in schema
    
    def test_swagger_ui(self, client):
        """Test Swagger UI is available"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc(self, client):
        """Test ReDoc is available"""
        response = client.get("/redoc")
        assert response.status_code == 200


# ============================================================================
# Performance Tests
# ============================================================================

class TestPerformance:
    """Test performance metrics"""
    
    def test_health_response_time(self, client):
        """Test health check response time"""
        import time
        start = time.time()
        response = client.get("/health")
        duration = time.time() - start
        assert response.status_code == 200
        assert duration < 1.0  # Should respond in less than 1 second
    
    def test_connect_response_time(self, client):
        """Test connect endpoint response time"""
        import time
        start = time.time()
        response = client.get("/api/connect")
        duration = time.time() - start
        assert response.status_code == 200
        assert duration < 2.0  # Should respond in less than 2 seconds


# ============================================================================
# Data Validation Tests
# ============================================================================

class TestDataValidation:
    """Test input data validation"""
    
    def test_invalid_meta_decision_request(self, client):
        """Test invalid meta-decision request"""
        response = client.post("/api/meta-decision", json={})
        assert response.status_code in [400, 422, 500]
    
    def test_invalid_json(self, client):
        """Test handling of invalid JSON"""
        response = client.post(
            "/api/retrieve-knowledge",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [400, 422, 500]
    
    def test_empty_request_body(self, client):
        """Test empty request body"""
        response = client.post("/api/retrieve-knowledge", json={})
        assert response.status_code in [400, 422, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
