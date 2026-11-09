import pandas as pd
import re
from pathlib import Path
 
BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)
 
df = pd.read_csv(BASE / "data/raw/tickets.csv")
 
def redact(text):
    text = str(text)
    text = re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', '[EMAIL]', text)
    text = re.sub(r'\b\d{10}\b', '[PHONE]', text)
    text = re.sub(r'ORD-\d+', '[ORDER_ID]', text)
    return text
 
def classify(text):
    t = str(text).lower()
 
    rules = {
        "fraud": ["fraud", "unauthorized", "scam", "transaction"],
        "billing": ["invoice", "amount", "bill", "payment", "charged"],
        "delivery": ["delivery", "late", "delay", "missing", "rider"],
        "refund": ["refund", "return", "money back"],
        "account": ["account", "login", "password", "profile"]
    }
 
    for category, keywords in rules.items():
        if any(word in t for word in keywords):
            return category
 
    return "other"
 
def priority(category, text):
    t = str(text).lower()
    if category == "fraud" or "unauthorized" in t:
        return "High"
    if category == "delivery" or category == "refund":
        return "Medium"
    return "Low"
 
df["redacted_text"] = df["text"].apply(redact)
df["predicted_category"] = df["redacted_text"].apply(classify)
df["priority"] = df.apply(
    lambda r: priority(r["predicted_category"], r["redacted_text"]),
    axis=1
)
 
df["correct"] = (
    df["predicted_category"].str.lower() ==
    df["true_category"].astype(str).str.lower()
)
 
df.to_csv(OUT / "triage_results.csv", index=False)
 
# Budget demonstration: process only the first 20 tickets
budget = df.head(20).copy()
budget["processing_mode"] = "Budget demo"
budget["estimated_cost"] = 0.0
budget.to_csv(OUT / "triage_budget_demo.csv", index=False)
 
print("PART C COMPLETED")
print("Total tickets:", len(df))
print("Classification accuracy:", round(df["correct"].mean() * 100, 2), "%")
print("Priority distribution:")
print(df["priority"].value_counts())
print("PII redaction completed")
print("Saved triage_results.csv")
print("Saved triage_budget_demo.csv")