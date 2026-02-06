# Federation Schema Specification

**Version**: 1.1
**Status**: Stable

This document defines the federation protocol that allows third-party skill repositories to be compatible with agents and tooling that consume the AI Skills format.

## Introduction

Federation enables skill repositories maintained by different authors to be discovered, validated, and consumed by any agent or tool that implements this specification. A federated repository does not need to be part of the official `ai-skills` collection. It only needs to follow the directory structure, frontmatter format, and naming conventions defined here.

The goals of federation are:

1. **Interoperability** -- Skills authored in any repository work with any compatible agent.
2. **Discoverability** -- Agents can enumerate skills from a repository without prior knowledge of its contents.
3. **Validation** -- Third parties can verify their skills conform to the specification before publishing.

## Directory Structure

A federated repository contains one or more skill directories. Each skill directory must contain a `SKILL.md` file.

### Minimal structure

```
my-repo/
  skills/
    my-skill/
      SKILL.md
```

### Full structure

```
my-repo/
  skills/
    my-skill/
      SKILL.md          # Required: metadata + instructions
      scripts/          # Optional: executable code
      references/       # Optional: supporting documentation
      assets/           # Optional: templates, images, fonts
```

The top-level directory name (`skills/` above) is not prescribed. Consumers locate skills by searching for `SKILL.md` files recursively, so any nesting scheme is valid.

Skill directories may be organized into category subdirectories:

```
my-repo/
  skills/
    development/
      api-patterns/
        SKILL.md
    creative/
      pixel-art/
        SKILL.md
```

## Frontmatter Format

Every `SKILL.md` must begin with YAML frontmatter delimited by `---` on its own line:

```yaml
---
name: my-skill
description: What the skill does and when an agent should use it.
---
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Skill identifier. Must match the containing directory name exactly. Restricted to lowercase alphanumeric characters and hyphens (`^[a-z0-9-]+$`). |
| `description` | string | Task-focused description of what the skill does. Length: 20--600 characters. |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `license` | string | License identifier (e.g., `MIT`, `Apache-2.0`) or reference to a bundled file (e.g., `Complete terms in LICENSE.txt`). |
| `complexity` | string | Skill complexity level. One of: `beginner`, `intermediate`, `advanced`. |
| `time_to_learn` | string | Estimated time to become productive. One of: `5min`, `30min`, `1hour`, `multi-hour`. |
| `prerequisites` | list of strings | Skill names that should be learned first. |
| `tags` | list of strings | Searchable keywords for discovery. Lowercase, hyphen-separated. |
| `metadata` | object | Arbitrary key-value pairs for agent-specific or vendor-specific data. |
| `inputs` | list of strings | Descriptions of what the skill expects from the user or context. |
| `outputs` | list of strings | Descriptions of what the skill produces. |
| `side_effects` | list of strings | Actions the skill may take beyond generating text. Valid values: `creates-files`, `modifies-git`, `runs-commands`, `network-access`, `installs-packages`, `reads-filesystem`. |
| `triggers` | list of strings | Activation conditions that hint when an agent should apply this skill. See [activation-conditions.md](activation-conditions.md). |
| `complements` | list of strings | Skill names that pair well with this skill but are not prerequisites. |
| `includes` | list of strings | Paths to files or directories bundled with the skill (relative to the skill directory). |
| `tier` | string | Distribution tier. One of: `core`, `community`. |

### Example: Full Frontmatter

```yaml
---
name: api-design-patterns
description: >
  Patterns and best practices for designing REST and GraphQL APIs.
  Use when creating new API endpoints or reviewing existing API designs.
license: MIT
complexity: intermediate
time_to_learn: 1hour
prerequisites:
  - backend-implementation-patterns
tags:
  - api
  - rest
  - graphql
  - openapi
inputs:
  - API requirements or existing endpoint specification
outputs:
  - API design document with endpoint definitions
  - OpenAPI specification file
side_effects:
  - creates-files
triggers:
  - user-asks-about-api-design
  - project-has-openapi-yaml
  - file-type:*.openapi.yaml
complements:
  - testing-patterns
  - deployment-cicd
includes:
  - references/rest-conventions.md
  - assets/templates/openapi-template.yaml
tier: community
metadata:
  category: development
  source: anthropic
---
```

## Discovery Protocol

A consuming agent or tool discovers skills by performing a recursive search for `SKILL.md` files within a repository root. The algorithm is:

1. Starting from the repository root (or a configured subdirectory), recursively glob for files named `SKILL.md`.
2. For each match, extract the YAML frontmatter.
3. Validate that the `name` field matches the parent directory name.
4. Build an in-memory index of skill name, description, tags, triggers, and directory path.

### Reference Implementation (Python)

```python
from pathlib import Path
import re

def discover_skills(root: Path) -> list[dict]:
    """Discover all skills under a repository root."""
    skills = []
    for skill_md in root.rglob("SKILL.md"):
        skill_dir = skill_md.parent
        if skill_dir == root:
            continue
        text = skill_md.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(text)
        if frontmatter.get("name") == skill_dir.name:
            skills.append({
                "name": frontmatter["name"],
                "description": frontmatter.get("description", ""),
                "tags": frontmatter.get("tags", []),
                "triggers": frontmatter.get("triggers", []),
                "path": str(skill_dir),
            })
    return sorted(skills, key=lambda s: s["name"])
