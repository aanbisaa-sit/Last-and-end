"""
availability.py — uptime and availability utilities.

Provides:
- :func:`availability_ratio`: fraction of checks that passed.
- :func:`uptime_seconds`: total healthy time from a result list.
- :func:`classify_availability`: bucket a ratio into a status label.
"""
from collections.abc import Iterable

from .models import CheckResult
from .status import ServiceStatus


def availability_ratio(results: Iterable[CheckResult]) -> float:
    """Return the fraction of results that are **healthy** (0.0 – 1.0).

    An empty result list returns ``0.0`` (conservative — treat unknown
    availability as down).
    """
    items = list(results)
    if not items:
        return 0.0
    return sum(1 for r in items if r.ok) / len(items)


def uptime_seconds(results: Iterable[CheckResult]) -> float:
    """Return the total healthy time across all results in seconds.

    Each :class:`CheckResult` carries a single snapshot, so this is
    computed as:

    ``uptime = total_results × healthy_fraction × period_seconds``

    where *period_seconds* is the per-check interval.  Because the actual
    interval is not stored in the result, callers should pass the *monitor
    period* explicitly if they need an absolute time value.
    """
    result = list(results)
    return availability_ratio(result) * len(result)


def classify_availability(ratio: float) -> ServiceStatus:
    """Bucket a raw availability ratio into the nearest service state.

    Thresholds follow the project convention:

    - ``>= 0.99`` → :attr:`ServiceStatus.HEALTHY`
    - ``>= 0.90`` → :attr:`ServiceStatus.DEGRADED`
    - ``>= 0.00`` → :attr:`ServiceStatus.DOWN`
    """
    if ratio >= 0.99:
        return ServiceStatus.HEALTHY
    if ratio >= 0.90:
        return ServiceStatus.DEGRADED
    return ServiceStatus.DOWN
