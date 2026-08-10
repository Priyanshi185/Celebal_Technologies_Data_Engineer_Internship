import sqlite3
import pandas as pd

conn = sqlite3.connect("assignment8/assignment8/ecommerce.db")


# Query 1: Total revenue per category
print("Q1: Total Revenue per Category ")
q1 = pd.read_sql("""
    SELECT p.category,
           ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) AS total_revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    WHERE oi.quantity > 0
    GROUP BY p.category
    ORDER BY total_revenue DESC
""", conn)
print(q1)
print()

# Query 2: Top 10 customers by total order value
print(" Q2: Top 10 Customers by Total Order Value ")
q2 = pd.read_sql("""
    SELECT c.customer_name,
           c.customer_id,
           ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) AS total_value
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE oi.quantity > 0
    GROUP BY c.customer_id, c.customer_name
    ORDER BY total_value DESC
    LIMIT 10
""", conn)
print(q2)
print()

# Query 3: Month-wise order count for last 12 months
print("Q3: Month-wise Order Count ")
q3 = pd.read_sql("""
    SELECT strftime('%Y-%m', order_date) AS month,
           COUNT(*) AS order_count
    FROM orders
    WHERE order_date >= date('now', '-12 months')
    GROUP BY month
    ORDER BY month
""", conn)
print(q3)
print()


# INTERMEDIATE QUERIES
# Query 4: Customers who placed orders but never had any item delivered
print("Q4: Customers with No Delivered Items ")
q4 = pd.read_sql("""
    SELECT DISTINCT c.customer_id, c.customer_name
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.customer_id NOT IN (
        SELECT DISTINCT o2.customer_id
        FROM orders o2
        WHERE o2.status = 'DELIVERED'
        AND o2.customer_id IS NOT NULL
    )
    LIMIT 10
""", conn)
print(q4)
print()

# Query 5: Products with more returns than purchases
print(" Q5: Products with More Returns than Purchases ")
q5 = pd.read_sql("""
    SELECT p.product_name,
           p.category,
           SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END) AS purchases,
           SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) AS returns
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category
    HAVING returns > purchases
    ORDER BY returns DESC
    LIMIT 10
""", conn)
print(q5)
print()

# Query 6: Return rate per category
print(" Q6: Return Rate per Category ")
q6 = pd.read_sql("""
    SELECT p.category,
           SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END) AS total_purchases,
           SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) AS total_returns,
           ROUND(
               SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) * 100.0 /
               NULLIF(SUM(ABS(oi.quantity)), 0), 2
           ) AS return_rate_percent
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.category
    ORDER BY return_rate_percent DESC
""", conn)
print(q6)
print()

# ADVANCED QUERIES

# Query 7: Running Total of Revenue per Region
print("Q7: Running Total of Revenue per Region ")
q7 = pd.read_sql("""
    WITH daily_revenue AS (
        SELECT o.region_code,
               DATE(o.order_date) AS order_date,
               ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) AS daily_revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE oi.quantity > 0
        GROUP BY o.region_code, DATE(o.order_date)
    )
    SELECT region_code,
           order_date,
           daily_revenue,
           ROUND(SUM(daily_revenue) OVER (
               PARTITION BY region_code
               ORDER BY order_date
           ), 2) AS running_total
    FROM daily_revenue
    ORDER BY region_code, order_date
    LIMIT 15
""", conn)
print(q7)
print()

# Query 8: Ranking products by revenue using DENSE_RANK
print("Q8: Product Ranking by Revenue per Category ")
q8 = pd.read_sql("""
    WITH product_revenue AS (
        SELECT p.category,
               p.product_name,
               ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) AS total_revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.quantity > 0
        GROUP BY p.category, p.product_name
    )
    SELECT category,
           product_name,
           total_revenue,
           DENSE_RANK() OVER (
               PARTITION BY category
               ORDER BY total_revenue DESC
           ) AS rank_in_category
    FROM product_revenue
    ORDER BY category, rank_in_category
    LIMIT 15
""", conn)
print(q8)
print()

# Query 9: LAG/LEAD Analysis — days between consecutive orders
print(" Q9: Days Between Consecutive Orders ")
q9 = pd.read_sql("""
    WITH order_gaps AS (
        SELECT customer_id,
               order_date,
               LAG(order_date) OVER (
                   PARTITION BY customer_id
                   ORDER BY order_date
               ) AS previous_order_date,
               JULIANDAY(order_date) - JULIANDAY(LAG(order_date) OVER (
                   PARTITION BY customer_id
                   ORDER BY order_date
               )) AS days_gap
        FROM orders
        WHERE customer_id != 'UNKNOWN'
    )
    SELECT customer_id,
           order_date,
           previous_order_date,
           ROUND(days_gap, 0) AS days_gap,
           CASE WHEN AVG(days_gap) OVER (PARTITION BY customer_id) > 30
                THEN 'At Risk'
                ELSE 'Active'
           END AS customer_status
    FROM order_gaps
    WHERE previous_order_date IS NOT NULL
    ORDER BY customer_id, order_date
    LIMIT 15
""", conn)
print(q9)
print()

# Query 10: CTE with Multiple Levels
print(" Q10: Customer Revenue Categories per Month ")
q10 = pd.read_sql("""
    WITH monthly_revenue AS (
        SELECT o.customer_id,
               strftime('%Y-%m', o.order_date) AS month,
               ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) AS revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE oi.quantity > 0 AND o.customer_id != 'UNKNOWN'
        GROUP BY o.customer_id, month
    ),
    categorized AS (
        SELECT month,
               customer_id,
               revenue,
               CASE WHEN revenue > 10000 THEN 'High'
                    WHEN revenue BETWEEN 5000 AND 10000 THEN 'Medium'
                    ELSE 'Low'
               END AS revenue_category
        FROM monthly_revenue
    )
    SELECT month,
           revenue_category,
           COUNT(*) AS customer_count
    FROM categorized
    GROUP BY month, revenue_category
    ORDER BY month, revenue_category
    LIMIT 15
""", conn)
print(q10)
print()

