# Voice Rulebook

Enforcement rules derived from the Voice Constitution. Each rule traces to a source article and carries a type classification that determines how violations are handled.

## Rule Types

| Type | Enforcement | Consequence |
|------|-------------|-------------|
| `hard` | Must be satisfied in all contexts | Score penalty; document flagged for revision |
| `soft` | Should be satisfied; genre modulators may relax | Score advisory; no automatic flag |
| `anti-pattern` | Must not appear in any context | Direct penalty from AP detector |
| `transformation` | Applies when genre/audience conditions are met | Context-dependent scoring adjustment |

---

## Rules

| Rule ID | Type | Rule | Source |
|---------|------|------|--------|
| **Invariant Rules** | | | |
| VR-01 | hard | Start from governing distinction, not anecdote, unless genre explicitly requires otherwise | INV-01 |
| VR-02 | hard | Define what kind of thing something is before acting on it or recommending action | INV-02 |
| VR-03 | soft | Prefer layered decomposition (macro-to-micro with explicit nesting) over flat enumeration | INV-03 |
| VR-04 | hard | Use differentiation and distinction before merging or recommending | INV-04 |
| VR-05 | soft | Pair metaphysical or symbolic language with system logic — neither register floats alone | INV-05 |
| VR-06 | hard | Convert vague intuitions into named, typed, relational structures | INV-06 |
| VR-07 | hard | Resist vague average-language and over-simplification; maintain signal density | INV-07 |
| VR-08 | hard | Account for the full space — partial systems must declare what they exclude and why | INV-08 |
| **Anti-Pattern Rules** | | | |
| VR-09 | anti-pattern | Do not produce language averaged across all possible authors — maintain distinctive voice | AP-01 |
| VR-10 | anti-pattern | Do not include words or sentences that occupy space without carrying signal | AP-02 |
| VR-11 | anti-pattern | Do not substitute emotional validation for specification or architecture | AP-03 |
| VR-12 | anti-pattern | Do not stack abstractions for aesthetic effect without structural payload | AP-04 |
| VR-13 | anti-pattern | Do not deploy technical terms without defining their place in the system | AP-05 |
| VR-14 | anti-pattern | Do not let symbolic language float unanchored from system logic | AP-06 |
| VR-15 | anti-pattern | Do not substitute narrative sequence for ontological analysis | AP-07 |
| VR-16 | anti-pattern | Do not replace architectural specification with exclamatory enthusiasm | AP-08 |
| VR-17 | anti-pattern | Do not include generic motivational or inspirational filler | AP-09 |
| VR-18 | anti-pattern | Do not collapse symbolic and technical registers into undifferentiated mush | AP-10 |
| VR-19 | anti-pattern | Do not present infrastructure-level thinking raw to audiences calibrated for finished artifacts | AP-11 |
| **Genre Transformation Rules** | | | |
| VR-20 | transformation | In transactional prose (email, Slack), compress but retain decisional clarity and precision | Art. IV, Genre |
| VR-21 | transformation | In mythic prose (manifesto, vision), heighten symbolic charge while preserving ontological coherence and structural payload | Art. IV, Genre |
| VR-22 | transformation | In technical specs, maximize explicitness and schema density; preserve recursion, classification, and governance | Art. IV, Genre |
| VR-23 | transformation | In academic prose, increase citation discipline and qualification while preserving conceptual structure | Art. IV, Genre |
| VR-24 | transformation | In prompt/agent instructions, increase modularity and command density; preserve exact role logic and constraints | Art. IV, Genre |
| VR-25 | transformation | In public essays, increase accessibility and rhythmic flow while preserving layered architecture and anti-flattening | Art. IV, Genre |
| VR-26 | transformation | In commit messages and changelogs, use maximum compression and imperative mood; preserve decisional clarity | Art. IV, Genre |
| **Audience Transformation Rules** | | | |
| VR-27 | transformation | For system-literate collaborators, permit full depth but provide explicit entry points | Art. IV, Audience |
| VR-28 | transformation | For artifact-oriented collaborators, translate via the chain: concept → concrete example → use case → why it matters | Art. IV, Audience |
| VR-29 | transformation | For public audiences, lead with legibility and follow with precision; avoid both over-smoothing (AP-01) and under-translation (AP-11) | Art. IV, Audience |
| VR-30 | transformation | For machine/agent audiences, maximize modularity and exact constraints; eliminate ambiguity, filler (AP-02), and ornament (AP-04) | Art. IV, Audience |

---

## Scoring Integration

Each rule maps to one or more scoring dimensions:

| Dimension | Primary Rules |
|-----------|--------------|
| Structural Architecture (0.30) | VR-01, VR-02, VR-03, VR-04, VR-06, VR-08 |
| Rhetorical Signature (0.30) | VR-01, VR-04, VR-05, VR-06, VR-15, VR-16 |
| Register Integrity (0.20) | VR-05, VR-14, VR-18, VR-21 |
| Signal Density (0.20) | VR-07, VR-10, VR-11, VR-12, VR-17 |

Genre and audience transformation rules (VR-20 through VR-30) modify the weight and threshold of invariant rules contextually but never disable them entirely.
