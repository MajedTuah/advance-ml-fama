"""Check that this laptop is ready for Day 1. Run from the repo root:

    python setup/check_env.py
"""

import importlib
import shutil
import socket
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGES = ["numpy", "pandas", "sklearn", "matplotlib", "seaborn", "optuna", "mlflow", "shap",
            "fastapi", "uvicorn", "httpx", "yaml", "joblib", "jupyterlab"]

problems = 0


def report(ok, text, fix=""):
    global problems
    print(("✅ " if ok else "❌ ") + text + ("" if ok or not fix else f"\n     → {fix}"))
    problems += not ok


report(sys.version_info[:2] in ((3, 11), (3, 12)), f"Python {sys.version.split()[0]}",
       "use Python 3.11: re-run the setup script, which creates .venv with the right version")
report(sys.prefix != sys.base_prefix, "running inside a virtual environment",
       "activate it first: macOS/Linux `source .venv/bin/activate`, Windows `.venv\\Scripts\\activate`")

for name in PACKAGES:
    try:
        mod = importlib.import_module(name)
        report(True, f"{name:<11} {getattr(mod, '__version__', '')}")
    except Exception as exc:  # report every package, not just the first failure
        report(False, f"{name:<11} {type(exc).__name__}: {exc}", "pip install -r requirements.txt")

for folder in ["notebooks", "scripts", "api", "data"]:
    report((ROOT / folder).is_dir(), f"folder {folder}/ present", "run this from inside the cloned repo")

if shutil.which("docker"):
    print("✅ docker installed (start Docker Desktop before Module 4)")
else:
    print("⚠️  docker not found. Optional: Module 4 can run the API with uvicorn instead.")

with socket.socket() as s:
    try:
        s.bind(("127.0.0.1", 8000))
        print("✅ port 8000 is free for the API")
    except OSError:
        print("⚠️  port 8000 is busy. In Module 4 use port 8001 instead.")

print("\nAll set. Start JupyterLab with:  jupyter lab" if not problems else f"\n{problems} problem(s) above. Fix them or ask the trainer.")
sys.exit(1 if problems else 0)
