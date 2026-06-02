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


def calculate_focus_battery(strain_score, time_of_day, continuous_focus_minutes):
    """
    Focus Battery (0-100%) — a Garmin Body Battery / WHOOP Recovery
    style metric that represents current mental & ciliary capacity.

    Starts at 100 and is reduced by:
    - Strain score (primary factor)
    - Time of day fatigue
    - Extended continuous focus duration
    """
    battery = 100

    # Strain deduction: each strain point costs 6% battery
    battery -= strain_score * 6

    # Time-of-day fatigue deduction
    time_deductions = {
        "morning": 0,
        "afternoon": 10,
        "evening": 20,
        "night": 35,
    }
    battery -= time_deductions.get(time_of_day, 0)

    # Extended focus duration penalty
    if continuous_focus_minutes > 40:
        battery -= 10

    # Clamp between 10 and 100
    return max(10, min(100, battery))


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

    # Calculate Focus Battery
    focus_battery = calculate_focus_battery(
        strain_score=strain.strain_score,
        time_of_day=telemetry.time_of_day,
        continuous_focus_minutes=telemetry.continuous_focus_minutes
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
            strain.risk_level,

        "focus_battery":
            focus_battery
    }