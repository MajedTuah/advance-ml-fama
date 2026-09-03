from pathlib import Path

import pandas as pd
from sklearn.datasets import make_classification


def ensure_dataset(data_path: str, target_column: str) -> Path:
    """Create a tiny synthetic dataset if no data file exists yet."""
    path = Path(data_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        X, y = make_classification(
            n_samples=1000,
            n_features=6,
            n_informative=4,
            n_redundant=1,
            n_classes=2,
            weights=[0.65, 0.35],
            random_state=42,
        )

        feature_names = [
            "age",
            "monthly_spend",
            "tenure_months",
            "support_tickets",
            "usage_score",
            "contract_type",
        ]
        df = pd.DataFrame(X, columns=feature_names)
        df["contract_type"] = df["contract_type"].round(0).astype(int)
        df["churn"] = y
        df.to_csv(path, index=False)

    return path


def load_data(data_path: str, target_column: str) -> pd.DataFrame:
    """Load the dataset and validate that the target exists."""
    path = ensure_dataset(data_path, target_column)
    df = pd.read_csv(path)

    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset.")

    return df


def split_data(df: pd.DataFrame, target_column: str, test_size: float, random_state: int):
    """Return train/test arrays for features and target."""
    from sklearn.model_selection import train_test_split

    X = df.drop(columns=[target_column])
    y = df[target_column]

    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )
