# Skill Specification

This document defines the format and requirements for AI agent skills.

## File Structure

Every skill must have this minimal structure:

```
skill-name/
└── SKILL.md          # Required: main skill file
```

Optional directories:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: supporting documentation
└── assets/           # Optional: templates, images, fonts
```

## SKILL.md Format

The `SKILL.md` file consists of two parts: YAML frontmatter and Markdown content.

### YAML Frontmatter

The file must begin with YAML frontmatter delimited by `---`:

```yaml
---
name: skill-name
description: What the skill does and when to use it.
license: MIT
---
```

#### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Skill identifier. Must match the directory name exactly. |
| `description` | string | Task-focused description of what the skill does. |

#### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `license` | string | License type (e.g., `MIT`, `Apache-2.0`, `Complete terms in LICENSE.txt`) |

### Field Constraints

**name**
- Must exactly match the parent directory name
- Lowercase letters, numbers, and hyphens only
- Pattern: `^[a-z0-9-]+$`
- Examples: `tdd-workflow`, `mcp-builder`, `cv-resume-builder`

**description**
- Should describe what the skill does and when to use it
- Task-focused, not agent-focused (describe the task, not Claude)
- Use third-person phrasing: "Guide for creating..." not "Use this to create..."
- Include trigger phrases that help agents recognize when to apply the skill

**license**
- Required for skills contributed to this repository
- Use `MIT` for open-source skills
- Use `Complete terms in LICENSE.txt` if providing a separate license file

### Markdown Content

After the frontmatter, include Markdown instructions:

```markdown
---
name: example-skill
description: Example skill demonstrating the format.
license: MIT
---

# Skill Title

Brief overview of what this skill provides.

## When to Use

Describe scenarios where this skill applies.

## Process

Step-by-step workflow or instructions.

## Examples

Concrete examples showing the skill in action.
```

## Optional Directories

### scripts/

Executable code (Python, Bash, etc.) for deterministic tasks.

- Include when the same code is repeatedly needed
- Scripts may be executed without loading into context
- Use for tasks requiring deterministic reliability

Example: `scripts/rotate_pdf.py`

### references/

Documentation loaded into context as needed.

- Database schemas, API documentation
- Company policies, domain knowledge
- Detailed guides too long for SKILL.md

Keep SKILL.md lean; move detailed information to references.

### assets/

Files used in skill output (not loaded into context).

- Templates (PowerPoint, Word, etc.)
- Images, icons, fonts
- Boilerplate code directories

Example: `assets/template.pptx`

## Validation

Run the validation script to check your skill:

```bash
python3 scripts/validate_skills.py --collection example --unique
```

The validator checks:
- YAML frontmatter is present and valid
- Required fields (`name`, `description`) exist
- `name` matches the directory name
- `name` uses valid characters (lowercase alphanumeric + hyphens)

## Examples

### Minimal Skill

```yaml
---
name: simple-helper
description: A simple helper skill for basic tasks.
license: MIT
---

# Simple Helper

Instructions for the skill go here.
```

### Complete Skill

```yaml
---
name: complex-workflow
description: Guide for complex multi-step workflows requiring external tools and detailed documentation. Use when implementing enterprise-grade solutions.
license: MIT
---

# Complex Workflow Guide

## Overview

This skill provides a comprehensive framework for...

## Process

### Phase 1: Planning

1. Understand requirements
2. Review documentation in `references/`

### Phase 2: Implementation

1. Use scripts in `scripts/` for automation
2. Apply templates from `assets/`

## References

See `references/detailed-guide.md` for in-depth documentation.
```

## Best Practices

1. **Be specific in descriptions** - Include trigger phrases and use cases
2. **Keep SKILL.md focused** - Move detailed docs to `references/`
3. **Use progressive disclosure** - Essential info in SKILL.md, details in references
4. **Avoid duplication** - Information should live in one place only
5. **Test with validation** - Run `validate_skills.py` before committing
