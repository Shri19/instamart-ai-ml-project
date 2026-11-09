import pandas as pd
from pathlib import Path
 
BASE = Path(__file__).resolve().parent.parent
 
raw = BASE / "data" / "raw" / "orders.csv"
out = BASE / "data" / "clean" / "orders.csv"
 
out.parent.mkdir(parents=True, exist_ok=True)
 
df = pd.read_csv(raw)
 
print("Original rows:", len(df))
 
# Remove exact duplicate records
df = df.drop_duplicates()
 
# Convert timestamps
df["order_ts"] = pd.to_datetime(df["order_ts"], errors="coerce")
 
# Sort by timestamp and retain latest status per order
df = df.sort_values("order_ts")
df = df.drop_duplicates(subset="order_id", keep="last")
 
# Convert order amount to numeric
df["order_amount"] = pd.to_numeric(
    df["order_amount"], errors="coerce"
)
 
# Replace negative delivery times with missing
df["delivery_minutes"] = pd.to_numeric(
    df["delivery_minutes"], errors="coerce"
)
df.loc[df["delivery_minutes"] < 0, "delivery_minutes"] = pd.NA
 
# Save cleaned data
df.to_csv(out, index=False)
 
print("\nORDER CLEANING COMPLETED")
print("Final rows:", len(df))
print("Unique order IDs:", df["order_id"].nunique())
print("Missing order amounts:", df["order_amount"].isna().sum())
print("Missing delivery times:", df["delivery_minutes"].isna().sum())
print("Saved:", out)
