# Governance-Aware Skill Taxonomy

**Date**: 2026-03-20
**Status**: Draft → Reviewed (v3)
**Scope**: a-i--skills repo — skill spec extension + full metadata population
**Review**: Spec reviewed 2026-03-20. v2 addresses all 14 findings (2 critical, 6 important, 6 suggestions).
**Cross-check**: v3 verifies all organ_affinity mappings against actual organ CLAUDE.md files, repo inventories, and tech stacks. 15 corrections applied (see "Corrections from ecosystem cross-check" below).

## Problem Statement

105 skills are organized by topic domain (creative, development, security, etc.) with 95% of semantic metadata empty:
- 5/105 have triggers, 7/105 have inputs/outputs, 5/105 have complements
- The activation engine, skill planner, and chain system are built but data-starved
- Skills that should fire as universal governance norms (repo hygiene, quality gates, security baselines) require manual per-invocation — "one bird at a time"

The ORGANVM system operates on three axes simultaneously:
1. **Institutional function** — the 8 organs (Theoria, Poiesis, Ergon, Taxis, Logos, Koinonia, Kerygma, Meta)
2. **Lifecycle phase** — FRAME → SHAPE → BUILD → PROVE → SHIP
3. **Governance norms** — standards that auto-apply at promotion gates and phase transitions

The current topic taxonomy encodes none of these. The activation conditions spec supports them but the fields are empty.

## Design Decision

**Road 1.5: Governance-aware metadata overlay on the existing topic tree.**

- Keep the 12 topic categories for human discovery (browsing on GitHub)
- Add four new flat frontmatter fields: `governance_phases`, `governance_norm_group`, `governance_auto_activate`, `organ_affinity`
- Populate ALL 105 skills with governance fields, triggers, and complements (inputs/outputs/side_effects deferred to Phase 2)
- Map governance articles to norm groups that compose skills
- Let the existing activation engine auto-fire skills at the right lifecycle moments

### Why Not Restructure

A directory tree can only encode one axis. The ORGANVM system needs three. Any restructuring (by organ, by phase, by norm) still requires metadata for the other two axes. The migration cost is high and the structural gain is marginal. The topic categories are fine for what they do — human browsing. The metadata does the governance work.

## New Frontmatter Fields

> **Parser constraint**: The existing hand-rolled YAML parser in `skill_lib.py` does not support nested objects. All new fields are flat top-level keys, consistent with every other field in the spec. This avoids a parser rewrite across three implementations.

### `governance_phases` (list of strings, optional)

Which ORGANVM session lifecycle phases this skill is relevant at.

```yaml
governance_phases: [build, prove]
```

Valid values: `frame`, `shape`, `build`, `prove`, `ship`

> **Terminology note**: `ship` maps to the session lifecycle's DONE state and the feature lifecycle's DEPLOY stage. It is named `ship` rather than `done` because DONE is a terminal session state (work is finished) while `ship` describes active deployment/distribution work that skills assist with. The activation engine maps: session state DONE → governance phase `ship`.

| Phase | Session Lifecycle | Feature Lifecycle | What Happens |
|-------|------------------|-------------------|--------------|
| `frame` | FRAME | PLAN | Explore, research, understand |
| `shape` | SHAPE | DESIGN | Design, plan, architect |
| `build` | BUILD | IMPLEMENT | Write code, create artifacts |
| `prove` | PROVE | TEST + REVIEW | Verify, test, audit, review |
| `ship` | DONE | DEPLOY | Deploy, distribute, announce |

A skill may list multiple phases. `feature-workflow-orchestrator` spans all five.

### `governance_norm_group` (string, optional)

Which governance norm group this skill belongs to. Norm groups are clusters of skills that compose into a governance standard. Only set for skills that function as standards — not all skills are norms.

Valid values:

| Norm Group | Governance Basis | When It Fires | Purpose |
|---|---|---|---|
| `repo-hygiene` | Article V (Portfolio-Quality), Article III (All Organs Visible) | Repo creation, every promotion gate, SHAPE/PROVE phases | Root cleanliness, config organization, README quality, code standards |
| `quality-gate` | Amendment E (Session Lifecycle), Amendment A (Bronze Tier) | Every BUILD→PROVE transition | Tests pass, types check, linting clean, security scan |
| `security-baseline` | Implicit (ORGANVM security posture) | CANDIDATE→PUBLIC promotion, PROVE phase | Threat model, auth patterns, compliance, incident readiness |
| `documentation-standard` | Article IV (Docs Precede Deployment), Article V | SHAPE phase, every promotion gate | PRD exists, docs written, README passes Stranger Test |
| `distribution-readiness` | Article III (All Organs Visible) | GRADUATED artifacts, SHIP phase | Deployment pipeline, content strategy, portfolio readiness |

