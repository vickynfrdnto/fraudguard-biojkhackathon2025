from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class RiskScore(Base, TimestampMixin):
    __tablename__ = "risk_scores"
    __table_args__ = (CheckConstraint("score >= 0 AND score <= 100", name="ck_risk_score_range"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id", ondelete="CASCADE"), unique=True, index=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[str] = mapped_column(String(20), nullable=False)
    classification: Mapped[str] = mapped_column(String(20), nullable=False)
    reasons: Mapped[str] = mapped_column(Text, default="", nullable=False)

    transaction = relationship("Transaction", back_populates="risk_score")
