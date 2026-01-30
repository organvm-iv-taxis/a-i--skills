#!/usr/bin/env python3
"""Validate generated skill bundle directories are in sync and not symlinked."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / ".build"

BUNDLES = {
    "example": {
        "list": BUILD_DIR / "collections" / "example-skills.txt",
        "targets": [
            BUILD_DIR / "direct" / "example",
            BUILD_DIR / "codex" / "skills",
            BUILD_DIR / "claude" / "skills",
            BUILD_DIR / "extensions" / "gemini" / "example-skills" / "skills",
        ],
    },
    "document": {
        "list": BUILD_DIR / "collections" / "document-skills.txt",
        "targets": [
            BUILD_DIR / "direct" / "document",
            BUILD_DIR / "codex" / "skills-document",
            BUILD_DIR / "claude" / "skills-document",
            BUILD_DIR / "extensions" / "gemini" / "document-skills" / "skills",
        ],
    },
}


def _load_list(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"Missing collection list: {path}")
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _check_marker(target: Path, errors: list[str]) -> None:
    marker = target / ".skills-generated"
    if not marker.exists():
        errors.append(f"{target}: missing .skills-generated marker")


def _check_no_symlinks(target: Path, errors: list[str]) -> None:
    for path in target.rglob("*"):
        if path.is_symlink():
            errors.append(f"{target}: contains symlink {path}")


def _check_top_level(target: Path, expected_names: set[str], errors: list[str]) -> None:
    if not target.exists():
        errors.append(f"{target}: missing target directory")
        return

    actual = {
        p.name
        for p in target.iterdir()
        if p.is_dir() and p.name != ".skills-generated"
    }
    missing = expected_names - actual
    extra = actual - expected_names
    if missing:
        errors.append(f"{target}: missing {sorted(missing)}")
    if extra:
        errors.append(f"{target}: extra {sorted(extra)}")


def main() -> int:
    errors: list[str] = []

    for bundle_name, bundle in BUNDLES.items():
        list_path = bundle["list"]
        expected_paths = _load_list(list_path)
        expected_names = {Path(path).name for path in expected_paths}
        for target in bundle["targets"]:
            _check_marker(target, errors)
            _check_no_symlinks(target, errors)
            _check_top_level(target, expected_names, errors)

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    print("Generated bundle directories are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
