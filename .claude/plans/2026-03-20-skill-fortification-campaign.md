# Skill Fortification Campaign — Full Spec Sequence

## Context

The gap analysis revealed 29 missing skills, 5 missing bundles, and a Phase 2 metadata pass needed to make the a-i--skills collection whole. This plan defines the spec-writing and implementation sequence: what runs in parallel, what runs in tandem (coordinated separate streams), and what runs in procession (sequential dependencies).

## Campaign Structure

```
                    ┌─── Stream A: Engineering Infrastructure (14 skills) ───┐
                    │                                                         │
Spec Sprint 1 ─────┼─── Stream B: Governance & Process (6 skills) ──────────┼──→ Bundle Sprint → Metadata Pass
(all 29 specs)      │                                                         │
                    ├─── Stream C: Organ-Specific (8 skills) ────────────────┤
                    │                                                         │
                    └─── Stream D: SOP Distillation (7 skills) ──────────────┘
```

Four parallel streams → bundle convergence → metadata convergence.

---

## Complete Inventory (35 work items)

### Stream A: Engineering Infrastructure (14 skills)

Skills that serve 3+ organs — the missing plumbing.

| # | Skill | Category | Organs | Wave | Depends On |
|---|-------|----------|--------|------|-----------|
| A1 | `python-packaging-patterns` | development | I,IV,V,VI,VII,META | 0 | — |
| A2 | `cli-tool-design` | development | I,VI,VII,META | 0 | — |
| A3 | `redis-patterns` | development | III,IV | 0 | — |
| A4 | `docker-containerization` | development | II,III,META | 0 | — |
| A5 | `resilience-patterns` | development | III,VII | 0 | — |
| A6 | `vector-search-patterns` | development | I,III | 0 | — |
| A7 | `json-schema-design` | development | META | 0 | — |
| A8 | `htmx-interaction-patterns` | development | META | 0 | — |
| A9 | `fastapi-patterns` | development | IV,VI,META | 1 | soft: A1 |
| A10 | `database-migration-patterns` | development | III,VI,META | 1 | soft: A1 |
| A11 | `monorepo-management` | development | II,III | 1 | — |
| A12 | `react-three-fiber-patterns` | creative | II | 1 | existing: three-js-interactive-builder |
| A13 | `configuration-management` | development | all | 0 | — |
| A14 | `error-handling-logging-patterns` | development | all | 0 | — |

### Stream B: Governance & Process (6 skills)

Skills that codify ORGANVM-specific lifecycle and governance.

| # | Skill | Category | Phase Affinity | Wave | Depends On |
|---|-------|----------|---------------|------|-----------|
| B1 | `session-lifecycle-patterns` | tools | all phases | 0 | — |
| B2 | `stranger-test-protocol` | documentation | prove | 0 | — |
| B3 | `prompt-engineering-patterns` | tools | build | 0 | — |
| B4 | `agent-testing-patterns` | development | prove | 1 | existing: testing-patterns |
| B5 | `cross-agent-handoff` | tools | prove | 1 | — |
| B6 | `repo-onboarding-flow` | development | shape | 2 | soft: A1, A4, B2 |
| B7 | `promotion-readiness-checklist` | project-management | prove | 2 | B2, B6 |

### Stream C: Organ-Specific (8 skills)

Skills tailored to specific organs' actual engineering work.

| # | Skill | Category | Organ | Wave | Depends On |
|---|-------|----------|-------|------|-----------|
| C1 | `essay-publishing-pipeline` | integrations | V | 0 | — |
| C2 | `social-media-api-integration` | integrations | VII | 0 | — |
| C3 | `posse-distribution-architecture` | integrations | VII | 1 | A5, C2 |
| C4 | `technical-analytical-writing` | documentation | V | 0 | — |
| C5 | `community-platform-patterns` | development | VI | 0 | — |
| C6 | `realtime-websocket-patterns` | development | II,III | 0 | — |
| C7 | `browser-extension-patterns` | development | III | 0 | — |
| C8 | `data-ingestion-pipeline` | data | META | 0 | — |

### Stream D: SOP Distillation (7 skills)

Existing SOPs converted to skill format.

