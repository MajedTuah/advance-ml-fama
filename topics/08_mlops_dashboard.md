# 📊 Topic 08 — MLOps Dashboard
> **Schedule:** Day 1 | 9:00 PM – 10:00 PM | Duration: 60 min
> **Folder:** `day1/08_mlops_dashboard/`
> **Status:** 🔲 Pending Build

---

## 🎯 Learning Objectives
1. Design a structured MLOps monitoring dashboard for a deployed model
2. Implement model performance tracking over time using simulated production data
3. Build drift and anomaly summary visualizations
4. Create a multi-panel dashboard with threshold alerts and export capability

---

## 🧠 Core Concepts

### 1. What to Monitor — The Four Pillars
| Pillar | Metrics | Why It Matters |
|--------|---------|----------------|
| **Model Performance** | Accuracy, AUC, F1, Precision, Recall | Is the model still good? |
| **Data Health** | PSI per feature, null rates, schema violations | Is input data still clean? |
| **System Health** | API latency (p50/p95/p99), error rate, throughput | Is the service reliable? |
| **Business Impact** | False positive cost, missed revenue, churn rate | Is the model still valuable? |

### 2. Golden Signals (from Google SRE)
- **Latency** — How long does a prediction take? (p50, p95, p99)
- **Traffic** — How many requests per second/minute?
- **Errors** — What % of requests fail?
- **Saturation** — How close to resource limits (CPU, memory, GPU)?

### 3. SLA / SLO / SLI Definitions
| Term | Full Name | Example |
|------|-----------|---------|
| **SLI** | Service Level Indicator | 99.2% requests succeed |
| **SLO** | Service Level Objective | Target: ≥ 99.5% uptime |
| **SLA** | Service Level Agreement | Contractual: 99.0% or penalty |

### 4. Dashboard Layout Design
```
┌─────────────────────────────────────────────────────────────────┐
│  MLOps Dashboard — Credit Default Model v2.1                    │
│  Updated: 2024-01-15 08:00 UTC                                  │
├────────────────────┬────────────────────┬───────────────────────┤
│  Model Accuracy    │  API Latency (ms)  │  Request Volume       │
│  (rolling 7d)      │  p50 / p95 / p99   │  (hourly)             │
│  [Line chart]      │  [Line chart]      │  [Bar chart]          │
├────────────────────┼────────────────────┼───────────────────────┤
│  Feature Drift     │  Anomaly Alert     │  Error Rate           │
│  Heatmap           │  Log (last 7d)     │  (hourly %)           │
│  [Heatmap]         │  [Table/text]      │  [Line chart]         │
└────────────────────┴────────────────────┴───────────────────────┘
```

### 5. Key Dashboard Components to Build

#### A. Model Accuracy Timeline
```python
import matplotlib.pyplot as plt
import numpy as np

weeks = np.arange(1, 13)
accuracy = [0.93, 0.92, 0.91, 0.90, 0.88, 0.86, 0.84, 0.81, 0.78, 0.75, 0.71, 0.68]
threshold = 0.80

fig, ax = plt.subplots()
ax.plot(weeks, accuracy, 'b-o', label='Model Accuracy')
ax.axhline(y=threshold, color='red', linestyle='--', label=f'Alert Threshold ({threshold})')
ax.fill_between(weeks, accuracy, threshold,
                where=[a < threshold for a in accuracy],
                color='red', alpha=0.2, label='Below threshold')
ax.set_xlabel('Week')
ax.set_ylabel('Accuracy')
ax.set_title('Model Accuracy Over Time')
ax.legend()
```

#### B. Feature Drift Heatmap
```python
import seaborn as sns
import pandas as pd

features = ['age', 'income', 'credit_score', 'debt_ratio', 'employment_years']
weeks = [f'W{i}' for i in range(1, 9)]
psi_matrix = np.random.uniform(0, 0.35, size=(len(features), len(weeks)))

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(psi_matrix, annot=True, fmt='.2f',
            xticklabels=weeks, yticklabels=features,
            cmap='RdYlGn_r',  # Red = high drift
            vmin=0, vmax=0.3, ax=ax)
ax.set_title('Feature Drift (PSI) Heatmap — Higher = More Drift')
```

