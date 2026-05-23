from enum import StrEnum


class ServiceStatus(StrEnum):
HEALTHY = "healthy"
DEGRADED = "degraded"
DOWN = "down"
UNKNOWN = "unknown"
