"""High-level analysis orchestrator and health scoring for RepoPulse."""

from collections import Counter
from pathlib import Path
from typing import Optional
from repopulse.analyzers.bus_factor import analyze_bus_factor
from repopulse.analyzers.coupling import analyze_coupling
from repopulse.analyzers.hotspots import analyze_hotspots
from repopulse.git_miner import GitMiner
from repopulse.models import RepoHealthReport


class RepoPulseEngine:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.miner = GitMiner(str(self.repo_path))

    def analyze(self, max_commits: Optional[int] = None, since: Optional[str] = None) -> RepoHealthReport:
        """Executes full forensic analysis and generates a RepoHealthReport."""
        commits = self.miner.mine_commits(max_commits=max_commits, since=since)

        if not commits:
            return RepoHealthReport(
                repo_name=self.repo_path.name,
                total_commits=0,
                total_authors=0,
                active_days=0,
                bus_factor_risks=[],
                hotspots=[],
                couplings=[],
                author_contributions={},
                overall_health_score=100,
            )

        # Basic Stats
        authors_counter = Counter(c.author_name or c.author_email for c in commits)
        active_dates = {c.date_str for c in commits if c.date_str}

        # Detailed Analysis
        bus_risks = analyze_bus_factor(commits)
        hotspots = analyze_hotspots(commits)
        couplings = analyze_coupling(commits)

        # Health Scoring (100 is pristine)
        score = 100
        critical_bus_count = sum(1 for b in bus_risks if b.is_at_risk)
        critical_hotspot_count = sum(1 for h in hotspots if h.risk_level in ("CRITICAL", "HIGH"))
        tight_coupling_count = len(couplings)

        score -= min(35, critical_bus_count * 5)
        score -= min(35, critical_hotspot_count * 5)
        score -= min(20, tight_coupling_count * 3)

        # Single author deduction if repo has >10 commits but only 1 author
        if len(authors_counter) == 1 and len(commits) >= 10:
            score -= 10

        overall_score = max(10, min(100, score))

        return RepoHealthReport(
            repo_name=self.repo_path.name,
            total_commits=len(commits),
            total_authors=len(authors_counter),
            active_days=len(active_dates),
            bus_factor_risks=bus_risks,
            hotspots=hotspots,
            couplings=couplings,
            author_contributions=dict(authors_counter.most_common(10)),
            overall_health_score=overall_score,
        )
