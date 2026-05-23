from collections.abc import Iterable
from .checker import check_endpoint
from .config import TrackerConfig
from .models import CheckResult, Endpoint

def run_checks(config: TrackerConfig) -> list[CheckResult]:
    return [check_endpoint(endpoint, timeout_seconds=config.timeout_seconds) for endpoint in config.endpoints]

def run_endpoint_list(endpoints: Iterable[Endpoint], timeout_seconds: float = 5.0) -> list[CheckResult]:
    return [check_endpoint(endpoint, timeout_seconds=timeout_seconds) for endpoint in endpoints]
