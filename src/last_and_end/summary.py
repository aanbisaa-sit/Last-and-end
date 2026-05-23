from collections.abc import Iterable
from .classifier import classify_result
from .models import CheckResult
from .status import ServiceStatus

def summarize_results(results: Iterable[CheckResult]) -> dict[ServiceStatus, int]:
    summary = {status: 0 for status in ServiceStatus}
    for result in results:
        summary[classify_result(result)] += 1
    return summary
