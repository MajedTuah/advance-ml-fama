# 📊 Topic 08 — MLOps Dashboard

> **Welcome to Topic 8!**  
> We have trained our model, deployed it into an API, and figured out how to detect drift. Now we need to put it all together on a single screen so we can monitor our system like a pilot monitors an airplane. Welcome to the **MLOps Dashboard**.

---

## 🎯 Learning Objectives

By the end of this 60-minute session, you will be able to:
1. **Design** a dashboard that tracks Model Health, Data Health, and System Health all at once.
2. **Visualize** how a model's accuracy decays over time using line charts and alert thresholds.
3. **Build a Feature Drift Heatmap** to spot exactly which inputs are failing.
4. **Export** your dashboard into a clean, automated report.

---

## 🧠 Core Concepts

### 1. You Can't Manage What You Don't Measure
If your model breaks in production, you shouldn't find out because a customer complained. You should find out because your dashboard turned red!

### 2. The Four Pillars of Monitoring
A good MLOps dashboard tracks four things:
- **Model Performance:** (Is it still accurate?)
- **Data Health:** (Are the inputs still clean, or has drift happened?)
- **System Health:** (Is the API fast, or is it crashing?)
- **Business Impact:** (Are we losing money?)

### 3. Google's "Golden Signals"
Google SRE (Site Reliability Engineering) says you must always track these 4 things for *any* API:
- **Latency:** How fast is it? (We look at the 99th percentile, not just the average).
- **Traffic:** How many people are using it?
- **Errors:** How many requests are crashing?
- **Saturation:** Is the server's CPU maxed out?

### 4. Alert Fatigue
If your dashboard sends you an email every time accuracy drops by 0.1%, you will start ignoring the emails. This is called **Alert Fatigue**. We only set alerts for things that require human action (like crossing a critical threshold).

---

## 🏋️ Activities

1. **Activity 1 — The 6-Panel Dashboard:** We will use `matplotlib` to build a massive, 6-part visual dashboard combining everything we've learned so far.
2. **Activity 2 — Adding Alerts:** We will draw bright red threshold lines on our charts. If the line drops below the red line, it's time to retrain!
3. **Activity 3 — Exporting the Report:** We will write code to automatically save our beautiful dashboard as an image that could be emailed to our boss every Monday morning.

---

## 📝 Key Takeaways
- **Dashboards are the heartbeat of MLOps.** Without them, you are flying blind.
- **SLO (Service Level Objective):** This is the goal (e.g., "Accuracy must stay above 85%").
- **Alert on the SLO, not random metrics.** Only wake up the data scientist if the SLO is broken!

---

## 📖 Further Reading
- [Google SRE Book — Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Evidently AI — ML Monitoring Guide](https://docs.evidentlyai.com/user-guide/monitoring)
