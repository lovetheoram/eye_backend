from app.telemetry.service import (
    create_telemetry_log
)

from app.context_engine.service import (
    generate_contexts
)

from app.strain_engine.service import (
    generate_strain_state
)

from app.notifications.service import (
    process_notification
)

from app.prediction.service import (
    predict_next_check_in
)


def process_behavioral_heartbeat(
    db,
    user_id,
    payload
):

    telemetry = create_telemetry_log(
        db=db,
        user_id=user_id,
        payload=payload
    )

    contexts = generate_contexts(
        db=db,
        telemetry=telemetry
    )

    strain = generate_strain_state(
        db=db,
        telemetry=telemetry,
        contexts=contexts
    )

    process_notification(
        db=db,
        strain_log=strain
    )

    prediction = predict_next_check_in(
        strain_score=strain.strain_score
    )

    return {
        "telemetry": telemetry,

        "contexts": [
            c.context_name
            for c in contexts
        ],

        "strain": strain,

        "next_check_in_minutes":
            prediction["next_check_in_minutes"],

        "message":
            prediction["message"],

        "strain_score":
            strain.strain_score,

        "strain_level":
            strain.risk_level
    }