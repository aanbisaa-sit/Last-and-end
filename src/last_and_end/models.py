from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class Endpoint:
    name: str
    url: str
    expected_status: int = 200


@dataclass(frozen=True)
class CheckResult:
    endpoint: Endpoint
    status_code: int | None
    latency_ms: int | None
    checked_at: datetime
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and self.status_code == self.endpoint.expected_status


def utc_now() -> datetime:
return datetime.now(timezone.utc)
