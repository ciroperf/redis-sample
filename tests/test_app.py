# Test dell'API: implementazione nei task del piano.

import time

import fakeredis
from fastapi.testclient import TestClient

import app.main as main_module
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


def test_data_cached_without_redis_url(monkeypatch):
    # Senza REDIS_URL l'endpoint funziona comunque, senza dipendenze esterne.
    monkeypatch.setattr(main_module, "redis_client", None)

    response = client.get("/data/cached/2")

    assert response.status_code == 200
    assert response.json() == {"item_id": 2, "source": "cached", "value": 42}


def test_data_cached_second_call_is_cache_hit(monkeypatch):
    monkeypatch.setattr(main_module, "redis_client", fakeredis.FakeRedis())

    call_count = 0
    original_slow_lookup = main_module._slow_lookup

    def counting_slow_lookup(item_id):
        nonlocal call_count
        call_count += 1
        return original_slow_lookup(item_id)

    monkeypatch.setattr(main_module, "_slow_lookup", counting_slow_lookup)

    first = client.get("/data/cached/3")
    second = client.get("/data/cached/3")

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert call_count == 1
