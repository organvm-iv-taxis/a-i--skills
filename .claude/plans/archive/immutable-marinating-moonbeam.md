# Plan: Universal AI Context & Skills

## Overview

1. ~~Add Serena MCP server to all AI tools~~ ✅ **COMPLETED**
2. ~~Universal AI contextualization~~ ✅ **COMPLETED**
3. **Universal Skills** - Make skills accessible across all AI tools

---

## Part 1: Serena MCP Server ✅ COMPLETED

Added to all 5 tools with appropriate context flags.

---

## Part 2: Universal AI Contextualization

### Architecture

Create a master instruction system within dotfiles that generates all tool-specific files.

```
dotfiles/
├── dot_config/
│   └── ai-context/                    # NEW: Master instruction sources
│       ├── master.md.tmpl             # Core instructions (system, code style)
│       ├── system-info.md.tmpl        # OS, shell, env (chezmoi-templated)
│       └── code-style.md.tmpl         # Language conventions
│
├── private_dot_claude/
│   └── CLAUDE.md.tmpl                 # Generated from master + Claude-specific
│
├── private_dot_gemini/
│   └── GEMINI.md.tmpl                 # Generated from master + Gemini-specific
│
├── dot_config/ai-instructions/
│   ├── cursor-rules/                  # Cursor keeps .mdc format
│   │   └── core.mdc.tmpl              # Include master content
│   └── copilot-instructions.md.tmpl   # Generated from master
│
└── private_Library/.../Claude Extensions Settings/
    └── *.json.tmpl                    # All 17 extension settings
```

### Master Instruction Content

**`dot_config/ai-context/master.md.tmpl`:**
```markdown
{{- /* Master AI Instructions - Single Source of Truth */ -}}
{{- $systemInfo := include "dot_config/ai-context/system-info.md.tmpl" | trim -}}
{{- $codeStyle := include "dot_config/ai-context/code-style.md.tmpl" | trim -}}

{{ $systemInfo }}

{{ $codeStyle }}
```

**`dot_config/ai-context/system-info.md.tmpl`:**
```markdown
## System Context

- **OS**: macOS 26 (Tahoe) Beta - ARM64 (Apple Silicon M3)
- **Shell**: zsh with Oh My Zsh
- **Package Manager**: Homebrew (`/opt/homebrew/`)
- **Dotfiles**: Managed by chezmoi at `~/dotfiles`

## Development Environment

- **Node.js**: v25.x via Homebrew
- **Python**: Anaconda at `/opt/anaconda3/`
- **Go**: Latest via Homebrew
- **Rust**: via rustup

## System Constraints

- Memory-constrained (16GB RAM); avoid spawning too many parallel processes
- Beta macOS may have GPU/WindowServer instability issues
- Dropbox and Backblaze run in background (can cause resource contention)

## Workspace

- Projects: `~/Workspace/`
- Documents: `~/Documents/`
```

**`dot_config/ai-context/code-style.md.tmpl`:**
```markdown
## Code Style Preferences

### General Principles

- Write clear, readable code over clever code
- Use descriptive names for variables, functions, classes
- Keep functions small and focused (single responsibility)
- Prefer composition over inheritance
- Don't repeat yourself (DRY), but avoid premature abstraction

### Comments & Documentation

- Comments explain "why", not "what"
- Use docstrings for public APIs
- Keep documentation up to date

### Error Handling

- Handle errors explicitly
- Provide helpful error messages
- Fail fast on invalid inputs

### Testing

- Write tests for new functionality
- Test edge cases and error conditions
- Use descriptive test names

### Git

- Commit messages: imperative mood, <72 chars for title
- Keep commits atomic and focused
- Never commit secrets or credentials

### Shell Scripts

- Use `#!/usr/bin/env bash` or `#!/usr/bin/env zsh`
- Always use `set -euo pipefail`
- Quote variables: `"$var"`
- Use `[[` over `[` for conditionals

### TypeScript/JavaScript

- Prefer `const` over `let`; avoid `var`
- Use async/await over raw Promises
- Prefer named exports over default exports
- Use TypeScript strict mode

### Python

