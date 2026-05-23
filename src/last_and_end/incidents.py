from dataclasses import dataclass
from .models import CheckResult

@dataclass(frozen=True)
class Incident:
    endpoint_name: str
    reason: str
    result_count: int

def detect_incident(results: list[CheckResult], minimum_failures: int = 2) -> Incident | None:
    failures = [result for result in results if not result.ok]
    if len(failures) < minimum_failures:
        return None
    first = failures[0]
    return Incident(first.endpoint.name, first.error or f"status {first.status_code}", len(failures))
