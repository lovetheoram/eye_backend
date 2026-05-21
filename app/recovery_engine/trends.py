def calculate_average_recovery(
    recovery_logs
):

    if not recovery_logs:
        return 0

    total = sum(
        log.recovery_delta
        for log in recovery_logs
    )

    average = (
        total / len(recovery_logs)
    )

    return round(average, 2)