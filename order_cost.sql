SELECT
    o.order_id,
    o.order_number,
    SUM(oi.quantity * si.quantity * mp.price_value) AS total_order_cost
FROM customer_orders o
JOIN customer_order_items oi ON oi.order_id = o.order_id
JOIN specifications s ON s.product_id = oi.product_id
JOIN specification_items si ON si.specification_id = s.specification_id
JOIN material_prices mp ON mp.material_id = si.material_id
GROUP BY o.order_id, o.order_number
ORDER BY o.order_id;