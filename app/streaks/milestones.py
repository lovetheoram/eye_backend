"""
Streak milestone definitions.

Milestones trigger the gratitude card
and optional donation prompt.
"""

MILESTONES = [
    7,      # 1 week of daily resets
    14,     # 2 weeks
    30,     # 1 month
    50,     # Dedicated user
    100,    # Eye health champion
    200,    # Power user
    365     # Full year
]

# Milestone messages shown on the
# gratitude card
MILESTONE_MESSAGES = {
    7: (
        "7 resets in a row. Your eyes "
        "are already thanking you."
    ),
    14: (
        "Two weeks strong. You've built "
        "a real eye health habit."
    ),
    30: (
        "One month of consistent eye care. "
        "That's rare. That's powerful."
    ),
    50: (
        "50 resets. You're not just using "
        "the app — you're protecting "
        "your vision."
    ),
    100: (
        "100 resets. You've earned the "
        "title: Eye Health Champion."
    ),
    200: (
        "200 resets. Your future self "
        "will thank you for this."
    ),
    365: (
        "A full year of eye care. "
        "This is extraordinary."
    )
}


def check_milestone(
    current_streak: int,
    last_milestone_shown: int
) -> int | None:
    """
    Returns the milestone to show,
    or None if no new milestone reached.

    Only returns milestones that haven't
    been shown yet (higher than last_shown).
    """

    for milestone in MILESTONES:

        if (
            current_streak >= milestone
            and milestone > last_milestone_shown
        ):
            return milestone

    return None


def get_milestone_message(
    milestone: int
) -> str:
    """
    Returns the gratitude card message
    for a given milestone.
    """

    return MILESTONE_MESSAGES.get(
        milestone,
        (
            f"{milestone} resets strong. "
            "Keep going."
        )
    )
