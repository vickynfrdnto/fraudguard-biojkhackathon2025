from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, decode_token, hash_password, sanitize, verify_password
from app.models.user import User
from app.schemas.auth import ForgotPasswordRequest, LoginRequest, RefreshRequest, RegisterRequest, ResetPasswordRequest, TokenPair, VerifyEmailRequest

router = APIRouter()


@router.post("/register", response_model=TokenPair, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(
        email=payload.email.lower(),
        full_name=sanitize(payload.full_name) or payload.full_name,
        hashed_password=hash_password(payload.password),
        verification_token=uuid4().hex,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _tokens(user.id)


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return _tokens(user.id)


@router.post("/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest):
    try:
        user_id = decode_token(payload.refresh_token, "refresh")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc
    return _tokens(int(user_id))


@router.post("/logout")
def logout():
    return {"detail": "Logged out"}


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if user:
        user.reset_token = uuid4().hex
        db.commit()
    return {"detail": "If the email exists, reset instructions have been created"}


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.reset_token == payload.token))
    if not user:
        raise HTTPException(status_code=400, detail="Invalid reset token")
    user.hashed_password = hash_password(payload.password)
    user.reset_token = None
    db.commit()
    return {"detail": "Password reset successful"}


@router.post("/verify-email")
def verify_email(payload: VerifyEmailRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.verification_token == payload.token))
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    user.is_verified = True
    user.verification_token = None
    db.commit()
    return {"detail": "Email verified"}


def _tokens(user_id: int) -> TokenPair:
    subject = str(user_id)
    return TokenPair(access_token=create_access_token(subject), refresh_token=create_refresh_token(subject))
