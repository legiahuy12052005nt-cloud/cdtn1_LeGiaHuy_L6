
-- Mekong Mobile - SQLite Data Warehouse
-- Star Schema: 1 Fact + 3 Dimensions

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date TEXT NOT NULL,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE dim_product (
    product_key INTEGER PRIMARY KEY,
    product_id TEXT NOT NULL UNIQUE,
    product_name TEXT,
    category TEXT,
    brand TEXT
);

CREATE TABLE dim_store (
    store_key INTEGER PRIMARY KEY,
    store_code TEXT NOT NULL UNIQUE,
    store_name TEXT,
    city TEXT,
    district TEXT
);

CREATE TABLE fact_sales (
    sales_key INTEGER PRIMARY KEY,
    source_line_id TEXT NOT NULL UNIQUE,
    order_id TEXT NOT NULL,

    date_key INTEGER,
    product_key INTEGER NOT NULL,
    store_key INTEGER NOT NULL,

    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price INTEGER NOT NULL CHECK (unit_price >= 0),
    reported_sales_amount INTEGER NOT NULL CHECK (reported_sales_amount >= 0),
    calculated_sales_amount INTEGER NOT NULL,
    difference_amount INTEGER NOT NULL,

    reconciliation_status TEXT NOT NULL
        CHECK (reconciliation_status IN ('MATCH', 'MISMATCH')),

    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
);
