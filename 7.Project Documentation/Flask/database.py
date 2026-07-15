import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Approval_Prediction(
    PredictionID INTEGER PRIMARY KEY AUTOINCREMENT,
    ApplicantID INTEGER,
    ApprovalResult TEXT,
    RiskCategory TEXT,
    PredictionDate TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")