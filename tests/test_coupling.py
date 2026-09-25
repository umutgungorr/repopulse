"""Unit tests for Temporal Coupling analysis."""

from repopulse.analyzers.coupling import analyze_coupling
from repopulse.models import CommitInfo, FileChange


def test_coupling_analysis():
    # File A and File B commit together 4 times out of 4
    commits = [
        CommitInfo("c1", "Dev", "dev@test.com", 1, "2026-01-01", "c1", [FileChange("models.py", 5, 0), FileChange("api.py", 10, 0)]),
        CommitInfo("c2", "Dev", "dev@test.com", 2, "2026-01-02", "c2", [FileChange("models.py", 2, 0), FileChange("api.py", 4, 0)]),
        CommitInfo("c3", "Dev", "dev@test.com", 3, "2026-01-03", "c3", [FileChange("models.py", 1, 0), FileChange("api.py", 1, 0)]),
        CommitInfo("c4", "Dev", "dev@test.com", 4, "2026-01-04", "c4", [FileChange("isolated.py", 10, 0)]),
    ]

    couplings = analyze_coupling(commits, min_co_changes=2, min_coupling_pct=50.0)
    assert len(couplings) == 1
    assert couplings[0].file_a == "api.py" or couplings[0].file_b == "api.py"
    assert couplings[0].co_changes == 3
    assert couplings[0].coupling_pct == 100.0
