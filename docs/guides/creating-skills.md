# Creating Skills

This guide walks you through creating a new skill for AI agents.

## Prerequisites

- Understanding of Markdown and YAML
- Familiarity with the task domain you're creating a skill for
- A cloned copy of this repository

## Skill Structure

Every skill is a directory containing at minimum a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: helper scripts
├── references/       # Optional: detailed documentation
└── assets/           # Optional: templates, images, fonts
```

## Step-by-Step Guide

### 1. Choose a Category

Skills are organized into category subdirectories within `skills/`. Choose the most appropriate category:

| Category | Purpose | Examples |
|----------|---------|----------|
| `creative` | Art, music, design | algorithmic-art, theme-factory |
| `data` | Data analysis, SQL | sql-query-optimizer |
| `development` | Coding patterns, tools | mcp-builder, tdd-workflow |
| `documentation` | Docs, READMEs | github-profile-architect |
| `education` | Teaching, learning | socratic-tutor |
| `integrations` | Third-party tools | specstory-* skills |
| `knowledge` | Knowledge management | second-brain-librarian |
| `professional` | Business, career | cv-resume-builder |
| `project-management` | Planning, roadmaps | github-roadmap-strategist |
| `security` | Security, compliance | gdpr-compliance-check |
| `specialized` | Niche domains | game-mechanics-designer |
| `tools` | Meta-skills | skill-creator |

### 2. Create the Directory

Create your skill directory in the appropriate category:

```bash
mkdir -p skills/development/my-new-skill
```

Use kebab-case (lowercase with hyphens) for the directory name.

### 3. Create SKILL.md

Create the main skill file with YAML frontmatter:

```markdown
---
name: my-new-skill
description: What this skill does and when to use it. Be specific about trigger phrases and use cases.
license: MIT
---

# My New Skill

Brief overview of what this skill provides.

## When to Use

- Scenario 1 where this skill applies
- Scenario 2 where this skill applies

## Process

### Step 1: Title

Instructions for step 1.

### Step 2: Title

Instructions for step 2.

## Examples

Concrete examples showing the skill in action.
```

### 4. Follow Frontmatter Rules

**name** (required)
- Must exactly match directory name
- Lowercase letters, numbers, and hyphens only
- Pattern: `^[a-z0-9-]+$`

**description** (required)
- Task-focused (describe the task, not the agent)
- Include trigger phrases for agent recognition
- Use third-person: "Guide for creating..." not "Use this to create..."

**license** (required for contributions)
- Use `MIT` for open-source skills
- Use `Complete terms in LICENSE.txt` for separate license files

### 5. Write Effective Instructions

**Be specific about when to use the skill:**
```markdown
description: Guide for creating MCP servers that enable LLMs to interact
with external services. Use when building MCP servers to integrate APIs.
```

**Provide step-by-step workflows:**
```markdown
## Process

### Phase 1: Research
1. Study the API documentation
2. Identify key endpoints

### Phase 2: Implementation
1. Set up the project structure
2. Implement tool handlers
```

**Include concrete examples:**
```markdown
## Example

When the user asks: "Help me create a Slack integration"
→ Follow Phase 1 to understand Slack's API
→ Implement message sending and receiving tools
```

### 6. Add Optional Resources

**scripts/** - For deterministic, reusable code:
```bash
mkdir skills/development/my-new-skill/scripts
```

Use when:
- The same code is repeatedly needed
- Deterministic reliability is required
- Tasks can be executed without loading into context

**references/** - For detailed documentation:
```bash
mkdir skills/development/my-new-skill/references
```

Use when:
- Documentation is too long for SKILL.md
- Information should be loaded on-demand
- Content includes schemas, API docs, or policies

**assets/** - For output resources:
```bash
mkdir skills/development/my-new-skill/assets
```

Use when:
- Templates are needed (PowerPoint, Word, etc.)
- Images, icons, or fonts are required
- Boilerplate code should be copied

### 7. Validate Your Skill

Run the validation script:

```bash
python3 scripts/validate_skills.py --collection example --unique
```

This checks:
- Frontmatter is valid YAML
- Required fields exist
- Name matches directory
- No duplicate skill names

### 8. Refresh Collections

After adding your skill, regenerate the collections:

```bash
python3 scripts/refresh_skill_collections.py
```

This updates:
- `.build/collections/example-skills.txt`
- Link directories in `.build/`
- Agent-specific bundles

### 9. Test Your Skill

1. Open Claude Code (or another AI agent)
2. Describe a task that should trigger your skill
3. Verify the agent applies your skill's patterns

## Best Practices

### Keep SKILL.md Focused

Move detailed information to `references/`:

```
# Good: Lean SKILL.md
SKILL.md (50 lines) → Core workflow
references/api-guide.md → Detailed API docs

# Bad: Bloated SKILL.md
SKILL.md (500 lines) → Everything
```

### Use Progressive Disclosure

Structure information in three levels:

1. **SKILL.md** - Essential workflow, always loaded
2. **references/** - Detailed docs, loaded on demand
3. **assets/** - Output files, never loaded into context

### Write Clear Descriptions

Good:
```yaml
description: Guide for test-driven development workflow. Use when
implementing new features with TDD or when users mention "write tests first".
```

Poor:
```yaml
description: TDD helper.
```

### Avoid Duplication

Information should exist in one place only:
- Either in SKILL.md OR in references
- Either in SKILL.md OR in scripts (as comments)

## Common Patterns

### Workflow Skills

For multi-step processes:
```markdown
## Process

### Phase 1: Planning
...

### Phase 2: Implementation
...

### Phase 3: Verification
...
```

### Reference Skills

For domain knowledge:
```markdown
## Overview

Brief context on the domain.

## Key Concepts

Definitions and explanations.

## Patterns

Common patterns with examples.
```

### Tool Integration Skills

For external tools:
```markdown
## Setup

Prerequisites and configuration.

## Usage

How to invoke the tool.

## Examples

Common use cases.
```

## Troubleshooting

**Validation fails with "name does not match directory"**
- Ensure the `name` field exactly matches the directory name
- Check for typos, case sensitivity, or extra spaces

**Skill not being detected by agent**
- Make description more specific with trigger phrases
- Include explicit "Use when..." scenarios
- Check that the skill is in the correct category

**Collections not updating**
- Run `python3 scripts/refresh_skill_collections.py`
- Verify the skill has valid frontmatter
- Check that SKILL.md exists in the directory

## Further Reading

- [Skill Format Specification](../api/skill-spec.md) - Complete spec details
- [Contributing Guide](../CONTRIBUTING.md) - Contribution process
- [skill-creator](../../skills/tools/skill-creator/SKILL.md) - The meta-skill for creating skills