| # | Skill | Source SOP | Wave | Depends On |
|---|-------|-----------|------|-----------|
| D1 | `source-evaluation-bibliography` | source-evaluation-and-bibliography | 0 | — |
| D2 | `data-backup-patterns` | data-migration-and-backup | 0 | — |
| D3 | `pitch-deck-patterns` | pitch-deck-rollout | 0 | — |
| D4 | `generative-art-deployment` | generative-art-deployment | 0 | — |
| D5 | `conversation-content-pipeline` | conversation-to-content-pipeline | 1 | — |
| D6 | `document-audit-extraction` | document-audit-feature-extraction | 1 | — |
| D7 | `market-gap-analysis` | market-gap-analysis | 1 | existing: systemic-product-analyst |

### Bundles (5 packs)

| # | Bundle | Includes | Depends On |
|---|--------|----------|-----------|
| E1 | `organvm-governance-pack` | B7, B6, B2, github-repository-standards, verification-loop, coding-standards-enforcer | B6, B7 |
| E2 | `essay-to-distribution-pack` | C1, creative-writing-craft, content-distribution, C3 | C1, C3 |
| E3 | `agent-development-pack` | agent-swarm-orchestrator, B4, B5, mcp-builder, B3 | B3, B4, B5 |
| E4 | `python-backend-pack` | A9, A1, A10, A2, A3 | A1, A2, A3, A9, A10 |
| E5 | `monorepo-devops-pack` | A11, A4, deployment-cicd, coding-standards-enforcer | A4, A11 |

### Phase 2 Metadata (1 work item)

| # | Work Item | Scope | Depends On |
|---|-----------|-------|-----------|
| F1 | Full suite metadata population | inputs, outputs, side_effects, tags for all ~140 skills | All of the above |

---

## Execution Sequence

### SPEC SPRINT 1: All 36 Skill Specs (max parallel)

**Duration estimate:** 1–2 sessions per spec, 4 parallel streams

For spec AUTHORING, almost all skills are independent — a spec can reference a future skill conceptually. Only bundles need constituent specs to exist. So we write all 36 skill specs in one sprint, organized into 4 parallel streams.

```
SESSION BLOCK 1 (4 streams, ~8 specs each)
─────────────────────────────────────────────

Stream A (Engineering)          Stream B (Governance)        Stream C (Organ)              Stream D (SOP)
─────────────────────          ─────────────────────        ────────────────              ──────────────
A1  python-packaging      ║    B1  session-lifecycle   ║    C1  essay-pipeline       ║    D1  source-eval
A2  cli-tool-design       ║    B2  stranger-test       ║    C2  social-media-api     ║    D2  data-backup
A3  redis-patterns        ║    B3  prompt-engineering   ║    C4  technical-writing    ║    D3  pitch-deck
A4  docker-container      ║    B4  agent-testing        ║    C5  community-platform   ║    D4  gen-art-deploy
A5  resilience-patterns   ║    B5  cross-agent-handoff  ║    C6  realtime-websocket   ║    D5  conversation-content
A6  vector-search         ║    B6  repo-onboarding*     ║    C7  browser-extension    ║    D6  document-audit
A7  json-schema-design    ║    B7  promotion-ready*     ║    C8  data-ingestion       ║    D7  market-gap
A8  htmx-patterns         ║                             ║    C3  posse-distrib*       ║
A9  fastapi-patterns      ║                             ║                              ║
A10 db-migration          ║                             ║                              ║
A11 monorepo-mgmt         ║                             ║                              ║
A12 r3f-patterns          ║                             ║                              ║
A13 config-mgmt           ║                             ║                              ║
A14 error-logging         ║                             ║                              ║

* = spec references other specs in its stream; write AFTER its dependencies
```

**Within each stream, the ordering is:**

**Stream A** (14 specs): A1–A8 are fully parallel (Wave 0). A9–A14 can start immediately but should reference A1 where appropriate. No hard blocks.

**Stream B** (7 specs): B1–B5 are fully parallel. B6 soft-depends on B2 (stranger-test informs onboarding quality bar). B7 depends on B6 (promotion needs to know what onboarding produces). Write B6 and B7 last in the stream.

**Stream C** (8 specs): C1, C2, C4–C8 are fully parallel. C3 (posse-distribution) soft-depends on A5 (resilience-patterns) and C2 (social-media-api). Write C3 last in the stream.

**Stream D** (7 specs): All fully parallel. No internal dependencies.

**Total: 36 specs, 4 parallel streams, ~9 specs per stream.**

### SPEC SPRINT 2: Bundle Specs (after Sprint 1)

5 bundle specs. Each references constituent skills from Sprint 1. Can be written in parallel after Sprint 1 completes.

```
SESSION BLOCK 2 (all parallel)
───────────────────────────────
E1  organvm-governance-pack
E2  essay-to-distribution-pack
E3  agent-development-pack
E4  python-backend-pack
E5  monorepo-devops-pack
```