### 6. Alert Design Principles
- **Set thresholds deliberately** — Not too tight (alert fatigue) or too loose (blind spots)
- **Layer alerts by severity:** INFO → WARNING → CRITICAL
- **Each alert needs a runbook** — Document what to do when it fires
- **Alert on SLOs, not metrics** — "AUC dropped below 0.80" not "AUC is 0.79"

### 7. MLOps Tooling Landscape
| Tool | Purpose | Open Source? |
|------|---------|-------------|
| **MLflow** | Experiment tracking + model registry | ✅ Yes |
| **Evidently AI** | Data/model drift monitoring | ✅ Yes |
| **Grafana + Prometheus** | Infrastructure + custom metrics | ✅ Yes |
| **Streamlit** | Custom monitoring web apps | ✅ Yes |
| **Azure ML Monitor** | Cloud-native ML monitoring | ❌ Paid |
| **Weights & Biases** | Full MLOps platform | 🟡 Freemium |

---

## 📊 Diagrams & Visuals Required

| # | Diagram | Type | Notebook Cell |
|---|---------|------|---------------|
| 1 | 6-panel dashboard (accuracy, latency, traffic, drift, anomaly, errors) | `plt.subplots(2,3)` | Cell 5 |
| 2 | Feature drift heatmap (features × weeks) | `seaborn.heatmap` | Cell 7 |
| 3 | Model accuracy decay with alert threshold line | Line chart + fill_between | Cell 9 |
| 4 | MLOps tooling architecture overview | Annotated layered diagram | Cell 11 |

---

## 🏋️ Activities

### Activity 1 — Build the 6-Panel Dashboard (30 min)
Using simulated production data (12 weeks):
- Panel 1: Model accuracy over time (with threshold)
- Panel 2: API latency p50/p95/p99 over time
- Panel 3: Daily request volume bar chart
- Panel 4: Feature drift PSI heatmap
- Panel 5: Anomaly detection alert timeline
- Panel 6: Error rate % over time

### Activity 2 — Add Alerts and Annotations (15 min)
- Add red dashed lines at threshold values
- Annotate the point where accuracy first drops below threshold
- Add `plt.text()` annotations for "Retraining triggered" events

### Activity 3 — Export as Report (code)
- `plt.savefig('reports/mlops_dashboard_week12.png', dpi=150, bbox_inches='tight')`
- Simulate a weekly report generation function

---

## 📝 Notebook Cell Plan

```
Cell 01 [MD]   → Session intro: "You can't manage what you don't measure"
Cell 02 [MD]   → Four pillars of ML monitoring
Cell 03 [MD]   → Golden signals + SLA/SLO/SLI explained
Cell 04 [MD]   → Dashboard design layout sketch
Cell 05 [Code] → Generate simulated 12-week production data
Cell 06 [Code] → 6-panel matplotlib dashboard
Cell 07 [Code] → Feature drift heatmap (seaborn)
Cell 08 [MD]   → Alert design principles
Cell 09 [Code] → Model accuracy decay with alert annotations
Cell 10 [MD]   → MLOps tooling landscape overview
Cell 11 [Code] → MLOps architecture diagram
Cell 12 [Code] → Export dashboard as PNG report
Cell 13 [MD]   → Key Takeaways + Quiz
```

---

## 📁 Files to Create

```
day1/08_mlops_dashboard/
├── README.md
└── notebook.ipynb
```

---

## 📝 Key Takeaways
- An MLOps dashboard is the heartbeat monitor of your deployed model
- Monitor model health, data health, and system health simultaneously
- Design alerts for your audience: engineering dashboards ≠ executive dashboards
- Every alert must have a linked runbook describing the response action
- Monitoring is a continuous investment — build it from day 1 of deployment

---

## ❓ Quiz Questions
1. What are the four "golden signals" from Google SRE?
2. What is the difference between an SLO and an SLA?
3. What is "alert fatigue" and how do you prevent it?
4. Which metric would you use to detect that your model's input data is degrading?
5. Name 2 open-source tools specifically designed for ML model monitoring

---

## 📖 Further Reading
- [Google SRE Book — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Evidently AI — ML Monitoring Guide](https://docs.evidentlyai.com/user-guide/monitoring)
- [MLflow Model Serving](https://mlflow.org/docs/latest/models.html)
- [Chip Huyen — "Designing ML Systems" Chapter 8: Data Distribution Shifts](https://www.oreilly.com/library/view/designing-machine-learning/9781098107963/)
