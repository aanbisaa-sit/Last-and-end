"""
tests/test_runner.py — tests for runner helpers

Covers:
- run_checks returns a list
- run_endpoint_list returns a list with per-endpoint CheckResult
- timeout_seconds is propagated to checker calls
- edge case: empty endpoint list returns empty list
"""
from datetime import datetime, timezone

import pytest

from last_and_end.checker import check_endpoint
from last_and_end.config import TrackerConfig
from last_and_end.models import Endpoint, CheckResult
from last_and_end.runner import (  # imported to make type: ignore
    run_checks,
    run_endpoint_list,
)


EP_URL = "http://localhost:0/does-not-exist"


@pytest.fixture()
def endpoints() -> list[Endpoint]:
    return [Endpoint("ep-a", EP_URL), Endpoint("ep-b", EP_URL)]


@pytest.fixture()
def config(endpoints: list[Endpoint]) -> TrackerConfig:
    return TrackerConfig(endpoints=tuple(endpoints), timeout_seconds=2.0)


# ── run_checks ───────────────────────────────────────────────────────────────

def test_run_checks_returns_list(endpoints: list[Endpoint], config: TrackerConfig):
    result = run_checks(config)
    assert isinstance(result, list)
    assert len(result) == 2


def test_run_checks_each_result_is_check_result(
    endpoints: list[Endpoint], config: TrackerConfig
):
    result = run_checks(config)
    assert all(isinstance(r, CheckResult) for r in result)


def test_run_checks_result_count_matches_endpoints(
    endpoints: list[Endpoint], config: TrackerConfig
):
    assert len(run_checks(config)) == len(endpoints)


def test_run_checks_timeout_passed_to_checker(
    monkeypatch: pytest.MonkeyPatch,
    endpoints: list[Endpoint],
    config: TrackerConfig,
):
    seen: list[float] = []

    def fake_check(ep: Endpoint, timeout_seconds: float = 5.0) -> CheckResult:
        seen.append(timeout_seconds)
        now = datetime.now(timezone.utc)
        return CheckResult(ep, None, None, now, error="TimedOut")

    monkeypatch.setattr("last_and_end.runner.check_endpoint", fake_check)
    run_checks(config)
    assert all(t == 2.0 for t in seen), f"Expected 2.0 for all, got {seen}"


def test_run_checks_empty_endpoints_returns_empty_list():
    result = run_checks(TrackerConfig())
    assert result == []


# ── run_endpoint_list ─────────────────────────────────────────────────────────

def test_run_endpoint_list_returns_list(endpoints: list[Endpoint]):
    result = run_endpoint_list(endpoints)
    assert isinstance(result, list)


def test_run_endpoint_list_count_matches_input(endpoints: list[Endpoint]):
    assert len(run_endpoint_list(endpoints)) == len(endpoints)


def test_run_endpoint_list_default_timeout(monkeypatch: pytest.MonkeyPatch):
    seen: list[float] = []

    def fake_check(ep: Endpoint, timeout_seconds: float = 5.0) -> CheckResult:
        seen.append(timeout_seconds)
        now = datetime.now(timezone.utc)
        return CheckResult(ep, None, None, now)

    monkeypatch.setattr("last_and_end.runner.check_endpoint", fake_check)
    run_endpoint_list([Endpoint("x", EP_URL)])
    assert seen == [5.0]


def test_run_endpoint_list_custom_timeout(monkeypatch: pytest.MonkeyPatch):
    seen: list[float] = []

    def fake_check(ep: Endpoint, timeout_seconds: float = 5.0) -> CheckResult:
        seen.append(timeout_seconds)
        now = datetime.now(timezone.utc)
        return CheckResult(ep, None, None, now)

    monkeypatch.setattr("last_and_end.runner.check_endpoint", fake_check)
    run_endpoint_list([Endpoint("x", EP_URL)], timeout_seconds=12.0)
    assert seen == [12.0]
