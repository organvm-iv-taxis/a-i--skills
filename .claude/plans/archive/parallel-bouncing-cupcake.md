# Plan: Restructure SpecKit Skill — GitHub Best Practices

## Context

The SpecKit skill at `a-i--skills/skills/tools/speckit/` is a core SDD toolkit (3 slash commands, 10 files) that currently has structural issues:
- Templates mixed with reference docs in `references/`
- Missing semantic frontmatter fields (only 3 of 13)
- No helper scripts (unlike peer skills like `skill-creator`)
- No workflow-integration doc (unlike 40+ other skills in the repo)
- One stale internal path reference (`.specify/templates/`)

This plan applies conventions from `github-repository-standards` and `github-repo-curator` skills, plus the repo's own skill structure conventions, to bring SpecKit up to the quality bar of the best skills in the collection.

## Target Directory Tree

```
speckit/
  SKILL.md                                # MODIFY: enrich frontmatter (3→13 fields), update 8 paths
  scripts/
    init_spec_dir.py                      # NEW: scaffold specs/{feature}/ directory
    validate_spec.py                      # NEW: validate spec completeness by stage
  references/
    methodology.md                        # UNCHANGED (read-only reference, stays here)
    workflow-integration.md               # NEW: ecosystem connections doc
    commands/
      specify.md                          # MODIFY: 1 template path update (line 35)
      plan.md                             # MODIFY: 1 template path update (line 46-47)
      tasks.md                            # MODIFY: 1 template path update (line 175)
  assets/
    templates/
      spec-template.md                    # MOVE from references/
      plan-template.md                    # MOVE from references/ + fix stale path (line 6)
      tasks-template.md                   # MOVE from references/
      constitution-template.md            # MOVE from references/
```

**Total: 12 files** (was 10 — adds 3 new, moves 4, modifies 5)

---

## Step-by-Step Implementation

### Step 1: Create new directories

```
mkdir -p assets/templates scripts
```

### Step 2: Move templates to `assets/templates/`

Templates are copy-and-customize resources (assets), not read-only documentation (references).

| Source | Destination |
|--------|-------------|
| `references/spec-template.md` | `assets/templates/spec-template.md` |
| `references/plan-template.md` | `assets/templates/plan-template.md` |
| `references/tasks-template.md` | `assets/templates/tasks-template.md` |
| `references/constitution-template.md` | `assets/templates/constitution-template.md` |

### Step 3: Fix stale path in plan-template.md

In `assets/templates/plan-template.md` line 6, change:
```
.specify/templates/commands/plan.md  →  references/commands/plan.md
```

### Step 4: Update all path references

**SKILL.md** (8 references):
- Lines 48, 81, 113, 151: `references/*-template.md` → `assets/templates/*-template.md`
- Lines 185-188 (Reference Files section): same path updates

**references/commands/specify.md** line 35:
```
references/spec-template.md  →  assets/templates/spec-template.md
```

**references/commands/plan.md** line 46-47:
```
references/plan-template.md  →  assets/templates/plan-template.md
```

**references/commands/tasks.md** line 175:
```
references/tasks-template.md  →  assets/templates/tasks-template.md
```

### Step 5: Enrich SKILL.md frontmatter

Replace the 3-field frontmatter with the full semantic block. All values validated against the repo's `validate_skills.py`:

```yaml
---
name: speckit
description: Specification-Driven Development (SDD) toolkit. Transforms ideas into executable specifications, implementation plans, and task lists. Use for feature planning, PRD creation, or when user invokes /speckit.specify, /speckit.plan, /speckit.tasks commands.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - specification
  - sdd
  - planning
  - requirements
  - prd
  - feature-spec
inputs:
  - feature-description
  - project-context
outputs:
  - feature-specification
  - implementation-plan
  - task-list
  - data-model
  - api-contracts
side_effects:
  - creates-files
triggers:
  - user-asks-about-specifications
  - user-asks-about-planning
  - user-asks-about-prd
  - user-invokes-speckit
complements:
  - tdd-workflow
  - verification-loop
  - product-requirements-designer
  - skill-chain-prompts
  - api-design-patterns
  - backend-implementation-patterns
  - testing-patterns
tier: core
---
```

**Validation constraints respected:**
- `complexity`: must be `beginner|intermediate|advanced` — using `intermediate`
- `time_to_learn`: must be `5min|30min|1hour|multi-hour` — using `30min`
- `side_effects`: restricted to `{creates-files, modifies-git, runs-commands, network-access, installs-packages, reads-filesystem}` — using `creates-files` only
- `tier: core` requires `complexity`, `time_to_learn`, `tags`, and `triggers` — all provided
- `complements`: all 7 skills verified to exist in the repo

### Step 6: Add body sections to SKILL.md

After the "Reference Files" section, add:

