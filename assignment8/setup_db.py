import sqlite3
import pandas as pd
import os


# Connect to SQLite database
conn = sqlite3.connect("assignment8/assignment8/ecommerce.db")
cursor = conn.cursor()
# Load cleaned CSVs
orders = pd.read_csv("assignment8/assignment8/orders_clean.csv")
products = pd.read_csv("assignment8/assignment8/products_clean.csv")
customers = pd.read_csv("assignment8/assignment8/customers.csv")
order_items = pd.read_csv("assignment8/assignment8/order_items.csv")

# Load into SQLite
orders.to_sql("orders", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
customers.to_sql("customers", conn, if_exists="replace", index=False)
order_items.to_sql("order_items", conn, if_exists="replace", index=False)

print("Database created successfully!")
print(f"Orders: {pd.read_sql('SELECT COUNT(*) as count FROM orders', conn).iloc[0,0]} rows")
print(f"Products: {pd.read_sql('SELECT COUNT(*) as count FROM products', conn).iloc[0,0]} rows")
print(f"Customers: {pd.read_sql('SELECT COUNT(*) as count FROM customers', conn).iloc[0,0]} rows")
print(f"Order Items: {pd.read_sql('SELECT COUNT(*) as count FROM order_items', conn).iloc[0,0]} rows")

conn.commit()
conn.close()