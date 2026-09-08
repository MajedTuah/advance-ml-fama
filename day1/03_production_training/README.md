# ⚙️ Session 03 — Production Model Training

> **Day 1 | 11:00 AM – 12:00 PM | Duration: 60 minutes**

---

This folder demonstrates a compact, production-style training pipeline implemented as small, testable scripts. The example is intentionally minimal so you can focus on the architecture and reproducibility aspects.

## What this folder contains

- `scripts/main.py` — orchestration script to run the end-to-end workflow
- `scripts/train.py` — model training and save helpers
- `scripts/evaluate.py` — compute and save evaluation metrics
- `scripts/features.py` — feature engineering / preprocessing
- `scripts/data_loader.py` — dataset creation/loading and train/test split
- `scripts/config.yaml` — configuration for the run (data paths, model params, artifact paths)
- `notebook.ipynb` — (optional) notebook version used to teach the same pattern interactively

---

## Goals & learning objectives

By the end of this session learners will be able to:
- Explain how configuration, logging and artifact management enable reproducible training runs
- Read a small pipeline and map each step to production responsibilities (ingest, features, train, evaluate, persist)
- Run the end-to-end script and inspect generated artifacts (model file, metrics, logs)

---

## Quick setup (recommended)

From the repository root create and activate a virtual environment and install dependencies:

```bash
# If `python` is not found, try `py -m venv .venv` on Windows
python -m venv .venv

# Windows PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

# Windows Command Prompt
# .\.venv\Scripts\activate.bat

# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

If you prefer a lightweight install for this folder you can install the minimum packages used here:

```bash
pip install pandas scikit-learn joblib pyyaml
```

---

## Run the pipeline (example)

Run the orchestrator from the repo root:

```bash
python day1/03_production_training/scripts/main.py --config day1/03_production_training/scripts/config.yaml
```

Default behaviour:
- If the CSV at `data.path` does not exist the loader will create a small synthetic dataset.
- Outputs are written to `artifacts/` (model.joblib, metrics.json, training.log).

Example artifacts to check after a run:
- `artifacts/model.joblib` — trained model persisted with `joblib`
- `artifacts/metrics.json` — JSON with accuracy, precision, recall, f1 and full classification report
- `artifacts/training.log` — the run log (INFO level)

---

## `scripts/config.yaml` — fields explained

- `data.path`: CSV path for dataset (relative to repo root). If missing the loader will create a synthetic CSV.
- `data.target_column`: name of the outcome column (e.g., `churn`).
- `data.test_size`: float (0–1) fraction used for the test set.
- `data.random_state`: RNG seed for reproducibility.
- `model.type`: currently supports `logistic_regression`.
- `model.max_iter`: hyperparameter for `LogisticRegression`.
- `paths.model_path`, `paths.report_path`, `paths.log_path`: where artifacts and logs are written.

Edit these values to demonstrate repeatable experiments and to teach configuration-driven workflows.

---

## File responsibilities (walk students through these)

- `data_loader.py`: ensures the dataset exists (creates synthetic data) and returns train/test splits — shows data acquisition and validation.
- `features.py`: demonstrates simple but realistic preprocessing (imputation and one-hot encoding) — shows separation of feature engineering.
- `train.py`: encapsulates model selection and fitting; `save_model` persists the model.
- `evaluate.py`: computes standard classification metrics and writes a JSON report.
- `main.py`: wires everything together and configures logging; this is the user-facing CLI for reproducible runs.

---

## Teaching notes and demo flow

1. Open `scripts/config.yaml` and explain each section (data, model, paths).
2. Show `data_loader.py` and run it in a REPL to inspect the generated dataset columns.
3. Run `python scripts/main.py` once to produce `artifacts/` and show the saved model + metrics.
4. Change a config value (e.g., `test_size` or `max_iter`) and re-run to show reproducibility and impact on metrics.
5. Optional: ask students to implement a second model (RandomForest) in `train.py` and compare.

---

## Troubleshooting

- If you see `ModuleNotFoundError`, install missing packages: `pip install -r requirements.txt` or `pip install <package>`.
- If `target_column` not found in CSV, open the CSV (path in `config.yaml`) to inspect headers.
- Logs are written to the path set in `paths.log_path` — tail that file to follow progress.

---

## Suggested follow-ups (I can add these)
- `run_demo.bat` and `run_demo.sh` wrappers for Windows/macOS-Linux.
- A short `explain.md` with talking points and slide notes for instructors.
- Add example contents of `artifacts/` committed to the repo so students can inspect outputs without running.

If you want, I can add the run wrappers and a 1-page instructor cheat-sheet next — which would you prefer?
