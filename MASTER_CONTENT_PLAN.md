# 📚 MASTER CONTENT PLAN — Advanced ML/FAMA Bootcamp
> Last Updated: 2026-09-01 | Structure: Topic-based (one .md per topic)

---

## 🗂️ Topic Index — All Sessions

Each topic has its own dedicated `.md` file inside `topics/`. Open any topic independently to add, edit, or remove content without affecting others.

| # | Topic File | Day | Time | Status |
|---|-----------|-----|------|--------|
| 01 | [01_ai_ml_dl_llm_landscape.md](topics/01_ai_ml_dl_llm_landscape.md) | Day 1 | 9–10am | 🔲 Pending |
| 02 | [02_data_quality_leakage.md](topics/02_data_quality_leakage.md) | Day 1 | 10–11am | 🔲 Pending |
| 03 | [03_production_model_training.md](topics/03_production_model_training.md) | Day 1 | 11am–12pm | 🔲 Pending |
| 04 | [04_hyperparameter_optimization.md](topics/04_hyperparameter_optimization.md) | Day 1 | 2–3pm | 🔲 Pending |
| 05 | [05_explainability_xai.md](topics/05_explainability_xai.md) | Day 1 | 4–5pm | 🔲 Pending |
| 06 | [06_data_drift_anomaly_detection.md](topics/06_data_drift_anomaly_detection.md) | Day 1 | 5–6pm | 🔲 Pending |
| 07 | [07_api_serving_containerization.md](topics/07_api_serving_containerization.md) | Day 1 | 8–9pm | 🔲 Pending |
| 08 | [08_mlops_dashboard.md](topics/08_mlops_dashboard.md) | Day 1 | 9–10pm | 🔲 Pending |
| 09 | [09_azure_fundamentals_workspace.md](topics/09_azure_fundamentals_workspace.md) | Day 2 | 9–10am | 🔲 Pending |
| 10 | [10_cloud_training_experiment_tracking.md](topics/10_cloud_training_experiment_tracking.md) | Day 2 | 11am–12pm | 🔲 Pending |

---

## 📁 Repository Structure

```
advance-ml-fama/
├── MASTER_CONTENT_PLAN.md       ← You are here (index + conventions)
├── README.md                    ← Public-facing participant syllabus
│
├── topics/                      ← ONE .md per topic (add/remove freely)
│   ├── 01_ai_ml_dl_llm_landscape.md
│   ├── 02_data_quality_leakage.md
│   ├── 03_production_model_training.md
│   ├── 04_hyperparameter_optimization.md
│   ├── 05_explainability_xai.md
│   ├── 06_data_drift_anomaly_detection.md
│   ├── 07_api_serving_containerization.md
│   ├── 08_mlops_dashboard.md
│   ├── 09_azure_fundamentals_workspace.md
│   └── 10_cloud_training_experiment_tracking.md
│
├── day1/                        ← Actual session folders (built from topic briefs)
│   ├── 01_ai_ml_dl_llm_landscape/
│   ├── 02_data_quality_leakage/
│   ├── 03_production_training/
│   ├── 04_hyperparameter_optim/
│   ├── 05_explainability_xai/
│   ├── 06_data_drift_anomaly/
│   ├── 07_api_serving_containers/
│   └── 08_mlops_dashboard/
│
└── day2/
    ├── 01_azure_fundamentals/
    └── 02_cloud_training_experiment/
```

---

## 📐 Per-Session Deliverables Checklist

Every session folder (inside `day1/` or `day2/`) must contain:
- [ ] `README.md` — Participant-facing guide (objectives, concepts, activities)
- [ ] `notebook.ipynb` — Hands-on Jupyter notebook with charts
- [ ] At least **2 activity exercises** per session
- [ ] At least **1 diagram/graph** per session
- [ ] A **Key Takeaways** section
- [ ] A **Quiz / Check Your Understanding** section (3–5 questions)

---

## 📝 Topic File Structure Convention

Each file in `topics/` follows this template:

```markdown
# [Emoji] Topic XX — [Title]
> Schedule, Folder, Status

## 🎯 Learning Objectives
## 🧠 Core Concepts
## 📊 Diagrams & Visuals Required   ← what charts to generate in notebook
## 🏋️ Activities                   ← hands-on exercises
## 📝 Notebook Cell Plan            ← exact cell-by-cell plan
## 📁 Files to Create               ← folder + file list
## 📝 Key Takeaways
## ❓ Quiz Questions
## 📖 Further Reading
```

---

## 🎨 Design Conventions

- **Charts:** `matplotlib` / `seaborn` embedded in notebooks
- **Architecture diagrams:** Mermaid in README + pre-rendered PNG in `assets/`
- **Code style:** PEP8 with `# EXPLAIN:` inline comments for learner clarity
- **Notebook flow:** Markdown intro → Code → Output → Markdown explanation
- **Color palette:** `#4A90D9` (primary blue), `#E94B4B` (accent red), `#2ECC71` (success green)

