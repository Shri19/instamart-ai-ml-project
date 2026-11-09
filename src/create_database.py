import pandas as pd
import sqlite3
from pathlib import Path
 
BASE = Path(__file__).resolve().parent.parent
clean = BASE / "data" / "clean"
db_path = BASE / "data" / "instamart.db"
 
conn = sqlite3.connect(db_path)
 
for name in ["customers", "orders", "products"]:
    df = pd.read_csv(clean / f"{name}.csv")
    df.to_sql(name, conn, if_exists="replace", index=False)
    print(f"{name}: {len(df)} records stored")
 
print("\nDatabase created:", db_path)
 
conn.close()
