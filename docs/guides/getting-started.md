# Getting Started with AI Skills

Welcome to the AI Skills repository! This guide will help you get started with using and contributing skills.

## What Are Skills?

Skills are markdown files that give AI agents specialized knowledge and workflows for specific tasks. When you install skills, your AI agent (Claude Code, Codex, Gemini CLI, etc.) can recognize relevant tasks and apply the right frameworks.

## Quick Start

### 1. Browse Available Skills

- See [CATEGORIES.md](../CATEGORIES.md) for all 80 skills organized by category
- Check `.build/collections/by-purpose/` for purpose-specific lists
- Look in `.build/collections/by-complexity/` if you're just starting

### 2. Find Skills for Your Needs

**I want to improve code quality:**
```bash
cat .build/collections/by-purpose/code-quality.txt
```

**I need testing help:**
```bash
cat .build/collections/by-purpose/testing.txt
```

**I'm working on backend:**
```bash
cat .build/collections/by-purpose/backend-development.txt
```

### 3. Install Skills

Skills are already available in your AI agent if you've cloned/installed this repository. Just ask your agent:

```
"Help me with test-driven development"
→ Agent uses tdd-workflow skill

"Verify my code quality"
→ Agent uses verification-loop skill

"Optimize my PostgreSQL queries"
→ Agent uses postgres-advanced-patterns skill
```

## Repository Structure

```
ai-skills/
├── README.md                    # Start here!
├── docs/                        # Documentation
│   ├── CATEGORIES.md            # Browse all skills by category
│   ├── CONTRIBUTING.md          # How to contribute
│   ├── architecture/
│   ├── guides/                  # You are here
│   └── api/
│
├── skills/                      # 80 skills organized by category
│   ├── creative/               # Art, music, design
│   ├── development/            # Coding patterns, tools
│   ├── professional/           # Business, career
│   └── ...                     # Other categories
│
└── .build/                      # Generated outputs
    ├── collections/             # Curated skill lists
    │   ├── by-category/        # By domain
    │   ├── by-purpose/         # By use case
    │   └── by-complexity/      # By difficulty
    ├── claude/                  # Claude Code bundles
    └── codex/                   # Codex bundles
```

## Using Skills

### With Claude Code

Skills are automatically detected. Just describe your task:

```
"I need to implement TDD for my new feature"
"Analyze my yak shaving from last week" (uses specstory-yak)
"Help me refactor this messy code" (uses code-refactoring-patterns)
```

### With Other Agents

Skills work with:
- **Codex**: Via `.codex/skills/`
- **Gemini CLI**: Via `extensions/gemini/`
- **Cursor**: Via agent-specific directories

## Exploring Skills

### Read a Skill

```bash
# View skill documentation
cat tdd-workflow/SKILL.md

# Check skill scripts
ls tdd-workflow/scripts/
```

### Try a Skill

1. Open Claude Code (or your AI agent)
2. Describe a task that matches the skill
3. The agent will apply the skill's patterns

Example:
```
"I want to set up TDD workflow for my new Node.js project"
```

The agent will follow the tdd-workflow skill to guide you through:
- Writing failing tests first
- Implementing minimal code
- Refactoring while keeping tests green

## Common Workflows

### For Developers

**Starting a new feature:**
1. Use `feature-workflow-orchestrator` for planning
2. Use `tdd-workflow` for implementation
3. Use `verification-loop` before committing

**Improving existing code:**
1. Use `code-refactoring-patterns` for refactoring
2. Use `verification-loop` to validate changes
3. Use `testing-patterns` to add missing tests

### For Project Managers

**Planning a project:**
1. Use `product-requirements-designer` for PRDs
2. Use `github-roadmap-strategist` for roadmaps
3. Use `project-orchestration` for execution

### For Writers

**Creating content:**
1. Use `creative-writing-craft` for storytelling
2. Use `doc-coauthoring` for collaboration
3. Use `content-distribution` for publishing

## Tips & Best Practices

### 1. Start Simple

Begin with beginner-friendly skills:
- `template-skill` - Learn skill format
- `verification-loop` - Essential code quality
- `tdd-workflow` - Core development practice

### 2. Combine Skills

Skills work together:
- `tdd-workflow` + `verification-loop` = Complete quality workflow
- `frontend-design-systems` + `responsive-design-patterns` = Full UI development
- `postgres-advanced-patterns` + `backend-implementation-patterns` = Complete backend stack

### 3. Read the SKILL.md

Each skill's `SKILL.md` contains:
- When to use it
- Step-by-step workflows
- Examples and patterns
- Integration with other skills

### 4. Check Script Documentation

Some skills include helper scripts in `scripts/` directory. Check for:
- README.md in scripts/
- Python requirements.txt
- Usage examples in SKILL.md

## Getting Help

### Documentation

- [Repository Structure](../architecture/repository-structure.md)
- [Creating Skills](creating-skills.md)
- [Skill Format Spec](../api/skill-spec.md)
- [Contributing Guide](../CONTRIBUTING.md)

### Finding Skills

- Browse by category: `docs/CATEGORIES.md`
- Browse by purpose: `.build/collections/by-purpose/`
- Browse by complexity: `.build/collections/by-complexity/`
- Search: `grep -r "keyword" */SKILL.md`

### Issues & Questions

- Check existing issues: https://github.com/your-repo/issues
- Open new issue with appropriate template
- Discussion forum: https://github.com/your-repo/discussions

## Next Steps

1. **Browse** [CATEGORIES.md](../CATEGORIES.md) to see all available skills
2. **Read** a few `SKILL.md` files to understand the format
3. **Try** using skills with your AI agent
4. **Contribute** your own skills (see [creating-skills.md](creating-skills.md))

## Common Questions

**Q: Do I need to install each skill separately?**
A: No! If you've cloned this repository, all skills are available to your agent.

**Q: Can I use multiple skills at once?**
A: Yes! Many skills are designed to complement each other.

**Q: How do I know which skill to use?**
A: Start with `CATEGORIES.md` or ask your agent: "Which skill should I use for [task]?"

**Q: Can I modify skills?**
A: Yes! Fork the repository and customize. See `CONTRIBUTING.md` for guidelines.

**Q: Do skills work offline?**
A: Yes! Skills are just markdown files with instructions.

---

**Ready to dive deeper?** Check out:
- [Creating Your Own Skills](creating-skills.md)
- [Contributing to the Repository](../CONTRIBUTING.md)
- [Skill Format Specification](../api/skill-spec.md)
