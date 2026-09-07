# 🚀 Session 10 — Cloud Training Jobs & Experiment Tracking

> **Day 2 | 11:00 AM – 12:00 PM | 60 minutes**  
> **Focus:** Submitting jobs to Azure ML, MLflow tracking, Sweep Jobs, and Model Registry

---

## 🎯 Learning Objectives

By the end of this session, you will be able to:

1. **Submit a training job** to an Azure ML Compute Cluster using SDK v2
2. **Track experiments, metrics, and artifacts** natively using MLflow inside Azure ML
3. **Run cloud-scale hyperparameter tuning** with Sweep Jobs (Bayesian + Bandit early termination)
4. **Compare training runs** in Azure ML Studio's Experiments dashboard
5. **Register the best model** to Azure ML Model Registry with tags and versioning

---

## 🏗️ Architecture Overview

```
Your Machine (SDK v2)
        │
        ▼
 Azure ML Workspace
        │
        ├── Jobs ──────────── Command Job   → Single-script training
        │                  ├── Pipeline Job → Multi-step (prep → train → eval)
        │                  ├── Sweep Job   → Cloud-scale HPO (30 parallel trials)
        │                  └── AutoML Job  → Automated model selection
        │
        ├── Environments ─── Docker image + Conda deps (versioned, cached)
        │
        ├── Compute ──────── Compute Cluster (auto-scales 0 → N nodes)
        │
        ├── MLflow Tracking ─ params / metrics / artifacts per run
        │
        └── Model Registry ── Experiment → Staging → Production
```

---

## 🧠 Core Concepts

### 1. Azure ML Job Types

| Job Type | Best For | Key Property |
|----------|----------|-------------|
| **Command Job** | Single-script training run | Simple, fast to configure |
| **Pipeline Job** | Multi-step workflows | DAG of components; reusable |
| **Sweep Job** | Hyperparameter optimization at scale | Parallel trials, early termination |
| **AutoML Job** | Automated algorithm selection | No-code ML experimentation |

### 2. The Training Job Lifecycle

```
[1] Define Job (SDK v2)
       ↓
[2] Upload code snapshot → Azure Blob Storage
       ↓
[3] Provision compute node (auto-scale)
       ↓
[4] Pull Docker environment image (ACR)
       ↓
[5] Execute training script
       ↓
[6] MLflow logs metrics → Azure ML Tracking Store
       ↓
[7] Save outputs (model artifacts) → Blob Storage
       ↓
[8] Register model → Model Registry
```

### 3. MLflow in Azure ML — Two Modes

| Mode | Code | Best For |
|------|------|---------|
| **Auto-logging** | `mlflow.autolog()` | Quick start — sklearn, XGBoost, PyTorch |
| **Manual logging** | `mlflow.log_param()` / `mlflow.log_metric()` | Full control over what you log |

```python
# Auto-logging — single line, captures everything
mlflow.autolog()

# Manual — fine-grained control
with mlflow.start_run():
    mlflow.log_param("learning_rate", lr)
    mlflow.log_metric("val_auc", val_auc, step=epoch)
    mlflow.log_figure(confusion_matrix_fig, "confusion_matrix.png")
    mlflow.sklearn.log_model(model, "model")
```

### 4. Sweep Job — Cloud-Scale HPO

Sweep Jobs run **many trials in parallel** on cloud compute, with:
- **Bayesian sampling** — learns from previous trials (smarter than random)
- **Bandit early termination** — kills poor-performing trials fast

```python
sweep_job = command_job.sweep(
    sampling_algorithm="bayesian",
    primary_metric="val_auc",
    goal="Maximize",
    search_space={
        "learning_rate": Uniform(0.001, 0.1),
        "max_depth": Choice([3, 5, 7, 10]),
        "n_estimators": Choice([100, 200, 300, 500])
    },
    limits={"max_total_trials": 30, "max_concurrent_trials": 5}
)
```

### 5. Model Registry

```
Model Registry is your single source of truth for production models.

Version history → Who trained it, when, with what metrics
Tags           → val_auc, framework, dataset version
Promotion path → None → Staging → Production (via label)
```