# Query 11: NTILE for Segmentation
print("Q11: Customer Quartile Segmentation ")
q11 = pd.read_sql("""
    WITH customer_value AS (
        SELECT o.customer_id,
               ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) AS total_value
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE oi.quantity > 0 AND o.customer_id != 'UNKNOWN'
        GROUP BY o.customer_id
    )
    SELECT customer_id,
           total_value,
           NTILE(4) OVER (ORDER BY total_value DESC) AS quartile,
           CASE NTILE(4) OVER (ORDER BY total_value DESC)
                WHEN 1 THEN 'Platinum'
                WHEN 2 THEN 'Gold'
                WHEN 3 THEN 'Silver'
                WHEN 4 THEN 'Bronze'
           END AS quartile_label
    FROM customer_value
    ORDER BY total_value DESC
    LIMIT 15
""", conn)
print(q11)
print()

# Query 12: Year-over-Year Comparison
print(" Q12: Year-over-Year Revenue Comparison ")
q12 = pd.read_sql("""
    WITH monthly AS (
        SELECT strftime('%Y', o.order_date) AS year,
               strftime('%m', o.order_date) AS month,
               ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) AS revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE oi.quantity > 0
        GROUP BY year, month
    )
    SELECT curr.year,
           curr.month,
           curr.revenue,
           prev.revenue AS prev_year_revenue,
           CASE WHEN prev.revenue IS NULL THEN NULL
                ELSE ROUND((curr.revenue - prev.revenue) * 100.0 / prev.revenue, 2)
           END AS yoy_growth_percent
    FROM monthly curr
    LEFT JOIN monthly prev
        ON curr.month = prev.month
        AND CAST(curr.year AS INT) = CAST(prev.year AS INT) + 1
    ORDER BY curr.year, curr.month
    LIMIT 15
""", conn)
print(q12)
print()

# Query 13: First/Last Value Analysis
print("Q13: First and Last Category per Customer ")
q13 = pd.read_sql("""
    WITH customer_categories AS (
        SELECT o.customer_id,
               p.category,
               o.order_date,
               FIRST_VALUE(p.category) OVER (
                   PARTITION BY o.customer_id
                   ORDER BY o.order_date
               ) AS first_category,
               LAST_VALUE(p.category) OVER (
                   PARTITION BY o.customer_id
                   ORDER BY o.order_date
                   ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
               ) AS last_category
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE o.customer_id != 'UNKNOWN'
    )
    SELECT DISTINCT customer_id,
           first_category,
           last_category,
           CASE WHEN first_category != last_category THEN 'Yes' ELSE 'No' END AS category_shift
    FROM customer_categories
    LIMIT 15
""", conn)
print(q13)
print()

# Query 14: Cumulative Distribution
print("Q14: Cumulative Revenue Distribution")
q14 = pd.read_sql("""
    WITH customer_revenue AS (
        SELECT o.customer_id,
               ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100)), 2) AS revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE oi.quantity > 0 AND o.customer_id != 'UNKNOWN'
        GROUP BY o.customer_id
    )
    SELECT customer_id,
           revenue,
           ROUND(SUM(revenue) OVER (ORDER BY revenue DESC), 2) AS cumulative_revenue,
           ROUND(SUM(revenue) OVER (ORDER BY revenue DESC) * 100.0 /
                 SUM(revenue) OVER (), 2) AS cumulative_percent
    FROM customer_revenue
    ORDER BY revenue DESC
    LIMIT 15
""", conn)
print(q14)
print()

# Query 15: Cohort Analysis
print("Q15: Cohort Analysis")
q15 = pd.read_sql("""
    WITH cohorts AS (
        SELECT c.customer_id,
               strftime('%Y-%m', c.registration_date) AS cohort_month
        FROM customers c
    ),
    orders_with_cohort AS (
        SELECT o.customer_id,
               co.cohort_month,
               strftime('%Y-%m', o.order_date) AS order_month,
               (strftime('%Y', o.order_date) - strftime('%Y', co.cohort_month)) * 12 +
               (strftime('%m', o.order_date) - strftime('%m', co.cohort_month)) AS months_since_registration
        FROM orders o
        JOIN cohorts co ON o.customer_id = co.customer_id
        WHERE o.customer_id != 'UNKNOWN'
    )
    SELECT cohort_month,
           months_since_registration,
           COUNT(DISTINCT customer_id) AS customers
    FROM orders_with_cohort
    WHERE months_since_registration BETWEEN 0 AND 3
    GROUP BY cohort_month, months_since_registration
    ORDER BY cohort_month, months_since_registration
    LIMIT 15
""", conn)
print(q15)
print()

# Query 16: Self-Join — Products bought together
print(" Q16: Products Frequently Bought Together ")
q16 = pd.read_sql("""
    SELECT a.product_id AS product_a,
           b.product_id AS product_b,
           COUNT(*) AS times_bought_together
    FROM order_items a
    JOIN order_items b
        ON a.order_id = b.order_id
        AND a.product_id < b.product_id
    GROUP BY a.product_id, b.product_id
    ORDER BY times_bought_together DESC
    LIMIT 10
""", conn)
print(q16)
print()

conn.close()
print("All queries executed successfully!")