import tomllib
from pathlib import Path

from .config import TrackerConfig
from .errors import ConfigurationError
from .models import Endpoint


def load_config(path: Path) -> TrackerConfig:
    """Parse a TOML uptime-tracker config file into an immutable TrackerConfig.

    Raises:
        ConfigurationError: if the file is missing or cannot be parsed.
        ValueError: if timeout_seconds is negative or retries is negative.
    """
    if not path.exists():
        raise ConfigurationError(f"Config file not found: {path}")

    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise ConfigurationError(f"Invalid TOML in {path}: {exc}") from exc

    raw_timeout  = data.get("timeout_seconds", 5.0)
    raw_retries  = data.get("retries", 0)

    if raw_timeout < 0:
        raise ValueError(f"timeout_seconds must be >= 0, got {raw_timeout!r}")
    if raw_retries < 0:
        raise ValueError(f"retries must be >= 0, got {raw_retries!r}")

    timeout_seconds = float(raw_timeout)  # type: ignore[arg-type]
    retries         = int(raw_retries)   # type: ignore[arg-type]

    endpoints = tuple(
        Endpoint(
            name=str(item.get("name", "unnamed")),
            url=str(item.get("url", "")),
            expected_status=int(item.get("expected_status", 200)),
        )
        for item in data.get("endpoints", [])
    )

    return TrackerConfig(
        endpoints=endpoints,
        timeout_seconds=timeout_seconds,
        retries=retries,
    )

