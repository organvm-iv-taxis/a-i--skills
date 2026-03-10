# Plan: Balance Skill Categories Based on User Profile

## Overview

Add new skills to balance the uneven category distribution, filling natural gaps that align with the user's demonstrated expertise from their GitHub repos/orgs.

## Current Distribution Analysis

| Category | Current | % | Assessment |
|----------|---------|---|------------|
| Development | 25 | 31% | Over-represented |
| Professional | 11 | 14% | Good |
| Creative | 10 | 13% | Good |
| Integrations | 6 | 8% | SpecStory-only, needs diversity |
| Security | 5 | 6% | Adequate |
| Documentation | 4 | 5% | GitHub-only focus |
| Education | 4 | 5% | Adequate |
| Project-Management | 4 | 5% | Adequate |
| Specialized | 4 | 5% | Eclectic |
| **Data** | **3** | **4%** | **Under-developed** |
| **Knowledge** | **2** | **2.5%** | **Minimal** |
| **Tools** | **2** | **2.5%** | **Minimal** |

## User's GitHub Profile Alignment

Key themes from repos/orgs:
- **AI & Agent Systems**: agentic-titan (swarm architecture), serena (coding agent), aionui (Gemini GUI)
- **Ontological/Recursive Systems**: recursive-engine, organon-noumenon, sēma-mētra
- **Creative Technology**: omni-dromenon-machina (generative music, choreography, theatre)
- **Practical Applications**: AR (my-block-warfare), crypto trading, real estate, subscription platforms
- **Knowledge Systems**: my-knowledge-base, cognitive archaeology, epistemic engines

## Proposed New Skills (15 total)

### Data Category (3 → 6 skills, +3 new)

| Skill | Description | Rationale |
|-------|-------------|-----------|
| `data-pipeline-architect` | ETL/ELT pipeline design patterns | Fundamental gap; user has data-heavy projects |
| `ml-experiment-tracker` | ML experiment logging and versioning | Aligns with local-llm-fine-tuning; practical ML workflow |
| `time-series-analyst` | Time-series data analysis patterns | Supports crypto trading (labores-profani-crux), practical analytics |

### Knowledge Category (2 → 5 skills, +3 new)

| Skill | Description | Rationale |
|-------|-------------|-----------|
| `knowledge-graph-builder` | Design and query knowledge graphs | User's my-knowledge-base, cognitive archaeology projects |
| `research-synthesis-workflow` | Systematic research compilation | Complements second-brain-librarian |
| `recursive-systems-architect` | Recursive and self-referential system design | Direct alignment with recursive-engine, organon-noumenon |

### Creative Category (10 → 13 skills, +3 new)

| Skill | Description | Rationale |
|-------|-------------|-----------|
| `generative-music-composer` | Algorithmic music composition | User's omni-dromenon-machina has music generation |
| `movement-notation-systems` | Choreography and movement scoring | User's omni-dromenon-machina has choreography systems |
| `interactive-theatre-designer` | Interactive narrative theatre experiences | User's theatre dialogue examples |

### Integrations Category (6 → 9 skills, +3 new)

| Skill | Description | Rationale |
|-------|-------------|-----------|
| `webhook-integration-patterns` | Design reliable webhook systems | Currently all SpecStory; needs general patterns |
| `oauth-flow-architect` | OAuth 2.0/OIDC implementation | Fundamental integration gap |
| `mcp-integration-patterns` | MCP client/server integration | User has serena MCP server; expands mcp-builder |

### Specialized Category (4 → 6 skills, +2 new)

| Skill | Description | Rationale |
|-------|-------------|-----------|
| `location-ar-experience` | Location-based AR patterns | User's my-block-warfare TurfSynth AR project |
| `defi-trading-systems` | DeFi and perpetual futures patterns | User's crypto perpetual futures trading repo |

### Tools Category (2 → 3 skills, +1 new)

| Skill | Description | Rationale |
|-------|-------------|-----------|
| `agent-swarm-orchestrator` | Multi-agent coordination patterns | User's agentic-titan swarm architecture |

## Distribution After Changes

| Category | Before | After | Change |
|----------|--------|-------|--------|
| Development | 25 | 25 | — |
| Professional | 11 | 11 | — |
| Creative | 10 | 13 | +3 |
| Integrations | 6 | 9 | +3 |
| Security | 5 | 5 | — |
| Documentation | 4 | 4 | — |
| Education | 4 | 4 | — |
| Project-Management | 4 | 4 | — |
| Specialized | 4 | 6 | +2 |
| Data | 3 | 6 | +3 |
| Knowledge | 2 | 5 | +3 |
| Tools | 2 | 3 | +1 |
| **TOTAL** | **80** | **95** | **+15** |

## Implementation Order

**Parallel execution** — Create all 15 skills simultaneously across all categories.

## Skill Template Structure

Each skill will have comprehensive structure:
```
skill-name/
├── SKILL.md              # Core instructions (~100-200 lines)
└── references/           # 2-3 supporting documents
    ├── patterns.md       # Domain patterns and examples
    ├── guide.md          # Step-by-step workflows
    └── [domain].md       # Domain-specific reference
```

## Content Sources

Each skill will draw from **both**:

1. **User's GitHub repos** — Pull patterns from:
   - `agentic-titan` → agent-swarm-orchestrator
   - `recursive-engine`, `organon-noumenon` → recursive-systems-architect
   - `omni-dromenon-machina` → generative-music-composer, movement-notation-systems, interactive-theatre-designer
   - `my-knowledge-base` → knowledge-graph-builder
   - `my-block-warfare` → location-ar-experience
   - `serena` → mcp-integration-patterns
   - Crypto repos → defi-trading-systems

2. **Industry best practices** — Augment with:
   - Standard patterns (ETL, MLOps, OAuth 2.0)
   - Framework documentation
   - Production-grade examples

## Verification

```bash
# After all skills created
python3 scripts/refresh_skill_collections.py
python3 scripts/validate_skills.py --collection example --unique

# Verify count
find skills -name "SKILL.md" | wc -l  # Should be 95

# Check distribution
for d in skills/*/; do echo -n "$d: "; ls -d "$d"*/ 2>/dev/null | wc -l; done
```

## Files to Create

15 new SKILL.md files with references/ directories:
- `skills/data/data-pipeline-architect/SKILL.md`
- `skills/data/ml-experiment-tracker/SKILL.md`
- `skills/data/time-series-analyst/SKILL.md`
- `skills/knowledge/knowledge-graph-builder/SKILL.md`
- `skills/knowledge/research-synthesis-workflow/SKILL.md`
- `skills/knowledge/recursive-systems-architect/SKILL.md`
- `skills/creative/generative-music-composer/SKILL.md`
- `skills/creative/movement-notation-systems/SKILL.md`
- `skills/creative/interactive-theatre-designer/SKILL.md`
- `skills/integrations/webhook-integration-patterns/SKILL.md`
- `skills/integrations/oauth-flow-architect/SKILL.md`
- `skills/integrations/mcp-integration-patterns/SKILL.md`
- `skills/specialized/location-ar-experience/SKILL.md`
- `skills/specialized/defi-trading-systems/SKILL.md`
- `skills/tools/agent-swarm-orchestrator/SKILL.md`

## Documentation Updates

After skill creation:
- Update `docs/CATEGORIES.md` with new skills and counts
- Update skill count in README.md (80 → 95)
