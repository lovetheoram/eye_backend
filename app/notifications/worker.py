import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.notifications.send_all_user_notifications import send_all_user_notifications
from app.core.config import settings

from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler(
    jobstores={
        "default": SQLAlchemyJobStore(
            url=settings.DATABASE_URL
        )
    }
)


def run_notification_job():
    try:
        send_all_user_notifications(SessionLocal)
    except Exception as e:
        logger.error("notification_job_failed", extra={"error": str(e)})


def start_scheduler(db_session_factory=None):
    if scheduler.running:
        return  # Prevent double-start in multi-worker

    scheduler.add_job(
        run_notification_job,
        "interval",
        minutes=5,
        max_instances=1,
        misfire_grace_time=60,
        id="notification_job",
        replace_existing=True
    )
    scheduler.start()
    logger.info("notification_scheduler_started")