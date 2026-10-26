"""Build the Day 1 participant notebooks and their solutions from one source.

    python day1/00_day1_4hr_overview/student_build/build_notebooks.py

Writes:
    student/notebooks/0X_*.ipynb   ✏️ TODO cells, outputs empty (published to participants)
    student_solutions/0X_*.ipynb   the same notebooks with every TODO solved (release after the session)

A cell is md(...), code(...) or todo(student_version, solution_version).
"""

import json
from pathlib import Path
from textwrap import dedent

HERE = Path(__file__).resolve().parent
STUDENT = HERE.parent / "student" / "notebooks"
SOLUTIONS = HERE.parent / "student_solutions"


def md(text):
    return ("markdown", dedent(text).strip())


def code(text):
    return ("code", dedent(text).strip())


def todo(student, solution):
    return ("todo", dedent(student).strip(), dedent(solution).strip())


HOW_TO = """
> **How to use this notebook.** Run cells top to bottom with **Shift + Enter**.
> Cells marked **✏️ TODO** are yours to complete. **🏁 Checkpoint** cells tell you when a module is done.
> Stuck? Ask your neighbour first, then the trainer. Solutions are released after the session.
"""

NOTEBOOKS = {}

# --------------------------------------------------------------------------- 00
NOTEBOOKS["00_environment_check"] = [
    md("""
    # 00 · Environment check
    Run the cell below. Every line should show ✅ before the session starts.
    If you see ❌, re-run the setup script in `setup/` or call the trainer over.
    """),
    code("""
    import importlib, shutil, sys

    ok = sys.version_info[:2] in ((3, 11), (3, 12))
    print(("✅" if ok else "⚠️ "), "Python", sys.version.split()[0], "" if ok else "→ use Python 3.11 (see README)")
    for pkg in ["numpy", "pandas", "sklearn", "matplotlib", "seaborn", "optuna", "mlflow", "shap",
                "fastapi", "uvicorn", "httpx", "yaml", "joblib"]:
        try:
            mod = importlib.import_module(pkg)
            print(f"✅ {pkg:<11} {getattr(mod, '__version__', '')}")
        except Exception as exc:  # show every failure, not just the first
            print(f"❌ {pkg:<11} {type(exc).__name__}: {exc}")
    print("✅ docker found" if shutil.which("docker") else "⚠️  docker not found: Module 4 can run the API with plain uvicorn instead")

    import course_utils
    print("✅ course files found at", course_utils.REPO_ROOT)
    """),
    md("""
    **All green?** You are ready. Keep JupyterLab open and follow the trainer's screen.
    """),
]

