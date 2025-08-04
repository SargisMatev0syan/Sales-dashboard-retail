import pandas as pd
import sqlite3

df = pd.read_csv("Sample - Superstore.csv", encoding='ISO-8859-1')

print("Initial shape:", df.shape)
print(df.head())

# --- Cleaning Steps ---

# Converting date columns to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')


#cheking  missing values
print("\nMissing values per column:\n", df.isnull().sum())

# Drop rows with missing critical values (optional)
df.dropna(subset=['Order Date', 'Sales', 'Product Name'], inplace=True)

# Convert data types (if needed)
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')

# Create new columns (e.g., month/year for analysis)
df['Order Month'] = df['Order Date'].dt.to_period('M')
df['Order Year'] = df['Order Date'].dt.year

# Final check
print("\nCleaned data sample:\n", df.head())
print("Cleaned shape:", df.shape)

# Save to new file
df.to_csv("cleaned_sales_data.csv", index=False)
print("\n✅ Cleaned data saved to 'cleaned_sales_data.csv'")


#-------------------------------------------------------------
df = pd.read_csv("cleaned_sales_data.csv")

# Connect to SQLite DB (creates file if it doesn't exist)
conn = sqlite3.connect("sales_dashboard.db")

# Load DataFrame into a new table
df.to_sql("sales_data", conn, if_exists="replace", index=False)

print("✅ Data loaded into SQLite as 'sales_data' table.")

# Sample query
result = pd.read_sql_query("""
SELECT Category, SUM(Sales) AS total_sales
FROM sales_data
GROUP BY Category
ORDER BY total_sales DESC
""", conn)

print("\n📊 Total Sales by Category:\n", result)