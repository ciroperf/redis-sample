# redis-sample

Dimostra, con numeri, i vantaggi e gli svantaggi del caching con Redis in un
contesto enterprise: una API simula una sorgente dati "lenta" (es. una query
su un sistema legacy), espone una versione con cache Redis e una senza, e un
benchmark strutturato misura la differenza. I risultati si trasformano in
grafici pronti per una presentazione.

## Per chi

Chi deve motivare (o mettere in discussione) l'introduzione di Redis come
cache in un'architettura esistente, con dati alla mano invece che opinioni.

## Stack

- Python 3.12, FastAPI (API dimostrativa) + redis-py
- Terraform + provider `azurerm` per l'istanza Azure Cache for Redis
- Script Python (`benchmark/`, `charts/`) per raccogliere e visualizzare i KPI
- Test: pytest (con `fakeredis`, nessuna istanza Redis reale richiesta)

## Avvio in locale

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Per usare una cache Redis reale in locale, esporta `REDIS_URL` (es. da
un'istanza Docker o dall'Azure Cache for Redis creata via Terraform) prima di
avviare l'app. Senza `REDIS_URL` l'endpoint cache si comporta come un
no-op, utile per sviluppare senza dipendenze esterne.

## Endpoint disponibili

- `GET /health` — controllo di stato, risponde sempre 200.
- `GET /data/nocache/{item_id}` — simula una sorgente dati lenta (50-150ms
  di latenza artificiale), base per il confronto con la versione con cache
  Redis.
- `GET /data/cached/{item_id}` — stessa sorgente lenta, ma il risultato
  viene letto/scritto su Redis con TTL di 30s prima di rifare il lavoro
  costoso. Senza `REDIS_URL` impostata si comporta come `nocache` (nessun
  crash, nessuna dipendenza esterna richiesta in sviluppo).

Esempio:

```bash
$ curl -w '\ntempo: %{time_total}s\n' http://127.0.0.1:8000/data/nocache/1
{"item_id":1,"source":"nocache","value":42}
tempo: 0.104s

$ curl -w '\ntempo: %{time_total}s\n' http://127.0.0.1:8000/data/cached/1
{"item_id":1,"value":42,"source":"cached"}
tempo: 0.098s

$ curl -w '\ntempo: %{time_total}s\n' http://127.0.0.1:8000/data/cached/1
{"item_id":1,"value":42,"source":"cached"}
tempo: 0.002s
```

## Test

```bash
pytest
```

## Benchmark e grafici

```bash
python benchmark/run_benchmark.py   # produce un CSV con i tempi di risposta
python charts/generate_charts.py    # legge il CSV e genera i grafici KPI
```

## Infrastruttura (Azure)

```bash
cd terraform
terraform init
terraform apply
```

Crea un resource group e un'istanza Azure Cache for Redis da usare per i
test contro un servizio reale (non solo in locale).

## Screenshot

_(da aggiungere)_
