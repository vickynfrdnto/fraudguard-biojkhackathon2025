# backend/summary.py

def get_summary(df):
    total = len(df)
    fraud = len(df[df["status"] == "Fraud"])
    suspicious = len(df[df["status"] == "Suspicious"])
    normal = len(df[df["status"] == "Normal"])

    return {
        "total": total,
        "fraud": fraud,
        "suspicious": suspicious,
        "normal": normal,
        "fraud_rate": round((fraud / total) * 100, 2) if total else 0
    }