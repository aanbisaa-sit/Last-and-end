"""
Last and End — A lightweight uptime and downtime tracker.

This package provides zero-dependency health checking for personal sites,
small APIs, and lightweight services.
"""

__version__ = "0.1.0"
__author__ = "aanbisaa-sit"
__license__ = "MIT"

from last_and_end.checker import check_endpoint
from last_and_end.config_loader import load_config
from last_and_end.runner import run_checks
from last_and_end.status import ServiceStatus

__all__ = [
    "check_endpoint",
    "load_config",
    "run_checks",
    "ServiceStatus",
]
