"""
config.py — immutable tracker configuration.

:class:`TrackerConfig` is the "root" data object for every run.  It is
produced by :func:`config_loader.load_config` and consumed by
:func:`runner.run_checks`.  Because it is a frozen dataclass it can be
safely shared across threads and cached without defensive copies.
"""
from dataclasses import dataclass, field
from .models import Endpoint


@dataclass(frozen=True, slots=True)
class TrackerConfig:
    """Complete runtime configuration for an uptime-check run.

    Attributes:
        endpoints: ordered tuple of :class:`Endpoint` definitions from the
            config file.  Order is preserved so that report sections match
            the config file layout.
        timeout_seconds: per-attempt socket timeout in seconds.  Must be >= 0.
        retries: number of additional attempts after the first failure.
            ``0`` means no retry.  Must be >= 0.
    """

    endpoints:        tuple[Endpoint, ...] = field(default_factory=tuple)
    timeout_seconds:  float = 5.0
    retries:          int   = 0
