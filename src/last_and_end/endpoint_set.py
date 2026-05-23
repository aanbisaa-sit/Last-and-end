from .models import Endpoint


def dedupe_endpoints(endpoints: list[Endpoint]) -> list[Endpoint]:
seen: set[str] = set()
output: list[Endpoint] = []
for endpoint in endpoints:
    key = endpoint.url
    if key in seen:
        continue
    seen.add(key)
    output.append(endpoint)
return output
