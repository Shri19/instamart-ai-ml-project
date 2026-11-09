import sqlite3
from pathlib import Path
 
BASE = Path(__file__).resolve().parent.parent
 
db_path = BASE / "data" / "instamart.db"
sql_path = BASE / "sql" / "queries.sql"
 
conn = sqlite3.connect(db_path)
 
with open(sql_path, "r", encoding="utf-8") as file:
    sql_text = file.read()
 
queries = [
    q.strip()
    for q in sql_text.split(";")
    if q.strip()
]
 
for i, query in enumerate(queries, start=1):
    print(f"\n{'='*40}")
    print(f"QUERY Q{i}")
    print("="*40)
 
    cursor = conn.execute(query)
    rows = cursor.fetchall()
 
    print("Columns:", [col[0] for col in cursor.description])
 
    for row in rows[:10]:
        print(row)
 
    print("Rows returned:", len(rows))
 
conn.close()
print("\nAll SQL queries executed successfully!")