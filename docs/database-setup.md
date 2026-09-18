# Collegare Redis a un database reale

Questo documento spiega come passare dal setup locale (SQLite +
`REDIS_URL` non impostata) a un caso reale: Azure Database for PostgreSQL
come sorgente dati e Azure Cache for Redis davanti.

## Caso d'uso: catalogo prodotti e-commerce

La sorgente dati e' un catalogo prodotti (`products`: `id`, `sku`, `name`,
`category`, `price_eur`, `stock_quantity`), popolato con un dataset fisso
di 24 prodotti in `app/seed_data.py`. E' il caso classico di caching: molte
letture (pagina prodotto, listino) contro pochi scritture, dati che
cambiano poco nel breve periodo — esattamente dove Redis rende di piu'.

Lo stesso dataset e' la fonte di verita' sia per i test (`tests/test_db.py`,
`tests/conftest.py`, contro un SQLite temporaneo) sia per l'istanza Azure
reale (`db/seed.sql`, generato da `db/generate_seed_sql.py`): niente dati
finti generati a runtime, sempre lo stesso catalogo riproducibile.

## 1. Provisionare le risorse Azure

```bash
cd terraform
export TF_VAR_postgres_admin_password="<scegli-una-password>"
terraform init
terraform apply
```

Crea, nello stesso resource group: un'istanza Azure Cache for Redis (tier
Basic) e un server Azure Database for PostgreSQL (tier Burstable
`B_Standard_B1ms`, il piano base) con un database `catalog`.

## 2. Popolare il catalogo

Da locale, con `psql` installato e la propria IP aggiunta alle regole del
firewall del server Postgres (`azurerm_postgresql_flexible_server_firewall_rule`
in `terraform/database.tf`, non incluso di default per non esporre il
server oltre ai servizi Azure):

```bash
export DATABASE_URL="postgresql://$(terraform -chdir=terraform output -raw postgres_admin_username):${TF_VAR_postgres_admin_password}@$(terraform -chdir=terraform output -raw postgres_fqdn):5432/$(terraform -chdir=terraform output -raw postgres_database_name)?sslmode=require"

psql "$DATABASE_URL" -f db/schema.sql -f db/seed.sql
```

`db/seed.sql` usa `INSERT ... ON CONFLICT DO UPDATE`: e' idempotente, si
puo' rilanciare per riportare il catalogo allo stato di riferimento.

## 3. Collegare l'app

```bash
export DATABASE_URL="postgresql+psycopg2://$(terraform -chdir=terraform output -raw postgres_admin_username):${TF_VAR_postgres_admin_password}@$(terraform -chdir=terraform output -raw postgres_fqdn):5432/$(terraform -chdir=terraform output -raw postgres_database_name)?sslmode=require"
export REDIS_URL="rediss://:$(terraform -chdir=terraform output -raw redis_primary_access_key)@$(terraform -chdir=terraform output -raw redis_hostname):$(terraform -chdir=terraform output -raw redis_ssl_port)/0"

uvicorn app.main:app --reload
```

A questo punto `/data/nocache/{id}` legge dal Postgres reale (la latenza e'
quella vera della rete + della query, non piu' simulata) e
`/data/cached/{id}` la mette in cache su Redis con TTL di 30s: il
`benchmark/run_benchmark.py` misura numeri reali, non piu' una latenza
finta.

Per distruggere le risorse a fine test: `terraform -chdir=terraform destroy`.

## Nota su test e CI

I test (`pytest`) non richiedono le risorse Azure: usano lo stesso schema
e lo stesso dataset (`app/seed_data.py`) contro un file SQLite temporaneo
creato da `tests/conftest.py`. E' un database relazionale reale, non una
libreria di mock: verifica la struttura dei dati e alcune metriche
calcolate sul catalogo (`tests/test_db.py`), non solo l'endpoint HTTP.
