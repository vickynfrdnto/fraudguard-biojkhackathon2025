from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.api.router import api_router
from app.core.config import settings
from app.core.database import Base, engine
from app.middleware.security_headers import SecurityHeadersMiddleware

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT])


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0", openapi_url="/api/openapi.json")
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_handler)
    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix="/api")
    Base.metadata.create_all(bind=engine)
    return app


async def _rate_limit_handler(request: Request, exc: RateLimitExceeded):
    from fastapi.responses import JSONResponse

    return JSONResponse({"detail": "Too many requests"}, status_code=429)


app = create_app()
