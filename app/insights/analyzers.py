def analyze_behavioral_patterns(
    strain_logs,
    recovery_logs
):

    insights = []

    high_strain_count = len([
        s for s in strain_logs
        if s.risk_level == "high"
    ])

    improved_recovery_count = len([
        r for r in recovery_logs
        if r.recovery_status
        == "improved"
    ])

    if high_strain_count >= 3:
        insights.append(
            "frequent_high_strain"
        )

    if improved_recovery_count >= 3:
        insights.append(
            "consistent_recovery"
        )

    return insights