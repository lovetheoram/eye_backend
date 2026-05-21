from enum import Enum


class InsightType(str, Enum):

    STRAIN_PATTERN = (
        "strain_pattern"
    )

    RECOVERY_PATTERN = (
        "recovery_pattern"
    )

    ATTENTION_PATTERN = (
        "attention_pattern"
    )

    IMPROVEMENT_PATTERN = (
        "improvement_pattern"
    )