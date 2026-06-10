# backend/detection.py
import pandas as pd

def detect_fraud(df: pd.DataFrame):
    def classify(amount):
        if amount > 10000000:
            return "Fraud"
        elif amount > 5000000:
            return "Suspicious"
        else:
            return "Normal"

    if "Amount" not in df.columns:
        raise ValueError("Missing 'Amount' column in uploaded data")

    df["status"] = df["Amount"].apply(classify)
    return df