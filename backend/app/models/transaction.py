from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, utcnow


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"
    __table_args__ = (
        Index("ix_transactions_user_created", "user_id", "created_at"),
        Index("ix_transactions_status", "status"),
        Index("ix_transactions_branch", "branch"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reference: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    sender_account: Mapped[str | None] = mapped_column(String(80))
    recipient_account: Mapped[str | None] = mapped_column(String(80))
    branch: Mapped[str | None] = mapped_column(String(80))
    country: Mapped[str | None] = mapped_column(String(80))
    ip_address: Mapped[str | None] = mapped_column(String(64))
    channel: Mapped[str | None] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(20), default="Legitimate", nullable=False)
    transaction_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user = relationship("User", back_populates="transactions")
    risk_score = relationship("RiskScore", back_populates="transaction", uselist=False, cascade="all, delete-orphan")
    fraud_reports = relationship("FraudReport", back_populates="transaction", cascade="all, delete-orphan")
