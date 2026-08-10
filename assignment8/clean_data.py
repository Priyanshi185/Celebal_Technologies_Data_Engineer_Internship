import pandas as pd
import re
import os


orders = pd.read_csv("assignment8/orders.csv")
products = pd.read_csv("assignment8/products.csv")
customers = pd.read_csv("assignment8/customers.csv")
order_items = pd.read_csv("assignment8/order_items.csv")



def clean_orders(df):
    print("=== clean_orders() ===")
    print(f"Before: {len(df)} rows")
    print(f"NULL customer_ids: {df['customer_id'].isnull().sum()}")

    # Fix date format — convert DD-MM-YYYY to YYYY-MM-DD HH:MM:SS
    def fix_date(date_str):
        if pd.isna(date_str):
            return None
        date_str = str(date_str)
        # Check if wrong format DD-MM-YYYY
        if re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
            try:
                return pd.to_datetime(date_str, format="%d-%m-%Y").strftime("%Y-%m-%d %H:%M:%S")
            except:
                return None
        return date_str

    df['order_date'] = df['order_date'].apply(fix_date)

    # Handle NULL customer_ids — fill with 'UNKNOWN'
    df['customer_id'] = df['customer_id'].fillna('UNKNOWN')

    print(f"After fixing dates and NULL customer_ids:")
    print(f"NULL customer_ids remaining: {df['customer_id'].isnull().sum()}")
    print(f"After: {len(df)} rows\n")
    return df



def clean_products(df):
    print("=== clean_products() ===")
    print(f"Before cleaning product names:")
    print(df['product_name'].head(5).tolist())

    # Trim spaces and convert to title case
    df['product_name'] = df['product_name'].str.strip().str.title()
    df['category'] = df['category'].str.strip().str.title()
    df['subcategory'] = df['subcategory'].str.strip().str.title()

    print(f"After cleaning product names:")
    print(df['product_name'].head(5).tolist())
    print()
    return df


def validate_emails(df):
    print("=== validate_emails() ===")

    # Valid email pattern
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    invalid = df[~df['email'].str.match(email_pattern, na=False)]
    invalid_customer_ids = invalid['customer_id'].tolist()

    print(f"Total invalid emails found: {len(invalid_customer_ids)}")
    print(f"Invalid customer_ids: {invalid_customer_ids[:10]}")
    print()
    return invalid_customer_ids



def check_referential_integrity(orders_df, order_items_df):
    print("=== check_referential_integrity() ===")

    valid_order_ids = set(orders_df['order_id'])
    invalid_items = order_items_df[~order_items_df['order_id'].isin(valid_order_ids)]

    print(f"Total order_items: {len(order_items_df)}")
    print(f"Order_items with non-existent order_id: {len(invalid_items)}")
    if len(invalid_items) > 0:
        print(invalid_items.head())
    print()
    return invalid_items



if __name__ == "__main__":
    # Clean data
    orders_clean = clean_orders(orders)
    products_clean = clean_products(products)
    invalid_emails = validate_emails(customers)
    invalid_items = check_referential_integrity(orders, order_items)

    # Save cleaned CSVs
    orders_clean.to_csv("assignment8/orders_clean.csv", index=False)
    products_clean.to_csv("assignment8/products_clean.csv", index=False)

    # Generate issues report
    report = f"""
=== DATA CLEANING REPORT ===

1. Orders Cleaned:
   - NULL customer_ids filled with UNKNOWN
   - Wrong date formats fixed to YYYY-MM-DD HH:MM:SS

2. Products Cleaned:
   - Product names trimmed and converted to Title Case

3. Invalid Emails Found: {len(invalid_emails)}
   - Customer IDs: {invalid_emails[:5]}

4. Referential Integrity Issues: {len(invalid_items)}
   - Order items referencing non-existent orders

============================
"""
    print(report)

    # Save report
    with open("assignment8/cleaning_report.txt", "w") as f:
        f.write(report)

    print("Cleaned CSVs and report saved successfully!")