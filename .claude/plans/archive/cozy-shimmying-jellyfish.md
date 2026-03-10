# Remove Redundant Skills Marketplace Clone

## Context

The `/plugin marketplace add file:///Users/4jp/Workspace/a-i--skills` command cloned the entire skills repo (70MB) into Claude Code's internal plugin storage at `~/.claude/plugins/marketplaces/anthropic-agent-skills/`. This is redundant because the skill-index in CLAUDE.md already points directly to the workspace source at `~/Workspace/a-i--skills/skills/`. The marketplace copy contains only a git clone + generated build artifacts — nothing unique.

## What exists

- `~/.claude/plugins/marketplaces/anthropic-agent-skills/` — 70MB clone (identical to workspace, plus `.build/` artifacts)
- `~/.claude/plugins/known_marketplaces.json` — registry entry pointing to the clone
- `~/.claude/plugins/install-counts-cache.json` — generic cache, not tied to this marketplace

## Steps

1. **Delete the marketplace clone**
   ```
   rm -rf ~/.claude/plugins/marketplaces/anthropic-agent-skills/
   ```

2. **Clean up the registry** — remove the `anthropic-agent-skills` entry from `~/.claude/plugins/known_marketplaces.json` (will become `{}`)

3. **Verify** nothing breaks:
   - Skills still discoverable via CLAUDE.md skill-index (path: `~/Workspace/a-i--skills/skills/{category}/{skill-name}/`)
   - No dangling references in `~/.claude/plugins/`

## Files modified
- **Delete**: `~/.claude/plugins/marketplaces/anthropic-agent-skills/` (entire directory)
- **Edit**: `~/.claude/plugins/known_marketplaces.json` — remove the entry
