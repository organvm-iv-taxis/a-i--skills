# Document Skills

Reference implementations for document processing with Claude Code.

## Overview

These skills provide Claude with specialized knowledge for working with common document formats. They are designed specifically for Claude Code's capabilities and may require specific tools or libraries.

## Available Skills

| Skill | Description | Key Libraries |
|-------|-------------|---------------|
| [pdf](pdf/) | PDF manipulation, form filling, text extraction | pypdf, pdf2image, PyMuPDF |
| [docx](docx/) | Word document creation and manipulation | python-docx |
| [xlsx](xlsx/) | Excel spreadsheet processing | openpyxl, pandas |
| [pptx](pptx/) | PowerPoint presentation creation | python-pptx |

## Important Notes

### Claude Code Specific

These skills are optimized for Claude Code and may not work identically with other AI agents. They assume:

- Access to Python environment
- Ability to install packages via pip
- File system access for reading/writing documents
- Script execution capabilities

### Reference Implementations

Document skills serve as **reference implementations** demonstrating:

- Best practices for document manipulation
- Common patterns and workflows
- Error handling approaches
- Library-specific techniques

They are intentionally detailed and technical, providing Claude with the exact code patterns needed for reliable document processing.

### Limitations

1. **Binary format handling**: Document formats are binary; Claude cannot directly "read" them without using these tools
2. **Library dependencies**: Each skill requires specific Python libraries
3. **Platform considerations**: Some operations (e.g., PDF rendering) may require system libraries
4. **Large files**: Memory constraints apply when processing large documents

## Usage

### With Claude Code

Claude Code automatically uses these skills when you ask for document operations:

```
"Extract text from this PDF"
→ Uses pdf skill

"Create a Word document with this content"
→ Uses docx skill

"Build a spreadsheet from this data"
→ Uses xlsx skill
```

### Manual Invocation

You can also explicitly request a skill:

```
"Using the pdf skill, fill out this form"
"Apply the xlsx skill to analyze this spreadsheet"
```

## Structure

Each document skill contains:

```
{format}/
├── SKILL.md          # Main skill instructions
├── references/       # Additional documentation
│   ├── forms.md      # (pdf) Form handling
│   ├── reference.md  # Advanced techniques
│   └── ...
├── scripts/          # Helper scripts (optional)
└── assets/           # Templates/resources (optional)
```

## Differences from Example Skills

| Aspect | Example Skills | Document Skills |
|--------|---------------|-----------------|
| Location | `skills/` | `document-skills/` |
| Purpose | General workflows | Specific format handling |
| Complexity | Varies | Technical/detailed |
| Dependencies | Minimal | Library-specific |
| License | MIT (open) | Proprietary |
| Collection | `example-skills.txt` | `document-skills.txt` |

## Contributing

Document skills require careful testing with actual documents. When contributing:

1. Test with real-world documents of varying complexity
2. Handle edge cases (encrypted, corrupted, large files)
3. Document library version requirements
4. Include error handling patterns

See [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for general contribution guidelines.

## License

Document skills are **proprietary** and subject to the license terms in each skill's `LICENSE.txt` file. They are provided as part of this repository for use with Claude Code.
