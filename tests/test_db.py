# Test sulla struttura dati del catalogo: DB reale (SQLite, seedato con
# tests/conftest.py) e dati fissi da app/seed_data.py, nessun mock.

from app import db
from app.seed_data import PRODUCTS


def test_catalog_is_seeded_with_reference_dataset():
    with db.session_scope() as session:
        assert session.query(db.Product).count() == len(PRODUCTS)


def test_get_product_matches_seed_data():
    expected = PRODUCTS[0]

    product = db.get_product(expected["id"])

    assert product == {
        "item_id": expected["id"],
        "sku": expected["sku"],
        "name": expected["name"],
        "category": expected["category"],
        "price_eur": expected["price_eur"],
        "stock_quantity": expected["stock_quantity"],
    }


def test_get_product_returns_none_when_missing():
    assert db.get_product(999999) is None


def test_electronics_catalog_value_metric():
    # Metrica su dati reali: valore di magazzino (prezzo * stock) per
    # categoria, calcolata sia dal DB sia dal dataset di riferimento.
    with db.session_scope() as session:
        rows = session.query(db.Product).filter_by(category="electronics").all()
        db_value = sum(float(row.price_eur) * row.stock_quantity for row in rows)

    expected_value = sum(
        p["price_eur"] * p["stock_quantity"]
        for p in PRODUCTS
        if p["category"] == "electronics"
    )

    assert round(db_value, 2) == round(expected_value, 2)
