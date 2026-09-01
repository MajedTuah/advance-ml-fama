# 🧹 Session 02 — Data Quality & Leakage-Free Pipeline Construction

> **Day 1 | 10:00 AM – 11:00 AM | Duration: 60 minutes**

---

## 🎯 Learning Objectives

By the end of this session, learners will be able to:
1. Identify the main dimensions of data quality and assess them on a realistic dataset.
2. Recognize the most common forms of leakage and explain why they distort model evaluation.
3. Build a reproducible, leakage-free machine learning pipeline using scikit-learn.
4. Use time-aware validation to avoid future information leaking into the past.

---

## 🧠 Core Concepts

### 1. Data quality dimensions

Good data is not only large — it must be valid, complete, and reliable.

| Dimension | What it means | Example |
|-----------|---------------|---------|
| Integrity | Data follows the expected schema and types | Birth year stored as text instead of integer |
| Completeness | Missing values are limited and understood | Null income values |
| Accuracy | Values are correct and realistic | Salary outside a plausible range |
| Timeliness | Data is current enough for the decision being made | Stale pricing data |
| Validity | Values respect business rules and constraints | Negative age values |

### 2. Missing data types

- MCAR: Missing completely at random
- MAR: Missingness depends on observed values
- MNAR: Missingness depends on the missing value itself

This matters because the correct handling strategy differs for each type.

### 3. Data leakage

Leakage is when information from outside the training context is used to make predictions. It creates optimistic metrics that do not hold in production.

Common sources include:
- target leakage from features that describe the future outcome
- preprocessing done on the full dataset before the split
- random splits on time-ordered data
- group leakage when the same entity appears in both train and test

### 4. Leakage-free pipeline design

The correct pattern is:

- split into train/validation/test
- fit preprocessing on training data only
- fit the model only on transformed training data
- evaluate on untouched test data

This is exactly what `Pipeline` and `ColumnTransformer` are designed for.

---

## 🏋️ Sample Activity — Loan Default Prediction

### Business problem
A bank wants to predict which customers are likely to default on a loan in the next 30 days.

### Data fields
- `customer_id`
- `loan_amount`
- `annual_income`
- `credit_score`
- `employment_years`
- `loan_type`
- `region`
- `days_since_last_payment`
- `defaulted_in_next_30_days`

### Task
Build a fraud/default prediction model, but do not allow any information that would not be available at prediction time.

### Example of leakage
If the dataset contains a feature like:
- `payment_status_after_30_days`
- `loan_outcome_label`
- `days_to_default`

then the model is effectively seeing the answer before it predicts.

This would cause the model to look extraordinarily accurate during validation, but it would fail badly in production when the feature is absent.

### Correct approach
1. Time-split the data by loan application date.
2. Identify numeric and categorical features.
3. Use `ColumnTransformer` to clean and encode features.
4. Fit a `Pipeline` on training data only.
5. Evaluate on the holdout period.

### Example code

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

# Assume df contains loan application variables and target
X = df.drop(columns=['customer_id', 'defaulted_in_next_30_days'])
y = df['defaulted_in_next_30_days']

numeric_features = ['loan_amount', 'annual_income', 'credit_score', 'employment_years']
categorical_features = ['loan_type', 'region']

preprocessor = ColumnTransformer([
    ('num', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ]), numeric_features),
    ('cat', Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ]), categorical_features)
])

model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=1000))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model.fit(X_train, y_train)
preds = model.predict(X_test)

print(classification_report(y_test, preds))
print('AUC:', roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))
```

---

## 💡 Explanation of the activity

This activity illustrates the central lesson of the session:

- A model can be very accurate on paper and still be useless in the real world if it is trained with leakage.
- The right features are not just statistically predictive — they must be available at the time the decision is made.
- Random train/test splits can be misleading on time-dependent data.
- `sklearn.Pipeline` ensures that data preparation happens inside the training process, not before it.
- The aim is to estimate how the model will perform in deployment, not how well it can memorize the observed label.

A strong answer to this exercise will show a clear distinction between:
- a leaky feature that bypasses the real problem
- a correct feature set based on information available at application time
- a valid validation strategy that respects business timing

---

## 📌 Recommended discussion questions

1. Which feature in the loan example is most likely to create leakage?
2. Why is time-based splitting more realistic than random splitting here?
3. What would happen if a scaler were fit on the full dataset before splitting?
4. Why is a `Pipeline` important even when the model code looks simple?

---

## 📝 Key Takeaways

- Leakage creates artificially high performance.
- A data pipeline should not see future information during training.
- Time-aware splits are essential for real-world forecasting and classification tasks.
- Reproducible preprocessing and validation prevent silent model failures.

---

## ❓ Quiz Questions

1. What is target leakage? Give one example from the loan dataset.
2. Why is fitting a scaler on the full dataset a problem?
3. When should you prefer a time-based validation split over random splitting?
4. How does `sklearn.Pipeline` help reduce leakage risk?
5. Why might a model with “great metrics” still be a bad production model?

---

## 📖 Further Reading

- [Kaggle — Data Leakage Tutorial](https://www.kaggle.com/learn/data-leakage)
- [scikit-learn Pipeline docs](https://scikit-learn.org/stable/modules/pipeline.html)
- [scikit-learn ColumnTransformer docs](https://scikit-learn.org/stable/modules/compose.html#columntransformer)
