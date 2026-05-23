from collections.abc import Iterable

from .models import CheckResult


def availability_ratio(results: Iterable[CheckResult]) -> float:
items = list(results)
if not items:
    return 0.0
healthy = sum(1 for result in items if result.ok)
return healthy / len(items)
