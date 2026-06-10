from fastapi import APIRouter

from app.api.routes import auth, dashboard, detect, reports, transactions

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(detect.router, tags=["compatibility"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