# --------------------------------------------------------------------------- 01
NOTEBOOKS["01_trustworthy_data"] = [
    md("""
    # Module 1 · Trustworthy data and leakage-free pipelines
    **Outcomes:** (a) choose the right approach, (b) detect leakage and build a leakage-free pipeline with a fitting validation strategy.

    The case study for the whole day: a **loan-default model**. Each row is a loan application;
    the target `defaulted_in_next_30_days` is 1 when the borrower defaulted (about 9% of loans).
    """ + HOW_TO),
    code("""
    import numpy as np
    import pandas as pd
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report, recall_score, roc_auc_score
    from sklearn.model_selection import TimeSeriesSplit, cross_val_score, train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    from course_utils import check_leak_verdicts, check_pipeline, make_loans

    TARGET = "defaulted_in_next_30_days"
    df = make_loans()
    print(df.shape, f"· default rate {df[TARGET].mean():.1%}")
    df.head()
    """),
    md("""
    ## A · Data quality first
    Five dimensions: **integrity, completeness, accuracy, timeliness, validity**. Check them before you trust any metric.
    """),
    code("""
    num = df.select_dtypes("number")
    q1, q3 = num.quantile(0.25), num.quantile(0.75)
    outside = ((num < q1 - 1.5 * (q3 - q1)) | (num > q3 + 1.5 * (q3 - q1))).mean() * 100

    report = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing_%": (df.isna().mean() * 100).round(1),
        "unique": df.nunique(),
        "outside_IQR_fences_%": outside.round(1),
    })
    report
    """),
    md("""
    Is the missing income **random**? Compare applicants with short and long employment:
    """),
    code("""
    short = df["employment_years"] < 2
    print(f"income missing · employment < 2 years : {df.loc[short, 'annual_income'].isna().mean():.0%}")
    print(f"income missing · employment ≥ 2 years : {df.loc[~short, 'annual_income'].isna().mean():.0%}")
    """),
    md("""
    A big gap means the blanks depend on another column: **MAR**. Impute using that information (inside the pipeline),
    and consider a `was_missing` flag.

    ## B · Hands-on: find every leak (15 min)
    For each column ask one question: **would I know this value at the moment the loan is approved?**

    | Verdict | Meaning |
    |---|---|
    | `LEAK` | Created after, or because of, the outcome. Never use it. |
    | `RISKY` | Usable only with care (as a split key, or if measured at the right time, or imputed correctly). |
    | `SAFE` | Known on the application form. |

    8 minutes alone, 3 minutes with your neighbour, then the reveal.
    """),
    todo(
        """
        # ✏️ TODO: replace each "?" with "LEAK", "RISKY" or "SAFE", then run the cell
        verdicts = {
            "customer_id": "?",
            "loan_approval_date": "?",
            "loan_amount": "?",
            "annual_income": "?",
            "employment_years": "?",
            "credit_score": "?",
            "days_since_last_payment": "?",
            "existing_loans": "?",
            "loan_type": "?",
            "region": "?",
            "days_to_default": "?",
            "post_approval_status_flag": "?",
        }
        check_leak_verdicts(verdicts)
        """,
        """
        verdicts = {
            "customer_id": "RISKY",              # not a feature; a group key for the split
            "loan_approval_date": "RISKY",       # not a feature; orders the time split
            "loan_amount": "SAFE",
            "annual_income": "RISKY",            # gaps: impute inside the Pipeline
            "employment_years": "SAFE",
            "credit_score": "RISKY",             # gaps: impute inside the Pipeline
            "days_since_last_payment": "RISKY",  # safe only if measured at application time
            "existing_loans": "SAFE",
            "loan_type": "SAFE",
            "region": "SAFE",
            "days_to_default": "LEAK",           # exists only after a default
            "post_approval_status_flag": "LEAK", # recorded after approval
        }
        check_leak_verdicts(verdicts)
        """),
    md("""
    ## C · What leakage does to a score
    Here is a model built the wrong way: it uses the two leaked columns and fills the gaps **before** splitting.
    """),
    code("""
    leaky_cols = ["loan_amount", "credit_score", "days_to_default", "post_approval_status_flag"]
    X_leak = pd.get_dummies(df[leaky_cols], columns=["post_approval_status_flag"]).fillna(-1)
    X_tr, X_te, y_tr, y_te = train_test_split(X_leak, df[TARGET], test_size=0.2, random_state=42, stratify=df[TARGET])
    leaky = LogisticRegression(max_iter=2000).fit(X_tr, y_tr)
    print(f"Leaky model ROC-AUC: {roc_auc_score(y_te, leaky.predict_proba(X_te)[:, 1]):.3f}   ← too good to be true")

    always_no = np.zeros(len(y_te), dtype=int)
    print(f"'Always predict no default': accuracy {(always_no == y_te).mean():.1%}, recall {recall_score(y_te, always_no):.0%}")
    """),
    md("""
    Two lessons from the ice breaker: a perfect score usually means a leak, and **accuracy hides a model that catches nobody**
    when defaults are rare. From now on we report **ROC-AUC and recall**.

    ## D · Hands-on: the leakage-free pipeline (20 min)
    The safe order: **split by time first → fit every step inside a `Pipeline` on training rows only → score the newest 20% once.**
    """),
    todo(
        """
        FEATURES_NUM = ["loan_amount", "annual_income", "employment_years", "credit_score",
                        "days_since_last_payment", "existing_loans"]
        FEATURES_CAT = ["loan_type", "region"]

        # 1. ✏️ TODO: sort by loan_approval_date; the oldest 80% trains, the newest 20% tests
        df_sorted = ...
        cut = ...
        train, test = ..., ...

        X_train, X_test = train[FEATURES_NUM + FEATURES_CAT], test[FEATURES_NUM + FEATURES_CAT]
        y_train, y_test = train[TARGET], test[TARGET]

        # 2. ✏️ TODO: numeric = median imputer then StandardScaler
        #             categorical = most_frequent imputer then OneHotEncoder(handle_unknown="ignore")
        num_pipe = Pipeline([...])
        cat_pipe = Pipeline([...])
        pre = ColumnTransformer([("num", num_pipe, FEATURES_NUM), ("cat", cat_pipe, FEATURES_CAT)])

        # 3. ✏️ TODO: chain `pre` with LogisticRegression(max_iter=1000, class_weight="balanced"), fit on TRAIN only
        model = Pipeline([...])
        model.fit(...)
        """,
        """
        FEATURES_NUM = ["loan_amount", "annual_income", "employment_years", "credit_score",
                        "days_since_last_payment", "existing_loans"]
        FEATURES_CAT = ["loan_type", "region"]

        df_sorted = df.sort_values("loan_approval_date").reset_index(drop=True)
        cut = int(len(df_sorted) * 0.8)
        train, test = df_sorted.iloc[:cut], df_sorted.iloc[cut:]

        X_train, X_test = train[FEATURES_NUM + FEATURES_CAT], test[FEATURES_NUM + FEATURES_CAT]
        y_train, y_test = train[TARGET], test[TARGET]

        num_pipe = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
        cat_pipe = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                             ("onehot", OneHotEncoder(handle_unknown="ignore"))])
        pre = ColumnTransformer([("num", num_pipe, FEATURES_NUM), ("cat", cat_pipe, FEATURES_CAT)])

        # class_weight="balanced" makes the rare defaults count during training
        model = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))])
        model.fit(X_train, y_train)
        """),
    code("""
    proba = model.predict_proba(X_test)[:, 1]
    pred = model.predict(X_test)
    print(f"Newest 20% · ROC-AUC {roc_auc_score(y_test, proba):.3f} · recall {recall_score(y_test, pred):.0%}")
    print(classification_report(y_test, pred, digits=3, zero_division=0))
    """),
    md("""
    Lower than the leaky model, and **honest**: this is what next month's applicants will see.

    ### 🏁 Checkpoint · Module 1
    """),
    code("""
    check_pipeline(model, X_train, X_test, train["loan_approval_date"], test["loan_approval_date"])
    """),
    md("""
    ## E · Validate the way the model will be used
    While tuning, use **TimeSeriesSplit** on the training rows: always train on the past, score the next slice.
    """),
    code("""
    scores = cross_val_score(model, X_train, y_train, cv=TimeSeriesSplit(n_splits=5), scoring="roc_auc")
    print("ROC-AUC per fold:", scores.round(3), "· mean", scores.mean().round(3))
    """),
    md("""
    **Stretch:** customers repeat in this data (`customer_id`). How would you keep each customer on one side of the split?
    (Hint: `GroupKFold` or `GroupShuffleSplit` with `groups=df["customer_id"]`.)

    ### Quick quiz
    1. Why is fitting a scaler on the full dataset a problem?
    2. When should you prefer a time-based split?
    3. Which columns here are pure target leakage?
    """),
]

