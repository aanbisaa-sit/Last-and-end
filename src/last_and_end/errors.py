"""
errors.py — shared exception hierarchy for last-and-end.

Only *last_and_end*-specific exceptions live here.
Standard-library exceptions (ValueError, TypeError, …) are raised
directly in calling code where appropriate.
"""


class TrackerError(Exception):
    """Base class for all last-and-end errors."""


class ConfigurationError(TrackerError):
    """Raised when a config file is missing, unreadable, or semantically invalid."""


class CheckError(TrackerError):
    """Raised when checker invariants are violated (programmer error)."""


class TimeoutError(CheckError):
    """Raised when a single check attempt exceeds the deadline before any response.

    Different from :class:`RetryExhaustedError` which covers the *whole*
    retry cycle.
    """


class RetryExhaustedError(TrackerError):
    """Raised when all retries are exhausted and every attempt failed.

    Attributes:
        attempts: total number of attempts made (1 + retries).
        last_error: the error message from the final attempt.
    """

    def __init__(self, attempts: int, last_error: str | None = None):
        self.attempts   = attempts
        self.last_error = last_error
        msg = f"all {attempts} attempt(s) failed"
        if last_error:
            msg += f" (last: {last_error})"
        super().__init__(msg)
