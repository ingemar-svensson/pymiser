# app/main.py

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.api.v1.endpoints import auth, users
from app.core.config import settings

app = FastAPI(
    title="Auth Service",
    version="1.0.0",
)

# Add session middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Include API routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
