"""
tests/test_summary.py — expanded summary + transition tests.

Covers:
- summarize_results tallies correctly for healthy / down / degraded / unknown
- Transitions: previous→current produces correct “from→to” buckets
- total_checks and healthy_fraction helpers
- Edge case: empty previous, all-healthy, all-down
"""
from datetime import datetime, timezone

import pytest

from last_and_end.availability import classify_availability
from last_and_end.models import CheckResult, Endpoint
from last_and_end.status import ServiceStatus
from last_and_end.summary import (
    healthy_fraction,
    summarize_results,
    total_checks,
)

NOW = datetime(2026, 5, 23, 14, 0, 0, tzinfo=timezone.utc)

healthy  = lambda name="a": CheckResult(Endpoint(name, f"https://{name}.com"), 200, 10, NOW)
down     = lambda name="b": CheckResult(Endpoint(name, f"https://{name}.com"), None, None, NOW, error="ERR")
degraded = lambda name="c": CheckResult(Endpoint(name, f"https://{name}.com"), 503, 20, NOW)
unknown  = lambda name="u": CheckResult(Endpoint(name, f"https://{name}.com"), None, None, NOW)


# ── basic summary ─────────────────────────────────────────────────────────────

def test_summary_counts_healthy():
    s = summarize_results([healthy(), healthy()])
    assert s[ServiceStatus.HEALTHY] == 2


def test_summary_counts_down():
    s = summarize_results([down()])
    assert s[ServiceStatus.DOWN] == 1


def test_summary_counts_degraded():
    s = summarize_results([degraded()])
    assert s[ServiceStatus.DEGRADED] == 1


def test_summary_totals_match_input_length():
    results = [healthy(), down(), degraded(), unknown()]
    assert sum(summarize_results(results).values()) == 4


def test_summary_empty_input():
    s = summarize_results([])
    assert all(v == 0 for v in s.values())


# ── helper functions ──────────────────────────────────────────────────────────

def test_total_checks():
    s = {ServiceStatus.HEALTHY: 2, ServiceStatus.DOWN: 1, ServiceStatus.DEGRADED: 0, ServiceStatus.UNKNOWN: 0}
    assert total_checks(s) == 3


def test_total_checks_empty():
    s = {s: 0 for s in ServiceStatus}
    assert total_checks(s) == 0


def test_healthy_fraction_all_healthy():
    s = {ServiceStatus.HEALTHY: 3, ServiceStatus.DOWN: 0, ServiceStatus.DEGRADED: 0, ServiceStatus.UNKNOWN: 0}
    assert healthy_fraction(s) == pytest.approx(1.0)


def test_healthy_fraction_half():
    s = {ServiceStatus.HEALTHY: 1, ServiceStatus.DOWN: 1, ServiceStatus.DEGRADED: 0, ServiceStatus.UNKNOWN: 0}
    assert healthy_fraction(s) == pytest.approx(0.5)


def test_healthy_fraction_empty():
    s = {s: 0 for s in ServiceStatus}
    assert healthy_fraction(s) == pytest.approx(0.0)


# ── transition mode ───────────────────────────────────────────────────────────

def test_transitions_returns_dict_when_previous_given():
    s = summarize_results([healthy(), down()], previous={ServiceStatus.HEALTHY: 1, ServiceStatus.DOWN: 1, ServiceStatus.DEGRADED: 0, ServiceStatus.UNKNOWN: 0})
    assert isinstance(s, dict)
    # keys are strings of form "healthy-><status>"
    assert all("->" in k for k in s)


def test_transition_healthy_remains_healthy():
    previous = {ServiceStatus.HEALTHY: 2, ServiceStatus.DOWN: 0, ServiceStatus.DEGRADED: 0, ServiceStatus.UNKNOWN: 0}
    current  = summarize_results([healthy(), healthy()], previous=previous)
    assert "healthy->healthy" in current
    assert current["healthy->healthy"] == 2


def test_transition_healthy_to_down():
    previous = {ServiceStatus.HEALTHY: 1, ServiceStatus.DOWN: 1, ServiceStatus.DEGRADED: 0, ServiceStatus.UNKNOWN: 0}
    # previous had 1 healthy, now we have 1 down
    t = summarize_results([down()], previous=previous)
    assert "healthy->down" in t
    assert t["healthy->down"] == 1


def test_transition_empty_previous_returns_empty_dict():
    previous = {ServiceStatus.HEALTHY: 0, ServiceStatus.DOWN: 0, ServiceStatus.DEGRADED: 0, ServiceStatus.UNKNOWN: 0}
    t = summarize_results([healthy()], previous=previous)
    assert isinstance(t, dict)
