-- Dati di riferimento per il catalogo prodotti (caso d'uso e-commerce).
-- Generato da db/generate_seed_sql.py a partire da app/seed_data.py: non
-- modificare a mano, rilanciare lo script dopo aver aggiornato PRODUCTS.
-- Uso: psql "$DATABASE_URL" -f db/schema.sql -f db/seed.sql


INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (1, 'ELEC-001', 'Mouse wireless', 'electronics', 19.99, 120)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (2, 'ELEC-002', 'Tastiera meccanica', 'electronics', 74.9, 45)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (3, 'ELEC-003', 'Monitor 27" 4K', 'electronics', 329.0, 18)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (4, 'ELEC-004', 'Webcam HD', 'electronics', 39.5, 60)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (5, 'ELEC-005', 'Cuffie bluetooth', 'electronics', 89.99, 33)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (6, 'ELEC-006', 'Hub USB-C 7 porte', 'electronics', 29.0, 80)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (7, 'HOME-001', 'Lampada da scrivania LED', 'home', 24.99, 95)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (8, 'HOME-002', 'Set 4 tazze in ceramica', 'home', 15.5, 150)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (9, 'HOME-003', 'Tappeto soggiorno 160x230', 'home', 129.0, 12)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (10, 'HOME-004', 'Organizer da cassetto', 'home', 9.9, 200)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (11, 'HOME-005', 'Diffusore aromi', 'home', 34.9, 40)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (12, 'HOME-006', 'Coperta in pile 200x220', 'home', 27.0, 70)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (13, 'SPRT-001', 'Tappetino yoga', 'sports', 22.9, 85)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (14, 'SPRT-002', 'Bottiglia termica 750ml', 'sports', 18.0, 110)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (15, 'SPRT-003', 'Corda per saltare', 'sports', 12.5, 130)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (16, 'SPRT-004', 'Guanti da palestra', 'sports', 16.9, 55)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (17, 'SPRT-005', 'Zaino running 10L', 'sports', 44.0, 28)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (18, 'SPRT-006', 'Fascia elastica fitness', 'sports', 9.99, 160)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (19, 'GROC-001', 'Caffe'' in grani 1kg', 'grocery', 14.9, 300)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (20, 'GROC-002', 'Olio extravergine 1L', 'grocery', 11.5, 220)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (21, 'GROC-003', 'Pasta artigianale 500g', 'grocery', 3.2, 400)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (22, 'GROC-004', 'Miele biologico 400g', 'grocery', 8.9, 90)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (23, 'GROC-005', 'Tisana relax 20 filtri', 'grocery', 5.5, 180)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;

INSERT INTO products (id, sku, name, category, price_eur, stock_quantity) VALUES (24, 'GROC-006', 'Cioccolato fondente 100g', 'grocery', 3.9, 260)
ON CONFLICT (id) DO UPDATE SET sku = EXCLUDED.sku, name = EXCLUDED.name, category = EXCLUDED.category, price_eur = EXCLUDED.price_eur, stock_quantity = EXCLUDED.stock_quantity;
