def test_decision_engine(client):
    meta_features = {
        "basic_info": {"num_rows": 100, "num_columns": 5},
        "feature_analysis": {"numeric_columns": 3, "categorical_columns": 2},
        "data_quality": {"overall_quality_score": 90, "completeness_score": 100},
        "class_distribution": {
            "potential_target_columns": [{"column": "label", "unique_values": 2}]
        },
    }

    response = client.post("/api/decide-pipeline", json={"dataset_meta_features": meta_features})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert "decision" in payload
