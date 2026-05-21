BLOCKED_PATTERNS = [

    "diagnosis",
    "medical certainty",
    "disease prediction",
    "clinical claims"
]


def validate_response(
    response
):

    lowered = response.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in lowered:
            return False

    return True