from .health_score import health_score
from .models import CheckResult

def score_delta(previous: list[CheckResult], current: list[CheckResult]) -> int:
    return health_score(current) - health_score(previous)
