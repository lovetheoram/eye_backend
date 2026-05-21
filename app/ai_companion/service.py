from sqlalchemy.orm import Session

from app.ai_companion.models import (
    ConversationLog
)

from app.ai_companion.conversation_engine import (
    generate_companion_response
)


def process_conversation(
    db: Session,
    user_id,
    user_message,
    profile,
    latest_insight
):

    response = (
        generate_companion_response(
            user_message,
            profile,
            latest_insight
        )
    )

    conversation = ConversationLog(

        user_id=user_id,

        user_message=user_message,

        assistant_response=response,

        emotional_tone="reflective"
    )

    db.add(conversation)

    db.commit()

    db.refresh(conversation)

    return conversation