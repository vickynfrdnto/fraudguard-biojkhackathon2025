from decimal import Decimal

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionUpdate
from app.services.transaction_service import TransactionService

router = APIRouter()


@router.post("", response_model=TransactionOut, status_code=201)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return TransactionService(db).create(payload, user.id)


@router.get("", response_model=list[TransactionOut])
def list_transactions(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.scalars(select(Transaction).options(selectinload(Transaction.risk_score)).order_by(Transaction.created_at.desc()).limit(100)).all()


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    transaction = db.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=TransactionOut)
def update_transaction(transaction_id: int, payload: TransactionUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    transaction = db.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return TransactionService(db).update(transaction, payload)


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    transaction = db.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()


@router.post("/detect")
async def detect_transactions(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return await _process_file(file, db, user.id)


async def _process_file(file: UploadFile, db: Session, user_id: int | None):
    if not file.filename.lower().endswith((".csv", ".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Unsupported file format")
    try:
        if file.filename.lower().endswith(".csv"):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Unable to read file: {exc}") from exc

    amount_column = next((col for col in ["Amount", "amount", "Jumlah", "jumlah", "Nominal", "nominal", "Total", "total"] if col in df.columns), None)
    if not amount_column:
        raise HTTPException(status_code=400, detail=f"No valid Amount column found. Columns: {list(df.columns)}")

    service = TransactionService(db)
    rows = []
    for _, row in df.fillna("").iterrows():
        transaction = service.create(
            TransactionCreate(
                amount=Decimal(str(row[amount_column])),
                sender_account=str(row.get("sender_account") or row.get("Sender") or ""),
                recipient_account=str(row.get("recipient_account") or row.get("Recipient") or ""),
                branch=str(row.get("branch") or row.get("Branch") or ""),
                country=str(row.get("country") or row.get("Country") or ""),
                channel=str(row.get("channel") or row.get("Channel") or ""),
            ),
            user_id,
        )
        rows.append({"Amount": float(transaction.amount), "status": _legacy_status(transaction.status), "risk_score": transaction.risk_score.score})
    return {"data": rows, "summary": _summary(rows)}


def _legacy_status(status_name: str) -> str:
    return {"Fraudulent": "Fraud", "Suspicious": "Suspicious", "Legitimate": "Normal"}.get(status_name, status_name)


def _summary(rows: list[dict]):
    total = len(rows)
    fraud = len([row for row in rows if row["status"] == "Fraud"])
    suspicious = len([row for row in rows if row["status"] == "Suspicious"])
    normal = total - fraud - suspicious
    return {"total": total, "fraud": fraud, "suspicious": suspicious, "normal": normal, "fraud_rate": round((fraud / total) * 100, 2) if total else 0}
