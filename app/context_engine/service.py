from sqlalchemy.orm import Session

from app.context_engine.models import (
    ContextLog
)

from app.context_engine.detectors import (
    detect_contexts
)


def generate_contexts(
    db: Session,
    telemetry
):

    contexts = detect_contexts(telemetry)

    created_contexts = []

    for context in contexts:

        context_log = ContextLog(
            user_id=telemetry.user_id,
            telemetry_id=telemetry.id,
            context_name=context.value
        )

        db.add(context_log)

        created_contexts.append(context_log)

    db.commit()

    return created_contexts