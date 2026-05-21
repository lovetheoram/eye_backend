from app.telemetry.enums import AppCategory


APP_CLASSIFICATION = {

    "com.termux": AppCategory.CODING,

    "com.instagram.android": AppCategory.SOCIAL,

    "com.google.android.youtube":
        AppCategory.ENTERTAINMENT,

    "com.amazon.kindle":
        AppCategory.READING,
}


def classify_app(app_name: str) -> AppCategory:

    return APP_CLASSIFICATION.get(
        app_name,
        AppCategory.UNKNOWN
    )