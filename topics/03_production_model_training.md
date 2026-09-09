# ⚙️ Topic 03 — Production Model Training & Modular Scripting

> **Schedule:** Day 1 | 11:00 AM – 12:00 PM | Duration: 60 min
> **Folder:** `day1/03_production_training/`
> **Status:** 🔲 Pending Build

---

## 🎯 Learning Objectives

1. Restructure a messy notebook into production-ready Python scripts
2. Apply the Single Responsibility Principle (SRP) to ML code
3. Implement configuration management with YAML + argparse
4. Build a reproducible training run with seeds, logging, and checkpointing

---

## 🧠 Core Concepts

### 1. Why Notebooks Fail in Production

| Problem                               | Impact                           |
| ------------------------------------- | -------------------------------- |
| Hidden state (cells run out of order) | Non-reproducible results         |
| No CLI interface                      | Can't be scheduled or automated  |
| Hard-coded values everywhere          | No environment flexibility       |
| No logging                            | Silent failures in production    |
| Global variables                      | Untestable, fragile code         |
| Monolithic structure                  | Can't unit test individual steps |

### 2. Module Design — Single Responsibility Principle

Each module does ONE thing:

1. ```
   scripts/
   ├── config.yaml        ← All parameters live here
   ├── data_loader.py     ← load_data(), validate_schema(), split_data()
   ├── features.py        ← build_features(), encode(), scale()
   ├── train.py           ← train_model(), save_checkpoint()
   ├── evaluate.py        ← evaluate_model(), generate_report()
   └── main.py            ← Orchestrates: data → features → train → evaluate
   ```

### 3. Configuration Management

**Problem:** Hardcoded values scattered across scripts
**Solution:** Single `config.yaml` + CLI overrides

```yaml
# config.yaml
model:
  type: random_forest
  n_estimators: 100
  max_depth: 5
  random_state: 42

data:
  train_path: data/train.csv
  test_path: data/test.csv
  target_column: churn

training:
  test_size: 0.2
  cv_folds: 5

output:
  model_path: models/model.pkl
  report_path: reports/evaluation.json
```

```python
# main.py — CLI override example
import argparse, yaml
parser = argparse.ArgumentParser()
parser.add_argument('--config', default='config.yaml')
parser.add_argument('--n_estimators', type=int)  # override config
args = parser.parse_args()
```

### 4. Reproducibility Checklist

- [ ] Set `random_state` / seed in numpy, sklearn, torch
- [ ] Pin library versions in `requirements.txt`
- [ ] Log all config parameters at run start
- [ ] Save model with timestamp + config hash
- [ ] Record train/val/test split indices

### 5. Production Logging Pattern

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info(f"Training started | Config: {config}")
```

### 6. Model Serialization Options

| Format       | Use Case                  | Pros                | Cons                       |
| ------------ | ------------------------- | ------------------- | -------------------------- |
| `joblib`   | sklearn models            | Fast, Python-native | Python-only                |
| `pickle`   | Any Python object         | Flexible            | Security risk, Python-only |
| ONNX         | Cross-platform deployment | Language-agnostic   | Complex conversion         |
| MLflow Model | Full MLOps lifecycle      | Versioned, tracked  | Requires MLflow            |

---

## 📊 Diagrams & Visuals Required

| # | Diagram                                     | Type                                | Notebook Cell |
| - | ------------------------------------------- | ----------------------------------- | ------------- |
| 1 | Notebook vs. Script architecture comparison | Side-by-side annotated diagram      | Cell 3        |
| 2 | Module dependency graph (what imports what) | Directed graph (networkx or manual) | Cell 5        |
| 3 | Training loop flowchart                     | Annotated flowchart                 | Cell 7        |
| 4 | Training loss + val loss curve              | Line chart with matplotlib          | Cell 9        |

---

## 🏋️ Activities

### Activity 1 — Refactor the Notebook (25 min)

Given a monolithic 200-line notebook:

- Extract `data_loader.py` (data loading + splitting)
- Extract `features.py` (feature engineering)
- Extract `train.py` (model training + saving)
- Extract `evaluate.py` (metrics + reporting)
- Wire everything through `main.py`

### Activity 2 — Add Config + CLI (15 min)

- Create `config.yaml` for the refactored scripts
- Add `argparse` CLI so `python main.py --n_estimators 200` works
- Verify: does `python main.py --help` show all options?

### Activity 3 — Training Curve (code)

- Simulate a training loss curve (decreasing) + validation loss curve (U-shaped)
- Annotate the "overfitting zone"
- Add a vertical dashed line at the optimal epoch

---

## 📝 Notebook Cell Plan

```
Cell 01 [MD]   → Session intro & objectives
Cell 02 [MD]   → Why notebooks fail in production (table)
Cell 03 [Code] → Architecture comparison diagram
Cell 04 [MD]   → Module design + SRP explanation
Cell 05 [Code] → Module dependency graph
Cell 06 [MD]   → config.yaml structure walkthrough
Cell 07 [Code] → Full config.yaml + argparse demo
Cell 08 [MD]   → Logging best practices
Cell 09 [Code] → Logging setup + training loop with logging
Cell 10 [Code] → Training loss curve plot
Cell 11 [MD]   → Model serialization comparison
Cell 12 [MD]   → Key Takeaways + Quiz
```

---

## 📁 Files to Create

```
day1/03_production_training/
├── README.md
├── notebook.ipynb
└── scripts/
    ├── config.yaml
    ├── data_loader.py
    ├── features.py
    ├── train.py
    ├── evaluate.py
    └── main.py
```

---

## 📝 Key Takeaways

- Notebooks are for **exploration**; scripts are for **production**
- Config files decouple logic from parameters — change behavior without touching code
- Every function should do ONE thing and do it well
- Logging is non-negotiable; `print()` is not logging
- Reproducibility requires explicit seeds + pinned dependencies

---

## ❓ Quiz Questions

1. Why can't you reliably run a Jupyter notebook in a CI/CD pipeline?
2. What is the "single responsibility principle" in software design?
3. Why do we set random seeds before training?
4. What is the functional difference between `logging` and `print()`?
5. When would you use ONNX format vs. `joblib` for model saving?

---

## 📖 Further Reading

- [Production ML Systems — Google](https://developers.google.com/machine-learning/crash-course/production-ml-systems)
- [Cookiecutter Data Science Project Structure](https://drivendata.github.io/cookiecutter-data-science/)
- "Clean Code" — Robert C. Martin (Chapter 3: Functions)
