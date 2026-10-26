"""Shared data generators and checkpoint checks for the Day 1 notebooks.

Every generator is seeded, so your numbers match the slides and your neighbour's.
You do not need to edit this file.
"""

import base64
import json
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
OK, NO = "✅", "❌"


# ---------------------------------------------------------------- Module 1

def make_loans(n=2000, seed=42):
    """A loan book with realistic quality problems and four leakage traps.

    Target: defaulted_in_next_30_days (about 9% positive, so accuracy alone misleads).
    """
    rng = np.random.default_rng(seed)
    customers = rng.integers(1, int(n * 0.75), n)            # some customers borrow more than once
    df = pd.DataFrame({
        "customer_id": customers,
        "loan_approval_date": pd.Timestamp("2023-01-01") + pd.to_timedelta(np.sort(rng.integers(0, 730, n)), unit="D"),
        "loan_amount": rng.lognormal(9.6, 0.6, n).round(2),
        "annual_income": rng.lognormal(11.0, 0.45, n).round(2),
        "employment_years": rng.gamma(2.5, 3.5, n).round(1),
        "credit_score": rng.normal(680, 55, n).clip(300, 850).round(0),
        "days_since_last_payment": rng.exponential(30, n).round(0),
        "existing_loans": rng.poisson(1.8, n),
        "loan_type": rng.choice(["personal", "auto", "mortgage", "student"], n, p=[0.4, 0.25, 0.2, 0.15]),
        "region": rng.choice(["North", "South", "East", "West"], n),
    })
    logit = (-3.8
             + 2.0 * (df["credit_score"] < 620)
             + 1.2 * (df["existing_loans"] > 2)
             + 0.9 * (df["loan_type"] == "personal")
             - 1.0 * (df["employment_years"] > 5)
             + 0.035 * (df["days_since_last_payment"] - 30)
             + 1.2 * (df["loan_amount"] / df["annual_income"] > 0.35))
    df["defaulted_in_next_30_days"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)

    # Leakage traps: only known after the outcome
    default = df["defaulted_in_next_30_days"] == 1
    df["days_to_default"] = np.where(default, rng.integers(1, 30, n), np.nan)
    df["post_approval_status_flag"] = np.where(default, rng.choice(["collections", "late"], n, p=[0.8, 0.2]),
                                               rng.choice(["current", "late"], n, p=[0.93, 0.07]))

    # Quality problems: income is missing more often for the self-employed-looking (MAR),
    # credit scores go missing for some risky applicants (MNAR-ish)
    miss_income = rng.random(n) < np.where(df["employment_years"] < 2, 0.25, 0.06)
    df.loc[miss_income, "annual_income"] = np.nan
    miss_score = rng.random(n) < np.where(df["credit_score"] < 620, 0.12, 0.03)
    df.loc[miss_score, "credit_score"] = np.nan
    return df


LEAK_KEY = "eyJkYXlzX3RvX2RlZmF1bHQiOiAiTEVBSyIsICJwb3N0X2FwcHJvdmFsX3N0YXR1c19mbGFnIjogIkxFQUsiLCAibG9hbl9hcHByb3ZhbF9kYXRlIjogIlJJU0tZIiwgImN1c3RvbWVyX2lkIjogIlJJU0tZIiwgImRheXNfc2luY2VfbGFzdF9wYXltZW50IjogIlJJU0tZIiwgImFubnVhbF9pbmNvbWUiOiAiUklTS1kiLCAiY3JlZGl0X3Njb3JlIjogIlJJU0tZIiwgImxvYW5fYW1vdW50IjogIlNBRkUiLCAiZW1wbG95bWVudF95ZWFycyI6ICJTQUZFIiwgImV4aXN0aW5nX2xvYW5zIjogIlNBRkUiLCAibG9hbl90eXBlIjogIlNBRkUiLCAicmVnaW9uIjogIlNBRkUifQ=="
LEAK_WHY = {
    "days_to_default": "only exists after the borrower defaults",
    "post_approval_status_flag": "recorded after approval; it encodes the outcome",
    "loan_approval_date": "not a feature; use it to order the split by time",
    "customer_id": "not a feature; use it to keep repeat customers on one side",
    "days_since_last_payment": "safe only if measured as of the application date",
    "annual_income": "has gaps; impute inside the Pipeline, never before the split",
    "credit_score": "has gaps; impute inside the Pipeline, never before the split",
}


