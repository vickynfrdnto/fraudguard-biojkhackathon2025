from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.risk_score import RiskScore
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.services.fraud_engine import FraudDetectionEngine


class TransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.engine = FraudDetectionEngine()

    def create(self, payload: TransactionCreate, user_id: int | None = None) -> Transaction:
        reference = payload.reference or f"TX-{uuid4().hex[:12].upper()}"
        transaction = Transaction(
            user_id=user_id,
            reference=reference,
            amount=payload.amount,
            sender_account=payload.sender_account,
            recipient_account=payload.recipient_account,
            branch=payload.branch,
            country=payload.country,
            ip_address=payload.ip_address,
            channel=payload.channel,
            transaction_time=payload.transaction_time or datetime.now(timezone.utc),
        )
        self.db.add(transaction)
        self.db.flush()
        self._rescore(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def update(self, transaction: Transaction, payload: TransactionUpdate) -> Transaction:
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(transaction, key, value)
        self._rescore(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def _rescore(self, transaction: Transaction) -> None:
        history = self.db.scalars(
            select(Transaction.amount)
            .where(Transaction.sender_account == transaction.sender_account, Transaction.id != transaction.id)
            .limit(25)
        ).all()
        since = datetime.now(timezone.utc) - timedelta(hours=24)
        frequency = self.db.scalar(
            select(func.count(Transaction.id)).where(
                Transaction.sender_account == transaction.sender_account,
                Transaction.transaction_time >= since,
                Transaction.id != transaction.id,
            )
        ) or 0
        result = self.engine.score(Decimal(transaction.amount), list(history), int(frequency), transaction.country)
        transaction.status = result.classification
        if transaction.risk_score:
            risk = transaction.risk_score
        else:
            risk = RiskScore(transaction=transaction)
            self.db.add(risk)
        risk.score = result.score
        risk.level = result.level
        risk.classification = result.classification
        risk.reasons = ", ".join(result.reasons)
