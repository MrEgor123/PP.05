-- Импорт данных из файла Заказчики.json

CREATE TEMP TABLE import_counterparties_raw (
    line text
);

\copy import_counterparties_raw(line) FROM '/Users/mvideomvideo/Desktop/ПП.05 Задание №1/doc/Заказчики.json' WITH (FORMAT csv, DELIMITER E'\x1f', QUOTE E'\x1e', ESCAPE E'\x1d')

WITH src AS (
    SELECT string_agg(line, E'\n')::jsonb AS doc
    FROM import_counterparties_raw
)
INSERT INTO counterparties (
    counterparty_id,
    name,
    inn,
    address,
    phone,
    is_buyer,
    is_supplier
)
SELECT
    (x.id)::integer,
    x.name,
    NULLIF(x.inn, ''),
    x.addres,
    x.phone,
    COALESCE(x.buyer, false),
    COALESCE(x.salesman, false)
FROM src,
LATERAL jsonb_to_recordset(src.doc) AS x(
    id text,
    name text,
    inn text,
    addres text,
    phone text,
    salesman boolean,
    buyer boolean
);
