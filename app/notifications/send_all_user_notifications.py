from app.notifications.user_selector import get_active_users
from app.strain_engine.service import generate_strain_state
from app.notifications.service import process_notification
from app.telemetry.models import TelemetryLog


def send_all_user_notifications(db_session_factory):

    db = db_session_factory()

    try:
        users = get_active_users(db)

        for user in users:

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

    finally:
        db.close()