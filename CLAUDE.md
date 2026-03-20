# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the Anthropic AI Skills repository—a collection of example skills that extend Claude's capabilities. Each skill is a self-contained folder with a `SKILL.md` file containing YAML frontmatter and instructions.

Two skill collections exist:
- **Example skills**: Located in `skills/` directory, organized by category (e.g., `skills/creative/algorithmic-art/`, `skills/development/mcp-builder/`)
- **Document skills**: Reference implementations in `document-skills/` (docx, pdf, pptx, xlsx)

## Repository Structure

```
ai-skills/
├── README.md              # Repository documentation
├── CLAUDE.md              # Claude Code instructions (this file)
├── skills/                # All example skills (101), organized by category
│   ├── creative/          # Art, music, design (13 skills)
│   ├── data/              # Data analysis and ML (6 skills)
│   ├── development/       # Coding patterns and tools (26 skills, incl. bundles)
│   ├── documentation/     # Docs and GitHub profiles (4 skills)
│   ├── education/         # Teaching and learning (4 skills)
│   ├── integrations/      # Third-party integrations (9 skills)
│   ├── knowledge/         # Knowledge management (6 skills)
│   ├── professional/      # Business and career (11 skills)
│   ├── project-management/ # Planning and roadmaps (4 skills)
│   ├── security/          # Security and compliance (6 skills, incl. bundle)
│   ├── specialized/       # Niche domains (6 skills)
│   └── tools/             # Meta-skills and orchestration (6 skills)
├── document-skills/       # Reference document skills (4)
├── docs/                  # Documentation files
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   ├── ROADMAP.md
│   ├── api/               # Skill spec, federation schema, activation conditions
│   └── guides/            # Getting started, overrides, core-vs-community
├── agents/                # AI agent definitions
│   └── skill-planner.md   # Skill composition planner
├── commands/              # Slash commands
│   ├── plan-workflow.md   # /plan-workflow - generate skill chains
│   └── skill-health.md   # /skill-health - run health checks
├── scripts/               # Build and validation tools
├── staging/               # Skills in development
├── .build/                # Generated outputs (hidden)
│   ├── collections/       # Skill path lists + tier lists
│   ├── skills-registry.json  # Machine-readable skill metadata
│   ├── skills-lock.json   # Lockfile with SHA-256 hashes
│   ├── claude/            # Claude Code bundles
│   ├── codex/             # Codex bundles
│   ├── direct/            # Direct link directories
│   └── extensions/        # Gemini CLI extensions
└── .claude-plugin/        # Marketplace metadata
```

## Common Commands

```bash
# Refresh collections, registry, lockfile, and generated link directories
python3 scripts/refresh_skill_collections.py
python3 scripts/refresh_skill_collections.py --mode symlink  # Use symlinks instead of copies

# Validate skill frontmatter (run both for full validation)
python3 scripts/validate_skills.py --collection example --unique
python3 scripts/validate_skills.py --collection document --unique

# Verify generated bundles, registry, and lockfile are in sync
python3 scripts/validate_generated_dirs.py

# Run skill health checks (scripts, references, size metrics)
python3 scripts/skill_health_check.py                        # All skills
python3 scripts/skill_health_check.py --skill mcp-builder    # Single skill
python3 scripts/skill_health_check.py --json                 # JSON output

# PR validation report (for CI)
python3 scripts/pr_validation_report.py --base origin/main

# Full release workflow (bumps versions, updates changelog, commits, tags, pushes)
python3 scripts/release.py 1.2.0 \
  --change "Description" \
  --add "New feature" \
  --fix "Bug fix" \
  --commit --tag --push --release --notes-from-changelog
```

## Architecture

### Skill Structure
```
my-skill/
  SKILL.md          # Required: YAML frontmatter + markdown instructions
  scripts/          # Optional: executable helpers
  references/       # Optional: supporting documentation
  assets/           # Optional: templates, resources
```

