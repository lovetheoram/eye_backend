from contextlib import asynccontextmanager
from fastapi import FastAPI

# Router imports — actual module locations
from app.api.auth import router as auth_router
from app.api.insights import router as insights_router
from app.api.telemetry import router as telemetry_router
from app.regulation.router import router as regulation_router
from app.api.context import router as context_router
from app.strain_engine.router import router as strain_router
from app.notifications.router import router as notification_router
from app.recovery_engine.router import router as recovery_router
from app.adaptive_engine.router import router as adaptive_router
from app.ai_companion.router import router as ai_router
from app.focal_isolation.router import router as focal_isolation_router
from app.streaks.router import router as streaks_router
from app.donations.router import router as donations_router

# Scheduler import
from app.notifications.worker import start_scheduler

# Database session for scheduler
from app.db.session import SessionLocal

# Middleware & utilities
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings

import structlog
import logging


# --- Structured Logging Setup ---
logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
)
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
logger = structlog.get_logger()


# --- Lifespan (replaces deprecated @app.on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("starting_scheduler")
    start_scheduler(SessionLocal)
    yield
    # Shutdown
    logger.info("shutting_down")


# --- Initialize FastAPI ---
app = FastAPI(
    title="Eye Buddy API",
    version="1.0.0",
    lifespan=lifespan,
)


# --- Rate Limiter ---
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.RATE_LIMIT],
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# --- CORS Middleware ---
cors_origins = [
    origin.strip()
    for origin in settings.CORS_ORIGINS.split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Include Routers ---
app.include_router(auth_router)
app.include_router(insights_router)
app.include_router(telemetry_router)
app.include_router(regulation_router)
app.include_router(context_router)
app.include_router(strain_router)
app.include_router(notification_router)
app.include_router(recovery_router)
app.include_router(adaptive_router)
app.include_router(ai_router)
app.include_router(focal_isolation_router)
app.include_router(streaks_router)
app.include_router(donations_router)


# --- Health Check ---
@app.get("/health")
def health_check():
    """Health check with DB connectivity verification."""
    from sqlalchemy import text
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "degraded", "database": "unreachable"}


# --- Root ---
@app.get("/")
def root():
    return {"message": "Eye Buddy API Running"}
