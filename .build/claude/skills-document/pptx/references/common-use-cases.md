# PPTX Common Use Cases

Practical recipes for common PowerPoint tasks.

## Creating Presentations

### Create Basic Presentation

```python
from pptx import Presentation
from pptx.util import Inches, Pt

def create_presentation(output_path: str, title: str, slides_content: list[dict]) -> None:
    """Create basic presentation with title and content slides."""
    prs = Presentation()

    # Title slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    slide.shapes.title.text = title
    slide.placeholders[1].text = "Subtitle text"

    # Content slides
    content_layout = prs.slide_layouts[1]  # Title and Content
    for content in slides_content:
        slide = prs.slides.add_slide(content_layout)
        slide.shapes.title.text = content.get('title', '')
        slide.placeholders[1].text = content.get('body', '')

    prs.save(output_path)
```

### Create from Template

```python
from pptx import Presentation

def create_from_template(template_path: str, output_path: str,
                          slides_data: list[dict]) -> None:
    """Create presentation from existing template."""
    prs = Presentation(template_path)

    for data in slides_data:
        # Use template's slide layout
        layout = prs.slide_layouts[data.get('layout_index', 1)]
        slide = prs.slides.add_slide(layout)

        # Fill in placeholders
        for idx, text in data.get('placeholders', {}).items():
            if idx < len(slide.placeholders):
                slide.placeholders[idx].text = text

    prs.save(output_path)
```

## Working with Text

### Add Text Box

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def add_text_box(slide, text: str, left: float, top: float,
                 width: float, height: float) -> None:
    """Add formatted text box to slide."""
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top),
        Inches(width), Inches(height)
    )

    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 0, 128)
```

### Add Bulleted List

```python
from pptx.enum.text import PP_ALIGN

def add_bullet_list(slide, items: list[str], left: float, top: float) -> None:
    """Add bulleted list to slide."""
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top),
        Inches(8), Inches(4)
    )

    tf = txBox.text_frame
    tf.word_wrap = True

    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        p.text = item
        p.level = 0
        p.font.size = Pt(18)
```

## Working with Images

### Add Image

```python
from pptx import Presentation
from pptx.util import Inches

def add_image(slide, image_path: str, left: float, top: float,
              width: float = None, height: float = None) -> None:
    """Add image to slide."""
    if width:
        slide.shapes.add_picture(
            image_path,
            Inches(left), Inches(top),
            width=Inches(width)
        )
    else:
        slide.shapes.add_picture(
            image_path,
            Inches(left), Inches(top)
        )
```

### Add Image from URL

```python
import requests
from io import BytesIO

def add_image_from_url(slide, url: str, left: float, top: float,
                       width: float) -> None:
    """Add image from URL to slide."""
    response = requests.get(url)
    image_stream = BytesIO(response.content)

    slide.shapes.add_picture(
        image_stream,
        Inches(left), Inches(top),
        width=Inches(width)
    )
```

## Working with Tables

### Create Table

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def add_table(slide, headers: list[str], rows: list[list],
              left: float, top: float) -> None:
    """Add formatted table to slide."""
    num_rows = len(rows) + 1  # +1 for header
    num_cols = len(headers)

    table = slide.shapes.add_table(
        num_rows, num_cols,
        Inches(left), Inches(top),
        Inches(9), Inches(3)
    ).table

    # Format headers
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(0, 112, 192)

        para = cell.text_frame.paragraphs[0]
        para.font.bold = True
        para.font.color.rgb = RGBColor(255, 255, 255)
        para.font.size = Pt(14)

    # Add data
    for row_idx, row_data in enumerate(rows, 1):
        for col_idx, value in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.text = str(value)
            cell.text_frame.paragraphs[0].font.size = Pt(12)
```

## Working with Charts

### Create Bar Chart

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

def add_bar_chart(slide, categories: list[str], series_data: dict,
                  left: float, top: float) -> None:
    """Add bar chart to slide."""
    chart_data = CategoryChartData()
    chart_data.categories = categories

    for series_name, values in series_data.items():
        chart_data.add_series(series_name, values)

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(left), Inches(top),
        Inches(8), Inches(4.5),
        chart_data
    ).chart

    chart.has_legend = True
