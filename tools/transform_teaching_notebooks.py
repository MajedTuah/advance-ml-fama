import json
import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(sys.argv[1])


def text_from_source(source):
    if isinstance(source, list):
        return "".join(source)
    return source or ""


def topic_for(path, notebook_text):
    match = re.search(r"#\s+[^\n]*Topic\s+\d+\s+[^\n]*", notebook_text, re.I)
    if match:
        return match.group(0).lstrip("# ").strip()
    return path.parent.name.replace("_", " ").title()


def heading_before(cells, index):
    for cell in reversed(cells[:index]):
        if cell.get("cell_type") == "markdown":
            text = text_from_source(cell.get("source", []))
            headings = re.findall(r"^#{1,4}\s+(.+)$", text, re.M)
            if headings:
                return headings[-1].strip()
    return "the current notebook section"


def classify(source, section, topic):
    text = source.lower()
    labels = []
    if "shap" in text or "lime" in text:
        labels.append("model explanations and feature attribution")
    if "optuna" in text or "hyperparameter" in text or "randomforest" in text:
        labels.append("hyperparameter search and experiment comparison")
    if "isolationforest" in text or "psi" in text or "drift" in text:
        labels.append("drift or anomaly monitoring")
    if "fastapi" in text or "docker" in text or "uvicorn" in text:
        labels.append("API serving or container deployment")
    if "azure" in text or "ml_client" in text or "command(" in text or "sweep" in text:
        labels.append("an Azure ML cloud job or asset workflow")
    if "mlflow" in text or "joblib" in text or "artifact" in text:
        labels.append("production training, tracking, or artifact management")
    if "timeseriessplit" in text or "leak" in text or "target" in text:
        labels.append("leakage-aware validation")
    if "classification_report" in text or "train_test_split" in text or ".fit(" in text:
        labels.append("model training and evaluation")
    if "matplotlib" in text or "seaborn" in text or "patches" in text or "plt." in text:
        labels.append("a visual analysis or architecture diagram")
    if not labels:
        labels.append("the analysis or implementation in this section")
    return labels


def context_items(source, section, topic, labels):
    context = [
        f"You are working in the notebook section: {section}.",
        f"The notebook topic is {topic}.",
        "Use the variables, data, libraries, and file paths already established above.",
        "Ask for an explanation of the reasoning and a runnable solution, not just a final answer.",
        "Request code that fits this notebook's existing style and does not overwrite unrelated variables.",
    ]
    names = re.findall(r"\b(?:def|class)\s+([A-Za-z_]\w*)|\b([A-Za-z_]\w*)\s*=", source)
    assigned = []
    for pair in names:
        name = pair[0] or pair[1]
        if name and name not in assigned and name not in {"i", "x", "y"}:
            assigned.append(name)
    if assigned:
        context.append("Mention the relevant variables or functions from this cell: " + ", ".join(assigned[:8]) + ".")
    return context


def is_setup_cell(source):
    """Keep imports, configuration, and data-loading cells runnable."""
    text = source.lower()
    exercise_markers = (
        "plt.", "sns.", "matplotlib", "seaborn", "patches", "plotly",
        "fit(", "predict", "evaluate", "classification_report", "roc_auc",
        "train_test_split", "timeseriessplit", "cross_val", "optuna", "mlflow",
        "shap_values", "lime_tabular", "isolationforest", "calculate_psi",
        "command(", "sweep", "ml_client", "submit", "register", "dashboard",
        "confusion_matrix", "roc_curve", "precision_recall", "gridsearch",
    )
    if any(marker in text for marker in exercise_markers):
        return False

    meaningful = [
        line.strip() for line in source.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not meaningful:
        return True
    setup_markers = (
        "import ", "from ", "pip install", "read_csv", "read_excel",
        "read_json", "path(", "os.environ", "random.seed", "np.random.seed",
        "set_option", "warnings.", "logging.", "load_dotenv",
    )
    return all(any(marker in line.lower() for marker in setup_markers) for line in meaningful)


def baseline_notebook(path):
    """Read the tracked notebook when an earlier pass flattened code cells."""
    try:
        relative = path.relative_to(ROOT).as_posix()
        raw = subprocess.check_output(
            ["git", "-c", f"safe.directory={ROOT}", "show", f"HEAD:{relative}"],
            cwd=ROOT,
            text=True,
        )
        return json.loads(raw)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError):
        return None


def guideline(path, cells, index, source, topic):
    section = heading_before(cells, index)
    labels = classify(source, section, topic)
    label_text = " and ".join(labels[:2])
    comment = next((line.strip(" #") for line in source.splitlines() if line.strip().startswith("#")), "")
    if comment:
        task_hint = f" Pay attention to the original cell's intended step: {comment}."
    else:
        task_hint = " Reconstruct the intended step from the section context and the variables already available."
    prompt = f"Implement {label_text} for this notebook section."
    if "plot" in source.lower() or "matplotlib" in source.lower() or "seaborn" in source.lower():
        output = "a readable plot or diagram plus a short interpretation of what it shows"
    elif ".fit(" in source or "train" in source.lower():
        output = "runnable code, evaluation output, and a brief explanation of the result"
    else:
        output = "runnable code and a brief explanation of the result"
    lines = [
        "# TODO: Produce " + output + " for " + label_text + "." + task_hint,
        "#",
        "# Before you prompt your AI, think through:",
        "#   - What should this cell produce, and how will you know that it worked?",
        "#   - Which assumptions, risks, or design choices matter for this result?",
        "#",
        "# What to prompt your AI:",
        "#   \"I am working in a Jupyter notebook section called " + section + ". " + prompt +
        " Show me the reasoning first, then return runnable Python for this cell.\"",
        "#",
        "# Context you MUST include:",
    ]
    lines.extend(f"#   - {item}" for item in context_items(source, section, topic, labels))
    lines.extend([
        "#",
        "# Once you have code, check it against:",
        "#   - The output type, columns, shape, or metric expected by the next section.",
        "#   - A small sanity check that would reveal an empty, impossible, or leaked result.",
    ])
    return lines


for path in sorted(ROOT.rglob("*.ipynb")):
    raw = path.read_text(encoding="utf-8")
    notebook = json.loads(raw)
    cells = notebook.get("cells", [])
    baseline = baseline_notebook(path)
    baseline_cells = baseline.get("cells", []) if baseline else []
    if baseline_cells and len(baseline_cells) != len(cells):
        baseline_cells = []
    topic = topic_for(path, raw)
    for index, cell in enumerate(cells):
        baseline_cell = baseline_cells[index] if baseline_cells else None
        if baseline_cell and baseline_cell.get("cell_type") == "code":
            source = text_from_source(baseline_cell.get("source", []))
            metadata = deepcopy(cell.get("metadata", {}))
            metadata.setdefault("id", f"teaching-{index + 1:03d}")
            metadata["language"] = "python"
            if is_setup_cell(source):
                cell.clear()
                cell.update({
                    "cell_type": "code",
                    "metadata": metadata,
                    "source": baseline_cell.get("source", []),
                    "execution_count": None,
                    "outputs": [],
                })
            else:
                cell.clear()
                cell.update({
                    "cell_type": "code",
                    "metadata": metadata,
                    "source": guideline(path, cells, index, source, topic),
                    "execution_count": None,
                    "outputs": [],
                })
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(path)