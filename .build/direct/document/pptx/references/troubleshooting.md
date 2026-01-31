# PPTX Troubleshooting Guide

Common issues and solutions when working with PowerPoint presentations.

## File Opening Issues

### Cannot Open File

**Symptoms**: `PackageNotFoundError` or `BadZipFile`

**Causes**:
1. File is corrupted
2. File is .ppt (older format), not .pptx
3. File is password protected

**Solutions**:

Check file type:
```python
import zipfile

def is_valid_pptx(path: str) -> bool:
    """Check if file is a valid PPTX."""
    try:
        with zipfile.ZipFile(path, 'r') as z:
            return 'ppt/presentation.xml' in z.namelist()
    except zipfile.BadZipFile:
        return False
```

Convert .ppt to .pptx:
```bash
# Using LibreOffice
libreoffice --headless --convert-to pptx old_file.ppt
```

### Permission Denied

**Symptoms**: `PermissionError`

**Solutions**:
```python
import shutil
from tempfile import NamedTemporaryFile

def open_locked_pptx(path: str):
    """Open presentation even if locked."""
    with NamedTemporaryFile(delete=False, suffix='.pptx') as tmp:
        shutil.copy2(path, tmp.name)
        return Presentation(tmp.name)
```

## Layout Issues

### Placeholder Not Found

**Symptoms**: `KeyError` when accessing placeholder

**Solutions**:
```python
def find_placeholder(slide, placeholder_type):
    """Find placeholder by type."""
    from pptx.enum.shapes import MSO_SHAPE_TYPE

    for shape in slide.shapes:
        if shape.is_placeholder:
            if shape.placeholder_format.type == placeholder_type:
                return shape
    return None

# List all placeholders
def list_placeholders(slide):
    for shape in slide.shapes:
        if shape.is_placeholder:
            ph = shape.placeholder_format
            print(f"Index: {ph.idx}, Type: {ph.type}")
```

### Wrong Slide Layout

**Symptoms**: Content doesn't appear in expected positions.

**Solutions**:
```python
def list_layouts(prs):
    """List all available slide layouts."""
    for i, layout in enumerate(prs.slide_layouts):
        print(f"{i}: {layout.name}")
        for shape in layout.placeholders:
            print(f"  - {shape.placeholder_format.idx}: {shape.name}")
```

## Text Formatting Issues

### Font Not Applied

**Symptoms**: Text uses default font instead of specified.

**Causes**: Font not available on system or applied to wrong element.

**Solutions**:
```python
from pptx.util import Pt

def set_font_reliably(text_frame, font_name: str, size: int):
    """Set font for all text in text frame."""
    for paragraph in text_frame.paragraphs:
        for run in paragraph.runs:
            run.font.name = font_name
            run.font.size = Pt(size)
```

### Text Overflow

**Symptoms**: Text gets cut off or doesn't fit.

**Solutions**:
```python
from pptx.util import Pt
from pptx.enum.text import MSO_AUTO_SIZE

def auto_fit_text(shape):
    """Enable text auto-fit."""
    shape.text_frame.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT

# Or manually adjust
def shrink_text(shape, min_size: int = 10):
    """Shrink text to fit."""
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            current_size = run.font.size.pt if run.font.size else 18
            run.font.size = Pt(max(min_size, current_size - 2))
```

### Line Spacing Issues

**Solutions**:
```python
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN

def set_paragraph_spacing(paragraph, before: int = 0, after: int = 0,
                          line_spacing: float = 1.0):
    """Set paragraph spacing."""
    paragraph.space_before = Pt(before)
    paragraph.space_after = Pt(after)
    paragraph.line_spacing = line_spacing
```

## Image Issues

### Image Not Displaying

**Symptoms**: Empty placeholder where image should be.

**Causes**: Invalid image path or unsupported format.

**Solutions**:
```python
from PIL import Image
from io import BytesIO

def add_image_safely(slide, image_path: str, left, top, width):
    """Add image with format conversion if needed."""
    try:
        slide.shapes.add_picture(image_path, left, top, width=width)
    except Exception:
        # Convert to PNG
        img = Image.open(image_path)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        slide.shapes.add_picture(buffer, left, top, width=width)
```

### Image Quality Loss

**Symptoms**: Images appear blurry.

**Solutions**:
```python
# Don't resize on insert - use original dimensions
slide.shapes.add_picture(image_path, left, top)

# Or use higher resolution source
# DPI should be at least 150 for presentations
```

