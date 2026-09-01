# 🎛️ Topic 04 — Hyperparameter Optimization & Experiment Tracking
> **Schedule:** Day 1 | 2:00 PM – 3:00 PM | Duration: 60 min
> **Folder:** `day1/04_hyperparameter_optim/`
> **Status:** 🔲 Pending Build

---

## 🎯 Learning Objectives
1. Distinguish hyperparameters from learned model parameters
2. Implement Bayesian Optimization with Optuna
3. Track experiments, metrics, and artifacts with MLflow
4. Analyze and compare runs using parallel coordinates and importance plots

---

## 🧠 Core Concepts

### 1. Hyperparameters vs. Model Parameters
| Type | Description | Who Sets It | Examples |
|------|-------------|-------------|---------|
| **Hyperparameter** | Controls the learning process | You (before training) | `learning_rate`, `max_depth`, `n_estimators` |
| **Model Parameter** | Learned from data | The algorithm | weights, biases, split thresholds |

### 2. Search Strategies Compared
| Strategy | How It Works | Pros | Cons |
|----------|-------------|------|------|
| **Grid Search** | Exhaustive: every combination | Thorough | Exponential cost |
| **Random Search** | Random samples from space | Faster, often better than grid | No learning from past trials |
| **Bayesian Optimization** | Builds surrogate model of objective | Learns from past trials, efficient | More complex |
| **Hyperband / ASHA** | Aggressive early stopping of bad runs | Very fast at scale | Needs iterative training |

> **Rule of thumb:** Random search outperforms grid search when only 2–3 hyperparameters matter significantly. Bayesian wins for expensive training runs.

### 3. Optuna — Bayesian Optimization in Python
```python
import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

def objective(trial):
    n_estimators = trial.suggest_int('n_estimators', 50, 500)
    max_depth = trial.suggest_int('max_depth', 2, 20)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 20)
    min_samples_leaf = trial.suggest_int('min_samples_leaf', 1, 10)

    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        random_state=42
    )
    return cross_val_score(clf, X_train, y_train, cv=5, scoring='roc_auc').mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)
print("Best params:", study.best_params)
print("Best AUC:", study.best_value)
```

### 4. Optuna Visualizations
- `optuna.visualization.plot_optimization_history()` — Score vs. trial number
- `optuna.visualization.plot_param_importances()` — Which hyperparams matter most
- `optuna.visualization.plot_parallel_coordinate()` — All params vs. score
- `optuna.visualization.plot_contour()` — 2D contour for any param pair

### 5. MLflow — Experiment Tracking
```python
import mlflow

with mlflow.start_run(run_name="RF_optuna_best"):
    # Log hyperparameters
    mlflow.log_params(study.best_params)

    # Train final model
    model = RandomForestClassifier(**study.best_params, random_state=42)
    model.fit(X_train, y_train)

    # Log metrics
    mlflow.log_metric("train_auc", train_auc)
    mlflow.log_metric("val_auc", val_auc)
    mlflow.log_metric("test_auc", test_auc)

    # Log model artifact
    mlflow.sklearn.log_model(model, "model")
```

### 6. MLflow UI — Key Features
- Compare multiple runs side by side
- Filter runs by metric threshold
- Download logged artifacts
- Promote best model to **Model Registry**
- Stages: `None → Staging → Production → Archived`

### 7. Best Practices
- Never tune on the test set — use a held-out validation set or CV
- Use nested cross-validation for an unbiased performance estimate
- Log EVERYTHING — you will forget your best configuration
- Set `n_trials` based on budget, not intuition
- Use `study.best_trial` to retrieve the full best result

---

## 📊 Diagrams & Visuals Required

| # | Diagram | Type | Notebook Cell |
|---|---------|------|---------------|
| 1 | Grid vs. Random vs. Bayesian — 2D scatter comparison | Matplotlib scatter (3 subplots) | Cell 4 |
| 2 | Optuna optimization history (score vs. trial) | Line chart | Cell 7 |
| 3 | Parallel coordinates plot (params → score) | Matplotlib / plotly parallel coords | Cell 9 |
| 4 | MLflow experiment tracking architecture | Annotated diagram | Cell 11 |
| 5 | Hyperparameter importance bar chart | Bar chart from Optuna | Cell 10 |

---

## 🏋️ Activities

### Activity 1 — Run Optuna on Random Forest (20 min)
- Load Breast Cancer / Bank Churn dataset
- Define objective function with 4 hyperparameters
- Run 50 trials
- Print best params and best AUC

### Activity 2 — Log to MLflow (20 min)
- Log best trial results to MLflow
- Run `mlflow ui` and explore the experiment dashboard
- Compare at least 3 different trial runs

### Activity 3 — Parallel Coordinates Analysis (code)
- Build a parallel coordinates chart from the Optuna study results
- Color-code lines by score value (green = high, red = low)
- Identify the high-performance region of the search space

---

## 📝 Notebook Cell Plan

```
Cell 01 [MD]   → Session intro & objectives
Cell 02 [MD]   → Hyperparams vs. model params — table comparison
Cell 03 [MD]   → Search strategy comparison
Cell 04 [Code] → Search strategy visualization (3 subplots)
Cell 05 [MD]   → Optuna walkthrough
Cell 06 [Code] → Full Optuna study (50 trials on RF)
Cell 07 [Code] → Optimization history chart
Cell 08 [MD]   → MLflow setup and concepts
Cell 09 [Code] → Log best trial to MLflow
Cell 10 [Code] → Hyperparameter importance bar chart
Cell 11 [Code] → Parallel coordinates chart (matplotlib)
Cell 12 [MD]   → Key Takeaways + Quiz
```

---

## 📁 Files to Create

```
day1/04_hyperparameter_optim/
├── README.md
└── notebook.ipynb
```

---

## 📝 Key Takeaways
- Random search beats grid search because the important params are sparse
- Bayesian optimization learns from past trials — it gets smarter with each run
- Experiment tracking is to ML what version control is to software — use it always
- Tuning on the test set produces numbers that can't be trusted in production
- MLflow Model Registry formalizes the path from experiment to production

---

## ❓ Quiz Questions
1. What is the difference between a hyperparameter and a learned parameter?
2. Why does random search often outperform grid search?
3. What does `mlflow.log_metric()` do and when should you call it?
4. What is "overfitting the validation set" and how does nested CV prevent it?
5. Name 3 things you should always log during a model training experiment

---

## 📖 Further Reading
- [Optuna Documentation](https://optuna.readthedocs.io/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- Bergstra & Bengio (2012) — "Random Search for Hyper-Parameter Optimization"
- [Neptune.ai — Hyperparameter Optimization Guide](https://neptune.ai/blog/hyperparameter-optimization-strategies)
