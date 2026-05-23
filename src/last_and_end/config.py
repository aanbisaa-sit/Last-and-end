from dataclasses import dataclass, field

from .models import Endpoint


@dataclass(frozen=True)
class TrackerConfig:
endpoints: tuple[Endpoint, ...] = field(default_factory=tuple)
timeout_seconds: float = 5.0
retries: int = 0