## Chart Issues

### Chart Data Not Updating

**Symptoms**: Chart shows old data.

**Solutions**:
```python
def update_chart_data(chart, categories, series_data):
    """Update existing chart data."""
    chart_data = chart.chart_data

    # Clear existing
    while len(chart_data.categories) > 0:
        chart_data.categories.pop()

    # Add new data
    chart_data.categories = categories
    for series in chart_data.series:
        series.values = series_data[series.name]
```

### Chart Type Not Supported

**Symptoms**: `ValueError` when creating chart.

**Solutions**:
```python
from pptx.enum.chart import XL_CHART_TYPE

# Supported chart types:
SUPPORTED_CHARTS = [
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    XL_CHART_TYPE.COLUMN_STACKED,
    XL_CHART_TYPE.BAR_CLUSTERED,
    XL_CHART_TYPE.LINE,
    XL_CHART_TYPE.PIE,
    XL_CHART_TYPE.AREA,
    XL_CHART_TYPE.SCATTER,
]
```

## Table Issues

### Table Formatting Lost

**Symptoms**: Table style doesn't persist.

**Solutions**:
```python
def style_table_cells(table, header_color, body_color):
    """Apply consistent table styling."""
    from pptx.dml.color import RGBColor

    for i, row in enumerate(table.rows):
        for cell in row.cells:
            cell.fill.solid()
            if i == 0:  # Header row
                cell.fill.fore_color.rgb = RGBColor(*header_color)
            else:
                cell.fill.fore_color.rgb = RGBColor(*body_color)
```

### Cell Merging Issues

**Symptoms**: Merged cells don't display correctly.

**Solutions**:
```python
def merge_cells(table, start_row, start_col, end_row, end_col):
    """Merge table cells safely."""
    start_cell = table.cell(start_row, start_col)
    end_cell = table.cell(end_row, end_col)
    start_cell.merge(end_cell)
```

## Slide Operations Issues

### Slide Copy Not Working

**Symptoms**: Copied slide is blank or missing elements.

**Solutions**:
```python
from copy import deepcopy
from pptx.parts.slide import Slide

def copy_slide(prs, index):
    """Copy slide with all content."""
    source = prs.slides[index]

    # Get slide layout
    layout = source.slide_layout

    # Add new slide
    new_slide = prs.slides.add_slide(layout)

    # Copy each shape
    for shape in source.shapes:
        el = deepcopy(shape.element)
        new_slide.shapes._spTree.insert_element_before(el, 'p:extLst')

    return new_slide
```

## Memory Issues

### Out of Memory on Large Presentations

**Solutions**:
```python
# Process slides one at a time
def process_large_pptx(path: str):
    """Process large presentation efficiently."""
    prs = Presentation(path)

    for slide in prs.slides:
        # Process slide
        process_slide(slide)

        # Clear references
        del slide

    # Save and close
    prs.save('output.pptx')
    del prs
```

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `PackageNotFoundError` | Not a valid pptx | Check file format |
| `KeyError: idx` | Invalid placeholder index | List available placeholders |
| `ValueError: not a valid layout` | Wrong layout reference | Use `slide_layouts` index |
| `AttributeError: 'NoneType'` | Missing object | Check if object exists |
| `BadZipFile` | Corrupted file | Re-download or repair |

## Performance Tips

### Speed Up Processing

```python
# Avoid loading large images multiple times
from functools import lru_cache

@lru_cache(maxsize=32)
def load_image(path):
    with open(path, 'rb') as f:
        return f.read()
```

### Reduce File Size

```python
# Compress images before adding
from PIL import Image

def compress_image(image_path: str, quality: int = 85) -> BytesIO:
    """Compress image for smaller file size."""
    img = Image.open(image_path)
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=quality, optimize=True)
    buffer.seek(0)
    return buffer
```

## Compatibility

### Cross-Platform Fonts

```python
# Use fonts available on all platforms
SAFE_FONTS = [
    'Arial',
    'Times New Roman',
    'Calibri',
    'Verdana',
]
```

### PowerPoint Version Compatibility

```python
# PPTX format is compatible with:
# - PowerPoint 2007 and later
# - Google Slides
# - LibreOffice Impress
# - Keynote (with some limitations)

# Avoid features that may not work everywhere:
# - Embedded videos (use links instead)
# - Complex animations
# - 3D effects
# - ActiveX controls
```