```markdown
## Helper Scripts

- `scripts/init_spec_dir.py` - Scaffold a new feature spec directory
- `scripts/validate_spec.py` - Validate specification completeness
```

Add to "Reference Files" list:
```markdown
- `references/workflow-integration.md` - Ecosystem integration patterns
```

### Step 7: Create `scripts/init_spec_dir.py`

**Purpose**: Scaffold a feature spec directory with auto-numbering. Pattern follows `skill-creator/scripts/init_skill.py`.

**Behavior**:
1. Accept `<feature-name>` and optional `--path <specs-dir>` (default `./specs`)
2. Auto-increment feature number by scanning existing dirs (001, 002, 003...)
3. Create `specs/{NNN}-{feature-name}/spec.md` from `assets/templates/spec-template.md`
4. Create `specs/{NNN}-{feature-name}/checklists/requirements.md`
5. Print created paths and next steps

**~80 lines**, Python 3, type hints, `Path` for filesystem ops, `argparse` for CLI.

### Step 8: Create `scripts/validate_spec.py`

**Purpose**: Validate spec directory completeness by stage. Pattern follows `skill-creator/scripts/quick_validate.py`.

**Behavior**: Accept `<spec-dir>` and `--stage specify|plan|tasks|all`.

| Stage | Checks |
|-------|--------|
| `specify` | spec.md exists with required sections, checklists/ exists, count `[NEEDS CLARIFICATION]` markers (warn if >3), user stories have priorities |
| `plan` | + plan.md, research.md, data-model.md, contracts/ exist and are non-empty |
| `tasks` | + tasks.md exists with numbered tasks (T001+), phase structure, user story labels |
| `all` | All of the above |

Exit 0 on pass, 1 on fail. **~120 lines**.

### Step 9: Create `references/workflow-integration.md`

**Purpose**: Document SpecKit's place in the skill ecosystem. Pattern follows `research-synthesis-workflow/references/workflow-integration.md`.

**Content**:
- Related Skills table (8 skills: tdd-workflow, verification-loop, product-requirements-designer, skill-chain-prompts, api-design-patterns, backend-implementation-patterns, testing-patterns, github-repository-standards)
- Prerequisites section
- Handoff patterns (from: product-requirements-designer; to: tdd-workflow, verification-loop, backend-implementation-patterns)
- Workflow sequence diagram (ASCII)
- Integration checklist
- Common scenarios (Greenfield, Existing Project, Exploratory)

---

## Critical Files

| File | Action | Key change |
|------|--------|-----------|
| `skills/tools/speckit/SKILL.md` | Modify | Frontmatter enrichment (3→13 fields) + 8 path updates + 2 new sections |
| `skills/tools/speckit/references/commands/specify.md` | Modify | 1 path update (line 35) |
| `skills/tools/speckit/references/commands/plan.md` | Modify | 1 path update (line 46-47) |
| `skills/tools/speckit/references/commands/tasks.md` | Modify | 1 path update (line 175) |
| `skills/tools/speckit/assets/templates/plan-template.md` | Move + fix | Fix stale `.specify/` reference (line 6) |
| `skills/tools/speckit/assets/templates/spec-template.md` | Move | No content changes |
| `skills/tools/speckit/assets/templates/tasks-template.md` | Move | No content changes |
| `skills/tools/speckit/assets/templates/constitution-template.md` | Move | No content changes |
| `skills/tools/speckit/scripts/init_spec_dir.py` | Create | ~80 lines |
| `skills/tools/speckit/scripts/validate_spec.py` | Create | ~120 lines |
| `skills/tools/speckit/references/workflow-integration.md` | Create | ~120 lines |

**Pattern files to reference during implementation:**
- `skills/tools/skill-creator/scripts/init_skill.py` — scaffolding script pattern
- `skills/tools/skill-creator/scripts/quick_validate.py` — validation script pattern
- `skills/knowledge/research-synthesis-workflow/references/workflow-integration.md` — integration doc pattern

---

## Verification

1. **Skill health check**: `python3 scripts/skill_health_check.py --skill speckit`
2. **Frontmatter validation**: `python3 scripts/validate_skills.py --collection example --unique`
3. **Link validation**: `python3 scripts/validate_skills.py --collection example --check-links`
4. **Registry refresh**: `python3 scripts/refresh_skill_collections.py` — regenerates `.build/` artifacts
5. **Generated dirs sync**: `python3 scripts/validate_generated_dirs.py`
6. **Manual check**: Verify all template references in SKILL.md, specify.md, plan.md, tasks.md resolve to existing files under `assets/templates/`
7. **Script test**: Run `python3 scripts/init_spec_dir.py test-feature --path /tmp/test-specs` and verify output
8. **Script test**: Run `python3 scripts/validate_spec.py /path/to/existing-spec --stage all` against a known spec
