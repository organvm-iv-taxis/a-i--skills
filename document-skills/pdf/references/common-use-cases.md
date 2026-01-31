# PDF Common Use Cases

Practical recipes for common PDF processing tasks.

## Text Extraction

### Extract All Text from PDF

```python
from pypdf import PdfReader

def extract_text(pdf_path: str) -> str:
    """Extract all text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
```

### Extract Text by Page

```python
def extract_text_by_page(pdf_path: str) -> dict[int, str]:
    """Extract text from each page separately."""
    reader = PdfReader(pdf_path)
    return {i: page.extract_text() for i, page in enumerate(reader.pages)}
```

## Merging PDFs

### Merge Multiple PDFs

```python
from pypdf import PdfWriter, PdfReader

def merge_pdfs(input_paths: list[str], output_path: str) -> None:
    """Merge multiple PDF files into one."""
    writer = PdfWriter()
    for path in input_paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
```

### Merge with Page Range Selection

```python
def merge_selective(
    files: list[tuple[str, int | None, int | None]],
    output_path: str
) -> None:
    """Merge PDFs with optional page ranges.

    Args:
        files: List of (path, start_page, end_page) tuples.
               Use None for start/end to include all pages.
    """
    writer = PdfWriter()
    for path, start, end in files:
        reader = PdfReader(path)
        pages = reader.pages[start:end]
        for page in pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
```

## Splitting PDFs

### Split into Individual Pages

```python
def split_pages(pdf_path: str, output_dir: str) -> list[str]:
    """Split a PDF into individual page files."""
    from pathlib import Path

    reader = PdfReader(pdf_path)
    output_paths = []

    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        output_path = Path(output_dir) / f"page_{i+1:03d}.pdf"
        with open(output_path, "wb") as f:
            writer.write(f)
        output_paths.append(str(output_path))

    return output_paths
```

### Split by Page Ranges

```python
def split_by_ranges(
    pdf_path: str,
    ranges: list[tuple[int, int]],
    output_dir: str
) -> list[str]:
    """Split a PDF by page ranges."""
    from pathlib import Path

    reader = PdfReader(pdf_path)
    output_paths = []

    for i, (start, end) in enumerate(ranges):
        writer = PdfWriter()
        for page in reader.pages[start:end]:
            writer.add_page(page)
        output_path = Path(output_dir) / f"section_{i+1}.pdf"
        with open(output_path, "wb") as f:
            writer.write(f)
        output_paths.append(str(output_path))

    return output_paths
```

## PDF Metadata

### Read Metadata

```python
def get_metadata(pdf_path: str) -> dict:
    """Get PDF metadata."""
    reader = PdfReader(pdf_path)
    return {
        "title": reader.metadata.title,
        "author": reader.metadata.author,
        "subject": reader.metadata.subject,
        "creator": reader.metadata.creator,
        "producer": reader.metadata.producer,
        "page_count": len(reader.pages),
    }
```

### Update Metadata

```python
def update_metadata(pdf_path: str, output_path: str, metadata: dict) -> None:
    """Update PDF metadata."""
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata(metadata)

    with open(output_path, "wb") as f:
        writer.write(f)
```

## PDF Rotation

### Rotate All Pages

```python
def rotate_all(pdf_path: str, output_path: str, degrees: int) -> None:
    """Rotate all pages in a PDF."""
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(degrees)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)
```

## Table Extraction

### Extract Tables with pdfplumber

```python
import pdfplumber

def extract_tables(pdf_path: str) -> list[list[list[str]]]:
    """Extract tables from all pages."""
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            tables.extend(page_tables)
    return tables
```

### Convert Tables to DataFrame

```python
import pdfplumber
import pandas as pd

def tables_to_dataframes(pdf_path: str) -> list[pd.DataFrame]:
    """Extract tables as pandas DataFrames."""
    dfs = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    dfs.append(df)
    return dfs
```

## PDF to Image

### Convert Pages to Images

```python
from pdf2image import convert_from_path

def pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 300) -> list[str]:
    """Convert PDF pages to PNG images."""
    from pathlib import Path

    images = convert_from_path(pdf_path, dpi=dpi)
    output_paths = []

    for i, image in enumerate(images):
        output_path = Path(output_dir) / f"page_{i+1:03d}.png"
        image.save(output_path, "PNG")
        output_paths.append(str(output_path))

    return output_paths
```

## Creating PDFs

### Create Simple PDF with ReportLab

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_simple_pdf(output_path: str, text: str) -> None:
    """Create a simple PDF with text."""
    c = canvas.Canvas(output_path, pagesize=letter)
    c.drawString(72, 720, text)
    c.save()
```

### Create Multi-Page PDF

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_document(output_path: str, paragraphs: list[str]) -> None:
    """Create a multi-page PDF document."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()

    story = [Paragraph(text, styles["Normal"]) for text in paragraphs]
    doc.build(story)
```
