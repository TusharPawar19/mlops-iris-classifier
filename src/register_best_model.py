# src/register_best_model.py
import os
import mlflow
from mlflow.tracking import MlflowClient

# MLflow setup
mlflow.set_tracking_uri(
    os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
)
client = MlflowClient()

# Locate experiment
experiment = client.get_experiment_by_name("iris-classification-baseline")
if not experiment:
  raise RuntimeError("Experiment 'iris-classification-baseline' not found.")

# Fetch best run based on macro F1 score
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id], order_by=["metrics.f1_macro DESC"]
)
best_run = runs[0]
best_run_id = best_run.info.run_id
print(f"Best Run ID: {best_run_id}")
print(f"Best Model: {best_run.data.params['model_type']}")
print(f"Best F1 Score: {best_run.data.metrics['f1_macro']}")

# Register the model
model_uri = f"runs:/{best_run_id}/model"
registered_model_name = "iris-classifier-prod"
model_version = mlflow.register_model(
    model_uri=model_uri, name=registered_model_name
)

# Transition to Staging
client.transition_model_version_stage(
    name=registered_model_name, version=model_version.version, stage="Staging"
)
print(f"Model version {model_version.version} successfully moved to Staging.")