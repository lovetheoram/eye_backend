def calculate_recovery_effectiveness(
    pre_score: int,
    post_score: int
):

    if pre_score == 0:
        return 0

    improvement = (
        pre_score - post_score
    )

    effectiveness = (
        improvement / pre_score
    ) * 100

    return round(effectiveness, 2)