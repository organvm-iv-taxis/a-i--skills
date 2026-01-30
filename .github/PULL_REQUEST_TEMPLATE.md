# Pull Request

## Description

Brief description of what this PR does.

## Type of Change

- [ ] New skill
- [ ] Bug fix in existing skill
- [ ] Enhancement to existing skill
- [ ] Documentation update
- [ ] Infrastructure/tooling change
- [ ] Other (please describe):

## Related Issue

Closes #(issue number)

## Changes Made

- Change 1
- Change 2
- Change 3

## Checklist

### For All PRs
- [ ] Code follows the repository's style guidelines
- [ ] Self-review of changes completed
- [ ] Comments added for complex/non-obvious code
- [ ] Documentation updated (if applicable)
- [ ] No breaking changes (or breaking changes documented)

### For New Skills
- [ ] Skill directory name is lowercase kebab-case
- [ ] `SKILL.md` file exists with valid YAML frontmatter
- [ ] `name` in frontmatter matches directory name exactly
- [ ] `description` is clear and task-focused
- [ ] No secrets or sensitive data in skill files
- [ ] Scripts are executable (if applicable)
- [ ] README added to scripts/ if they need explanation
- [ ] External assets credited in THIRD_PARTY_NOTICES.md (if applicable)

### For Skill Modifications
- [ ] Tested with relevant AI agent (Claude Code, Codex, etc.)
- [ ] Backward compatible (or breaking changes documented)
- [ ] Examples/usage updated if behavior changed

### Validation
- [ ] `python3 scripts/validate_skills.py --collection example --unique` passes
- [ ] `python3 scripts/refresh_skill_collections.py` executed
- [ ] Generated directories included in PR

## Testing

How was this tested?

- [ ] Manual testing with Claude Code
- [ ] Tested specific scenarios:
  - Scenario 1: ...
  - Scenario 2: ...
- [ ] Validated with scripts

## Screenshots (if applicable)

Add screenshots of the skill in action, terminal output, or UI changes.

## Additional Notes

Any additional information reviewers should know.
