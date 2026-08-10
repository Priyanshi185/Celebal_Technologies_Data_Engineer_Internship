# Assignment 8 — E-Commerce Order Analytics System

## Tools Used
Python, Pandas, SQLite3

## Project Structure
- generate_data.py  → Part 1: Generate 4 CSV files with dirty data
- clean_data.py     → Part 2: Data cleaning functions
- setup_db.py       → Load cleaned data into SQLite database
- queries.py        → Part 3: 16 SQL queries
- report_tool.py    → Part 4: Command-line reporting tool
- test_cases.py     → Part 5: Edge case test functions

## Dataset
4 CSV files (500 rows each):
- orders.csv        → Orders with intentional nulls and wrong dates
- order_items.csv   → Items with negative quantities (returns)
- products.csv      → Products with mixed case and extra spaces
- customers.csv     → Customers with invalid emails

## How to Run
1. python assignment8/generate_data.py
2. python assignment8/clean_data.py
3. python assignment8/setup_db.py
4. python assignment8/queries.py
5. python assignment8/report_tool.py
6. python assignment8/test_cases.py

## Intentional Data Issues
- 5% orders have NULL customer_id
- 3% order_items have negative quantity
- 10% orders have wrong date format (DD-MM-YYYY)
- 10% product names have extra spaces or mixed case
- 2% emails are invalid