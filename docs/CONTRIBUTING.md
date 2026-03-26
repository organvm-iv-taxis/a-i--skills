# Contributing a Skill

You can create and submit a new skill in about 15 minutes. A skill is a folder with a single Markdown file -- no build system, no dependencies, no framework.

## Quick Start

### 1. Fork and clone

```bash
gh repo fork organvm-iv-taxis/a-i--skills --clone
cd a-i--skills
```

### 2. Pick a category

| Category | What belongs here |
|----------|-------------------|
| `creative` | Art, music, design, narrative, performance |
| `data` | Pipelines, ML, analytics, time-series |
| `development` | Code quality, testing, infrastructure, frontend, backend |
| `documentation` | READMEs, profiles, standards, style guides |
| `education` | Tutoring, curriculum, feedback, pedagogy |
| `integrations` | MCP, OAuth, webhooks, API connectors |
| `knowledge` | Knowledge graphs, research synthesis, second-brain |
| `professional` | Branding, CVs, proposals, networking, presentations |
| `project-management` | Roadmaps, requirements, coordination, orchestration |
| `security` | Threat modeling, compliance, incident response, auditing |
| `specialized` | Blockchain, gaming, AR, domain-specific |
| `tools` | Agent utilities, meta-tools, automation helpers |

### 3. Create your skill directory

```bash
mkdir -p skills/<category>/your-skill-name
```

The directory name must be lowercase kebab-case (letters, numbers, hyphens only).

### 4. Write your SKILL.md

Create `skills/<category>/your-skill-name/SKILL.md` with this template:

```markdown
---
name: your-skill-name
description: >-
  Brief, task-focused description of what the skill teaches an AI agent to do.
  Between 20 and 600 characters.
license: MIT
---

# Your Skill Name

Brief introduction: what this skill does and when an agent should use it.

## Instructions

Step-by-step workflow the agent follows. Be specific and actionable.

### Step 1: [Action]

Explain what to do, with code examples if relevant.

### Step 2: [Action]

Continue the workflow. Include constraints, edge cases, and expected outputs.

## Examples

Show concrete input/output pairs so the agent knows what "good" looks like.

## Common Mistakes

List pitfalls and how to avoid them.
```

**Two fields are required:** `name` (must match the directory name exactly) and `description` (20-600 characters, task-focused).

### 5. Validate

```bash
python3 scripts/validate_skills.py --collection example --unique
```

This checks that your frontmatter is valid, the name matches the directory, and the description is within bounds.

### 6. Regenerate build artifacts

```bash
python3 scripts/refresh_skill_collections.py
```

This updates the registry and multi-runtime bundles in `.build/`. Include these generated files in your PR.

### 7. Submit your PR

```bash
git checkout -b feat/add-your-skill-name
git add skills/<category>/your-skill-name/ .build/
git commit -m "feat: add your-skill-name skill"
git push -u origin feat/add-your-skill-name
gh pr create --title "feat: add your-skill-name skill"
```

CI will validate your skill automatically. A maintainer will review and merge.

---

## Skill Anatomy

Every skill is a folder containing at minimum a `SKILL.md` file:

```
your-skill-name/
├── SKILL.md           # Required: YAML frontmatter + Markdown instructions
├── scripts/           # Optional: helper scripts (Python, Bash)
├── references/        # Optional: supporting documentation
└── assets/            # Optional: templates, images, data files
```

Most skills are a single `SKILL.md` file. Only add scripts, references, or assets if they genuinely improve the skill.

## Frontmatter Reference

Required fields:

| Field | Rules |
|-------|-------|
| `name` | Lowercase kebab-case. Must match directory name exactly. |
| `description` | 20-600 characters. Task-focused ("Guide for creating..." not "Use this to..."). |

Optional fields that improve discoverability:

| Field | Example | Purpose |
|-------|---------|---------|
| `license` | `MIT` | License identifier |
| `complexity` | `beginner`, `intermediate`, `advanced` | Difficulty level |
| `time_to_learn` | `5min`, `30min`, `1hour`, `multi-hour` | Estimated learning time |
| `tags` | `[testing, coverage, tdd]` | Discovery keywords |
| `inputs` | `[source-code, openapi-spec]` | What the skill expects |
| `outputs` | `[test-report, documentation]` | What the skill produces |
| `side_effects` | `[creates-files, runs-commands]` | Environment changes |
| `triggers` | `[user-asks-about-testing]` | When to auto-activate |
| `complements` | `[related-skill]` | Skills that pair well |
| `tier` | `core` or `community` | Quality tier (default: `community`) |

Valid `side_effects` values: `creates-files`, `modifies-git`, `runs-commands`, `network-access`, `installs-packages`, `reads-filesystem`.

## Writing Effective Skills

**Be specific.** A skill called "Python best practices" is too broad. A skill called "python-async-patterns" that teaches structured concurrency with `asyncio.TaskGroup` is actionable.

**Show, don't tell.** Include code examples, input/output pairs, and concrete scenarios. The agent needs to know what "done" looks like.

**Declare constraints.** If the skill creates files, say so in `side_effects`. If it requires another skill first, list it in `prerequisites`. Agents use these fields to assess risk and plan execution order.

**Keep it focused.** One skill, one job. If your skill does three unrelated things, split it into three skills and link them with `complements`.

## Validation Commands

```bash
# Validate frontmatter and naming rules
python3 scripts/validate_skills.py --collection example --unique

# Regenerate multi-runtime bundles (Claude, Codex, Gemini)
python3 scripts/refresh_skill_collections.py

# Verify bundles match source
python3 scripts/validate_generated_dirs.py

# Health check a specific skill
python3 scripts/skill_health_check.py --skill your-skill-name
```

## What Happens After You Submit

1. CI runs `validate_skills.py` on your PR automatically.
2. A maintainer reviews the skill content and frontmatter.
3. Once merged, the skill is available in all supported runtimes (Claude Code, Codex, Gemini CLI).

Community-contributed skills start at `tier: community`. Skills that demonstrate broad utility and high quality may be promoted to `tier: core` over time.

## Questions?

Open an issue using the [New Skill Proposal](https://github.com/organvm-iv-taxis/a-i--skills/issues/new?template=new_skill.md) template to discuss your idea before building it, or jump straight to a PR if you already know what you want to build.
