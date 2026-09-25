"""Unit tests for Hotspot analysis."""

from repopulse.analyzers.hotspots import analyze_hotspots
from repopulse.models import CommitInfo, FileChange


def test_hotspot_analysis():
    commits = []
    # 12 commits on volatile.py with 500 lines added
    for i in range(12):
        commits.append(
            CommitInfo(f"c{i}", "Dev", "dev@test.com", i, "2026-01-01", f"c{i}", [FileChange("volatile.py", 50, 5)])
        )
    # 2 commits on quiet.py
    commits.append(CommitInfo("cq1", "Dev", "dev@test.com", 20, "2026-01-01", "cq1", [FileChange("quiet.py", 10, 0)]))

    hotspots = analyze_hotspots(commits)
    assert len(hotspots) >= 2

    top = hotspots[0]
    assert top.path == "volatile.py"
    assert top.churn_count == 12
    assert top.risk_level in ("CRITICAL", "HIGH")
    assert top.hotspot_score > hotspots[1].hotspot_score
