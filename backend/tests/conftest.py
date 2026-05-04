import io

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def _sample_csv_bytes() -> bytes:
    csv_content = """feature1,feature2,label
1,10,0
2,20,0
3,30,1
4,40,1
5,50,1
"""
    return csv_content.encode("utf-8")


@pytest.fixture()
def sample_dataset_file():
    return {
        "file": ("sample.csv", io.BytesIO(_sample_csv_bytes()), "text/csv"),
        "description": "test dataset",
    }
