from app.strain_engine.rules import (
    CONTEXT_WEIGHTS,
    HIGH_BRIGHTNESS_WEIGHT,
    LONG_SCREEN_TIME_WEIGHT,
    FOCUS_LOCK_WEIGHT,
    HIGH_SCREEN_THRESHOLD,
    FOCUS_LOCK_THRESHOLD
)

def calculate_strain_score(
    telemetry,
    contexts
):

    score = 0

    # ✅ FIX: handle None safely
    contexts = contexts or []

    for context in contexts:

        score += CONTEXT_WEIGHTS.get(
            context.context_name,
            0
        )

    if telemetry.brightness_level >= 80:
        score += HIGH_BRIGHTNESS_WEIGHT

    if telemetry.screen_on_minutes >= HIGH_SCREEN_THRESHOLD:
        score += LONG_SCREEN_TIME_WEIGHT

    if telemetry.continuous_focus_minutes >= FOCUS_LOCK_THRESHOLD:
        score += FOCUS_LOCK_WEIGHT

    return max(score, 0)