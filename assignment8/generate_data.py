import os
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)


# HELPER DATA


indian_names = [
    "Priya Sharma", "Rahul Verma", "Ananya Singh", "Vikram Patel",
    "Sneha Gupta", "Arjun Mehta", "Pooja Reddy", "Karan Joshi",
    "Divya Nair", "Rohan Iyer", "Neha Agarwal", "Amit Kumar",
    "Swati Mishra", "Raj Malhotra", "Kavya Pillai", "Siddharth Das",
    "Meera Chopra", "Aditya Shah", "Riya Bose", "Suresh Rao"
]

categories = {
    "Electronics": ["Smartphone", "Laptop", "Tablet", "Headphones",
                    "Smart Watch", "Camera", "Speaker", "Charger"],
    "Clothing": ["T-Shirt", "Jeans", "Saree", "Kurta",
                 "Jacket", "Shoes", "Sandals", "Dress"],
    "Home": ["Pillow", "Bedsheet", "Lamp", "Curtains",
             "Vase", "Mirror", "Clock", "Rug"],
    "Books": ["Python Programming", "Data Science", "Fiction Novel",
              "Self Help", "History Book", "Cookbook", "Comics", "Biography"]
}

regions = ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"]
statuses = ["PLACED", "SHIPPED", "DELIVERED", "CANCELLED", "RETURNED"]
customer_types = ["REGULAR", "PREMIUM", "VIP"]



# PART 1: GENERATE CUSTOMERS (500 rows)


def generate_customers(n=500):
    customer_ids = [f"CUST{str(i).zfill(4)}" for i in range(1, n + 1)]
    names = [random.choice(indian_names) + f" {i}" for i in range(1, n + 1)]

    # Generate emails — 2% invalid
    emails = []
    for i, name in enumerate(names):
        base = name.lower().replace(" ", "").replace("0123456789", "")
        if random.random() < 0.02:
            # Invalid email — missing @ or domain
            if random.random() < 0.5:
                emails.append(f"{base}gmail.com")  # missing @
            else:
                emails.append(f"{base}@")  # missing domain
        else:
            emails.append(f"{base}@gmail.com")

    reg_dates = [
        (datetime(2022, 1, 1) + timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d")
        for _ in range(n)
    ]

    df = pd.DataFrame({
        "customer_id": customer_ids,
        "customer_name": names,
        "email": emails,
        "registration_date": reg_dates,
        "customer_type": [random.choice(customer_types) for _ in range(n)]
    })

    df.to_csv("assignment8/customers.csv", index=False)
    print(f"customers.csv generated — {len(df)} rows")
    return df



# PART 2: GENERATE PRODUCTS (500 rows)


def generate_products(n=500):
    product_ids = [f"PROD{str(i).zfill(4)}" for i in range(1, n + 1)]

    product_names = []
    cats = []
    subcats = []

    for i in range(n):
        cat = random.choice(list(categories.keys()))
        subcat = random.choice(categories[cat])

        # Some product names with extra spaces or mixed case
        if random.random() < 0.1:
            subcat = subcat.upper()  # ALL CAPS
        elif random.random() < 0.1:
            subcat = "  " + subcat + "  "  # extra spaces
        elif random.random() < 0.1:
            subcat = subcat.lower()  # all lowercase

        product_names.append(f"{subcat} {i + 1}")
        cats.append(cat)
        subcats.append(subcat.strip())

    df = pd.DataFrame({
        "product_id": product_ids,
        "product_name": product_names,
        "category": cats,
        "subcategory": subcats,
        "cost_price": [round(random.uniform(50, 5000), 2) for _ in range(n)]
    })

    df.to_csv("assignment8/products.csv", index=False)
    print(f"products.csv generated — {len(df)} rows")
    return df



# PART 3: GENERATE ORDERS (500 rows)


def generate_orders(customers_df, n=500):
    order_ids = [f"ORD{str(i).zfill(5)}" for i in range(1, n + 1)]
    customer_ids = list(customers_df["customer_id"])

    # 5% NULL customer_id
    selected_customers = []
    for _ in range(n):
        if random.random() < 0.05:
            selected_customers.append(None)
        else:
            selected_customers.append(random.choice(customer_ids))

    # Generate dates — some wrong format
    order_dates = []
    for _ in range(n):
        date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 547))
        if random.random() < 0.1:
            # Wrong format DD-MM-YYYY
            order_dates.append(date.strftime("%d-%m-%Y"))
        else:
            # Correct format YYYY-MM-DD HH:MM:SS
            order_dates.append(date.strftime("%Y-%m-%d %H:%M:%S"))

    df = pd.DataFrame({
        "order_id": order_ids,
        "customer_id": selected_customers,
        "order_date": order_dates,
        "status": [random.choice(statuses) for _ in range(n)],
        "region_code": [random.choice(regions) for _ in range(n)]
    })

    df.to_csv("assignment8/orders.csv", index=False)
    print(f"orders.csv generated — {len(df)} rows")
    return df



# PART 4: GENERATE ORDER ITEMS (500 rows)


def generate_order_items(orders_df, products_df, n=500):
    order_ids = list(orders_df["order_id"])
    product_ids = list(products_df["product_id"])

    item_ids = [f"ITEM{str(i).zfill(5)}" for i in range(1, n + 1)]

    quantities = []
    for _ in range(n):
        if random.random() < 0.03:
            # 3% negative quantity (returns)
            quantities.append(random.randint(-10, -1))
        else:
            quantities.append(random.randint(1, 20))

    df = pd.DataFrame({
        "item_id": item_ids,
        "order_id": [random.choice(order_ids) for _ in range(n)],
        "product_id": [random.choice(product_ids) for _ in range(n)],
        "quantity": quantities,
        "unit_price": [round(random.uniform(50, 5000), 2) for _ in range(n)],
        "discount_percent": [round(random.uniform(0, 100), 2) for _ in range(n)]
    })

    df.to_csv("assignment8/order_items.csv", index=False)
    print(f"order_items.csv generated — {len(df)} rows")
    return df



# MAIN — Run all generators

if __name__ == "__main__":
    os.makedirs("assignment8", exist_ok=True)

    print("Generating data...")
    customers_df = generate_customers(500)
    products_df = generate_products(500)
    orders_df = generate_orders(customers_df, 500)
    order_items_df = generate_order_items(orders_df, products_df, 500)
    print("\nAll 4 CSV files generated successfully!")