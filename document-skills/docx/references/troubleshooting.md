# DOCX Troubleshooting Guide

Common issues and solutions when working with Word documents.

## File Opening Issues

### Cannot Open Document

**Symptoms**: `PackageNotFoundError` or `BadZipFile`

**Causes**:
1. File is corrupted
2. File is not a valid .docx (might be .doc)
3. File is encrypted/password protected

**Solutions**:

Check file type:
```python
import zipfile

def is_valid_docx(path: str) -> bool:
    """Check if file is a valid DOCX."""
    try:
        with zipfile.ZipFile(path, 'r') as z:
            return 'word/document.xml' in z.namelist()
    except zipfile.BadZipFile:
        return False
```

For .doc files (older format):
```python
# Use alternative library for .doc
import textract
text = textract.process("file.doc")

# Or convert with LibreOffice
import subprocess
subprocess.run(['libreoffice', '--headless', '--convert-to', 'docx', 'file.doc'])
```

### Permission Denied

**Symptoms**: `PermissionError: [Errno 13]`

**Causes**: File is open in another application.

**Solutions**:
```python
import shutil
from tempfile import NamedTemporaryFile

def safe_open_document(path: str):
    """Open document even if original is locked."""
    with NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
        shutil.copy2(path, tmp.name)
        return Document(tmp.name)
```

## Formatting Issues

### Formatting Lost After Save

**Symptoms**: Styles, fonts, or colors don't persist.

**Causes**: Direct formatting vs style-based formatting.

**Solutions**:
```python
# Apply formatting to runs, not paragraphs
para = doc.add_paragraph()
run = para.add_run("Text")
run.bold = True
run.font.size = Pt(12)

# Or use styles
para = doc.add_paragraph("Text", style="Heading 1")
```

### Wrong Font Displayed

**Symptoms**: Document uses different font than specified.

**Solutions**:
```python
from docx.shared import Pt
from docx.oxml.ns import qn

def set_font_reliably(run, font_name: str, size_pt: int):
    """Set font that works across systems."""
    run.font.name = font_name
    run.font.size = Pt(size_pt)

    # Also set East Asian font for full compatibility
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
```

### Paragraph Spacing Issues

**Symptoms**: Unexpected spacing between paragraphs.

**Solutions**:
```python
from docx.shared import Pt

para = doc.add_paragraph("Text")
para_format = para.paragraph_format
para_format.space_before = Pt(0)
para_format.space_after = Pt(0)
para_format.line_spacing = 1.0
```

## Table Issues

### Merged Cells Not Working

**Symptoms**: `merge` method doesn't combine cells properly.

**Solutions**:
```python
from docx import Document

def merge_cells(table, start_row, start_col, end_row, end_col):
    """Merge cells in a range."""
    start_cell = table.cell(start_row, start_col)
    end_cell = table.cell(end_row, end_col)
    start_cell.merge(end_cell)
```

### Table Width Not Respected

**Symptoms**: Table doesn't fill page width.

**Solutions**:
```python
from docx.shared import Inches, Twips
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_table_width(table, width_inches: float):
    """Set table to specific width."""
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:type'), 'dxa')
    tblW.set(qn('w:w'), str(int(width_inches * 1440)))  # 1440 twips per inch
    tblPr.append(tblW)
```

## Image Issues

### Image Not Displaying

**Symptoms**: Image placeholder appears but no image.

**Causes**: Invalid image path or unsupported format.

**Solutions**:
```python
from docx import Document
from docx.shared import Inches
from PIL import Image
import io

def add_image_safely(doc, image_path: str, width_inches: float = 4):
    """Add image with format conversion if needed."""
    try:
        # Try direct addition
        doc.add_picture(image_path, width=Inches(width_inches))
    except Exception:
        # Convert to PNG first
        img = Image.open(image_path)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        doc.add_picture(buffer, width=Inches(width_inches))
```

### Image Quality Loss

**Symptoms**: Images appear blurry or pixelated.

**Solutions**:
```python
# Don't compress images
doc.add_picture(image_path, width=Inches(6))  # Use larger size

# Or use original resolution without width constraint
doc.add_picture(image_path)
```

## Header/Footer Issues

### Different First Page Header

**Symptoms**: Can't set different header for first page.

**Solutions**:
```python
def set_different_first_header(doc, first_header: str, other_header: str):
    """Set different header for first page."""
    section = doc.sections[0]
    section.different_first_page_header_footer = True

    # First page header
    first_header_obj = section.first_page_header
    first_header_obj.paragraphs[0].text = first_header

    # Other pages header
    header = section.header
    header.paragraphs[0].text = other_header
```

### Page Numbers Not Working

**Solutions**:
```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_page_number(para):
    """Add page number field to paragraph."""
    run = para.add_run()
    fld_char_begin = OxmlElement('w:fldChar')
    fld_char_begin.set(qn('w:fldCharType'), 'begin')

    instr_text = OxmlElement('w:instrText')
    instr_text.set(qn('xml:space'), 'preserve')
    instr_text.text = "PAGE"

    fld_char_end = OxmlElement('w:fldChar')
    fld_char_end.set(qn('w:fldCharType'), 'end')

    run._r.append(fld_char_begin)
    run._r.append(instr_text)
    run._r.append(fld_char_end)
```

## Find/Replace Issues

### Replace Not Finding Text

**Symptoms**: Text exists but replace doesn't work.

**Causes**: Text is split across multiple runs.

**Solutions**:
```python
def find_replace_robust(doc, find: str, replace: str):
    """Replace text even when split across runs."""
    for para in doc.paragraphs:
        if find in para.text:
            # Combine all runs
            full_text = para.text
            new_text = full_text.replace(find, replace)

            # Clear existing runs
            for run in para.runs:
                run.text = ""

            # Add new text to first run
            if para.runs:
                para.runs[0].text = new_text
            else:
                para.add_run(new_text)
```

## Memory Issues

### Out of Memory on Large Documents

**Solutions**:
```python
# Process sections instead of entire document
from docx import Document

def process_large_doc(path: str):
    """Process large document efficiently."""
    doc = Document(path)

    # Process paragraphs one at a time
    for para in doc.paragraphs:
        # Process paragraph
        yield para.text

    # Explicitly close to release memory
    del doc
```

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `PackageNotFoundError` | Not a valid DOCX | Check file format |
| `KeyError: 'word/document.xml'` | Corrupted DOCX | Try repair with Word |
| `AttributeError: 'NoneType'` | Missing element | Check if object exists first |
| `ValueError: Paragraph.style` | Invalid style name | Use existing style |
| `BadZipFile` | File corrupted | Re-download or restore |

## Compatibility Tips

### Cross-Platform Fonts

```python
# Use fonts available on all platforms
SAFE_FONTS = [
    'Arial',
    'Times New Roman',
    'Calibri',
    'Verdana',
    'Georgia'
]
```

### Save for Older Word Versions

```python
# DOCX is compatible with Word 2007+
# For older versions, consider PDF export

from docx2pdf import convert
convert("input.docx", "output.pdf")
```
