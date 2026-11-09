# Masai Instamart Customer Intelligence & Support Copilot
 
## Project Overview
This project develops a local customer intelligence and support copilot using synthetic Instamart data.
 
## Environment Setup
1. Create a virtual environment:
   python -m venv venv
 
2. Activate it:
   .\venv\Scripts\Activate.ps1
 
3. Install dependencies:
   pip install -r requirements.txt
 
4. Generate data:
   python generate_data.py
 
## Run the Project
1. Clean customer and order data using the cleaning scripts.
2. Create the SQLite database:
   python src/create_database.py
3. Execute SQL queries:
   python src/run_queries.py
4. Run customer segmentation:
   python src/part_b.py
5. Run ticket triage:
   python src/part_c.py
6. Run policy retrieval and refund demonstration:
   python src/part_d.py
 
## Part A - Data Foundation
Cleaned customer, order and product datasets, SQLite storage and seven SQL queries.
 
## Part B - Customer Intelligence
RFM analysis, K-means segmentation, lapse classification and retention list.
 
## Part C - Support Ticket Triage
Ticket categorization, priority assignment and PII redaction.
 
## Part D - Policy RAG and Refund Agent
TF-IDF policy retrieval, scenario processing and simulated refund decisions.
 
## Limitations
The current implementation uses baseline clustering, a recency-based lapse label, rule-based ticket classification and simulated refund actions. It does not connect to real payment services or external LLM APIs. Further work includes leakage-safe model evaluation, retry handling, advanced agent orchestration and expanded policy evaluation.
 
## Outputs
Generated CSV, model, JSONL and SQLite files are stored in the data and outputs directories.
