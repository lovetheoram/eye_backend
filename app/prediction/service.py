def predict_next_check_in(
    strain_score: float,
    work_type: str | None = None
):

    """
    Higher strain
    → quicker reminder
    """

    if strain_score >= 80:

        return {
            "next_check_in_minutes": 1,

            "message":
                "High eye strain detected. Look away from the screen and blink slowly."
        }

    elif strain_score >= 60:

        return {
            "next_check_in_minutes": 1,

            "message":
                "Your eyes are under moderate stress. Relax focus for a few seconds."
        }

    elif strain_score >= 40:

        return {
            "next_check_in_minutes": 1,

            "message":
                "Take a small visual reset break."
        }

    else:

        return {
            "next_check_in_minutes": 1,

            "message":
                "Healthy visual flow detected. Remember to blink naturally."
        }