from .models import CheckResult
from .status import ServiceStatus

def classify_result(result: CheckResult) -> ServiceStatus:
    if result.error:
        return ServiceStatus.DOWN
    if result.ok:
        return ServiceStatus.HEALTHY
    if result.status_code is None:
        return ServiceStatus.UNKNOWN
    if 500 <= result.status_code <= 599:
        return ServiceStatus.DOWN
    return ServiceStatus.DEGRADED
