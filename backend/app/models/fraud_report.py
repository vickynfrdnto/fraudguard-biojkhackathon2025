from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class FraudReport(Base, TimestampMixin):
    __tablename__ = "fraud_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(30), default="Open", nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    assigned_to: Mapped[str | None] = mapped_column(String(255))

    transaction = relationship("Transaction", back_populates="fraud_reports")
