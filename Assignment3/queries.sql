-- Q1:
SELECT order_id, customer_id, sales
FROM orders
WHERE sales > (SELECT AVG(sales) FROM orders)
ORDER BY sales DESC;

SET SESSION wait_timeout = 600;
SET SESSION interactive_timeout = 600;

-- Q2: Highest sales order for each customer (Subquery)
SELECT o.order_id, o.customer_id, o.sales
FROM orders o
INNER JOIN (
    SELECT customer_id, MAX(sales) AS max_sales
    FROM orders
    GROUP BY customer_id
) AS max_orders
ON o.customer_id = max_orders.customer_id
AND o.sales = max_orders.max_sales
ORDER BY o.sales DESC;

-- Q3: Total sales per customer using CTE
WITH customer_sales AS (
    SELECT customer_id,
    SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT
    c.customer_name,
    cs.customer_id,
    ROUND(cs.total_sales, 2) AS total_sales
FROM customer_sales cs
JOIN customers c ON cs.customer_id = c.customer_id
ORDER BY total_sales DESC;

-- Q4:
WITH customer_sales AS (
    SELECT customer_id,
    SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT
    c.customer_name,
    ROUND(cs.total_sales, 2) AS total_sales
FROM customer_sales cs
JOIN customers c ON cs.customer_id = c.customer_id
WHERE cs.total_sales > (SELECT AVG(total_sales) FROM customer_sales)
ORDER BY total_sales DESC;

-- Q5: Rank all customers based on total sales (Window Function)
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT
    c.customer_name,
    ROUND(cs.total_sales, 2) AS total_sales,
    RANK() OVER (ORDER BY cs.total_sales DESC) AS sales_rank
FROM customer_sales cs
JOIN customers c ON cs.customer_id = c.customer_id;

-- Q6: Assign row numbers to each order within a customer (Window Function + PARTITION BY)
SELECT
    order_id,
    customer_id,
    sales,
    order_date,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY sales DESC
    ) AS row_num
FROM orders
ORDER BY customer_id, row_num;

-- Q7: Top 3 customers based on total sales (Window Function)
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
),
ranked AS (
    SELECT
        c.customer_name,
        ROUND(cs.total_sales, 2) AS total_sales,
        DENSE_RANK() OVER (ORDER BY cs.total_sales DESC) AS sales_rank
    FROM customer_sales cs
    JOIN customers c ON cs.customer_id = c.customer_id
)
SELECT * FROM ranked
WHERE sales_rank <= 3;

-- Step 3: Final Combined Query (JOIN + CTE + Window Function)
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT
    c.customer_name,
    ROUND(cs.total_sales, 2) AS total_sales,
    RANK() OVER (ORDER BY cs.total_sales DESC) AS sales_rank
FROM customer_sales cs
JOIN customers c ON cs.customer_id = c.customer_id
ORDER BY sales_rank;

-- Mini Project
-- Q1: Top 5 customers
WITH customer_sales AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT c.customer_name,
ROUND(cs.total_sales, 2) AS total_sales
FROM customer_sales cs
JOIN customers c ON cs.customer_id = c.customer_id
ORDER BY total_sales DESC
LIMIT 5;

-- Q2: Bottom 5 customers
WITH customer_sales AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT c.customer_name,
    ROUND(cs.total_sales, 2) AS total_sales
FROM customer_sales cs
JOIN customers c ON cs.customer_id = c.customer_id
ORDER BY total_sales ASC
LIMIT 5;

-- Q3: Customers who made only one order
SELECT  c.customer_name,
    COUNT(DISTINCT o.order_id) AS order_count
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_name
HAVING COUNT(DISTINCT o.order_id) = 1;

-- Q4: Customers with above average sales
WITH customer_sales AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT c.customer_name,
 ROUND(cs.total_sales, 2) AS total_sales
FROM customer_sales cs
JOIN customers c ON cs.customer_id = c.customer_id
WHERE cs.total_sales > (SELECT AVG(total_sales) FROM customer_sales)
ORDER BY total_sales DESC;

--  Q5: Highest order value per customer
SELECT
c.customer_name,ROUND(MAX(o.sales), 2) AS highest_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY highest_order_value DESC;