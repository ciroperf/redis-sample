# Test dell'API: implementazione nei task del piano.

import time

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_data_nocache():
    start = time.perf_counter()
    response = client.get("/data/nocache/1")
    elapsed = time.perf_counter() - start

    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "source": "nocache", "value": 42}
    assert elapsed > 0.05
