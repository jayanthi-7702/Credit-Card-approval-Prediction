# Credit Card Approval Prediction

## Project Overview
The Credit Card Approval Prediction project is a Machine Learning web application developed using Flask. It predicts whether a credit card application is likely to be approved or rejected based on applicant details. The application also stores prediction history, provides a dashboard with approval statistics, and allows users to download prediction reports in CSV format.

---

## Features

- Credit Card Approval Prediction
- 70% Approval Confidence Threshold
- Risk Category Prediction (Low, Medium, High)
- Prediction History using SQLite Database
- Dashboard with Pie Chart and Bar Chart
- Download Prediction History as CSV
- User-Friendly Flask Web Interface

---

## Technologies Used

- Python
- Flask
- Scikit-learn
- Pandas
- Matplotlib
- SQLite
- HTML
- CSS
- Joblib

---

## Project Structure

```
Credit-Card-Approval-Prediction/
│
├── app.py
├── credit_card_model.pkl
├── database.db
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── history.html
│   └── dashboard.html
│
├── static/
│   ├── approval_chart.png
│   └── approval_bar.png
│
└── downloads/
    └── Prediction_History.csv
```

---

## Input Features

- Gender
- Own Car
- Own House / Realty
- Number of Children
- Annual Income
- Income Type
- Education
- Family Status
- Housing Type
- Age
- Years of Experience
- Mobile Availability
- Email Availability
- Occupation
- Family Members

---

## Output

The application predicts:

- Credit Card Approved / Rejected
- Approval Probability
- Risk Category
- Prediction History
- Approval Statistics Dashboard

---

## How to Run

1. Install required packages:

```bash
pip install -r requirements.txt
```

2. Run the Flask application:

```bash
python app.py
```

3. Open the browser and visit:

```
http://127.0.0.1:5000
```

---

## Future Enhancements

- User Authentication
- PDF Report Generation
- Interactive Dashboard
- Email Notification
- Cloud Deployment

---

## Author

Developed as a Machine Learning project using Flask and Python.