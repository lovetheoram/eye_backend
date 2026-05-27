import logging

from app.notifications.user_selector import get_active_users
from app.strain_engine.service import generate_strain_state
from app.notifications.service import process_notification
from app.telemetry.models import TelemetryLog

logger = logging.getLogger(__name__)

BATCH_SIZE = 100


def send_all_user_notifications(db_session_factory):

    db = db_session_factory()

    try:
        users = get_active_users(db)
        total = len(users)
        processed = 0
        errors = 0

        logger.info("notification_batch_started", extra={"total_users": total})

        for user in users:
            try:
                # get latest telemetry only
                telemetry = db.query(TelemetryLog)\
                    .filter(TelemetryLog.user_id == user.id)\
                    .order_by(TelemetryLog.created_at.desc())\
                    .first()

                if not telemetry:
                    continue

                strain = generate_strain_state(
                    db=db,
                    telemetry=telemetry,
                    contexts=None
                )

                process_notification(
                    db=db,
                    strain_log=strain
                )

                processed += 1

            except Exception as e:
                errors += 1
                logger.error(
                    "notification_user_failed",
                    extra={"user_id": str(user.id), "error": str(e)}
                )
                # Continue processing remaining users
                continue

        logger.info(
            "notification_batch_completed",
            extra={"processed": processed, "errors": errors, "total": total}
        )

    finally:
        db.close()