```

### Create Pie Chart

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

def add_pie_chart(slide, labels: list[str], values: list[float],
                  left: float, top: float) -> None:
    """Add pie chart to slide."""
    chart_data = CategoryChartData()
    chart_data.categories = labels
    chart_data.add_series('Series 1', values)

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.PIE,
        Inches(left), Inches(top),
        Inches(6), Inches(4.5),
        chart_data
    ).chart
```

## Working with Shapes

### Add Basic Shapes

```python
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def add_rectangle(slide, left: float, top: float,
                  width: float, height: float, color: tuple) -> None:
    """Add colored rectangle to slide."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(left), Inches(top),
        Inches(width), Inches(height)
    )

    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*color)
    shape.line.fill.background()  # No border
```

### Add Arrow

```python
from pptx.enum.shapes import MSO_SHAPE

def add_arrow(slide, start_x: float, start_y: float,
              end_x: float, end_y: float) -> None:
    """Add arrow connector between points."""
    connector = slide.shapes.add_connector(
        MSO_SHAPE.LINE_ARROW,
        Inches(start_x), Inches(start_y),
        Inches(end_x), Inches(end_y)
    )
```

## Slide Operations

### Duplicate Slide

```python
from copy import deepcopy

def duplicate_slide(prs, index: int) -> None:
    """Duplicate slide at given index."""
    template = prs.slides[index]
    layout = template.slide_layout

    new_slide = prs.slides.add_slide(layout)

    # Copy shapes
    for shape in template.shapes:
        el = shape.element
        new_el = deepcopy(el)
        new_slide.shapes._spTree.insert_element_before(new_el, 'p:extLst')
```

### Delete Slide

```python
def delete_slide(prs, index: int) -> None:
    """Delete slide at given index."""
    rId = prs.slides._sldIdLst[index].rId
    prs.part.drop_rel(rId)
    del prs.slides._sldIdLst[index]
```

### Reorder Slides

```python
def move_slide(prs, from_index: int, to_index: int) -> None:
    """Move slide from one position to another."""
    slides = list(prs.slides._sldIdLst)
    slide = slides.pop(from_index)
    slides.insert(to_index, slide)

    prs.slides._sldIdLst[:] = slides
```

## Extract Content

### Extract All Text

```python
def extract_text(pptx_path: str) -> list[str]:
    """Extract all text from presentation."""
    prs = Presentation(pptx_path)
    text = []

    for slide in prs.slides:
        slide_text = []
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                slide_text.append(shape.text)
        text.append("\n".join(slide_text))

    return text
```

### Extract Images

```python
from pathlib import Path

def extract_images(pptx_path: str, output_dir: str) -> list[str]:
    """Extract all images from presentation."""
    prs = Presentation(pptx_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    image_paths = []
    img_counter = 0

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.shape_type == 13:  # Picture
                image = shape.image
                ext = image.ext
                image_path = output_dir / f"image_{img_counter}.{ext}"
                image_path.write_bytes(image.blob)
                image_paths.append(str(image_path))
                img_counter += 1

    return image_paths
```

## Speaker Notes

### Add Speaker Notes

```python
def add_notes(slide, notes_text: str) -> None:
    """Add speaker notes to slide."""
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = notes_text
```

### Extract Speaker Notes

```python
def extract_notes(pptx_path: str) -> list[str]:
    """Extract speaker notes from all slides."""
    prs = Presentation(pptx_path)
    notes = []

    for slide in prs.slides:
        notes_slide = slide.notes_slide
        notes.append(notes_slide.notes_text_frame.text)

    return notes
```

## Merge Presentations

### Combine Presentations

```python
from pptx import Presentation
from copy import deepcopy

def merge_presentations(input_paths: list[str], output_path: str) -> None:
    """Merge multiple presentations into one."""
    merged = Presentation()

    for path in input_paths:
        prs = Presentation(path)
        for slide in prs.slides:
            # Get matching layout
            layout = merged.slide_layouts[0]  # Default to first layout

            new_slide = merged.slides.add_slide(layout)

            # Copy shapes
            for shape in slide.shapes:
                el = deepcopy(shape.element)
                new_slide.shapes._spTree.insert_element_before(el, 'p:extLst')

    merged.save(output_path)
```
