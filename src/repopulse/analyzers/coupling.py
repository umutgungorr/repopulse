"""Temporal co-change coupling analyzer."""

from collections import Counter
from itertools import combinations
from repopulse.models import CommitInfo, TemporalCoupling


def analyze_coupling(
    commits: list[CommitInfo], min_co_changes: int = 2, min_coupling_pct: float = 50.0, top_n: int = 15
) -> list[TemporalCoupling]:
    """
    Detects implicit architectural coupling by identifying file pairs
    that frequently commit together across multiple commits.
    """
    file_revisions: Counter = Counter()
    pair_co_changes: Counter = Counter()

    for c in commits:
        unique_paths = sorted(list({f.path for f in c.files}))
        for path in unique_paths:
            file_revisions[path] += 1

        # Calculate co-changes for all pairs in this commit (skip huge bulk commits > 25 files)
        if 2 <= len(unique_paths) <= 25:
            for pair in combinations(unique_paths, 2):
                pair_co_changes[pair] += 1

    couplings: list[TemporalCoupling] = []
    for (file_a, file_b), co_count in pair_co_changes.items():
        if co_count < min_co_changes:
            continue

        rev_a = file_revisions[file_a]
        rev_b = file_revisions[file_b]
        min_rev = min(rev_a, rev_b)

        pct = (co_count / min_rev) * 100.0
        if pct >= min_coupling_pct:
            couplings.append(
                TemporalCoupling(
                    file_a=file_a,
                    file_b=file_b,
                    co_changes=co_count,
                    coupling_pct=pct,
                )
            )

    couplings.sort(key=lambda x: (-x.co_changes, -x.coupling_pct))
    return couplings[:top_n]