- Follow PEP 8
- Use type hints for function signatures
- Prefer f-strings for formatting
- Use dataclasses or Pydantic for data structures
```

---

## Files to Create/Modify

### Phase 1: Master Instructions

| File | Action |
|------|--------|
| `dot_config/ai-context/master.md.tmpl` | Create |
| `dot_config/ai-context/system-info.md.tmpl` | Create |
| `dot_config/ai-context/code-style.md.tmpl` | Create |

### Phase 2: Tool-Specific Files (Include Master)

| File | Action |
|------|--------|
| `private_dot_claude/CLAUDE.md.tmpl` | Rewrite to include master |
| `private_dot_gemini/GEMINI.md.tmpl` | Rewrite to include master |
| `dot_config/ai-instructions/copilot-instructions.md.tmpl` | Rewrite to include master |
| `dot_config/ai-instructions/cursor-rules/core.mdc.tmpl` | Update to include master |

### Phase 3: Claude Desktop Extension Settings (All 17)

Create templates in `private_Library/private_Application Support/private_Claude/private_Claude Extensions Settings/`:

| Extension | Has Custom Config? |
|-----------|-------------------|
| `ant.dir.ant.anthropic.filesystem.json.tmpl` | Yes (allowed_directories) |
| `ant.dir.ant.anthropic.imessage.json.tmpl` | No |
| `ant.dir.ant.anthropic.notes.json.tmpl` | No |
| `ant.dir.ant.anthropic.chrome-control.json.tmpl` | No |
| `ant.dir.ant.anthropic.ms_office_word.json.tmpl` | No |
| `ant.dir.ant.anthropic.ms_office_excel.json.tmpl` | No |
| `ant.dir.ant.anthropic.ms_office_powerpoint.json.tmpl` | No |
| `ant.dir.ant.figma.figma.json.tmpl` | No |
| `ant.dir.domdomegg.airtable-mcp-server.json.tmpl` | Yes (API key via 1Password) |
| `ant.dir.gh.flux159.mcp-server-kubernetes.json.tmpl` | Possible (kubeconfig) |
| `ant.dir.gh.k6l3.osascript.json.tmpl` | No |
| `ant.dir.gh.k6l3.spotify.json.tmpl` | No |
| `ant.dir.gh.silverstein.pdf-filler-simple.json.tmpl` | No |
| `ant.dir.gh.socketdev.socket-mcp.json.tmpl` | Yes (API key) |
| `ant.dir.gh.tooluniverse.tooluniverse-mcp.json.tmpl` | No |
| `ant.dir.gh.wonderwhy-er.desktopcommandermcp.json.tmpl` | No |
| `context7.json.tmpl` | No |

### Phase 4: Extension Audit Script

Create `.chezmoiscripts/run_after_check-claude-extensions.sh.tmpl`:

```bash
#!/bin/bash
# Report missing Claude Desktop extensions

EXPECTED_EXTENSIONS=(
  "ant.dir.ant.anthropic.filesystem"
  "ant.dir.ant.anthropic.imessage"
  # ... full list
)

SETTINGS_DIR="$HOME/Library/Application Support/Claude/Claude Extensions Settings"

echo "Checking Claude Desktop extensions..."
missing=0

for ext in "${EXPECTED_EXTENSIONS[@]}"; do
  if [[ ! -f "$SETTINGS_DIR/${ext}.json" ]]; then
    echo "  Missing: $ext"
    ((missing++))
  fi
done

if [[ $missing -eq 0 ]]; then
  echo "All expected extensions are installed."
else
  echo ""
  echo "$missing extensions missing. Install from Claude Desktop's extension registry."
fi
```

---

## Implementation Order

1. **Create master instruction files** (3 files in `ai-context/`)
2. **Update tool instruction files** to include master (4 files)
3. **Create extension settings templates** (17 files)
4. **Create extension audit script** (1 file)

Total: ~25 files to create/modify

---

## Verification

```bash
# Apply changes
chezmoi apply --force

# Verify master instructions exist
cat ~/.config/ai-context/master.md

# Verify tool files include master content
head -50 ~/.claude/CLAUDE.md
head -50 ~/.gemini/GEMINI.md

# Verify extension settings
ls ~/Library/Application\ Support/Claude/Claude\ Extensions\ Settings/

# Run extension audit
# (runs automatically via chezmoi script)
```

---

## Part 2 Notes

- Chezmoi's `include` function requires source-relative paths
- Extension settings with secrets use 1Password injection
- `.mdc` files need YAML frontmatter preserved
- Extension installation is manual (Anthropic registry), only settings managed

---

## Part 3: Universal Skills

### Current State

**Local Claude Desktop skills** (45 skills):
`/Users/4jp/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/.../skills/`

**GitHub repo** (`ivviiviivvi/skills`): ~12 skills (Anthropic examples)

**Gap**: ~33 local skills not yet in GitHub - need to push upstream first.

### Architecture (Option 4: Separate but Coordinated)

```
Local Claude Desktop skills (45)
         │
         ▼ (one-time push to GitHub)
