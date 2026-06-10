from decimal import Decimal

from app.core.database import Base, SessionLocal, engine
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.services.transaction_service import TransactionService


def test_transaction_service_create_and_update_scores_transaction():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        service = TransactionService(db)
        transaction = service.create(
            TransactionCreate(
                amount=Decimal("12500000"),
                sender_account="A-001",
                recipient_account="B-001",
                branch="Jakarta",
                country="Indonesia",
                channel="mobile",
            )
        )
        assert transaction.reference.startswith("TX-")
        assert transaction.status == "Fraudulent"
        assert transaction.risk_score.score >= 70

        updated = service.update(transaction, TransactionUpdate(amount=Decimal("100000")))
        assert updated.status == "Legitimate"
        assert updated.risk_score.level == "LOW"
    finally:
        db.close()
