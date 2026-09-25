"""Unit tests for Bus Factor analysis."""

from repopulse.analyzers.bus_factor import analyze_bus_factor
from repopulse.models import CommitInfo, FileChange


def test_bus_factor_detection():
    # 4 commits by Alice on auth.py, 1 by Bob
    # 2 commits by Alice on shared.py, 2 by Bob
    commits = [
        CommitInfo("c1", "Alice", "alice@test.com", 1, "2026-01-01", "c1", [FileChange("auth.py", 10, 0)]),
        CommitInfo("c2", "Alice", "alice@test.com", 2, "2026-01-02", "c2", [FileChange("auth.py", 5, 1)]),
        CommitInfo("c3", "Alice", "alice@test.com", 3, "2026-01-03", "c3", [FileChange("auth.py", 3, 0)]),
        CommitInfo("c4", "Alice", "alice@test.com", 4, "2026-01-04", "c4", [FileChange("auth.py", 2, 0), FileChange("shared.py", 5, 0)]),
        CommitInfo("c5", "Bob", "bob@test.com", 5, "2026-01-05", "c5", [FileChange("auth.py", 1, 0), FileChange("shared.py", 5, 0)]),
    ]

    results = analyze_bus_factor(commits)
    auth_res = next(r for r in results if r.path == "auth.py")

    assert auth_res.total_revisions == 5
    assert auth_res.top_author == "Alice"
    assert auth_res.top_author_pct == 80.0  # 4/5 = 80%
    assert auth_res.is_at_risk is True

    shared_res = next(r for r in results if r.path == "shared.py")
    assert shared_res.top_author_pct == 50.0
    assert shared_res.is_at_risk is False
