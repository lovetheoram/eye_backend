from fastapi import FastAPI

from app.auth.router import router as auth_router
# from app.visual_logs.router import router as visual_logs_router
# from app.analytics.router import router as analytics_router
from app.insights.router import router as insights_router
from app.telemetry.router import (
    router as telemetry_router
)


app = FastAPI(
    title="Eye Buddy API",
    version="1.0.0"
)

from app.regulation.router import router as regulation_router
from app.context_engine.router import router as context_router
from app.strain_engine.router import router as strain_router
from app.notifications.router import router as notification_router
from app.recovery_engine.router import router as recovery_router
from app.adaptive_engine.router import router as adaptive_router
from app.ai_companion.router import router as ai_router
from app.orchestration.behavioral_pipeline import process_behavioral_heartbeat

app.include_router(regulation_router)
app.include_router(auth_router)
# app.include_router(visual_logs_router)
# app.include_router(analytics_router)
app.include_router(insights_router)
app.include_router(telemetry_router)
app.include_router(context_router)
app.include_router(strain_router)
app.include_router(notification_router)
app.include_router(recovery_router)
app.include_router(adaptive_router)
app.include_router(ai_router)

from app.notifications.worker import start_scheduler
from app.db.session import SessionLocal
from fastapi.middleware.cors import (
    CORSMiddleware
)

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    start_scheduler(SessionLocal)

@app.get("/")
def root():
    return {
        "message": "Eye Buddy API Running"
    }

