"""Core data models for RepoPulse Git forensic analysis."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FileChange:
    path: str
    added: int
    deleted: int


@dataclass
class CommitInfo:
    hash: str
    author_name: str
    author_email: str
    timestamp: int
    date_str: str
    message: str
    files: list[FileChange] = field(default_factory=list)


@dataclass
class FileBusFactor:
    path: str
    total_revisions: int
    top_author: str
    top_author_pct: float
    author_count: int
    is_at_risk: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "total_revisions": self.total_revisions,
            "top_author": self.top_author,
            "top_author_pct": round(self.top_author_pct, 1),
            "author_count": self.author_count,
            "is_at_risk": self.is_at_risk,
        }


@dataclass
class Hotspot:
    path: str
    churn_count: int
    lines_added: int
    lines_deleted: int
    estimated_size: int
    hotspot_score: float
    risk_level: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "churn_count": self.churn_count,
            "lines_added": self.lines_added,
            "lines_deleted": self.lines_deleted,
            "estimated_size": self.estimated_size,
            "hotspot_score": round(self.hotspot_score, 2),
            "risk_level": self.risk_level,
        }


@dataclass
class TemporalCoupling:
    file_a: str
    file_b: str
    co_changes: int
    coupling_pct: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "file_a": self.file_a,
            "file_b": self.file_b,
            "co_changes": self.co_changes,
            "coupling_pct": round(self.coupling_pct, 1),
        }


@dataclass
class RepoHealthReport:
    repo_name: str
    total_commits: int
    total_authors: int
    active_days: int
    bus_factor_risks: list[FileBusFactor]
    hotspots: list[Hotspot]
    couplings: list[TemporalCoupling]
    author_contributions: dict[str, int]
    overall_health_score: int  # 0 to 100

    def to_dict(self) -> dict[str, Any]:
        return {
            "repo_name": self.repo_name,
            "total_commits": self.total_commits,
            "total_authors": self.total_authors,
            "active_days": self.active_days,
            "overall_health_score": self.overall_health_score,
            "author_contributions": self.author_contributions,
            "bus_factor_risks": [b.to_dict() for b in self.bus_factor_risks],
            "hotspots": [h.to_dict() for h in self.hotspots],
            "couplings": [c.to_dict() for c in self.couplings],
        }
