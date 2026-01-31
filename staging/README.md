# Staging Directory

This directory contains work-in-progress materials that may be promoted to skills or absorbed into existing skills.

## Contents

- **`.skill` files**: Draft skill definitions being refined
- **`.md` files**: Research documents and reference material
- **`.zip` files**: Archived content for potential extraction

## Promotion Workflow

### 1. Research Phase
Raw research and ideas are collected here as markdown files.

### 2. Draft Phase
When research matures, create a `.skill` file with:
- Initial frontmatter (name, description, license)
- Core instructions draft
- Identified reference materials

### 3. Review Phase
Before promotion, verify:
- [ ] Frontmatter follows [skill-spec.md](../docs/api/skill-spec.md)
- [ ] No duplicate of existing skill
- [ ] Clear value proposition
- [ ] References are properly formatted

### 4. Promotion
To promote a draft to a full skill:

```bash
# 1. Create skill directory in appropriate category
mkdir -p skills/{category}/{skill-name}/

# 2. Move and rename the skill file
mv staging/{skill-name}.skill skills/{category}/{skill-name}/SKILL.md

# 3. Add references (if any)
mkdir skills/{category}/{skill-name}/references/
mv staging/related-research.md skills/{category}/{skill-name}/references/

# 4. Validate
python3 scripts/validate_skills.py --collection example --unique

# 5. Refresh collections
python3 scripts/refresh_skill_collections.py
```

### 5. Cleanup
After promotion:
- Remove original `.skill` file from staging
- Archive or remove absorbed research documents
- Update skill counts in documentation

## Absorbing Research into Existing Skills

Some research documents enhance existing skills rather than becoming new skills:

```bash
# Add research as a reference document
cp staging/research-doc.md skills/{category}/{skill-name}/references/

# Update the skill's SKILL.md to reference the new document
# Then validate and refresh
```

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Draft skill | `{skill-name}.skill` | `api-design-patterns.skill` |
| Research | `{Topic} Research.md` | `GitHub README Best Practices Research.md` |
| Framework | `{Framework-Name}.md` | `Creative-Leadership-Framework.md` |
| Archive | `{descriptive-name}.zip` | `claude-skills-set-a.zip` |

## Current Staging Contents

This directory may contain:
- Skills being refined before promotion
- Research documents awaiting absorption
- Archived skill bundles for reference
- Framework documents exploring new concepts

---

**Note**: This directory is not validated by CI. Files here are works-in-progress and may not follow the standard skill format.
