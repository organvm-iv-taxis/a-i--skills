# Activation Conditions Specification

**Version**: 1.1
**Status**: Stable

This document defines the syntax and semantics of the `triggers` field in `SKILL.md` frontmatter. Triggers are advisory hints that help agents decide when to activate a skill.

## Overview

The `triggers` field is an optional list of strings in the YAML frontmatter. Each string describes a condition under which the skill is relevant. When any trigger matches the current context, the agent may activate the skill.

```yaml
---
name: testing-patterns
description: Patterns for writing effective tests across frameworks.
triggers:
  - user-asks-about-testing
  - project-has-jest-config-js
  - file-type:*.test.ts
  - command:test
  - context:debugging
---
```

Triggers use **OR logic**: if any single trigger matches, the skill is considered relevant. An agent is not required to activate a skill just because a trigger matches -- triggers are one input among potentially many heuristics.

## Trigger Types

There are five trigger types. Each is identified by its prefix or structure.

### 1. `user-asks-about-<topic>`

Matches when the user's message contains keywords related to the topic.

**Syntax**:

```
user-asks-about-<topic>
```

Where `<topic>` is a lowercase, hyphen-separated keyword phrase.

**Regex**:

```
^user-asks-about-[a-z0-9]+(-[a-z0-9]+)*$
```

**Semantics**: The agent should match the topic against the user's input using keyword or semantic similarity. The topic string is not a literal substring match; it is a hint. For example, `user-asks-about-api-design` should match user messages like "how should I structure my REST endpoints" even though the exact phrase "api design" does not appear.

**Examples**:

```yaml
triggers:
  - user-asks-about-testing
  - user-asks-about-mcp-servers
  - user-asks-about-resume-writing
  - user-asks-about-git-workflow
```

### 2. `project-has-<pattern>`

Matches when the project workspace contains a file or directory matching the pattern.

**Syntax**:

```
project-has-<filename-pattern>
```

Where `<filename-pattern>` is a lowercase, hyphen-separated representation of a filename. Dots in filenames are replaced with hyphens in the trigger string.

**Regex**:

```
^project-has-[a-z0-9]+(-[a-z0-9]+)*$
```

**Semantics**: The agent checks whether the project root (or workspace) contains the referenced file. The filename is reconstructed from the pattern by converting hyphens back to dots where appropriate. Agents should use reasonable heuristics for this reconstruction:

| Trigger | Expected file |
|---------|---------------|
| `project-has-package-json` | `package.json` |
| `project-has-dockerfile` | `Dockerfile` |
| `project-has-pyproject-toml` | `pyproject.toml` |
| `project-has-jest-config-js` | `jest.config.js` |
| `project-has-openapi-yaml` | `openapi.yaml` |
| `project-has-cargo-toml` | `Cargo.toml` |
| `project-has-makefile` | `Makefile` |

**Examples**:

```yaml
# Activate for Node.js projects
triggers:
  - project-has-package-json

# Activate for Python projects
triggers:
  - project-has-pyproject-toml
  - project-has-setup-py

# Activate for containerized projects
triggers:
  - project-has-dockerfile
  - project-has-docker-compose-yml
```

### 3. `file-type:<glob>`

Matches when the user is working with a file whose path matches the glob pattern.

**Syntax**:

```
file-type:<glob-pattern>
```

Where `<glob-pattern>` is a standard file glob using `*` and `**` wildcards.

**Regex**:

```
^file-type:[^\s]+$
```

**Semantics**: The agent evaluates the glob against the currently active file, recently mentioned files, or files the user is asking about. The glob follows standard rules: `*` matches any characters except path separators, `**` matches across directories.

**Examples**:

```yaml
# Activate for test files
triggers:
  - file-type:*.test.ts
  - file-type:*.test.js
  - file-type:*.spec.py

# Activate for configuration files
triggers:
  - file-type:*.config.ts
  - file-type:*.config.js

# Activate for specific directories
triggers:
  - file-type:migrations/*.sql
  - file-type:**/templates/*.html
```

