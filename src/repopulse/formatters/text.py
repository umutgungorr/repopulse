"""Colorized terminal dashboard formatter for RepoPulse."""

import sys
from repopulse.models import RepoHealthReport


USE_COLOR = sys.stdout.isatty()


def _color(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def bold(text: str) -> str:
    return _color("1", text)


def red(text: str) -> str:
    return _color("31;1", text)


def yellow(text: str) -> str:
    return _color("33;1", text)


def green(text: str) -> str:
    return _color("32;1", text)


def cyan(text: str) -> str:
    return _color("36;1", text)


def gray(text: str) -> str:
    return _color("90", text)


def format_score(score: int) -> str:
    if score >= 80:
        return green(f"{score} / 100 (HEALTHY)")
    elif score >= 60:
        return yellow(f"{score} / 100 (MODERATE RISK)")
    else:
        return red(f"{score} / 100 (HIGH RISK)")


def format_text(report: RepoHealthReport) -> str:
    out = []
    out.append(bold(cyan("\n🩺 RepoPulse - Git Forensic Health & Knowledge Silo Audit")))
    out.append(gray("=" * 76))
    out.append(f"{bold('Target Repository:')} {report.repo_name}")
    out.append(f"{bold('Overall Health Score:')} {format_score(report.overall_health_score)}")
    out.append(
        f"{bold('Vitals:')} {report.total_commits} commits | {report.total_authors} author(s) | {report.active_days} active day(s)"
    )
    out.append(gray("-" * 76))

    # 1. Bus Factor Knowledge Concentration
    out.append(bold("\n🚨 Bus Factor & Knowledge Silo Alerts:"))
    at_risk = [b for b in report.bus_factor_risks if b.is_at_risk]
    if at_risk:
        out.append(gray(f"{'Concentration':<15} {'Revisions':<11} {'Top Author':<20} {'File Path'}"))
        out.append(gray("-" * 76))
        for b in at_risk[:8]:
            pct_str = red(f"{b.top_author_pct:.1f}% solo")
            out.append(f"{pct_str:<24} {b.total_revisions:<11} {b.top_author[:18]:<20} {cyan(b.path)}")
        if len(at_risk) > 8:
            out.append(gray(f"   ... and {len(at_risk) - 8} more at-risk files."))
    else:
        out.append(green("  ✅ Balanced ownership across scanned files. No acute bus-factor bottlenecks."))

    # 2. Architectural Hotspots (Churn + Size)
    out.append(bold("\n🔥 Architectural Hotspots (High Churn + Complexity):"))
    if report.hotspots:
        out.append(gray(f"{'Risk Level':<12} {'Churn':<8} {'Size (loc)':<12} {'File Path'}"))
        out.append(gray("-" * 76))
        for h in report.hotspots[:8]:
            if h.risk_level == "CRITICAL":
                lvl = red("[CRITICAL]")
            elif h.risk_level == "HIGH":
                lvl = red("[HIGH]")
            elif h.risk_level == "MEDIUM":
                lvl = yellow("[MEDIUM]")
            else:
                lvl = gray("[LOW]")
            out.append(f"{lvl:<21} {h.churn_count:<8} {h.estimated_size:<12} {cyan(h.path)}")
    else:
        out.append(gray("  No hotspots detected."))

    # 3. Temporal Coupling (Co-change pairs)
    out.append(bold("\n🔗 Temporal Coupling (Implicit Dependencies):"))
    if report.couplings:
        out.append(gray(f"{'Co-Changes':<12} {'Coupling %':<12} {'Connected File Pair'}"))
        out.append(gray("-" * 76))
        for c in report.couplings[:6]:
            c_pct = yellow(f"{c.coupling_pct:.1f}%")
            out.append(f"{c.co_changes:<12} {c_pct:<21} {c.file_a} <--> {c.file_b}")
    else:
        out.append(green("  ✅ No tight temporal coupling detected between disjoint files."))

    # 4. Top Contributors
    out.append(bold("\n👥 Top Contributor Breakdown:"))
    for author, count in list(report.author_contributions.items())[:5]:
        pct = (count / max(1, report.total_commits)) * 100
        out.append(f"  {gray('•')} {author:<24} {count} commits ({pct:.1f}%)")

    out.append(gray("\n" + "=" * 76 + "\n"))
    return "\n".join(out)
