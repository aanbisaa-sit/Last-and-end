"""
serialize.py — convert CheckResult objects to/from plain dictionaries.

Used by store backends, notification payloads, and disk snapshots.
All datetime values are serialised as ISO-8601 strings so that the
result is JSON-safe without a custom encoder.
"""
from datetime import datetime
from typing import Any

from .models import CheckResult, Endpoint


def result_to_dict(result: CheckResult) -> dict[str, Any]:
    """Serialise a :class:`CheckResult` to a JSON-friendly dict."""
    return {
        "name":             result.endpoint.name,
        "url":              result.endpoint.url,
        "expected_status":  result.endpoint.expected_status,
        "status_code":      result.status_code,
        "latency_ms":       result.latency_ms,
        "checked_at":       result.checked_at.isoformat(),
        "error":            result.error,
    }


def result_from_dict(data: dict[str, Any]) -> CheckResult:
    """Reconstruct a :class:`CheckResult` from a dict produced by :func:`result_to_dict`.

    Accepts ``None`` for nullable fields and normalises types so that
    values loaded from JSON (which are always strings) round-trip cleanly.
    """
    endpoint = Endpoint(
        name     = str(data["name"]),
        url      = str(data["url"]),
        expected_status = int(data["expected_status"]),
    )
    checked_at  = datetime.fromisoformat(str(data["checked_at"]))
    raw_status  = data.get("status_code")
    raw_latency = data.get("latency_ms")
    raw_error   = data.get("error")
    return CheckResult(
        endpoint      = endpoint,
        status_code   = None if raw_status is None else int(raw_status),
        latency_ms    = None if raw_latency is None else int(raw_latency),
        checked_at    = checked_at,
        error         = None if raw_error is None else str(raw_error),
    )
