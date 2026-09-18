# Test dell'API: implementazione nei task del piano.

import fakeredis
from fastapi.testclient import TestClient

import app.main as main_module
from app.main import app
from app.seed_data import PRODUCTS

client = TestClient(app)


def _expected_product(item_id: int, source: str) -> dict:
    product = next(p for p in PRODUCTS if p["id"] == item_id)
    return {
        "item_id": product["id"],
        "sku": product["sku"],
        "name": product["name"],
        "category": product["category"],
        "price_eur": product["price_eur"],
        "stock_quantity": product["stock_quantity"],
        "source": source,
    }


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_data_nocache():
    response = client.get("/data/nocache/1")

    assert response.status_code == 200
    assert response.json() == _expected_product(1, "nocache")


def test_data_nocache_missing_item():
    response = client.get("/data/nocache/999999")

    assert response.status_code == 404


def test_data_cached_without_redis_url(monkeypatch):
    # Senza REDIS_URL l'endpoint funziona comunque, senza dipendenze esterne.
    monkeypatch.setattr(main_module, "redis_client", None)

    response = client.get("/data/cached/2")

    assert response.status_code == 200
    assert response.json() == _expected_product(2, "cached")


def test_data_cached_second_call_is_cache_hit(monkeypatch):
    monkeypatch.setattr(main_module, "redis_client", fakeredis.FakeRedis())

    call_count = 0
    original_lookup_product = main_module._lookup_product

    def counting_lookup_product(item_id):
        nonlocal call_count
        call_count += 1
        return original_lookup_product(item_id)

    monkeypatch.setattr(main_module, "_lookup_product", counting_lookup_product)

    first = client.get("/data/cached/3")
    second = client.get("/data/cached/3")

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert call_count == 1