### SKILL.md Format
```markdown
---
name: my-skill-name          # Must match folder name, lowercase + hyphens
description: What it does    # Task-focused sentence (20-600 chars)
license: MIT                 # Required: license type
# Optional semantic fields:
inputs: [source-code]        # What the skill expects
outputs: [test-report]       # What the skill produces
side_effects: [creates-files] # Environment changes
triggers: [user-asks-about-testing] # Activation conditions
complements: [verification-loop]    # Skills that pair well
includes: [skill-a, skill-b]       # Bundle: skills to install together
tier: core                          # Quality tier: core or community
---

# Instructions and content here
```

### Generated Directories (in .build/, managed by refresh script)
- `.build/collections/example-skills.txt` / `document-skills.txt` — skill path lists
- `.build/collections/core-skills.txt` / `community-skills.txt` — tier lists
- `.build/skills-registry.json` — machine-readable skill metadata (all frontmatter + resources)
- `.build/skills-lock.json` — lockfile with SHA-256 hashes per skill
- `.build/direct/example/` / `document/` — direct link directories
- `.build/codex/skills` / `.build/claude/skills` — agent-specific bundles
- `.build/extensions/gemini/*/skills` — Gemini CLI extensions

These are committed artifacts; include refreshed outputs in PRs that change skills. CI validates that generated files are up-to-date (no git diff allowed).

### Version Files (updated during releases)
- `.claude-plugin/marketplace.json` (metadata.version)
- `.build/extensions/gemini/example-skills/gemini-extension.json`
- `.build/extensions/gemini/document-skills/gemini-extension.json`

## Key Guidelines

- Skill `name` in frontmatter must exactly match the directory name
- All skills must have a `license` field (MIT for open skills)
- Skills are organized into category subdirectories; new skills must go in the appropriate category
- Document skills (docx, pdf, pptx, xlsx) are only in `document-skills/`, not in `skills/`
- No repo-wide test suite; run per-skill tests when they exist (e.g., `python3 document-skills/pdf/scripts/check_bounding_boxes_test.py`)
- Update `docs/THIRD_PARTY_NOTICES.md` when adding external assets
- CI includes secret detection for patterns like `sk-`, `ghp_`, `AKIA` in new files

## GitHub MCP Usage Policy

**IMPORTANT:** This repo exists locally. ALWAYS use local filesystem tools (Read, Grep, Glob) to read files — NEVER use `mcp__github__get_file_contents` or similar GitHub MCP tools for content that exists on disk. GitHub MCP tools trigger API content filtering errors on repos with security-domain content (security skills contain terms like STRIDE, XSS, SQL injection that trip the output filter).

Use GitHub MCP tools ONLY for operations that require the GitHub API:
- Setting repo description/topics (`update_pull_request`, etc.)
- Creating/managing issues and PRs
- Managing labels, releases, branches

For these API-only operations, always set `minimal_output: true` where the parameter is available.

<!-- ORGANVM:AUTO:START -->
## System Context (auto-generated — do not edit)

**Organ:** ORGAN-IV (Orchestration) | **Tier:** standard | **Status:** GRADUATED
**Org:** `organvm-iv-taxis` | **Repo:** `a-i--skills`

### Edges
- **Consumes** ← `organvm-iv-taxis/agent--claude-smith`: dependency

### Siblings in Orchestration
`orchestration-start-here`, `petasum-super-petasum`, `universal-node-network`, `.github`, `agentic-titan`, `agent--claude-smith`, `tool-interaction-design`, `system-governance-framework`, `reverse-engine-recursive-run`, `collective-persona-operations`

### Governance
- *Standard ORGANVM governance applies*

*Last synced: 2026-03-20T10:58:30Z*

## Session Review Protocol

At the end of each session that produces or modifies files:
1. Run `organvm session review --latest` to get a session summary
2. Check for unimplemented plans: `organvm session plans --project .`
3. Export significant sessions: `organvm session export <id> --slug <slug>`
4. Run `organvm prompts distill --dry-run` to detect uncovered operational patterns

Transcripts are on-demand (never committed):
- `organvm session transcript <id>` — conversation summary
- `organvm session transcript <id> --unabridged` — full audit trail
- `organvm session prompts <id>` — human prompts only


