-- Расчет полной стоимости заказа покупателя по стоимости материалов

WITH latest_material_prices AS (
    SELECT DISTINCT ON (material_id)
        material_id,
        price_value,
        date_from
    FROM material_prices
    ORDER BY material_id, date_from DESC
)
SELECT
    co.order_id,
    co.order_number,
    co.order_date,
    cp.name AS customer_name,
    SUM(coi.quantity * si.quantity * lmp.price_value) AS material_total_cost
FROM customer_orders co
JOIN counterparties cp
    ON cp.counterparty_id = co.counterparty_id
JOIN customer_order_items coi
    ON coi.order_id = co.order_id
JOIN products p
    ON p.product_id = coi.product_id
JOIN specifications s
    ON s.product_id = p.product_id
JOIN specification_items si
    ON si.specification_id = s.specification_id
JOIN latest_material_prices lmp
    ON lmp.material_id = si.material_id
GROUP BY
    co.order_id,
    co.order_number,
    co.order_date,
    cp.name
ORDER BY
    co.order_id;