### 4. `command:<command>`

Matches when the user invokes a slash command or explicit action keyword.

**Syntax**:

```
command:<command-name>
```

Where `<command-name>` is a lowercase alphanumeric string with optional hyphens.

**Regex**:

```
^command:[a-z0-9]+(-[a-z0-9]+)*$
```

**Semantics**: The agent matches this trigger when the user types a slash command (e.g., `/test`, `/deploy`) or uses an equivalent invocation. The command name does not include the leading slash.

**Examples**:

```yaml
# Activate on /test command
triggers:
  - command:test

# Activate on deployment commands
triggers:
  - command:deploy
  - command:release

# Activate on documentation commands
triggers:
  - command:docs
  - command:readme
```

### 5. `context:<keyword>`

Matches when the conversation context suggests a particular activity or phase.

**Syntax**:

```
context:<keyword>
```

Where `<keyword>` is a lowercase alphanumeric string with optional hyphens.

**Regex**:

```
^context:[a-z0-9]+(-[a-z0-9]+)*$
```

**Semantics**: Context triggers match against the inferred state of the conversation rather than a single message. The agent determines context from the recent conversation history, the type of work being done, or explicit mode indicators. Common contexts include phases of development, problem-solving activities, or workflow stages.

**Examples**:

```yaml
# Activate during debugging sessions
triggers:
  - context:debugging
  - context:troubleshooting

# Activate during code review
triggers:
  - context:code-review
  - context:refactoring

# Activate during planning phases
triggers:
  - context:architecture
  - context:design-review
```

## Processing Rules

### Matching

1. **OR logic**: A skill is considered relevant if any one of its triggers matches the current context.
2. **Case insensitivity**: Trigger matching should be case-insensitive. The trigger strings themselves are stored in lowercase.
3. **Partial matching**: For `user-asks-about` triggers, agents should use semantic or fuzzy matching, not exact substring matching.
4. **Multiple skills**: When multiple skills have matching triggers, agents should rank them by relevance and may activate more than one.

### Precedence

Triggers do not define a priority order. If an agent needs to choose between multiple matching skills, it should consider:

1. The specificity of the match (a `file-type:*.test.ts` match is more specific than `user-asks-about-testing`).
2. The number of matching triggers for each skill.
3. The user's explicit intent as expressed in their message.
4. Any agent-specific ranking heuristics.

### Absence of triggers

If a skill has no `triggers` field (or an empty list), the agent falls back to matching based on the `name`, `description`, and `tags` fields. Skills without triggers are not excluded from activation.

## Complete Examples

### Testing skill

```yaml
---
name: testing-patterns
description: >
  Patterns and strategies for writing effective tests including unit tests,
  integration tests, and end-to-end tests. Use when writing or improving tests.
license: MIT
complexity: intermediate
tags:
  - testing
  - tdd
  - jest
  - pytest
triggers:
  - user-asks-about-testing
  - user-asks-about-tdd
  - project-has-jest-config-js
  - project-has-pytest-ini
  - file-type:*.test.ts
  - file-type:*.test.js
  - file-type:*.spec.py
  - file-type:*_test.go
  - command:test
  - context:debugging
---
```

### Deployment skill

```yaml
---
name: deployment-cicd
description: >
  CI/CD pipeline patterns and deployment strategies for production systems.
  Use when setting up or improving deployment workflows.
license: MIT
complexity: advanced
tags:
  - deployment
  - cicd
  - github-actions
  - docker
triggers:
  - user-asks-about-deployment
  - user-asks-about-cicd
  - project-has-dockerfile
  - project-has-docker-compose-yml
  - file-type:.github/workflows/*.yml
  - command:deploy
  - command:release
  - context:deployment
---
```

### Canvas design skill

```yaml
---
name: canvas-design
description: >
  Create visual designs using HTML Canvas API with a curated font library.
  Use when generating illustrations, diagrams, or visual compositions.
license: MIT
complexity: intermediate
tags:
  - design
  - canvas
  - visual
triggers:
  - user-asks-about-design
  - user-asks-about-illustration
  - command:design
  - context:visual-design
---
```

