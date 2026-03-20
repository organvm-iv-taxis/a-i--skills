# Governance-Aware Skill Taxonomy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add governance-aware metadata (lifecycle phases, norm groups, organ affinity) to all 105 skills and wire the build pipeline to extract, validate, and publish it.

**Architecture:** Four new flat frontmatter fields (`governance_phases`, `governance_norm_group`, `governance_auto_activate`, `organ_affinity`) added to SKILL.md files. A JSON mapping file drives batch application. Existing validation, registry generation, and collection refresh scripts are extended to handle the new fields. No parser changes needed — all fields are flat top-level keys.

**Tech Stack:** Python 3 scripts (no external deps), YAML frontmatter, JSON registry

**Spec:** `docs/superpowers/specs/2026-03-20-governance-aware-skill-taxonomy-design.md` (v3)

---

## File Map

| Action | File | Responsibility |
|--------|------|---------------|
| Create | `scripts/governance_mapping.json` | Complete mapping of all 105 skills to new governance fields + triggers + complements |
| Create | `scripts/apply_governance_metadata.py` | Batch script to inject frontmatter fields from mapping into SKILL.md files |
| Modify | `scripts/validate_skills.py:17-24` | Add validation constants for new governance fields |
| Modify | `scripts/validate_skills.py:110-148` | Add validation logic for `governance_phases`, `governance_norm_group`, `governance_auto_activate`, `organ_affinity` |
| Modify | `scripts/generate_registry.py:20-23` | Add new fields to `LIST_FIELDS` tuple |
| Modify | `scripts/generate_registry.py:50-60` | Extract `governance_*` and `organ_affinity` into registry entries |
| Modify | `scripts/generate_registry.py:114` | Bump registry version `1.1` → `1.2` |
| Modify | `scripts/refresh_skill_collections.py:120-139` | Add `_write_governance_lists()` for governance-norms.txt and auto-activate-skills.txt |
| Modify | `docs/api/skill-spec.md` | Document new fields in optional fields table |
| Modify | `docs/api/activation-conditions.md` | Document governance-aware activation behavior |
| Modify | 101 files | `skills/**/SKILL.md` — add governance frontmatter |
| Modify | 4 files | `document-skills/*/SKILL.md` — add governance frontmatter |

---

## Task 1: Create the Governance Mapping Data File

**Files:**
- Create: `scripts/governance_mapping.json`

This is the single source of truth for all 105 skill → governance metadata assignments. The batch script (Task 5) reads this file.

- [ ] **Step 1: Create `scripts/governance_mapping.json`**

The file structure is a JSON object keyed by skill name. Each entry contains only the fields to ADD — existing fields are preserved. The complete mapping is derived from the spec (v3) tables.

```json
{
  "_meta": {
    "spec": "docs/superpowers/specs/2026-03-20-governance-aware-skill-taxonomy-design.md",
    "version": "v3",
    "description": "Governance metadata mapping for all 105 skills. Source of truth for apply_governance_metadata.py."
  },
  "accessibility-patterns": {
    "governance_phases": ["build", "prove"],
    "governance_norm_group": "quality-gate",
    "organ_affinity": ["organ-iii", "organ-ii"],
    "triggers": ["user-asks-about-accessibility", "user-asks-about-wcag", "file-type:*.html", "context:frontend"],
    "complements": ["responsive-design-patterns", "frontend-design-systems", "webapp-testing"]
  },
  "agent-swarm-orchestrator": {
    "governance_phases": ["shape", "build"],
    "organ_affinity": ["organ-iv"],
    "triggers": ["user-asks-about-agent-swarm", "user-asks-about-multi-agent", "context:multi-agent"],
    "complements": ["multi-agent-workforce-planner", "skill-chain-prompts"]
  }
}
```

The full file will contain all 105 entries. Build it by transcribing every row from the spec's "Full Skill Matrix" tables. Rules:
- Only include `governance_norm_group` if the spec assigns one (most skills have `—`)
- Only include `governance_auto_activate` if `true` (omit = false default)
- For skills that already have triggers (5 skills: api-design-patterns, canvas-design, mcp-builder, security-threat-modeler, tdd-workflow), set `"triggers_mode": "merge"` to merge rather than replace
- For skills that already have complements (5 skills), set `"complements_mode": "merge"`
- `organ_affinity` is always a list, even for single organs
- Skills with no organ affinity (cv-resume-builder, interview-preparation, networking-outreach) should have `"organ_affinity": []`

