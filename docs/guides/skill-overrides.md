# Skill Overrides

Custom skill overrides let you replace or extend built-in skills without modifying the repository. This follows the same pattern as Oh My Zsh's `$ZSH_CUSTOM` directory.

## Setup

Set the `SKILLS_CUSTOM_DIR` environment variable to a directory containing your custom skills:

```bash
export SKILLS_CUSTOM_DIR="$HOME/.local/share/ai-skills-custom"
```

Add this to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.) to make it persistent.

## How It Works

When a skill is loaded, the resolution order is:

1. `$SKILLS_CUSTOM_DIR/<skill-name>/SKILL.md` (if it exists)
2. Built-in `skills/<category>/<skill-name>/SKILL.md`

Custom skills with the same name as a built-in skill take precedence. The built-in version is never loaded when an override exists.

## Directory Structure

Custom skills follow the same format as built-in skills. No category subdirectories are needed:

```
$SKILLS_CUSTOM_DIR/
├── tdd-workflow/          # Overrides built-in tdd-workflow
│   └── SKILL.md
├── my-private-skill/      # New skill not in the repo
│   ├── SKILL.md
│   └── references/
│       └── internal-api.md
└── cv-resume-builder/     # Customized resume builder
    ├── SKILL.md
    └── assets/
        └── templates/
            └── company-template.md
```

## Common Use Cases

### Replacing a Built-In Skill

Copy the built-in skill and modify it:

```bash
mkdir -p "$SKILLS_CUSTOM_DIR/tdd-workflow"
cp skills/development/tdd-workflow/SKILL.md "$SKILLS_CUSTOM_DIR/tdd-workflow/"

# Edit to match your team's testing conventions
$EDITOR "$SKILLS_CUSTOM_DIR/tdd-workflow/SKILL.md"
```

### Adding Private Skills

Create skills with internal knowledge that should not be committed to a shared repository:

```bash
mkdir -p "$SKILLS_CUSTOM_DIR/internal-deploy"
cat > "$SKILLS_CUSTOM_DIR/internal-deploy/SKILL.md" << 'EOF'
---
name: internal-deploy
description: Deploy services to the internal staging and production clusters using our custom toolchain.
license: Proprietary
---

# Internal Deployment

Steps for deploying to our infrastructure...
EOF
```

### Extending a Built-In Skill

Copy a skill and add references or assets specific to your workflow:

```bash
mkdir -p "$SKILLS_CUSTOM_DIR/api-design-patterns/references"
cp skills/development/api-design-patterns/SKILL.md "$SKILLS_CUSTOM_DIR/api-design-patterns/"

# Add internal API guidelines
cp ~/docs/api-standards.md "$SKILLS_CUSTOM_DIR/api-design-patterns/references/"
```

Then update the copied `SKILL.md` to reference the new file:

```markdown
See `references/api-standards.md` for our internal API conventions.
```

## Validation

Custom skills are validated with the same rules as built-in skills. Run the validator against your custom directory:

```bash
python3 scripts/validate_skills.py --collection all
```

The `SKILLS_CUSTOM_DIR` must contain valid skill directories with proper `SKILL.md` frontmatter.

## Compatibility

The following tools honor `SKILLS_CUSTOM_DIR`:

- MCP skill server (reads custom skills at startup)
- Registry and search tools (index custom skills alongside built-in ones)
- Generated bundles (custom skills are not included in `.build/` outputs)

Custom skills are local to your machine. They are not included in generated bundles or published artifacts.

## See Also

- [Creating Skills](creating-skills.md) -- How to write a new skill
- [Skill Specification](../api/skill-spec.md) -- Frontmatter format reference
- [Core vs Community Tiers](core-vs-community.md) -- Quality tiers for built-in skills
