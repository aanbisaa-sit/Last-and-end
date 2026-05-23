"""
tests/test_serialize.py — round-trip contract for serialize module.

Every field that survives a result_to_dict → result_from_dict cycle
must be byte-for-byte equal to the original value.
"""
from datetime import datetime, timezone

import pytest

from last_and_end.models import CheckResult, Endpoint
from last_and_end.serialize import result_from_dict, result_to_dict


NOW = datetime(2026, 5, 23, 14, 0, 0, tzinfo=timezone.utc)


@pytest.fixture()
def healthy_result() -> CheckResult:
    return CheckResult(
        endpoint=Endpoint("home", "https://example.com", 200),
        status_code=200,
        latency_ms=42,
        checked_at=NOW,
        error=None,
    )


@pytest.fixture()
def down_result() -> CheckResult:
    return CheckResult(
        endpoint=Endpoint("api", "https://api.example.com", 200),
        status_code=None,
        latency_ms=None,
        checked_at=NOW,
        error="ConnectionRefused",
    )


@pytest.fixture()
def degraded_result() -> CheckResult:
    return CheckResult(
        endpoint=Endpoint("old", "https://old.example.com", 200),
        status_code=503,
        latency_ms=150,
        checked_at=NOW,
        error=None,
    )


# ── round-trip ────────────────────────────────────────────────────────────────

def test_roundtrip_healthy(healthy_result: CheckResult):
    d = result_to_dict(healthy_result)
    r = result_from_dict(d)
    assert r == healthy_result


def test_roundtrip_down(down_result: CheckResult):
    d = result_to_dict(down_result)
    r = result_from_dict(d)
    assert r == down_result
    assert r.status_code is None
    assert r.latency_ms is None
    assert r.error == "ConnectionRefused"


def test_roundtrip_degraded(degraded_result: CheckResult):
    d = result_to_dict(degraded_result)
    r = result_from_dict(d)
    assert r == degraded_result
    assert r.error is None


# ── field invariance ──────────────────────────────────────────────────────────

def test_checked_at_roundtrip_preserves_isoformat(healthy_result: CheckResult):
    d = result_to_dict(healthy_result)
    assert d["checked_at"] == NOW.isoformat()
    r = result_from_dict(d)
    assert r.checked_at == NOW


def test_url_is_string_after_roundtrip(healthy_result: CheckResult):
    d = result_to_dict(healthy_result)
    assert isinstance(d["url"], str)
    r = result_from_dict(d)
    assert r.endpoint.url == "https://example.com"


def test_error_none_roundtrips_as_none(healthy_result: CheckResult):
    d = result_to_dict(healthy_result)
    assert d["error"] is None
    r = result_from_dict(d)
    assert r.error is None