# --------------------------------------------------------------------------- 02
NOTEBOOKS["02_train_tune_track"] = [
    md("""
    # Module 2 · Production training, tuning and tracking
    **Outcomes:** (c) organise training into reproducible scripts, (d) tune with Optuna and track runs in MLflow.
    """ + HOW_TO),
    code("""
    import json, subprocess, sys

    import matplotlib.pyplot as plt
    from sklearn.datasets import make_classification
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import cross_val_score, train_test_split

    from course_utils import REPO_ROOT

    SCRIPTS = REPO_ROOT / "scripts"
    print("Training scripts:", sorted(p.name for p in SCRIPTS.iterdir() if p.suffix in (".py", ".yaml")))
    """),
    md("""
    ## A · From notebook to modular scripts
    | File | One responsibility |
    |---|---|
    | `scripts/config.yaml` | every setting: data, model, paths |
    | `scripts/data_loader.py` | load the data, check the target, split |
    | `scripts/features.py` | impute and encode |
    | `scripts/train.py` | build the model from config and save it |
    | `scripts/evaluate.py` | write precision, recall and F1 to JSON |
    | `scripts/main.py` | read the config, log, run each step |

    In a terminal (repo root, environment active) this is one command:
    ```bash
    python scripts/main.py --config scripts/config.yaml
    ```
    The cell below runs exactly that.
    """),
    code("""
    def run_training():
        out = subprocess.run([sys.executable, str(SCRIPTS / "main.py"), "--config", str(SCRIPTS / "config.yaml")],
                             capture_output=True, text=True)
        print((out.stderr or out.stdout)[-800:])
        if out.returncode:
            raise RuntimeError("Training failed: read the log above")
        return json.loads((REPO_ROOT / "artifacts" / "metrics.json").read_text())

    run1 = run_training()
    print({k: round(v, 3) for k, v in run1.items() if isinstance(v, float)})
    """),
    md("""
    **✏️ Hands-on:** open `scripts/config.yaml` in JupyterLab, change `test_size` from `0.2` to `0.3`
    (or `max_iter`), **save**, then run the next cell and compare. Same config + same seed = same result.
    Put it back to `0.2` afterwards.
    """),
    code("""
    run2 = run_training()
    for k in ["accuracy", "precision", "recall", "f1"]:
        print(f"{k:<10} run 1 {run1[k]:.3f}   run 2 {run2[k]:.3f}")
    """),
    md("""
    ## B · Hyperparameter tuning with Optuna (20 min)
    **Parameters** are learned by `fit()`. **Hyperparameters** are chosen by you, so search for them,
    and **never let the test set choose**: score each trial with cross-validation on the training rows.
    """),
    code("""
    X, y = make_classification(n_samples=2000, n_features=20, n_informative=10, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    guess = RandomForestClassifier(n_estimators=10, max_depth=2, random_state=42).fit(X_train, y_train)
    baseline_auc = roc_auc_score(y_test, guess.predict_proba(X_test)[:, 1])
    print(f"Guessed hyperparameters · test ROC-AUC {baseline_auc:.3f}")
    """),
    todo(
        """
        import optuna
        optuna.logging.set_verbosity(optuna.logging.WARNING)

        def objective(trial):
            # ✏️ TODO 1: suggest n_estimators (50–300), max_depth (3–20), min_samples_split (2–15)
            #           hint: trial.suggest_int("name", low, high)
            params = {
                "n_estimators": ...,
                "max_depth": ...,
                "min_samples_split": ...,
            }
            clf = RandomForestClassifier(**params, random_state=42, n_jobs=-1)
            # ✏️ TODO 2: return the mean ROC-AUC of 3-fold cross-validation on X_train, y_train
            #           hint: cross_val_score(clf, X_train, y_train, cv=3, scoring="roc_auc").mean()
            return ...

        N_TRIALS = 20   # use 10 on a slow laptop
        study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=42))
        study.optimize(objective, n_trials=N_TRIALS)
        print("Best CV ROC-AUC:", round(study.best_value, 4))
        print("Best params:", study.best_params)
        """,
        """
        import optuna
        optuna.logging.set_verbosity(optuna.logging.WARNING)

        def objective(trial):
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 50, 300),
                "max_depth": trial.suggest_int("max_depth", 3, 20),
                "min_samples_split": trial.suggest_int("min_samples_split", 2, 15),
            }
            clf = RandomForestClassifier(**params, random_state=42, n_jobs=-1)
            return cross_val_score(clf, X_train, y_train, cv=3, scoring="roc_auc").mean()

        N_TRIALS = 20
        study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=42))
        study.optimize(objective, n_trials=N_TRIALS)
        print("Best CV ROC-AUC:", round(study.best_value, 4))
        print("Best params:", study.best_params)
        """),
    code("""
    trials = study.trials_dataframe()
    importance = optuna.importance.get_param_importances(study)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(trials["number"], trials["value"], "o", alpha=0.5, label="trial")
    axes[0].plot(trials["number"], trials["value"].cummax(), "-", label="best so far")
    axes[0].set(title="Optimisation history", xlabel="trial", ylabel="CV ROC-AUC")
    axes[0].legend()
    axes[1].barh(list(importance)[::-1], list(importance.values())[::-1])
    axes[1].set(title="Which hyperparameter mattered?")
    plt.tight_layout()
    plt.show()
    """),
    md("""
    ## C · If it is not logged, it did not happen: MLflow (20 min)
    Runs are stored in `mlruns/` at the repo root.
    """),
    code("""
    import mlflow
    import mlflow.sklearn

    mlflow.set_tracking_uri((REPO_ROOT / "mlruns").as_uri())
    mlflow.set_experiment("day1_loan_default")

    with mlflow.start_run(run_name="rf_baseline"):
        mlflow.log_params({"n_estimators": 10, "max_depth": 2})
        mlflow.log_metric("test_auc", baseline_auc)
    print("Baseline logged.")
    """),
    todo(
        """
        with mlflow.start_run(run_name="optuna_best_rf"):
            best = RandomForestClassifier(**study.best_params, random_state=42, n_jobs=-1).fit(X_train, y_train)
            test_auc = roc_auc_score(y_test, best.predict_proba(X_test)[:, 1])   # scored ONCE, after tuning

            # ✏️ TODO: log (1) the best params, (2) test_auc and the CV score, (3) a data_version tag, (4) the model
            #   hints: mlflow.log_params(...), mlflow.log_metric("name", value), mlflow.set_tag("name", "value"),
            #          mlflow.sklearn.log_model(best, "model")
            ...

        print(f"Logged · test ROC-AUC {test_auc:.4f}")
        """,
        """
        with mlflow.start_run(run_name="optuna_best_rf"):
            best = RandomForestClassifier(**study.best_params, random_state=42, n_jobs=-1).fit(X_train, y_train)
            test_auc = roc_auc_score(y_test, best.predict_proba(X_test)[:, 1])

            mlflow.log_params(study.best_params)
            mlflow.log_metric("test_auc", test_auc)
            mlflow.log_metric("cv_auc", study.best_value)
            mlflow.set_tag("data_version", "make_classification_seed42")
            mlflow.sklearn.log_model(best, "model")

        print(f"Logged · test ROC-AUC {test_auc:.4f}")
        """),
    md("""
    ### 🏁 Checkpoint · Module 2
    """),
    code("""
    runs = mlflow.search_runs(experiment_names=["day1_loan_default"])
    cols = [c for c in ["tags.mlflow.runName", "metrics.test_auc", "params.n_estimators", "params.max_depth"] if c in runs]
    print(runs[cols].sort_values("metrics.test_auc", ascending=False).head(8).to_string(index=False))

    tuned = runs[runs["tags.mlflow.runName"] == "optuna_best_rf"] if "tags.mlflow.runName" in runs else runs.iloc[0:0]
    ok = (not tuned.empty and "params.min_samples_split" in tuned and tuned["params.min_samples_split"].notna().any()
          and tuned["metrics.test_auc"].notna().any())
    print("\\n🏁 Module 2 checkpoint passed. Now open the MLflow UI." if ok
          else "\\n❌ No tuned run with params and test_auc yet. Finish the TODO above.")
    """),
    md("""
    **Open the MLflow UI.** In a new terminal at the repo root, with the environment active:
    ```bash
    mlflow ui
    ```
    Then browse to http://127.0.0.1:5000, open **day1_loan_default**, sort by `test_auc`, and compare the runs.

    ### Quick quiz
    1. Why does random search often beat grid search?
    2. Why must the test set never guide tuning?
    3. What should every MLflow run log?
    """),
]

