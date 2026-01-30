#!/usr/bin/env python3
"""Release helper: update versions, changelog, and run refresh/validation."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VERSION_FILES = [
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / "extensions" / "gemini" / "example-skills" / "gemini-extension.json",
    ROOT / "extensions" / "gemini" / "document-skills" / "gemini-extension.json",
]


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def _update_versions(version: str) -> None:
    marketplace = VERSION_FILES[0]
    data = json.loads(marketplace.read_text(encoding="utf-8"))
    data.setdefault("metadata", {})["version"] = version
    marketplace.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    for path in VERSION_FILES[1:]:
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["version"] = version
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _render_section(title: str, bullets: list[str]) -> str:
    if not bullets:
        return ""
    lines = [f"### {title}"]
    lines.extend([f"- {item}" for item in bullets])
    return "\n".join(lines)


def _update_changelog(version: str, date_str: str, added: list[str], changed: list[str], fixed: list[str]) -> None:
    changelog = ROOT / "CHANGELOG.md"
    content = changelog.read_text(encoding="utf-8")

    entry_lines = [f"## [{version}] - {date_str}"]
    sections = [
        _render_section("Added", added),
        _render_section("Changed", changed),
        _render_section("Fixed", fixed),
    ]
    sections = [s for s in sections if s]
    if not sections:
        raise ValueError("Provide at least one --add/--change/--fix entry for the changelog.")
    entry_lines.extend(sections)
    entry = "\n".join(entry_lines) + "\n\n"

    marker = "\n## ["
    idx = content.find(marker)
    if idx == -1:
        content = content.rstrip() + "\n\n" + entry
    else:
        insert_at = idx + 1
        content = content[:insert_at] + entry + content[insert_at:]

    changelog.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a release by bumping versions and updating CHANGELOG.md.")
    parser.add_argument("version", help="Release version (e.g., 1.2.0)")
    parser.add_argument("--date", help="Release date (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--add", action="append", default=[], help="Changelog entry under Added.")
    parser.add_argument("--change", action="append", default=[], help="Changelog entry under Changed.")
    parser.add_argument("--fix", action="append", default=[], help="Changelog entry under Fixed.")
    parser.add_argument("--skip-refresh", action="store_true", help="Skip refresh_skill_collections.py")
    parser.add_argument("--skip-validate", action="store_true", help="Skip validate_skills.py")
    args = parser.parse_args()

    date_str = args.date or dt.date.today().isoformat()

    _update_versions(args.version)
    _update_changelog(args.version, date_str, args.add, args.change, args.fix)

    if not args.skip_refresh:
        _run(["python3", "scripts/refresh_skill_collections.py"])
    if not args.skip_validate:
        _run(["python3", "scripts/validate_skills.py", "--collection", "example", "--unique"])
        _run(["python3", "scripts/validate_skills.py", "--collection", "document", "--unique"])

    print(f"Updated versions and CHANGELOG for {args.version} ({date_str}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
