# 🚀 Topic 10 — Cloud Training Jobs & Experiment Tracking
> **Schedule:** Day 2 | 11:00 AM – 12:00 PM | Duration: 60 min
> **Folder:** `day2/02_cloud_training_experiment/`
> **Status:** 🔲 Pending Build

---

## 🎯 Learning Objectives
1. Submit a training job to Azure ML Compute Cluster using SDK v2
2. Track experiments, metrics, and artifacts natively in Azure ML
3. Compare training runs in Azure ML Studio
4. Register the best model to Azure ML Model Registry

---

## 🧠 Core Concepts

### 1. Azure ML Job Types
| Job Type | Use Case | When to Use |
|----------|----------|-------------|
| **Command Job** | Single-script training | Basic training run |
| **Pipeline Job** | Multi-step workflows | Data prep → train → evaluate |
| **Sweep Job** | Hyperparameter tuning | Automated HPO at scale |
| **AutoML Job** | Automated model selection | When you want Azure to choose the algorithm |

### 2. Submitting a Command Job (SDK v2)
```python
from azure.ai.ml import MLClient, command
from azure.ai.ml.entities import Environment, AmlCompute
from azure.ai.ml import Input, Output
from azure.ai.ml.constants import AssetTypes

# Define the training job
job = command(
    code="./scripts",                          # Local code to upload
    command="python train.py --data ${{inputs.training_data}} --learning-rate 0.01 --epochs 50",
    inputs={
        "training_data": Input(
            type=AssetTypes.URI_FILE,
            path="azureml:credit_data:1"      # Registered Data Asset
        )
    },
    outputs={
        "model": Output(type=AssetTypes.MLFLOW_MODEL)
    },
    environment="azureml:sklearn-env:1",       # Registered Environment
    compute="cpu-cluster",                     # Compute target
    display_name="credit-model-training-v1",
    experiment_name="credit-default-model",
    tags={"framework": "sklearn", "version": "1.0"}
)

# Submit
returned_job = ml_client.jobs.create_or_update(job)
print("Job URL:", returned_job.studio_url)
```

### 3. Logging Metrics from Training Script
```python
# Inside train.py — running on Azure ML Compute
import mlflow

mlflow.autolog()  # Automatically logs sklearn params + metrics

# Or manual logging:
with mlflow.start_run():
    mlflow.log_param("learning_rate", args.learning_rate)
    mlflow.log_param("max_depth", args.max_depth)

    model.fit(X_train, y_train)

    train_auc = roc_auc_score(y_train, model.predict_proba(X_train)[:, 1])
    val_auc = roc_auc_score(y_val, model.predict_proba(X_val)[:, 1])

    mlflow.log_metric("train_auc", train_auc)
    mlflow.log_metric("val_auc", val_auc)

    # Log confusion matrix as artifact
    mlflow.log_figure(fig_confusion, "confusion_matrix.png")

    # Log model
    mlflow.sklearn.log_model(model, "model")
```

### 4. Azure ML Environments
```python
from azure.ai.ml.entities import Environment

# Create custom environment from conda YAML
env = Environment(
    name="credit-model-env",
    version="1",
    description="Environment for credit default model",
    conda_file="environment.yml",
    image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest"
)
ml_client.environments.create_or_update(env)
```

```yaml
# environment.yml
name: credit-model-env
dependencies:
  - python=3.10
  - pip:
    - scikit-learn==1.3.0
    - pandas==2.0.3
    - numpy==1.24.3
    - mlflow==2.7.0
    - shap==0.43.0
    - optuna==3.3.0
```

### 5. Sweep Job — Cloud-Scale Hyperparameter Tuning
```python
from azure.ai.ml.sweep import Choice, Uniform, BanditPolicy

# Define sweep
sweep_job = command_job.sweep(
    sampling_algorithm="bayesian",
    primary_metric="val_auc",
    goal="Maximize",
    search_space={
        "learning_rate": Uniform(min_value=0.001, max_value=0.1),
        "max_depth": Choice(values=[3, 5, 7, 10]),
        "n_estimators": Choice(values=[100, 200, 300, 500])
    },
    limits={
        "max_total_trials": 30,
        "max_concurrent_trials": 5,
        "timeout": 7200   # 2 hours
    },
    early_termination_policy=BanditPolicy(
        slack_factor=0.1,
        evaluation_interval=1
    )
)

returned_sweep_job = ml_client.jobs.create_or_update(sweep_job)
```

