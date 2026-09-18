# Livello di accesso al catalogo prodotti: la sorgente dati "vera" che le
# API di app/main.py mettono in cache. Senza DATABASE_URL usa un file
# SQLite locale (nessuna dipendenza esterna richiesta per lo sviluppo);
# in produzione DATABASE_URL punta a un'istanza Azure Database for
# PostgreSQL (vedi terraform/database.tf e docs/database-setup.md).

import os
from contextlib import contextmanager

from sqlalchemy import Column, Integer, Numeric, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.seed_data import PRODUCTS

Base = declarative_base()

DEFAULT_DATABASE_URL = "sqlite:///./catalog.db"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    sku = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price_eur = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)


_engine = None
_SessionLocal = None


def configure(database_url: str | None = None) -> None:
    """(Ri)crea l'engine puntato da DATABASE_URL. Usata all'avvio dell'app
    e nei test per isolare ogni run su un database dedicato."""
    global _engine, _SessionLocal
    url = database_url or os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    _engine = create_engine(url, connect_args=connect_args)
    _SessionLocal = sessionmaker(bind=_engine)


@contextmanager
def session_scope():
    if _SessionLocal is None:
        configure()
    session = _SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    """Crea la tabella se manca e popola il catalogo di riferimento se e'
    vuota (idempotente: sicura da richiamare ad ogni avvio)."""
    if _engine is None:
        configure()
    Base.metadata.create_all(_engine)
    with session_scope() as session:
        if session.query(Product).count() == 0:
            session.bulk_insert_mappings(Product, PRODUCTS)
            session.commit()


def get_product(item_id: int) -> dict | None:
    with session_scope() as session:
        product = session.get(Product, item_id)
        if product is None:
            return None
        return {
            "item_id": product.id,
            "sku": product.sku,
            "name": product.name,
            "category": product.category,
            "price_eur": float(product.price_eur),
            "stock_quantity": product.stock_quantity,
        }
