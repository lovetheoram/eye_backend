def retrieve_recent_context(
    conversations,
    limit=5
):

    recent = conversations[-limit:]

    context = []

    for convo in recent:

        context.append({

            "user":
            convo.user_message,

            "assistant":
            convo.assistant_response
        })

    return context