GitHub: ivviiviivvi/skills          ← Canonical source (portable)
         │
         ▼ (git clone/pull via chezmoi)
~/.local/share/ai-skills/           ← Local clone
         │
         ├── symlink ──▶ Claude Desktop skills location
         │
         └── referenced by ──▶ All tool configs

agent--claude-smith                 ← Can reference skills, doesn't own them
```

**Why separate repos:**
- Skills stay portable (SKILL.md works in Claude Desktop, Cursor, Gemini, etc.)
- agent--claude-smith is Claude SDK-specific orchestration
- Each repo has clear purpose
- Skills can be used by anyone; agents are personal tooling

### Skills Inventory (Local → GitHub)

**Already in GitHub** (~12): algorithmic-art, brand-guidelines, canvas-design, internal-comms, mcp-builder, skill-creator, slack-gif-creator, theme-factory, document-skills (pdf/docx/xlsx/pptx), webapp-testing, artifacts-builder

**Need to push** (~33):
- accessibility-patterns, api-design-patterns, audio-engineering-patterns
- blockchain-integration-builder, content-distribution, creative-writing-craft
- cv-resume-builder, deployment-cicd, doc-coauthoring
- enc1101-curriculum-designer, evaluation-to-growth, feedback-pedagogy
- freelance-client-ops, gcp-resource-optimizer, generative-art-algorithms
- github-repo-curator, grant-proposal-writer, interfaith-sacred-geometry
- interview-preparation, knowledge-architecture, mcp-server-orchestrator
- modular-synthesis-philosophy, narratological-algorithms, networking-outreach
- nextjs-fullstack-patterns, portfolio-presentation, product-requirements-designer
- project-orchestration, reality-tv-narrative-analyzer, testing-patterns
- three-js-interactive-builder, web-artifacts-builder, workshop-presentation-design

---

### Files to Create (Dotfiles)

| File | Purpose |
|------|---------|
| `.chezmoiscripts/run_onchange_after_sync-skills.sh.tmpl` | Clone/update skills from GitHub |
| `.chezmoiscripts/run_after_link-skills.sh.tmpl` | Symlink to Claude Desktop location |
| `dot_config/ai-skills/skill-index.md.tmpl` | Markdown skill summary for tool configs |

### Files to Modify

| File | Change |
|------|--------|
| `private_dot_claude/CLAUDE.md.tmpl` | Add skills path + available skills section |
| `private_dot_gemini/GEMINI.md.tmpl` | Add skills path reference |

---

### Phase 0: Push Local Skills to GitHub (One-Time)

Copy all local skills to GitHub repo, preserving structure:

```bash
# Clone repo locally (if not already)
cd ~/Workspace
git clone https://github.com/ivviiviivvi/skills.git skills-repo
cd skills-repo

# Copy all local skills (excluding any that already exist)
LOCAL_SKILLS="/Users/4jp/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/1ffa4db5-d1bd-4b19-92ef-8cdf8282b01d/251a1e88-094d-4d08-81ba-b4b711de7350/skills"

