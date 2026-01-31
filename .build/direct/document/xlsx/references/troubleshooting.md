# XLSX Troubleshooting Guide

Common issues and solutions when working with Excel spreadsheets.

## File Opening Issues

### Cannot Open File

**Symptoms**: `InvalidFileException` or `BadZipFile`

**Causes**:
1. File is corrupted
2. File is .xls (older format), not .xlsx
3. File is password protected

**Solutions**:

Check and convert file type:
```python
from pathlib import Path

def convert_xls_to_xlsx(xls_path: str, xlsx_path: str) -> None:
    """Convert old .xls to .xlsx using xlrd and openpyxl."""
    import xlrd
    import openpyxl

    xls_book = xlrd.open_workbook(xls_path)
    xlsx_book = openpyxl.Workbook()
    xlsx_book.remove(xlsx_book.active)

    for sheet_name in xls_book.sheet_names():
        xls_sheet = xls_book.sheet_by_name(sheet_name)
        xlsx_sheet = xlsx_book.create_sheet(sheet_name)

        for row_idx in range(xls_sheet.nrows):
            for col_idx in range(xls_sheet.ncols):
                xlsx_sheet.cell(row_idx + 1, col_idx + 1).value = \
                    xls_sheet.cell_value(row_idx, col_idx)

    xlsx_book.save(xlsx_path)
```

### File Locked by Another Process

**Symptoms**: `PermissionError`

**Solutions**:
```python
import shutil
from tempfile import NamedTemporaryFile

def open_locked_file(path: str):
    """Open file even if locked by Excel."""
    with NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        shutil.copy2(path, tmp.name)
        return openpyxl.load_workbook(tmp.name)
```

## Formula Issues

### Formulas Show as Text

**Symptoms**: Formulas display as `=SUM(A1:A10)` instead of calculated value.

**Causes**: Cell formatted as text before formula entry.

**Solutions**:
```python
# Ensure cell is not text formatted
cell = ws['A1']
cell.number_format = 'General'
cell.value = '=SUM(B1:B10)'
```

### Formula Not Calculating

**Symptoms**: Formula returns 0 or wrong value.

**Causes**: `data_only=True` reads cached values, which may be stale.

**Solutions**:
```python
# Read formulas, not cached values
wb = openpyxl.load_workbook(path)  # data_only=False by default

# Or recalculate with xlcalc
from xlcalc import xlfunctions
# Evaluate formulas programmatically
```

### Circular Reference

**Symptoms**: Formula returns error or infinite loop.

**Solutions**:
```python
def check_circular_refs(xlsx_path: str) -> list[str]:
    """Find potential circular references."""
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active
    circular = []

    for row in ws.iter_rows():
        for cell in row:
            if cell.value and str(cell.value).startswith('='):
                formula = str(cell.value)
                if cell.coordinate in formula:
                    circular.append(f"{cell.coordinate}: {formula}")

    return circular
```

## Data Type Issues

### Numbers Stored as Text

**Symptoms**: Numbers left-aligned, can't do math operations.

**Solutions**:
```python
def convert_text_to_numbers(ws, column: str) -> None:
    """Convert text numbers to actual numbers."""
    for cell in ws[column]:
        if cell.value:
            try:
                cell.value = float(cell.value)
            except (ValueError, TypeError):
                pass
```

### Date Parsing Issues

**Symptoms**: Dates show as numbers or wrong format.

**Solutions**:
```python
from datetime import datetime
from openpyxl.utils.datetime import from_excel

def read_excel_date(cell_value) -> datetime:
    """Convert Excel date to Python datetime."""
    if isinstance(cell_value, datetime):
        return cell_value
    if isinstance(cell_value, (int, float)):
        return from_excel(cell_value)
    return datetime.strptime(cell_value, "%Y-%m-%d")
```

### Float Precision

**Symptoms**: Numbers like 0.1 + 0.2 show as 0.30000000000000004.

**Solutions**:
```python
from decimal import Decimal

# Use Decimal for financial data
def precise_calculation(a: float, b: float) -> Decimal:
    return Decimal(str(a)) + Decimal(str(b))

# Or round when writing
cell.value = round(calculated_value, 2)
```

