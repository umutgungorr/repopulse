"""Command Line Interface for RepoPulse."""

import argparse
from pathlib import Path
import sys
from typing import Optional

# UTF-8 safety on Windows terminals
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from repopulse import __version__
from repopulse.engine import RepoPulseEngine
from repopulse.formatters import format_json, format_markdown, format_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repopulse",
        description="Zero-dependency Git forensic health, hotspot churn, and bus-factor risk engine.",
    )
    parser.add_argument("-v", "--version", action="version", version=f"RepoPulse v{__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # audit command
    audit_parser = subparsers.add_parser("audit", help="Run forensic health audit on a Git repository")
    audit_parser.add_argument("path", nargs="?", default=".", help="Path to Git repository (default: current directory)")
    audit_parser.add_argument(
        "-f",
        "--format",
        choices=["text", "json", "markdown"],
        default="text",
        help="Report format (default: text)",
    )
    audit_parser.add_argument(
        "-o",
        "--output",
        help="Optional file path to write the report to",
    )
    audit_parser.add_argument(
        "-n",
        "--max-commits",
        type=int,
        help="Limit analysis to last N commits",
    )
    audit_parser.add_argument(
        "--since",
        help="Analyze commits since date (e.g. '1.year.ago', '2026-01-01')",
    )
    audit_parser.add_argument(
        "--fail-under",
        type=int,
        help="Exit with code 1 if health score is strictly below this threshold (for CI gates)",
    )

    return parser


def main(args: Optional[list[str]] = None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(args)

    if not parsed.command:
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
            parsed = parser.parse_args(["audit"] + sys.argv[1:])
        else:
            parser.print_help()
            return 0

    if parsed.command == "audit":
        try:
            engine = RepoPulseEngine(parsed.path)
            report = engine.analyze(max_commits=parsed.max_commits, since=parsed.since)
        except (ValueError, RuntimeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2

        if parsed.format == "json":
            content = format_json(report)
        elif parsed.format == "markdown":
            content = format_markdown(report)
        else:
            content = format_text(report)

        if parsed.output:
            out_file = Path(parsed.output)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(content, encoding="utf-8")
            print(f"Report written to '{parsed.output}'.")
        else:
            print(content)

        if parsed.fail_under is not None and report.overall_health_score < parsed.fail_under:
            print(
                f"\nCI Gate Failed: Health score {report.overall_health_score} is below threshold {parsed.fail_under}.",
                file=sys.stderr,
            )
            return 1

        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
