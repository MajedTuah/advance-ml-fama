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

### Activity 3 — CV Fold Visualization (code)
Build a matplotlib grid showing 5-fold TimeSeriesSplit with color-coded train/test blocks

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