```python
model = Model(
    path=f"azureml://jobs/{job_name}/outputs/model",
    name="credit-default-classifier",
    type=AssetTypes.MLFLOW_MODEL,
    tags={"val_auc": "0.923", "framework": "sklearn"}
)
ml_client.models.create_or_update(model)
```

---

## 📁 Files in This Session

```
day2/02_cloud_training_experiment/
├── README.md                 ← You are here
├── notebook.ipynb            ← Main exercise notebook (14 cells)
└── scripts/
    ├── train.py              ← AzureML-compatible training script
    ├── environment.yml       ← Conda dependency spec
    └── job_config.yml        ← Job YAML (alternative to Python SDK)
```

---

## 🛠️ Prerequisites

### Azure Access
| Requirement | How to Check |
|-------------|-------------|
| Azure Subscription | `az account show` |
| Azure ML Workspace | `az ml workspace show -n <name> -g <rg>` |
| Compute Cluster `cpu-cluster` | Azure ML Studio → Compute |
| Registered data asset `credit_data:1` | Azure ML Studio → Data |

### Python Packages
```bash
pip install azure-ai-ml==1.12.0 mlflow==2.7.0 scikit-learn pandas numpy matplotlib
```

> **No Azure access?** The notebook includes a full **simulation mode** — all outputs, charts, and registry operations are mocked locally.

---

## 📋 Pre-Session Checklist

- [ ] Python 3.10+ installed
- [ ] `pip install azure-ai-ml mlflow` completed
- [ ] Azure CLI authenticated: `az login`
- [ ] Workspace config ready (`MLClient.from_config()` or env vars)
- [ ] Compute cluster `cpu-cluster` exists (min 0 nodes, max 4 nodes, Standard_DS3_v2)
- [ ] Reviewed the [Azure ML Job Types overview](https://learn.microsoft.com/en-us/azure/machine-learning/concept-ml-pipelines)

---

## 🏋️ Activities

### Activity 1 — Submit Your First Cloud Training Job (25 min)
1. Open `notebook.ipynb`, run cells 1–6
2. Wrap `train.py` as an Azure ML Command Job
3. Submit to `cpu-cluster` using SDK v2
4. Watch the job in Azure ML Studio → **Jobs** tab
5. Verify metrics appear in **Experiments** dashboard

### Activity 2 — Run a Sweep Job (20 min)
1. Continue from cells 9–11
2. Convert Command Job to Sweep Job (Bayesian, 10 trials)
3. Set `max_concurrent_trials=3` for budget control
4. Identify the best trial in Studio
5. Promote the winning model to **Model Registry**

### Activity 3 — Compare Runs in Studio (10 min)
1. Navigate to Azure ML Studio → **Jobs** → your experiment
2. Select 3+ runs with Ctrl+Click → click **Compare**
3. View parallel coordinates + metric charts
4. Sort by `val_auc` descending
5. Register the best model directly from Studio UI

---

## 📝 Key Takeaways

| Concept | Why It Matters |
|---------|---------------|
| Cloud training | Eliminates local resource limits — 30 parallel trials while you sleep |
| `mlflow.autolog()` | Fastest path to full experiment tracking — zero extra code |
| Sweep Jobs | Optuna-at-cloud-scale with auto early termination; cost-efficient |
| Model Registry | Formalizes `experiment → staging → production` promotion path |
| Run tagging | Always tag models with metrics — enables traceability across versions |

---

## ❓ Self-Check Quiz

1. What is the key difference between a **Command Job** and a **Sweep Job**?
2. What does `mlflow.autolog()` capture automatically for a scikit-learn model?
3. Why does early termination policy (Bandit Policy) save money in Sweep Jobs?
4. What does it mean to "register" a model in Azure ML Model Registry?
5. If `max_concurrent_trials=5` and `max_total_trials=30`, how many "rounds" will the sweep run?

---

## 📖 Further Reading

- [Azure ML: Submit a Training Job](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-train-model)
- [Hyperparameter Tuning with Sweep Jobs](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-tune-hyperparameters)
- [MLflow on Azure ML](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-mlflow-cli-runs)
- [Azure ML Model Registry](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-models)
