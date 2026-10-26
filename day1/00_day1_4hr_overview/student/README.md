# Advanced Machine Learning in Production · Day 1

Everything you need for the 4-hour session. One case study, a **loan-default model**, goes through the whole production lifecycle:

```
choose approach → leakage-free pipeline → modular training → Optuna + MLflow
→ SHAP explanations → drift checks (PSI / KS) → FastAPI in Docker → dashboard + Azure ML
```

**Please complete steps 1–3 before the session.** It takes about 10 minutes, most of it downloading packages.

---

## What you need
| | |
|---|---|
| A laptop | Windows, macOS or Linux, with admin rights to install software |
| [Git](https://git-scm.com/downloads) | to download this repo |
| Python 3.11 | the setup script can install it for you (see step 2) |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | *optional*, used in Module 4. Without it you run the API with plain Python. |

## 1 · Download the materials
```bash
git clone https://github.com/MajedTuah/4Hour_Session.git
cd 4Hour_Session
```

## 2 · Create the Python environment (once)
**macOS / Linux** (Terminal):
```bash
bash setup/setup_mac_linux.sh
```

**Windows** (PowerShell):
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup\setup_windows.ps1
```

The script creates a `.venv` folder with Python 3.11 and every package from `requirements.txt`, then runs a check.
You want to see **"All set"** at the end.

> **No Python 3.11?** The easiest fix is to install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run the script again. It downloads Python 3.11 for you.
> macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh` · Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

<details>
<summary>Prefer to do it by hand?</summary>

```bash
python3.11 -m venv .venv                 # Windows: py -3.11 -m venv .venv
source .venv/bin/activate                # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python setup/check_env.py
```
</details>

## 3 · Start JupyterLab
Every time you work on the materials:
```bash
source .venv/bin/activate        # Windows: .venv\Scripts\activate
jupyter lab
```
Open **`notebooks/00_environment_check.ipynb`** and run it. Every line should show ✅.
Optional: if you have Docker, run `docker pull python:3.11-slim` now. It saves a slow download during Module 4.

## 4 · On the day: join the live session
The trainer shows a **QR code and a link** on the first slides. Open it on your laptop (or phone), pick a nickname,
and your screen follows the trainer's. The quizzes and games count toward the class leaderboard.
Keep JupyterLab open next to it for the hands-on parts.

---

## The day at a glance
| Time | Module | You will use |
|---|---|---|
| 0:00–0:15 | Welcome, ice breaker, environment check | `notebooks/00_environment_check.ipynb` |
| 0:15–1:10 | **1 · Trustworthy data and leakage-free pipelines** | `notebooks/01_trustworthy_data.ipynb` |
| 1:10–2:05 | **2 · Production training, tuning and tracking** | `notebooks/02_train_tune_track.ipynb`, `scripts/`, MLflow UI |
| 2:05–3:00 | **3 · Explainability and drift monitoring** | `notebooks/03_explain_and_monitor.ipynb` |
| 3:00–4:00 | **4 · Serving, monitoring and cloud** | `api/`, `notebooks/04_serve_and_monitor.ipynb`, `docs/WORKSHEET.md` |

Each notebook has **✏️ TODO** cells for you to complete and a **🏁 Checkpoint** cell that tells you when the module is done.
Solutions are shared after the session.

## What is in this repo
```
notebooks/        one notebook per module, plus course_utils.py (data generators and checks)
scripts/          the modular training pipeline (Module 2): config.yaml, main.py, data_loader.py, features.py, train.py, evaluate.py
api/              the FastAPI service and its Dockerfile (Module 4)
data/             sample data for the training scripts
docs/             WORKSHEET.md (activities and action plan) and CHEATSHEET.md (commands and thresholds)
slides/           the session deck: open slides/index.html in a browser to review it later
setup/            setup scripts and check_env.py
```
Generated while you work (ignored by Git): `artifacts/`, `mlruns/`, `reports/`.

## Commands you will run
Always from the repo root, with the environment active.

| What | Command |
|---|---|
| Train with the modular scripts | `python scripts/main.py --config scripts/config.yaml` |
| Open the MLflow UI | `mlflow ui` → http://127.0.0.1:5000 |
| Run the API with Docker | `cd api` → `docker build -t loan-api:1.0 .` → `docker run -d -p 8000:8000 --name loan-api loan-api:1.0` |
| Run the API without Docker | `cd api` → `uvicorn main:app --reload --port 8000` |
| Call the API | `curl -X POST http://localhost:8000/v1/predict -H "Content-Type: application/json" -d '{"age": 35, "income": 72000, "credit_score": 710}'` |
| API docs in the browser | http://localhost:8000/docs |
| Stop the container | `docker rm -f loan-api` |

On Windows PowerShell, use `curl.exe` instead of `curl`, or send the request from http://localhost:8000/docs.

## Troubleshooting
| Problem | Fix |
|---|---|
| `error: externally-managed-environment` | You ran `pip` outside the environment. Activate `.venv` first, or use the setup script. |
| `python: command not found` (macOS) | Use `python3`, or activate `.venv` (inside it, `python` works). |
| Packages fail to build on Python 3.13 or 3.14 | These versions need Python 3.11. Delete `.venv` and re-run the setup script (with uv installed). |
| `ModuleNotFoundError: No module named 'course_utils'` | Open the notebooks from inside the `notebooks/` folder in JupyterLab. |
| Jupyter uses the wrong Python | Start `jupyter lab` from the activated `.venv`. |
| Port 8000 already in use | Use `-p 8001:8000` (Docker) or `--port 8001` (uvicorn), and set `API = "http://localhost:8001"` in notebook 04. |
| Docker: "Cannot connect to the Docker daemon" | Start Docker Desktop and wait until it says it is running. |
| Corporate laptop blocks installs | Tell the trainer before the session. You can pair with a neighbour for the hands-on parts. |
