# 🎛️ Topic 04 — Hyperparameter Optimization & Experiment Tracking

> **Welcome to Topic 4!**  
> We have trained a model, but is it the *best* model it can be? In this session, you'll learn how to magically find the perfect settings for your models using a technique called **Bayesian Optimization** (via Optuna). We'll also cover how to keep track of all your experiments using **MLflow** so you never lose your best model again!

---

## 🎯 Learning Objectives

By the end of this 60-minute session, you will be able to:
1. **Explain** the difference between parameters the model learns itself and hyperparameters that *you* have to set.
2. **Understand** why grid search is too slow and how Bayesian optimization works smarter, not harder.
3. **Use Optuna** to automatically find the best hyperparameters for a Random Forest classifier.
4. **Use MLflow** to log your experiments, track your models, and easily compare different runs.

---

## 🧠 Core Concepts

### 1. Hyperparameters vs. Model Parameters
Imagine baking a cake. 
- **Model Parameters** are what happens *inside* the oven (how the ingredients fuse together). The model learns this from the data.
- **Hyperparameters** are the oven temperature and the baking time. *You* have to set these before you start! If you set them wrong, the cake burns (or the model overfits). Examples: `learning_rate`, `max_depth`.

### 2. The Search Strategies
- **Grid Search:** Checking every single combination (Temperature: 180, 190, 200. Time: 30, 40, 50). Extremely slow.
- **Random Search:** Randomly picking combinations. Surprisingly, this works better than Grid Search in many cases!
- **Bayesian Optimization (Optuna):** Learns from past mistakes. "Ah, 200 degrees for 50 minutes burned the cake. Let's try 180 degrees for 40 minutes." This is the smartest approach.

### 3. Experiment Tracking (MLflow)
When you start tuning, you will run dozens or hundreds of experiments. You will quickly forget which settings gave you the best result. **MLflow** acts like a journal or version control for your machine learning experiments.

---

## 🏋️ Activities

1. **Activity 1 — Optuna in Action:** You will write a few lines of code to let Optuna automatically search for the best `max_depth` and `n_estimators` for a Random Forest.
2. **Activity 2 — MLflow Tracking:** You will integrate MLflow into your training loop to log metrics (like AUC) and save the trained model artifacts.
3. **Activity 3 — Visualizing the Search Space:** You will generate beautiful charts to see exactly which hyperparameters were the most important for the model's success.

---

## 📝 Key Takeaways
- **Work Smarter:** Don't guess hyperparameters. Use Optuna to find them systematically.
- **Track Everything:** Treat experiments like code. If it's not in MLflow, it didn't happen!
- **Don't Cheat:** Never use your test set to tune hyperparameters. Always use cross-validation or a separate validation set.

---

## 📖 Further Reading
- [Optuna Official Documentation](https://optuna.readthedocs.io/)
- [MLflow Quickstart](https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html)
