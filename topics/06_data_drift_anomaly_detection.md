# 📉 Topic 06 — Data Drift & Unsupervised Anomaly Detection (MLOps Guardrail)
> **Schedule:** Day 1 | 5:00 PM – 6:00 PM | Duration: 60 min
> **Folder:** `day1/06_data_drift_anomaly/`
> **Status:** 🔲 Pending Build

---

## 🎯 Learning Objectives
1. Define and distinguish between feature drift, concept drift, and label drift
2. Implement statistical drift detection using KS test and PSI
3. Train an Isolation Forest for unsupervised anomaly detection
4. Design a monitoring architecture with alert thresholds

---

## 🧠 Core Concepts

### 1. Why Models Decay in Production
> "A model that was 95% accurate at training can silently decay to 60% in production within 3 months."

**Root cause:** The world changes, but the model doesn't.

### 2. Three Types of Drift
| Type | What Changes | Example |
|------|-------------|---------|
| **Feature Drift (Covariate Shift)** | Input distribution P(X) | Customer demographics shift post-pandemic |
| **Concept Drift** | Relationship P(Y\|X) | Customer behaviour changes — old signals no longer predict churn |
| **Label Drift (Prior Shift)** | Output distribution P(Y) | Fraud rate doubles during economic crisis |

**Real-world triggers:** Seasonality, market crashes, regulatory changes, new customer segments, sensor failures, data pipeline bugs

### 3. Drift Detection Methods

#### PSI (Population Stability Index)
> Most widely used in banking/insurance for credit model monitoring

**Formula:**
```
PSI = Σ (Actual% - Expected%) × ln(Actual% / Expected%)
```

**Thresholds:**
| PSI Value | Interpretation | Action |
|-----------|---------------|--------|
| < 0.1 | Stable — no change | Monitor normally |
| 0.1 – 0.2 | Slight shift — watch | Investigate feature |
| > 0.2 | Major shift — alert | Retrain model |

```python
def compute_psi(expected, actual, buckets=10):
    expected_perc = np.histogram(expected, bins=buckets)[0] / len(expected)
    actual_perc = np.histogram(actual, bins=buckets)[0] / len(actual)
    # Avoid division by zero
    expected_perc = np.clip(expected_perc, 1e-6, None)
    actual_perc = np.clip(actual_perc, 1e-6, None)
    psi = np.sum((actual_perc - expected_perc) * np.log(actual_perc / expected_perc))
    return psi
```

#### KS Test (Kolmogorov-Smirnov)
```python
from scipy.stats import ks_2samp
stat, p_value = ks_2samp(reference_data, current_data)
if p_value < 0.05:
    print("DRIFT DETECTED — distributions are significantly different")
```

#### Chi-Square Test (Categorical Features)
```python
from scipy.stats import chi2_contingency
chi2, p, dof, expected = chi2_contingency(contingency_table)
```

### 4. Isolation Forest — Unsupervised Anomaly Detection
**Why "isolation"?** Anomalies are few and different → they're isolated by random splits faster than normal points.

```python
from sklearn.ensemble import IsolationForest

iso_forest = IsolationForest(
    n_estimators=100,
    contamination=0.05,  # Expected 5% anomaly rate
    random_state=42
)
iso_forest.fit(X_train)

# -1 = anomaly, 1 = normal
predictions = iso_forest.predict(X_test)
anomaly_scores = iso_forest.score_samples(X_test)  # More negative = more anomalous
```

**Key parameters:**
- `contamination` — Expected proportion of anomalies (0.01–0.20)
- `n_estimators` — Number of trees (more = more stable)
- `max_samples` — Subsample per tree (default: 'auto')

### 5. MLOps Monitoring Architecture
```
Production Traffic
       ↓
Feature Store / Logging Layer
       ↓
Drift Monitor (PSI, KS daily batch)
       ↓
   PSI > 0.2?    Anomaly Rate > threshold?
       ↓                    ↓
   ALERT               ALERT
       ↓                    ↓
Data Science Team → Investigate → Retrain? → Deploy v2
```

