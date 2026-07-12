import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\eleve\Desktop\prj\Dataset\superstore_sales_cleaned.csv")

#Dataset Information
print(df.info())

#Shape
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

#Column Names
print(df.columns)

#Missing Values
print(df.isnull().sum())

#Duplicate Rows
print(df.duplicated().sum())

#Summary Statistics
print(df.describe())

#Check Data Types
print(df.dtypes)

# Convert Date Column
df["Order Date"] = pd.to_datetime(df["Order Date"])

#----------------------------------------------------------------------------------------------------
#Visualization
#Monthly Sales Trend
#It shows- A line chart showing how sales change month by month.
monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
      .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(12,6))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.grid(True)

plt.show()

#Sales by Category
category_sales = (
    df.groupby("Category")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

plt.figure(figsize=(8,5))
plt.bar(category_sales.index, category_sales.values)

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.show()

#Profit by Category
category_profit = (
    df.groupby("Category")["Profit"]
      .sum()
      .sort_values(ascending=False)
)

plt.figure(figsize=(8,5))
plt.bar(category_profit.index, category_profit.values)

plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit")

plt.show()

#Sales by Region
region_sales = (
    df.groupby("Region")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

plt.figure(figsize=(8,5))
plt.bar(region_sales.index, region_sales.values)

plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")

plt.show()

#Top 10 Customers
top_customers = (
    df.groupby("Customer Name")["Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

plt.figure(figsize=(12,5))
plt.bar(top_customers.index, top_customers.values)

plt.xticks(rotation=60)
plt.title("Top 10 Customers by Sales")
plt.xlabel("Customer")
plt.ylabel("Sales")

plt.show()

#Top 10 Products
top_products = (
    df.groupby("Product Name")["Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

plt.figure(figsize=(12,5))
plt.bar(top_products.index, top_products.values)

plt.xticks(rotation=90)
plt.title("Top 10 Products")
plt.xlabel("Product")
plt.ylabel("Sales")

plt.show()

#-----------------------------------------------------------------------------------------------------
#Business KPIs & Insights
print("\nBUSINESS KPIs\n")
#KPI 1: Total Sales
print("Total Sales: ₹{:,.2f}".format(df["Sales"].sum()))

#KPI 2: Total Profit
print("Total Profit: ₹{:,.2f}".format(df["Profit"].sum()))

#KPI 3: Total Orders
print("Total Orders:", df["Order ID"].nunique())

#KPI 4: Total Customers
print("Total Customers:", df["Customer ID"].nunique())

#KPI 5: Average Order Value
avg_order = df["Sales"].sum() / df["Order ID"].nunique()

print("Average Order Value: ₹{:.2f}".format(avg_order))

#KPI 6: Profit Margin
profit_margin = (df["Profit"].sum()/df["Sales"].sum())*100

print("Profit Margin: {:.2f}%".format(profit_margin))

#------------------------------------------------------------------------------------------------
#Business Insights
print("\nBUSINESS INSIGHTS\n")

#Highest Sales Category
top_category = df.groupby("Category")["Sales"].sum().idxmax()

print("Highest Sales Category :", top_category)

#Highest Profit Region
top_region = df.groupby("Region")["Profit"].sum().idxmax()

print("Highest Profit Region :", top_region)

#Best Customer
best_customer = df.groupby("Customer Name")["Sales"].sum().idxmax()

print("Best Customer :", best_customer)

#Most Sold Product
top_product = df.groupby("Product Name")["Quantity"].sum().idxmax()

print("Most Sold Product :", top_product)

#Most Profitable Product
profit_product = df.groupby("Product Name")["Profit"].sum().idxmax()

print("Most Profitable Product :", profit_product)

#----------------------------------------------------------------------------------------------------
#Correlation Analysis
corr = df[["Sales","Profit","Quantity","Discount"]].corr()

print(corr)

#-----------------------------------------------------------------------------------------------------
#Correlation Heatmap
plt.figure(figsize=(6,5))
sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")
plt.show()

#------------------------------------------------------------------------------------------------------
#Save Business Summary
summary = pd.DataFrame({
    "Metric":[
        "Total Sales",
        "Total Profit",
        "Total Orders",
        "Total Customers",
        "Average Order Value",
        "Profit Margin"
    ],
    "Value":[
        df["Sales"].sum(),
        df["Profit"].sum(),
        df["Order ID"].nunique(),
        df["Customer ID"].nunique(),
        avg_order,
        profit_margin
    ]
})

summary.to_csv("business_summary.csv",index=False)

print("Business Summary Saved")
