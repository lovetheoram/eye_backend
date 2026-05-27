from enum import Enum


class PatternType(str, Enum):

    LINEAR = "linear"

    FIGURE_EIGHT = "figure_eight"

    SPIRAL = "spiral"


class SessionStatus(str, Enum):

    ACTIVE = "active"

    COMPLETED = "completed"

    SKIPPED = "skipped"

    EXPIRED = "expired"
