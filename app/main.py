# API dimostrativa: endpoint con e senza cache Redis.
# Implementazione nei task del piano, non qui.

import random
import time

from fastapi import FastAPI

app = FastAPI(title="redis-sample")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/data/nocache/{item_id}")
def data_nocache(item_id: int):
    return {"item_id": item_id, "source": "nocache", "value": 42}
