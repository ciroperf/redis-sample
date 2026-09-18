-- Schema del catalogo prodotti per Azure Database for PostgreSQL.
-- In locale/nei test lo crea SQLAlchemy (app/db.py); questo file serve
-- per popolare a mano un'istanza Postgres reale (es. con psql).

CREATE TABLE IF NOT EXISTS products (
    id             INTEGER PRIMARY KEY,
    sku            VARCHAR(32) NOT NULL UNIQUE,
    name           VARCHAR(255) NOT NULL,
    category       VARCHAR(64) NOT NULL,
    price_eur      NUMERIC(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL
);
