# InsureSense — Claim Fraud Detection Engine

A full-stack machine learning web application for the insurance industry
that detects fraudulent claims and gives insurers an interactive analytics
dashboard. Built as an internship-level project using Flask, scikit-learn,
and a glassmorphism-themed Bootstrap 5 frontend — no database, CSV files only.

---

## Project Overview

InsureSense lets an insurance administrator:

- Log in through a simple, static admin login.
- View a live analytics dashboard (total claims, fraud claims, fraud %,
  average/highest claim amounts) backed by an 11-chart visual gallery.
- Run a **real-time fraud prediction** on a new claim using a trained
  Random Forest classifier.
- Browse deeper analytics (age distribution, severity, vehicle type,
  fraud heatmap, feature importance, confusion matrix).
- Generate and download **CSV reports** plus a monthly and state-wise fraud summary.

---

## Features

- 🔐 Static admin authentication (`admin` / `admin123`), no DB required
- 📊 6 KPI dashboard cards + 4 headline charts
- 🧠 ML-powered fraud prediction form with probability & confidence output
- 📈 11 Matplotlib/Seaborn charts: bar, pie, line/trend, histograms,
  heatmap, scatter, feature importance, confusion matrix
- 📄 Downloadable CSV reports (full + fraud-only) and tabular summaries
- 🎨 Premium glassmorphism UI — blue/purple/white on a dark gradient,
  responsive sidebar navigation, hover/motion micro-interactions
- 🧾 Fully reproducible model training notebook (`model_training.ipynb`)

---

## Technologies Used

**Frontend:** HTML5, CSS3 (custom glassmorphism design system), JavaScript, Bootstrap 5, Font Awesome

**Backend:** Python 3, Flask

**Machine Learning:** NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, Pickle

**Data storage:** CSV files only (no database)


---

## Application Pages

| Route         | Description                                             |
|---------------|----------------------------------------------------------|
| `/login`      | Static admin login                                       |
| `/dashboard`  | KPI cards + headline charts + model performance summary  |
| `/predict`    | Fraud prediction form with live probability/confidence   |
| `/analytics`  | Extended chart gallery + top fraud states                |
| `/reports`    | Monthly & state-wise summaries + CSV report downloads    |
| `/logout`     | Clears session, returns to login                         |


## 🎓 Conclusion

This project was developed by **Sabahat** as part of my Data Science& Machine Learning Internship.

Through this internship project, I have learned and implemented:

- ✅ Real-world data analysis using Python & Pandas
- ✅ Data visualization using Matplotlib & Seaborn
- ✅ Machine Learning model using Scikit-learn
- ✅ Web dashboard development using Flask
- ✅ Professional UI design using Bootstrap 5
- ✅ End-to-end project development from dataset to deployment

This project demonstrates my skills in **Python, Data Analytics and Machine Learning** gained during my internship training.

---

> **Developed by Saba**
> Data Science & Machine Learning Internship Project
> © 2026 All Rights Reserved



