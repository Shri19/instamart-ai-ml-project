import pandas as pd
from pathlib import Path
 
BASE = Path(__file__).resolve().parent.parent
 
df = pd.read_csv(BASE / "data" / "raw" / "orders.csv")
 
print("Raw rows:", len(df))
 
df = df.drop_duplicates()
df["order_ts"] = pd.to_datetime(df["order_ts"], errors="coerce")
df = df.sort_values("order_ts")
df = df.drop_duplicates(subset="order_id", keep="last")
 
df["order_amount"] = pd.to_numeric(
    df["order_amount"], errors="coerce"
)
 
print("\nRows after deduplication:", len(df))
print("\nOrders by status:")
print(df["status"].value_counts())
 
print("\nRevenue by status:")
print(
    df.groupby("status")["order_amount"]
    .agg(["count", "sum"])
)
 
print("\nMissing amounts:", df["order_amount"].isna().sum())