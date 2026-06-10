from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class RiskScoreOut(BaseModel):
    score: int
    level: str
    classification: str
    reasons: str

    model_config = {"from_attributes": True}


class TransactionBase(BaseModel):
    reference: str | None = Field(default=None, max_length=80)
    amount: Decimal = Field(gt=0)
    sender_account: str | None = None
    recipient_account: str | None = None
    branch: str | None = None
    country: str | None = None
    ip_address: str | None = None
    channel: str | None = None
    transaction_time: datetime | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0)
    sender_account: str | None = None
    recipient_account: str | None = None
    branch: str | None = None
    country: str | None = None
    ip_address: str | None = None
    channel: str | None = None
    transaction_time: datetime | None = None


class TransactionOut(BaseModel):
    id: int
    reference: str
    amount: Decimal
    sender_account: str | None
    recipient_account: str | None
    branch: str | None
    country: str | None
    ip_address: str | None
    channel: str | None
    status: str
    transaction_time: datetime
    risk_score: RiskScoreOut | None = None

    model_config = {"from_attributes": True}
