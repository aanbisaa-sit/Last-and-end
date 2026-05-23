"""
runner.py — orchestrates endpoint health checks.

Provides two public helpers:
- ``run_checks``: consumes an immutable :class:`TrackerConfig` and returns
  a plain ``list[CheckResult]`` (no deduplication, no side-effects).
- ``run_endpoint_list``: runs against a bare iterable of ``Endpoint`` objects
  with an explicit per-call timeout, useful for ad-hoc probes or tests.

The runner is deliberately kept stateless so it is trivially testable and
safe to call with different config objects in the same process lifetime.
"""
from collections.abc import Iterable

from .checker import check_endpoint
from .config import TrackerConfig
from .models import CheckResult, Endpoint


def run_checks(config: TrackerConfig) -> list[CheckResult]:
    """Return one :class:`CheckResult` per endpoint in *config*.

    The order of results always matches the order defined in the config so
    that callers can zip results with the original endpoint list.

    Args:
        config: an immutable :class:`TrackerConfig` produced by
            :func:`config_loader.load_config`.

    Returns:
        A :class:`list` with exactly ``len(config.endpoints)`` entries.
    """
    return [
        check_endpoint(
            endpoint,
            timeout_seconds=config.timeout_seconds,
            retries=config.retries,
        )
        for endpoint in config.endpoints
    ]


def run_endpoint_list(
    endpoints: Iterable[Endpoint],
    timeout_seconds: float = 5.0,
) -> list[CheckResult]:
    """Probe an arbitrary iterable of endpoints without a full :class:`TrackerConfig`.

    Convenient for ad-hoc probes and integration tests where building
    a complete config object feels boilerplate-heavy.

    Args:
        endpoints: any iterable of :class:`Endpoint` objects.
        timeout_seconds: per-attempt socket timeout in seconds (default 5).

    Returns:
        A :class:`list` of :class:`CheckResult` in the same order as *endpoints*.
    """
    return [
        check_endpoint(endpoint, timeout_seconds=timeout_seconds)
        for endpoint in endpoints
    ]