### `governance_auto_activate` (boolean, default false)

```yaml
governance_auto_activate: true
```

When `true`, this skill fires automatically when:
1. The session enters a matching `governance_phases` phase, OR
2. A promotion gate is reached and this skill's `governance_norm_group` applies

When `false` (default), the skill is phase-aware but only activates on manual invocation or trigger match.

Only a subset of norm-group skills should auto-activate. The rest are available but not forced. Core auto-activate skills:
- `github-repository-standards` (repo-hygiene)
- `github-repo-curator` (repo-hygiene)
- `coding-standards-enforcer` (repo-hygiene)
- `verification-loop` (quality-gate)
- `tdd-workflow` (quality-gate)
- `security-threat-modeler` (security-baseline)
- `product-requirements-designer` (documentation-standard)

### `organ_affinity` (list of strings, optional)

Which ORGANVM organs this skill serves. Determines conductor routing — "am I working in Organ II? Which skills are Poiesis-relevant?"

> **Mapping principle**: `organ_affinity` answers "which organ's repos would actually USE this skill during development" — not "which organ's conceptual domain does this skill belong to." Kerygma is conceptually about distribution but technically needs backend patterns, API design, and testing. Map by engineering reality, not by name.

```yaml
organ_affinity: [organ-ii, organ-iii]
```

Valid values: `all`, `organ-i`, `organ-ii`, `organ-iii`, `organ-iv`, `organ-v`, `organ-vi`, `organ-vii`, `meta`

| Value | Organ | Actual Tech Stacks |
|-------|-------|--------|
| `all` | Universal | Applies to every organ |
| `organ-i` | Theoria | Python, pytest, spaCy, NLP, symbolic engines, SQLite/ChromaDB |
| `organ-ii` | Poiesis | TypeScript (pnpm), Next.js 16, React Three Fiber, Vitest, SuperCollider, p5.js, Vanilla JS |
| `organ-iii` | Ergon | React/Vite, Next.js, NestJS, Fastify, Turborepo, PostgreSQL, Redis, Stripe, Kotlin, Swift, Python |
| `organ-iv` | Taxis | Python (hatch), TypeScript (Node ≥20), Redis, FastAPI, Vitest, Anthropic SDK |
| `organ-v` | Logos | Jekyll, Python (validators), YAML schemas, RSS, Markdown essays |
| `organ-vi` | Koinonia | Python 3.11+, FastAPI, SQLAlchemy 2.0, PostgreSQL (psycopg), Alembic, Click CLIs |
| `organ-vii` | Kerygma | Python 3.11+, 4 packages with CLIs, platform APIs (Mastodon/Discord/Bluesky/Ghost), circuit breakers, rate limiters |
| `meta` | Meta | Python (engine, ontologia, dashboard, alchemia, MCP server), FastAPI + HTMX, Next.js (stakeholder-portal), JSON Schemas, 404K+ word docs corpus |

A skill may list multiple organs. `organ_affinity` is determined by which organ's repos would actually use the skill during development. Skills with `all` are governance norms or universally applicable utilities. `all` should be reserved for true universals — don't use it as a shortcut when the skill applies to 3-4 specific organs.

## Complete Skill Mapping

### Governance Norms (auto_activate: true)

These skills fire automatically at governance gates.

#### repo-hygiene

| Skill | Phases | Triggers to Add |
|-------|--------|-----------------|
| `github-repository-standards` | shape, prove | `context:repo-setup`, `context:promotion`, `command:repo-standards` |
| `github-repo-curator` | shape, prove | `context:repo-setup`, `context:promotion`, `command:repo-audit` |
| `coding-standards-enforcer` | build | `context:new-project`, `project-has-package-json`, `project-has-pyproject-toml` |
| `dotfile-systems-architect` | shape | `user-asks-about-dotfiles`, `context:system-configuration` |

#### quality-gate

| Skill | Phases | Triggers to Add |
|-------|--------|-----------------|
| `verification-loop` | prove | `context:pre-commit`, `context:code-review`, `context:promotion` |
| `tdd-workflow` | build, prove | *(already has triggers)* |
| `testing-patterns` | prove | `user-asks-about-testing`, `project-has-jest-config-js`, `file-type:*.test.*`, `context:testing` |
| `webapp-testing` | prove | `user-asks-about-e2e-testing`, `project-has-playwright-config-ts`, `context:testing` |

