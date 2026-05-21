from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.dependencies import (
    get_current_user
)

from app.ai_companion.schemas import (
    ConversationRequest
)

from app.ai_companion.service import (
    process_conversation
)

router = APIRouter(
    prefix="/companion",
    tags=["AI Companion"]
)


@router.post("/chat")
def companion_chat(
    payload: ConversationRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):

    # mock profile and insight
    profile = current_user.profile
    latest_insight = (
        current_user.latest_insight
    )

    conversation = process_conversation(
        db=db,
        user_id=current_user.id,
        user_message=payload.message,
        profile=profile,
        latest_insight=latest_insight
    )

    return {
        "assistant_response":
        conversation.assistant_response,

        "emotional_tone":
        conversation.emotional_tone
    }