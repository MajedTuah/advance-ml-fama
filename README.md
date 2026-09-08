# advance-ml-fama — Study materials for AI/ML course

This repository contains lesson materials, notebooks and exercises for an introductory AI/ML workshop.

## First step for students

Before opening the notebooks or installing packages, clone the course repository from the GitHub `students` branch:

```bash
git clone -b students https://github.com/MajedTuah/advance-ml-fama.git
cd advance-ml-fama
```

If you already cloned the repo, run:

```bash
git fetch origin students
git checkout students
```

A reference guide is included in [CLONE_STUDENTS_BRANCH.md](CLONE_STUDENTS_BRANCH.md).

Contents
- `day1/01_ai_ml_dl_llm_landscape/` — Session 01: AI, ML, DL & LLM Landscape (notebooks, data, slides)

Quickstart
1. Install Python 3.11 and create a matching virtual environment (recommended):

```bash
# On Windows, install the correct interpreter if needed
py install 3.11

# Create a Python 3.11 virtual environment
py -3.11 -m venv .venv

# Windows PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

# Windows Command Prompt
# .\.venv\Scripts\activate.bat

python -m pip install -U pip setuptools wheel
pip install -r  advance-ml-fama/requirements.txt
```

2. Launch Jupyter Lab / Notebook:

```bash
jupyter lab
# or
jupyter notebook
```

3. Open the main notebook for session 1:
`day1/01_ai_ml_dl_llm_landscape/ai_ml_landscape.ipynb`

Note: The course requirements in this repository are tested with Python 3.11.
If the `py` launcher is missing or Python 3.11 is not installed, run:

```bash
py install 3.11
```

Then recreate the virtual environment with `py -3.11 -m venv .venv`.

Binder / Colab
- Add a `binder/` or `runtime.txt` if you want reproducible cloud launches. You can also add a Colab link for the notebook.

Contributing
- Add issues for improvements, submit PRs for fixes or extra exercises.

Requirements
- See `requirements.txt` for the exact Python packages used in the notebooks.

---

Happy teaching! If you want, I can add Binder/Colab badges and a GitHub Actions workflow next.