def check_leak_verdicts(verdicts):
    """Score your LEAK / RISKY / SAFE calls against the answer key."""
    key = json.loads(base64.b64decode(LEAK_KEY))
    right = 0
    for col, answer in key.items():
        got = str(verdicts.get(col, "?")).upper()
        if got == answer:
            right += 1
            print(f"{OK} {col:<26} {got}")
        elif got in ("?", ""):
            print(f"⏳ {col:<26} not classified yet")
        else:
            print(f"{NO} {col:<26} you said {got}, think again: would you know it at approval?")
    print(f"\n{right} / {len(key)} correct")
    if right == len(key):
        print("All correct. Reasons for the non-SAFE ones:")
        for col, why in LEAK_WHY.items():
            print(f"  · {col}: {why}")
    return right == len(key)


def check_pipeline(model, X_train, X_test, train_dates, test_dates):
    """Module 1 checkpoint: Pipeline, no leaked columns, time-ordered split."""
    from sklearn.pipeline import Pipeline
    leaks = {"days_to_default", "post_approval_status_flag", "customer_id", "loan_approval_date", "defaulted_in_next_30_days"}
    checks = [
        ("model is a scikit-learn Pipeline", isinstance(model, Pipeline)),
        ("no leaked or ID columns in the features", not (set(X_train.columns) & leaks)),
        ("train and test use the same columns", list(X_train.columns) == list(X_test.columns)),
        ("every training loan is older than every test loan", pd.Series(train_dates).max() <= pd.Series(test_dates).min()),
        ("roughly 80/20 split", 0.15 <= len(X_test) / (len(X_train) + len(X_test)) <= 0.25),
    ]
    for label, ok in checks:
        print(f"{OK if ok else NO} {label}")
    passed = all(ok for _, ok in checks)
    print("\n🏁 Module 1 checkpoint passed." if passed else "\nFix the ❌ items and run this cell again.")
    return passed


# ---------------------------------------------------------------- Module 3

def make_credit_data():
    """The exact credit data and model from the slides (Session 05), so the plots match."""
    from sklearn.datasets import make_classification
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import train_test_split

    names = ["income", "age", "credit_utilization", "missed_payments", "loan_amount", "years_employed"]
    X, y = make_classification(n_samples=1000, n_features=6, n_informative=4, n_redundant=0, random_state=42)
    X = pd.DataFrame(X, columns=names)
    X["income"] = (X["income"] - X["income"].min() + 1) * 20000
    X["age"] = (X["age"] - X["age"].min() + 1) * 10 + 18
    X["credit_utilization"] = np.abs(X["credit_utilization"]) / X["credit_utilization"].max()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = GradientBoostingClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)
    return model, X_train, X_test, y_train, y_test


def check_narrative(sentences):
    """A quick sanity check for the three-sentence business narrative."""
    text = " ".join(s for s in sentences if isinstance(s, str)).strip()
    jargon = [w for w in ("shap", "log-odds", "logit", "phi", "feature importance") if w in text.lower()]
    checks = [
        ("three sentences written", all(isinstance(s, str) and len(s.strip()) > 15 for s in sentences)),
        ("mentions a concrete value (a number)", any(ch.isdigit() for ch in text)),
        ("no ML jargon a branch manager would not know", not jargon),
        ("ends with an action (would / could / if / reduce / increase…)",
         any(w in text.lower() for w in ("would", "could", "if ", "reduce", "increase", "lower", "raise", "pay"))),
    ]
    for label, ok in checks:
        print(f"{OK if ok else NO} {label}")
    if jargon:
        print("   jargon found:", ", ".join(jargon))
    print("\nNow swap with a neighbour: could they act on it?" if all(ok for _, ok in checks) else "\nRevise and run again.")


def make_drift_data():
    """Training month vs one production month: the exact simulation behind the PSI slide."""
    rng = np.random.default_rng(42)
    n_tr, n_pr = 5000, 2000
    sim = {
        "credit_utilization": (rng.beta(2, 5, n_tr), rng.beta(2.7, 4.6, n_pr)),
        "age": (rng.normal(40, 10, n_tr), rng.normal(36.5, 10, n_pr)),
        "annual_income": (rng.lognormal(11, 0.4, n_tr), rng.lognormal(10.9, 0.43, n_pr)),
        "loan_amount": (rng.lognormal(9.5, 0.5, n_tr), rng.lognormal(9.52, 0.5, n_pr)),
        "credit_score": (rng.normal(680, 50, n_tr), rng.normal(677, 50, n_pr)),
        "employment_years": (rng.gamma(2, 3, n_tr), rng.gamma(2, 3, n_pr)),
    }
    train = pd.DataFrame({k: v[0] for k, v in sim.items()})
    prod = pd.DataFrame({k: v[1] for k, v in sim.items()})
    return train, prod