- [ ] **Step 2: Validate the JSON is parseable**

Run: `python3 -c "import json; d=json.load(open('scripts/governance_mapping.json')); print(f'{len(d)-1} skills mapped')"`
Expected: `105 skills mapped` (105 skills + 1 _meta entry)

- [ ] **Step 3: Commit**

```bash
git add scripts/governance_mapping.json
git commit -m "feat: add governance metadata mapping for all 105 skills"
```

---

## Task 2: Add Validation Constants and Logic

**Files:**
- Modify: `scripts/validate_skills.py`

- [ ] **Step 1: Add validation constants after line 24**

After the `VALID_TIERS` line, add:

```python
VALID_GOVERNANCE_PHASES = {"frame", "shape", "build", "prove", "ship"}
VALID_NORM_GROUPS = {
    "repo-hygiene", "quality-gate", "security-baseline",
    "documentation-standard", "distribution-readiness",
}
VALID_ORGAN_AFFINITY = {
    "all", "organ-i", "organ-ii", "organ-iii", "organ-iv",
    "organ-v", "organ-vi", "organ-vii", "meta",
}
```

- [ ] **Step 2: Add validation logic after the tier validation block (after line 147)**

After the `if tier == "core":` block, add:

```python
    # Validate governance fields
    gov_phases_raw = data.get("governance_phases")
    if gov_phases_raw:
        gov_phases = parse_list_field(gov_phases_raw)
        for phase in gov_phases:
            if phase not in VALID_GOVERNANCE_PHASES:
                errors.append(
                    f"{skill_dir}: invalid governance_phases '{phase}', "
                    f"must be one of: {', '.join(sorted(VALID_GOVERNANCE_PHASES))}"
                )

    gov_norm = data.get("governance_norm_group")
    if gov_norm and gov_norm not in VALID_NORM_GROUPS:
        errors.append(
            f"{skill_dir}: invalid governance_norm_group '{gov_norm}', "
            f"must be one of: {', '.join(sorted(VALID_NORM_GROUPS))}"
        )

    gov_auto = data.get("governance_auto_activate")
    if gov_auto and gov_auto not in ("true", "false"):
        errors.append(
            f"{skill_dir}: governance_auto_activate must be 'true' or 'false', "
            f"got '{gov_auto}'"
        )

    organ_raw = data.get("organ_affinity")
    if organ_raw:
        organs = parse_list_field(organ_raw)
        for organ in organs:
            if organ not in VALID_ORGAN_AFFINITY:
                errors.append(
                    f"{skill_dir}: invalid organ_affinity '{organ}', "
                    f"must be one of: {', '.join(sorted(VALID_ORGAN_AFFINITY))}"
                )
```

- [ ] **Step 3: Run the validator to confirm no regressions**