## Active Directives

| Scope | Phase | Name | Description |
|-------|-------|------|-------------|
| system | any | prompting-standards | Prompting Standards |
| system | any | research-standards-bibliography | APPENDIX: Research Standards Bibliography |
| system | any | phase-closing-and-forward-plan | METADOC: Phase-Closing Commemoration & Forward Attack Plan |
| system | any | research-standards | METADOC: Architectural Typology & Research Standards |
| system | any | sop-ecosystem | METADOC: SOP Ecosystem — Taxonomy, Inventory & Coverage |
| system | any | autonomous-content-syndication | SOP: Autonomous Content Syndication (The Broadcast Protocol) |
| system | any | autopoietic-systems-diagnostics | SOP: Autopoietic Systems Diagnostics (The Mirror of Eternity) |
| system | any | background-task-resilience | background-task-resilience |
| system | any | cicd-resilience-and-recovery | SOP: CI/CD Pipeline Resilience & Recovery |
| system | any | community-event-facilitation | SOP: Community Event Facilitation (The Dialectic Crucible) |
| system | any | context-window-conservation | context-window-conservation |
| system | any | conversation-to-content-pipeline | SOP — Conversation-to-Content Pipeline |
| system | any | cross-agent-handoff | SOP: Cross-Agent Session Handoff |
| system | any | cross-channel-publishing-metrics | SOP: Cross-Channel Publishing Metrics (The Echo Protocol) |
| system | any | data-migration-and-backup | SOP: Data Migration and Backup Protocol (The Memory Vault) |
| system | any | document-audit-feature-extraction | SOP: Document Audit & Feature Extraction |
| system | any | dynamic-lens-assembly | SOP: Dynamic Lens Assembly |
| system | any | essay-publishing-and-distribution | SOP: Essay Publishing & Distribution |
| system | any | formal-methods-applied-protocols | SOP: Formal Methods Applied Protocols |
| system | any | formal-methods-master-taxonomy | SOP: Formal Methods Master Taxonomy (The Blueprint of Proof) |
| system | any | formal-methods-tla-pluscal | SOP: Formal Methods — TLA+ and PlusCal Verification (The Blueprint Verifier) |
| system | any | generative-art-deployment | SOP: Generative Art Deployment (The Gallery Protocol) |
| system | any | market-gap-analysis | SOP: Full-Breath Market-Gap Analysis & Defensive Parrying |
| system | any | mcp-server-fleet-management | SOP: MCP Server Fleet Management (The Server Protocol) |
| system | any | multi-agent-swarm-orchestration | SOP: Multi-Agent Swarm Orchestration (The Polymorphic Swarm) |
| system | any | network-testament-protocol | SOP: Network Testament Protocol (The Mirror Protocol) |
| system | any | open-source-licensing-and-ip | SOP: Open Source Licensing and IP (The Commons Protocol) |
| system | any | performance-interface-design | SOP: Performance Interface Design (The Stage Protocol) |
| system | any | pitch-deck-rollout | SOP: Pitch Deck Generation & Rollout |
| system | any | polymorphic-agent-testing | SOP: Polymorphic Agent Testing (The Adversarial Protocol) |
| system | any | promotion-and-state-transitions | SOP: Promotion & State Transitions |
| system | any | recursive-study-feedback | SOP: Recursive Study & Feedback Loop (The Ouroboros) |
| system | any | repo-onboarding-and-habitat-creation | SOP: Repo Onboarding & Habitat Creation |
| system | any | research-to-implementation-pipeline | SOP: Research-to-Implementation Pipeline (The Gold Path) |
| system | any | security-and-accessibility-audit | SOP: Security & Accessibility Audit |
| system | any | session-self-critique | session-self-critique |
| system | any | smart-contract-audit-and-legal-wrap | SOP: Smart Contract Audit and Legal Wrap (The Ledger Protocol) |
| system | any | source-evaluation-and-bibliography | SOP: Source Evaluation & Annotated Bibliography (The Refinery) |
| system | any | stranger-test-protocol | SOP: Stranger Test Protocol |
| system | any | strategic-foresight-and-futures | SOP: Strategic Foresight & Futures (The Telescope) |
| system | any | styx-pipeline-traversal | SOP: Styx Pipeline Traversal (The 7-Organ Transmutation) |
| system | any | system-dashboard-telemetry | SOP: System Dashboard Telemetry (The Panopticon Protocol) |
| system | any | the-descent-protocol | the-descent-protocol |
| system | any | the-membrane-protocol | the-membrane-protocol |
| system | any | theoretical-concept-versioning | SOP: Theoretical Concept Versioning (The Epistemic Protocol) |
| system | any | theory-to-concrete-gate | theory-to-concrete-gate |
| system | any | typological-hermeneutic-analysis | SOP: Typological & Hermeneutic Analysis (The Archaeology) |

