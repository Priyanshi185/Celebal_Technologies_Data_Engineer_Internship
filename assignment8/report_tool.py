import sqlite3
from datetime import datetime, timedelta


def get_date_range(report_type, start_date):

    start = datetime.strptime(start_date, "%Y-%m-%d")

    if report_type == "daily":
        end = start + timedelta(days=1)
        prev_start = start - timedelta(days=1)
        prev_end = start
    elif report_type == "weekly":
        end = start + timedelta(weeks=1)
        prev_start = start - timedelta(weeks=1)
        prev_end = start
    elif report_type == "monthly":
        # Add one month
        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1)
        else:
            end = start.replace(month=start.month + 1)
        # Previous month
        if start.month == 1:
            prev_start = start.replace(year=start.year - 1, month=12)
        else:
            prev_start = start.replace(month=start.month - 1)
        prev_end = start

    return (start.strftime("%Y-%m-%d"),
            end.strftime("%Y-%m-%d"),
            prev_start.strftime("%Y-%m-%d"),
            prev_end.strftime("%Y-%m-%d"))


def generate_report(report_type, start_date):
    conn = sqlite3.connect("assignment8/assignment8/ecommerce.db")
    cursor = conn.cursor()

    start, end, prev_start, prev_end = get_date_range(report_type, start_date)

    print("\n" + "=" * 50)
    print(f"  {report_type.upper()} REPORT")
    print(f"  Period: {start} to {end}")
    print("=" * 50)

    # Current period stats
    cursor.execute("""
        SELECT COUNT(DISTINCT o.order_id) AS total_orders,
               ROUND(SUM(oi.quantity * oi.unit_price * 
                   (1 - oi.discount_percent/100)), 2) AS revenue,
               COUNT(DISTINCT o.customer_id) AS unique_customers
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_date >= ? AND o.order_date < ?
        AND oi.quantity > 0
    """, (start, end))

    current = cursor.fetchone()
    total_orders = current[0] or 0
    revenue = current[1] or 0
    unique_customers = current[2] or 0

    print(f"\n SUMMARY:")
    print(f"   Total Orders    : {total_orders}")
    print(f"   Total Revenue   : ₹{revenue:,.2f}")
    print(f"   Unique Customers: {unique_customers}")

    # Top 3 products
    cursor.execute("""
        SELECT p.product_name,
               ROUND(SUM(oi.quantity * oi.unit_price * 
                   (1 - oi.discount_percent/100)), 2) AS revenue
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE o.order_date >= ? AND o.order_date < ?
        AND oi.quantity > 0
        GROUP BY p.product_name
        ORDER BY revenue DESC
        LIMIT 3
    """, (start, end))

    top_products = cursor.fetchall()
    print(f"\n TOP 3 PRODUCTS:")
    if top_products:
        for i, (name, rev) in enumerate(top_products, 1):
            print(f"   {i}. {name[:30]} — ₹{rev:,.2f}")
    else:
        print("   No data found for this period")

    # Previous period stats for comparison
    cursor.execute("""
        SELECT ROUND(SUM(oi.quantity * oi.unit_price * 
                   (1 - oi.discount_percent/100)), 2) AS revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_date >= ? AND o.order_date < ?
        AND oi.quantity > 0
    """, (prev_start, prev_end))

    prev = cursor.fetchone()
    prev_revenue = prev[0] or 0

    print(f"\nCOMPARISON WITH PREVIOUS {report_type.upper()}:")
    print(f"   Previous Revenue: ₹{prev_revenue:,.2f}")
    if prev_revenue > 0:
        change = ((revenue - prev_revenue) / prev_revenue) * 100
        arrow = "↑" if change >= 0 else "↓"
        print(f"   Change          : {arrow} {abs(change):.2f}%")
    else:
        print("   Change          : No previous data")

    print("\n" + "=" * 50)
    conn.close()



if __name__ == "__main__":
    print("\n E-Commerce Order Analytics Report Tool")
    print("-" * 50)

    # Get report type
    while True:
        report_type = input("\nEnter report type (daily/weekly/monthly): ").strip().lower()
        if report_type in ["daily", "weekly", "monthly"]:
            break
        print("Invalid! Please enter daily, weekly or monthly")

    # Get start date
    while True:
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD")

    generate_report(report_type, start_date)