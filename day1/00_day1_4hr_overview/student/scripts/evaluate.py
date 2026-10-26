import json
from pathlib import Path

from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score


def evaluate_model(model, X_test, y_test, output_path: str):
    predictions = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "classification_report": classification_report(y_test, predictions, output_dict=True),
    }

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metrics, indent=2, default=str))

    return metrics