#### security-baseline

| Skill | Phases | Triggers to Add |
|-------|--------|-----------------|
| `security-threat-modeler` | prove | *(already has triggers)* |
| `security-implementation-guide` | build | `user-asks-about-security`, `context:authentication`, `context:authorization` |
| `gdpr-compliance-check` | prove | `user-asks-about-gdpr`, `user-asks-about-privacy`, `context:compliance` |
| `incident-response-commander` | prove | `user-asks-about-incident`, `context:incident-response`, `context:outage` |
| `security-essentials-pack` | shape | `context:new-project`, `context:security-review` |

#### documentation-standard

| Skill | Phases | Triggers to Add |
|-------|--------|-----------------|
| `doc-coauthoring` | shape, prove | `user-asks-about-documentation`, `command:docs`, `context:documentation` |
| `product-requirements-designer` | frame, shape | `user-asks-about-prd`, `user-asks-about-requirements`, `context:product-planning` |
| `github-profile-architect` | ship | `user-asks-about-github-profile`, `context:github-setup` |
| `github-roadmap-strategist` | shape | `user-asks-about-roadmap`, `user-asks-about-github-projects`, `context:planning` |

#### distribution-readiness

| Skill | Phases | Triggers to Add |
|-------|--------|-----------------|
| `deployment-cicd` | ship | `user-asks-about-deployment`, `file-type:.github/workflows/*.yml`, `project-has-dockerfile` |
| `content-distribution` | ship | `user-asks-about-promotion`, `user-asks-about-content-strategy`, `context:distribution` |
| `portfolio-presentation` | ship | `user-asks-about-portfolio`, `context:presentation` |

### Full Skill Matrix

Every skill mapped to governance fields, organ affinity, primary phase, and triggers.

#### creative (13 skills) — Organ II primary

| Skill | Phases | Organ | Norm | Triggers |
|-------|--------|-------|------|----------|
| `algorithmic-art` | build | organ-ii | — | `user-asks-about-generative-art`, `user-asks-about-p5js`, `context:creative-coding` |
| `audio-engineering-patterns` | build | organ-ii | — | `user-asks-about-audio`, `user-asks-about-dsp`, `user-asks-about-mixing`, `context:audio-production` |
| `canvas-design` | build | organ-ii, organ-v, organ-vii | — | *(has triggers)* |
| `creative-writing-craft` | build | organ-ii, organ-v | — | `user-asks-about-writing`, `user-asks-about-fiction`, `user-asks-about-prose`, `context:creative-writing` |
| `generative-art-algorithms` | build | organ-ii | — | `user-asks-about-generative-art`, `user-asks-about-fractals`, `user-asks-about-noise-functions`, `context:creative-coding` |
| `generative-music-composer` | build | organ-ii | — | `user-asks-about-algorithmic-music`, `user-asks-about-composition`, `context:music-generation` |
| `interactive-theatre-designer` | shape, build | organ-ii | — | `user-asks-about-theatre`, `user-asks-about-interactive-narrative`, `context:performance` |
| `modular-synthesis-philosophy` | shape | organ-ii, organ-iv | — | `user-asks-about-modular-systems`, `user-asks-about-synthesis`, `context:system-architecture` |
| `movement-notation-systems` | shape, build | organ-ii | — | `user-asks-about-choreography`, `user-asks-about-movement`, `user-asks-about-laban` |
| `narratological-algorithms` | frame, shape | organ-i, organ-ii | — | `user-asks-about-narrative`, `user-asks-about-story-structure`, `context:narrative-analysis` |
| `reality-tv-narrative-analyzer` | frame | organ-i, organ-ii | — | `user-asks-about-reality-tv`, `context:media-analysis` |
| `theme-factory` | build | organ-ii, organ-v, organ-vii | — | `user-asks-about-theming`, `user-asks-about-styling`, `context:visual-design` |
| `three-js-interactive-builder` | build | organ-ii, organ-iii | — | `user-asks-about-threejs`, `user-asks-about-3d`, `user-asks-about-webgl`, `context:webgl` |

#### data (6 skills) — Organs I + III

