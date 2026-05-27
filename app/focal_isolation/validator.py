"""
Session integrity validator.

Prevents fake completions by verifying:
1. Minimum elapsed time (19.5s for 20s session)
2. Client frame count within expected range
3. Session wasn't already completed
"""

import logging

from datetime import datetime, timezone

from app.focal_isolation.patterns import (
    EXPECTED_FRAME_COUNT
)

logger = logging.getLogger(__name__)

# Allow 500ms clock drift tolerance
MIN_DURATION_MS = 19500

# Client must render at least 80% of expected frames
MIN_FRAME_RATIO = 0.80


def validate_completion(
    session,
    client_report
):
    """
    Validates a session completion report.

    Returns:
        dict with 'valid', 'integrity_score',
        and 'rejection_reason' fields.
    """

    # Already completed — reject duplicate
    if session.completed:
        return {
            "valid": False,
            "integrity_score": 0.0,
            "rejection_reason": (
                "session_already_completed"
            )
        }

    # Already marked as skipped
    if session.skipped:
        return {
            "valid": False,
            "integrity_score": 0.0,
            "rejection_reason": (
                "session_was_skipped"
            )
        }

    # Verify minimum elapsed time
    now = datetime.now(timezone.utc)

    if session.started_at:

        elapsed_ms = (
            (now - session.started_at)
            .total_seconds() * 1000
        )

        if elapsed_ms < MIN_DURATION_MS:
            logger.warning(
                "focal_isolation_too_fast",
                extra={
                    "session_id": str(session.id),
                    "elapsed_ms": elapsed_ms
                }
            )

            return {
                "valid": False,
                "integrity_score": 0.0,
                "rejection_reason": (
                    "completed_too_quickly"
                )
            }

    # Calculate integrity score from frame count
    client_frames = (
        client_report.client_frame_count
        or 0
    )

    expected = (
        session.expected_frame_count
        or EXPECTED_FRAME_COUNT
    )

    if expected > 0:
        integrity_score = min(
            client_frames / expected,
            1.0
        )
    else:
        integrity_score = 0.0

    # Check minimum frame ratio
    if integrity_score < MIN_FRAME_RATIO:
        logger.warning(
            "focal_isolation_low_integrity",
            extra={
                "session_id": str(session.id),
                "integrity_score": integrity_score,
                "client_frames": client_frames
            }
        )

        return {
            "valid": False,
            "integrity_score": integrity_score,
            "rejection_reason": (
                "insufficient_frame_count"
            )
        }

    return {
        "valid": True,
        "integrity_score": integrity_score,
        "rejection_reason": None
    }
