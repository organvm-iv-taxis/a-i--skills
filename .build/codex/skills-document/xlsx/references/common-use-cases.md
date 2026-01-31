# XLSX Common Use Cases

Practical recipes for common Excel spreadsheet tasks.

## Reading Spreadsheets

### Read Entire Workbook

```python
import openpyxl

def read_workbook(xlsx_path: str) -> dict[str, list[list]]:
    """Read all sheets from workbook."""
    wb = openpyxl.load_workbook(xlsx_path)
    data = {}

    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        sheet_data = []
        for row in sheet.iter_rows(values_only=True):
            sheet_data.append(list(row))
        data[sheet_name] = sheet_data

    return data
```

### Read with Pandas

```python
import pandas as pd

def read_to_dataframe(xlsx_path: str, sheet_name: str = None) -> pd.DataFrame:
    """Read Excel to pandas DataFrame."""
    return pd.read_excel(xlsx_path, sheet_name=sheet_name)

def read_all_sheets(xlsx_path: str) -> dict[str, pd.DataFrame]:
    """Read all sheets as DataFrames."""
    return pd.read_excel(xlsx_path, sheet_name=None)
```

### Read Specific Range

```python
def read_range(xlsx_path: str, sheet_name: str,
               start_row: int, start_col: int,
               end_row: int, end_col: int) -> list[list]:
    """Read specific cell range."""
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    sheet = wb[sheet_name]

    data = []
    for row in sheet.iter_rows(min_row=start_row, max_row=end_row,
                                min_col=start_col, max_col=end_col,
                                values_only=True):
        data.append(list(row))
    return data
```

## Creating Spreadsheets

### Create Basic Workbook

```python
import openpyxl

def create_workbook(output_path: str, data: dict[str, list[list]]) -> None:
    """Create workbook with multiple sheets."""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # Remove default sheet

    for sheet_name, rows in data.items():
        ws = wb.create_sheet(sheet_name)
        for row in rows:
            ws.append(row)

    wb.save(output_path)
```

### Create with Formatting

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

def create_formatted(output_path: str, headers: list[str], data: list[list]) -> None:
    """Create formatted spreadsheet."""
    wb = Workbook()
    ws = wb.active

    # Header style
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_align = Alignment(horizontal="center")

    # Add headers
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align

    # Add data
    for row_idx, row_data in enumerate(data, 2):
        for col_idx, value in enumerate(row_data, 1):
            ws.cell(row=row_idx, column=col_idx, value=value)

    # Auto-adjust column widths
    for col in ws.columns:
        max_length = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_length + 2

    wb.save(output_path)
```

### Create from DataFrame

```python
import pandas as pd

def df_to_excel(df: pd.DataFrame, output_path: str, sheet_name: str = "Sheet1") -> None:
    """Write DataFrame to Excel with formatting."""
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Get workbook and worksheet
        wb = writer.book
        ws = wb[sheet_name]

        # Format headers
        for cell in ws[1]:
            cell.font = Font(bold=True)
```

## Formulas

### Add Formulas

```python
def add_formulas(xlsx_path: str, output_path: str) -> None:
    """Add formulas to spreadsheet."""
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active

    # Sum formula
    ws['E2'] = '=SUM(A2:D2)'

    # Average
    ws['E3'] = '=AVERAGE(A3:D3)'

    # Conditional
    ws['E4'] = '=IF(A4>100,"High","Low")'

    # VLOOKUP
    ws['E5'] = '=VLOOKUP(A5,Sheet2!A:B,2,FALSE)'

    wb.save(output_path)
```

### Read Calculated Values

```python
def read_with_formulas(xlsx_path: str) -> tuple[list, list]:
    """Read both formulas and calculated values."""
    # Read formulas
    wb_formulas = openpyxl.load_workbook(xlsx_path)
    ws_formulas = wb_formulas.active

    # Read calculated values
    wb_values = openpyxl.load_workbook(xlsx_path, data_only=True)
    ws_values = wb_values.active

    formulas = [[cell.value for cell in row] for row in ws_formulas.iter_rows()]
    values = [[cell.value for cell in row] for row in ws_values.iter_rows()]

    return formulas, values