**Monitoring cadence:**
| Data Volume | Recommended Cadence |
|-------------|-------------------|
| < 10K/day | Weekly batch report |
| 10K–1M/day | Daily batch report |
| > 1M/day | Hourly streaming monitor |

---

## 📊 Diagrams & Visuals Required

| # | Diagram | Type | Notebook Cell |
|---|---------|------|---------------|
| 1 | Reference vs. current distribution overlay (drift demo) | Dual KDE plot | Cell 4 |
| 2 | PSI score bar chart across all features | Horizontal bar with thresholds | Cell 6 |
| 3 | Isolation Forest anomaly scatter plot in 2D PCA space | Scatter with color-coded anomalies | Cell 9 |
| 4 | MLOps monitoring architecture | Annotated flow diagram | Cell 11 |
| 5 | Drift score timeline (rolling window over weeks) | Line chart with alert threshold | Cell 12 |

---

## 🏋️ Activities

### Activity 1 — Detect Feature Drift (20 min)
- Generate reference distribution (month 1 data) and drifted distribution (month 6 data)
- Compute PSI for all 8 features
- Build a bar chart flagging drifted features (PSI > 0.2)

### Activity 2 — Isolation Forest Anomaly Detection (20 min)
- Train Isolation Forest on "normal" production data
- Inject 5% synthetic anomalies
- Visualize anomalies in 2D PCA space
- Compare anomaly score distribution between normal and anomalous points

### Activity 3 — Build a Drift Dashboard (code)
- Create a 3-panel matplotlib figure:
  - Panel 1: Distribution overlay (reference vs. current)
  - Panel 2: PSI bar chart
  - Panel 3: Anomaly score histogram

---

## 📝 Notebook Cell Plan

```
Cell 01 [MD]   → Session intro: why models decay
Cell 02 [MD]   → Three types of drift with examples
Cell 03 [Code] → Simulate feature drift (gaussian shift)
Cell 04 [Code] → Distribution overlay plot (KDE dual)
Cell 05 [MD]   → PSI formula and thresholds explained
Cell 06 [Code] → Compute PSI for all features → bar chart
Cell 07 [Code] → KS test for drift detection
Cell 08 [MD]   → Isolation Forest — how it works
Cell 09 [Code] → Train Isolation Forest → PCA scatter plot
Cell 10 [Code] → Anomaly score distribution comparison
Cell 11 [Code] → MLOps monitoring architecture diagram
Cell 12 [Code] → Drift score timeline chart
Cell 13 [MD]   → Key Takeaways + Quiz
```

---

## 📁 Files to Create

```
day1/06_data_drift_anomaly/
├── README.md
└── notebook.ipynb
```

---

## 📝 Key Takeaways
- A deployed model without monitoring is a ticking time bomb
- Feature drift ≠ concept drift — different causes, different responses
- PSI > 0.2 is the universal banking industry signal for "retrain now"
- Isolation Forest requires NO labeled anomaly data — perfect for production monitoring
- Set drift thresholds conservatively at first; tighten them as you build operational confidence

---

## ❓ Quiz Questions
1. What is the difference between feature drift and concept drift?
2. What PSI threshold should trigger a model retraining review?
3. Why is Isolation Forest called "isolation" forest — what does it isolate?
4. What is a "reference window" in drift monitoring?
5. Name 2 real-world events that would cause concept drift in a credit scoring model

---

## 📖 Further Reading
- [Evidently AI — ML Monitoring Docs](https://docs.evidentlyai.com/)
- Liu et al. (2008) — "Isolation Forest" (original paper)
- [NannyML — Concept Drift Detection](https://nannyml.com/)
- [Towards Data Science — PSI Tutorial](https://towardsdatascience.com/population-stability-index-psi-explain-like-im-5-aed7e16e59e9)
