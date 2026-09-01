# 🔍 Topic 05 — Explainability AI (XAI) for Business Decisions
> **Schedule:** Day 1 | 4:00 PM – 5:00 PM | Duration: 60 min
> **Folder:** `day1/05_explainability_xai/`
> **Status:** 🔲 Pending Build

---

## 🎯 Learning Objectives
1. Explain the spectrum from interpretable to black-box models
2. Generate SHAP values and interpret both global and local explanations
3. Use LIME to explain a single prediction to a non-technical stakeholder
4. Translate model explanations into actionable business language

---

## 🧠 Core Concepts

### 1. Why XAI Matters in Business
| Reason | Business Context |
|--------|-----------------|
| **Regulatory compliance** | GDPR Art. 22 (EU), FINRA, MAS FEAT, OJK |
| **Stakeholder trust** | "Why should I deploy a model I can't explain?" |
| **Model debugging** | Find spurious correlations, detect shortcuts |
| **Bias & fairness** | Detect protected-attribute leakage |
| **Auditability** | Explain past decisions to regulators |

### 2. The Transparency Spectrum
```
INTERPRETABLE ────────────────────────── BLACK-BOX
     │                                        │
Linear Reg → Decision Tree → Random Forest → Neural Net → LLM
     │              │               │              │
  Full global    Full local     Post-hoc XAI   Post-hoc XAI
 transparency   transparency     needed          needed
```

### 3. SHAP (SHapley Additive exPlanations)
**Theory:** From cooperative game theory — each feature's contribution is its average marginal contribution across all possible feature orderings.

**Key properties:**
- **Local accuracy:** SHAP values sum to model output (minus baseline)
- **Consistency:** If feature matters more, SHAP value increases
- **Dummy:** Features with no impact get SHAP = 0

**SHAP Plot Types:**
| Plot | What It Shows | Audience |
|------|--------------|----------|
| **Summary (Beeswarm)** | Global: all features × all samples | Data scientist |
| **Bar chart** | Global: mean absolute SHAP per feature | Manager |
| **Waterfall** | Local: single prediction breakdown | Business user |
| **Force plot** | Local: interactive prediction walkthrough | Executive |
| **Dependence plot** | Feature X vs. SHAP value (interaction) | Analyst |

```python
import shap

# Tree-based models (fast)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot (global)
shap.summary_plot(shap_values, X_test, feature_names=feature_names)

# Waterfall for one prediction
shap.waterfall_plot(shap.Explanation(
    values=shap_values[0],
    base_values=explainer.expected_value,
    data=X_test.iloc[0]
))
```

### 4. LIME (Local Interpretable Model-agnostic Explanations)
**Theory:** Perturb the input → observe output changes → fit a local linear model in the neighborhood → use linear coefficients as explanation

```python
from lime import lime_tabular

explainer = lime_tabular.LimeTabularExplainer(
    X_train.values,
    feature_names=feature_names,
    class_names=['No Default', 'Default'],
    mode='classification'
)
exp = explainer.explain_instance(X_test.iloc[0].values, model.predict_proba)
exp.show_in_notebook()
```

**SHAP vs. LIME:**
| Dimension | SHAP | LIME |
|-----------|------|------|
| Scope | Global + Local | Local only |
| Theory | Game theory (exact) | Local linear approximation |
| Speed | Fast for tree models | Slower (perturbation-based) |
| Consistency | Guaranteed | Not guaranteed |
| Text/Image | Requires specific explainers | Native support |

### 5. Business Translation Framework
**From SHAP to narrative:**
```
Technical: "Feature 'credit_utilization' has SHAP value +0.23 for sample #1042"
Business:  "High credit card utilization (87%) increased this applicant's
            default probability by 23 percentage points."

Technical: "Feature 'employment_years' has SHAP value -0.15"
Business:  "A stable employment history (8 years) reduced default probability
            by 15 percentage points — a positive signal."
```

**Counterfactual:** "If your credit utilization dropped below 30%, your application would likely be approved."

---

## 📊 Diagrams & Visuals Required

| # | Diagram | Type | Notebook Cell |
|---|---------|------|---------------|
| 1 | Transparency spectrum axis | Annotated matplotlib axis | Cell 3 |
| 2 | SHAP beeswarm summary plot | `shap.summary_plot()` | Cell 6 |
| 3 | SHAP waterfall — single prediction | `shap.waterfall_plot()` | Cell 8 |
| 4 | LIME explanation — single prediction | `lime` in-notebook display | Cell 10 |
| 5 | Business report snippet with SHAP bar chart | Styled matplotlib bar | Cell 12 |

---

## 🏋️ Activities

### Activity 1 — Global SHAP Analysis (20 min)
- Train a Gradient Boosting model on credit risk dataset
- Generate SHAP summary (beeswarm) plot
- Answer: Which 3 features drive the most predictions globally?

### Activity 2 — Local Explanation to Business Narrative (15 min)
- Pick the single most badly predicted sample (highest error)
- Generate SHAP waterfall plot
- Write a 3-sentence plain-English explanation of the prediction as if presenting to a Risk Committee

### Activity 3 — LIME for Regulatory Audience (10 min)
- Explain the same sample using LIME
- Compare: Is the LIME explanation consistent with SHAP?
- Which format is more accessible to a non-technical executive?

---

## 📝 Notebook Cell Plan

```
Cell 01 [MD]   → Session intro & why XAI matters in business
Cell 02 [MD]   → Transparency spectrum
Cell 03 [Code] → Transparency spectrum diagram
Cell 04 [MD]   → SHAP theory explained (game theory, Shapley values)
Cell 05 [Code] → Train GBM on credit risk data
Cell 06 [Code] → SHAP summary (beeswarm) + bar chart
Cell 07 [MD]   → Reading SHAP plots for business decisions
Cell 08 [Code] → SHAP waterfall for single prediction
Cell 09 [MD]   → Business narrative framework
Cell 10 [Code] → LIME explanation for same prediction
Cell 11 [MD]   → SHAP vs. LIME comparison table
Cell 12 [MD]   → Key Takeaways + Quiz
```

---

## 📁 Files to Create

```
day1/05_explainability_xai/
├── README.md
└── notebook.ipynb
```

---

## 📝 Key Takeaways
- Accuracy without explainability is unacceptable in regulated industries (banking, insurance, healthcare)
- SHAP values are **additive** — they sum to the model prediction (minus baseline)
- LIME creates a local approximation; it's less theoretically grounded than SHAP but easier to communicate
- Counterfactual explanations are the most actionable format for end users
- Always pair your SHAP chart with 2–3 plain-language sentences

---

## ❓ Quiz Questions
1. Which regulation in the EU requires explainability for automated decisions affecting individuals?
2. What is the difference between global and local explainability?
3. Why can't you use standard feature importance from Random Forest as a SHAP substitute?
4. What is a counterfactual explanation? Give an example from finance.
5. How would you present a SHAP waterfall plot to a Risk Committee with no ML background?

---

## 📖 Further Reading
- [SHAP Documentation](https://shap.readthedocs.io/)
- [LIME GitHub](https://github.com/marcotcr/lime)
- Lundberg & Lee (2017) — "A Unified Approach to Interpreting Model Predictions"
- [Google PAIR — People + AI Guidebook](https://pair.withgoogle.com/guidebook)
- [MAS FEAT Principles (Singapore AI Fairness)](https://www.mas.gov.sg/publications/monographs-or-information-paper/2019/feat-principles)
