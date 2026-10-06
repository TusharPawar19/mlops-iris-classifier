# prepare_feature_source.py
"""
Prepares the iris_features.parquet source file with sample_id and event_timestamp.
"""
from pathlib import Path
import numpy as np
import pandas as pd

output_file = Path("data/iris_features.parquet")
output_file.parent.mkdir(parents=True, exist_ok=True)

# Attempt to locate Experiment 4 output relative to feature_repo
candidate_paths = [
    Path("C:/Users/tushh/mlops-iris-classifier/data/processed/iris_features.csv"),
    Path("../../../data/processed/iris_features.csv"),
    Path("../../data/processed/iris_features.csv"),
]

csv_file = None
for p in candidate_paths:
    if p.exists():
        csv_file = p
        break

if csv_file:
    print(f"Reading from: {csv_file}")
    df = pd.read_csv(csv_file)
else:
    print("CSV not found. Generating Iris feature dataset directly...")
    from sklearn.datasets import load_iris
    iris = load_iris(as_frame=True)
    df = iris.frame
    df.columns = [c.replace(" (cm)", "") + " (cm)" if "cm" in c else c for c in df.columns]
    df["species"] = [iris.target_names[i] for i in iris.target]
    df["sepal_area"] = df["sepal length (cm)"] * df["sepal width (cm)"]
    df["petal_area"] = df["petal length (cm)"] * df["petal width (cm)"]
    df["sepal_to_petal_length_ratio"] = df["sepal length (cm)"] / df["petal length (cm)"]
    df["petal_length_bin"] = pd.qcut(df["petal length (cm)"], q=3, labels=["short", "medium", "long"]).astype(str)

# Ensure sample_id is present as the first column with int64 type
if "sample_id" in df.columns:
    df["sample_id"] = df["sample_id"].astype("int64")
else:
    df.insert(0, "sample_id", np.arange(len(df), dtype="int64"))

# Ensure event_timestamp and created_timestamp exist with UTC timezone
start_time = pd.Timestamp("2026-08-15 15:20:02", tz="UTC")
df["event_timestamp"] = pd.date_range(start=start_time, periods=len(df), freq="min")
df["created_timestamp"] = df["event_timestamp"]

# Cast numerical columns to float32 to match Feast schema
float_cols = [
    "sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)",
    "sepal_area", "petal_area", "sepal_to_petal_length_ratio"
]
for col in float_cols:
    if col in df.columns:
        df[col] = df[col].astype("float32")

# Save to Parquet
df.to_parquet(output_file, index=False)
print(f"Successfully wrote {len(df)} rows to {output_file}")
print("Columns present:", df.columns.tolist())