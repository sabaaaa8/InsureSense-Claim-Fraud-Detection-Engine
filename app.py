"""
InsureSense - Claim Fraud Detection Engine
================================================
Flask web application entry point.

Routes
------
/                -> redirects to login
/login           -> static admin login (admin / admin123)
/dashboard       -> analytics dashboard (cards + charts)
/predict         -> fraud prediction form + result
/analytics       -> deeper analytics / chart gallery
/reports         -> fraud reports + CSV downloads
/logout          -> clears session, returns to login

No database is used anywhere - all data is read from insurance_claims.csv
and the trained model is loaded from fraud_model.pkl.
"""

import os
import io
import pickle
from datetime import datetime

import numpy as np
import pandas as pd
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, send_file, flash, jsonify, send_from_directory
)

from utils.preprocessing import build_feature_matrix, FEATURE_ORDER

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "insurance_claims.csv")
MODEL_PATH = os.path.join(BASE_DIR, "fraud_model.pkl")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")

app = Flask(__name__)
app.secret_key = "insuresense-internship-project-secret-key"

# ---------------------------------------------------------------------------
# Static credentials (no database, as per project spec)
# ---------------------------------------------------------------------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ---------------------------------------------------------------------------
# Load model bundle + dataset once at startup
# ---------------------------------------------------------------------------
model_bundle = None
df_claims = None


def load_resources():
    global model_bundle, df_claims
    with open(MODEL_PATH, "rb") as f:
        model_bundle = pickle.load(f)
    df_claims = pd.read_csv(CSV_PATH)


load_resources()


def login_required(view_func):
    """Simple session-based guard for protected pages."""
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------
@app.route("/charts/<path:filename>")
def serve_chart(filename):
    return send_from_directory(CHARTS_DIR, filename)


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password. Please try again.", "error")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    total_claims = len(df_claims)
    fraud_claims = int(df_claims["fraud_reported"].sum())
    genuine_claims = total_claims - fraud_claims
    fraud_percentage = round((fraud_claims / total_claims) * 100, 2)
    avg_claim_amount = round(df_claims["claim_amount"].mean(), 2)
    highest_claim_amount = round(df_claims["claim_amount"].max(), 2)

    metrics = model_bundle.get("metrics", {})

    cards = {
        "total_claims": total_claims,
        "fraud_claims": fraud_claims,
        "genuine_claims": genuine_claims,
        "fraud_percentage": fraud_percentage,
        "avg_claim_amount": avg_claim_amount,
        "highest_claim_amount": highest_claim_amount,
    }

    chart_timestamp = int(datetime.now().timestamp())

    return render_template(
        "dashboard.html",
        cards=cards,
        metrics=metrics,
        username=session.get("username", "Admin"),
        chart_timestamp=chart_timestamp
    )


# ---------------------------------------------------------------------------
# Analytics (chart gallery)
# ---------------------------------------------------------------------------
@app.route("/analytics")
@login_required
def analytics():
    chart_timestamp = int(datetime.now().timestamp())
    top_states = (
        df_claims.groupby("incident_state")["fraud_reported"]
        .agg(["count", "sum"])
        .rename(columns={"count": "total", "sum": "fraud"})
        .sort_values("fraud", ascending=False)
        .head(5)
        .reset_index()
    )
    top_states_records = top_states.to_dict(orient="records")

    return render_template(
        "analytics.html",
        username=session.get("username", "Admin"),
        chart_timestamp=chart_timestamp,
        top_states=top_states_records
    )


# ---------------------------------------------------------------------------
# Prediction module
# ---------------------------------------------------------------------------
@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    result = None

    if request.method == "POST":
        try:
            form = request.form
            input_row = {
                "age": float(form.get("age")),
                "vehicle_age": float(form.get("vehicle_age")),
                "vehicle_type": form.get("vehicle_type"),
                "premium_amount": float(form.get("premium_amount")),
                "claim_amount": float(form.get("claim_amount")),
                "policy_type": form.get("policy_type"),
                "accident_severity": form.get("accident_severity"),
                "number_of_previous_claims": float(form.get("previous_claims")),
                "medical_cost": float(form.get("medical_cost")),
                "repair_cost": float(form.get("repair_cost")),
                "police_report": form.get("police_report"),
                "witness_present": form.get("witness_present"),
                # Fields not collected in the simplified form get sensible defaults
                "gender": "Male",
                "accident_type": "Collision",
                "incident_state": "Maharashtra",
                "days_since_policy": 200,
                "claim_status": "Under Review",
            }

            input_df = pd.DataFrame([input_row])
            X, _ = build_feature_matrix(
                input_df, model_bundle["encoders"], fit=False
            )
            X = X[model_bundle["feature_order"]]

            model = model_bundle["model"]
            proba = model.predict_proba(X)[0][1]
            prediction = int(proba >= 0.5)

            result = {
                "prediction": "Fraudulent" if prediction == 1 else "Genuine",
                "is_fraud": prediction == 1,
                "fraud_probability": round(proba * 100, 2),
                "confidence": round((proba if prediction == 1 else 1 - proba) * 100, 2),
            }
        except Exception as exc:
            flash(f"Prediction error: {exc}", "error")

    return render_template(
        "prediction.html",
        result=result,
        username=session.get("username", "Admin")
    )


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------
@app.route("/reports")
@login_required
def reports():
    total_claims = len(df_claims)
    fraud_claims = int(df_claims["fraud_reported"].sum())
    genuine_claims = total_claims - fraud_claims
    fraud_percentage = round((fraud_claims / total_claims) * 100, 2)

    # Monthly-style summary simulated from days_since_policy buckets
    df_temp = df_claims.copy()
    df_temp["month_bucket"] = pd.cut(
        df_temp["days_since_policy"], bins=12,
        labels=[f"M{i}" for i in range(1, 13)]
    )
    monthly_summary = (
        df_temp.groupby("month_bucket", observed=True)
        .agg(total_claims=("claim_id", "count"), fraud_claims=("fraud_reported", "sum"))
        .reset_index()
        .to_dict(orient="records")
    )

    state_summary = (
        df_claims.groupby("incident_state")
        .agg(total_claims=("claim_id", "count"), fraud_claims=("fraud_reported", "sum"))
        .reset_index()
        .sort_values("fraud_claims", ascending=False)
        .to_dict(orient="records")
    )

    return render_template(
        "reports.html",
        username=session.get("username", "Admin"),
        total_claims=total_claims,
        fraud_claims=fraud_claims,
        genuine_claims=genuine_claims,
        fraud_percentage=fraud_percentage,
        monthly_summary=monthly_summary,
        state_summary=state_summary
    )


@app.route("/reports/download/full")
@login_required
def download_full_report():
    buffer = io.BytesIO()
    df_claims.to_csv(buffer, index=False)
    buffer.seek(0)
    return send_file(
        buffer, mimetype="text/csv", as_attachment=True,
        download_name="insurance_claims_full_report.csv"
    )


@app.route("/reports/download/fraud")
@login_required
def download_fraud_report():
    fraud_df = df_claims[df_claims["fraud_reported"] == 1]
    buffer = io.BytesIO()
    fraud_df.to_csv(buffer, index=False)
    buffer.seek(0)
    return send_file(
        buffer, mimetype="text/csv", as_attachment=True,
        download_name="fraud_claims_report.csv"
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
