from sqlalchemy.orm import Session

from app.telemetry.models import TelemetryLog

from app.telemetry.schemas import (
    TelemetryHeartbeatCreate
)

from app.telemetry.classifiers import (
    classify_app
)


def create_telemetry_log(
    db: Session,
    user_id,
    payload: TelemetryHeartbeatCreate
):

    category = classify_app(payload.app_name)

    telemetry = TelemetryLog(
        user_id=user_id,
        app_name=payload.app_name,
        app_category=category.value,
        screen_on_minutes=payload.screen_on_minutes,
        continuous_focus_minutes=(
            payload.continuous_focus_minutes
        ),
        brightness_level=payload.brightness_level,
        session_count=payload.session_count,
        time_of_day=payload.time_of_day.value
    )

    db.add(telemetry)

    db.commit()

    db.refresh(telemetry)

    return telemetry