"""Unit tests for Git miner and log parsing."""

from repopulse.git_miner import GitMiner, clean_renamed_path
from repopulse.models import CommitInfo, FileChange


def test_clean_renamed_path():
    assert clean_renamed_path("src/old.py => src/new.py") == "src/new.py"
    assert clean_renamed_path("lib/{foo => bar}/baz.py") == "lib/bar/baz.py"
    assert clean_renamed_path("normal/path/file.py") == "normal/path/file.py"


def test_parse_git_log_output():
    raw_log = """
---REPO_PULSE_COMMIT---\x1f1a2b3c4d\x1fAlice Dev\x1falice@test.com\x1f1700000000\x1f2026-01-01\x1fInitial commit
10\t2\tsrc/main.py
5\t0\tsrc/utils.py

---REPO_PULSE_COMMIT---\x1f5e6f7a8b\x1fBob Dev\x1fbob@test.com\x1f1700005000\x1f2026-01-02\x1fFix bug
1\t1\tsrc/main.py
"""
    commits = GitMiner.parse_git_log_output(raw_log)
    assert len(commits) == 2

    c1 = commits[0]
    assert c1.hash == "1a2b3c4d"
    assert c1.author_name == "Alice Dev"
    assert len(c1.files) == 2
    assert c1.files[0].path == "src/main.py"
    assert c1.files[0].added == 10
    assert c1.files[0].deleted == 2

    c2 = commits[1]
    assert c2.hash == "5e6f7a8b"
    assert c2.author_name == "Bob Dev"
    assert len(c2.files) == 1
    assert c2.files[0].path == "src/main.py"