### SPEC SPRINT 3: Metadata Pass Spec

1 spec defining the Phase 2 metadata schema and population strategy for ALL ~140 skills (105 original + ~35 new).

```
SESSION BLOCK 3
───────────────
F1  Full suite metadata pass (inputs/outputs/side_effects/tags for all skills)
```

---

## Implementation Sequence

After all specs are written and approved, implementation proceeds in waves based on HARD dependencies.

### IMPLEMENTATION WAVE 0 — Foundation (max parallel)

**All Wave 0 skills from all streams simultaneously.** These have zero dependencies.

```
PARALLEL EXECUTION (up to 6 agents)
────────────────────────────────────
A1  python-packaging-patterns     │ A2  cli-tool-design              │ A3  redis-patterns
A4  docker-containerization       │ A5  resilience-patterns           │ A6  vector-search-patterns
A7  json-schema-design            │ A8  htmx-interaction-patterns     │ A13 configuration-management
A14 error-handling-logging        │ B1  session-lifecycle-patterns    │ B2  stranger-test-protocol
B3  prompt-engineering-patterns   │ C1  essay-publishing-pipeline     │ C2  social-media-api-integration
C4  technical-analytical-writing  │ C5  community-platform-patterns   │ C6  realtime-websocket-patterns
C7  browser-extension-patterns    │ C8  data-ingestion-pipeline       │ D1  source-evaluation-bibliography
D2  data-backup-patterns          │ D3  pitch-deck-patterns           │ D4  generative-art-deployment
```

**24 skills, all parallel.** Limited only by agent bandwidth (memory-constrained 16GB system → 4–6 concurrent agents max).

After Wave 0: run `refresh_skill_collections.py`, validate, commit.

### IMPLEMENTATION WAVE 1 — First Dependencies (max parallel)

Skills that soft-depend on Wave 0 patterns.

```
PARALLEL EXECUTION
──────────────────
A9  fastapi-patterns (references A1)          │ A10 database-migration-patterns (references A1)
A11 monorepo-management                       │ A12 react-three-fiber-patterns
B4  agent-testing-patterns                    │ B5  cross-agent-handoff
D5  conversation-content-pipeline             │ D6  document-audit-extraction
D7  market-gap-analysis                       │
```

**9 skills, all parallel.**

After Wave 1: refresh, validate, commit.

### IMPLEMENTATION WAVE 2 — Composite Skills (limited parallel)

```
SEQUENTIAL/PARALLEL
───────────────────
C3  posse-distribution-architecture (needs A5 + C2)    ║ IN PARALLEL
B6  repo-onboarding-flow (needs A1 + A4 + B2)          ║ WITH EACH OTHER
                                                        ║
THEN (procession):                                      ║
B7  promotion-readiness-checklist (needs B6 + B2)       ← AFTER B6
```

**3 skills: 2 parallel, then 1 sequential.**

After Wave 2: refresh, validate, commit.

### IMPLEMENTATION WAVE 3 — Bundles (all parallel)

```
PARALLEL EXECUTION
──────────────────
E1  organvm-governance-pack         │ E2  essay-to-distribution-pack
E3  agent-development-pack          │ E4  python-backend-pack
E5  monorepo-devops-pack            │
```

**5 bundles, all parallel.** Bundles are lightweight — just `includes` lists + description.

After Wave 3: refresh, validate, commit.

### IMPLEMENTATION WAVE 4 — Full Suite Metadata

Phase 2 of the governance work. Populate `inputs`, `outputs`, `side_effects`, `tags` for ALL ~140 skills.

```
SEQUENTIAL (one large batch operation)
──────────────────────────────────────
F1  Create metadata_phase2_mapping.json (all ~140 skills)
F2  Extend apply_governance_metadata.py for Phase 2 fields
F3  Run batch application
F4  Regenerate all build artifacts
F5  Final validation
```

---

## Tandem Coordination Points

These are moments where streams must synchronize:

| Sync Point | What Waits | What Delivers | When |
|-----------|------------|---------------|------|
| **S1: Resilience → POSSE** | C3 (posse-distribution) | A5 (resilience-patterns) | Wave 0 → Wave 1 |
| **S2: Stranger → Onboarding** | B6 (repo-onboarding) | B2 (stranger-test-protocol) | Wave 0 → Wave 2 |
| **S3: Social API → POSSE** | C3 (posse-distribution) | C2 (social-media-api) | Wave 0 → Wave 1 |
| **S4: Onboarding → Promotion** | B7 (promotion-readiness) | B6 (repo-onboarding) | Wave 2a → Wave 2b |
| **S5: All Skills → Bundles** | E1–E5 (all bundles) | All constituent skills | Wave 2 → Wave 3 |
| **S6: Everything → Metadata** | F1 (metadata pass) | All 36 new items | Wave 3 → Wave 4 |

