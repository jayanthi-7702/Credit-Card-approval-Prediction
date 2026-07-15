-- Credit Card Approval Prediction Database Schema

CREATE TABLE IF NOT EXISTS Approval_Prediction (
    PredictionID INTEGER PRIMARY KEY AUTOINCREMENT,
    ApplicantID INTEGER NOT NULL,
    ApprovalResult TEXT NOT NULL,
    RiskCategory TEXT NOT NULL,
    PredictionDate TEXT NOT NULL
);