## Advisory Nature of Triggers

Triggers are advisory. They are intended to improve skill discovery but do not create hard activation rules. Agents may:

- Activate a skill even when no trigger matches, if the agent determines the skill is relevant through other means (description matching, user history, etc.).
- Decline to activate a skill even when a trigger matches, if the agent determines the skill is not appropriate for the current task.
- Combine trigger signals with other heuristics such as conversation topic classification, user preferences, or skill usage history.

Skill authors should write triggers that are specific enough to be useful but should not rely on triggers as the sole discovery mechanism. The `description` and `tags` fields remain the primary means of skill discovery.

## Implementation Guidance

### For consuming tools

A minimal trigger evaluator:

```python
import re
from pathlib import Path

TRIGGER_PATTERNS = {
    "user-asks-about": re.compile(r"^user-asks-about-(.+)$"),
    "project-has": re.compile(r"^project-has-(.+)$"),
    "file-type": re.compile(r"^file-type:(.+)$"),
    "command": re.compile(r"^command:(.+)$"),
    "context": re.compile(r"^context:(.+)$"),
}


def evaluate_trigger(trigger: str, context: dict) -> bool:
    """Evaluate a single trigger against the current context.

    The context dict may contain:
      - user_message: str
      - project_root: Path
      - active_file: str
      - command: str or None
      - conversation_context: list[str]
    """
    for kind, pattern in TRIGGER_PATTERNS.items():
        match = pattern.match(trigger)
        if not match:
            continue
        value = match.group(1)

        if kind == "user-asks-about":
            keywords = value.replace("-", " ").split()
            msg = context.get("user_message", "").lower()
            return any(kw in msg for kw in keywords)

        if kind == "project-has":
            root = context.get("project_root")
            if not root:
                return False
            # Reconstruct filename: hyphens to dots for known extensions
            filename = _reconstruct_filename(value)
            return (root / filename).exists()

        if kind == "file-type":
            active = context.get("active_file", "")
            return Path(active).match(value)

        if kind == "command":
            return context.get("command") == value

        if kind == "context":
            ctx_keywords = context.get("conversation_context", [])
            return value in ctx_keywords

    return False


def _reconstruct_filename(pattern: str) -> str:
    """Convert trigger pattern back to a filename.

    Heuristic: the last hyphen-separated segment that looks like a file
    extension (json, toml, yaml, yml, js, ts, py, etc.) is joined with a dot.
    """
    parts = pattern.split("-")
    extensions = {
        "json", "toml", "yaml", "yml", "js", "ts", "py", "cfg",
        "ini", "xml", "lock", "sql", "md", "txt", "sh",
    }
    # Walk from the end to find extension boundaries
    result = []
    i = len(parts) - 1
    while i >= 0:
        if parts[i] in extensions and result:
            result[-1] = parts[i] + "." + result[-1]
        else:
            result.append(parts[i])
        i -= 1
    result.reverse()
    # Capitalize known filenames
    name = "-".join(result)
    capitalizations = {"dockerfile": "Dockerfile", "makefile": "Makefile"}
    return capitalizations.get(name.lower(), name)


def check_skill_triggers(triggers: list[str], context: dict) -> bool:
    """Return True if any trigger matches (OR logic)."""
    return any(evaluate_trigger(t, context) for t in triggers)
```

### For skill authors

When writing triggers:

1. **Be specific**: Prefer `project-has-jest-config-js` over `project-has-package-json` for a testing skill.
2. **Cover multiple signals**: Include triggers from at least two different types to increase discovery reliability.
3. **Avoid over-triggering**: Do not add triggers so broad that the skill activates for unrelated tasks.
4. **Complement with tags**: Triggers and tags serve different purposes. Tags support search queries; triggers support automatic activation.
5. **Test your triggers**: Mentally walk through common user scenarios and verify that your triggers would fire when expected.
