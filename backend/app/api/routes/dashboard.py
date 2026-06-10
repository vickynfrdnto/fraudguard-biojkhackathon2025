from collections import Counter, defaultdict
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.transaction import Transaction
from app.models.user import User

router = APIRouter()


@router.get("/summary")
def summary(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    transactions = _transactions(db)
    total = len(transactions)
    fraud = len([tx for tx in transactions if tx.status == "Fraudulent"])
    suspicious = len([tx for tx in transactions if tx.status == "Suspicious"])
    avg_score = round(sum((tx.risk_score.score if tx.risk_score else 0) for tx in transactions) / total, 1) if total else 0
    return {
        "cards": [
            {"title": "Total Transactions", "value": f"{total:,}", "icon": "fa-exchange-alt", "bg": "bg-blue-100", "text": "text-blue-500", "change": "Live from database", "changeColor": "text-green-500"},
            {"title": "Fraud Detected", "value": f"{fraud:,}", "icon": "fa-exclamation-triangle", "bg": "bg-red-100", "text": "text-red-500", "change": f"{suspicious:,} suspicious cases", "changeColor": "text-red-500"},
            {"title": "Precision Rate", "value": f"{max(0, 100 - avg_score / 2):.1f}%", "icon": "fa-check-circle", "bg": "bg-green-100", "text": "text-green-500", "change": "Risk-weighted estimate", "changeColor": "text-green-500"},
            {"title": "Avg Detection Time", "value": "0.8s", "icon": "fa-stopwatch", "bg": "bg-purple-100", "text": "text-purple-500", "change": "Real-time API scoring", "changeColor": "text-green-500"},
        ]
    }


@router.get("/risk-overview")
def risk_overview(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    counts = Counter((tx.risk_score.level if tx.risk_score else "LOW") for tx in _transactions(db))
    return {"labels": ["LOW", "MEDIUM", "HIGH"], "datasets": [{"label": "Risk Scores", "data": [counts["LOW"], counts["MEDIUM"], counts["HIGH"]], "backgroundColor": ["#10B981", "#FBBF24", "#EF4444"]}]}


@router.get("/transaction-trends")
def transaction_trends(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    groups: dict[str, Counter] = defaultdict(Counter)
    for tx in _transactions(db):
        label = tx.transaction_time.strftime("%b")
        groups[label]["fraud" if tx.status == "Fraudulent" else "normal"] += 1
    labels = list(groups.keys()) or ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
    return {
        "labels": labels,
        "datasets": [
            {"label": "Normal Transactions", "data": [groups[label]["normal"] for label in labels], "borderColor": "#10B981", "backgroundColor": "rgba(16, 185, 129, 0.1)", "tension": 0.3, "fill": True},
            {"label": "Fraudulent Transactions", "data": [groups[label]["fraud"] for label in labels], "borderColor": "#EF4444", "backgroundColor": "rgba(239, 68, 68, 0.1)", "tension": 0.3, "fill": True},
        ],
    }


@router.get("/fraud-analysis")
def fraud_analysis(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    counts = Counter(tx.status for tx in _transactions(db))
    return {"labels": ["Normal", "Suspicious", "Fraud"], "datasets": [{"label": "Transaction Status", "data": [counts["Legitimate"], counts["Suspicious"], counts["Fraudulent"]], "backgroundColor": ["#10B981", "#FBBF24", "#EF4444"]}]}


@router.get("/branch-comparison")
def branch_comparison(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    counts = Counter(tx.branch or "Unknown" for tx in _transactions(db) if tx.status in {"Fraudulent", "Suspicious"})
    labels = [item[0] for item in counts.most_common(5)] or ["Jakarta", "Bandung", "Surabaya", "Medan", "Makassar"]
    return {"labels": labels, "datasets": [{"label": "Fraud Cases", "data": [counts[label] for label in labels], "backgroundColor": "#6366F1"}]}


@router.get("/recent-transactions")
def recent_transactions(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = db.scalars(select(Transaction).options(selectinload(Transaction.risk_score)).order_by(Transaction.created_at.desc()).limit(20)).all()
    return [{"Reference": tx.reference, "Amount": float(tx.amount), "Branch": tx.branch or "-", "Risk": tx.risk_score.level if tx.risk_score else "LOW", "status": _legacy_status(tx.status)} for tx in rows]


@router.get("/alerts")
def alerts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    risky = [tx for tx in _transactions(db) if tx.status in {"Fraudulent", "Suspicious"}][:10]
    return [
        {
            "type": "High Risk Transaction" if tx.status == "Fraudulent" else "Suspicious Pattern",
            "desc": f"IDR {float(tx.amount):,.0f} at {tx.branch or 'unknown branch'}",
            "time": _relative_time(tx.created_at),
            "color": "red" if tx.status == "Fraudulent" else "yellow",
        }
        for tx in risky
    ]


@router.get("/analytics-summary")
def analytics_summary(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    transactions = _transactions(db)
    total = len(transactions)
    fraud = len([tx for tx in transactions if tx.status == "Fraudulent"])
    branch = Counter(tx.branch or "Unknown" for tx in transactions if tx.status == "Fraudulent").most_common(1)
    return [
        {"label": "Total Transactions", "value": f"{total:,}", "color": "text-blue-600"},
        {"label": "Fraud Rate", "value": f"{((fraud / total) * 100):.0f}%" if total else "0%", "color": "text-red-600"},
        {"label": "Most Risky Region", "value": branch[0][0] if branch else "N/A", "color": "text-yellow-600"},
    ]


def _transactions(db: Session) -> list[Transaction]:
    return db.scalars(select(Transaction).options(selectinload(Transaction.risk_score)).order_by(Transaction.created_at.desc())).all()


def _legacy_status(status_name: str) -> str:
    return {"Fraudulent": "Fraud", "Suspicious": "Suspicious", "Legitimate": "Normal"}.get(status_name, status_name)


def _relative_time(value: datetime) -> str:
    delta = datetime.now(timezone.utc) - value
    minutes = int(delta.total_seconds() // 60)
    if minutes < 60:
        return f"{max(1, minutes)} min ago"
    return f"{minutes // 60} hr ago"
