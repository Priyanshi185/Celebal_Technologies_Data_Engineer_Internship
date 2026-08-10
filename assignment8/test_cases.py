import sqlite3
import pandas as pd

conn = sqlite3.connect("assignment8/assignment8/ecommerce.db")


# TEST CASE 1: order_items has order_id not in orders


def test_invalid_order_id():
    print(" Test 1: Invalid Order ID in order_items ")

    cursor = conn.cursor()

    # Insert an order_item with non-existent order_id
    cursor.execute("""
        INSERT INTO order_items VALUES 
        ('ITEM99999', 'ORD99999', 'PROD0001', 5, 100.0, 10.0)
    """)
    conn.commit()

    # Check referential integrity
    result = pd.read_sql("""
        SELECT oi.item_id, oi.order_id
        FROM order_items oi
        LEFT JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_id IS NULL
    """, conn)

    if len(result) > 0:
        print(f"FAIL: Found {len(result)} order_items with invalid order_id!")
        print(result)
    else:
        print("PASS: All order_items have valid order_ids")

    # Cleanup
    cursor.execute("DELETE FROM order_items WHERE item_id = 'ITEM99999'")
    conn.commit()
    print()


# TEST CASE 2: discount_percent > 100


def test_invalid_discount():
    print("Test 2: discount_percent > 100 ")

    cursor = conn.cursor()

    # Insert order_item with discount > 100
    cursor.execute("""
        INSERT INTO order_items VALUES 
        ('ITEM88888', 'ORD00001', 'PROD0001', 5, 100.0, 150.0)
    """)
    conn.commit()

    # Check for invalid discounts
    result = pd.read_sql("""
        SELECT item_id, discount_percent
        FROM order_items
        WHERE discount_percent > 100
    """, conn)

    if len(result) > 0:
        print(f" FAIL: Found {len(result)} items with discount > 100!")
        print(result)
    else:
        print(" PASS: All discounts are valid (0-100)")

    # Cleanup
    cursor.execute("DELETE FROM order_items WHERE item_id = 'ITEM88888'")
    conn.commit()
    print()


# TEST CASE 3: quantity = 0


def test_zero_quantity():
    print("Test 3: Quantity = 0 ")

    cursor = conn.cursor()

    # Insert order_item with quantity = 0
    cursor.execute("""
        INSERT INTO order_items VALUES 
        ('ITEM77777', 'ORD00001', 'PROD0001', 0, 100.0, 10.0)
    """)
    conn.commit()

    # Check for zero quantity
    result = pd.read_sql("""
        SELECT item_id, quantity
        FROM order_items
        WHERE quantity = 0
    """, conn)

    if len(result) > 0:
        print(f" FAIL: Found {len(result)} items with quantity = 0!")
        print(result)
    else:
        print(" PASS: No items with zero quantity")

    # Cleanup
    cursor.execute("DELETE FROM order_items WHERE item_id = 'ITEM77777'")
    conn.commit()
    print()



# TEST CASE 4: order_date is in the future


def test_future_order_date():
    print("Test 4: order_date in the Future ")

    cursor = conn.cursor()

    # Insert order with future date
    cursor.execute("""
        INSERT INTO orders VALUES 
        ('ORD99998', 'CUST0001', '2099-01-01 00:00:00', 'PLACED', 'NORTH')
    """)
    conn.commit()

    # Check for future dates
    result = pd.read_sql("""
        SELECT order_id, order_date
        FROM orders
        WHERE order_date > datetime('now')
    """, conn)

    if len(result) > 0:
        print(f"FAIL: Found {len(result)} orders with future dates!")
        print(result)
    else:
        print(" PASS: No orders with future dates")

    # Cleanup
    cursor.execute("DELETE FROM orders WHERE order_id = 'ORD99998'")
    conn.commit()
    print()


if __name__ == "__main__":
    print("Running Edge Case Tests...\n")
    test_invalid_order_id()
    test_invalid_discount()
    test_zero_quantity()
    test_future_order_date()
    print("All tests completed!")
    conn.close()