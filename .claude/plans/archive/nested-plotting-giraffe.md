# Enhance dotfile-systems-architect Skill

## Overview

Enhance the existing `dotfile-systems-architect` skill with comprehensive reference documents extracted from a detailed staging document. The staging document provides deep coverage of XDG compliance, bare git repositories, and cross-platform strategies.

**Source:** `staging/Dotfile Management via GitHub.md` (500+ lines)
**Target:** `skills/development/dotfile-systems-architect/`

---

## Current State

**SKILL.md (56 lines)** - Concise, well-structured with:
- Core philosophies (Minimal Root, Bare Git, XDG Shims)
- Basic instructions for shell, hostile apps, secrets
- Migration plan outline
- Good persona/tone

**references/dotfile-patterns.md** - **CONFLICTS with SKILL.md**
- Advocates traditional `~/.dotfiles` + GNU Stow
- Doesn't align with Bare Git + XDG philosophy
- Should be replaced or significantly revised

---

## Proposed Reference Documents

Extract content from staging document into focused references:

### 1. `references/xdg-specification.md` (NEW)
Content from staging Sections 2.1-2.2:
- XDG variables table (CONFIG_HOME, DATA_HOME, CACHE_HOME, STATE_HOME, RUNTIME_DIR)
- Backup policies per directory type
- Compliance landscape (compliant, partial, non-compliant apps)
- Shim strategy overview

### 2. `references/bare-git-setup.md` (NEW)
Content from staging Section 3.1:
- Bare repository mechanism explained
- Step-by-step implementation guide
- The `status.showUntrackedFiles no` linchpin
- Comparison table: Bare Repo vs Stow vs Chezmoi
- When to use each approach

### 3. `references/shell-bootstrap.md` (NEW)
Content from staging Section 4:
- The immutable `~/.zshenv` strategy
- Full bootstrap file template
- ZDOTDIR redirection
- Bash compatibility shims
- Moving .zsh_history to STATE_HOME

### 4. `references/app-configurations.md` (NEW)
Content from staging Section 5:
- VS Code: extensions directory, settings.json symlinks
- Claude: Desktop and CLI config locations
- AWS CLI: environment variables
- Kubernetes: KUBECONFIG
- Cross-platform path differences

### 5. `references/secrets-management.md` (NEW)
Content from staging Section 6:
- Private repository strategy
- git-crypt setup and workflow
- SOPS alternative
- 1Password/Bitwarden + direnv runtime injection
- What NOT to commit

### 6. `references/cross-platform.md` (NEW)
Content from staging Section 7:
- macOS ~/Library challenges
- Symlink strategies for GUI apps
- Windows/WSL considerations
- When Chezmoi is the better choice

### 7. `references/migration-guide.md` (NEW)
Content from staging Section 10:
- Phase 1: Audit and backup
- Phase 2: Create XDG skeleton
- Phase 3: Move and shim
- Phase 4: Commit and push
- Restore on new machine

### 8. `references/dotfile-patterns.md` (REPLACE)
Rewrite to align with XDG philosophy:
- Remove Stow-centric content
- Focus on file organization within `.config/`
- Common aliases, git config, etc. (keep useful parts)

---

## Updated SKILL.md

Minor enhancements:
- Add reference links in instructions
- Add `complexity: intermediate` and `time_to_learn: 1hour` to frontmatter
- Add `tags: [dotfiles, xdg, git, configuration, cross-platform]`

---

## Files to Create/Modify

| File | Action | Source Section |
|------|--------|----------------|
| `references/xdg-specification.md` | Create | §2 |
| `references/bare-git-setup.md` | Create | §3 |
| `references/shell-bootstrap.md` | Create | §4 |
| `references/app-configurations.md` | Create | §5 |
| `references/secrets-management.md` | Create | §6 |
| `references/cross-platform.md` | Create | §7 |
| `references/migration-guide.md` | Create | §10 |
| `references/dotfile-patterns.md` | Replace | Keep useful, align with XDG |
| `SKILL.md` | Update | Add frontmatter fields, reference links |

**Total: 7 new files, 2 modified files**

---

## Implementation Steps

### Phase 1: Create Reference Documents
Write each reference file, extracting and adapting content from staging document:

1. `xdg-specification.md` - XDG variables, compliance landscape
2. `bare-git-setup.md` - Bare repo mechanism, comparison table
3. `shell-bootstrap.md` - ~/.zshenv strategy, templates
4. `app-configurations.md` - VS Code, Claude, AWS, Kube configs
5. `secrets-management.md` - git-crypt, 1Password+direnv
6. `cross-platform.md` - macOS/Linux/Windows strategies
7. `migration-guide.md` - Step-by-step transition plan

### Phase 2: Replace dotfile-patterns.md
Rewrite to align with XDG philosophy, keeping useful patterns like:
- Common aliases
- Git configuration
- Modular shell setup

### Phase 3: Update SKILL.md
Add optional frontmatter fields and reference links:
```yaml
complexity: intermediate
time_to_learn: 1hour
tags: [dotfiles, xdg, git, configuration, cross-platform]
```

### Phase 4: Validate and Bundle
```bash
python3 scripts/validate_skills.py --collection example --unique
python3 scripts/refresh_skill_collections.py
python3 scripts/validate_generated_dirs.py
```

### Phase 5: Clean Up
- Delete or archive staging document
- Commit changes

---

## Verification

1. Run validation script - should pass
2. Verify SKILL.md backtick references exist as files
3. Check reference content is comprehensive but not redundant
4. Confirm all XDG terminology is consistent across files
5. Bundle regeneration succeeds

---

## Key Decisions

1. **Enhance existing skill** rather than create duplicate
2. **Replace conflicting reference** to maintain philosophical consistency
3. **Extract focused references** rather than one massive document
4. **Keep SKILL.md concise** - references hold the depth
5. **Archive staging document** after extraction complete
