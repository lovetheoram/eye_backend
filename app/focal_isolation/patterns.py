"""
Server-defined dot movement patterns.

The client renders the animation, but the server
owns the configuration — allows A/B testing and
pattern rotation without app updates.
"""


PATTERNS = {

    "linear": {
        "title": "Horizontal Sweep",
        "path": "horizontal_sweep",
        "speed": 0.05,
        "loops": 3,
        "description": (
            "Smooth left-to-right sweep "
            "forcing horizontal saccades."
        )
    },

    "figure_eight": {
        "title": "Figure Eight",
        "path": "lemniscate",
        "speed": 0.04,
        "loops": 2,
        "description": (
            "Infinity path engaging both "
            "horizontal and vertical muscles."
        )
    },

    "spiral": {
        "title": "Outward Spiral",
        "path": "archimedean",
        "speed": 0.03,
        "loops": 1,
        "description": (
            "Expanding spiral forcing "
            "progressive focal distance shift."
        )
    }
}

# Default pattern for new users
DEFAULT_PATTERN = "linear"

# Neon orange — high contrast on pitch black
DEFAULT_DOT_COLOR = "#FF6600"

# Fixed 20 seconds — the hard stop
SESSION_DURATION_MS = 20000

# Expected frames at 60fps over 20s
EXPECTED_FRAME_COUNT = 1200


def get_pattern_config(pattern_type: str) -> dict:
    """
    Returns the full pattern config for the client.
    Falls back to linear if unknown pattern is requested.
    """

    pattern = PATTERNS.get(
        pattern_type,
        PATTERNS[DEFAULT_PATTERN]
    )

    return {
        "pattern": pattern,
        "dot_color": DEFAULT_DOT_COLOR,
        "duration_ms": SESSION_DURATION_MS,
        "expected_frame_count": EXPECTED_FRAME_COUNT
    }
