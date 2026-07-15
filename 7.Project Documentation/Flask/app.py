from flask import Flask, render_template, request, send_file
import joblib
import sqlite3
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os

app = Flask(__name__)

# Load trained model
model = joblib.load("credit_card_model.pkl")


def get_connection():
    return sqlite3.connect("database.db")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    age = int(request.form["age"])
    experience = int(request.form["experience"])

    # Convert Age & Experience into dataset format
    days_birth = -(age * 365)
    days_employed = -(experience * 365)

    values = [[
        int(request.form["gender"]),
        int(request.form["car"]),
        int(request.form["realty"]),
        int(request.form["children"]),
        float(request.form["income"]),
        int(request.form["income_type"]),
        int(request.form["education"]),
        int(request.form["family"]),
        int(request.form["housing"]),
        days_birth,
        days_employed,
        int(request.form["mobile"]),
        0,                      # Work Phone
        0,                      # Phone
        int(request.form["email"]),
        int(request.form["occupation"]),
        float(request.form["family_members"])
    ]]

    probability = model.predict_proba(values)[0]

    approval_probability = round(probability[0] * 100, 2)
    rejection_probability = round(probability[1] * 100, 2)

    # 70% Approval Threshold
    if approval_probability >= 70:
        prediction = 0
    else:
        prediction = 1

    print("Input Values :", values)
    print("Prediction :", prediction)
    print("Probabilities :", probability)

    if prediction == 0:

        result = "✅ Credit Card Approved"
        confidence = f"Approval Probability : {approval_probability}%"

        if approval_probability >= 80:
            risk = "🟢 Low Risk"

        elif approval_probability >= 60:
            risk = "🟡 Medium Risk"

        else:
            risk = "🔴 High Risk"

    else:

        result = "❌ Credit Card Rejected"
        confidence = f"Rejection Probability : {rejection_probability}%"

        if rejection_probability >= 80:
            risk = "🔴 High Risk"

        elif rejection_probability >= 60:
            risk = "🟡 Medium Risk"

        else:
            risk = "🟢 Low Risk"

    # Save prediction into database
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Approval_Prediction
        (
            ApplicantID,
            ApprovalResult,
            RiskCategory,
            PredictionDate
        )
        VALUES (?, ?, ?, ?)
    """, (
        1,
        result,
        risk,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return render_template(
        "index.html",
        prediction=result,
        confidence=confidence,
        risk=risk
    )
@app.route("/history")
def history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ApplicantID,
               ApprovalResult,
               RiskCategory,
               PredictionDate
        FROM Approval_Prediction
        ORDER BY PredictionID DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return render_template("history.html", rows=rows)


@app.route("/download")
def download():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM Approval_Prediction",
        conn
    )

    conn.close()

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    file_path = os.path.join(
        "downloads",
        "Prediction_History.csv"
    )

    df.to_csv(
        file_path,
        index=False,
        encoding="utf-8-sig"
    )

    return send_file(
        file_path,
        as_attachment=True
    )


@app.route("/dashboard")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    # Total Applications
    cursor.execute(
        "SELECT COUNT(*) FROM Approval_Prediction"
    )
    total = cursor.fetchone()[0]

    # Total Approved
    cursor.execute("""
        SELECT COUNT(*)
        FROM Approval_Prediction
        WHERE ApprovalResult='✅ Credit Card Approved'
    """)
    approved = cursor.fetchone()[0]

    # Total Rejected
    cursor.execute("""
        SELECT COUNT(*)
        FROM Approval_Prediction
        WHERE ApprovalResult='❌ Credit Card Rejected'
    """)
    rejected = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        approval_rate = 0
    else:
        approval_rate = round(
            (approved / total) * 100,
            2
        )

    # -----------------------------
    # Pie Chart
    # -----------------------------

    if not os.path.exists("static"):
        os.makedirs("static")

    plt.figure(figsize=(5,5))

    plt.pie(
        [approved, rejected],
        labels=["Approved", "Rejected"],
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Credit Card Approval Statistics")
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            "static",
            "approval_chart.png"
        )
    )

    plt.close()

    # -----------------------------
    # Bar Chart
    # -----------------------------

    plt.figure(figsize=(6,4))

    plt.bar(
        ["Approved", "Rejected"],
        [approved, rejected],
        color=["green", "red"]
    )

    plt.title("Credit Card Approval Comparison")
    plt.ylabel("Number of Applications")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            "static",
            "approval_bar.png"
        )
    )

    plt.close()

    return render_template(
        "dashboard.html",
        total=total,
        approved=approved,
        rejected=rejected,
        approval_rate=approval_rate
    )


if __name__ == "__main__":
    app.run(debug=True)