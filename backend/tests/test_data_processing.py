def test_upload_and_meta_features(client, sample_dataset_file):
    response = client.post("/api/upload-dataset", files={"file": sample_dataset_file["file"]})
    assert response.status_code == 200
    payload = response.json()
    dataset_id = payload["dataset_id"]
    assert payload["status"] == "success"

    meta = client.post(f"/api/extract-meta-features/{dataset_id}")
    assert meta.status_code == 200
    meta_payload = meta.json()
    assert meta_payload["status"] == "success"
    assert "meta_features" in meta_payload

    info = client.get(f"/api/dataset/{dataset_id}")
    assert info.status_code == 200

    delete = client.delete(f"/api/dataset/{dataset_id}")
    assert delete.status_code == 200