Linked skills: cicd-resilience-and-recovery, continuous-learning-agent, evaluation-to-growth, genesis-dna, multi-agent-workforce-planner, promotion-and-state-transitions, quality-gate-baseline-calibration, repo-onboarding-and-habitat-creation, structural-integrity-audit


**Prompting (Anthropic)**: context 200K tokens, format: XML tags, thinking: extended thinking (budget_tokens)


## Ecosystem Status

- **delivery**: 1/2 live, 1 planned
- **content**: 0/2 live, 1 planned
- **community**: 0/1 live, 0 planned

Run: `organvm ecosystem show a-i--skills` | `organvm ecosystem validate --organ IV`


## Entity Identity (Ontologia)

**UID:** `ent_repo_01KKKX3RVP46F8K5E48GAFEC2P` | **Matched by:** primary_name

Resolve: `organvm ontologia resolve a-i--skills` | History: `organvm ontologia history ent_repo_01KKKX3RVP46F8K5E48GAFEC2P`


## Live System Variables (Ontologia)

| Variable | Value | Scope | Updated |
|----------|-------|-------|---------|
| `active_repos` | 1 | global | 2026-03-20 |
| `archived_repos` | 0 | global | 2026-03-20 |
| `ci_workflows` | 1 | global | 2026-03-20 |
| `code_files` | 0 | global | 2026-03-20 |
| `dependency_edges` | 0 | global | 2026-03-20 |
| `operational_organs` | 1 | global | 2026-03-20 |
| `published_essays` | 0 | global | 2026-03-20 |
| `repos_with_tests` | 0 | global | 2026-03-20 |
| `sprints_completed` | 0 | global | 2026-03-20 |
| `test_files` | 0 | global | 2026-03-20 |
| `total_organs` | 1 | global | 2026-03-20 |
| `total_repos` | 1 | global | 2026-03-20 |
| `total_words_formatted` | 0 | global | 2026-03-20 |
| `total_words_numeric` | 0 | global | 2026-03-20 |
| `total_words_short` | 0K+ | global | 2026-03-20 |

Metrics: 9 registered | Observations: 7184 recorded
Resolve: `organvm ontologia status` | Refresh: `organvm refresh`


## System Density (auto-generated)

AMMOI: 54% | Edges: 28 | Tensions: 33 | Clusters: 5 | Adv: 3 | Events(24h): 12929
Structure: 8 organs / 117 repos / 1654 components (depth 17) | Inference: 98% | Organs: META-ORGANVM:66%, ORGAN-I:55%, ORGAN-II:47%, ORGAN-III:56% +4 more
Last pulse: 2026-03-20T10:58:23 | Δ24h: -3.7% | Δ7d: n/a

<!-- ORGANVM:AUTO:END -->


## ⚡ Conductor OS Integration
This repository is a managed component of the ORGANVM meta-workspace.
- **Orchestration:** Use `conductor patch` for system status and work queue.
- **Lifecycle:** Follow the `FRAME -> SHAPE -> BUILD -> PROVE` workflow.
- **Governance:** Promotions are managed via `conductor wip promote`.
- **Intelligence:** Conductor MCP tools are available for routing and mission synthesis.