| Skill | Phases | Organ | Norm | Triggers |
|-------|--------|-------|------|----------|
| `data-pipeline-architect` | shape, build | organ-iii, organ-i, organ-vi, meta | — | `user-asks-about-etl`, `user-asks-about-data-pipeline`, `context:data-engineering` |
| `data-storytelling-analyst` | build, prove | organ-iii, organ-v | — | `user-asks-about-data-visualization`, `user-asks-about-data-narrative`, `context:data-analysis` |
| `ml-experiment-tracker` | build, prove | organ-iii, organ-i | — | `user-asks-about-ml-experiments`, `user-asks-about-mlflow`, `context:machine-learning` |
| `sql-query-optimizer` | prove | organ-iii | — | `user-asks-about-sql-performance`, `file-type:*.sql`, `context:database` |
| `systemic-product-analyst` | frame | meta, organ-iii | — | `user-asks-about-product-analysis`, `user-asks-about-market-fit`, `context:strategic-analysis` |
| `time-series-analyst` | build | organ-iii, organ-i | — | `user-asks-about-time-series`, `user-asks-about-forecasting`, `context:data-analysis` |

#### development (26 skills) — Organ III primary

| Skill | Phases | Organ | Norm | Triggers |
|-------|--------|-------|------|----------|
| `accessibility-patterns` | build, prove | organ-iii, organ-ii | quality-gate | `user-asks-about-accessibility`, `user-asks-about-wcag`, `file-type:*.html`, `context:frontend` |
| `api-design-patterns` | shape | organ-iii, organ-iv, organ-vii, meta | — | *(has triggers)* |
| `artifacts-builder` | build | organ-ii, organ-iii | — | `user-asks-about-artifacts`, `context:claude-ai` |
| `backend-implementation-patterns` | build | organ-iii, organ-vi, organ-vii, meta | — | `user-asks-about-backend`, `user-asks-about-api-implementation`, `context:backend` |
| `code-refactoring-patterns` | build, prove | all | — | `user-asks-about-refactoring`, `context:code-review`, `context:technical-debt` |
| `coding-standards-enforcer` | build | all | repo-hygiene | `context:new-project`, `project-has-package-json`, `project-has-pyproject-toml` |
| `continuous-learning-agent` | prove | organ-iv | — | `user-asks-about-agent-learning`, `context:ai-agents` |
| `deployment-cicd` | ship | organ-iii, organ-iv | distribution-readiness | `user-asks-about-deployment`, `user-asks-about-cicd`, `file-type:.github/workflows/*.yml`, `project-has-dockerfile` |
| `dotfile-systems-architect` | shape | all | repo-hygiene | `user-asks-about-dotfiles`, `user-asks-about-xdg`, `context:system-configuration` |
| `feature-workflow-orchestrator` | shape, build | all | — | `user-asks-about-workflow`, `user-asks-about-feature-development`, `context:feature-development` |
| `frontend-design-systems` | shape | organ-iii, organ-ii | — | `user-asks-about-design-system`, `user-asks-about-components`, `context:frontend` |
| `fullstack-starter-pack` | shape | organ-iii | — | `user-asks-about-fullstack`, `context:new-project` |
| `gcp-resource-optimizer` | ship | organ-iii | — | `user-asks-about-gcp`, `user-asks-about-cloud-costs`, `context:infrastructure` |
| `iterative-code-exploration` | frame | all | — | `user-asks-about-codebase`, `context:onboarding`, `context:unfamiliar-code` |
| `mcp-builder` | build | organ-iv, meta | — | *(has triggers)* |
| `mcp-server-orchestrator` | build, ship | organ-iv, meta | — | `user-asks-about-mcp-server`, `user-asks-about-mcp-configuration`, `context:mcp-setup` |
| `mobile-platform-architect` | shape, build | organ-iii | — | `user-asks-about-mobile`, `user-asks-about-react-native`, `user-asks-about-flutter` |
| `nextjs-fullstack-patterns` | build | organ-iii, organ-ii, meta | — | `user-asks-about-nextjs`, `project-has-next-config-js`, `context:nextjs` |
| `postgres-advanced-patterns` | build | organ-iii, organ-vi | — | `user-asks-about-postgres`, `user-asks-about-database`, `file-type:*.sql`, `context:database` |
| `responsive-design-patterns` | build | organ-iii, organ-ii | — | `user-asks-about-responsive`, `user-asks-about-mobile-first`, `context:frontend` |
| `rust-systems-design` | build | organ-iii | — | `user-asks-about-rust`, `project-has-cargo-toml`, `file-type:*.rs`, `context:systems-programming` |
| `tdd-workflow` | build, prove | all | quality-gate | *(has triggers)* |
| `testing-patterns` | prove | all | quality-gate | `user-asks-about-testing`, `project-has-jest-config-js`, `project-has-pytest-ini`, `file-type:*.test.*`, `context:testing` |
| `verification-loop` | prove | all | quality-gate | `context:pre-commit`, `context:code-review`, `context:promotion` |
| `web-artifacts-builder` | build | organ-ii, organ-iii | — | `user-asks-about-web-artifacts`, `context:claude-ai` |
| `webapp-testing` | prove | organ-iii | quality-gate | `user-asks-about-e2e-testing`, `user-asks-about-playwright`, `context:testing` |

