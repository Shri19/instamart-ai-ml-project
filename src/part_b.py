import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score
 
BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)
 
orders = pd.read_csv(BASE / "data/clean/orders.csv")
orders["order_ts"] = pd.to_datetime(orders["order_ts"], errors="coerce")
orders["order_amount"] = pd.to_numeric(orders["order_amount"], errors="coerce")
orders["status"] = orders["status"].astype(str).str.lower()
 
orders = orders[
    (orders["status"] == "completed") &
    orders["customer_id"].notna() &
    orders["order_ts"].notna()
].copy()
 
as_of = orders["order_ts"].max() + pd.Timedelta(days=1)
 
rfm = orders.groupby("customer_id").agg(
    Recency=("order_ts", lambda x: (as_of - x.max()).days),
    Frequency=("order_id", "nunique"),
    Monetary=("order_amount", "sum")
).reset_index()
 
rfm["Monetary"] = rfm["Monetary"].fillna(0)
 
features = rfm[["Recency", "Frequency", "Monetary"]].copy()
features["Frequency"] = np.log1p(features["Frequency"])
features["Monetary"] = np.log1p(features["Monetary"].clip(lower=0))
 
scaler = StandardScaler()
X = scaler.fit_transform(features)
 
model = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm["Cluster"] = model.fit_predict(X)
 
rfm["Segment"] = rfm["Cluster"].map({
    0: "Segment 1",
    1: "Segment 2",
    2: "Segment 3",
    3: "Segment 4"
})
 
rfm.to_csv(OUT / "customer_segments.csv", index=False)
 
# Lapse classification baseline: no completed order in the
# 90 days before the observation date.
rfm["Lapsed"] = (rfm["Recency"] > 90).astype(int)
 
X_model = features.copy()
y = rfm["Lapsed"]
 
if y.nunique() == 2 and y.value_counts().min() >= 2:
    X_train, X_test, y_train, y_test = train_test_split(
        X_model, y, test_size=0.2, random_state=42, stratify=y
    )
 
    rf = RandomForestClassifier(
        n_estimators=150,
        class_weight="balanced",
        random_state=42
    )
    rf.fit(X_train, y_train)
    predictions = rf.predict(X_test)
 
    print("Lapse model F1:", f1_score(y_test, predictions))
    print(classification_report(y_test, predictions, zero_division=0))
else:
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_model, y)
    print("Only one lapse class found; fitted a baseline model.")
 
joblib.dump(rf, OUT / "lapse_model.joblib")
 
rfm[rfm["Lapsed"] == 1].sort_values(
    "Recency", ascending=False
).to_csv(OUT / "retention_list.csv", index=False)
 
print("\nPART B OUTPUTS CREATED")
print("RFM customers:", len(rfm))
print("Lapsed customers:", int(y.sum()))
print("Cluster counts:")
print(rfm["Cluster"].value_counts().sort_index())
print("Saved customer_segments.csv")
print("Saved lapse_model.joblib")
print("Saved retention_list.csv")