```

## Charts

### Create Chart

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference

def create_chart(output_path: str, data: list[list], title: str) -> None:
    """Create spreadsheet with bar chart."""
    wb = Workbook()
    ws = wb.active

    # Add data
    for row in data:
        ws.append(row)

    # Create chart
    chart = BarChart()
    chart.title = title
    chart.y_axis.title = "Values"
    chart.x_axis.title = "Categories"

    # Data range (excluding header)
    data_ref = Reference(ws, min_col=2, min_row=1,
                         max_col=len(data[0]), max_row=len(data))
    cats_ref = Reference(ws, min_col=1, min_row=2, max_row=len(data))

    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)

    ws.add_chart(chart, "E2")
    wb.save(output_path)
```

## Data Validation

### Add Dropdown List

```python
from openpyxl.worksheet.datavalidation import DataValidation

def add_dropdown(xlsx_path: str, output_path: str,
                 cell_range: str, options: list[str]) -> None:
    """Add dropdown validation to cells."""
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active

    dv = DataValidation(
        type="list",
        formula1=f'"{",".join(options)}"',
        showDropDown=False
    )
    ws.add_data_validation(dv)
    dv.add(cell_range)

    wb.save(output_path)
```

## Conditional Formatting

### Add Color Scale

```python
from openpyxl.formatting.rule import ColorScaleRule

def add_color_scale(xlsx_path: str, output_path: str, cell_range: str) -> None:
    """Add color scale formatting."""
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active

    rule = ColorScaleRule(
        start_type="min", start_color="F8696B",
        mid_type="percentile", mid_value=50, mid_color="FFEB84",
        end_type="max", end_color="63BE7B"
    )
    ws.conditional_formatting.add(cell_range, rule)

    wb.save(output_path)
```

## Filtering and Sorting

### Apply AutoFilter

```python
def add_autofilter(xlsx_path: str, output_path: str) -> None:
    """Add autofilter to data range."""
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active

    # Get data range
    max_row = ws.max_row
    max_col = ws.max_column
    end_col = openpyxl.utils.get_column_letter(max_col)

    ws.auto_filter.ref = f"A1:{end_col}{max_row}"

    wb.save(output_path)
```

### Sort Data with Pandas

```python
import pandas as pd

def sort_excel(xlsx_path: str, output_path: str,
               sort_columns: list[str], ascending: bool = True) -> None:
    """Sort Excel data."""
    df = pd.read_excel(xlsx_path)
    df_sorted = df.sort_values(by=sort_columns, ascending=ascending)
    df_sorted.to_excel(output_path, index=False)
```

## Pivot Tables (via Pandas)

### Create Pivot Table

```python
import pandas as pd

def create_pivot(xlsx_path: str, output_path: str,
                 index: str, columns: str, values: str) -> None:
    """Create pivot table from Excel data."""
    df = pd.read_excel(xlsx_path)

    pivot = pd.pivot_table(
        df,
        index=index,
        columns=columns,
        values=values,
        aggfunc='sum'
    )

    pivot.to_excel(output_path)
```

## Merge Workbooks

### Combine Sheets

```python
import openpyxl

def merge_workbooks(input_paths: list[str], output_path: str) -> None:
    """Merge multiple workbooks into one."""
    merged = openpyxl.Workbook()
    merged.remove(merged.active)

    for path in input_paths:
        wb = openpyxl.load_workbook(path)
        for sheet_name in wb.sheetnames:
            # Handle duplicate names
            new_name = sheet_name
            counter = 1
            while new_name in merged.sheetnames:
                new_name = f"{sheet_name}_{counter}"
                counter += 1

            source = wb[sheet_name]
            target = merged.create_sheet(new_name)

            for row in source.iter_rows():
                for cell in row:
                    target[cell.coordinate].value = cell.value

    merged.save(output_path)
```

### Combine Data Vertically

```python
import pandas as pd

def stack_sheets(input_paths: list[str], output_path: str) -> None:
    """Stack data from multiple Excel files."""
    dfs = [pd.read_excel(path) for path in input_paths]
    combined = pd.concat(dfs, ignore_index=True)
    combined.to_excel(output_path, index=False)
```
