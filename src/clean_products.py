import pandas as pd
from pathlib import Path
 
BASE = Path(__file__).resolve().parent.parent
raw = BASE / "data" / "raw" / "products.csv"
out = BASE / "data" / "clean" / "products.csv"
 
out.parent.mkdir(parents=True, exist_ok=True)
 
df = pd.read_csv(raw)
df = df.drop_duplicates()
df["product_id"] = df["product_id"].astype(str).str.strip()
df["product_name"] = df["product_name"].astype(str).str.strip()
df["category"] = df["category"].astype(str).str.strip()
df["price_inr"] = pd.to_numeric(df["price_inr"], errors="coerce")
 
df.to_csv(out, index=False)
 
print("Products cleaning completed")
print("Final rows:", len(df))
print("Missing values:", df.isna().sum().sum())
print("Saved:", out)
