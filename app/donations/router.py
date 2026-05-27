from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.dependencies import (
    get_current_user
)

from app.donations.schemas import (
    DonationAction
)

from app.donations.service import (
    log_donation_action,
    get_payment_configs
)

router = APIRouter(
    prefix="/donations",
    tags=["Donations"]
)


@router.get("/config")
def get_donation_config(
    db: Session = Depends(get_db)
):
    """
    Returns active payment configurations.
    Server-managed — updateable without
    app release.
    """

    configs = get_payment_configs(db=db)

    return {
        "payment_options": [
            {
                "payment_app": c.payment_app,
                "display_name": c.display_name,
                "deep_link_template": (
                    c.deep_link_template
                ),
                "upi_id": c.upi_id,
                "suggested_amounts": (
                    c.suggested_amounts
                ),
                "icon_name": c.icon_name
            }
            for c in configs
        ]
    }


@router.post(
    "/prompt/{prompt_id}/action"
)
def record_donation_action(
    prompt_id: str,
    payload: DonationAction,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):
    """
    Logs user action on a donation prompt.
    Used for analytics only — never gates
    features or content.
    """

    prompt = log_donation_action(
        db=db,
        prompt_id=prompt_id,
        action_taken=payload.action_taken
    )

    if not prompt:
        raise HTTPException(
            status_code=404,
            detail="Donation prompt not found"
        )

    return {
        "status": "logged",
        "action": payload.action_taken
    }
