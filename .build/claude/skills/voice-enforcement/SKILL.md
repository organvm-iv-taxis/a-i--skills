---
name: voice-enforcement
description: Enforce the Orchestrator Voice Constitution during text generation. Provides voice constraints, anti-pattern awareness, and scoring guidance. Use when writing or reviewing prose-heavy documents (READMEs, design docs, essays, manifestos).
category: tools
triggers:
  - voice
  - voice enforcement
  - voice check
  - orchestrator voice
---

# Voice Enforcement

You have access to the Orchestrator Voice Constitution and Rulebook in this skill's references/ directory. Use them to guide your writing.

## When to Use

Activate when writing or editing prose-heavy documents: READMEs, design docs, vision documents, essays, manifestos, CLAUDE.md files, or any text that represents the orchestrator's voice.

## Quick Reference

**Default discourse sequence**: opening distinction → field definition → layering → formalization → governance → extension

**Identity invariants** (always preserve):
- System-first over anecdote-first (INV-01)
- Ontology before implementation (INV-02)
- Recursive layering (INV-03)
- Precision through distinction (INV-04)
- Mythic-structural synthesis (INV-05)
- Procedural transmutation (INV-06)
- Anti-flattening (INV-07)
- Exhaustiveness imperative (INV-08)

**Top anti-patterns** (never use):
- Generic corporate smoothness (AP-01)
- Chatty filler (AP-02)
- Enthusiasm replacing architecture (AP-08)
- Generic motivational filler (AP-09)
- System abstraction exceeding audience bandwidth (AP-11)

## Scoring

If `voice-scorer` CLI is installed:
```bash
voice-scorer score path/to/doc.md       # Heuristic score
voice-scorer score --deep path/to/doc.md # Deep LLM scoring
voice-scorer diff path/to/doc.md         # Voice erosion check
```

## Full Reference

See `references/VOICE_CONSTITUTION.md` and `references/VOICE_RULEBOOK.md` for complete governance rules.
