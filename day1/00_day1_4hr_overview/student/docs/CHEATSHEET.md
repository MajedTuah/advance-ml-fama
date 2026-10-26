# Day 1 cheat sheet

## Choosing the approach
| Data | Start with |
|---|---|
| Rows and columns (tabular) | Classic ML: gradient boosting, logistic regression |
| Images, audio, raw signals | Deep learning |
| Free text, documents, conversation | An LLM (with retrieval over your documents) |

## Leakage: the four kinds
| Kind | Example | Fix |
|---|---|---|
| Target leakage | `days_to_default` | keep only what is known at decision time |
| Train-test contamination | scaler fitted on all rows | split first, fit inside a `Pipeline` |
| Temporal leakage | random split across years | time-ordered split, `TimeSeriesSplit` |
| Group leakage | same customer in train and test | `GroupKFold` on the customer id |

**The safe order:** full data → time-ordered split → fit the Pipeline on train → tune on validation folds → score the newest 20% once.

## Missing data
| Type | Meaning | Fix |
|---|---|---|
| MCAR | random | simple imputation |
| MAR | depends on another column | impute using that column |
| MNAR | depends on the value itself | add a `was_missing` flag and investigate |

## Training, tuning, tracking
- **Parameters** are learned by `fit()`. **Hyperparameters** are set by you.
- Tune with cross-validation on the training rows. **Never** let the test set choose.
- Search: grid wastes trials, random beats grid, Bayesian (Optuna TPE) learns from earlier trials.
- Every MLflow run logs **params, metrics, artefacts, and tags** (git commit, data version).

## Explainability
- SHAP is additive: `f(x) = E[f(X)] + Σ φᵢ`. Beeswarm = global, waterfall = one applicant.
- Narrative formula: **observed value → direction and size → one action that would change the decision.**

## Drift
| Kind | What changes | How you see it |
|---|---|---|
| Feature drift | P(X), the inputs | PSI / KS on every input, immediately |
| Concept drift | P(y \| X), the rules | performance on new labels, months later |
| Label drift | P(y), the outcome rate | predicted vs realised default rate |

**PSI bands:** < 0.10 stable · 0.10–0.20 watch · ≥ 0.20 alert. PSI above 1 usually means a broken pipeline.
**KS** says *whether* distributions differ; with big samples it flags tiny shifts. PSI says whether it is *big enough to act on*.

## Serving
| Status | Meaning |
|---|---|
| 200 | OK |
| 422 | input failed validation (Pydantic), the model never ran |
| 5xx | a bug on the server: it belongs on the error-rate panel |

Load the model **once** at startup. Validate **every** input. Expose `/health`.
Docker: the **image** is the frozen blueprint, the **container** is a running copy. Copy `requirements.txt` first so the dependency layer stays cached.

## Monitoring
- Four pillars: **model, data, system, business**.
- Golden signals: **latency (p99), traffic, errors, saturation**.
- Page someone only when an **SLO** breaks. Everything else stays on the dashboard.

| SLO (example) | Pillar |
|---|---|
| AUC ≥ 0.75 on the monthly labelled sample | Model |
| PSI < 0.2 on the top 10 features | Data |
| p99 latency < 300 ms, errors < 1% | System |
| Expected loss within 10% of plan | Business |

## From laptop to Azure ML
| Today | Azure ML |
|---|---|
| `scripts/main.py` + `config.yaml` | command job on a compute cluster |
| Optuna study | sweep job |
| local MLflow | MLflow tracking in the workspace |
| `model.joblib` | model registry |
| FastAPI + Docker | managed online endpoint |
| PSI / KS checks | model monitoring |
