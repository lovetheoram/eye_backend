from enum import Enum


class RecoveryStatus(str, Enum):

    IMPROVED = "improved"

    STABLE = "stable"

    WORSENED = "worsened"