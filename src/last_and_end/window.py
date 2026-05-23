from datetime import datetime, timedelta

from .models import CheckResult


def results_since(results: list[CheckResult], since: datetime) -> list[CheckResult]:
return [result for result in results if result.checked_at >= since]


def recent_results(results: list[CheckResult], minutes: int) -> list[CheckResult]:
if not results:
    return []
latest = max(result.checked_at for result in results)
return results_since(results, latest - timedelta(minutes=minutes))