### 6. Model Registry
```python
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes

# Register the best model from a completed job
model = Model(
    path=f"azureml://jobs/{returned_job.name}/outputs/model",
    name="credit-default-classifier",
    description="Credit default prediction model v1",
    type=AssetTypes.MLFLOW_MODEL,
    tags={"val_auc": "0.923", "framework": "sklearn"}
)
registered_model = ml_client.models.create_or_update(model)
print(f"Registered: {registered_model.name} v{registered_model.version}")
```

### 7. Comparing Runs in Studio
- Navigate to **Azure ML Studio → Jobs → Experiment**
- Select multiple runs → Compare
- Sort by `val_auc`, filter by `framework = sklearn`
- View parallel coordinates chart, metric comparison chart
- Promote best run's model to Registry directly from UI

---

## 📊 Diagrams & Visuals Required

| # | Diagram | Type | Notebook Cell |
|---|---------|------|---------------|
| 1 | Azure ML job lifecycle (submit → compute → log → register) | Annotated flowchart | Cell 4 |
| 2 | Sweep job parallel coordinates (hyperparams → val_auc) | Matplotlib parallel coords | Cell 8 |
| 3 | Experiment comparison chart (multiple runs) | Multi-line chart | Cell 10 |
| 4 | Model registry lifecycle (None → Staging → Production) | State transition diagram | Cell 12 |

---

## 🏋️ Activities

### Activity 1 — Submit Your First Cloud Training Job (25 min)
- Wrap `train.py` from Session 3 as an Azure ML Command Job
- Submit to `cpu-cluster`
- Monitor in Azure ML Studio (Jobs tab)
- Confirm metrics appear in the Experiments dashboard

### Activity 2 — Run a Sweep Job (20 min)
- Convert Command Job to Sweep Job
- Define search space for `n_estimators`, `max_depth`, `min_samples_split`
- Run 10 trials (budget-limited)
- Identify and promote the best trial to Model Registry

### Activity 3 — Compare Runs in Studio (10 min)
- Select 3+ runs in Azure ML Studio
- Use the built-in comparison view
- Export the comparison chart as PNG

---

## 📝 Notebook Cell Plan

```
Cell 01 [MD]   → Session intro: from local to cloud training
Cell 02 [MD]   → Azure ML Job types overview
Cell 03 [Code] → Job lifecycle diagram
Cell 04 [Code] → Define + submit Command Job (SDK v2)
Cell 05 [MD]   → Logging metrics with mlflow.autolog() vs. manual
Cell 06 [Code] → Training script with full metric logging
Cell 07 [MD]   → Azure ML Environments — why they matter
Cell 08 [Code] → Create and register custom environment
Cell 09 [MD]   → Sweep Job for HPO at scale
Cell 10 [Code] → Define + submit Sweep Job
Cell 11 [Code] → Parallel coordinates chart from sweep results
Cell 12 [MD]   → Model Registry concepts
Cell 13 [Code] → Register best model + state transition diagram
Cell 14 [MD]   → Key Takeaways + Quiz
```

---

## 📁 Files to Create

```
day2/02_cloud_training_experiment/
├── README.md
├── notebook.ipynb
└── scripts/
    ├── train.py          ← AzureML-compatible training script
    ├── environment.yml   ← Conda environment spec
    └── job_config.yml    ← Job YAML definition (alternative to SDK)
```

> ⚠️ **Note:** Requires Azure ML Workspace access. Use `ml_client_mock.py` for offline exploration if no subscription is available.

---

## 📝 Key Takeaways
- Cloud training eliminates local resource constraints — run 30 parallel trials while you sleep
- `mlflow.autolog()` is the fastest way to start tracking in Azure ML
- Sweep Jobs are Optuna-at-cloud-scale with early termination — extremely cost-efficient
- Model Registry formalizes the promotion path: experiment → staging → production
- Always tag your registered models with performance metrics for traceability

---

## ❓ Quiz Questions
1. What is the difference between a Command Job and a Sweep Job in Azure ML?
2. What does `mlflow.autolog()` capture automatically for sklearn models?
3. Why is early termination policy important in a Sweep Job?
4. What does it mean to "register" a model in Azure ML Model Registry?
5. How does Azure ML's Sweep Job differ from running Optuna locally?

---

## 📖 Further Reading
- [Azure ML Command Job Tutorial](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-train-model)
- [Azure ML Sweep Job — Hyperparameter Tuning](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-tune-hyperparameters)
- [Azure ML Model Registry](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-models)
- [MLflow on Azure ML](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-mlflow-cli-runs)