#### documentation (4 skills) — Universal Norms + Organ V

| Skill | Phases | Organ | Norm | Auto | Triggers |
|-------|--------|-------|------|------|----------|
| `doc-coauthoring` | shape, prove | all | documentation-standard | false | `user-asks-about-documentation`, `command:docs`, `context:documentation` |
| `github-profile-architect` | ship | organ-v, meta | documentation-standard | false | `user-asks-about-github-profile`, `context:github-setup` |
| `github-repo-curator` | shape, prove | all | repo-hygiene | **true** | `context:repo-setup`, `context:promotion`, `command:repo-audit` |
| `github-repository-standards` | shape, prove | all | repo-hygiene | **true** | `context:repo-setup`, `context:promotion`, `command:repo-standards` |

#### education (4 skills) — Organ VI primary

| Skill | Phases | Organ | Norm | Triggers |
|-------|--------|-------|------|----------|
| `enc1101-curriculum-designer` | shape, build | organ-vi | — | `user-asks-about-curriculum`, `user-asks-about-composition-course` |
| `evaluation-to-growth` | prove | organ-vi, organ-i, organ-v | — | `user-asks-about-evaluation`, `user-asks-about-critique`, `context:review` |
| `feedback-pedagogy` | prove | organ-vi | — | `user-asks-about-feedback`, `user-asks-about-rubrics`, `context:education` |
| `socratic-tutor` | frame | organ-vi, organ-i | — | `user-asks-about-learning`, `user-asks-about-understanding`, `context:education` |

#### integrations (9 skills) — Organ IV primary

| Skill | Phases | Organ | Norm | Triggers |
|-------|--------|-------|------|----------|
| `mcp-integration-patterns` | build | organ-iv, meta | — | `user-asks-about-mcp`, `user-asks-about-mcp-client`, `context:mcp-integration` |
| `oauth-flow-architect` | build | organ-iii | — | `user-asks-about-oauth`, `user-asks-about-authentication`, `context:auth` |
| `specstory-guard` | build | organ-iv | — | `command:specstory-guard`, `user-asks-about-secret-scanning`, `context:security` |
| `specstory-link-trail` | prove | organ-iv | — | `command:link-trail`, `user-asks-about-fetched-urls` |
| `specstory-organize` | prove | organ-iv | — | `command:specstory-organize`, `user-asks-about-organizing-sessions` |
| `specstory-project-stats` | frame | organ-iv | — | `command:project-stats`, `user-asks-about-specstory-stats` |
| `specstory-session-summary` | prove | organ-iv | — | `command:session-summary`, `user-asks-about-sessions` |
| `specstory-yak` | prove | organ-iv | — | `command:yak-shave`, `user-asks-about-yak-shaving` |
| `webhook-integration-patterns` | build | organ-iii, organ-iv, organ-vii | — | `user-asks-about-webhooks`, `user-asks-about-event-driven`, `context:integration` |

#### knowledge (6 skills) — Organ I primary

| Skill | Phases | Organ | Norm | Triggers |
|-------|--------|-------|------|----------|
| `claude-project-manifest` | frame, prove | organ-i, meta | — | `user-asks-about-project-manifest`, `user-asks-about-file-inventory`, `context:project-documentation` |
| `knowledge-architecture` | shape | organ-i, meta | — | `user-asks-about-knowledge-management`, `user-asks-about-ontology`, `context:information-architecture` |
| `knowledge-graph-builder` | shape, build | organ-i | — | `user-asks-about-knowledge-graph`, `user-asks-about-neo4j`, `context:data-modeling` |
| `recursive-systems-architect` | shape | organ-i, organ-iv | — | `user-asks-about-recursive-systems`, `user-asks-about-strange-loops`, `context:meta-design` |
| `research-synthesis-workflow` | frame | organ-i, organ-v | — | `user-asks-about-research`, `user-asks-about-literature-review`, `context:research` |
| `second-brain-librarian` | frame | organ-i, organ-vi | — | `user-asks-about-knowledge-base`, `user-asks-about-obsidian`, `user-asks-about-notion`, `context:note-taking` |

