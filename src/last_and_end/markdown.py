from .models import CheckResult
from .report import build_report


def build_markdown_report(results: list[CheckResult]) -> str:
    report = build_report(results)
    return "# Status Report

```text
" + report + "
```"
