import pandas as pd
from pathlib import Path
 
# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent
 
input_file = BASE_DIR / "data" / "raw" / "customers.csv"
output_file = BASE_DIR / "data" / "clean" / "customers.csv"
 
# Create output folder
output_file.parent.mkdir(parents=True, exist_ok=True)
 
# Load original data
df = pd.read_csv(input_file)
 
print("ORIGINAL CUSTOMER DATA")
print("Total records:", len(df))
 
# 1. Check and remove duplicate customer IDs
duplicate_count = df.duplicated(subset="customer_id").sum()
df = df.drop_duplicates(subset="customer_id", keep="first")
 
print("Duplicate customer IDs removed:", duplicate_count)
 
# 2. Clean city names
df["city"] = df["city"].astype("string").str.strip().str.title()
 
# 3. Standardize gender
df["gender"] = df["gender"].astype("string").str.strip().str.lower()
 
df["gender"] = df["gender"].replace({
    "f": "Female",
    "female": "Female",
    "m": "Male",
    "male": "Male"
})
 
df["gender"] = df["gender"].fillna("Unknown")
 
# 4. Clean age values
df["age"] = pd.to_numeric(df["age"], errors="coerce")
 
invalid_age_count = ((df["age"] < 0) | (df["age"] > 100)).sum()
 
df.loc[(df["age"] < 0) | (df["age"] > 100), "age"] = pd.NA
 
# Fill missing ages with median
median_age = df["age"].median()
df["age"] = df["age"].fillna(median_age)
 
# 5. Convert signup date
df["signup_date"] = pd.to_datetime(
    df["signup_date"], errors="coerce"
)
 
# 6. Remove exact duplicate rows
exact_duplicates = df.duplicated().sum()
df = df.drop_duplicates()
 
# 7. Save cleaned data
df.to_csv(output_file, index=False)
 
# 8. Display final report
print("\nCUSTOMER DATA CLEANING REPORT")
print("--------------------------------")
print("Final records:", len(df))
print("Invalid ages corrected:", invalid_age_count)
print("Median age used:", median_age)
print("Exact duplicate rows removed:", exact_duplicates)
 
print("\nMissing values:")
print(df.isnull().sum())
 
print("\nGender distribution:")
print(df["gender"].value_counts())
 
print("\nCity distribution:")
print(df["city"].value_counts())
 
print("\nCleaned file saved successfully:")
print(output_file)
df = pd.read_csv(input_file)
df.loc[(df["age"] < 18) | (df["age"] > 100), "age"] = pd.NA