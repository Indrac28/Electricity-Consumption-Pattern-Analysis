import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Create database and table
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Drop table if already exists
cursor.execute("DROP TABLE IF EXISTS sales")

# Create the sales table
cursor.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    product TEXT,
    quantity INTEGER,
    price REAL,
    region TEXT,
    customer_type TEXT,
    sale_date TEXT
)
""")

# Step 2: Insert sample data
sample_data = [
    ("Laptop", 3, 50000, "North", "Retail", "2025-06-01"),
    ("Phone", 5, 20000, "South", "Wholesale", "2025-06-01"),
    ("Tablet", 2, 30000, "North", "Retail", "2025-06-02"),
    ("Laptop", 1, 50000, "East", "Retail", "2025-06-02"),
    ("Phone", 7, 20000, "West", "Wholesale", "2025-06-03"),
    ("Tablet", 4, 30000, "South", "Retail", "2025-06-03"),
    ("Laptop", 2, 50000, "South", "Wholesale", "2025-06-04"),
    ("Phone", 6, 20000, "North", "Retail", "2025-06-04"),
    ("Tablet", 3, 30000, "East", "Retail", "2025-06-05"),
    ("Laptop", 1, 50000, "West", "Retail", "2025-06-05")
]

cursor.executemany("INSERT INTO sales (product, quantity, price, region, customer_type, sale_date) VALUES (?, ?, ?, ?, ?, ?)", sample_data)
conn.commit()

# Step 3: Run SQL queries and create DataFrames

# 1. Revenue by Product
query1 = "SELECT product, SUM(quantity * price) AS revenue FROM sales GROUP BY product"
df1 = pd.read_sql_query(query1, conn)

# 2. Revenue by Region
query2 = "SELECT region, SUM(quantity * price) AS revenue FROM sales GROUP BY region"
df2 = pd.read_sql_query(query2, conn)

# 3. Revenue by Customer Type
query3 = "SELECT customer_type, SUM(quantity * price) AS revenue FROM sales GROUP BY customer_type"
df3 = pd.read_sql_query(query3, conn)

# 4. Daily Sales Trend
query4 = "SELECT sale_date, SUM(quantity * price) AS daily_sales FROM sales GROUP BY sale_date ORDER BY sale_date"
df4 = pd.read_sql_query(query4, conn)

conn.close()

# Step 4: Visualizations

# 1. Revenue by Product
df1.plot(kind='bar', x='product', y='revenue', legend=False)
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("revenue_by_product.png")
plt.show()

# 2. Revenue by Region
df2.set_index('region').plot(kind='pie', y='revenue', autopct='%1.1f%%', legend=False)
plt.title("Region-wise Revenue")
plt.ylabel("")
plt.tight_layout()
plt.savefig("revenue_by_region.png")
plt.show()

# 3. Revenue by Customer Type
df3.plot(kind='bar', x='customer_type', y='revenue', color='green', legend=False)
plt.title("Customer Type Revenue")
plt.xlabel("Customer Type")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("revenue_by_customer_type.png")
plt.show()

# 4. Daily Sales Trend
df4.plot(kind='line', x='sale_date', y='daily_sales', marker='o', color='purple', legend=False)
plt.title("Daily Sales Trend")
plt.xlabel("Sale Date")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("daily_sales_trend.png")
plt.show()
