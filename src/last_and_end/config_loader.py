import tomllib
from pathlib import Path

from .config import TrackerConfig
from .errors import ConfigurationError
from .models import Endpoint


def load_config(path: Path) -> TrackerConfig:
if not path.exists():
    raise ConfigurationError(f"Config file not found: {path}")
data = tomllib.loads(path.read_text(encoding="utf-8"))
endpoints = tuple(
    Endpoint(
        name=str(item["name"]),
        url=str(item["url"]),
        expected_status=int(item.get("expected_status", 200)),
    )
    for item in data.get("endpoints", [])
)
return TrackerConfig(
    endpoints=endpoints,
    timeout_seconds=float(data.get("timeout_seconds", 5)),
    retries=int(data.get("retries", 0)),
)
