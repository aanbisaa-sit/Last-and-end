from collections import deque
from collections.abc import Iterable

from .models import CheckResult


class ResultHistory:
def __init__(self, max_items: int = 100) -> None:
    self._items: deque[CheckResult] = deque(maxlen=max_items)

def add(self, result: CheckResult) -> None:
    self._items.append(result)

def all(self) -> tuple[CheckResult, ...]:
    return tuple(self._items)

def extend(self, results: Iterable[CheckResult]) -> None:
    for result in results:
        self.add(result)