#### professional (11 skills) — Organs V + VII

| Skill | Phases | Organ | Norm | Triggers |
|-------|--------|-------|------|----------|
| `brand-guidelines` | build | organ-v, organ-vii | — | `user-asks-about-branding`, `user-asks-about-anthropic-brand`, `context:visual-identity` |
| `content-distribution` | ship | organ-vii | distribution-readiness | `user-asks-about-promotion`, `user-asks-about-content-strategy`, `context:distribution` |
| `cv-resume-builder` | build | — | — | `user-asks-about-resume`, `user-asks-about-cv`, `context:job-search` |
| `freelance-client-ops` | frame, shape | organ-iii | — | `user-asks-about-freelance`, `user-asks-about-contracts`, `user-asks-about-invoicing`, `context:client-work` |
| `grant-proposal-writer` | shape, build | organ-v, organ-vi | — | `user-asks-about-grants`, `user-asks-about-funding`, `user-asks-about-nsf` |
| `internal-comms` | build | organ-v | — | `user-asks-about-internal-communications`, `user-asks-about-status-report`, `context:corporate-communications` |
| `interview-preparation` | build | — | — | `user-asks-about-interview`, `user-asks-about-behavioral-questions`, `context:job-search` |
| `networking-outreach` | ship | — | — | `user-asks-about-networking`, `user-asks-about-outreach`, `user-asks-about-linkedin` |
| `portfolio-presentation` | ship | organ-v | distribution-readiness | `user-asks-about-portfolio`, `user-asks-about-case-study`, `context:presentation` |
| `slack-gif-creator` | build | organ-ii | — | `user-asks-about-gif`, `user-asks-about-slack-emoji`, `user-asks-about-animation` |
| `workshop-presentation-design` | shape, build | organ-vi, organ-v | — | `user-asks-about-workshop`, `user-asks-about-presentation`, `user-asks-about-talk` |

#### project-management (4 skills) — META + Organ IV

| Skill | Phases | Organ | Norm | Auto | Triggers |
|-------|--------|-------|------|------|----------|
| `github-roadmap-strategist` | shape | meta, organ-iv | documentation-standard | false | `user-asks-about-roadmap`, `user-asks-about-github-projects`, `context:planning` |
| `product-requirements-designer` | frame, shape | all | documentation-standard | **true** | `user-asks-about-prd`, `user-asks-about-requirements`, `context:product-planning` |
| `project-alchemy-orchestrator` | frame | meta | — | false | `user-asks-about-portfolio-management`, `user-asks-about-creative-portfolio`, `context:multi-project` |
| `project-orchestration` | frame, shape | meta, organ-iv | — | false | `user-asks-about-project-management`, `user-asks-about-coordination`, `context:multi-project` |

#### security (6 skills) — Governance Norms

| Skill | Phases | Organ | Norm | Auto | Triggers |
|-------|--------|-------|------|------|----------|
| `contract-risk-analyzer` | frame | organ-iii | — | false | `user-asks-about-contract-risk`, `user-asks-about-sow`, `context:legal-review` |
| `gdpr-compliance-check` | prove | organ-iii | security-baseline | false | `user-asks-about-gdpr`, `user-asks-about-privacy`, `context:compliance` |
| `incident-response-commander` | prove | organ-iv | security-baseline | false | `user-asks-about-incident`, `user-asks-about-outage`, `context:incident-response` |
| `security-essentials-pack` | build, prove | all | security-baseline | false | `context:new-project`, `context:security-review` |
| `security-implementation-guide` | build | all | security-baseline | false | `user-asks-about-security-patterns`, `user-asks-about-auth`, `context:authentication` |
| `security-threat-modeler` | prove | all | security-baseline | **true** | *(has triggers)* |

#### specialized (6 skills) — Organ II + III

