# PDF Troubleshooting Guide

Common issues and solutions when working with PDFs.

## Text Extraction Issues

### No Text Extracted

**Symptoms**: `extract_text()` returns empty string or gibberish.

**Causes**:
1. **Scanned PDF (image-based)**: Contains images of text, not actual text
2. **Custom font encoding**: Uses non-standard character mapping
3. **Corrupted PDF**: File structure is damaged

**Solutions**:

For scanned PDFs, use OCR:
```python
import pytesseract
from pdf2image import convert_from_path

def ocr_pdf(pdf_path: str) -> str:
    """Extract text from scanned PDF using OCR."""
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text
```

For encoding issues, try different extraction methods:
```python
from pypdf import PdfReader

reader = PdfReader(pdf_path)
# Try extraction_mode parameter
text = reader.pages[0].extract_text(extraction_mode="layout")
```

### Garbled Characters / Wrong Encoding

**Symptoms**: Text contains replacement characters (�) or wrong characters.

**Solutions**:
```python
# Force UTF-8 encoding
text = page.extract_text().encode('utf-8', errors='ignore').decode('utf-8')

# Or try different library
import pdfplumber
with pdfplumber.open(pdf_path) as pdf:
    text = pdf.pages[0].extract_text()
```

## Form Handling Issues

### Form Fields Not Detected

**Symptoms**: `reader.get_form_text_fields()` returns empty dict.

**Causes**:
1. PDF has XFA forms (not AcroForms)
2. Form fields are flattened
3. PDF is protected

**Solutions**:

Check form type:
```python
reader = PdfReader(pdf_path)
if "/XFA" in reader.trailer.get("/Root", {}).get("/AcroForm", {}):
    print("XFA form detected - limited support")
```

For XFA forms, consider converting to AcroForm or using alternative tools.

### Form Values Not Saving

**Symptoms**: Filled values disappear when opening saved PDF.

**Solutions**:
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader(pdf_path)
writer = PdfWriter()

# Add all pages
for page in reader.pages:
    writer.add_page(page)

# Update form field
writer.update_page_form_field_values(
    writer.pages[0],
    {"field_name": "value"},
    auto_regenerate=False  # Important: prevent field regeneration
)

with open(output_path, "wb") as f:
    writer.write(f)
```

## Memory Issues

### Out of Memory on Large PDFs

**Symptoms**: MemoryError or system slowdown.

**Solutions**:

Process pages iteratively:
```python
from pypdf import PdfReader

def process_large_pdf(pdf_path: str):
    """Process large PDF without loading all pages."""
    reader = PdfReader(pdf_path)

    for i in range(len(reader.pages)):
        # Process one page at a time
        page = reader.pages[i]
        text = page.extract_text()
        yield text
        # Page is garbage collected when we move to next
```

For image conversion, limit DPI:
```python
# Use lower DPI for memory efficiency
images = convert_from_path(pdf_path, dpi=150, thread_count=1)
```

## Merging Issues

### Merged PDF Has Wrong Page Order

**Solutions**:
```python
# Explicitly sort files before merging
from pathlib import Path

files = sorted(Path(directory).glob("*.pdf"), key=lambda p: p.name)
merge_pdfs([str(f) for f in files], output_path)
```

### Merged PDF Is Corrupted

**Causes**: Incompatible PDF versions or encryption.

**Solutions**:
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()

for path in input_paths:
    try:
        reader = PdfReader(path)
        if reader.is_encrypted:
            reader.decrypt("")  # Try empty password
        for page in reader.pages:
            writer.add_page(page)
    except Exception as e:
        print(f"Skipping {path}: {e}")

with open(output_path, "wb") as f:
    writer.write(f)
```

## Encryption Issues

### Cannot Open Encrypted PDF

**Symptoms**: `PdfReadError: file has not been decrypted`

**Solutions**:
```python
reader = PdfReader(pdf_path)
if reader.is_encrypted:
    # Try empty password first
    if reader.decrypt(""):
        print("Decrypted with empty password")
    else:
        # Need actual password
        reader.decrypt(password)
```

### Cannot Remove Password Protection

**Solutions**:
```python
reader = PdfReader(pdf_path)
reader.decrypt(password)

writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)

# Save without encryption
with open(output_path, "wb") as f:
    writer.write(f)
```

## Poppler/pdf2image Issues

### poppler-utils Not Found

**Symptoms**: `PDFInfoNotInstalledError`

**Solutions**:

macOS:
```bash
brew install poppler
```

Ubuntu/Debian:
```bash
apt-get install poppler-utils
```

Windows: Download from poppler releases and add to PATH.

### Image Conversion Fails

**Symptoms**: `PDFPageCountError` or `PDFSyntaxError`

**Solutions**:
```python
# Try with strict=False
images = convert_from_path(pdf_path, strict=False)

# Or use PyMuPDF as alternative
import fitz
doc = fitz.open(pdf_path)
for page in doc:
    pix = page.get_pixmap()
    pix.save(f"page_{page.number}.png")
```

## Performance Tips

### Speed Up Bulk Processing

```python
from concurrent.futures import ProcessPoolExecutor

def process_pdf(path):
    # Your processing logic
    pass

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_pdf, pdf_paths))
```

### Reduce Output File Size

```python
writer = PdfWriter()
# Add pages...

# Compress content streams
for page in writer.pages:
    page.compress_content_streams()

with open(output_path, "wb") as f:
    writer.write(f)
```

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `PdfReadError: EOF marker not found` | Truncated/corrupted file | Re-download or repair PDF |
| `PyPDF2.utils.PdfReadError: Illegal character` | Invalid PDF structure | Try `strict=False` |
| `DependencyNotAvailable: pdftotext` | Missing poppler | Install poppler-utils |
| `ValueError: invalid mode` | Wrong parameter type | Check function signature |
