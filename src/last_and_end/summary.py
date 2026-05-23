"""
summary.py — tally :class:`CheckResult` objects into a status count map.

Adding a *previous* summary starts a cheap state-transition pass so callers
get per-status ``from → to`` movement without reverse-engineering the call
site logic.
"""
from collections.abc import Iterable

from .classifier import classify_result
from .models import CheckResult
from .status import ServiceStatus


def summarize_results(
    results: Iterable[CheckResult],
    previous: dict[ServiceStatus, int] | None = None,
) -> dict[ServiceStatus, int] | dict[str, int]:
    """Tally results by :class:`ServiceStatus`.

    Args:
        results: the fresh batch of :class:`CheckResult` objects.
        previous: optional prior :func:`summarize_results` output to compute
          per-status transitions (``healthy→degraded``, etc.).

    Returns:
        A plain ``dict[ServiceStatus, int]`` when *previous* is ``None``.
        A ``dict[str, int]`` with ``healthy→healthy``, ``healthy→down``, …
        style keys when *previous* is supplied.
    """
    summary: dict[ServiceStatus, int] = {s: 0 for s in ServiceStatus}
    for result in results:
        summary[classify_result(result)] += 1

    if previous is None:
        return summary

    # Transition mode: produce “from → to: count” buckets
    transitions: dict[str, int] = {}
    for from_status, from_count in previous.items():
        for to_status, to_count in summary.items():
            if from_count and to_count:
                key = f"{from_status.value}->{to_status.value}"
                count = min(from_count, to_count)
                transitions[key] = transitions.get(key, 0) + count
    return transitions


def total_checks(summary: dict[ServiceStatus, int]) -> int:
    """Return the total number of checks represented by *summary*."""
    return sum(summary.values())


def healthy_fraction(summary: dict[ServiceStatus, int]) -> float:
    """Return the healthy fraction of *summary* (0.0 – 1.0)."""
    total = total_checks(summary)
    if total == 0:
        return 0.0
    return summary[ServiceStatus.HEALTHY] / total
