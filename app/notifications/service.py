


from app.notifications.models import NotificationLog
from app.notifications.cooldowns import can_send_notification
from app.notifications.triggers import determine_notification_type
from app.notifications.templates import generate_message
from app.notifications.delivery import deliver_notification
from app.auth.models import User
from app.notifications.enums import NotificationType  # Imported for testing default

def process_notification(db, strain_log):
    """
    [TESTING MODE] Cooldown protection bypassed
    To restore production behavior, uncomment the check below:
    """
    # if not can_send_notification(db, strain_log.user_id):
    #     return None

    """
    Determine notification type with a fallback default for testing
    """
    notification_type = determine_notification_type(strain_log)

    if not notification_type:
        # FALLBACK: If strain criteria are not fulfilled, force a default type for testing
        notification_type = NotificationType.GENTLE_AWARENESS

    """
    Generate human-friendly message
    """
    message = generate_message(notification_type)

    """
    Get user and handle potential missing records safely
    """
    user = db.query(User).filter(User.id == strain_log.user_id).first()
    if not user:
        print(f"Testing Error: No user found with ID {strain_log.user_id}")
        return None
        
    if not user.expo_push_token:
        print(f"Testing Error: User {user.id} does not have an expo_push_token set.")
        return None

    """
    Send push notification
    """
    delivered = deliver_notification(
        user.expo_push_token,
        message
    )

    """
    Store notification history
    """
    notification = NotificationLog(
        user_id=strain_log.user_id,
        strain_log_id=strain_log.id,
        notification_type=notification_type.value,
        message=message,
        delivered=delivered  # This saves True or False directly to your DB log
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification