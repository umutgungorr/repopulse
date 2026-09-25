"""Git log mining and commit stream extraction engine."""

from pathlib import Path
import re
import subprocess
from typing import Optional
from repopulse.models import CommitInfo, FileChange


COMMIT_DELIMITER = "---REPO_PULSE_COMMIT---"


def clean_renamed_path(path: str) -> str:
    """Normalizes git renamed paths like 'lib/{old => new}/file.py' or 'old.py => new.py'."""
    if "=>" not in path:
        return path

    # Case: dir/{old => new}/file.py
    brace_match = re.search(r"\{([^}]+)\}", path)
    if brace_match:
        inside = brace_match.group(1)
        if "=>" in inside:
            parts = inside.split("=>")
            new_sub = parts[1].strip()
            return path[: brace_match.start()] + new_sub + path[brace_match.end() :]

    # Case: old.py => new.py
    parts = path.split("=>")
    return parts[-1].strip()


class GitMiner:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self._verify_git_repo()

    def _verify_git_repo(self):
        if not self.repo_path.exists() or not self.repo_path.is_dir():
            raise ValueError(f"Target directory '{self.repo_path}' is not a valid Git repository.")
        try:
            res = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False,
            )
            if res.returncode != 0 or "true" not in res.stdout.strip().lower():
                raise ValueError(f"Target directory '{self.repo_path}' is not a valid Git repository.")
        except FileNotFoundError:
            raise RuntimeError("Git executable not found in system PATH.")

    def mine_commits(self, max_commits: Optional[int] = None, since: Optional[str] = None) -> list[CommitInfo]:
        """
        Extracts structured commit history using git log --numstat.
        Format delimiter ensures zero collision with commit messages.
        """
        cmd = [
            "git",
            "log",
            f"--pretty=format:{COMMIT_DELIMITER}%x1f%H%x1f%an%x1f%ae%x1f%at%x1f%ad%x1f%s",
            "--date=short",
            "--numstat",
            "--no-merges",
        ]
        if max_commits:
            cmd.extend(["-n", str(max_commits)])
        if since:
            cmd.extend(["--since", since])

        res = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if res.returncode != 0:
            raise RuntimeError(f"Git log failed: {res.stderr}")

        return self.parse_git_log_output(res.stdout)

    @staticmethod
    def parse_git_log_output(output: str) -> list[CommitInfo]:
        """Parses the raw text output from git log --numstat."""
        commits: list[CommitInfo] = []
        raw_blocks = output.split(COMMIT_DELIMITER)

        for block in raw_blocks:
            block = block.strip()
            if not block:
                continue

            lines = block.splitlines()
            meta_line = lines[0]
            fields = [f.strip() for f in meta_line.split("\x1f") if f.strip()]
            if len(fields) < 5:
                continue

            commit_hash = fields[0]
            author_name = fields[1]
            author_email = fields[2]
            timestamp = int(fields[3]) if fields[3].isdigit() else 0
            date_str = fields[4]
            message = fields[5] if len(fields) > 5 else ""

            file_changes: list[FileChange] = []
            for numstat_line in lines[1:]:
                numstat_line = numstat_line.strip()
                if not numstat_line:
                    continue

                parts = numstat_line.split("\t")
                if len(parts) >= 3:
                    added_str, deleted_str, raw_path = parts[0], parts[1], parts[2]
                    added = int(added_str) if added_str.isdigit() else 0
                    deleted = int(deleted_str) if deleted_str.isdigit() else 0
                    cleaned_path = clean_renamed_path(raw_path.strip())

                    # Skip non-code files like images/lockfiles if binary
                    if added_str == "-" and deleted_str == "-":
                        continue

                    file_changes.append(FileChange(path=cleaned_path, added=added, deleted=deleted))

            commits.append(
                CommitInfo(
                    hash=commit_hash,
                    author_name=author_name,
                    author_email=author_email,
                    timestamp=timestamp,
                    date_str=date_str,
                    message=message,
                    files=file_changes,
                )
            )

        return commits
