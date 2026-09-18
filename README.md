# redis-sample

Dimostra, con numeri, i vantaggi e gli svantaggi del caching con Redis in un
contesto enterprise: una API legge da una sorgente dati reale (un catalogo
prodotti su database relazionale), espone una versione con cache Redis e
una senza, e un benchmark strutturato misura la differenza. I risultati si
trasformano in grafici pronti per una presentazione.

## Per chi

Chi deve motivare (o mettere in discussione) l'introduzione di Redis come
cache in un'architettura esistente, con dati alla mano invece che opinioni.

Per il contesto su cos'e' Redis, quando conviene come cache e quando no,
si veda [`docs/redis-overview.md`](docs/redis-overview.md). Per collegare
l'app a un database e a una cache Redis reali su Azure, si veda
[`docs/database-setup.md`](docs/database-setup.md).

## Stack

- Python 3.12, FastAPI (API dimostrativa) + redis-py
- SQLAlchemy per il catalogo prodotti (SQLite in locale, Azure Database for
  PostgreSQL in cloud — vedi `app/db.py`)
- Terraform + provider `azurerm` per Azure Cache for Redis e Azure Database
  for PostgreSQL
- Script Python (`benchmark/`, `charts/`) per raccogliere e visualizzare i KPI
- Test: pytest, su un database reale (SQLite temporaneo seedato con lo
  stesso catalogo di riferimento usato in produzione — nessun dato finto da
  libreria di mock); `fakeredis` resta usato solo per il livello cache

## Avvio in locale

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Senza `DATABASE_URL` l'app crea e popola un file SQLite locale
(`catalog.db`) con il catalogo di riferimento (`app/seed_data.py`): nessuna
dipendenza esterna richiesta per iniziare. Per usare un database reale
(es. l'Azure Database for PostgreSQL creato via Terraform), esporta
`DATABASE_URL` prima di avviare l'app — vedi
[`docs/database-setup.md`](docs/database-setup.md).

Per usare una cache Redis reale in locale, esporta `REDIS_URL` (es. da
un'istanza Docker o dall'Azure Cache for Redis creata via Terraform) prima di
avviare l'app. Senza `REDIS_URL` l'endpoint cache si comporta come un
no-op, utile per sviluppare senza dipendenze esterne.

Un file `.env.example` documenta entrambe le variabili.

## Endpoint disponibili

- `GET /health` — controllo di stato, risponde sempre 200.
- `GET /data/nocache/{item_id}` — legge un prodotto dal catalogo (DB
  relazionale), base per il confronto con la versione con cache Redis.
  Risponde 404 se `item_id` non esiste.
- `GET /data/cached/{item_id}` — stessa sorgente, ma il risultato viene
  letto/scritto su Redis con TTL di 30s prima di rifare la query. Senza
  `REDIS_URL` impostata si comporta come `nocache` (nessun crash, nessuna
  dipendenza esterna richiesta in sviluppo).

Esempio (con `DATABASE_URL` non impostata, quindi contro il catalogo SQLite
locale seedato all'avvio):

```bash
$ curl -w '\ntempo: %{time_total}s\n' http://127.0.0.1:8000/data/nocache/1
{"item_id":1,"sku":"ELEC-001","name":"Mouse wireless","category":"electronics","price_eur":19.99,"stock_quantity":120,"source":"nocache"}
tempo: 0.006s

$ curl -w '\ntempo: %{time_total}s\n' http://127.0.0.1:8000/data/cached/1
{"item_id":1,"sku":"ELEC-001","name":"Mouse wireless","category":"electronics","price_eur":19.99,"stock_quantity":120,"source":"cached"}
tempo: 0.005s

$ curl -w '\ntempo: %{time_total}s\n' http://127.0.0.1:8000/data/cached/1
{"item_id":1,"sku":"ELEC-001","name":"Mouse wireless","category":"electronics","price_eur":19.99,"stock_quantity":120,"source":"cached"}
tempo: 0.002s
```

Con un database reale su Azure la latenza di rete rende la differenza tra
`nocache` e `cached` molto piu' marcata (vedi
[`docs/database-setup.md`](docs/database-setup.md)).

## Test

```bash
pytest
```

## Benchmark e grafici

```bash
python benchmark/run_benchmark.py   # produce un CSV con i tempi di risposta
python charts/generate_charts.py    # legge il CSV e genera i grafici KPI
```

`run_benchmark.py` accetta `--base-url` (default `http://localhost:8000`),
`-n/--requests` (default 50) e `--output` (default `benchmark/results.csv`).
Esegue N richieste su `/data/nocache/{id}` e N su `/data/cached/{id}`,
scrive `benchmark/results.csv` con colonne
`endpoint,item_id,request_index,response_time_ms` e stampa un riepilogo:

```bash
$ python benchmark/run_benchmark.py -n 20
Risultati salvati in benchmark/results.csv
/data/nocache: mean=109.89ms p50=108.59ms p95=135.67ms
/data/cached: mean=7.82ms p50=1.54ms p95=2.07ms
```

(esempio con `REDIS_URL` configurata; senza cache reale `/data/cached` si
comporta come `/data/nocache`, come descritto sopra).

`generate_charts.py` accetta il percorso del CSV come primo argomento
(default `benchmark/results.csv`) e `--output-dir` (default `charts/output`).
Legge il CSV e genera tre grafici PNG, pronti per una presentazione:

- `mean_response_time.png` — tempo medio di risposta, cached vs nocache.
- `percentiles.png` — percentili p50/p95/p99 per i due endpoint.
- `response_time_distribution.png` — distribuzione dei tempi di risposta.

Se il CSV non esiste ancora (nessun benchmark eseguito), lo script stampa un
messaggio invece di terminare con uno stack trace.

## Infrastruttura (Azure)

```bash
cd terraform
export TF_VAR_postgres_admin_password="<scegli-una-password>"
terraform init
terraform apply
```

Crea un resource group, un'istanza Azure Cache for Redis (tier Basic) e un
server Azure Database for PostgreSQL (tier Burstable, il piano base) da
usare per i test contro servizi reali (non solo in locale).

Per passare l'istanza Redis appena creata a `REDIS_URL`:

```bash
export REDIS_URL="rediss://:$(terraform output -raw redis_primary_access_key)@$(terraform output -raw redis_hostname):$(terraform output -raw redis_ssl_port)/0"
```

Lo schema `rediss://` forza la connessione TLS, richiesta dall'istanza Azure
(porta SSL, TLS minimo 1.2). Per popolare il database Postgres con il
catalogo di riferimento e collegare l'app, si veda la guida completa in
[`docs/database-setup.md`](docs/database-setup.md) (query in `db/schema.sql`
e `db/seed.sql`).

Per distruggere le risorse a fine test: `terraform destroy`.

## Screenshot

Esempio di grafico generato da `charts/generate_charts.py` (tempo medio di
risposta, cached vs nocache):

![Tempo medio di risposta: cache vs no cache](docs/img/mean_response_time_example.png)
