# Persist Spec Kit Skill to GitHub + Dotfiles

## Summary

The speckit skill was created at `~/.local/share/ai-skills/speckit/` but needs to be persisted properly since the dotfiles sync script does `git reset --hard` and would overwrite it.

## Steps

### 1. Push speckit to `4444J99/a-i--skills` repo

```bash
gh repo clone 4444J99/a-i--skills /tmp/a-i--skills
cp -r ~/.local/share/ai-skills/speckit /tmp/a-i--skills/
cd /tmp/a-i--skills
git add speckit/
git commit -m "Add speckit skill for Specification-Driven Development"
git push
```

### 2. Update dotfiles sync script

Edit `dotfiles/.chezmoiscripts/run_onchange_after_sync-skills.sh.tmpl`:

```diff
- SKILLS_REPO="https://github.com/ivviiviivvi/skills.git"
+ SKILLS_REPO="https://github.com/4444J99/a-i--skills.git"
```

### 3. Update skill index

Add to `dotfiles/dot_config/ai-skills/skill-index.md.tmpl`:

```diff
  **Development Skills**: api-design-patterns, testing-patterns, deployment-cicd, nextjs-fullstack-patterns
+ **Planning Skills**: speckit
```

## Files to Modify

| File | Change |
|------|--------|
| `/tmp/a-i--skills/speckit/` | Add entire skill directory (new) |
| `dotfiles/.chezmoiscripts/run_onchange_after_sync-skills.sh.tmpl` | Update SKILLS_REPO URL |
| `dotfiles/dot_config/ai-skills/skill-index.md.tmpl` | Add speckit to index |

## Verification

```bash
# After pushing to GitHub
gh repo view 4444J99/a-i--skills --web  # Verify speckit/ exists

# After chezmoi apply
ls ~/.local/share/ai-skills/speckit/SKILL.md  # Verify synced
python3 ~/.local/share/ai-skills/skill-creator/scripts/quick_validate.py ~/.local/share/ai-skills/speckit
```
