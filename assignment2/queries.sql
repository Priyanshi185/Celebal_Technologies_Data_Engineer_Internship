-- Q1: Display all columns and rows from the customers table
SELECT * FROM customers;

-- Q2: Retrieve only first_name, last_name, and city of all customers
SELECT first_name, last_name, city FROM customers;

-- Q3: List all unique categories from the products table
SELECT DISTINCT category FROM products;

-- Q6: Try inserting a product with unit_price = -50
INSERT INTO products VALUES (209, 'Test Product', 'Electronics', 'TestBrand', -50, 100);

-- Q7: Retrieve all orders with status = 'Delivered'
SELECT * FROM orders
WHERE status = 'Delivered';

-- Q8: Electronics products with unit_price greater than 2000
SELECT * FROM products
WHERE category = 'Electronics' AND unit_price > 2000;

-- Q9: Customers who joined in 2024 AND are from Maharashtra
SELECT * FROM customers
WHERE join_date BETWEEN '2024-01-01' AND '2024-12-31'
AND state = 'Maharashtra';

-- Q10: Orders placed between Aug 10-25 that are NOT cancelled
SELECT * FROM orders
WHERE order_date BETWEEN '2024-08-10' AND '2024-08-25'
AND status != 'Cancelled';

-- Q11: Sample query that benefits from idx_orders_date index
SELECT * FROM orders
WHERE order_date BETWEEN '2024-08-01' AND '2024-08-31';

-- Q12:
SELECT * FROM customers
WHERE join_date BETWEEN '2024-01-01' AND '2024-12-31';

-- Q13: Count total number of orders
SELECT COUNT(*) AS total_orders FROM orders;

-- Q14: Total revenue from Delivered orders
SELECT SUM(total_amount) AS total_revenue
FROM orders
WHERE status = 'Delivered';

-- Q15: Average unit_price of products in each category
SELECT category, AVG(unit_price) AS avg_price
FROM products
GROUP BY category;

-- Q16: Count of orders and total revenue per status, sorted by revenue desc
SELECT status,
COUNT(*) AS order_count,
SUM(total_amount) AS total_revenue
FROM orders
GROUP BY status
ORDER BY total_revenue DESC;

-- Q17: Most expensive and cheapest product in each category
SELECT category,
MAX(unit_price) AS most_expensive,
MIN(unit_price) AS cheapest
FROM products
GROUP BY category;

-- Q18: Categories where average unit_price is greater than 2000
SELECT category, AVG(unit_price) AS avg_price
FROM products
GROUP BY category
HAVING AVG(unit_price) > 2000;

-- Q19: INNER JOIN orders with customers
SELECT o.order_id,
       o.order_date,
       c.first_name,
       c.last_name,
       o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;

-- Q20: LEFT JOIN -- all customers even with no orders
SELECT c.customer_id,c.first_name,c.last_name,o.order_id,o.total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- Q21: 3-table JOIN orders -> order_items -> products
SELECT o.order_id,p.product_name,oi.quantity,oi.unit_price,oi.discount_pct
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id;

-- Q22: LEFT JOIN example
SELECT c.first_name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
-- RIGHT JOIN example
SELECT c.first_name, o.order_id
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;

-- Q23:
INSERT INTO orders VALUES (1011, 999, '2024-09-01', 'Pending', 500.00);

-- Q24
SELECT product_name , unit_price, CASE
WHEN unit_price < 1000 THEN 'Budget'
WHEN unit_price BETWEEN 1000 AND 3000 THEN 'Mid-Range'
WHEN unit_price > 3000 THEN 'Premium'
END AS price_tier
FROM products;

-- Q25: Count Delivered vs Not Delivered in a single row
SELECT SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) AS delivered,
SUM(CASE WHEN status != 'Delivered' THEN 1 ELSE 0 END) AS not_delivered
FROM orders;

-- Q27: Complete BEGIN...COMMIT/ROLLBACK transaction block
BEGIN;
-- Step 1: Insert new order
INSERT INTO orders VALUES (1011, 102, CURDATE(), 'Pending', 1598.00);
-- Step 2: Insert two order items for that order
INSERT INTO order_items VALUES (5016, 1011, 206, 1, 1299.00, 0);
INSERT INTO order_items VALUES (5017, 1011, 208, 1, 599.00, 0);
-- Step 3: Update stock_qty of the purchased products
UPDATE products SET stock_qty = stock_qty - 1 WHERE product_id = 206;
UPDATE products SET stock_qty = stock_qty - 1 WHERE product_id = 208;

-- Step 4: If all steps succeeded, commit
COMMIT;
-- If any step above had failed, you would run this instead:
-- ROLLBACK;
SELECT * FROM orders WHERE order_id = 1011;