```

### Frontmatter Extraction

Frontmatter is the text between the first `---` line and the next `---` line. Parse it as YAML. A minimal extractor:

```python
import yaml

def extract_frontmatter(text: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return yaml.safe_load("\n".join(lines[1:i])) or {}
    return {}
```

## Validation Rules

Third-party repositories should validate their skills before publishing. The following rules apply:

### Required checks

| Rule | Description |
|------|-------------|
| Frontmatter present | File starts with `---` and has a closing `---`. |
| `name` exists | The `name` field is present and non-empty. |
| `name` matches directory | The `name` value equals the parent directory name. |
| `name` format | Matches `^[a-z0-9-]+$`. |
| `description` exists | The `description` field is present and non-empty. |
| `description` length | Between 20 and 600 characters. |
| Unique names | No two skills in the same collection share a `name`. |

### Optional checks

| Rule | Description |
|------|-------------|
| `complexity` value | If present, must be one of `beginner`, `intermediate`, `advanced`. |
| `time_to_learn` value | If present, must be one of `5min`, `30min`, `1hour`, `multi-hour`. |
| `side_effects` values | If present, each entry must be a recognized value (see field table). |
| `tier` value | If present, must be one of `core`, `community`. |
| `prerequisites` resolution | Each prerequisite name should correspond to a skill in the same collection or a known external collection. |
| Internal links | Markdown links to local files (`[text](path)`) should resolve relative to the skill directory. |
| Reference files | Paths mentioned in backticks (`` `references/file.md` ``) should exist on disk. |

### Running Validation

```bash
# Validate all skills in a repository
python3 scripts/validate_skills.py --collection example --unique

# Include broken link detection
python3 scripts/validate_skills.py --collection example --unique --check-links
```

## Registry Format

A registry is a JSON document that catalogs all skills in a repository. It is produced by a generation script (e.g., `generate_registry.py`) and can be consumed by agents, search tools, and dashboards.

### Schema

```json
{
  "version": "1.1",
  "generated_at": "2026-02-06T12:00:00Z",
  "repository": {
    "name": "my-skill-repo",
    "url": "https://github.com/org/my-skill-repo",
    "license": "MIT"
  },
  "skills": [
    {
      "name": "api-design-patterns",
      "description": "Patterns and best practices for designing REST and GraphQL APIs.",
      "path": "skills/development/api-design-patterns",
      "license": "MIT",
      "complexity": "intermediate",
      "time_to_learn": "1hour",
      "tags": ["api", "rest", "graphql", "openapi"],
      "triggers": ["user-asks-about-api-design"],
      "prerequisites": ["backend-implementation-patterns"],
      "side_effects": ["creates-files"],
      "tier": "community",
      "has_scripts": true,
      "has_references": true,
      "has_assets": false
    }
  ],
  "categories": {
    "development": ["api-design-patterns", "backend-implementation-patterns"],
    "creative": ["algorithmic-art", "canvas-design"]
  },
  "bundles": {
    "claude": ".build/claude/skills",
    "codex": ".build/codex/skills",
    "gemini": ".build/extensions/gemini/example-skills/skills"
  }
}
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Registry schema version. |
| `generated_at` | string | ISO 8601 timestamp of generation. |
| `repository` | object | Repository metadata (name, URL, license). |
| `skills` | array | Array of skill objects. |
| `categories` | object | Map from category name to list of skill names. Categories are derived from the directory structure (e.g., `skills/development/` yields the `development` category). |
| `bundles` | object | Map from agent name to the path where pre-built skill bundles are stored. |

### Skill Object Fields

Each entry in the `skills` array corresponds to one skill directory. All frontmatter fields are included directly. Three computed fields are added:

| Field | Type | Description |
|-------|------|-------------|
| `path` | string | Relative path from repository root to the skill directory. |
| `has_scripts` | boolean | Whether a `scripts/` directory exists. |
| `has_references` | boolean | Whether a `references/` directory exists. |
| `has_assets` | boolean | Whether an `assets/` directory exists. |

## Compatibility Notes

### Version history

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-16 | Initial specification. Required fields: `name`, `description`. Optional: `license`, `metadata`. |
| 1.1 | 2026-02-06 | Added optional fields: `complexity`, `time_to_learn`, `prerequisites`, `tags`, `inputs`, `outputs`, `side_effects`, `triggers`, `complements`, `includes`, `tier`. Added registry format and discovery protocol. |

### Backward compatibility

- Skills conforming to version 1.0 are valid under version 1.1. All new fields are optional.
- Consumers should ignore frontmatter fields they do not recognize.
- The `metadata` field remains the recommended place for vendor-specific extensions that are not part of this specification.

### Agent compatibility

Different agents may support different subsets of the specification:

- **Claude Code**: Full support. Reads `SKILL.md`, `scripts/`, `references/`, `assets/`.
- **Codex**: Reads `SKILL.md` and bundled directories. Does not execute `scripts/` directly.
- **Gemini CLI**: Reads skills through the Gemini extension format. Bundled via `.build/extensions/gemini/`.

Agents that do not support a given optional field (e.g., `triggers`) should silently ignore it. The skill must still function correctly when optional fields are absent.
