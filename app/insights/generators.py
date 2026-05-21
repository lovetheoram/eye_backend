from app.insights.templates import (
    INSIGHT_TEMPLATES
)


def generate_insight_objects(
    insight_keys
):

    generated = []

    for key in insight_keys:

        template = (
            INSIGHT_TEMPLATES.get(key)
        )

        if not template:
            continue

        generated.append({

            "key": key,

            "title":
            template["title"],

            "message":
            template["message"]
        })

    return generated