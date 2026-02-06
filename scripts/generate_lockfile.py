#!/usr/bin/env python3
"""Generate .build/skills-lock.json with hashes and metadata for all skills."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / ".build"
SKILLS_DIR = ROOT / "skills"
DOC_SKILLS_DIR = ROOT / "document-skills"
LOCK_FILE = BUILD_DIR / "skills-lock.json"


def _find_skill_dirs(base_dir: Path) -> list[Path]:
    """Return sorted list of directories containing a SKILL.md file."""
    return sorted(
        [p.parent for p in base_dir.rglob("SKILL.md") if p.parent != base_dir],
        key=lambda p: p.name,
    )


def _sha256(path: Path) -> str:
    """Return hex SHA-256 digest of a file's contents."""
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _git_head() -> str:
    """Return the current HEAD commit hash."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=True,
    )
    return result.stdout.strip()


def main() -> int:
    skill_dirs = _find_skill_dirs(SKILLS_DIR) + _find_skill_dirs(DOC_SKILLS_DIR)

    if not skill_dirs:
        print("ERROR: no skills found", file=sys.stderr)
        return 1

    git_commit = _git_head()

    skills = []
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        skills.append({
            "name": skill_dir.name,
            "path": str(skill_dir.relative_to(ROOT)),
            "sha256": _sha256(skill_file),
        })

    lockfile = {
        "version": "1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit,
        "skills": skills,
    }

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    LOCK_FILE.write_text(
        json.dumps(lockfile, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Generated {LOCK_FILE.relative_to(ROOT)} with {len(skills)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
