def generate_weekly_summary(
    strain_logs,
    recovery_logs
):

    avg_strain = round(
        sum(
            s.strain_score
            for s in strain_logs
        ) / max(len(strain_logs), 1),
        2
    )

    recovery_count = len([
        r for r in recovery_logs
        if r.recovery_status
        == "improved"
    ])

    return {

        "average_strain":
        avg_strain,

        "successful_recoveries":
        recovery_count
    }