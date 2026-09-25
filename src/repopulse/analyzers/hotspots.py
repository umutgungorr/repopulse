"""Code churn and hotspot risk analyzer."""

from collections import Counter, defaultdict
import math
from repopulse.models import CommitInfo, Hotspot


def analyze_hotspots(commits: list[CommitInfo], top_n: int = 15) -> list[Hotspot]:
    """
    Identifies high-risk architectural hotspots by combining
    change frequency (churn) and code volume.
    """
    file_churn: Counter = Counter()
    file_added: Counter = Counter()
    file_deleted: Counter = Counter()

    for c in commits:
        for f in c.files:
            file_churn[f.path] += 1
            file_added[f.path] += f.added
            file_deleted[f.path] += f.deleted

    hotspots: list[Hotspot] = []
    for path, churn in file_churn.items():
        added = file_added[path]
        deleted = file_deleted[path]
        net_size = max(5, added - deleted)

        # Hotspot score: log(churn + 1) * sqrt(size)
        score = math.log1p(churn) * math.sqrt(net_size)

        # Risk classification
        if churn >= 10 and score >= 25.0:
            risk = "CRITICAL"
        elif churn >= 6 or score >= 15.0:
            risk = "HIGH"
        elif churn >= 3 or score >= 8.0:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        hotspots.append(
            Hotspot(
                path=path,
                churn_count=churn,
                lines_added=added,
                lines_deleted=deleted,
                estimated_size=net_size,
                hotspot_score=score,
                risk_level=risk,
            )
        )

    hotspots.sort(key=lambda x: -x.hotspot_score)
    return hotspots[:top_n]
