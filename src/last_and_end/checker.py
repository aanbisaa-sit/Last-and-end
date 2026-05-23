import time
import urllib.error
import urllib.request
from .models import CheckResult, Endpoint, utc_now

def check_endpoint(endpoint: Endpoint, timeout_seconds: float = 5.0) -> CheckResult:
    started = time.perf_counter()
    try:
        request = urllib.request.Request(endpoint.url, method="GET", headers={"User-Agent": "last-and-end/0.1"})
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return CheckResult(endpoint, response.status, int((time.perf_counter() - started) * 1000), utc_now())
    except urllib.error.HTTPError as exc:
        return CheckResult(endpoint, exc.code, int((time.perf_counter() - started) * 1000), utc_now())
    except Exception as exc:
        return CheckResult(endpoint, None, int((time.perf_counter() - started) * 1000), utc_now(), error=exc.__class__.__name__)