for skill in "$LOCAL_SKILLS"/*/; do
    name=$(basename "$skill")
    if [[ ! -d "./$name" ]]; then
        cp -r "$skill" "./$name"
        echo "Added: $name"
    fi
done

# Commit and push
git add .
git commit -m "Add local skills collection (33 skills)"
git push origin main
```

---

### Phase 1: Skills Sync Script

Create `.chezmoiscripts/run_onchange_after_sync-skills.sh.tmpl`:

```bash
#!/bin/bash
set -euo pipefail

SKILLS_DIR="${HOME}/.local/share/ai-skills"
SKILLS_REPO="https://github.com/ivviiviivvi/skills.git"

echo "Syncing AI skills..."

if [[ -d "$SKILLS_DIR/.git" ]]; then
    cd "$SKILLS_DIR"
    git fetch origin
    git reset --hard origin/main 2>/dev/null || git reset --hard origin/master
    echo "Skills updated from GitHub"
else
    mkdir -p "$(dirname "$SKILLS_DIR")"
    git clone "$SKILLS_REPO" "$SKILLS_DIR"
    echo "Skills cloned from GitHub"
fi
```

### Phase 2: Claude Desktop Symlink

Create `.chezmoiscripts/run_after_link-skills.sh.tmpl`:

```bash
#!/bin/bash
set -euo pipefail

SKILLS_SOURCE="${HOME}/.local/share/ai-skills"
CLAUDE_SKILLS_PLUGIN="${HOME}/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin"

if [[ ! -d "$SKILLS_SOURCE" ]]; then
    echo "Skills not synced yet, skipping link"
    exit 0
fi

# Find existing skills directory (UUID paths are dynamic)
SKILLS_TARGET=$(find "$CLAUDE_SKILLS_PLUGIN" -type d -name "skills" 2>/dev/null | head -1)

if [[ -n "$SKILLS_TARGET" ]]; then
    # Backup if not already a symlink
    if [[ ! -L "$SKILLS_TARGET" ]]; then
        mv "$SKILLS_TARGET" "${SKILLS_TARGET}.backup.$(date +%s)"
    fi
    ln -sfn "$SKILLS_SOURCE" "$SKILLS_TARGET"
    echo "Linked: $SKILLS_TARGET -> $SKILLS_SOURCE"
else
    echo "Claude Desktop skills directory not found (will link on next run)"
fi
```

### Phase 3: Skill Index Template

Create `dot_config/ai-skills/skill-index.md.tmpl`:

```markdown
## Available Skills

Skills extend capabilities with specialized knowledge and workflows.
Location: `~/.local/share/ai-skills/{skill-name}/`

Each skill contains:
- `SKILL.md` - Main instructions (read first)
- `scripts/` - Executable utilities (optional)
- `references/` - Detailed docs (optional)
- `assets/` - Templates/resources (optional)

**Document Skills**: pdf, docx, xlsx, pptx
**Builder Skills**: mcp-builder, skill-creator, artifacts-builder
**Design Skills**: canvas-design, theme-factory, algorithmic-art
**Enterprise Skills**: internal-comms, webapp-testing, brand-guidelines
```

### Phase 4: Update Tool Configs

**CLAUDE.md.tmpl** - Add after Claude-Specific section:

```markdown
## Skills

{{- $skillIndex := include "dot_config/ai-skills/skill-index.md.tmpl" }}
{{ $skillIndex }}
```

**GEMINI.md.tmpl** - Add at end:

```markdown
## Skills

Specialized skills available at `~/.local/share/ai-skills/`.
Each skill has SKILL.md with instructions plus optional scripts, references, assets.
```

---

## Implementation Order

**Phase 0: Push local skills to GitHub** (one-time)
1. Copy ~33 local-only skills to ivviiviivvi/skills repo
2. Commit and push to GitHub

**Phase 1-4: Dotfiles setup**
3. Create skills sync script (clone GitHub repo)
4. Create Claude Desktop symlink script
5. Create skill index template
6. Update CLAUDE.md.tmpl with skills section
7. Update GEMINI.md.tmpl with skills reference
8. Run `chezmoi apply`

Total: 3 new files, 2 modified files + GitHub repo update

---

## Verification

```bash
# Phase 0: Verify GitHub has all skills
gh api repos/ivviiviivvi/skills/contents --jq '.[].name' | wc -l
# Should show ~45+ items

# Phase 1-4: Apply dotfiles
chezmoi apply

# Verify skills cloned locally
ls ~/.local/share/ai-skills/ | wc -l
# Should show 45 skills

# Verify Claude Desktop symlink
ls -la ~/Library/Application\ Support/Claude/local-agent-mode-sessions/skills-plugin/*/skills
# Should point to ~/.local/share/ai-skills

# Verify CLAUDE.md has skills section
grep -A10 "## Skills" ~/.claude/CLAUDE.md

# Test skill access (in Claude Code)
# Ask: "Read the pdf skill and summarize what it does"

# Test skill access (in Claude Desktop)
# Skills should appear in native skills UI
```

---

## Notes

- **Option 4 approach**: Skills and agents stay in separate repos
- Skills sync runs on chezmoi apply (onchange trigger)
- Symlink preserves Claude Desktop's native skills access
- GitHub `ivviiviivvi/skills` is single source of truth for portable skills
- `agent--claude-smith` can reference skills but doesn't own them
- Tools reference skills by path (no content duplication in configs)
- SKILL.md format stays Anthropic-compatible for ecosystem portability
- Future: agent--claude-smith could have skill-invoking agents that read from `~/.local/share/ai-skills/`
