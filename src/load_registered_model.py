# src/load_registered_model.py
import os
import mlflow
import mlflow.sklearn

mlflow.set_tracking_uri(
    os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
)
MODEL_URI = "models:/iris-classifier-prod/Staging"

print(f"Loading registered model from: {MODEL_URI}")
model = mlflow.sklearn.load_model(MODEL_URI)

print("Model loaded successfully!")
print("Model type:", type(model))
print("Model details:", model)