# 📉 Topic 06 — Data Drift & Unsupervised Anomaly Detection

> **Welcome to Topic 6!**  
> "A model that was 95% accurate when you trained it can silently drop to 60% accuracy in just 3 months in production." Why? Because the real world changes! 
> In this session, you'll learn how to set up early warning systems (like a smoke alarm) to detect when your data changes (Drift) or when a strange, unexpected data point enters your system (Anomaly).

---

## 🎯 Learning Objectives

By the end of this 60-minute session, you will be able to:
1. **Explain** the difference between Feature Drift (the input changes) and Concept Drift (the rules of the game change).
2. **Use Population Stability Index (PSI)** to mathematically prove that your data has shifted.
3. **Train an Isolation Forest** to catch weird data points (anomalies) *without* needing any labeled examples!
4. **Design** a monitoring system so your models never silently fail in production.

---

## 🧠 Core Concepts

### 1. Why Models Decay
When you train a model, you take a "snapshot" of the world on that specific day. But the world keeps moving. A global pandemic happens, a competitor launches a new product, or an engineer accidentally changes how `age` is calculated in the database. When the real world no longer matches your snapshot, the model fails.

### 2. The Types of Drift
- **Feature Drift:** The inputs change. (e.g., Suddenly, 80% of your applicants are over 50 years old instead of 30).
- **Concept Drift:** The relationship between inputs and outputs changes. (e.g., Before, a $1000 balance meant a customer was rich. Due to massive inflation, a $1000 balance now means they are broke).

### 3. Population Stability Index (PSI)
PSI is the industry standard (especially in banking) for measuring drift. 
- **PSI < 0.1:** Nothing to see here.
- **PSI between 0.1 and 0.2:** Keep an eye on it.
- **PSI > 0.2:** ALERT! The data has shifted drastically. Time to retrain the model!

### 4. Isolation Forest (Anomaly Detection)
How do you find weird data points if you don't know what "weird" looks like? Imagine you are lost in a forest. If you are standing next to a common pine tree, it takes many steps to isolate you from the other pine trees. If you are standing next to a neon-pink glowing tree (an anomaly), it's very easy to draw a box around you. Isolation Forest builds random boxes (trees) and finds the data points that are easiest to isolate.

---

## 🏋️ Activities

1. **Activity 1 — Simulating Data Drift:** You will write code to simulate a shift in customer income, calculate the PSI, and build a chart to flag the exact moment the data drifted.
2. **Activity 2 — Catch the Anomaly:** You will inject 5% "fake" weird data into a dataset and train an Isolation Forest to hunt them down.
3. **Activity 3 — The MLOps Dashboard:** You will create the visual components of a drift dashboard that a data scientist would check every morning.

---

## 📝 Key Takeaways
- **No model lives forever.** If you deploy a model without monitoring, it is a ticking time bomb.
- **PSI is your smoke alarm.** A PSI > 0.2 means it is time to investigate.
- **Isolation Forest is Unsupervised.** It doesn't need labeled data to find anomalies, making it perfect for real-time production monitoring.

---

## 📖 Further Reading
- [Evidently AI — ML Monitoring Guide](https://docs.evidentlyai.com/)
- [Towards Data Science — PSI Explained Like I'm 5](https://towardsdatascience.com/population-stability-index-psi-explain-like-im-5-aed7e16e59e9)