def reference_psi(expected, actual, buckets=10):
    bp = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    bp[0], bp[-1] = -np.inf, np.inf
    e = np.clip(np.histogram(expected, bp)[0] / len(expected), 1e-4, None)
    a = np.clip(np.histogram(actual, bp)[0] / len(actual), 1e-4, None)
    return float(np.sum((a - e) * np.log(a / e)))


def check_psi(psi_fn):
    train, prod = make_drift_data()
    ok = True
    for col in train.columns:
        want = reference_psi(train[col], prod[col])
        try:
            got = float(psi_fn(train[col], prod[col]))
        except Exception as exc:  # noqa: BLE001 - show the student what went wrong
            print(f"{NO} {col}: your function raised {type(exc).__name__}: {exc}")
            return False
        match = abs(got - want) < 0.005
        ok &= match
        print(f"{OK if match else NO} {col:<20} yours {got:.3f}   expected {want:.3f}")
    print("\nPSI function verified." if ok else "\nNot matching yet. Check the bins (cut on the TRAINING quantiles) and the formula.")
    return ok


def check_drift_table(table):
    """Module 3 checkpoint: one row per feature with psi, ks_pvalue and status."""
    train, prod = make_drift_data()
    expected = {c: ("ALERT" if p >= 0.2 else "WATCH" if p >= 0.1 else "STABLE")
                for c in train.columns for p in [reference_psi(train[c], prod[c])]}
    need = {"feature", "psi", "ks_pvalue", "status"}
    if not need <= set(table.columns):
        print(f"{NO} the table needs the columns {sorted(need)}; it has {list(table.columns)}")
        return False
    got = dict(zip(table["feature"], table["status"].str.upper()))
    ok = True
    for col, want in expected.items():
        match = got.get(col) == want
        ok &= match
        print(f"{OK if match else NO} {col:<20} {got.get(col, 'missing'):<7} (expected {want})")
    print("\n🏁 Module 3 checkpoint passed." if ok else "\nCheck the band rule: < 0.10 STABLE, 0.10 to 0.20 WATCH, ≥ 0.20 ALERT.")
    return ok


# ---------------------------------------------------------------- Module 4

def check_status_codes(results, age_too_low, missing_field):
    """results: {name: status_code} from your three API calls, plus the two payloads you wrote."""
    fields = {"age", "income", "credit_score"}
    payload_checks = [
        ("age_too_low keeps all three fields", isinstance(age_too_low, dict) and set(age_too_low) == fields),
        ("age_too_low uses an age under 18", isinstance(age_too_low, dict) and isinstance(age_too_low.get("age"), (int, float))
         and age_too_low["age"] < 18),
        ("missing_field leaves out exactly one field", isinstance(missing_field, dict) and set(missing_field) < fields
         and len(missing_field) == 2),
    ]
    want = {"valid": 200, "age_too_low": 422, "missing_field": 422}
    ok = True
    for label, good in payload_checks:
        ok &= good
        print(f"{OK if good else NO} {label}")
    for name, code in want.items():
        got = results.get(name)
        match = got == code
        ok &= match
        print(f"{OK if match else NO} {name:<14} got {got}, expected {code}")
    print("\n🏁 Your API validates its input." if ok else "\nAdjust the payloads so each call triggers the expected status.")
    return ok


def dashboard_series():
    """Ten weeks of illustrative production metrics (the dashboard slide)."""
    return pd.DataFrame({
        "week": [f"W{i}" for i in range(1, 11)],
        "auc": [0.82, 0.82, 0.81, 0.81, 0.80, 0.79, 0.78, 0.76, 0.75, 0.73],
        "predicted_default_rate_pct": [3.1, 3.0, 3.2, 3.3, 3.6, 3.9, 4.2, 4.6, 4.9, 5.3],
        "p99_latency_ms": [110, 120, 115, 130, 125, 180, 240, 210, 150, 140],
        "requests_per_hour": [820, 900, 870, 950, 1010, 990, 1100, 1050, 980, 1020],
        "error_rate_pct": [0.3, 0.2, 0.4, 0.3, 0.3, 0.5, 1.6, 0.8, 0.4, 0.3],
        "top_feature_psi": [0.02, 0.03, 0.05, 0.07, 0.09, 0.12, 0.16, 0.21, 0.26, 0.30],
    })
