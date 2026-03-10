# Plan: Register AI Skills with Claude Code, Codex, and Gemini

## Problem Summary

Skills exist at `/Users/4jp/.local/share/ai-skills` (95 example skills + 4 document skills) but none of the AI coding assistants are discovering or loading them.

**Current State:**
- Skills repository is properly structured with SKILL.md files
- Build artifacts exist for all three platforms in `.build/`
- CLAUDE.md documents the skills but Claude Code doesn't auto-load them
- Gemini CLI has 0 extensions installed
- Codex has no config file and no built-in skill discovery

---

## Solution by Platform

### 1. Claude Code (CLI)

**Issue:** Claude Code doesn't have a `/plugin` command like Claude Desktop. Skills in CLAUDE.md are informational only.

**Solution:** Use Claude Code's custom instructions system via `settings.json` or project-level CLAUDE.md files to make skills actionable.

**Implementation:**
1. Update `~/.claude/CLAUDE.md` to include explicit skill invocation instructions
2. Add a skill loader hook that injects skill context when invoked via `/skill-name`
3. Alternative: Create slash command aliases in settings that read SKILL.md files

**Files to modify:**
- `/Users/4jp/.claude/CLAUDE.md` - Add skill invocation patterns
- `/Users/4jp/.claude/settings.json` - Add hooks for skill loading (optional)

---

### 2. Gemini CLI

**Issue:** Extension bundles exist but aren't installed.

**Solution:** Install the pre-built Gemini extensions.

**Commands:**
```bash
cd /Users/4jp/.local/share/ai-skills
gemini extensions install ./.build/extensions/gemini/example-skills
gemini extensions install ./.build/extensions/gemini/document-skills
```

**Verification:**
```bash
gemini extensions list
```

---

### 3. Codex (OpenAI)

**Issue:** Codex looks for skills in repo-local `.codex/` directories, not a global location.

**Solution Options:**
1. **Symlink approach**: Create `~/.codex/skills/` pointing to the skills
2. **CODEX_INSTRUCTIONS approach**: Use `codex.md` or instructions file to reference skills
3. **Per-project**: Symlink `.codex/skills` in each project to the global skills

**Recommended:** Create global Codex instructions file referencing the skills path.

**Files to create/modify:**
- `~/.codex/instructions.md` - Global instructions referencing skills location
- Or use `CODEX.md` in working directories

---

## Implementation Steps

### Step 1: Gemini CLI Extensions (Quick Win)
```bash
cd /Users/4jp/.local/share/ai-skills
gemini extensions install ./.build/extensions/gemini/example-skills
gemini extensions install ./.build/extensions/gemini/document-skills
```

### Step 2: Claude Code Enhancement
Update `~/.claude/CLAUDE.md` to add actionable skill patterns:

```markdown
## Skill Invocation

When the user mentions a skill by name (e.g., "use pdf skill", "/pdf"), read the corresponding SKILL.md:
- Path pattern: `~/.local/share/ai-skills/skills/{category}/{skill-name}/SKILL.md`
- Document skills: `~/.local/share/ai-skills/document-skills/{skill-name}/SKILL.md`
- Follow the instructions in the SKILL.md file to complete the task
```

### Step 3: Codex Configuration
Create `~/.codex/instructions.md`:

```markdown
# Codex Instructions

## Available Skills
Skills are located at: ~/.local/share/ai-skills/

To use a skill, read its SKILL.md file:
- Example skills: ~/.local/share/ai-skills/skills/{category}/{skill-name}/SKILL.md
- Document skills: ~/.local/share/ai-skills/document-skills/{name}/SKILL.md
```

---

## Verification Plan

1. **Gemini:** Run `gemini extensions list` - should show 2 extensions
2. **Claude Code:** Ask "use the pdf skill to..." - should read and follow SKILL.md
3. **Codex:** Ask "list available skills" - should reference the skills directory

---

## Files Summary

| Action | File |
|--------|------|
| Edit | `/Users/4jp/.claude/CLAUDE.md` |
| Create | `/Users/4jp/.codex/instructions.md` |
| Run | Gemini extension install commands |

---

## Decisions Made

- **Codex:** Global `~/.codex/instructions.md` approach
- **Claude Code:** Updated CLAUDE.md instructions approach
