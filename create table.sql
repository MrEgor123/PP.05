DROP TABLE IF EXISTS production_batch_items CASCADE;
DROP TABLE IF EXISTS production_batches CASCADE;
DROP TABLE IF EXISTS customer_order_items CASCADE;
DROP TABLE IF EXISTS customer_orders CASCADE;
DROP TABLE IF EXISTS specification_items CASCADE;
DROP TABLE IF EXISTS specifications CASCADE;
DROP TABLE IF EXISTS product_prices CASCADE;
DROP TABLE IF EXISTS material_prices CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS materials CASCADE;
DROP TABLE IF EXISTS counterparties CASCADE;
DROP TABLE IF EXISTS units CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    login VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    login_attempts INTEGER NOT NULL DEFAULT 0,
    is_blocked BOOLEAN NOT NULL DEFAULT FALSE,
    role_id INTEGER NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50) NOT NULL,
    CONSTRAINT users_role_fk FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

CREATE TABLE units (
    unit_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    short_name VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE counterparties (
    counterparty_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    inn VARCHAR(12),
    address VARCHAR(255),
    phone VARCHAR(50),
    is_buyer BOOLEAN NOT NULL DEFAULT FALSE,
    is_supplier BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE materials (
    material_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    unit_id INTEGER NOT NULL,
    CONSTRAINT materials_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES units(unit_id)
);

CREATE TABLE material_prices (
    material_price_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    material_id INTEGER NOT NULL,
    price_value NUMERIC(14,2) NOT NULL CHECK (price_value >= 0),
    date_from DATE NOT NULL,
    CONSTRAINT material_prices_material_id_fkey FOREIGN KEY (material_id) REFERENCES materials(material_id)
);

CREATE TABLE products (
    product_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    sku VARCHAR(100),
    unit_id INTEGER NOT NULL,
    CONSTRAINT products_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES units(unit_id)
);

CREATE TABLE product_prices (
    product_price_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INTEGER NOT NULL,
    price_value NUMERIC(10,2) NOT NULL CHECK (price_value >= 0),
    date_from DATE NOT NULL,
    CONSTRAINT product_prices_product_id_fkey FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE specifications (
    specification_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT specifications_product_id_fkey FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE specification_items (
    specification_item_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    material_id INTEGER NOT NULL,
    specification_id INTEGER NOT NULL,
    quantity NUMERIC(10,2) NOT NULL CHECK (quantity > 0),
    CONSTRAINT specification_items_material_id_fkey FOREIGN KEY (material_id) REFERENCES materials(material_id),
    CONSTRAINT specification_items_specification_id_fkey FOREIGN KEY (specification_id) REFERENCES specifications(specification_id)
);

CREATE TABLE customer_orders (
    order_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_number VARCHAR(100) NOT NULL UNIQUE,
    order_date DATE NOT NULL,
    counterparty_id INTEGER NOT NULL,
    CONSTRAINT customer_orders_counterparty_id_fkey FOREIGN KEY (counterparty_id) REFERENCES counterparties(counterparty_id)
);

CREATE TABLE customer_order_items (
    order_item_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity NUMERIC(10,2) NOT NULL CHECK (quantity > 0),
    price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    CONSTRAINT customer_order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES customer_orders(order_id),
    CONSTRAINT customer_order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE production_batches (
    production_batch_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    batch_number VARCHAR(100) NOT NULL UNIQUE,
    batch_date DATE NOT NULL
);

CREATE TABLE production_batch_items (
    production_batch_item_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    production_batch_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity NUMERIC(10,2) NOT NULL CHECK (quantity > 0),
    CONSTRAINT production_batch_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT production_batch_items_production_batch_id_fkey FOREIGN KEY (production_batch_id) REFERENCES production_batches(production_batch_id)
);