from exponent_server_sdk import (
    PushClient,
    PushMessage
)


def deliver_notification(
    expo_push_token: str,
    message: str
):

    if not expo_push_token:
        return False

    try:

        response = PushClient().publish(

            PushMessage(
                to=expo_push_token,

                body=message,

                sound="default",

                data={
                    "screen": "regulation"
                }
            )
        )
        print(response,"  message sent successfull.")
        return response.is_success()

    except Exception as e:

        print(
            f"Push notification failed: {e}"
        )

        return False


# def deliver_notification(
#     message: str
# ):

#     """
#     Placeholder for:
#     - Firebase Push
#     - Android Local Notification
#     - Email
#     - Future wearable delivery
#     """

#     print(
#         f"Delivering Notification: {message}"
#     )

#     return True