# --------------------------------------------------------------------------- 03
NOTEBOOKS["03_explain_and_monitor"] = [
    md("""
    # Module 3 · Explainability and drift monitoring
    **Outcomes:** (e) explain a prediction with SHAP, in plain language; (f) detect drift with PSI and KS, and set thresholds.
    """ + HOW_TO),
    code("""
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import shap
    from scipy.stats import ks_2samp
    from sklearn.ensemble import IsolationForest

    from course_utils import check_drift_table, check_narrative, check_psi, make_credit_data, make_drift_data

    model, X_train, X_test, y_train, y_test = make_credit_data()
    print(f"Gradient boosting credit model · test accuracy {model.score(X_test, y_test):.2f}")
    """),
    md("""
    ## A · SHAP: fair credit for every feature (20 min)
    `f(x) = E[f(X)] + Σ φᵢ`: each feature's contribution adds up to the prediction (in log-odds).
    **Global** view first: what drives the whole portfolio? Red is a high value, right means more risk.
    """),
    code("""
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    base_value = float(np.ravel(explainer.expected_value)[0])
    shap.summary_plot(shap_values, X_test)
    """),
    md("""
    **Local** view: why did *this* applicant get *this* score?
    """),
    code("""
    i = 0   # applicant 0, the one on the slides
    shap.waterfall_plot(shap.Explanation(values=shap_values[i], base_values=base_value,
                                         data=X_test.iloc[i], feature_names=list(X_test.columns)))

    contrib = pd.DataFrame({"value": X_test.iloc[i].round(2), "shap": shap_values[i].round(3)})
    contrib = contrib.reindex(contrib["shap"].abs().sort_values(ascending=False).index)
    probability = 1 / (1 + np.exp(-(base_value + shap_values[i].sum())))
    print(f"Applicant {i}: estimated default probability {probability:.0%}")
    contrib
    """),
    md("""
    ## B · Pair exercise: from numbers to a narrative (10 min)
    Never hand a raw SHAP value to a stakeholder. Formula: **observed value → direction and size → one action that would change the decision.**

    *Example for a different applicant:* "High card utilisation (87%) was the main reason for the decline: it pushed the estimated
    default risk well above the approval line. Reducing utilisation below 30% would move the application to approval."
    """),
    todo(
        """
        # ✏️ TODO: three sentences about applicant 0 that a branch manager could act on (use the table above)
        sentence_1 = ""   # the main driver and its value
        sentence_2 = ""   # its direction and size, in plain words (no "SHAP", no "log-odds")
        sentence_3 = ""   # one action or change that would move the decision

        check_narrative([sentence_1, sentence_2, sentence_3])
        """,
        """
        sentence_1 = "The applicant's age (52) was the strongest factor in their favour, helped by a clean payment history."
        sentence_2 = "Together these lowered the estimated chance of default to about 6%, well below our approval line, so we approve."
        sentence_3 = "If card utilisation rose from 20% to above 60%, the decision would need a fresh review."

        print(sentence_1, sentence_2, sentence_3, sep="\\n")
        check_narrative([sentence_1, sentence_2, sentence_3])
        """),
    md("""
    Swap with your neighbour: **could a branch manager with no ML background act on it?**

    ## C · Detecting drift: PSI and the KS test (15 min)
    One month of production data against the training month. Same simulation as the slides.
    """),
    code("""
    train, prod = make_drift_data()
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.hist(train["credit_utilization"], bins=40, alpha=0.5, density=True, label="training")
    ax.hist(prod["credit_utilization"], bins=40, alpha=0.5, density=True, label="production")
    ax.set(title="credit_utilization: training vs production", xlabel="utilisation")
    ax.legend()
    plt.show()
    """),
    md("""
    **Population Stability Index:** cut the *training* data into 10 equal bins, then compare the share of rows per bin.
    `PSI = Σ (Aᵢ − Eᵢ) · ln(Aᵢ / Eᵢ)` where E is the training share and A the production share.
    Bands: **< 0.10 stable · 0.10–0.20 watch · ≥ 0.20 alert.**
    """),
    todo(
        """
        def psi(expected, actual, buckets=10):
            \"\"\"Population Stability Index of `actual` (production) against `expected` (training).\"\"\"
            edges = np.percentile(expected, np.linspace(0, 100, buckets + 1))   # bins from the TRAINING quantiles
            edges[0], edges[-1] = -np.inf, np.inf                               # open ends: nothing falls off
            e = np.clip(np.histogram(expected, edges)[0] / len(expected), 1e-4, None)   # training share per bin
            a = np.clip(np.histogram(actual, edges)[0] / len(actual), 1e-4, None)       # production share per bin
            # ✏️ TODO: return PSI = Σ (a − e) · ln(a / e)      hint: np.sum, np.log
            return ...

        check_psi(psi)
        """,
        """
        def psi(expected, actual, buckets=10):
            \"\"\"Population Stability Index of `actual` (production) against `expected` (training).\"\"\"
            edges = np.percentile(expected, np.linspace(0, 100, buckets + 1))
            edges[0], edges[-1] = -np.inf, np.inf
            e = np.clip(np.histogram(expected, edges)[0] / len(expected), 1e-4, None)
            a = np.clip(np.histogram(actual, edges)[0] / len(actual), 1e-4, None)
            return float(np.sum((a - e) * np.log(a / e)))

        check_psi(psi)
        """),
    todo(
        """
        rows = []
        for col in train.columns:
            p = psi(train[col], prod[col])
            ks = ks_2samp(train[col], prod[col])
            # ✏️ TODO: "ALERT" if p is 0.20 or more, "WATCH" if 0.10 or more, otherwise "STABLE"
            status = ...
            rows.append({"feature": col, "psi": round(p, 3), "ks_pvalue": round(ks.pvalue, 4), "status": status})

        drift = pd.DataFrame(rows).sort_values("psi", ascending=False)
        print(drift.to_string(index=False), "\\n")
        check_drift_table(drift)
        """,
        """
        rows = []
        for col in train.columns:
            p = psi(train[col], prod[col])
            ks = ks_2samp(train[col], prod[col])
            status = "ALERT" if p >= 0.2 else "WATCH" if p >= 0.1 else "STABLE"
            rows.append({"feature": col, "psi": round(p, 3), "ks_pvalue": round(ks.pvalue, 4), "status": status})

        drift = pd.DataFrame(rows).sort_values("psi", ascending=False)
        print(drift.to_string(index=False), "\\n")
        check_drift_table(drift)
        """),
    md("""
    Look at `annual_income`: the KS p-value is tiny, yet PSI says stable. With thousands of rows KS flags
    *any* difference; PSI tells you whether it is **big enough to act on**.

    ## D · Trainer demo: anomalies without labels (Isolation Forest)
    """),
    code("""
    rng = np.random.default_rng(0)
    cols = ["credit_utilization", "age"]
    iso = IsolationForest(contamination=0.05, random_state=42).fit(train[cols].to_numpy())

    normal = train[cols].sample(950, random_state=0).to_numpy()   # ordinary applicants
    odd = np.column_stack([rng.uniform(0.85, 1.0, 50), rng.uniform(85, 110, 50)])   # 50 injected odd rows
    live = np.vstack([normal, odd])
    flagged = iso.predict(live) == -1
    print(f"Injected 50 odd rows · flagged {flagged.sum()} in total · caught {flagged[-50:].sum()} of the 50")

    plt.figure(figsize=(7, 4))
    plt.scatter(live[~flagged, 0], live[~flagged, 1], s=8, alpha=0.4, label="normal")
    plt.scatter(live[flagged, 0], live[flagged, 1], s=30, marker="x", color="crimson", label="flagged")
    plt.xlabel("credit_utilization"); plt.ylabel("age"); plt.legend(); plt.title("Isolation Forest on live traffic")
    plt.show()
    """),
    md("""
    `contamination=0.05` tells the forest to expect about 5% odd rows, so it also flags a few ordinary ones.
    Tune it on real traffic so the alert rate is one a human will actually read.

    ### Monitoring cadence for the loan model
    | Cadence | Check | Action |
    |---|---|---|
    | Every request | schema and ranges (Pydantic) | reject with HTTP 422 |
    | Daily | volume, missing rate, anomaly rate | investigate if anomalies > 2× baseline |
    | Weekly | PSI and KS per feature | watch at 0.1, alert at 0.2 |
    | Monthly | AUC and recall on labelled loans | retrain if below the SLO |
    | Quarterly | model review with risk | re-approve or retire |

    ### Quick quiz
    1. What does SHAP additivity guarantee?
    2. A feature has PSI = 0.27. What do you do?
    3. Does Isolation Forest need labelled anomalies?
    """),
]

