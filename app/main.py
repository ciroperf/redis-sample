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
def get_data_nocache(item_id: int):
    # Simula una sorgente dati lenta (es. query non ottimizzata su DB).
    time.sleep(random.uniform(0.05, 0.15))
    return {"item_id": item_id, "source": "nocache", "value": item_id * 42}
