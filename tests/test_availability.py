"""
tests/test_availability.py — uptime and availability helpers.

Covers:
- availability_ratio: all-healthy, all-down, half-healthy, empty input
- uptime_seconds: proportional to number of healthy results
- classify_availability: threshold boundaries at 0.99, 0.90, 0.00
"""
from datetime import datetime, timezone

import pytest

from last_and_end.availability import (
    availability_ratio,
    classify_availability,
    uptime_seconds,
)
from last_and_end.models import CheckResult, Endpoint
from last_and_end.status import ServiceStatus

NOW = datetime(2026, 5, 23, 14, 0, 0, tzinfo=timezone.utc)

# ── helpers ────────────────────────────────────────────────────────────────────

def healthy(name="a") -> CheckResult:
    return CheckResult(Endpoint(name, f"https://{name}.com"), 200, 10, NOW)

def down(name="b") -> CheckResult:
    return CheckResult(Endpoint(name, f"https://{name}.com"), None, None, NOW, error="ERR")

def degraded(name="c") -> CheckResult:
    return CheckResult(Endpoint(name, f"https://{name}.com"), 503, 20, NOW)


# ── availability_ratio ─────────────────────────────────────────────────────────
# 

def test_all_healthy_is_one():
    assert availability_ratio([healthy()]) == pytest.approx(1.0)


def test_all_down_is_zero():
    assert availability_ratio([down()]) == pytest.approx(0.0)


def test_half_healthy():
    assert availability_ratio([healthy(), down()]) == pytest.approx(0.5)


def test_three_quarters():
    assert availability_ratio([healthy(), healthy(), healthy(), down()]) == pytest.approx(0.75)


def test_empty_list_returns_zero():
    assert availability_ratio([]) == pytest.approx(0.0)


# ── uptime_seconds ─────────────────────────────────────────────────────────────

def test_uptime_all_healthy():
    assert uptime_seconds([healthy(), healthy()]) == pytest.approx(2.0)


def test_uptime_all_down():
    assert uptime_seconds([down(), down()]) == pytest.approx(0.0)


def test_uptime_mixed():
    assert uptime_seconds([healthy(), down(), healthy()]) == pytest.approx(2.0 / 3)


def test_uptime_empty():
    assert uptime_seconds([]) == pytest.approx(0.0)


# ── classify_availability ─────────────────────────────────────────────────────

def test_ratio_099_classifies_healthy():
    assert classify_availability(0.99) == ServiceStatus.HEALTHY


def test_ratio_100_classifies_healthy():
    assert classify_availability(1.0) == ServiceStatus.HEALTHY


def test_ratio_098_classifies_degraded():
    assert classify_availability(0.98) == ServiceStatus.DEGRADED


def test_ratio_090_classifies_degraded():
    assert classify_availability(0.90) == ServiceStatus.DEGRADED


def test_ratio_089_classifies_down():
    assert classify_availability(0.89) == ServiceStatus.DOWN


def test_ratio_zero_classifies_down():
    assert classify_availability(0.0) == ServiceStatus.DOWN
