# API dimostrativa: endpoint con e senza cache Redis su un catalogo
# prodotti reale (DB relazionale), non su dati finti in memoria.

import json
import os

import redis
from fastapi import FastAPI, HTTPException

from app import db

app = FastAPI(title="redis-sample")

CACHE_TTL_SECONDS = 30

# Se REDIS_URL non e' impostata, redis_client resta None e /data/cached
# si comporta come /data/nocache (nessuna dipendenza esterna richiesta).
_redis_url = os.environ.get("REDIS_URL")
redis_client = redis.from_url(_redis_url) if _redis_url else None

db.configure()
db.init_db()


def _lookup_product(item_id: int) -> dict | None:
    # Sorgente dati reale: query sul catalogo prodotti (SQLite in locale,
    # Azure Database for PostgreSQL quando DATABASE_URL punta a un'istanza
    # cloud). La latenza non e' piu' simulata: e' quella vera della query.
    return db.get_product(item_id)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/data/nocache/{item_id}")
def data_nocache(item_id: int):
    product = _lookup_product(item_id)
    if product is None:
        raise HTTPException(status_code=404, detail="item not found")
    return {**product, "source": "nocache"}


@app.get("/data/cached/{item_id}")
def data_cached(item_id: int):
    if redis_client is None:
        product = _lookup_product(item_id)
        if product is None:
            raise HTTPException(status_code=404, detail="item not found")
        return {**product, "source": "cached"}

    cache_key = f"item:{item_id}"
    cached_value = redis_client.get(cache_key)
    if cached_value is not None:
        return json.loads(cached_value)

    product = _lookup_product(item_id)
    if product is None:
        raise HTTPException(status_code=404, detail="item not found")
    data = {**product, "source": "cached"}
    redis_client.set(cache_key, json.dumps(data), ex=CACHE_TTL_SECONDS)
    return data
