# API dimostrativa: endpoint con e senza cache Redis.

import json
import os
import random
import time

import redis
from fastapi import FastAPI

app = FastAPI(title="redis-sample")

CACHE_TTL_SECONDS = 30

# Se REDIS_URL non e' impostata, redis_client resta None e /data/cached
# si comporta come /data/nocache (nessuna dipendenza esterna richiesta).
_redis_url = os.environ.get("REDIS_URL")
redis_client = redis.from_url(_redis_url) if _redis_url else None


def _slow_lookup(item_id: int) -> dict:
    # Simula una sorgente dati lenta (50-150ms)
    time.sleep(random.uniform(0.05, 0.15))
    return {"item_id": item_id, "value": 42}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/data/nocache/{item_id}")
def data_nocache(item_id: int):
    return {**_slow_lookup(item_id), "source": "nocache"}


@app.get("/data/cached/{item_id}")
def data_cached(item_id: int):
    if redis_client is None:
        return {**_slow_lookup(item_id), "source": "cached"}

    cache_key = f"item:{item_id}"
    cached_value = redis_client.get(cache_key)
    if cached_value is not None:
        return json.loads(cached_value)

    data = {**_slow_lookup(item_id), "source": "cached"}
    redis_client.set(cache_key, json.dumps(data), ex=CACHE_TTL_SECONDS)
    return data
