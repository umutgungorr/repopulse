"""JSON formatter for RepoPulse."""

import json
from repopulse.models import RepoHealthReport


def format_json(report: RepoHealthReport) -> str:
    return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
