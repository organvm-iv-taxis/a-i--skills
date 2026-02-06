#!/usr/bin/env python3
"""Generate a machine-readable skills registry JSON from SKILL.md frontmatter."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
DOC_SKILLS_DIR = ROOT / "document-skills"
BUILD_DIR = ROOT / ".build"
OUTPUT_PATH = BUILD_DIR / "skills-registry.json"

NAME_RE = re.compile(r"^[a-z0-9-]+$")

# Fields that are stored as lists in the registry
LIST_FIELDS = (
    "prerequisites", "tags", "inputs", "outputs", "side_effects",
    "triggers", "complements", "includes",
)


def _find_skill_dirs(base_dir: Path) -> list[Path]:
    return sorted(
        [p.parent for p in base_dir.rglob("SKILL.md") if p.parent != base_dir],
        key=lambda p: p.name,
    )


def _extract_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}

    data: dict[str, str] = {}
    current_key = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith(" ") or raw.startswith("\t"):
            if current_key:
                data[current_key] = f"{data[current_key]}\n{raw.lstrip()}"
            continue
        key, sep, value = raw.partition(":")
        if not sep:
            continue
        current_key = key.strip()
        data[current_key] = value.strip()
    return data


def _parse_list_field(value: str) -> list[str]:
    """Parse an inline or multiline YAML list from frontmatter."""
    if not value:
        return []
    stripped = value.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        inner = stripped[1:-1]
        return [item.strip() for item in inner.split(",") if item.strip()]
    items: list[str] = []
    for line in stripped.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
        elif line:
            items.append(line)
    return items


def _category_from_path(skill_dir: Path, base_dir: Path) -> str:
    """Derive category from directory structure (e.g., skills/development/x -> development)."""
    try:
        rel = skill_dir.relative_to(base_dir)
        parts = rel.parts
        if len(parts) >= 2:
            return parts[0]
    except ValueError:
        pass
    return "uncategorized"


def _build_skill_entry(skill_dir: Path, base_dir: Path, collection: str) -> dict | None:
    skill_file = skill_dir / "SKILL.md"
    try:
        text = skill_file.read_text(encoding="utf-8")
    except OSError:
        return None

    fm = _extract_frontmatter(text)
    name = fm.get("name")
    if not name or name != skill_dir.name:
        return None

    entry: dict = {
        "name": name,
        "description": fm.get("description", ""),
        "category": _category_from_path(skill_dir, base_dir),
        "collection": collection,
        "path": str(skill_dir.relative_to(ROOT)),
        "license": fm.get("license"),
        "complexity": fm.get("complexity"),
        "time_to_learn": fm.get("time_to_learn"),
        "tier": fm.get("tier"),
    }

    # Parse list fields
    for field in LIST_FIELDS:
        raw = fm.get(field)
        entry[field] = _parse_list_field(raw) if raw else []

    # Resource directories
    entry["resources"] = {
        "scripts": sorted(p.name for p in (skill_dir / "scripts").iterdir()) if (skill_dir / "scripts").is_dir() else [],
        "references": sorted(p.name for p in (skill_dir / "references").iterdir()) if (skill_dir / "references").is_dir() else [],
        "assets": sorted(p.name for p in (skill_dir / "assets").iterdir()) if (skill_dir / "assets").is_dir() else [],
    }

    return entry


def _build_categories(skills: list[dict]) -> dict:
    categories: dict[str, dict] = {}
    for skill in skills:
        cat = skill["category"]
        if cat not in categories:
            categories[cat] = {"count": 0, "skills": []}
        categories[cat]["count"] += 1
        categories[cat]["skills"].append(skill["name"])
    return categories


def _build_bundles(skills: list[dict]) -> list[dict]:
    bundles = []
    for skill in skills:
        if skill.get("includes"):
            bundles.append({
                "name": skill["name"],
                "includes": skill["includes"],
            })
    return bundles


def main() -> int:
    example_dirs = _find_skill_dirs(SKILLS_DIR)
    document_dirs = _find_skill_dirs(DOC_SKILLS_DIR)

    skills: list[dict] = []
    for d in example_dirs:
        entry = _build_skill_entry(d, SKILLS_DIR, "example")
        if entry:
            skills.append(entry)
    for d in document_dirs:
        entry = _build_skill_entry(d, DOC_SKILLS_DIR, "document")
        if entry:
            skills.append(entry)

    registry = {
        "version": "1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "anthropic-agent-skills",
        "skills": skills,
        "categories": _build_categories(skills),
        "bundles": _build_bundles(skills),
    }

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(registry, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(f"Registry generated: {len(skills)} skills -> {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
