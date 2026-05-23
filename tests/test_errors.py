"""
tests/test_errors.py — contract tests for the exception hierarchy.

Every public exception class must:
  - be a subclass of TrackerError
  - carry the expected attributes
  - produce a readable str() representation
"""
import pytest

from last_and_end.errors import (
    CheckError,
    ConfigurationError,
    RetryExhaustedError,
    TimeoutError,
    TrackerError,
)


# ── hierarchy ─────────────────────────────────────────────────────────────────

def test_tracker_error_is_exception():
    assert issubclass(TrackerError, Exception)


def test_all_errors_inherit_from_tracker_error():
    for cls in (ConfigurationError, CheckError, TimeoutError, RetryExhaustedError):
        assert issubclass(cls, TrackerError)


def test_timeout_error_is_check_error():
    assert issubclass(TimeoutError, CheckError)


# ── RetryExhaustedError ────────────────────────────────────────────────────────

def test_retry_exhausted_default_message():
    err = RetryExhaustedError(attempts=3)
    assert "3 attempt(s)" in str(err)


def test_retry_exhausted_with_last_error():
    err = RetryExhaustedError(attempts=4, last_error="ConnectionRefused")
    assert "ConnectionRefused" in str(err)


def test_retry_exhausted_stores_attempts():
    err = RetryExhaustedError(attempts=7)
    assert err.attempts == 7


def test_retry_exhausted_stores_last_error():
    err = RetryExhaustedError(attempts=2, last_error="Timeout")
    assert err.last_error == "Timeout"


def test_retry_exhausted_can_be_raised_and_caught():
    with pytest.raises(RetryExhaustedError):
        raise RetryExhaustedError(attempts=3, last_error="fail")


def test_retry_exhausted_caught_as_tracker_error():
    with pytest.raises(TrackerError):
        raise RetryExhaustedError(attempts=1)


# ── TimeoutError ──────────────────────────────────────────────────────────────

def test_timeout_error_has_message():
    err = TimeoutError("handshake took too long")
    assert "handshake took too long" in str(err)


def test_timeout_error_can_be_raised_and_caught():
    with pytest.raises(TimeoutError):
        raise TimeoutError("deadline hit")


def test_timeout_error_caught_as_check_error():
    with pytest.raises(CheckError):
        raise TimeoutError("timed out")


def test_timeout_error_caught_as_tracker_error():
    with pytest.raises(TrackerError):
        raise TimeoutError("timed out")


# ── ConfigurationError ─────────────────────────────────────────────────────────

def test_configuration_error_can_be_raised():
    with pytest.raises(ConfigurationError):
        raise ConfigurationError("file not found")


def test_configuration_error_message():
    err = ConfigurationError("missing config.toml")
    assert "missing config.toml" in str(err)
