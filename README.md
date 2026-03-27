[![ORGAN-IV: Taxis](https://img.shields.io/badge/ORGAN--IV-Taxis-e65100?style=flat-square)](https://github.com/organvm-iv-taxis)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-101-4CAF50?style=flat-square)](./docs/CATEGORIES.md)

# a-i--skills

[![CI](https://github.com/organvm-iv-taxis/a-i--skills/actions/workflows/ci.yml/badge.svg)](https://github.com/organvm-iv-taxis/a-i--skills/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-pending-lightgrey)](https://github.com/organvm-iv-taxis/a-i--skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/organvm-iv-taxis/a-i--skills/blob/main/LICENSE)
[![Organ IV](https://img.shields.io/badge/Organ-IV%20Taxis-10B981)](https://github.com/organvm-iv-taxis)
[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/organvm-iv-taxis/a-i--skills)
[![Python](https://img.shields.io/badge/lang-Python-informational)](https://github.com/organvm-iv-taxis/a-i--skills)


**A composable skill framework for AI agent orchestration** -- 101 production-ready skill modules spanning creative, technical, enterprise, and governance domains, organized into a federated registry with multi-agent runtime support.

> Part of [ORGAN-IV: Taxis](https://github.com/organvm-iv-taxis) -- the orchestration and governance layer of the [ORGAN system](https://github.com/meta-organvm).

---

## Table of Contents

- [Product Overview](#product-overview)
- [Why This Exists](#why-this-exists)
- [Orchestration Philosophy](#orchestration-philosophy)
- [Technical Architecture](#technical-architecture)
- [Installation and Quick Start](#installation-and-quick-start)
- [Skill Catalog](#skill-catalog)
- [Skill Specification Format](#skill-specification-format)
- [Federation Protocol](#federation-protocol)
- [Tooling and Scripts](#tooling-and-scripts)
- [Cross-Organ Integration](#cross-organ-integration)
- [Related Work](#related-work)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Product Overview

`a-i--skills` is a structured repository of 101 AI agent skills -- self-contained instruction modules that teach large language models how to perform specialized tasks in a repeatable, composable way. Each skill is a directory containing a `SKILL.md` file with YAML frontmatter (metadata for discovery and activation) and Markdown content (the actual instructions an agent follows).

The repository serves three distinct functions:

1. **Skill Library** -- A browsable catalog of 101 skills across 12 categories, from algorithmic art generation to security threat modeling, each with standardized metadata, optional helper scripts, reference documentation, and asset templates.

2. **Orchestration In

## Installation and Quick Start

To integrate these skills into your Python-based agent framework:

```bash
# Clone the repository
git clone https://github.com/organvm-iv-taxis/a-i--skills.git
cd a-i--skills

# Install dependencies for helper scripts
pip install -r requirements.txt

# Use the discovery script to list available skills
python scripts/discover_skills.py --category technical
```

To use a skill, import the corresponding `SKILL.md` content into your agent's system prompt or tool-calling registry.