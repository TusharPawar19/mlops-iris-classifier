import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

import mlflow
import mlflow.sklearn

# 1. Connect to MLflow server
mlflow.set_tracking_uri("http://127.0.0.1:5000")
experiment_name = "iris_classification"
mlflow.set_experiment(experiment_name)


def load_data():
    iris = load_iris(as_frame=True)
    df = iris.frame
    X = df.drop(columns=["target"])
    y = df["target"]
    return X, y, iris.target_names


def plot_confusion_matrix(cm, target_names, model_name):
    fig, ax = plt.subplots(figsize=(6, 5))
    cax = ax.matshow(cm, cmap=plt.cm.Blues)
    fig.colorbar(cax)

    ax.set_xticks(range(len(target_names)))
    ax.set_yticks(range(len(target_names)))
    ax.set_xticklabels(target_names)
    ax.set_yticklabels(target_names)

    for i in range(len(target_names)):
        for j in range(len(target_names)):
            ax.text(
                j,
                i,
                str(cm[i, j]),
                va="center",
                ha="center",
                color="red" if cm[i, j] > (cm.max() / 2) else "black",
            )

    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(f"Confusion Matrix - {model_name}")

    os.makedirs("artifacts", exist_ok=True)
    plot_path = os.path.join("artifacts", f"{model_name}_cm.png")
    plt.savefig(plot_path, bbox_inches="tight")
    plt.close(fig)
    return plot_path


def train_and_log(model_name, model, X_train, X_test, y_train, y_test, target_names):
    print(f"\nTraining: {model_name}")

    with mlflow.start_run(run_name=model_name):
        # Log parameters
        params = model.get_params()
        mlflow.log_params(params)

        # Train model
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")

        print(f"  Accuracy: {acc:.4f} | F1-Score: {f1:.4f}")

        # Log metrics
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)

        # Save and log confusion matrix plot
        cm = confusion_matrix(y_test, y_pred)
        plot_path = plot_confusion_matrix(cm, target_names, model_name)
        mlflow.log_artifact(plot_path, artifact_path="plots")

        # Log model (resolves skops untrusted tree error and artifact_path deprecation)
        try:
            mlflow.sklearn.log_model(
                sk_model=model,
                name="model",
                serialization_format=mlflow.sklearn.SERIALIZATION_FORMAT_CLOUDPICKLE,
            )
        except TypeError:
            # Fallback for older MLflow versions that still expect artifact_path
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                serialization_format=mlflow.sklearn.SERIALIZATION_FORMAT_CLOUDPICKLE,
            )


def main():
    X, y, target_names = load_data()
    print(f"Dataset shape: {X.shape}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "logistic_regression": LogisticRegression(max_iter=200, random_state=42),
        "random_forest_shallow": RandomForestClassifier(
            n_estimators=50, max_depth=3, random_state=42
        ),
        "random_forest_deep": RandomForestClassifier(
            n_estimators=100, max_depth=None, random_state=42
        ),
    }

    for name, model in models.items():
        train_and_log(name, model, X_train, X_test, y_train, y_test, target_names)


if __name__ == "__main__":
    main()