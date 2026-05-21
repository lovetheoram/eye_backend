from sqlalchemy.orm import Session

from app.insights.models import (
    InsightLog
)

from app.insights.analyzers import (
    analyze_behavioral_patterns
)

from app.insights.generators import (
    generate_insight_objects
)

def generate_user_insights(
    db: Session,
    user_id,
    strain_logs,
    recovery_logs
):

    keys = analyze_behavioral_patterns(
        strain_logs,
        recovery_logs
    )

    generated = generate_insight_objects(
        keys
    )

    existing_titles = db.query(
        InsightLog.title
    ).filter(
        InsightLog.user_id == user_id
    ).all()

    existing_titles = [
        item[0]
        for item in existing_titles
    ]

    stored = []

    for insight in generated:

        if insight["title"] in existing_titles:
            continue

        log = InsightLog(

            user_id=user_id,

            insight_type=insight["key"],

            title=insight["title"],

            message=insight["message"]
        )

        db.add(log)

        stored.append(log)

    db.commit()

    return stored