## Memory Issues

### Out of Memory on Large Files

**Solutions**:

Use read_only mode:
```python
wb = openpyxl.load_workbook(path, read_only=True)

for row in ws.iter_rows(values_only=True):
    # Process one row at a time
    process_row(row)

wb.close()  # Important: close when done
```

Write in streaming mode:
```python
from openpyxl import Workbook
from openpyxl.writer.write_only import WriteOnlyCell

wb = Workbook(write_only=True)
ws = wb.create_sheet()

for row_data in data_generator():  # Use generator
    ws.append(row_data)

wb.save(path)
```

Use pandas with chunking:
```python
import pandas as pd

chunks = pd.read_excel(path, chunksize=10000)
for chunk in chunks:
    process_chunk(chunk)
```

## Styling Issues

### Styles Not Applied

**Symptoms**: Font, color, or border doesn't appear.

**Solutions**:
```python
from openpyxl.styles import Font, PatternFill, Border, Side

# Create new style objects for each cell
def style_cell(cell):
    # Don't reuse style objects
    cell.font = Font(bold=True)  # New Font for each cell
    cell.fill = PatternFill(start_color="FFFF00", fill_type="solid")
```

### Merged Cells Losing Style

**Solutions**:
```python
def style_merged_cells(ws, cell_range: str, font=None, fill=None):
    """Apply style to merged cell range."""
    # Get top-left cell
    start_cell = cell_range.split(':')[0]
    cell = ws[start_cell]

    if font:
        cell.font = font
    if fill:
        cell.fill = fill
```

## Chart Issues

### Chart Not Displaying

**Symptoms**: Empty chart area.

**Causes**: Incorrect data reference.

**Solutions**:
```python
from openpyxl.chart import Reference

# Verify data range exists
print(f"Data range: {ws.dimensions}")

# Check reference is correct
data = Reference(ws, min_col=2, min_row=1, max_col=4, max_row=10)
print(f"Reference: min_col={data.min_col}, max_col={data.max_col}")
```

## Pandas Integration Issues

### dtype Warning

**Symptoms**: `DtypeWarning: Columns have mixed types`

**Solutions**:
```python
import pandas as pd

# Specify dtypes
df = pd.read_excel(path, dtype={
    'column_a': str,
    'column_b': float,
    'column_c': 'Int64'  # Nullable integer
})

# Or convert after reading
df['column'] = pd.to_numeric(df['column'], errors='coerce')
```

### Missing Data

**Symptoms**: NaN values where data should exist.

**Solutions**:
```python
# Check for empty strings
df = df.replace('', pd.NA)

# Or skip empty rows
df = pd.read_excel(path, skiprows=lambda x: x in empty_rows)
```

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `InvalidFileException` | Not a valid xlsx | Check file format |
| `KeyError: 'Sheet1'` | Sheet doesn't exist | Check `wb.sheetnames` |
| `ValueError: row/column must be > 0` | Invalid cell reference | Use 1-based indexing |
| `TypeError: unsupported operand` | Wrong data type | Convert types first |
| `MemoryError` | File too large | Use read_only mode |

## Performance Tips

### Speed Up Reading

```python
# Use data_only if you don't need formulas
wb = openpyxl.load_workbook(path, data_only=True)

# Use read_only for large files
wb = openpyxl.load_workbook(path, read_only=True)

# Use pandas for analysis
df = pd.read_excel(path, engine='openpyxl')
```

### Speed Up Writing

```python
# Use write_only mode
wb = Workbook(write_only=True)

# Disable calculation on open
wb.calculation.calcMode = 'manual'

# Write in batches, not cell by cell
ws.append(row_data)  # Instead of cell-by-cell
```

## Compatibility

### Excel Version Compatibility

```python
# XLSX works with Excel 2007+
# For older versions, export to CSV

import pandas as pd
df = pd.read_excel('data.xlsx')
df.to_csv('data.csv', index=False)
```

### LibreOffice Compatibility

```python
# Some features may differ
# Test with LibreOffice if targeting both

# Avoid Excel-specific features:
# - Power Query
# - ActiveX controls
# - Some chart types
```
