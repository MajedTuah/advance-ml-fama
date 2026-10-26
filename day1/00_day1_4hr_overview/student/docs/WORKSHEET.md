# Day 1 worksheet

Fill this in as you go. It stays on your laptop: it is yours to keep.

---

## Ice breaker · Would you ship it?
A model scores **99% accuracy** on a loan book where 1% of borrowers default.

My vote (A ship / B need more metrics / C reject): ____

Which metric would I ask for, and why? ______________________________________________

---

## Module 1 · Find every leak
For each column: *would I know this value at the moment the loan is approved?*

| Column | LEAK / RISKY / SAFE | Why |
|---|---|---|
| customer_id | | |
| loan_approval_date | | |
| loan_amount | | |
| annual_income | | |
| employment_years | | |
| credit_score | | |
| days_since_last_payment | | |
| existing_loans | | |
| loan_type | | |
| region | | |
| days_to_default | | |
| post_approval_status_flag | | |

**My pipeline checklist** (notebook 01, part D)
- [ ] Split by time first: the oldest 80% trains, the newest 20% tests
- [ ] Imputer, scaler and encoder all inside one `Pipeline`
- [ ] `fit()` only on training rows
- [ ] ROC-AUC and recall reported on the newest 20%, once

Leaky model ROC-AUC: ______  Clean model ROC-AUC: ______  Clean model recall: ______

---

## Module 2 · Train, tune, track
| Run | test_size / max_iter | accuracy | recall | f1 |
|---|---|---|---|---|
| run 1 | | | | |
| run 2 | | | | |

Optuna best CV ROC-AUC: ______  Best params: ______________________________

The hyperparameter that mattered most: ______________

---

## Module 3 · Explain it to a branch manager
Applicant 0. Three sentences, no jargon.

1. **The main driver and its value:** ______________________________________________
2. **Direction and size, in plain words:** _________________________________________
3. **One action that would change the decision:** ___________________________________

Neighbour's verdict: could they act on it? ☐ yes ☐ not yet

**My PSI table** (notebook 03, part C)

| Feature | PSI | KS p-value | STABLE / WATCH / ALERT |
|---|---|---|---|
| credit_utilization | | | |
| age | | | |
| annual_income | | | |
| credit_score | | | |
| employment_years | | | |
| loan_amount | | | |

What business event could explain the ALERT and WATCH features? __________________________

---

## Module 4 · Serve and monitor
- [ ] Image built (or uvicorn running)
- [ ] `/health` answers
- [ ] A valid request returns 200
- [ ] `age = 7` returns 422
- [ ] A missing field returns 422

Which SLOs are broken in the latest week of the dashboard? ______________________________

Who should be paged, and who should just look at the dashboard? _________________________

---

## My back-to-work action plan
1. **One pipeline I will audit for leakage:** ________________________________________
2. **One script I will refactor into config and modules:** ____________________________
3. **One prediction I will explain to a stakeholder:** ________________________________
4. **One drift or alert check I will add:** __________________________________________
5. **My first step on Monday, and my deadline:** _____________________________________

| 30 days | 60 days | 90 days |
|---|---|---|
| Leakage audit and a Pipeline on one live model | Scripts, Optuna and MLflow for that model | An API, drift checks and a dashboard |
