from .availability import availability_ratio
from .models import CheckResult
from .render import render_summary
from .summary import summarize_results

def build_report(results: list[CheckResult]) -> str:
    summary = render_summary(summarize_results(results))
    availability = availability_ratio(results) * 100
    return f"{summary}\nAvailability: {availability:.2f}%"
