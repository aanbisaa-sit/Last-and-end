from .incidents import detect_incident
from .models import CheckResult
from .policy import AlertPolicy

def should_alert(results: list[CheckResult], policy: AlertPolicy | None = None) -> bool:
    active_policy = policy or AlertPolicy()
    return detect_incident(results, minimum_failures=active_policy.minimum_failures) is not None
