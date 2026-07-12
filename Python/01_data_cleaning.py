import pandas as pd

# Read dataset
df = pd.read_excel(r"C:\Users\eleve\Desktop\prj\Dataset\superstore_sales_dataset.xlsx")

# Check first 5 rows
print(df.head())

# Check data types
print(df.dtypes)

# Convert Order Date
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="mixed",
    dayfirst=False,
    errors="coerce"
)

# Convert Ship Date
df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="mixed",
    dayfirst=False,
    errors="coerce"
)

# Convert into standard format
df["Order Date"] = df["Order Date"].dt.strftime("%Y-%m-%d")
df["Ship Date"] = df["Ship Date"].dt.strftime("%Y-%m-%d")

# Check missing values
print(df.isnull().sum())

# Save cleaned dataset
df.to_csv(r"C:\Users\eleve\Desktop\prj\Dataset\superstore_sales_cleaned.csv", index=False)

print("Cleaned dataset saved successfully!")