---

## 📖 Shared Glossary

| Term | Definition |
|------|-----------|
| Feature | An individual measurable input variable to a model |
| Label/Target | The output variable a model tries to predict |
| Pipeline | End-to-end sequence of data processing + modeling steps |
| Overfitting | Model memorizes training noise; fails on new data |
| Leakage | Future/test information contaminating model training |
| MLOps | DevOps practices applied to ML lifecycle |
| Inference | Using a trained model to make predictions on new data |
| Hyperparameter | Configuration set before training (not learned from data) |
| Drift | Statistical shift in data or concept distribution over time |
| Explainability | Ability to understand and communicate why a model predicted a given output |
| PSI | Population Stability Index — measures feature distribution shift |
| SHAP | SHapley Additive exPlanations — game-theory-based feature attribution |
| LIME | Local Interpretable Model-agnostic Explanations |
| Endpoint | A deployed model accessible via an API URL |

---

## 🗓️ Overview

| Day | Session | Time | Status |
|-----|---------|------|--------|
| Day 1 | AI, ML, DL & LLM Landscape | 9am–10am | 🔲 Pending |
| Day 1 | Data Quality & Leakage-Free Pipeline | 10am–11am | 🔲 Pending |
| Day 1 | Production Model Training & Modular Scripting | 11am–12pm | 🔲 Pending |
| Day 1 | Hyperparameter Optimization & Experiment Tracking | 2pm–3pm | 🔲 Pending |
| Day 1 | Explainability AI (XAI) for Biz Decisions | 4pm–5pm | 🔲 Pending |
| Day 1 | Data Drift & Unsupervised Anomaly Detection (MLOps Guardrail) | 5pm–6pm | 🔲 Pending |
| Day 1 | API Serving & Containerized Inference Concepts | 8pm–9pm | 🔲 Pending |
| Day 1 | MLOps Dashboard | 9pm–10pm | 🔲 Pending |
| Day 2 | Azure Fundamentals & Azure ML Workspace | 9am–10am | 🔲 Pending |
| Day 2 | Cloud Training Jobs & Experiment Tracking | 11am–12pm | 🔲 Pending |

---

## 📁 Folder Structure

```
advance-ml-fama/
├── MASTER_CONTENT_PLAN.md          ← You are here
├── README.md                        ← Public-facing syllabus
├── assets/                          ← Shared diagrams
│
├── day1/
│   ├── DAY1_CONTENT_BRIEF.md        ← Full day 1 content outline
│   ├── 01_ai_ml_dl_llm_landscape/
│   ├── 02_data_quality_leakage/
│   ├── 03_production_training/
│   ├── 04_hyperparameter_optim/
│   ├── 05_explainability_xai/
│   ├── 06_data_drift_anomaly/
│   ├── 07_api_serving_containers/
│   └── 08_mlops_dashboard/
│
└── day2/
    ├── DAY2_CONTENT_BRIEF.md        ← Full day 2 content outline
    ├── 01_azure_fundamentals/
    └── 02_cloud_training_experiment/
```

---

## 📐 Per-Session Deliverables Checklist

Every session must have:
- [ ] `README.md` — Objectives, concepts, timeline, activities, further reading
- [ ] `notebook.ipynb` — Hands-on Jupyter notebook with charts
- [ ] At least **2 activity exercises** per session
- [ ] At least **1 diagram/graph** per session
- [ ] A "Key Takeaways" section
- [ ] A "Quiz / Check Your Understanding" section (3–5 questions)

---

## 🎨 Design Conventions

- All charts → `matplotlib` / `seaborn` embedded in notebooks
- All architecture diagrams → described in Mermaid (README) + pre-rendered PNG (assets/)
- Code style → PEP8, with inline `# EXPLAIN:` comments for clarity
- Notebook structure → Markdown → Code → Output → Markdown explanation
- Color palette for charts → `#4A90D9` (primary), `#E94B4B` (accent), `#2ECC71` (success)

---

## 📖 Shared Glossary Terms (to appear in all sessions)

| Term | Definition |
|------|-----------|
| Feature | An individual measurable input to a model |
| Label/Target | The output variable a model tries to predict |
| Pipeline | An end-to-end sequence of data processing + modeling steps |
| Overfitting | Model learns noise in training data, fails on new data |
| Leakage | Future/test information contaminating training |
| MLOps | DevOps practices applied to ML lifecycle |
| Inference | Using a trained model to make predictions on new data |
| Hyperparameter | Settings tuned before training (not learned from data) |
| Drift | Statistical shift in data distribution over time |
| Explainability | Ability to understand why a model made a prediction |
