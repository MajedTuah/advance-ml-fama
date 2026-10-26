from __future__ import annotations

import pandas as pd


def build_features(df: pd.DataFrame, target_column: str):
    """Create a simple feature matrix for training.

    This keeps the example understandable while still demonstrating a real
    production-style separation of responsibilities.
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]

    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = [col for col in X.columns if col not in numeric_cols]

    X_clean = X.copy()

    for col in numeric_cols:
        median_value = X_clean[col].median()
        X_clean[col] = X_clean[col].fillna(median_value)

    for col in categorical_cols:
        X_clean[col] = X_clean[col].fillna("missing")

    X_processed = pd.get_dummies(X_clean, columns=categorical_cols, drop_first=True)

    return X_processed, y
