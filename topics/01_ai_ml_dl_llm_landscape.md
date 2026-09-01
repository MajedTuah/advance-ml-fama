# 🧠 Topic 01 — AI, ML, DL & LLM Landscape
> **Schedule:** Day 1 | 9:00 AM – 10:00 AM | Duration: 60 min
> **Folder:** `day1/01_ai_ml_dl_llm_landscape/`
> **Status:** 🔲 Pending Build

---

## 🎯 Learning Objectives
By the end of this session, learners will be able to:
1. Distinguish between AI, ML, Deep Learning, and LLMs with concrete examples
2. Map real business problems to the correct technology category
3. Explain the evolutionary timeline from rule-based AI to modern LLMs
4. Understand where LLMs fit in the data-driven enterprise

---

## 🧠 Core Concepts

### 1. The AI Hierarchy
- **Artificial Intelligence** — Umbrella field; machines that simulate human intelligence
- **Machine Learning** — Learns patterns from data without explicit rules
- **Deep Learning** — Subset of ML using multi-layer neural networks; excels at unstructured data (images, text, audio)
- **Large Language Models (LLMs)** — Foundation models trained on massive text corpora; GPT, Gemini, Claude, LLaMA

### 2. ML Task Types
| Task Type | Description | Example |
|-----------|-------------|---------|
| Supervised — Classification | Predict a category | Spam detection, Churn |
| Supervised — Regression | Predict a number | House price, Sales forecast |
| Unsupervised — Clustering | Group similar data | Customer segmentation |
| Unsupervised — Dim. Reduction | Compress features | PCA, UMAP |
| Reinforcement Learning | Learn by reward | Game AI, Robotics |
| Self-supervised / Foundation | Learn from data itself | BERT, GPT |

### 3. LLM Specifics
- What makes a model "large"? → Parameters (billions), training tokens (trillions), compute (FLOPS)
- Key milestones: GPT-1 (2018) → BERT (2018) → GPT-3 (2020) → ChatGPT (2022) → GPT-4 / Gemini (2023) → Llama 3 / Gemini 2.0 (2024)
- **Prompt Engineering** — Zero/few-shot; no retraining needed
- **Fine-tuning** — Update weights on domain data; task-specific
- **RAG (Retrieval-Augmented Generation)** — Inject real-time knowledge; no hallucination risk

### 4. Choosing the Right Tool
| Scenario | Best Choice | Why |
|----------|-------------|-----|
| Tabular fraud detection | Classic ML (XGBoost) | Interpretable, fast, accurate |
| Customer churn | Classic ML + XAI | Regulatory explainability needed |
| Document summarization | LLM (RAG) | Unstructured text, zero labeled data |
| Image defect detection | Deep Learning (CNN) | Spatial feature extraction |
| Real-time recommendation | ML + feature store | Low latency, structured data |

---

## 📊 Diagrams & Visuals Required

| # | Diagram | Type | Tool |
|---|---------|------|------|
| 1 | Nested circles — AI ⊃ ML ⊃ DL ⊃ LLM | Matplotlib patches | `notebook.ipynb` Cell 4 |
| 2 | Timeline: Key AI milestones 1950–2024 | Horizontal bar chart | `notebook.ipynb` Cell 6 |
| 3 | Radar chart: Speed vs Cost vs Accuracy vs Interpretability | Matplotlib radar | `notebook.ipynb` Cell 8 |
| 4 | Decision tree: "Which tech should I use?" | Matplotlib annotated tree | `notebook.ipynb` Cell 10 |

---

## 🏋️ Activities

### Activity 1 — Business Problem Classification (15 min)
**Format:** Group discussion / individual worksheet
Given 10 business problems, classify each as AI/ML/DL/LLM and justify:
1. Predict whether a customer will default on a loan
2. Generate a personalized email for a prospect
3. Detect a manufacturing defect from a conveyor belt camera
4. Group customers into segments without labels
5. Recommend the next product to buy
6. Transcribe a customer service call
7. Forecast electricity demand for the next 7 days
8. Detect insider trading from chat logs
9. Answer employee questions from a company policy PDF
10. Identify the most important features driving churn

### Activity 2 — Parameter Scale Visualization (10 min)
**Format:** Code exercise in notebook
- Plot the growth of model parameters from 1950 to 2024 (log scale)
- Highlight the "transformer inflection point" (2017)

### Activity 3 — Build the Hierarchy Diagram (code)
- Use `matplotlib.patches` to draw nested circles with labels and color coding

---

## 📝 Notebook Cell Plan

```
Cell 01 [MD]   → Session title, objectives, agenda
Cell 02 [Code] → Import libraries (matplotlib, numpy, pandas)
Cell 03 [MD]   → AI vs ML vs DL — concept explanation
Cell 04 [Code] → Draw nested hierarchy diagram (patches)
Cell 05 [MD]   → ML task types table + explanations
Cell 06 [Code] → Timeline chart (horizontal bar, annotated milestones)
Cell 07 [MD]   → LLM: prompt engineering vs fine-tuning vs RAG
Cell 08 [Code] → Radar chart: capability comparison across 5 model types
Cell 09 [MD]   → Business use case mapping
Cell 10 [Code] → Decision tree: which technology to choose
Cell 11 [MD]   → Key Takeaways
Cell 12 [MD]   → Quiz (5 questions)
```

---

## 📁 Files to Create

```
day1/01_ai_ml_dl_llm_landscape/
├── README.md         ← Participant-facing session guide
└── notebook.ipynb    ← Hands-on Jupyter notebook
```

---

## 📝 Key Takeaways
- AI is the parent field; ML, DL, and LLMs are progressively specialized subsets
- LLMs are pattern-matching at scale — not reasoning engines (yet)
- Most enterprise ML problems don't need LLMs — classical ML still dominates tabular data
- Choosing the wrong paradigm wastes months and millions

---

## ❓ Quiz Questions
1. What is the key difference between supervised and unsupervised learning?
2. Why would you choose classical ML over a fine-tuned LLM for fraud detection?
3. What does "self-supervised learning" mean and which model types use it?
4. Name 2 trade-offs between Deep Learning vs. a simple Logistic Regression
5. What is RAG and when would you use it over fine-tuning?

---

## 📖 Further Reading
- [Andrej Karpathy — "Software 2.0"](https://karpathy.medium.com/software-2-0-a64152b37c35)
- [A Visual Intro to Machine Learning](http://www.r2d3.us/visual-intro-to-machine-learning-part-1/)
- Deep Learning Book — Chapter 1 (Goodfellow et al.)
- Google ML Crash Course — https://developers.google.com/machine-learning/crash-course