Run: `python3 scripts/validate_skills.py --collection all --unique`
Expected: Same pass/fail count as before (no new errors — fields don't exist yet)

- [ ] **Step 4: Commit**

```bash
git add scripts/validate_skills.py
git commit -m "feat: add validation for governance_phases, governance_norm_group, governance_auto_activate, organ_affinity"
```

---

## Task 3: Update Registry Generation

**Files:**
- Modify: `scripts/generate_registry.py`

- [ ] **Step 1: Add new fields to LIST_FIELDS (line 20-23)**

Replace the `LIST_FIELDS` tuple:

```python
LIST_FIELDS = (
    "prerequisites", "tags", "inputs", "outputs", "side_effects",
    "triggers", "complements", "includes",
    "governance_phases", "organ_affinity",
)
```

- [ ] **Step 2: Add scalar governance fields to `_build_skill_entry` (after line 59)**

After the `"tier": fm.get("tier"),` line, add:

```python
        "governance_norm_group": fm.get("governance_norm_group"),
        "governance_auto_activate": fm.get("governance_auto_activate") == "true",
```

- [ ] **Step 3: Bump registry version (line 114)**

Change `"version": "1.1"` to `"version": "1.2"`.

- [ ] **Step 4: Regenerate registry to confirm no errors**

Run: `python3 scripts/generate_registry.py`
Expected: `Registry generated: 105 skills -> .build/skills-registry.json`

- [ ] **Step 5: Commit**

```bash
git add scripts/generate_registry.py
git commit -m "feat: extract governance metadata into skills registry v1.2"
```

---

## Task 4: Update Collection Refresh for Governance Lists

**Files:**
- Modify: `scripts/refresh_skill_collections.py`

- [ ] **Step 1: Add `_write_governance_lists()` function after `_write_tier_lists` (after line 139)**

```python
def _write_governance_lists(
    collections_dir: Path, skill_dirs: list[Path],
) -> None:
    """Generate governance-norms.txt and auto-activate-skills.txt."""
    norms: list[Path] = []
    auto_activate: list[Path] = []
    for d in skill_dirs:
        skill_file = d / "SKILL.md"
        try:
            text = skill_file.read_text(encoding="utf-8")
        except OSError:
            continue
        fm = _extract_frontmatter(text)
        if fm.get("governance_norm_group"):
            norms.append(d)
        if fm.get("governance_auto_activate") == "true":
            auto_activate.append(d)
    _write_list(collections_dir / "governance-norms.txt", norms)
    _write_list(collections_dir / "auto-activate-skills.txt", auto_activate)
```

- [ ] **Step 2: Call `_write_governance_lists` from the main refresh flow**

Find where `_write_tier_lists` is called and add a call to `_write_governance_lists` immediately after, with the same arguments.

- [ ] **Step 3: Run refresh to confirm it works**

Run: `python3 scripts/refresh_skill_collections.py`
Expected: Completes without error. Two new empty files created in `.build/collections/` (empty because no skills have governance fields yet)

- [ ] **Step 4: Commit**

```bash
git add scripts/refresh_skill_collections.py
git commit -m "feat: generate governance-norms.txt and auto-activate-skills.txt collection files"
```

---

## Task 5: Create the Batch Metadata Application Script

**Files:**
- Create: `scripts/apply_governance_metadata.py`

This script reads `governance_mapping.json` and injects the new frontmatter fields into each SKILL.md file.

- [ ] **Step 1: Write `scripts/apply_governance_metadata.py`**

```python
#!/usr/bin/env python3
"""Apply governance metadata from mapping file to all SKILL.md frontmatter.

Reads governance_mapping.json and injects new fields into each skill's
SKILL.md frontmatter. Existing fields are preserved. List fields can be
merged or replaced based on the mapping entry's mode flags.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
DOC_SKILLS_DIR = ROOT / "document-skills"
MAPPING_PATH = Path(__file__).resolve().parent / "governance_mapping.json"

# Fields that this script manages
GOVERNANCE_FIELDS = (
    "governance_phases", "governance_norm_group",
    "governance_auto_activate", "organ_affinity",
)
LIST_MERGE_FIELDS = ("triggers", "complements")


def _find_all_skills() -> dict[str, Path]:
    """Return {skill_name: skill_dir} for all skills."""
    skills: dict[str, Path] = {}
    for base in (SKILLS_DIR, DOC_SKILLS_DIR):
        for skill_file in base.rglob("SKILL.md"):
            skill_dir = skill_file.parent
            if skill_dir != base:
                skills[skill_dir.name] = skill_dir
    return skills


def _parse_frontmatter_bounds(text: str) -> tuple[int, int] | None:
    """Return (start, end) line indices of frontmatter delimiters."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return (0, i)
    return None


def _format_list(items: list[str]) -> str:
    """Format a list as YAML inline: [a, b, c]."""
    return "[" + ", ".join(items) + "]"


def _parse_existing_list(text: str, field: str) -> list[str]:
    """Extract existing list field values from frontmatter text."""
    pattern = re.compile(rf"^{re.escape(field)}:\s*(.+)$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return []
    value = match.group(1).strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1]
        return [item.strip() for item in inner.split(",") if item.strip()]
    return []


def _apply_to_skill(skill_dir: Path, mapping: dict) -> bool:
    """Apply governance metadata to a single SKILL.md. Returns True if modified."""
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    bounds = _parse_frontmatter_bounds(text)
    if bounds is None:
        print(f"  SKIP {skill_dir.name}: no frontmatter")
        return False

    lines = text.splitlines(keepends=True)
    start, end = bounds
    fm_lines = lines[start + 1 : end]  # lines between --- delimiters
    fm_text = "".join(fm_lines)

    new_lines: list[str] = []

    # Add governance fields
    for field in GOVERNANCE_FIELDS:
        if field not in mapping:
            continue
        value = mapping[field]
        # Remove existing line for this field if present
        fm_text = re.sub(rf"^{re.escape(field)}:.*\n?", "", fm_text, flags=re.MULTILINE)
        if isinstance(value, list):
            if value:  # skip empty lists
                new_lines.append(f"{field}: {_format_list(value)}\n")
        elif isinstance(value, bool):
            if value:  # only write true (false is default)
                new_lines.append(f"{field}: true\n")
        elif value:
            new_lines.append(f"{field}: {value}\n")

    # Handle triggers and complements (merge or replace)
    for field in LIST_MERGE_FIELDS:
        if field not in mapping:
            continue
        new_items = mapping[field]
        mode = mapping.get(f"{field}_mode", "replace")
        if mode == "merge":
            existing = _parse_existing_list(fm_text, field)
            merged = list(dict.fromkeys(existing + new_items))  # preserve order, dedup
            fm_text = re.sub(rf"^{re.escape(field)}:.*\n?", "", fm_text, flags=re.MULTILINE)
            new_lines.append(f"{field}: {_format_list(merged)}\n")
        else:
            fm_text = re.sub(rf"^{re.escape(field)}:.*\n?", "", fm_text, flags=re.MULTILINE)
            if new_items:
                new_lines.append(f"{field}: {_format_list(new_items)}\n")

    if not new_lines:
        return False

    # Reconstruct the file
    reconstructed = (
        lines[0]  # opening ---
        + fm_text.rstrip("\n") + "\n"
        + "".join(new_lines)
        + lines[end]  # closing ---
        + "".join(lines[end + 1 :])
    )

    skill_file.write_text(reconstructed, encoding="utf-8")
    return True


def main() -> int:
    mapping = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    skills = _find_all_skills()

    meta = mapping.pop("_meta", {})
    print(f"Mapping version: {meta.get('version', 'unknown')}")
    print(f"Skills found: {len(skills)}")
    print(f"Mappings loaded: {len(mapping)}")
    print()

    modified = 0
    skipped = 0
    missing = 0

    for skill_name, skill_mapping in sorted(mapping.items()):
        if skill_name in skills:
            if _apply_to_skill(skills[skill_name], skill_mapping):
                print(f"  OK  {skill_name}")
                modified += 1
            else:
                print(f"  SKIP {skill_name} (no changes)")
                skipped += 1
        else:
            print(f"  MISS {skill_name} (not found on disk)")
            missing += 1

    # Check for unmapped skills
    mapped_names = set(mapping.keys())
    unmapped = set(skills.keys()) - mapped_names
    if unmapped:
        print(f"\nWARNING: {len(unmapped)} skills not in mapping:")
        for name in sorted(unmapped):
            print(f"  {name}")

    print(f"\nDone: {modified} modified, {skipped} skipped, {missing} missing")
    return 1 if missing > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Dry-run test (before mapping file is complete)**

Run: `python3 scripts/apply_governance_metadata.py`
Expected: Shows "0 skills mapped" or errors because mapping file is minimal. Confirms the script loads and runs.

- [ ] **Step 3: Commit**

```bash
git add scripts/apply_governance_metadata.py
git commit -m "feat: add batch governance metadata application script"
```

---

## Task 6: Populate the Full Mapping File

**Files:**
- Modify: `scripts/governance_mapping.json`

- [ ] **Step 1: Transcribe all 105 entries from the spec**

Read every row from the spec's "Full Skill Matrix" tables (sections: creative, data, development, documentation, education, integrations, knowledge, professional, project-management, security, specialized, tools, document skills).

For each skill, create an entry in `governance_mapping.json` with:
- `governance_phases`: from the "Phases" column (list of strings)
- `governance_norm_group`: from the "Norm" column (string, omit if `—`)
- `governance_auto_activate`: source from the **"Governance Norms (auto_activate: true)"** section of the spec (the explicit list of 7 skills), NOT from the matrix tables (which only show the Auto column for 3 of 12 category tables). The 7 auto-activate skills are: `github-repository-standards`, `github-repo-curator`, `coding-standards-enforcer`, `verification-loop`, `tdd-workflow`, `security-threat-modeler`, `product-requirements-designer`
- `organ_affinity`: from the "Organ" column (list of strings)
- `triggers`: from the "Triggers" column (list of strings). For skills marked "*(has triggers)*", set `"triggers_mode": "merge"` and provide the NEW triggers to add
- `complements`: from the "Complement Graph" section — ensure bidirectionality (if A complements B, B must also complement A)

The 5 skills with existing triggers that need merge mode:
- `api-design-patterns`: `"triggers_mode": "merge"`
- `canvas-design`: `"triggers_mode": "merge"`
- `mcp-builder`: `"triggers_mode": "merge"`
- `security-threat-modeler`: `"triggers_mode": "merge"`
- `tdd-workflow`: `"triggers_mode": "merge"`

The 5 skills with existing complements that need merge mode:
- `api-design-patterns`: `"complements_mode": "merge"`
- `canvas-design`: `"complements_mode": "merge"`
- `mcp-builder`: `"complements_mode": "merge"`
- `security-threat-modeler`: `"complements_mode": "merge"`
- `tdd-workflow`: `"complements_mode": "merge"`

- [ ] **Step 2: Validate entry count**

Run: `python3 -c "import json; d=json.load(open('scripts/governance_mapping.json')); print(f'{len(d)-1} skills mapped')"`
Expected: `105 skills mapped`

- [ ] **Step 3: Commit**

```bash
git add scripts/governance_mapping.json
git commit -m "feat: complete governance metadata mapping for all 105 skills"
```

---

## Task 7: Apply Metadata to All Skills

**Files:**
- Modify: 105 `SKILL.md` files across `skills/` and `document-skills/`

- [ ] **Step 1: Run the batch application script**

Run: `python3 scripts/apply_governance_metadata.py`
Expected: `105 modified, 0 skipped, 0 missing` with no warnings about unmapped skills

- [ ] **Step 2: Spot-check 5 representative skills**

Verify frontmatter was correctly injected by reading:

```bash
head -20 skills/development/verification-loop/SKILL.md
head -20 skills/documentation/github-repository-standards/SKILL.md
head -20 skills/security/security-threat-modeler/SKILL.md
head -20 skills/creative/algorithmic-art/SKILL.md
head -20 document-skills/pdf/SKILL.md
```

Expected: Each shows the new `governance_phases`, `organ_affinity` fields in the frontmatter, with correct values matching the spec.

- [ ] **Step 3: Run validation**

Run: `python3 scripts/validate_skills.py --collection all --unique`
Expected: All skills pass (no new errors from governance fields)

- [ ] **Step 4: Commit**

```bash
git add skills/ document-skills/
git commit -m "feat: apply governance metadata to all 105 skills

Adds governance_phases, governance_norm_group, governance_auto_activate,
and organ_affinity to all SKILL.md frontmatter. Populates triggers for
100 skills and complements based on the complement graph.

Spec: docs/superpowers/specs/2026-03-20-governance-aware-skill-taxonomy-design.md"
```

---

## Task 8: Regenerate All Build Artifacts

**Files:**
- Regenerate: `.build/skills-registry.json`, `.build/skills-lock.json`, `.build/collections/*.txt`, all bundle directories

- [ ] **Step 1: Run full refresh**

Run: `python3 scripts/refresh_skill_collections.py`
Expected: Completes without error

- [ ] **Step 2: Verify governance collection files**

Run: `cat .build/collections/governance-norms.txt | wc -l`
Expected: ~22 lines (skills with norm_group set)

Run: `cat .build/collections/auto-activate-skills.txt | wc -l`
Expected: ~7 lines (auto-activate skills)

- [ ] **Step 3: Verify registry has governance fields**

Run: `python3 -c "import json; r=json.load(open('.build/skills-registry.json')); s=r['skills'][0]; print(s.get('governance_phases'), s.get('organ_affinity'), r['version'])"`
Expected: Shows list values and version `1.2`

- [ ] **Step 4: Run generated-dirs validation**

Run: `python3 scripts/validate_generated_dirs.py`
Expected: All checks pass

- [ ] **Step 5: Commit all generated artifacts**

```bash
git add .build/
git commit -m "chore: regenerate build artifacts with governance metadata (registry v1.2)"
```

---

## Task 9: Update Spec Documentation

**Files:**
- Modify: `docs/api/skill-spec.md`
- Modify: `docs/api/activation-conditions.md`

- [ ] **Step 1: Add new fields to skill-spec.md optional fields table**

After the `tier` field entry in the optional fields table, add:

```markdown
| `governance_phases` | list | Lifecycle phases where this skill is relevant: `frame`, `shape`, `build`, `prove`, `ship` |
| `governance_norm_group` | string | Governance norm group: `repo-hygiene`, `quality-gate`, `security-baseline`, `documentation-standard`, `distribution-readiness` |
| `governance_auto_activate` | boolean | Whether this skill fires automatically at governance gates (default: false) |
| `organ_affinity` | list | Which ORGANVM organs this skill serves: `all`, `organ-i` through `organ-vii`, `meta` |
```

Add field constraint sections for each (following the existing pattern for complexity, time_to_learn, etc.).

- [ ] **Step 2: Add governance activation section to activation-conditions.md**

After the "Advisory Nature of Triggers" section, add a new section:

```markdown
## Governance-Aware Activation

In addition to the five trigger types, skills may declare governance metadata that enables phase-aware and norm-based activation.

### Governance Fields

Skills can declare:
- `governance_phases`: lifecycle phases where the skill is relevant
- `governance_norm_group`: which governance norm cluster the skill belongs to
- `governance_auto_activate`: whether the skill fires automatically at governance gates

### Activation Behavior

When `governance_auto_activate` is `true`, the activation engine should fire the skill when:
1. The session enters a lifecycle phase matching `governance_phases`, OR
2. A promotion gate is reached and the skill's `governance_norm_group` applies

The `context:promotion` keyword is a recognized context trigger that fires when a promotion state transition is being evaluated.

### Organ Routing

The `organ_affinity` field enables conductor routing: when working within a specific organ's repository, skills with matching organ affinity are ranked higher for activation.
```

- [ ] **Step 3: Commit**

```bash
git add docs/api/skill-spec.md docs/api/activation-conditions.md
git commit -m "docs: document governance_phases, governance_norm_group, governance_auto_activate, organ_affinity fields"
```

---

## Task 10: Final Validation and Cleanup

- [ ] **Step 1: Run full validation suite**

```bash
python3 scripts/validate_skills.py --collection example --unique && \
python3 scripts/validate_skills.py --collection document --unique && \
python3 scripts/validate_generated_dirs.py
```
Expected: All pass

- [ ] **Step 2: Verify registry stats**

```bash
python3 -c "
import json
r = json.load(open('.build/skills-registry.json'))
skills = r['skills']
print(f'Registry version: {r[\"version\"]}')
print(f'Total skills: {len(skills)}')
print(f'With governance_phases: {sum(1 for s in skills if s.get(\"governance_phases\"))}')
print(f'With organ_affinity: {sum(1 for s in skills if s.get(\"organ_affinity\"))}')
print(f'With governance_norm_group: {sum(1 for s in skills if s.get(\"governance_norm_group\"))}')
print(f'With governance_auto_activate: {sum(1 for s in skills if s.get(\"governance_auto_activate\"))}')
print(f'With triggers: {sum(1 for s in skills if s.get(\"triggers\"))}')
print(f'With complements: {sum(1 for s in skills if s.get(\"complements\"))}')
"
```

Expected:
```
Registry version: 1.2
Total skills: 105
With governance_phases: 105
With organ_affinity: ~102 (3 career skills have empty)
With governance_norm_group: ~22
With governance_auto_activate: 7
With triggers: 105
With complements: ~60+
```

- [ ] **Step 3: Commit the spec and plan documents**

```bash
git add docs/superpowers/specs/ docs/superpowers/plans/ .claude/plans/
git commit -m "docs: add governance-aware skill taxonomy spec (v3) and implementation plan"
```

---

## Deferred to Phase 2

The following items from the spec are explicitly out of scope for this plan:

- **`spec_version: "2.0"` field**: The spec mentions adding a version field to `docs/api/skill-spec.md` itself. Deferred — the registry version bump (1.1→1.2) is sufficient for consumer compatibility.
- **`inputs`, `outputs`, `side_effects` population**: Enables skill-planner chain composition. Requires a separate mapping exercise.
- **`tags` population**: Lower priority; many skills already have discoverable descriptions.
- **Conductor integration**: Building the runtime that reads governance metadata for phase-aware activation.
- **Promotion-gate integration**: Enforcing norm groups at state transitions in the promotion pipeline.
