# Isola i test su un database SQLite temporaneo, popolato con il catalogo
# di riferimento (app/seed_data.py). E' un DB reale, non una libreria di
# mock: la struttura e i dati sono gli stessi usati contro Azure Postgres.

import os
import tempfile

from app import db

_tmp_dir = tempfile.mkdtemp(prefix="redis-sample-test-db-")
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp_dir}/catalog.db"

db.configure()
db.init_db()
