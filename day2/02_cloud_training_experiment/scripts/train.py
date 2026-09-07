"""
train.py — Azure ML-compatible training script for credit default model.
Run locally:   python train.py --learning-rate 0.05 --max-depth 5 --n-estimators 200
Run on AzureML: submitted via Command Job in notebook.ipynb
"""

import argparse
import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn

# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--data", type=str, default=None, help="Path to training CSV")
parser.add_argument("--learning-rate", type=float, default=0.05)
parser.add_argument("--max-depth", type=int, default=5)
parser.add_argument("--n-estimators", type=int, default=200)
parser.add_argument("--min-samples-split", type=int, default=20)
parser.add_argument("--output-dir", type=str, default="./outputs")
args = parser.parse_args()

os.makedirs(args.output_dir, exist_ok=True)

# ---------------------------------------------------------------------------
# Data — use provided path or generate synthetic dataset
# ---------------------------------------------------------------------------
if args.data and os.path.exists(args.data):
    df = pd.read_csv(args.data)
    X = df.drop("default", axis=1)
    y = df["default"]
else:
    print("[INFO] No data path provided — using synthetic dataset.")
    np.random.seed(42)
    n = 5000
    X = pd.DataFrame({
        "limit_bal": np.random.randint(10000, 500000, n),
        "age": np.random.randint(21, 75, n),
        "pay_0": np.random.randint(-1, 9, n),
        "pay_2": np.random.randint(-1, 9, n),
        "bill_amt1": np.random.randint(0, 200000, n),
        "pay_amt1": np.random.randint(0, 50000, n),
    })
    y = (0.3 * (X["pay_0"] > 2) + 0.2 * (X["limit_bal"] < 50000) +
         np.random.rand(n) * 0.5 > 0.55).astype(int)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------------------------------------------------------------
# MLflow tracking
# ---------------------------------------------------------------------------
mlflow.autolog()

with mlflow.start_run():
    mlflow.log_param("learning_rate", args.learning_rate)
    mlflow.log_param("max_depth", args.max_depth)
    mlflow.log_param("n_estimators", args.n_estimators)
    mlflow.log_param("min_samples_split", args.min_samples_split)

    model = GradientBoostingClassifier(
        learning_rate=args.learning_rate,
        max_depth=args.max_depth,
        n_estimators=args.n_estimators,
        min_samples_split=args.min_samples_split,
        random_state=42
    )
    model.fit(X_train, y_train)

    train_auc = roc_auc_score(y_train, model.predict_proba(X_train)[:, 1])
    val_auc   = roc_auc_score(y_val,   model.predict_proba(X_val)[:, 1])

    mlflow.log_metric("train_auc", train_auc)
    mlflow.log_metric("val_auc",   val_auc)

    print(f"Train AUC: {train_auc:.4f} | Val AUC: {val_auc:.4f}")

    # Confusion matrix artifact
    cm = confusion_matrix(y_val, model.predict(X_val))
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix"); fig.colorbar(im)
    plt.tight_layout()
    cm_path = os.path.join(args.output_dir, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=100); plt.close()
    mlflow.log_artifact(cm_path)

    # Save model
    mlflow.sklearn.log_model(model, "model")

    # Summary JSON
    summary = {"train_auc": round(train_auc, 4), "val_auc": round(val_auc, 4)}
    summary_path = os.path.join(args.output_dir, "summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

print("Training complete.")