| Skill | Phases | Organ | Norm | Triggers |
|-------|--------|-------|------|----------|
| `blockchain-integration-builder` | build | organ-iii | — | `user-asks-about-blockchain`, `user-asks-about-web3`, `user-asks-about-smart-contracts` |
| `defi-trading-systems` | build | organ-iii | — | `user-asks-about-defi`, `user-asks-about-trading`, `user-asks-about-liquidity` |
| `game-mechanics-designer` | shape, build | organ-ii, organ-iii | — | `user-asks-about-game-design`, `user-asks-about-game-mechanics`, `context:game-development` |
| `interfaith-sacred-geometry` | build | organ-ii | — | `user-asks-about-sacred-geometry`, `user-asks-about-interfaith`, `context:spiritual-art` |
| `local-llm-fine-tuning` | build | organ-iii, organ-iv | — | `user-asks-about-fine-tuning`, `user-asks-about-lora`, `user-asks-about-qlora`, `context:local-llm` |
| `location-ar-experience` | shape, build | organ-ii, organ-iii | — | `user-asks-about-ar`, `user-asks-about-augmented-reality`, `user-asks-about-geospatial` |

#### tools (6 skills) — Organ IV

| Skill | Phases | Organ | Norm | Triggers |
|-------|--------|-------|------|----------|
| `agent-swarm-orchestrator` | shape, build | organ-iv | — | `user-asks-about-agent-swarm`, `user-asks-about-multi-agent`, `context:multi-agent` |
| `multi-agent-workforce-planner` | shape | organ-iv | — | `user-asks-about-parallel-agents`, `user-asks-about-agent-planning`, `context:multi-agent` |
| `ontological-renamer` | shape | all | — | `user-asks-about-naming`, `user-asks-about-renaming`, `context:naming` |
| `skill-chain-prompts` | shape | organ-iv | — | `user-asks-about-skill-chains`, `user-asks-about-workflow-composition`, `context:skill-orchestration` |
| `skill-creator` | build | organ-iv | — | `user-asks-about-creating-skills`, `command:create-skill` |
| `speckit` | frame, shape | organ-iv | — | `user-asks-about-specifications`, `command:speckit`, `context:specification` |

#### document skills (4) — Universal tools

| Skill | Phases | Organ | Norm | Triggers |
|-------|--------|-------|------|----------|
| `docx` | build | all | — | `user-asks-about-docx`, `user-asks-about-word-document`, `file-type:*.docx` |
| `pdf` | build | all | — | `user-asks-about-pdf`, `file-type:*.pdf` |
| `pptx` | build | all | — | `user-asks-about-presentation`, `user-asks-about-powerpoint`, `file-type:*.pptx` |
| `xlsx` | build | all | — | `user-asks-about-spreadsheet`, `user-asks-about-excel`, `file-type:*.xlsx` |

## Complement Graph

Natural skill clusters that should cross-reference each other via `complements`.

### Development Pipeline
```
product-requirements-designer
  → api-design-patterns
    → backend-implementation-patterns
      → tdd-workflow → testing-patterns
        → verification-loop
          → deployment-cicd
```

### Repo Standards Chain
```
github-repository-standards ↔ github-repo-curator ↔ coding-standards-enforcer ↔ dotfile-systems-architect
```

### Security Stack
```
security-threat-modeler ↔ security-implementation-guide ↔ gdpr-compliance-check ↔ incident-response-commander
```

### Research Pipeline
```
research-synthesis-workflow → knowledge-architecture → knowledge-graph-builder
```

### Distribution Pipeline
```
content-distribution ↔ portfolio-presentation ↔ networking-outreach ↔ github-profile-architect
```

### MCP Stack
```
mcp-builder ↔ mcp-integration-patterns ↔ mcp-server-orchestrator
```

### Frontend Stack
```
frontend-design-systems ↔ responsive-design-patterns ↔ accessibility-patterns
```

### Creative Coding Stack
```
algorithmic-art ↔ generative-art-algorithms ↔ three-js-interactive-builder ↔ canvas-design
```

### Agent Stack
```
agent-swarm-orchestrator ↔ multi-agent-workforce-planner ↔ skill-chain-prompts
```

## Corrections from Ecosystem Cross-Check (v3)

Verified against actual organ CLAUDE.md files, repo inventories, and tech stacks on 2026-03-20.

**Principle applied**: `organ_affinity` answers "which organ's repos would actually USE this skill" — mapped by engineering reality (tech stacks, actual repos), not conceptual domain names.

