SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS branches (
    branch_id VARCHAR(10) PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    location_type VARCHAR(100) NOT NULL,
    cuisine_focus VARCHAR(150) NOT NULL,
    demand_pattern TEXT NOT NULL,
    staffing_model TEXT NOT NULL,
    inventory_model TEXT NOT NULL,
    preparation_model TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id VARCHAR(20) PRIMARY KEY,
    branch_id VARCHAR(10) NOT NULL REFERENCES branches(branch_id),
    sale_date DATE NOT NULL,
    meal_period VARCHAR(30) NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    quantity_sold INTEGER NOT NULL CHECK (quantity_sold >= 0)
);

CREATE TABLE IF NOT EXISTS preparations (
    preparation_id VARCHAR(20) PRIMARY KEY,
    branch_id VARCHAR(10) NOT NULL REFERENCES branches(branch_id),
    prep_date DATE NOT NULL,
    meal_period VARCHAR(30) NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    quantity_prepared INTEGER NOT NULL CHECK (quantity_prepared >= 0),
    quantity_sold INTEGER NOT NULL CHECK (quantity_sold >= 0),
    remaining_quantity INTEGER NOT NULL CHECK (remaining_quantity >= 0)
);

CREATE TABLE IF NOT EXISTS waste_records (
    waste_id VARCHAR(20) PRIMARY KEY,
    branch_id VARCHAR(10) NOT NULL REFERENCES branches(branch_id),
    waste_date DATE NOT NULL,
    meal_period VARCHAR(30) NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    waste_quantity_kg NUMERIC(10, 2) NOT NULL CHECK (waste_quantity_kg >= 0),
    waste_reason VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id VARCHAR(20) PRIMARY KEY,
    branch_id VARCHAR(10) NOT NULL REFERENCES branches(branch_id),
    inventory_date DATE NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    opening_stock_kg NUMERIC(10, 2) NOT NULL CHECK (opening_stock_kg >= 0),
    purchased_stock_kg NUMERIC(10, 2) NOT NULL CHECK (purchased_stock_kg >= 0),
    closing_stock_kg NUMERIC(10, 2) NOT NULL CHECK (closing_stock_kg >= 0),
    spoilage_kg NUMERIC(10, 2) NOT NULL CHECK (spoilage_kg >= 0)
);

CREATE TABLE IF NOT EXISTS purchases (
    purchase_id VARCHAR(20) PRIMARY KEY,
    branch_id VARCHAR(10) NOT NULL REFERENCES branches(branch_id),
    purchase_date DATE NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    quantity_kg NUMERIC(10, 2) NOT NULL CHECK (quantity_kg >= 0),
    supplier_category VARCHAR(100) NOT NULL,
    unit_cost NUMERIC(10, 2) NOT NULL CHECK (unit_cost >= 0)
);
"""