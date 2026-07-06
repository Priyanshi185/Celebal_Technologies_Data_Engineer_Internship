CREATE DATABASE superstore_db;
USE superstore_db;
-- Checking number of rows
SELECT COUNT(*) AS total_rows FROM superstore_raw;

-- Checking if same Customer ID has multiple segments or regions
SELECT `Customer ID`, COUNT(DISTINCT `Segment`), COUNT(DISTINCT `Region`)
FROM superstore_raw
GROUP BY `Customer ID`
HAVING COUNT(DISTINCT `Segment`) > 1 OR COUNT(DISTINCT `Region`) > 1;

-- Creating customers table
CREATE TABLE customers AS
SELECT DISTINCT
    `Customer ID`   AS customer_id,
    `Customer Name` AS customer_name,
    `Segment`       AS segment
FROM superstore_raw;

SELECT COUNT(*) AS total_customers FROM customers;

-- Creating table products
CREATE TABLE products AS
SELECT DISTINCT
    `Product ID`   AS product_id,
    `Product Name` AS product_name,
    `Category`     AS category,
    `Sub-Category` AS sub_category
FROM superstore_raw;

SELECT COUNT(*) AS total_products FROM products;

-- Creating table orders
CREATE TABLE orders AS
SELECT DISTINCT
    `Order ID`    AS order_id,
    `Customer ID` AS customer_id,
    `Order Date`  AS order_date,
    `Ship Date`   AS ship_date,
    `Ship Mode`   AS ship_mode,
    `Product ID`  AS product_id,
    `Sales`       AS sales,
    `Quantity`    AS quantity,
    `Discount`    AS discount,
    `Profit`      AS profit
FROM superstore_raw;

SELECT COUNT(*) AS total_orders FROM orders;