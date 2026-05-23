import time
import urllib.error
import urllib.request

from .models import CheckResult, Endpoint, utc_now


def check_endpoint(endpoint: Endpoint, timeout_seconds: float = 5.0) -> CheckResult:
started = time.perf_counter()
try:
    request = urllib.request.Request(endpoint.url, method="GET", headers={"User-Agent": "last-and-end/0.1"})
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        latency_ms = int((time.perf_counter() - started) * 1000)
        return CheckResult(endpoint, response.status, latency_ms, utc_now())
except urllib.error.HTTPError as exc:
    latency_ms = int((time.perf_counter() - started) * 1000)
    return CheckResult(endpoint, exc.code, latency_ms, utc_now(), error=None)
except Exception as exc:
    latency_ms = int((time.perf_counter() - started) * 1000)
    return CheckResult(endpoint, None, latency_ms, utc_now(), error=exc.__class__.__name__)
