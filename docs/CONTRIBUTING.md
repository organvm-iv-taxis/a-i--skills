# Contributing

Thanks for contributing to this skills repository. Each skill is a self-contained folder with a `SKILL.md` entrypoint. Follow the steps below to keep the collections consistent across Claude Code, Codex, and Gemini CLI.

## Add or Update a Skill
1. Choose the appropriate category subdirectory in `skills/` (see [CATEGORIES.md](CATEGORIES.md) for the list).
2. Create a new folder using kebab-case (e.g., `skills/development/my-new-skill/`).
3. Add `SKILL.md` with YAML frontmatter:
   - `name:` must match the folder name.
   - `description:` short, specific, and task-focused (20-600 chars).
   - `license:` required (use `MIT` for open-source skills).
4. Add optional semantic fields to improve discoverability and enable composition:
   - `inputs:` what the skill expects (e.g., `[source-code, openapi-spec]`)
   - `outputs:` what the skill produces (e.g., `[test-report, mcp-server-code]`)
   - `side_effects:` environment changes (values: `creates-files`, `modifies-git`, `runs-commands`, `network-access`, `installs-packages`, `reads-filesystem`)
   - `triggers:` activation conditions (see [Activation Conditions](api/activation-conditions.md))
   - `complements:` skills that pair well (list of skill names)
   - `tier:` quality tier (`core` or `community`)
5. Put helper scripts in `scripts/` and any supporting material in `references/` or `assets/`.

For detailed guidance, see [Creating Skills](guides/creating-skills.md) and the [Skill Specification](api/skill-spec.md).

## Skill Bundles

To create a skill bundle (a pack that groups related skills):

1. Create a skill directory like any other skill.
2. Add an `includes:` field listing the skill names to bundle (all must exist in the repo).
3. The SKILL.md body should describe the bundle's purpose and list the included skills.

Example: `skills/development/fullstack-starter-pack/` bundles 6 development skills.

## Quality Tiers

Skills can be tagged with `tier: core` or `tier: community`:

- **Core**: Curated, reviewed skills with stricter validation (must have `complexity`, `time_to_learn`, `tags`).
- **Community**: Contributed skills with standard validation.

See [Core vs Community](guides/core-vs-community.md) for the promotion path and quality gates.

## Refresh Collections
Run after adding/removing skills:

```bash
python3 scripts/refresh_skill_collections.py
```
Use `--mode symlink` if you prefer symlinks instead of copies.

This regenerates:
- `.build/collections/example-skills.txt` and `document-skills.txt`
- `.build/collections/core-skills.txt` and `community-skills.txt` (tier lists)
- `.build/skills-registry.json` (machine-readable registry)
- `.build/skills-lock.json` (lockfile with SHA-256 hashes)
- Link directories under `.build/claude/skills`, `.build/codex/skills`, and `.build/extensions/gemini/*/skills`

These generated files are committed to the repo. Include the updated outputs in your PRs.

## Validate
Ensure the frontmatter and naming rules are correct:

```bash
python3 scripts/validate_skills.py --collection example --unique
python3 scripts/validate_skills.py --collection document --unique
python3 scripts/validate_generated_dirs.py
```

Run health checks to verify scripts, references, and resource integrity:

```bash
python3 scripts/skill_health_check.py                    # All skills
python3 scripts/skill_health_check.py --skill mcp-builder  # Single skill
```

## Commit Guidance
- Use short, imperative subject lines (e.g., "Add prompt for X" or "Update README for Y").
- If a change affects a curated list or install flow, update `README.md`.
- Add third-party attributions to `THIRD_PARTY_NOTICES.md` when you introduce external assets or data.

## Gemini / Codex / Claude Code Notes
- Install only one collection at a time to avoid duplicate skill names (e.g., `docx`, `pdf` exist in both sets).
- Gemini CLI extensions live under `.build/extensions/gemini/` and point to the generated `skills/` links.
- Codex and Claude Code load skills from `.build/codex/skills` and `.build/claude/skills` respectively.

## Release Checklist
1. Run refresh + validation:
   ```bash
   python3 scripts/refresh_skill_collections.py
   python3 scripts/validate_skills.py --collection example --unique
   python3 scripts/validate_skills.py --collection document --unique
   ```
2. Update `CHANGELOG.md` with the release summary.
3. Bump versions in:
   - `.claude-plugin/marketplace.json` (`metadata.version`)
   - `extensions/gemini/example-skills/gemini-extension.json`
   - `extensions/gemini/document-skills/gemini-extension.json`
4. Update `README.md` if install steps or collection membership changed.
5. Verify CI passes (`.github/workflows/validate-skills.yml`).
6. Tag and publish, then create a release (prefer `gh release create vX.Y.Z --generate-notes` or attach the changelog section as notes).

Optional: use the release helper to do steps 1-6 automatically:

```bash
python3 scripts/release.py 1.2.0 \\
  --change \"Describe the release\" \\
  --add \"New capability\" \\
  --fix \"Bug fix summary\" \\
  --commit --tag --push --release --notes-from-changelog
```
