# Consolidate a-i--skills to Single Canonical Path

## Context

The `a-i--skills` repo exists in **two separate clones** with different remotes and diverged histories:

| Location | Remote | HEAD | Tools Using It |
|----------|--------|------|----------------|
| `~/Workspace/a-i--skills/` | `4444J99/a-i--skills` (personal fork) | `f0bcfcf` | **Claude** (via `~/.claude/skills/` symlink → `.build/claude/skills/`) |
| `~/Workspace/organvm-iv-taxis/a-i--skills/` | `organvm-iv-taxis/a-i--skills` (org repo) | `88455a2` (4 commits ahead) | **Codex** (via `AGENTS.md`) |

Additionally, **Gemini CLI** points to `~/.local/share/ai-skills/.build/extensions/gemini/` which **doesn't exist** — completely broken.

The org copy is the canonical one (correct organ directory, more up-to-date, has GEMINI.md + AGENTS.md). The workspace-root copy is a stale personal fork.

**Goal:** Make `~/Workspace/organvm-iv-taxis/a-i--skills/` the single source of truth for all three tools.

## Plan

### Step 1: Migrate the GitHub MCP policy from the stale copy

The previous task added a `## GitHub MCP Usage Policy` section to `~/Workspace/a-i--skills/CLAUDE.md`. The org copy at `~/Workspace/organvm-iv-taxis/a-i--skills/CLAUDE.md` doesn't have it yet. Add it there.

**File:** `/Users/4jp/Workspace/organvm-iv-taxis/a-i--skills/CLAUDE.md`

### Step 2: Rebuild Claude skills from the canonical copy

The `~/.claude/skills/` symlink currently points to:
```
~/Workspace/a-i--skills/.build/claude/skills/
```

Update it to point to:
```
~/Workspace/organvm-iv-taxis/a-i--skills/.build/claude/skills/
```

First, regenerate the `.build/` artifacts in the org copy (they may be stale):
```bash
cd ~/Workspace/organvm-iv-taxis/a-i--skills
python3 scripts/refresh_skill_collections.py
```

Then update the symlink:
```bash
rm ~/.claude/skills
ln -s ~/Workspace/organvm-iv-taxis/a-i--skills/.build/claude/skills ~/.claude/skills
```

### Step 3: Fix Gemini CLI extensions

Gemini's install metadata points to `~/.local/share/ai-skills/` (doesn't exist). Re-install from the canonical copy:

```bash
# Remove stale extension registrations
rm -rf ~/.local/share/gemini/extensions/example-skills
rm -rf ~/.local/share/gemini/extensions/document-skills

# Re-install from canonical location
gemini extensions install ~/Workspace/organvm-iv-taxis/a-i--skills/.build/extensions/gemini/example-skills
gemini extensions install ~/Workspace/organvm-iv-taxis/a-i--skills/.build/extensions/gemini/document-skills
```

If `gemini extensions install` isn't available, manually create the symlinks/copies and update `.gemini-extension-install.json` to point to the new path.

### Step 4: Update global CLAUDE.md skills path

**File:** `/Users/4jp/.claude/CLAUDE.md`

Change the skills location line from:
```
Location: ~/Workspace/a-i--skills/skills/{category}/{skill-name}/
```
To:
```
Location: ~/Workspace/organvm-iv-taxis/a-i--skills/skills/{category}/{skill-name}/
```

### Step 5: Update workspace CLAUDE.md reference (if any)

Check `/Users/4jp/Workspace/CLAUDE.md` for references to `~/Workspace/a-i--skills` and update to `~/Workspace/organvm-iv-taxis/a-i--skills`.

### Step 6: Remove the stale workspace-root clone

```bash
rm -rf ~/Workspace/a-i--skills
```

This is safe because:
- The org copy has all its commits plus 4 more
- The only unique content was the GitHub MCP policy section added to CLAUDE.md (migrated in Step 1)
- No other tools reference this path after Steps 2-5

### Step 7: Update auto-memory

**File:** `/Users/4jp/.claude/projects/-Users-4jp/memory/MEMORY.md`

Add a note about the consolidation so future sessions know the canonical path.

## Files to Modify

1. `/Users/4jp/Workspace/organvm-iv-taxis/a-i--skills/CLAUDE.md` — add GitHub MCP policy section
2. `~/.claude/skills` — update symlink target
3. `~/.local/share/gemini/extensions/example-skills/.gemini-extension-install.json` — fix source path
4. `~/.local/share/gemini/extensions/document-skills/.gemini-extension-install.json` — fix source path
5. `/Users/4jp/.claude/CLAUDE.md` — update skills Location path
6. `/Users/4jp/Workspace/CLAUDE.md` — update any a-i--skills references
7. `/Users/4jp/.claude/projects/-Users-4jp/memory/MEMORY.md` — add consolidation note
8. `~/Workspace/a-i--skills/` — delete after migration

## Verification

1. After symlink update: `ls ~/.claude/skills/algorithmic-art/SKILL.md` should resolve
2. After Gemini fix: `cat ~/.local/share/gemini/extensions/example-skills/.gemini-extension-install.json` should show the organvm-iv-taxis path
3. Start a new Claude Code session — skills list in system prompt should still load correctly
4. Run `python3 ~/Workspace/organvm-iv-taxis/a-i--skills/scripts/validate_generated_dirs.py` to confirm build artifacts are in sync
5. Confirm `~/Workspace/a-i--skills` no longer exists
