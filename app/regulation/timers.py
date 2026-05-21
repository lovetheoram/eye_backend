def validate_duration(
    duration_seconds: int
):

    MIN_DURATION = 30

    MAX_DURATION = 1800

    return (
        MIN_DURATION
        <= duration_seconds
        <= MAX_DURATION
    )