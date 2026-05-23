"""Immutable data types used throughout last-and-end."""
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class Endpoint:
    """A single HTTP endpoint to probe.

    Attributes:
        name: human-readable label, used in reports and logs.
        url: full URL including scheme (e.g. ``https://example.com/health``).
        expected_status: HTTP status code treated as healthy (default 200).
    """

    name: str
    url: str
    expected_status: int = 200


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Outcome of a single :func:`checker.check_endpoint` call.

    Attributes:
        endpoint: the endpoint that was probed.
        status_code: HTTP status code returned, or ``None`` on network error.
        latency_ms: round-trip time in milliseconds, or ``None`` on error.
        checked_at: UTC timestamp of when the check finished.
        error: short error class name (e.g. ``TimeoutError``), or ``None``.
    """

    endpoint:      Endpoint
    status_code:   int | None
    latency_ms:    int | None
    checked_at:    datetime
    error:         str | None = None

    @property
    def ok(self) -> bool:
        """``True`` when the response matched the expected status and no error occurred."""
        return self.error is None and self.status_code == self.endpoint.expected_status


def utc_now() -> datetime:
    """Return the current UTC time with tzinfo set."""
    return datetime.now(timezone.utc)
