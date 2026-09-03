import argparse
import logging
from pathlib import Path

import yaml

from data_loader import load_data, split_data
from evaluate import evaluate_model
from features import build_features
from train import save_model, train_model


def load_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def configure_logging(log_path: str):
    log_file = Path(log_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="a", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def main():
    parser = argparse.ArgumentParser(description="Train a modular ML model.")
    parser.add_argument("--config", default="scripts/config.yaml", help="Path to YAML config file")
    args = parser.parse_args()

    config = load_config(args.config)
    data_cfg = config["data"]
    model_cfg = config["model"]
    path_cfg = config["paths"]

    configure_logging(path_cfg["log_path"])
    logger = logging.getLogger(__name__)
    logger.info("Starting training workflow")
    logger.info(f"Config loaded from {args.config}")

    df = load_data(data_cfg["path"], data_cfg["target_column"])
    X_train, X_test, y_train, y_test = split_data(
        df,
        data_cfg["target_column"],
        data_cfg["test_size"],
        data_cfg["random_state"],
    )

    X_train_processed, y_train_processed = build_features(X_train.join(y_train), data_cfg["target_column"])
    X_test_processed, y_test_processed = build_features(X_test.join(y_test), data_cfg["target_column"])

    model = train_model(X_train_processed, y_train_processed, model_cfg)
    save_model(model, path_cfg["model_path"])
    metrics = evaluate_model(model, X_test_processed, y_test_processed, path_cfg["report_path"])

    logger.info(f"Training complete. Metrics: {metrics}")


if __name__ == "__main__":
    main()
