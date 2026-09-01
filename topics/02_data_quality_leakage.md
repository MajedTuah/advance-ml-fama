# 🧹 Topic 02 — Data Quality & Leakage-Free Pipeline Construction
> **Schedule:** Day 1 | 10:00 AM – 11:00 AM | Duration: 60 min
> **Folder:** `day1/02_data_quality_leakage/`
> **Status:** 🔲 Pending Build

---

## 🎯 Learning Objectives
1. Identify the top 5 data quality dimensions and measure them on a real dataset
2. Detect and eliminate all forms of data leakage before model training
3. Build a reproducible, leakage-free `sklearn.Pipeline` object
4. Implement train/val/test splits that respect time-ordering

---

## 🧠 Core Concepts

### 1. Data Quality Dimensions (ICATV Framework)
| Dimension | Description | Detection Method |
|-----------|-------------|-----------------|
| **I**ntegrity | Schema correctness, data types | `df.dtypes`, schema validation |
| **C**ompleteness | Missing values | `df.isnull().sum()`, heatmaps |
| **A**ccuracy | Outliers, wrong values | IQR boxplots, z-score |
| **T**imeliness | Stale data, future leakage | timestamp analysis |
| **V**alidity | Constraint violations | range checks, regex |

### 2. Missing Data Taxonomy
- **MCAR** (Missing Completely At Random) — Safe to drop/impute simply
- **MAR** (Missing At Random) — Missingness depends on other observed features
- **MNAR** (Missing Not At Random) — Missingness depends on the missing value itself (hardest — e.g., high earners don't report income)

### 3. Data Leakage — The Silent Killer
> "Leakage is the single most important issue affecting the practical application of machine learning." — Kaggle

**Types of Leakage:**
| Type | Description | Example |
|------|-------------|---------|
| Target Leakage | Feature encodes the target | Using `loan_approved` to predict `default` |
| Train-Test Contamination | Preprocessing fit on full data | Fitting scaler on train+test, then splitting |
| Temporal Leakage | Future data used for past prediction | Using Dec data to predict Nov outcomes |
| Group Leakage | Same entity in train and test | Same customer in both splits |

### 4. Leakage-Free sklearn Pipeline
```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# CORRECT: fit only on X_train
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])
pipeline = Pipeline([('preprocessor', preprocessor), ('model', clf)])
pipeline.fit(X_train, y_train)  # ← Only sees training data
```

### 5. Validation Strategies
| Strategy | Use Case | Risk |
|----------|----------|------|
| Hold-out (80/20) | Large datasets, quick iteration | High variance if small dataset |
| K-Fold CV | Medium datasets | Slow but robust |
| Stratified K-Fold | Imbalanced classes | Required for rare events |
| TimeSeriesSplit | Time series / sequential data | Only correct method for temporal data |
| Group K-Fold | Grouped data (patients, stores) | Prevents group leakage |

---

## 📊 Diagrams & Visuals Required

| # | Diagram | Type | Notebook Cell |
|---|---------|------|---------------|
| 1 | Missing data heatmap (before cleaning) | `seaborn.heatmap` | Cell 3 |
| 2 | Data quality radar — before vs. after | Matplotlib radar | Cell 5 |
| 3 | Leakage types flowchart | Annotated flowchart | Cell 7 |
| 4 | Pipeline `fit` vs `transform` flow | Matplotlib annotated arrows | Cell 9 |
| 5 | TimeSeriesSplit folds visualization | Matplotlib color grid | Cell 11 |

---

## 🏋️ Activities

### Activity 1 — Find All Leakage Sources (20 min)
Given a "poisoned" synthetic dataset (credit card fraud), identify:
- Which features leak the target?
- Which preprocessing steps were done on full data?
- Is the split time-ordered?

### Activity 2 — Refactor Broken Pipeline (20 min)
Given a broken script that fits a scaler on train+test data:
- Identify the bug
- Rewrite using `sklearn.Pipeline`
- Compare metrics: leaky model vs. clean model

### Activity 3 — ML Sample Activity: Predict Loan Default Without Leakage (20 min)
Use the following business case to practice the full data quality workflow:

#### Scenario
A bank wants to predict whether a borrower will default on a loan within the next 30 days.

You have a data table with fields such as:
- `customer_id`
- `loan_amount`
- `annual_income`
- `employment_years`
- `credit_score`
- `days_since_last_payment`
- `existing_loans`
- `loan_approval_date`
- `defaulted_in_next_30_days`

#### Exercise
1. Split the data by time, not randomly.
2. Build a simple baseline model using `LogisticRegression`.
3. Identify at least one leakage feature.
4. Rebuild the model using a leakage-free `Pipeline`.
5. Compare the model performance before and after fixing the leak.

#### Example of the leak
A feature such as `days_to_default` or a post-approval status flag is not available at prediction time and should never be used to train the model. If you include it, the model will look unrealistically good because it is effectively seeing the answer.

#### Example implementation
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

# Example: historical loan data
# Assume defaulted_in_next_30_days is the target
X = df.drop(columns=['customer_id', 'defaulted_in_next_30_days'])
y = df['defaulted_in_next_30_days']

# Bad approach: random split + leakage feature still present
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Leaky feature example: training on a variable that only exists after the loan outcome
# For example, 'payment_status_after_30_days' or 'loan_outcome_label'
# would create target leakage.

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

model.fit(X_train, y_train)
preds = model.predict(X_test)
print(classification_report(y_test, preds))
print('AUC:', roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))
```

#### Explanation
This activity teaches the core idea behind leakage-free modelling:

- The model must only learn from information available at the time the prediction is made.
- If a feature is only known after the outcome occurs, it is leakage.
- Random splitting is dangerous when the business problem is time-dependent.
- `sklearn.Pipeline` ensures that preprocessing is fit only on the training data, preventing train/test contamination.
- A clean model may have lower test accuracy than the leaky variant, but it is the valid one because it reflects real-world deployment.

In practice, a lender should predict default for a prospective borrower using data available at application time, not data that only exists after the default has happened.

---

## 📝 Notebook Cell Plan

```
Cell 01 [MD]   → Session intro & objectives
Cell 02 [Code] → Generate synthetic dataset with quality issues
Cell 03 [Code] → Missing data heatmap (seaborn)
Cell 04 [MD]   → MCAR / MAR / MNAR explanation
Cell 05 [Code] → Data quality radar chart (before vs. after)
Cell 06 [MD]   → Leakage types explained with examples
Cell 07 [Code] → Demonstrate target leakage (inflated accuracy demo)
Cell 08 [Code] → Fix leakage: before vs. after accuracy comparison
Cell 09 [Code] → Build leakage-free sklearn Pipeline
Cell 10 [MD]   → Validation strategy comparison
Cell 11 [Code] → TimeSeriesSplit fold visualization
Cell 12 [MD]   → Key Takeaways + Quiz
```

---

## 📁 Files to Create

```
day1/02_data_quality_leakage/
├── README.md
└── notebook.ipynb
```

---

## 📝 Key Takeaways
- Leakage causes optimistic metrics during training → catastrophic failure in production
- Always `fit()` preprocessing on ONLY the training set
- Temporal data **requires** temporal splits — never random
- A clean pipeline guarantees reproducibility and prevents silent failures

---

## ❓ Quiz Questions
1. What is target leakage? Give a real-world example.
2. Why is fitting a scaler on the full dataset (train + test) a problem?
3. When should you use TimeSeriesSplit instead of K-Fold?
4. What is MNAR missing data and why is it the hardest to handle?
5. How does `sklearn.Pipeline` structurally prevent leakage?

---

## 📖 Further Reading
- [Kaggle — Data Leakage Tutorial](https://www.kaggle.com/learn/data-leakage)
- [scikit-learn Pipeline docs](https://scikit-learn.org/stable/modules/pipeline.html)
- Kuhn & Johnson — "Feature Engineering and Selection" Chapter 1
