from .availability import availability_ratio
from .models import CheckResult

def health_score(results: list[CheckResult]) -> int:
    return round(availability_ratio(results) * 100)