| Skill | v2 Organ | v3 Organ | Reason |
|-------|----------|----------|--------|
| `api-design-patterns` | organ-iii, organ-iv | +organ-vii, +meta | Kerygma has platform API clients; META has dashboard + portal APIs |
| `backend-implementation-patterns` | organ-iii | +organ-vi, +organ-vii, +meta | Koinonia=FastAPI, Kerygma=4 Python packages, META=engine+dashboard |
| `data-pipeline-architect` | organ-iii, organ-i | +organ-vi, +meta | Koinonia=Alembic migrations, META=alchemia-ingestvm pipeline |
| `mcp-builder` | organ-iv | +meta | META has organvm-mcp-server |
| `mcp-integration-patterns` | organ-iv | +meta | MCP server imports engine + ontologia |
| `mcp-server-orchestrator` | organ-iv | +meta | MCP server deployment |
| `nextjs-fullstack-patterns` | organ-iii | +organ-ii, +meta | Poiesis=MET4MORFOSES (Next.js 16), META=stakeholder-portal |
| `postgres-advanced-patterns` | organ-iii | +organ-vi | Koinonia=koinonia-db (PostgreSQL + psycopg) |
| `rust-systems-design` | organ-iii, organ-i | organ-iii only | Organ I is Python-only — no Rust repos |
| `webhook-integration-patterns` | organ-iii, organ-iv | +organ-vii | Kerygma uses event-driven dispatch |
| `networking-outreach` | organ-vii | — (no organ) | Human networking ≠ automated distribution |
| `slack-gif-creator` | organ-vii | organ-ii | Creative artifact, not distribution infrastructure |
| `cv-resume-builder` | organ-vii | — (no organ) | Personal career tool, not organ-specific |
| `interview-preparation` | organ-vii | — (no organ) | Personal career tool, not organ-specific |
| `portfolio-presentation` | organ-vii, organ-v | organ-v only | Portfolio is discourse (Logos), not distribution (Kerygma) |

## Build Pipeline Changes

### 1. Skill Spec Update (`docs/api/skill-spec.md`)

Add `governance_phases`, `governance_norm_group`, `governance_auto_activate`, and `organ_affinity` to optional fields table with validation rules.

### 2. Activation Conditions Update (`docs/api/activation-conditions.md`)

Document that `governance_phases` and `governance_norm_group` fields are evaluated by the activation engine in addition to the `triggers` list. Add `context:promotion` as a recognized context keyword. No new trigger type syntax needed — the governance fields are read directly by the engine.

### 3. Validation Script Update (`scripts/validate_skills.py`)

Validate:
- `governance_phases` values are from: `frame`, `shape`, `build`, `prove`, `ship`
- `governance_norm_group` values are from: `repo-hygiene`, `quality-gate`, `security-baseline`, `documentation-standard`, `distribution-readiness`
- `governance_auto_activate` is boolean
- `organ_affinity` values are from: `all`, `organ-i` through `organ-vii`, `meta`

### 4. Registry Schema Update (`scripts/refresh_skill_collections.py`)

Add `governance_phases`, `governance_norm_group`, `governance_auto_activate`, and `organ_affinity` fields to the registry JSON extraction so they appear in `.build/skills-registry.json`. Bump registry version from `1.1` to `1.2`.

### 5. Lockfile Regeneration

All 105 skills will have modified SKILL.md files → lockfile hashes change → regenerate `.build/skills-lock.json`.

### 6. Governance Collection Files (new)

Generate two new collection files in `.build/collections/`:
- `governance-norms.txt` — skills with `governance_norm_group` set
- `auto-activate-skills.txt` — skills with `governance_auto_activate: true`

## Migration Path

1. Update spec docs (skill-spec.md, activation-conditions.md)
2. Update validation and refresh scripts
3. Apply governance metadata to all 105 SKILL.md files (batch operation)
4. Regenerate all build artifacts
5. Validate everything passes

The SKILL.md modifications are additive — existing fields are preserved, new fields are appended to frontmatter. No breaking changes to consumers that don't read the new fields.

## Scope Clarification

### Phase 1 (this spec)
- Add `governance_phases`, `governance_norm_group`, `governance_auto_activate`, `organ_affinity` to all 105 skills
- Populate `triggers` for all skills that currently lack them (~100 skills)
- Populate `complements` based on the complement graph above (~100 skills)
- Update spec docs, validation, and build pipeline
- Regenerate all build artifacts

### Phase 2 (deferred)
- Populate `inputs`, `outputs`, `side_effects` for all skills (enables skill-planner chain composition)
- Populate `tags` for skills that lack them
- Build conductor integration that reads governance metadata for phase-aware activation
- Build promotion-gate integration that enforces norm groups at state transitions

### Version Strategy
- Registry JSON version: `1.1` → `1.2`
- No skill spec version field exists currently — add one: `spec_version: "2.0"`
- Consumers that do not understand the new fields ignore them (backward compatible)
- Consumers that want governance-aware behavior read `governance_*` and `organ_affinity`
