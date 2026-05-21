from app.ai_companion.prompts import (
    build_reflection_prompt
)

from app.ai_companion.emotional_tone import (
    determine_emotional_tone
)


def generate_companion_response(
    user_message,
    profile,
    latest_insight
):

    tone = determine_emotional_tone(
        strain_level="moderate",
        recovery_profile=(
            profile.recovery_profile
        )
    )

    prompt = build_reflection_prompt(
        user_message=user_message,
        behavioral_profile=profile,
        latest_insight=latest_insight,
        emotional_tone=tone
    )

    # future LLM call here

    simulated_response = (
        "It seems your visual "
        "system has been under "
        "steady focus recently. "
        "A slower visual rhythm "
        "may help tonight."
    )

    return simulated_response