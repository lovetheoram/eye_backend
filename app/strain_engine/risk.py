from app.strain_engine.enums import (
    RiskLevel
)


def classify_risk(score: int):

    if score <= 3:
        return RiskLevel.LOW

    if score <= 6:
        return RiskLevel.MODERATE

    if score <= 10:
        return RiskLevel.HIGH

    return RiskLevel.SEVERE