# --------------------------------------------------------------------------- 04
NOTEBOOKS["04_serve_and_monitor"] = [
    md("""
    # Module 4 · Serving, monitoring and cloud
    **Outcomes:** (g) serve a model as a REST API with FastAPI inside Docker; (h) monitor it in production and map the workflow to Azure ML.
    """ + HOW_TO),
    md("""
    ## A · Start the API (in a terminal, not here)
    Open a terminal **at the repo root** with the environment active, then pick one:

    **With Docker** (the checkpoint):
    ```bash
    cd api
    docker build -t loan-api:1.0 .
    docker run -d -p 8000:8000 --name loan-api loan-api:1.0
    ```
    **Without Docker** (same API, runs in your Python environment):
    ```bash
    cd api
    uvicorn main:app --reload --port 8000
    ```
    Port 8000 taken? Use `-p 8001:8000` (Docker) or `--port 8001`, and change `API` below.
    """),
    code("""
    import httpx
    import matplotlib.pyplot as plt

    from course_utils import REPO_ROOT, check_status_codes, dashboard_series

    API = "http://localhost:8000"
    try:
        r = httpx.get(f"{API}/health", timeout=3)
        print("✅", r.status_code, r.json(), "· Swagger docs at", f"{API}/docs")
    except httpx.HTTPError as exc:
        print(f"❌ Nothing answering at {API} ({type(exc).__name__}). Start the API in a terminal first (see above).")
    """),
    code("""
    def call(payload):
        \"\"\"POST one application to /v1/predict and show what comes back.\"\"\"
        try:
            r = httpx.post(f"{API}/v1/predict", json=payload, timeout=5)
        except httpx.HTTPError as exc:
            print(f"❌ API not reachable ({type(exc).__name__})")
            return None
        body = r.json()
        print(r.status_code, body if r.status_code == 200 else body["detail"][0]["msg"])
        return r.status_code

    call({"age": 35, "income": 72000, "credit_score": 710})
    """),
    md("""
    ## B · Hands-on: make Pydantic say no
    The API declares `age` 18–120, `income` > 0, `credit_score` 300–850, all required.
    Bad input should be rejected with **422** before it ever reaches the model.
    """),
    todo(
        """
        valid = {"age": 35, "income": 72000, "credit_score": 710}

        # ✏️ TODO: copy `valid`, then change the age to one the API must refuse
        age_too_low = {}
        # ✏️ TODO: copy `valid`, then leave out one required field
        missing_field = {}

        results = {"valid": call(valid), "age_too_low": call(age_too_low), "missing_field": call(missing_field)}
        check_status_codes(results, age_too_low, missing_field)
        """,
        """
        valid = {"age": 35, "income": 72000, "credit_score": 710}
        age_too_low = {**valid, "age": 7}
        missing_field = {"age": 35, "income": 72000}

        results = {"valid": call(valid), "age_too_low": call(age_too_low), "missing_field": call(missing_field)}
        check_status_codes(results, age_too_low, missing_field)
        """),
    md("""
    🏁 **Checkpoint · Module 4:** the container (or uvicorn) answers, and bad input gets a 422.
    Try the same calls from the interactive docs at http://localhost:8000/docs.

    ## C · The MLOps dashboard and SLOs (15 min)
    Ten weeks of production metrics for the loan model (illustrative). Alert only when a **promise (SLO)** breaks.
    """),
    todo(
        """
        data = dashboard_series()

        # ✏️ TODO: set the service level objectives from the slides
        SLO = {
            "auc_min": ...,              # model: monthly AUC must stay at or above this
            "top_feature_psi_max": ...,  # data: PSI of the top features must stay below this
            "p99_latency_ms_max": ...,   # system: p99 latency in ms
            "error_rate_pct_max": ...,   # system: share of failed requests, in %
        }
        """,
        """
        data = dashboard_series()

        SLO = {
            "auc_min": 0.75,
            "top_feature_psi_max": 0.2,
            "p99_latency_ms_max": 300,
            "error_rate_pct_max": 1.0,
        }
        """),
    code("""
    rules = {
        "Model · AUC": ("auc", lambda v: v >= SLO["auc_min"]),
        "Data · top feature PSI": ("top_feature_psi", lambda v: v < SLO["top_feature_psi_max"]),
        "System · p99 latency": ("p99_latency_ms", lambda v: v < SLO["p99_latency_ms_max"]),
        "System · error rate": ("error_rate_pct", lambda v: v < SLO["error_rate_pct_max"]),
    }
    latest = data.iloc[-1]
    print(f"Latest week ({latest.week}):")
    for name, (col, within) in rules.items():
        broken = [w for w, v in zip(data.week, data[col]) if not within(v)]
        state = "🟢 dashboard only" if within(latest[col]) else "🔴 PAGE SOMEONE"
        print(f"  {state:<18} {name:<24} now {latest[col]:<6}  weeks out of SLO: {', '.join(broken) or 'none'}")
    """),
    code("""
    panels = [("auc", "Model · AUC", SLO["auc_min"]), ("predicted_default_rate_pct", "Model · predicted default rate %", None),
              ("top_feature_psi", "Data · top feature PSI", SLO["top_feature_psi_max"]),
              ("p99_latency_ms", "System · p99 latency (ms)", SLO["p99_latency_ms_max"]),
              ("requests_per_hour", "System · requests per hour", None), ("error_rate_pct", "System · error rate %", SLO["error_rate_pct_max"])]
    fig, axes = plt.subplots(2, 3, figsize=(15, 7))
    for ax, (col, title, line) in zip(axes.flat, panels):
        ax.plot(data.week, data[col], "o-")
        if line is not None:
            ax.axhline(line, color="crimson", linestyle="--", label="SLO")
            ax.legend()
        ax.set_title(title)
    fig.suptitle("Loan default model · weekly MLOps dashboard", fontsize=15, fontweight="bold")
    plt.tight_layout()

    out = REPO_ROOT / "reports" / "mlops_dashboard.png"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=120)
    plt.show()
    print("Saved", out)
    """),
    md("""
    Read it as one story: AUC slides toward its SLO while the top feature's PSI climbs into the alert band:
    the same drift you measured in Module 3.

    ## D · The same workflow on Azure Machine Learning (trainer demo)
    | Built today | Azure ML equivalent |
    |---|---|
    | `scripts/main.py` + `config.yaml` | command job on a compute cluster |
    | Optuna study | sweep job, with early stopping |
    | local MLflow (`mlruns/`) | MLflow tracking in the workspace |
    | `model.joblib` | model registry, versioned and tagged |
    | FastAPI + Docker | managed online endpoint |
    | PSI / KS checks | model monitoring |

    ## E · Your action plan
    Open `docs/WORKSHEET.md` and fill in the five action-plan prompts before you leave.

    **Clean up** (Docker): `docker rm -f loan-api`
    """),
]


def to_cells(spec, solved):
    cells = []
    for item in spec:
        kind = item[0]
        if kind == "todo":
            kind, text = "code", item[2] if solved else item[1]
        else:
            text = item[1]
        cell = {"cell_type": kind, "metadata": {}, "source": text.splitlines(keepends=True)}
        if kind == "code":
            cell.update(execution_count=None, outputs=[])
        cells.append(cell)
    return cells


def write(path, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    STUDENT.mkdir(parents=True, exist_ok=True)
    SOLUTIONS.mkdir(parents=True, exist_ok=True)
    for name, spec in NOTEBOOKS.items():
        write(STUDENT / f"{name}.ipynb", to_cells(spec, solved=False))
        write(SOLUTIONS / f"{name}.ipynb", to_cells(spec, solved=True))
        todos = sum(1 for item in spec if item[0] == "todo")
        print(f"{name:<24} {len(spec):>2} cells · {todos} TODO")


if __name__ == "__main__":
    main()
