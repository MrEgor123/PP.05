-- Физическая модель БД по ER-диаграмме

CREATE TABLE units (
    unit_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL UNIQUE,
    short_name varchar(20) NOT NULL UNIQUE
);

CREATE TABLE counterparties (
    counterparty_id integer PRIMARY KEY,
    name varchar(255) NOT NULL,
    inn varchar(12),
    address varchar(255),
    phone varchar(50),
    is_buyer boolean NOT NULL DEFAULT false,
    is_supplier boolean NOT NULL DEFAULT false
);

CREATE TABLE products (
    product_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(255) NOT NULL UNIQUE,
    sku varchar(100),
    unit_id integer NOT NULL REFERENCES units(unit_id)
);

CREATE TABLE materials (
    material_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(255) NOT NULL UNIQUE,
    unit_id integer NOT NULL REFERENCES units(unit_id)
);

CREATE TABLE material_prices (
    material_price_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    material_id integer NOT NULL REFERENCES materials(material_id),
    price_value decimal(10, 2) NOT NULL CHECK (price_value >= 0),
    date_from date NOT NULL
);

CREATE TABLE product_prices (
    product_price_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id integer NOT NULL REFERENCES products(product_id),
    price_value decimal(10, 2) NOT NULL CHECK (price_value >= 0),
    date_from date NOT NULL
);

CREATE TABLE specifications (
    specification_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id integer NOT NULL REFERENCES products(product_id),
    name varchar(100) NOT NULL
);

CREATE TABLE specification_items (
    specification_item_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    material_id integer NOT NULL REFERENCES materials(material_id),
    specification_id integer NOT NULL REFERENCES specifications(specification_id),
    quantity decimal(10, 2) NOT NULL CHECK (quantity > 0)
);

CREATE TABLE customer_orders (
    order_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_number varchar(100) NOT NULL UNIQUE,
    order_date date NOT NULL,
    counterparty_id integer NOT NULL REFERENCES counterparties(counterparty_id)
);

CREATE TABLE customer_order_items (
    order_item_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id integer NOT NULL REFERENCES customer_orders(order_id),
    product_id integer NOT NULL REFERENCES products(product_id),
    quantity decimal(10, 2) NOT NULL CHECK (quantity > 0),
    price decimal(10, 2) NOT NULL CHECK (price >= 0)
);

CREATE TABLE production_batches (
    production_batch_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    batch_number varchar(100) NOT NULL UNIQUE,
    batch_date date NOT NULL
);

CREATE TABLE production_batch_items (
    production_batch_item_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    production_batch_id integer NOT NULL REFERENCES production_batches(production_batch_id),
    product_id integer NOT NULL REFERENCES products(product_id),
    quantity decimal(10, 2) NOT NULL CHECK (quantity > 0)
);
