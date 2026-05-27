import logging

from exponent_server_sdk import (
    PushClient,
    PushMessage
)

from app.notifications.templates import (
    generate_title
)

logger = logging.getLogger(__name__)


def deliver_notification(
    expo_push_token: str,
    message: str,
    notification_type=None,
    session_config=None
):
    """
    Delivers a high-priority push notification
    via Expo. Includes title, priority, channel,
    and auto-launch routing data for the client.
    """

    if not expo_push_token:
        return False

    # Generate contextual title
    title = "👁️ Eye Buddy"
    if notification_type:
        title = generate_title(
            notification_type
        )

    # Build notification data payload
    data = {
        "screen": "focal_isolation",
        "auto_launch": True
    }

    if session_config:
        data["session_config"] = (
            session_config
        )

    try:

        response = PushClient().publish(

            PushMessage(
                to=expo_push_token,

                title=title,

                body=message,

                sound="default",

                priority="high",

                channel_id="strain_alerts",

                data=data
            )
        )

        logger.info(
            "push_notification_sent",
            extra={
                "token": (
                    expo_push_token[:20]
                    + "..."
                ),
                "type": (
                    notification_type.value
                    if notification_type
                    else "unknown"
                )
            }
        )

        return response.is_success()

    except Exception as e:

        logger.error(
            "push_notification_failed",
            extra={
                "error": str(e),
                "token": (
                    expo_push_token[:20]
                    + "..."
                )
            }
        )

        return False