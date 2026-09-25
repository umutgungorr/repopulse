"""Bus factor and knowledge concentration analyzer."""

from collections import Counter, defaultdict
from repopulse.models import CommitInfo, FileBusFactor


def analyze_bus_factor(commits: list[CommitInfo], min_revisions: int = 2) -> list[FileBusFactor]:
    """
    Analyzes knowledge concentration per file based on commit authors.
    Files with >=75% contribution from a single author are flagged as high bus-factor risk.
    """
    file_authors: dict[str, Counter] = defaultdict(Counter)
    file_revisions: Counter = Counter()

    for c in commits:
        author = c.author_name or c.author_email or "Unknown"
        for f in c.files:
            file_authors[f.path][author] += 1
            file_revisions[f.path] += 1

    results: list[FileBusFactor] = []
    for path, authors in file_authors.items():
        total_revs = file_revisions[path]
        if total_revs < min_revisions:
            continue

        top_author, top_count = authors.most_common(1)[0]
        pct = (top_count / total_revs) * 100.0
        is_risk = pct >= 75.0 and total_revs >= 3

        results.append(
            FileBusFactor(
                path=path,
                total_revisions=total_revs,
                top_author=top_author,
                top_author_pct=pct,
                author_count=len(authors),
                is_at_risk=is_risk,
            )
        )

    # Sort by risk status (at risk first), then by total revisions descending
    results.sort(key=lambda x: (not x.is_at_risk, -x.total_revisions))
    return results
