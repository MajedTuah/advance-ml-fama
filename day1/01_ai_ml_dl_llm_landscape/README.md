# 🧠 Session 01 — AI, ML, DL & LLM Landscape

> **Day 1 | 9:00 AM – 10:00 AM | Duration: 60 minutes**

---

## 🎯 What You'll Learn

By the end of this session you will be able to:

1. **Distinguish** between AI, ML, Deep Learning, and LLMs with concrete examples
2. **Map** real business problems to the correct technology category
3. **Explain** the evolutionary timeline from rule-based AI to modern LLMs
4. **Decide** when to use ML vs. DL vs. LLM for a given problem

---

## ⏱️ Session Agenda

| Time | Activity | Format |
|------|---------|--------|
| 0:00 – 0:10 | The AI Hierarchy — concepts + diagram | Instructor-led |
| 0:10 – 0:20 | ML Task Types — table walkthrough | Instructor-led |
| 0:20 – 0:30 | LLM Landscape — milestones + timeline | Instructor-led + Notebook |
| 0:30 – 0:40 | **Activity 1** — Business Problem Classification | Group/Individual |
| 0:40 – 0:50 | **Activity 2** — Parameter Scale Visualization | Notebook |
| 0:50 – 1:00 | Capability Radar Chart + Decision Framework | Notebook + Debrief |

---

## 🧠 Key Concepts

### The AI Hierarchy (Nested)

```
╔══════════════════════════════════════════╗
║           ARTIFICIAL INTELLIGENCE        ║
║   ╔══════════════════════════════════╗   ║
║   ║       MACHINE LEARNING           ║   ║
║   ║   ╔══════════════════════════╗   ║   ║
║   ║   ║     DEEP LEARNING        ║   ║   ║
║   ║   ║  ╔════════════════════╗  ║   ║   ║
║   ║   ║  ║  LARGE LANGUAGE    ║  ║   ║   ║
║   ║   ║  ║      MODELS        ║  ║   ║   ║
║   ║   ║  ╚════════════════════╝  ║   ║   ║
║   ║   ╚══════════════════════════╝   ║   ║
║   ╚══════════════════════════════════╝   ║
╚══════════════════════════════════════════╝
```

### ML Task Types at a Glance

| Task | Description | Business Example |
|------|-------------|-----------------|
| **Classification** | Predict a category | Fraud? Yes/No. Churn? High/Low |
| **Regression** | Predict a number | Loan amount, Sales forecast |
| **Clustering** | Group without labels | Customer segments |
| **Dim. Reduction** | Compress features | PCA for visualization |
| **Reinforcement Learning** | Learn by reward | Trading bot, Robotics |
| **Foundation / LLM** | Learn from raw text at scale | Summarization, Q&A, Code gen |

### LLM Adaptation Strategies

| Strategy | What Changes | When to Use |
|----------|-------------|-------------|
| **Prompt Engineering** | Only the prompt, no training | Quick prototyping, zero labeled data |
| **Fine-tuning** | Model weights updated on your data | Domain-specific tasks, enough labeled examples |
| **RAG** | Retrieval layer added at inference | Dynamic knowledge, reduce hallucination |

---

## 🏋️ Activities

### Activity 1 — Business Problem Classifier (15 min)

For each business problem below, decide: **AI / ML / DL / LLM** and write your justification.

| # | Business Problem | Your Answer | Justification |
|---|----------------|-------------|--------------|
| 1 | Predict whether a customer will default on a loan | | |
| 2 | Generate a personalized email for a prospect | | |
| 3 | Detect a manufacturing defect from a conveyor belt camera | | |
| 4 | Group customers into segments without any labels | | |
| 5 | Recommend the next product to buy | | |
| 6 | Transcribe a customer service call | | |
| 7 | Forecast electricity demand for the next 7 days | | |
| 8 | Detect insider trading from internal chat logs | | |
| 9 | Answer employee questions from a company policy PDF | | |
| 10 | Identify the most important features driving customer churn | | |

> 💡 **Hint:** There is often more than one valid answer — justify your reasoning!

### Activity 2 — Parameter Scale Visualization (10 min)
Open `notebook.ipynb` → run **Cell 06** to plot the growth of AI model parameters from 2017–2024 on a log scale. Spot the "transformer inflection point".

### Activity 3 — Radar Chart Analysis (10 min)
Run **Cell 08** — the capability radar chart. Answer: *For a regulated banking use case requiring model approval, which model type would you eliminate first, and why?*

---

## 📝 Key Takeaways

> ✅ AI is the umbrella; ML, DL, and LLMs are progressively specialized subsets

> ✅ LLMs excel at unstructured text — not at tabular, structured, or real-time prediction tasks

> ✅ Most enterprise ML problems are tabular → classical ML (XGBoost, LightGBM) still wins

> ✅ Choosing the wrong paradigm wastes months and millions — framework matters before code

---

## ❓ Quiz — Check Your Understanding

1. What is the key difference between **supervised** and **unsupervised** learning?
2. Why would you choose classical ML over a fine-tuned LLM for **fraud detection**?
3. What does **"self-supervised learning"** mean and which model types use it?
4. Name **2 trade-offs** between Deep Learning vs. a simple Logistic Regression model
5. What is **RAG** and when would you use it over fine-tuning?

---

## 📖 Further Reading

| Resource | Link |
|---------|------|
| Andrej Karpathy — "Software 2.0" | https://karpathy.medium.com/software-2-0-a64152b37c35 |
| A Visual Intro to Machine Learning | http://www.r2d3.us/visual-intro-to-machine-learning-part-1/ |
| Deep Learning Book — Chapter 1 | https://www.deeplearningbook.org/ |
| Google ML Crash Course | https://developers.google.com/machine-learning/crash-course |
| Illustrated Transformer | https://jalammar.github.io/illustrated-transformer/ |

---

*Next session → [Topic 02: Data Quality & Leakage-Free Pipeline Construction](../../topics/02_data_quality_leakage.md)*
