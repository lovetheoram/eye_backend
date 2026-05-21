from enum import Enum


class AppCategory(str, Enum):
    CODING = "coding"
    SOCIAL = "social"
    ENTERTAINMENT = "entertainment"
    READING = "reading"
    PRODUCTIVITY = "productivity"
    UNKNOWN = "unknown"


class TimeOfDay(str, Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"