"""Markdown report formatter for RepoPulse."""

from repopulse.models import RepoHealthReport


def format_markdown(report: RepoHealthReport) -> str:
    lines = [
        f"# 🩺 RepoPulse Forensic Audit: {report.repo_name}",
        "",
        f"**Health Score:** `{report.overall_health_score} / 100` | **Total Commits:** `{report.total_commits}` | **Contributors:** `{report.total_authors}`",
        "",
        "---",
        "",
        "## 🚨 Bus Factor Knowledge Concentration",
        "",
    ]

    at_risk = [b for b in report.bus_factor_risks if b.is_at_risk]
    if at_risk:
        lines.extend([
            "| File Path | Revisions | Top Contributor | Concentration % |",
            "|:---|:---:|:---|:---:|",
        ])
        for b in at_risk[:10]:
            lines.append(f"| `{b.path}` | {b.total_revisions} | {b.top_author} | **{b.top_author_pct:.1f}%** |")
    else:
        lines.append("✅ No acute bus-factor bottlenecks identified.")

    lines.extend([
        "",
        "## 🔥 Architectural Hotspots",
        "",
        "| File Path | Churn (Revs) | Net Lines | Risk Level |",
        "|:---|:---:|:---:|:---:|",
    ])
    for h in report.hotspots[:10]:
        lines.append(f"| `{h.path}` | {h.churn_count} | {h.estimated_size} | **{h.risk_level}** |")

    lines.extend([
        "",
        "## 🔗 Temporal Coupling",
        "",
    ])
    if report.couplings:
        lines.extend([
            "| File Pair | Co-Changes | Coupling Degree |",
            "|:---|:---:|:---:|",
        ])
        for c in report.couplings[:10]:
            lines.append(f"| `{c.file_a}` ⟷ `{c.file_b}` | {c.co_changes} | **{c.coupling_pct:.1f}%** |")
    else:
        lines.append("✅ No tight implicit coupling detected between files.")

    lines.append("")
    return "\n".join(lines)
