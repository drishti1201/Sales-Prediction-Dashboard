import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
np.random.seed(42)

# ==========================
# Load Dataset
# ==========================

df = pd.read_excel(r"C:\Users\eleve\Desktop\prj\Dataset\superstore_sales_cleaned.xlsx")

# ==========================
# Date Features
# ==========================

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month
df["Order Day"] = df["Order Date"].dt.day

df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# ==========================
# Drop unwanted columns
# ==========================

df.drop([
    "Row ID",
    "Order ID",
    "Customer ID",
    "Customer Name",
    "Product ID",
    "Order Date",
    "Ship Date"
], axis=1, inplace=True)

# ==========================
# Label Encoding
# ==========================

encoders = {}

categorical_columns = [
    "Ship Mode",
    "Segment",
    "Country",
    "City",
    "State",
    "Region",
    "Category",
    "Sub-Category",
    "Product Name"
]

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# ==========================
# Features & Target
# ==========================

features = [
    "Ship Mode",
    "Segment",
    "Country",
    "City",
    "State",
    "Postal Code",
    "Region",
    "Category",
    "Sub-Category",
    "Product Name",
    "Quantity",
    "Discount",
    "Order Year",
    "Order Month",
    "Order Day",
    "Shipping Days"
]

X = df[features]
y = df["Sales"]


# ==========================
# Train Test Split
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    "XGBoost": XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)
}

results = []

best_model = None
best_r2 = -999

for name, model in models.items():

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    r2 = r2_score(y_test, pred)
    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))

    results.append({
        "Model": name,
        "R2": round(r2,3),
        "MAE": round(mae,2),
        "RMSE": round(rmse,2)
    })

    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        best_prediction = pred

comparison = pd.DataFrame(results)

print(comparison)
best_name = comparison.loc[comparison["R2"].idxmax(), "Model"]

print("\nBest Model :", best_name)
print("Best R² :", round(best_r2, 3))

comparison.to_excel("model_comparison.xlsx", index=False)
comparison.to_csv("model_comparison.csv", index=False)


# ==========================
# Save Model
# ==========================

best_name = comparison.loc[comparison["R2"].idxmax(),"Model"]

metrics = {
    "Model": best_name,
    "R2": round(best_r2,3),
    "MAE": round(mean_absolute_error(y_test,best_prediction),2),
    "RMSE": round(np.sqrt(mean_squared_error(y_test,best_prediction)),2)
}

# ==========================
# Feature Importance
# ==========================
if hasattr(best_model, "feature_importances_"):

    importance = pd.DataFrame({
        "Feature": X.columns,
        "Importance": best_model.feature_importances_
    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    importance.to_csv("feature_importance.csv", index=False)

joblib.dump(best_model, "sales_prediction_model.pkl")
joblib.dump(encoders, "label_encoders.pkl")
joblib.dump(metrics, "metrics.pkl")
comparison.to_csv("model_comparison.csv", index=False)

print("\nModel Saved Successfully.")