---

## Parallel Capacity Planning

Given 16GB RAM constraint and recommended 4–6 concurrent agents:

| Wave | Total Items | Parallel Slots | Batches Needed | Est. Sessions |
|------|------------|---------------|----------------|---------------|
| Spec Sprint 1 | 36 specs | 4 streams | 4 streams × ~4 batches | 4–6 sessions |
| Spec Sprint 2 | 5 bundles | 5 | 1 batch | 1 session |
| Spec Sprint 3 | 1 metadata | 1 | 1 | 1 session |
| Wave 0 | 24 skills | 6 agents | 4 batches of 6 | 4 sessions |
| Wave 1 | 9 skills | 6 agents | 2 batches | 2 sessions |
| Wave 2 | 3 skills | 2+1 | 2 batches | 1 session |
| Wave 3 | 5 bundles | 5 agents | 1 batch | 1 session |
| Wave 4 | 1 metadata | 1 (batch script) | 1 | 1 session |
| **TOTAL** | **42 items** | | | **~15–17 sessions** |

---

## Procession Order (if running strictly sequential)

If running single-threaded (one skill at a time), the optimal order is:

```
 1. python-packaging-patterns      (unlocks A9, A10, B6)
 2. cli-tool-design                (unlocks E4)
 3. resilience-patterns            (unlocks C3)
 4. stranger-test-protocol         (unlocks B6, B7)
 5. docker-containerization        (unlocks B6, E5)
 6. redis-patterns
 7. vector-search-patterns
 8. json-schema-design
 9. htmx-interaction-patterns
10. configuration-management
11. error-handling-logging-patterns
12. session-lifecycle-patterns
13. prompt-engineering-patterns
14. essay-publishing-pipeline
15. social-media-api-integration   (unlocks C3)
16. technical-analytical-writing
17. community-platform-patterns
18. realtime-websocket-patterns
19. browser-extension-patterns
20. data-ingestion-pipeline
21. source-evaluation-bibliography
22. data-backup-patterns
23. pitch-deck-patterns
24. generative-art-deployment
25. fastapi-patterns
26. database-migration-patterns
27. monorepo-management
28. react-three-fiber-patterns
29. agent-testing-patterns
30. cross-agent-handoff
31. conversation-content-pipeline
32. document-audit-extraction
33. market-gap-analysis
34. posse-distribution-architecture  (needs A5 + C2)
35. repo-onboarding-flow             (needs A1 + A4 + B2)
36. promotion-readiness-checklist    (needs B6)
37. organvm-governance-pack          (bundle)
38. essay-to-distribution-pack       (bundle)
39. agent-development-pack           (bundle)
40. python-backend-pack              (bundle)
41. monorepo-devops-pack             (bundle)
42. Full suite metadata pass
```

Items 1–5 are the critical path — they unlock the most downstream dependencies.

---

## Verification Strategy

After each wave:
1. `python3 scripts/validate_skills.py --collection all --unique`
2. `python3 scripts/refresh_skill_collections.py`
3. `python3 scripts/validate_generated_dirs.py`
4. Verify registry stats show expected counts
5. Spot-check 2–3 skills from the wave

After Wave 4 (final):
- Full registry audit: all ~140 skills have governance_phases, organ_affinity, triggers, complements, inputs, outputs, side_effects, tags
- Zero empty semantic fields
- All complement relationships bidirectional
- All norm groups properly composed
- Governance norms collection = ~28 skills
- Auto-activate collection = ~10 skills

---

## What This Produces

| Metric | Before | After |
|--------|--------|-------|
| Total skills | 105 | ~140 |
| With triggers | 105 (just completed) | ~140 |
| With complements | 35 | ~100+ |
| With inputs/outputs | 7 | ~140 |
| With side_effects | 0 | ~140 |
| With tags | ~30 | ~140 |
| Skill bundles | 4 | 9 |
| Governance norms | 21 | ~28 |
| Auto-activate | 7 | ~10 |
| SOPs with linked skills | 9/46 | ~20/46 |
| Organ-specific skills (V,VI,VII) | ~5 | ~15 |
