"""Integration tests for RepoPulse CLI using a local temporary git repository."""

import json
from pathlib import Path
import subprocess
from repopulse.cli import main


def create_mock_git_repo(repo_dir: Path):
    """Initializes a git repository with mock commits for testing."""
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Alice Test"], cwd=repo_dir, check=True)
    subprocess.run(["git", "config", "user.email", "alice@test.com"], cwd=repo_dir, check=True)

    # Commit 1
    (repo_dir / "app.py").write_text("print('hello')\n")
    (repo_dir / "utils.py").write_text("def helper(): pass\n")
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_dir, check=True)

    # Commit 2
    (repo_dir / "app.py").write_text("print('hello world')\n")
    subprocess.run(["git", "commit", "-am", "Update app"], cwd=repo_dir, check=True)


def test_cli_audit_text(tmp_path: Path):
    create_mock_git_repo(tmp_path)

    code = main(["audit", str(tmp_path)])
    assert code == 0


def test_cli_audit_json(tmp_path: Path):
    create_mock_git_repo(tmp_path)
    out_json = tmp_path / "report.json"

    code = main(["audit", str(tmp_path), "-f", "json", "-o", str(out_json)])
    assert code == 0
    assert out_json.exists()

    data = json.loads(out_json.read_text())
    assert data["total_commits"] == 2
    assert data["total_authors"] == 1
    assert data["overall_health_score"] > 0


def test_cli_audit_markdown(tmp_path: Path):
    create_mock_git_repo(tmp_path)
    out_md = tmp_path / "report.md"

    code = main(["audit", str(tmp_path), "-f", "markdown", "-o", str(out_md)])
    assert code == 0
    assert out_md.exists()
    assert "# 🩺 RepoPulse Forensic Audit" in out_md.read_text(encoding="utf-8")


def test_cli_audit_fail_under(tmp_path: Path):
    create_mock_git_repo(tmp_path)

    # A health score is at most 100. If we require 101, it must fail with exit code 1
    code = main(["audit", str(tmp_path), "--fail-under", "101"])
    assert code == 1


def test_cli_invalid_path():
    code = main(["audit", "non_existent_path_xyz_123"])
    assert code == 2
