import pandas as pd
import json
import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 
BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "outputs"
POLICY_DIR = BASE / "data" / "policies"
STATE = BASE / "state"
 
OUT.mkdir(exist_ok=True)
STATE.mkdir(exist_ok=True)
 
# Load and chunk policy documents
documents = []
 
for path in POLICY_DIR.glob("*.txt"):
    text = path.read_text(encoding="utf-8")
    words = text.split()
 
    for i in range(0, len(words), 30):
        chunk = " ".join(words[i:i+40])
        if chunk:
            documents.append({
                "source": path.name,
                "text": chunk
            })
 
if not documents:
    documents = [{"source": "fallback", "text":
        "Completed orders only. Delivery over 45 minutes qualifies "
        "for a full refund. Orders above 1000 rupees require human review."
    }]
 
vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform([d["text"] for d in documents])
 
def retrieve(question):
    q = vectorizer.transform([question])
    scores = cosine_similarity(q, matrix).flatten()
    best = scores.argsort()[-3:][::-1]
    return [
        {"source": documents[i]["source"],
         "text": documents[i]["text"],
         "score": round(float(scores[i]), 3)}
        for i in best
    ]
 
# Load orders
orders = pd.read_csv(BASE / "data" / "clean" / "orders.csv")
orders["status"] = orders["status"].astype(str).str.lower()
orders["delivery_minutes"] = pd.to_numeric(
    orders["delivery_minutes"], errors="coerce"
)
orders["order_amount"] = pd.to_numeric(
    orders["order_amount"], errors="coerce"
)
 
# Load agent scenarios
scenario_file = BASE / "data" / "raw" / "agent_scenarios.csv"
scenarios = pd.read_csv(scenario_file)
 
runs = []
ledger = []
 
for index, row in scenarios.iterrows():
    record = row.to_dict()
    combined = " ".join(str(v) for v in record.values())
 
    match = re.search(r"ORD-\d+", combined)
    order_id = match.group(0) if match else None
 
    result = {
        "scenario": index + 1,
        "order_id": order_id,
        "status": "stopped",
        "action": "No refund issued",
        "reason": "Order not identified",
        "retrieved_policy": retrieve(combined)
    }
 
    if order_id:
        found = orders[orders["order_id"].astype(str) == order_id]
 
        if not found.empty:
            order = found.iloc[-1]
            status = str(order["status"]).lower()
            delivery = order["delivery_minutes"]
            amount = order["order_amount"]
 
            if status != "completed":
                result.update(
                    status="blocked",
                    reason="Only completed orders qualify"
                )
 
            elif pd.isna(delivery) or pd.isna(amount):
                result.update(
                    status="escalated",
                    action="Human review",
                    reason="Required order information is missing"
                )
                ledger.append({
                    "scenario": index + 1,
                    "order_id": order_id,
                    "action": "escalated",
                    "amount": None
                })
 
            elif amount > 1000:
                result.update(
                    status="escalated",
                    action="Human review",
                    reason="Refund exceeds automatic approval limit"
                )
                ledger.append({
                    "scenario": index + 1,
                    "order_id": order_id,
                    "action": "escalated",
                    "amount": float(amount)
                })
 
            elif delivery > 45:
                result.update(
                    status="approved",
                    action="Full refund eligible",
                    reason="Completed order delivered after 45 minutes"
                )
                ledger.append({
                    "scenario": index + 1,
                    "order_id": order_id,
                    "action": "issued_demo",
                    "amount": float(amount)
                })
 
            else:
                result.update(
                    status="rejected",
                    reason="Delivery time is 45 minutes or less"
                )
 
    runs.append(result)
 
# Save agent logs and refund ledger
with open(OUT / "agent_runs.jsonl", "w", encoding="utf-8") as f:
    for item in runs:
        f.write(json.dumps(item) + "\n")
 
with open(OUT / "refund_ledger.jsonl", "w", encoding="utf-8") as f:
    for item in ledger:
        f.write(json.dumps(item) + "\n")
 
# Policy retrieval demonstration
questions = [
    "What is the refund policy?",
    "When is a full refund allowed?",
    "What happens when delivery is delayed?",
    "Which orders qualify for refunds?",
    "When is human approval required?"
]
 
with open(OUT / "policy_answers.jsonl", "w", encoding="utf-8") as f:
    for question in questions:
        answer = {
            "question": question,
            "retrieved_chunks": retrieve(question)
        }
        f.write(json.dumps(answer) + "\n")
 
print("PART D COMPLETED")
print("Policy chunks:", len(documents))
print("Scenarios processed:", len(runs))
print("Refund ledger entries:", len(ledger))
print("Agent logs saved")
print("Policy answers saved")
print("State folder:", STATE)