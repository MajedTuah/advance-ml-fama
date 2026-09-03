# ⚙️ Session 03 — Production Model Training in One Notebook

> **Day 1 | 11:00 AM – 12:00 PM | Duration: 60 minutes**

---

## 🎯 Learning Objectives

By the end of this session, learners will be able to:
1. Explain why notebooks are powerful for exploration but need structure for production.
2. Organize ML code into clean, reusable functions inside a single notebook.
3. Use a config dictionary and a small CLI pattern to make training reproducible.
4. Log progress and save model artifacts without creating separate Python files.

---

## 🧠 Core Concepts

### 1. Why training code needs structure

Even inside a notebook, production-style ML should avoid hidden cell state and hard-coded values.

| Problem | Impact |
|---|---|
| Hidden state | Runs depend on execution order |
| Hard-coded values | Hard to reproduce and tune |
| Unclear logging | Failures are difficult to debug |
| Monolithic cells | Code becomes hard to maintain |

### 2. Single Responsibility in a notebook

Each function in the notebook should do one thing:
- load data
- build features
- train the model
- evaluate the model
- save the artifact

This keeps the notebook readable while still teaching production patterns.

### 3. Configuration in a single file

Instead of a separate YAML config, the notebook can keep a dictionary of params at the top.

```python
config = {
    'target_column': 'churn',
    'test_size': 0.2,
    'random_state': 42,
    'model_type': 'logistic_regression',
    'max_iter': 500
}
```

This is enough to teach the production principle without splitting the work across files.

### 4. Reproducibility checklist

- Use a fixed random seed
- Log parameter values
- Save the trained model
- Store evaluation metrics
- Keep the notebook deterministic and runnable top-to-bottom

### 5. Logging vs print

`print()` is fine for quick checks, but `logging` is better for real training flows because it supports levels, files, and timestamps.

---

## 🏋️ Activity

This session uses a single notebook to walk through a complete training workflow:

1. Generate a synthetic churn dataset
2. Split into train/test sets
3. Define reusable functions inside the notebook
4. Train a logistic regression model
5. Evaluate metrics
6. Save model and metrics locally

The key idea is that the same production workflow can live inside a notebook without creating script files.

---

## 📌 What this folder contains

- `notebook.ipynb` — the complete lesson and working ML pipeline
- no separate Python files required

---

## 📝 Key Takeaways

- A notebook can still follow production patterns without being split into many files.
- Good ML code is structured, parameterized, and logged.
- Reproducibility matters even inside a single notebook.
- Functions inside the notebook are a practical bridge between exploration and production.

---

## ❓ Quiz Questions

1. Why do notebooks still need structure even when they are not deployed as scripts?
2. What does the Single Responsibility Principle mean in a notebook workflow?
3. Why is a config dictionary useful during model training?
4. What is the difference between `print()` and `logging`?
5. Why is it important to save model artifacts and metrics?

---

## 📖 Further Reading

- [Google Production ML Systems Overview](https://developers.google.com/machine-learning/crash-course/production-ml-systems)
- [scikit-learn Model Persistence](https://scikit-learn.org/stable/modules/model_persistence.html)
- [Python Logging Guide](https://docs.python.org/3/library/logging.html)
