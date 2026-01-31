# Troubleshooting Guide

Common issues and solutions when working with AI skills.

## Skill Discovery Issues

### Skills Not Being Applied

**Symptoms**: Agent doesn't use the expected skill for a task.

**Causes**:
1. Skill description doesn't match your request
2. Multiple skills could apply
3. Skills not loaded/installed

**Solutions**:

Be explicit about which skill to use:
```
"Using the tdd-workflow skill, help me implement this feature"
"Apply the cv-resume-builder skill to review my resume"
```

Check skill descriptions match your task:
```bash
# Search skill descriptions
grep -r "your keyword" skills/*/SKILL.md
```

### Wrong Skill Selected

**Symptoms**: Agent uses a different skill than expected.

**Solutions**:

Check for skill overlaps:
- `testing-patterns` vs `tdd-workflow` - both involve testing
- `api-design-patterns` vs `mcp-builder` - both involve API design

Specify the exact skill:
```
"Use specifically the testing-patterns skill (not tdd-workflow)"
```

## Validation Errors

### Frontmatter Validation Failed

**Symptoms**: `validate_skills.py` reports errors.

**Common Errors**:

| Error | Cause | Fix |
|-------|-------|-----|
| `missing 'name'` | No name field | Add `name:` to frontmatter |
| `name does not match directory` | Mismatch | Ensure name equals folder name |
| `name must be lowercase` | Invalid characters | Use only `a-z`, `0-9`, `-` |
| `missing 'description'` | No description | Add `description:` field |
| `description too short` | < 20 characters | Expand description |
| `description too long` | > 600 characters | Condense description |

**Fix Process**:
```bash
# Run validation
python3 scripts/validate_skills.py --collection example --unique

# Fix reported errors in SKILL.md
# Re-run validation
```

### Generated Files Out of Sync

**Symptoms**: `validate_generated_dirs.py` fails.

**Solution**:
```bash
# Regenerate all bundles
python3 scripts/refresh_skill_collections.py

# Verify
python3 scripts/validate_generated_dirs.py

# Commit the regenerated files
git add .build/
```

## Skill Content Issues

### References Not Loading

**Symptoms**: Agent doesn't find reference files mentioned in SKILL.md.

**Causes**:
1. Wrong path in SKILL.md
2. Reference file doesn't exist
3. File in wrong directory

**Solutions**:

Use relative paths from skill directory:
```markdown
<!-- Correct -->
See `references/patterns.md` for details.

<!-- Incorrect -->
See `skills/development/my-skill/references/patterns.md`
```

Verify file exists:
```bash
ls skills/development/my-skill/references/
```

### Scripts Not Executing

**Symptoms**: Skill scripts fail to run.

**Causes**:
1. Missing dependencies
2. Wrong Python version
3. Permission issues

**Solutions**:

Check dependencies:
```bash
# Check if required packages are installed
pip list | grep package-name
```

Make scripts executable:
```bash
chmod +x scripts/my_script.py
```

Use shebang:
```python
#!/usr/bin/env python3
```

## Agent-Specific Issues

### Claude Code

**Skill not recognized**:
- Ensure skill is in `~/.local/share/ai-skills/skills/` or custom location
- Restart Claude Code after adding skills

**Context too long**:
- Large skills may exceed context limits
- Move detailed content to `references/` directory
- Use progressive disclosure

### Codex

**Skills not available**:
- Check `.codex/skills/` directory exists
- Verify skill was copied correctly
- Run `python3 scripts/refresh_skill_collections.py`

### Gemini CLI

**Extension not loading**:
- Check `~/.gemini/extensions/` structure
- Verify `gemini-extension.json` is valid
- Restart Gemini CLI

## Performance Issues

### Slow Skill Loading

**Causes**:
1. Too many large reference files
2. Binary assets being loaded

**Solutions**:

Keep SKILL.md concise (< 2000 lines):
```markdown
<!-- Good: Reference external docs -->
See `references/detailed-guide.md` for complete documentation.

<!-- Bad: Include everything inline -->
[2000 lines of detailed documentation...]
```

Use lazy loading for references:
```markdown
<!-- Only load when needed -->
If you need X, read `references/x-details.md` first.
```

### Memory Issues

**Symptoms**: Agent runs out of context window.

**Solutions**:

Structure skills for progressive disclosure:
1. SKILL.md - Overview and quick start
2. references/ - Detailed documentation
3. Only load what's needed for current task

## Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| `YAML parse error` | Invalid frontmatter syntax | Check YAML formatting |
| `missing frontmatter` | No `---` delimiters | Add YAML frontmatter |
| `invalid character in name` | Name has special chars | Use lowercase + hyphens only |
| `duplicate skill names` | Two skills same name | Rename one skill |
| `file not found` | Missing reference | Create file or fix path |

## Debugging Tips

### Check Skill Structure

```bash
# Verify skill has required files
ls -la skills/category/my-skill/

# Should have at minimum:
# SKILL.md

# May also have:
# references/
# scripts/
# assets/
```

### Validate Single Skill

```bash
# Check specific skill
head -20 skills/category/my-skill/SKILL.md

# Verify frontmatter
python3 -c "
import yaml
with open('skills/category/my-skill/SKILL.md') as f:
    content = f.read()
    _, fm, _ = content.split('---', 2)
    print(yaml.safe_load(fm))
"
```

### Test Skill in Isolation

Ask the agent to use only one skill:
```
"Using ONLY the testing-patterns skill (no other skills),
explain the testing trophy concept."
```

## Getting Help

### Documentation

- [Skill Specification](../api/skill-spec.md) - Frontmatter format
- [Creating Skills](creating-skills.md) - How to create skills
- [Contributing](../CONTRIBUTING.md) - Contribution guidelines

### Reporting Issues

When reporting issues, include:

1. **Skill name** and **category**
2. **Error message** (exact text)
3. **Steps to reproduce**
4. **Expected behavior**
5. **Agent being used** (Claude Code, Codex, etc.)

Open issues at: https://github.com/anthropics/ai-skills/issues
