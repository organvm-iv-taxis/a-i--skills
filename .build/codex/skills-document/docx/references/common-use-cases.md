# DOCX Common Use Cases

Practical recipes for common Word document tasks.

## Document Creation

### Create Basic Document

```python
from docx import Document
from docx.shared import Inches, Pt

def create_document(output_path: str, title: str, content: list[str]) -> None:
    """Create a basic Word document."""
    doc = Document()

    # Add title
    doc.add_heading(title, level=0)

    # Add paragraphs
    for text in content:
        doc.add_paragraph(text)

    doc.save(output_path)
```

### Create Document with Formatting

```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_formatted_doc(output_path: str) -> None:
    """Create document with formatting."""
    doc = Document()

    # Title with styling
    title = doc.add_heading("Document Title", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Formatted paragraph
    para = doc.add_paragraph()
    run = para.add_run("Bold text")
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0, 0, 128)

    para.add_run(" and ")

    run2 = para.add_run("italic text")
    run2.italic = True

    doc.save(output_path)
```

## Text Extraction

### Extract All Text

```python
from docx import Document

def extract_text(docx_path: str) -> str:
    """Extract all text from a Word document."""
    doc = Document(docx_path)
    text = []

    for para in doc.paragraphs:
        text.append(para.text)

    return "\n".join(text)
```

### Extract Text with Formatting Info

```python
def extract_with_formatting(docx_path: str) -> list[dict]:
    """Extract text with formatting information."""
    doc = Document(docx_path)
    content = []

    for para in doc.paragraphs:
        para_info = {
            "text": para.text,
            "style": para.style.name,
            "runs": []
        }
        for run in para.runs:
            run_info = {
                "text": run.text,
                "bold": run.bold,
                "italic": run.italic,
                "font_size": run.font.size.pt if run.font.size else None
            }
            para_info["runs"].append(run_info)
        content.append(para_info)

    return content
```

## Tables

### Create Table

```python
from docx import Document
from docx.shared import Inches

def create_table(output_path: str, headers: list[str], rows: list[list[str]]) -> None:
    """Create document with a table."""
    doc = Document()

    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"

    # Add headers
    for i, header in enumerate(headers):
        table.rows[0].cells[i].text = header

    # Add data rows
    for row_data in rows:
        row = table.add_row()
        for i, cell_data in enumerate(row_data):
            row.cells[i].text = str(cell_data)

    doc.save(output_path)
```

### Extract Tables

```python
def extract_tables(docx_path: str) -> list[list[list[str]]]:
    """Extract all tables from document."""
    doc = Document(docx_path)
    tables = []

    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = [cell.text for cell in row.cells]
            table_data.append(row_data)
        tables.append(table_data)

    return tables
```

## Images

### Add Image

```python
from docx import Document
from docx.shared import Inches

def add_image(docx_path: str, image_path: str, output_path: str) -> None:
    """Add image to document."""
    doc = Document(docx_path)

    doc.add_paragraph("Image:")
    doc.add_picture(image_path, width=Inches(4))

    doc.save(output_path)
```

### Extract Images

```python
from docx import Document
from pathlib import Path

def extract_images(docx_path: str, output_dir: str) -> list[str]:
    """Extract all images from document."""
    doc = Document(docx_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    image_paths = []
    for i, rel in enumerate(doc.part.rels.values()):
        if "image" in rel.target_ref:
            image_data = rel.target_part.blob
            ext = rel.target_ref.split(".")[-1]
            image_path = output_dir / f"image_{i}.{ext}"
            image_path.write_bytes(image_data)
            image_paths.append(str(image_path))

    return image_paths
```

## Headers and Footers

### Add Header and Footer

```python
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_header_footer(docx_path: str, output_path: str,
                      header_text: str, footer_text: str) -> None:
    """Add header and footer to document."""
    doc = Document(docx_path)

    # Get or create section
    section = doc.sections[0]

    # Header
    header = section.header
    header_para = header.paragraphs[0]
    header_para.text = header_text
    header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Footer
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.text = footer_text
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.save(output_path)
```

## Find and Replace

### Simple Replace

```python
def find_replace(docx_path: str, output_path: str,
                 find_text: str, replace_text: str) -> None:
    """Find and replace text in document."""
    doc = Document(docx_path)

    for para in doc.paragraphs:
        if find_text in para.text:
            for run in para.runs:
                run.text = run.text.replace(find_text, replace_text)

    doc.save(output_path)
```

### Replace with Formatting Preservation

```python
def replace_preserving_format(docx_path: str, output_path: str,
                               replacements: dict[str, str]) -> None:
    """Replace text while preserving formatting."""
    doc = Document(docx_path)

    for para in doc.paragraphs:
        for run in para.runs:
            for find_text, replace_text in replacements.items():
                if find_text in run.text:
                    run.text = run.text.replace(find_text, replace_text)

    # Also check tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for run in para.runs:
                        for find_text, replace_text in replacements.items():
                            if find_text in run.text:
                                run.text = run.text.replace(find_text, replace_text)

    doc.save(output_path)
```

## Styles

### Apply Styles

```python
from docx import Document
from docx.enum.style import WD_STYLE_TYPE

def create_styled_doc(output_path: str) -> None:
    """Create document with various styles."""
    doc = Document()

    doc.add_heading("Heading 1", level=1)
    doc.add_heading("Heading 2", level=2)
    doc.add_heading("Heading 3", level=3)

    doc.add_paragraph("Normal paragraph text.")

    para = doc.add_paragraph("Quoted text.", style="Quote")

    para = doc.add_paragraph("List item 1", style="List Bullet")
    para = doc.add_paragraph("List item 2", style="List Bullet")

    doc.save(output_path)
```

## Page Setup

### Configure Page Layout

```python
from docx import Document
from docx.shared import Inches

def set_page_layout(output_path: str) -> None:
    """Configure page layout."""
    doc = Document()

    section = doc.sections[0]

    # Page size (Letter)
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)

    # Margins
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)

    doc.add_paragraph("Content with custom margins.")
    doc.save(output_path)
```

## Merge Documents

### Combine Multiple Documents

```python
from docx import Document
from docxcompose.composer import Composer

def merge_documents(input_paths: list[str], output_path: str) -> None:
    """Merge multiple Word documents."""
    if not input_paths:
        return

    master = Document(input_paths[0])
    composer = Composer(master)

    for path in input_paths[1:]:
        doc = Document(path)
        composer.append(doc)

    composer.save(output_path)
```

### Alternative Merge (without docxcompose)

```python
from docx import Document

def simple_merge(input_paths: list[str], output_path: str) -> None:
    """Simple merge by copying content."""
    merged = Document()

    for i, path in enumerate(input_paths):
        doc = Document(path)

        # Add page break between documents
        if i > 0:
            merged.add_page_break()

        for element in doc.element.body:
            merged.element.body.append(element)

    merged.save(output_path)
```
