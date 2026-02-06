---
name: skill-health
description: Run health checks on skills to verify references, scripts, and overall quality.
---

# /skill-health

Run health diagnostics on one or all skills.

## Usage

`/skill-health [skill-name]`

- Without arguments: checks all skills and shows a summary table
- With a skill name: shows detailed health for that specific skill

## Process

1. Run `python3 scripts/skill_health_check.py` (or `--skill <name>` if specified)
2. Display the results table showing:
   - Skill name and path
   - Missing references or scripts
   - SKILL.md size (lines/estimated tokens)
   - Resource counts (scripts, references, assets)
3. Highlight any issues found

## Output Format

Present results as a markdown table:

| Skill | Status | Issues | Lines | Scripts | References | Assets |
|-------|--------|--------|-------|---------|------------|--------|
| ... | ... | ... | ... | ... | ... | ... |
