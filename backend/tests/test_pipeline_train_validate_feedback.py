def test_pipeline_training_validation_feedback(client, sample_dataset_file):
    upload = client.post("/api/upload-dataset", files={"file": sample_dataset_file["file"]})
    assert upload.status_code == 200
    dataset_id = upload.json()["dataset_id"]

    meta = client.post(f"/api/extract-meta-features/{dataset_id}")
    assert meta.status_code == 200
    meta_features = meta.json()["meta_features"]

    build_payload = {
        "pipeline_config": {
            "problem_type": "classification",
            "preprocessing": [
                {"name": "handle_missing", "step_type": "preprocessing", "parameters": {}},
                {"name": "scale_features", "step_type": "preprocessing", "parameters": {}},
            ],
            "feature_engineering": [],
            "model": {
                "name": "random_forest",
                "step_type": "model",
                "parameters": {"n_estimators": 20, "max_depth": 5},
            },
        },
        "dataset_meta_features": meta_features,
    }

    build = client.post("/api/build-pipeline", json=build_payload)
    assert build.status_code == 200
    pipeline_id = build.json()["pipeline_id"]

    train_payload = {
        "dataset_id": dataset_id,
        "pipeline_id": pipeline_id,
        "target_column": "label",
        "test_size": 0.2,
        "cv_folds": 3,
        "tune_hyperparameters": False,
    }

    train = client.post("/api/train-pipeline", json=train_payload)
    assert train.status_code == 200
    training = train.json()["training"]
    model_id = training["model_id"]

    validate = client.post(
        "/api/validate-model",
        json={"dataset_id": dataset_id, "pipeline_id": pipeline_id, "target_column": "label", "cv_folds": 3},
    )
    assert validate.status_code == 200

    trace_payload = {
        "decision": "RandomForest baseline",
        "reasoning": ["Balanced features", "Small dataset"],
        "confidence": 0.8,
        "sources": ["rule-engine"],
        "alternatives": [{"model": "LogisticRegression", "score": 0.7}],
    }
    trace = client.post("/api/decision-trace", json=trace_payload)
    assert trace.status_code == 200

    feedback_payload = {
        "dataset_id": dataset_id,
        "pipeline_id": pipeline_id,
        "model_id": model_id,
        "target_column": "label",
        "performance_metrics": training["metrics"],
        "dataset_meta_features": meta_features,
        "notes": "baseline accepted",
        "accepted": True,
    }
    feedback = client.post("/api/feedback", json=feedback_payload)
    assert feedback.status_code == 200

    delete = client.delete(f"/api/dataset/{dataset_id}")
    assert delete.status_code == 200
