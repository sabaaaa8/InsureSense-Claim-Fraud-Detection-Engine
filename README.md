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
- Generate and download **CSV reports** (full claims report, fraud-only
  report) plus a monthly and state-wise fraud summary.

All data lives in `insurance_claims.csv` — there is no SQL database
anywhere in this project, per the project brief.

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

> **Note on TensorFlow:** the project spec allows TensorFlow "only if
> needed." A traditional ML model (Random Forest) already achieves strong
> accuracy on this tabular, moderately-sized dataset, so TensorFlow was
> intentionally not used — this keeps the project lighter and easier to
> run for an internship submission. `pickle` (Python standard library) is
> used directly to serialize the trained model.

---

## Project Structure

```
InsureSense/
│
├── app.py                     # Flask application (routes, auth, prediction API)
├── fraud_model.pkl            # Trained model bundle (model + encoders + metrics)
├── insurance_claims.csv       # Dataset (3,200 records, ~17% fraud)
├── requirements.txt
├── README.md
│
├── templates/
│   ├── base.html               # Shared layout: sidebar + topbar
│   ├── login.html
│   ├── dashboard.html
│   ├── analytics.html
│   ├── prediction.html
│   └── reports.html
│
├── static/
│   ├── css/style.css           # Glassmorphism design system
│   ├── js/script.js            # Sidebar toggle, alert auto-dismiss, animations
│   └── images/
│
├── charts/                     # Generated chart PNGs (served via /charts/<file>)
│
├── notebooks/
│   └── model_training.ipynb    # Full training walkthrough notebook
│
└── utils/
    ├── generate_dataset.py     # Synthetic dataset generator
    ├── preprocessing.py        # Shared cleaning/feature-engineering pipeline
    ├── train_model.py          # Training script (creates .pkl + all charts)
    └── build_notebook.py       # Builds the .ipynb notebook programmatically
```

---

## Installation Steps

1. **Clone / unzip** the project folder and move into it:
   ```bash
   cd InsureSense
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Run

The dataset and trained model are already included in the project
(`insurance_claims.csv` and `fraud_model.pkl`), so you can start the app
immediately:

```bash
python app.py
```

Then open your browser at **http://127.0.0.1:5000**

**Login credentials:**
- Username: `admin`
- Password: `admin123`

### (Optional) Regenerate the dataset / retrain the model

If you want to regenerate the synthetic dataset or retrain the model
(this also regenerates every chart in `/charts`):

```bash
python utils/generate_dataset.py   # creates a fresh insurance_claims.csv
python utils/train_model.py        # retrains model, saves fraud_model.pkl, regenerates charts
```

You can also open `notebooks/model_training.ipynb` in Jupyter to walk
through the full training process interactively.

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

---

## Model Summary

- **Algorithm:** Random Forest Classifier (`scikit-learn`), 300 trees,
  `class_weight="balanced"` to handle the ~17% fraud class imbalance
- **Pipeline:** missing-value imputation → feature engineering
  (`claim_to_premium_ratio`, `total_cost`) → label encoding → train/test split (80/20, stratified)
- **Typical performance** (varies slightly per run/seed):
  - Accuracy: ~84%
  - ROC-AUC: ~0.84
  - Precision/Recall/F1 reported per-class in the notebook and dashboard

---

## Screenshots

_Add screenshots of the login page, dashboard, prediction module, analytics
gallery, and reports page here before final submission._

```
static/images/screenshot-login.png
static/images/screenshot-dashboard.png
static/images/screenshot-prediction.png
static/images/screenshot-analytics.png
static/images/screenshot-reports.png
```

---

## Disclaimer

The dataset is entirely **synthetic** (programmatically generated with
realistic distributions and fraud-risk signal) — no real customer or
insurance data is used anywhere in this project. This project is intended
for educational / internship demonstration purposes.
