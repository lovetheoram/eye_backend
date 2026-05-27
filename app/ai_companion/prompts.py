def build_reflection_prompt(
    user_message,
    behavioral_profile,
    latest_insight,
    emotional_tone
):
    focus_style = behavioral_profile.focus_profile if behavioral_profile else "standard"
    insight_msg = latest_insight.message if latest_insight else "Maintain clean visual habits."

    return f"""
You are a calm reflective
nervous-system companion.

User behavioral profile:
- Focus Style: {focus_style}

Latest insight: {insight_msg}

Emotional tone: {emotional_tone}

User says: {user_message}

Respond gently and reflectively.
Avoid medical advice.
Avoid productivity pressure.
"""