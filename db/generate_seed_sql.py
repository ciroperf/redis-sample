# Genera db/seed.sql a partire da app/seed_data.PRODUCTS, cosi' il
# catalogo usato dai test e quello caricato su Azure Postgres restano la
# stessa fonte di verita'. Da rilanciare se PRODUCTS cambia:
#   python db/generate_seed_sql.py

from pathlib import Path

from app.seed_data import PRODUCTS

HEADER = """-- Dati di riferimento per il catalogo prodotti (caso d'uso e-commerce).
-- Generato da db/generate_seed_sql.py a partire da app/seed_data.py: non
-- modificare a mano, rilanciare lo script dopo aver aggiornato PRODUCTS.
-- Uso: psql "$DATABASE_URL" -f db/schema.sql -f db/seed.sql

"""


def _sql_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def main() -> None:
    lines = [HEADER]
    for product in PRODUCTS:
        lines.append(
            "INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) "
            f"VALUES ({product['id']}, {_sql_literal(product['sku'])}, "
            f"{_sql_literal(product['name'])}, {_sql_literal(product['category'])}, "
            f"{product['price_eur']}, {product['stock_quantity']})\n"
            "ON CONFLICT (id) DO UPDATE SET "
            "sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, "
            "price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;\n"
        )

    output_path = Path(__file__).parent / "seed.sql"
    output_path.write_text("\n".join(lines))
    print(f"Scritto {output_path} con {len(PRODUCTS)} prodotti.")


if __name__ == "__main__":
    main()
