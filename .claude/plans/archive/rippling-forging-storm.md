# Plan: Restructure speckit Skill Directory

## Context

The speckit skill at `/Users/4jp/Workspace/organvm-iv-taxis/a-i--skills/skills/tools/speckit/` implements Specification-Driven Development (SDD) with three commands (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`). It currently lacks a human-readable README and mixes templates with reference docs in a flat `references/` directory.

Applying principles from the **GitHub Repository Standards** skill (Minimal Root, Progressive Disclosure, World-Class README) and **GitHub Repo Curator** skill (README as conversion funnel, clear file structure):

**Problems:**
1. No `README.md` — GitHub renders nothing useful when humans browse the directory
2. Templates (fill-in artifacts) mixed with reference docs (methodology, commands) in `references/`
3. Stale internal reference in `plan-template.md` pointing to `.specify/templates/commands/plan.md` (pre-packaging path)

## Target Structure

```
speckit/
├── README.md                              # NEW - human-readable overview
├── SKILL.md                               # UPDATED - path refs
├── assets/
│   └── templates/
│       ├── spec-template.md               # MOVED from references/
│       ├── plan-template.md               # MOVED + stale ref fixed
│       ├── tasks-template.md              # MOVED from references/
│       └── constitution-template.md       # MOVED from references/
└── references/
    ├── commands/
    │   ├── plan.md                        # UPDATED - template path
    │   ├── specify.md                     # UPDATED - template path
    │   └── tasks.md                       # UPDATED - template path
    └── methodology.md                     # UNCHANGED
```

**Rationale:** Templates are actionable resources the AI copies into output (belong in `assets/`). Methodology and commands are reference reading (stay in `references/`). This matches the established skill convention (`SKILL.md` / `scripts/` / `references/` / `assets/`).

## Steps

### 1. Create `assets/templates/` and move template files
```bash
mkdir -p assets/templates
git mv references/spec-template.md assets/templates/
git mv references/plan-template.md assets/templates/
git mv references/tasks-template.md assets/templates/
git mv references/constitution-template.md assets/templates/
```

### 2. Fix stale reference in `assets/templates/plan-template.md`
- Line 6: `.specify/templates/commands/plan.md` → `references/commands/plan.md`

### 3. Update SKILL.md (10 path changes + Reference Files section)
Replace all `references/*-template.md` paths with `assets/templates/*-template.md`:
- Lines 48, 81, 113, 151 (inline template references)
- Lines 185-190: Rewrite "Reference Files" section into two subsections (Templates / Documentation)

### 4. Update command files (3 path changes)
- `references/commands/specify.md` line 35: `references/spec-template.md` → `assets/templates/spec-template.md`
- `references/commands/plan.md` line 46: `references/plan-template.md` → `assets/templates/plan-template.md`
- `references/commands/tasks.md` line 175: `references/tasks-template.md` → `assets/templates/tasks-template.md`

### 5. Create README.md
World-Class README following the conversion funnel pattern:
- **Hero**: Title + one-sentence pitch
- **Value table**: Three commands with purpose and output
- **Quick Start**: Copy-pasteable commands
- **How It Works**: Brief SDD overview, links to methodology
- **File Structure**: Directory tree for orientation
- **Constitution**: Optional feature callout

## Verification

After all changes:
- `grep -r "references/.*-template" .` returns zero matches
- `assets/templates/` has exactly 4 files
- `references/` has `methodology.md` and `commands/` (3 files)
- `README.md` exists and renders cleanly
- No broken internal references remain

## Files Modified

| File | Change |
|------|--------|
| `SKILL.md` | 10 path updates + Reference Files section rewrite |
| `references/commands/specify.md` | 1 path update |
| `references/commands/plan.md` | 1 path update |
| `references/commands/tasks.md` | 1 path update |
| `assets/templates/plan-template.md` | Fix stale `.specify/` reference |
| `README.md` | New file |
| 4 template files | Moved from `references/` to `assets/templates/` |
