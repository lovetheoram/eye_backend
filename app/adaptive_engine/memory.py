def calculate_average_focus(
    telemetry_logs
):

    if not telemetry_logs:
        return 0

    total = sum(
        t.continuous_focus_minutes
        for t in telemetry_logs
    )

    return round(
        total / len(telemetry_logs),
        2
    )


def calculate_average_recovery(
    recovery_logs
):

    if not recovery_logs:
        return 0

    total = sum(
        r.recovery_delta
        for r in recovery_logs
    )

    return round(
        total / len(recovery_logs),
        2
    )