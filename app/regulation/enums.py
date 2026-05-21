from enum import Enum


class RegulationMode(str, Enum):

    HORIZON = "horizon"

    BREATHING = "breathing"

    PERIPHERAL = "peripheral"

    DARKNESS = "darkness"

    VISUAL_DRIFT = "visual_drift"