# Spreadsheets (XLSX)

## Overview

The Spreadsheets skill provides comprehensive capabilities for creating, editing, and analyzing Excel spreadsheets (.xlsx, .xlsm, .csv, .tsv files) with support for formulas, formatting, data analysis, and visualization. This skill handles everything from simple data manipulation to complex financial modeling with professional-grade formula construction, color coding standards, and automatic formula recalculation. Built on industry-standard Python libraries (openpyxl, pandas) and LibreOffice integration, it enables complete spreadsheet workflow automation.

## Who Should Use This Skill

- **Financial Analysts** building complex financial models and projections
- **Data Analysts** processing and analyzing large datasets
- **Business Analysts** creating reports and dashboards
- **Accountants** preparing financial statements and schedules
- **Data Scientists** working with structured data
- **Operations Managers** tracking KPIs and metrics
- **Investment Bankers** creating valuation models and pitch books
- **Anyone** needing to programmatically create or edit spreadsheets

## Purpose and Use Cases

Use this skill when you need to:
- Create new Excel files with formulas and professional formatting
- Read and analyze data from spreadsheets
- Modify existing spreadsheets while preserving formulas and formatting
- Build financial models with proper color coding and documentation
- Perform data analysis and create visualizations in Excel
- Recalculate formulas and detect errors automatically
- Convert between Excel, CSV, and other formats
- Generate reports programmatically from data sources
- Validate spreadsheet formulas and detect errors

**Keywords that trigger this skill:** xlsx, excel, spreadsheet, financial model, data analysis, formulas, csv processing

## What's Included

### Data Analysis and Manipulation

**pandas Library:**
- Read Excel files (single or multiple sheets)
- Analyze data with describe(), info(), head()
- Filter, group, and aggregate data
- Create pivot tables and cross-tabulations
- Time series analysis
- Export to Excel, CSV, or other formats
- Handle large datasets efficiently

**Capabilities:**
- Multi-sheet workbook support
- Data type specification and conversion
- Date parsing and handling
- Column selection for performance
- Statistical analysis

### Spreadsheet Creation and Editing

**openpyxl Library:**
- Create new Excel workbooks from scratch
- Load and modify existing files
- Add, delete, insert rows and columns
- Work with multiple sheets
- Apply formulas with Excel syntax
- Comprehensive formatting capabilities
- Preserve existing formulas and formatting

**Advanced Features:**
- Named ranges
- Data validation
- Conditional formatting
- Cell protection
- Merged cells
- Hyperlinks
- Comments

### Formula Management

**Critical Principle: Use Formulas, Not Hardcoded Values:**
- Always use Excel formulas instead of calculating in Python
- Ensures spreadsheets remain dynamic and updateable
- Allows users to modify assumptions and see results
- Maintains professional spreadsheet standards

**Formula Recalculation:**
- Automatic formula calculation using LibreOffice
- Error detection and reporting (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)
- Detailed error locations and counts
- JSON output with complete error analysis

**Requirements:**
- Zero formula errors in all deliverables
- Proper cell references and range validation
- Test formulas before deployment

### Financial Modeling Standards

**Color Coding (Industry Standard):**
- **Blue text** (RGB: 0,0,255) - Hardcoded inputs and user-changeable numbers
- **Black text** (RGB: 0,0,0) - ALL formulas and calculations
- **Green text** (RGB: 0,128,0) - Links from other worksheets (same workbook)
- **Red text** (RGB: 255,0,0) - External links to other files
- **Yellow background** (RGB: 255,255,0) - Key assumptions or cells needing attention

**Number Formatting:**
- Years as text strings ("2024" not "2,024")
- Currency with units in headers ("Revenue ($mm)")
- Zeros displayed as "-" including percentages
- Percentages: 0.0% format (one decimal)
- Multiples: 0.0x format (EV/EBITDA, P/E)
- Negative numbers in parentheses (123) not minus -123

**Formula Construction:**
- Place assumptions in separate cells
- Use cell references, never hardcode values in formulas
- Example: `=B5*(1+$B$6)` not `=B5*1.05`
- Verify all cell references are correct
- Test with edge cases (zero, negative, large values)

**Documentation:**
- Comment hardcoded values with source information
- Format: "Source: [System/Document], [Date], [Reference], [URL]"
- Example: "Source: Company 10-K, FY2024, Page 45, Revenue Note"

### Formatting Capabilities

**Cell Formatting:**
- Font properties (bold, italic, color, size, family)
- Fill colors and patterns
- Borders (style, color, position)
- Alignment (horizontal, vertical, text rotation)
- Number formats (currency, percentage, date, custom)

**Advanced Formatting:**
- Conditional formatting rules
- Cell protection and locking
- Row height and column width
- Merged cells
- Text wrapping
- Indentation

## How It Works

### Step-by-Step Process

**1. Reading and Analyzing Data**

*Using pandas:*
```python
import pandas as pd

# Read Excel file
df = pd.read_excel('file.xlsx')  # First sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets

# Analyze data
print(df.head())      # Preview
print(df.info())      # Column info
print(df.describe())  # Statistics

# Filter and analyze
filtered = df[df['Revenue'] > 1000000]
summary = df.groupby('Category')['Sales'].sum()
```

*Using openpyxl:*
```python
from openpyxl import load_workbook

wb = load_workbook('file.xlsx')
sheet = wb.active

# Read cell values
value = sheet['A1'].value
print(f"Cell A1: {value}")

# Iterate through rows
for row in sheet.iter_rows(min_row=2, values_only=True):
    print(row)
```

**2. Creating New Excel Files**

*Basic Structure:*
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active
sheet.title = "Financial Model"

# Add headers
sheet['A1'] = 'Year'
sheet['B1'] = 'Revenue'
sheet['C1'] = 'Growth Rate'

# Format headers
header_font = Font(bold=True, color='000000')
header_fill = PatternFill('solid', start_color='D3D3D3')

for cell in sheet[1]:
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center')

# Add data and formulas (NOT hardcoded values)
sheet['A2'] = '2024'
sheet['B2'] = 1000000  # Blue text for input
sheet['C2'] = 0.15     # Blue text for assumption

# Use formulas for calculations (Black text)
sheet['B3'] = '=B2*(1+$C$2)'  # 2025 revenue formula

# Apply color coding
sheet['B2'].font = Font(color='0000FF')  # Blue for input
sheet['C2'].font = Font(color='0000FF')  # Blue for assumption
sheet['B3'].font = Font(color='000000')  # Black for formula

wb.save('model.xlsx')
```

**3. Applying Professional Formatting**

*Financial Model Standards:*
```python
from openpyxl.styles import Font, PatternFill, Alignment, numbers

# Color coding fonts
input_font = Font(color='0000FF')       # Blue
formula_font = Font(color='000000')     # Black
internal_link_font = Font(color='008000') # Green
external_link_font = Font(color='FF0000') # Red

# Yellow highlight for key assumptions
yellow_fill = PatternFill('solid', start_color='FFFF00')

# Number formats
currency_format = '$#,##0;($#,##0);-'
percentage_format = '0.0%;(0.0%);-'
multiple_format = '0.0x'

# Apply to cells
sheet['B2'].font = input_font
sheet['B2'].number_format = currency_format

sheet['B3'].font = formula_font
sheet['B3'].number_format = currency_format

sheet['C2'].font = input_font
sheet['C2'].fill = yellow_fill  # Key assumption
sheet['C2'].number_format = percentage_format
```

**4. Using Formulas (Critical)**

*ALWAYS use formulas, NEVER hardcode calculations:*
```python
# ❌ WRONG - Hardcoding calculated values
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# ✅ CORRECT - Using Excel formulas
sheet['B10'] = '=SUM(B2:B9)'

# ❌ WRONG - Python calculation for growth
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # Hardcodes 0.15

# ✅ CORRECT - Excel formula
sheet['C5'] = '=(C4-C2)/C2'

# ❌ WRONG - Python average
avg = sum(values) / len(values)
sheet['D20'] = avg  # Hardcodes 42.5

# ✅ CORRECT - Excel formula
sheet['D20'] = '=AVERAGE(D2:D19)'
```

**5. Recalculating Formulas (MANDATORY)**

*After creating/editing files with formulas:*
```bash
python recalc.py output.xlsx
```

*Response includes error detection:*
```json
{
  "status": "success",           // or "errors_found"
  "total_errors": 0,
  "total_formulas": 42,
  "error_summary": {              // Only if errors found
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    },
    "#DIV/0!": {
      "count": 1,
      "locations": ["Sheet1!D15"]
    }
  }
}
```

*Error fixing workflow:*
1. Save spreadsheet with formulas
2. Run `recalc.py` to calculate and detect errors
3. If errors found, fix identified cells
4. Run `recalc.py` again
5. Repeat until `status: "success"`

**6. Working with Multiple Sheets**

*Create and manage sheets:*
```python
from openpyxl import Workbook

wb = Workbook()

# Create sheets
assumptions = wb.create_sheet('Assumptions', 0)
income_stmt = wb.create_sheet('Income Statement', 1)
balance_sheet = wb.create_sheet('Balance Sheet', 2)

# Link between sheets
income_stmt['B2'] = "=Assumptions!B5"  # Pull from Assumptions
income_stmt['B2'].font = Font(color='008000')  # Green for internal link

# Access sheets
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Sheet: {sheet_name}")

wb.save('model.xlsx')
```

**7. Data Analysis with pandas**

*Advanced analysis:*
```python
import pandas as pd

# Read with options
df = pd.read_excel('data.xlsx',
                   sheet_name='Sales',
                   dtype={'Customer_ID': str},
                   parse_dates=['Date'])

# Analysis
monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Revenue'].sum()
top_customers = df.groupby('Customer')['Revenue'].sum().nlargest(10)

# Pivot table
pivot = df.pivot_table(values='Revenue',
                       index='Product',
                       columns='Region',
                       aggfunc='sum')

# Export results
with pd.ExcelWriter('analysis.xlsx') as writer:
    monthly_sales.to_excel(writer, sheet_name='Monthly')
    top_customers.to_excel(writer, sheet_name='Top Customers')
    pivot.to_excel(writer, sheet_name='Pivot')
```

**8. Modifying Existing Files**

*Preserve formulas and formatting:*
```python
from openpyxl import load_workbook

# Load (preserves formulas)
wb = load_workbook('existing.xlsx')
sheet = wb.active

# Modify while preserving formulas
sheet['A1'] = 'Updated Title'
sheet.insert_rows(2)  # Insert at position 2
sheet.delete_cols(3)  # Delete column 3

# Add new sheet
new_sheet = wb.create_sheet('New Analysis')
new_sheet['A1'] = 'New Data'

# Save (formulas preserved)
wb.save('modified.xlsx')

# Recalculate (MANDATORY after modifications)
# Run: python recalc.py modified.xlsx
```

### Quality Standards

**Formula Quality:**
- Zero formula errors in deliverables
- All cell references verified and correct
- Tested with edge cases
- No circular references (unless intentional and documented)
- Assumptions in separate cells, never hardcoded in formulas

**Formatting Quality:**
- Consistent color coding throughout
- Proper number formats with units in headers
- Professional appearance
- Clear visual hierarchy
- Zeros displayed as "-"

**Code Quality:**
- Minimal, concise Python code
- No verbose variable names
- Limited print statements
- Clear but not redundant comments

**Documentation:**
- Hardcoded values sourced and dated
- Complex formulas explained
- Key assumptions highlighted (yellow)
- Model structure clear and logical

## Technical Details

### Libraries and Tools

**openpyxl:**
- Excel file creation and editing
- Formula preservation
- Comprehensive formatting
- Multi-sheet support
- Cell-level operations

**Key Features:**
- 1-based indexing (row=1, column=1 = A1)
- `data_only=True` reads calculated values (WARNING: saves without formulas)
- `read_only=True` for large file reading
- `write_only=True` for large file writing
- Formulas preserved but not evaluated

**pandas:**
- Data analysis and manipulation
- Statistical operations
- Grouping and aggregation
- Pivot tables
- Time series support
- Multiple format support (Excel, CSV, etc.)

**LibreOffice Integration:**
- Automatic formula recalculation
- Error detection and reporting
- Configures automatically on first run
- Cross-platform (Linux, macOS)

### Formula Verification

**Essential Checks:**
- [ ] Test 2-3 sample references before building full model
- [ ] Verify column mapping (column 64 = BL, not BK)
- [ ] Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6)
- [ ] Check for NaN values with `pd.notna()`
- [ ] Search all occurrences, not just first match
- [ ] Verify denominators before division (#DIV/0!)
- [ ] Confirm all cell references point to intended cells (#REF!)
- [ ] Use correct cross-sheet format (Sheet1!A1)

**Testing Strategy:**
- Start with 2-3 cells before applying broadly
- Verify all formula dependencies exist
- Test edge cases (zero, negative, large values)
- Run recalc.py and fix all errors

### recalc.py Output

**Success:**
```json
{
  "status": "success",
  "total_errors": 0,
  "total_formulas": 42
}
```

**Errors Found:**
```json
{
  "status": "errors_found",
  "total_errors": 3,
  "total_formulas": 42,
  "error_summary": {
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    },
    "#DIV/0!": {
      "count": 1,
      "locations": ["Sheet1!D15"]
    }
  }
}
```

## Use Cases and Examples

### Financial Model Creation
**Scenario:** Build 3-statement financial model for valuation

**Workflow:**
1. Create workbook with sheets: Assumptions, Income Statement, Balance Sheet, Cash Flow
2. Add assumptions with blue text and yellow highlights
3. Build formulas referencing assumptions (black text)
4. Link between sheets with green text
5. Apply professional formatting and number formats
6. Save and run recalc.py
7. Fix any formula errors
8. Validate calculations

**Key Features Used:** Multi-sheet workbooks, color coding, formulas, recalculation, error detection

### Data Analysis Report
**Scenario:** Analyze sales data and create executive summary

**Workflow:**
1. Read sales data with pandas
2. Perform grouping, aggregation, pivot analysis
3. Create summary statistics
4. Export multiple analysis sheets to Excel
5. Add charts and formatting with openpyxl
6. Generate final report

**Key Features Used:** pandas analysis, multi-sheet export, formatting

### Template-Based Generation
**Scenario:** Generate 100 client reports from Excel template

**Workflow:**
1. Load template with openpyxl
2. Identify input cells and formulas
3. Update input values for each client
4. Save individual reports
5. Batch recalculate all files
6. Verify no formula errors

**Key Features Used:** Template loading, formula preservation, batch processing, error detection

### Budget Tracking
**Scenario:** Create department budget tracker with actuals vs. budget

**Workflow:**
1. Set up budget inputs (blue text)
2. Create formulas for variance calculations (black text)
3. Add conditional formatting for over/under budget
4. Include month-to-month growth formulas
5. Format with professional number formats
6. Recalculate and validate

**Key Features Used:** Formulas, conditional formatting, professional formats, validation

### Data Consolidation
**Scenario:** Merge data from 50 regional Excel files

**Workflow:**
1. Use pandas to read all files
2. Concatenate or merge DataFrames
3. Clean and standardize data
4. Perform summary analysis
5. Export consolidated workbook
6. Add summary formulas with openpyxl

**Key Features Used:** pandas batch reading, data manipulation, multi-sheet export

## Best Practices

### Formula Construction
- **Use formulas always**: Never hardcode calculated values
- **Reference cells**: Use cell references, not values in formulas
- **Absolute references**: Use $ for fixed references (e.g., $B$6)
- **Test incrementally**: Verify 2-3 formulas before building full model
- **Check edge cases**: Test with zero, negative, very large values
- **Document assumptions**: Place in separate cells with comments

### Color Coding
- **Follow standards**: Use industry-standard colors consistently
- **Blue for inputs**: All user-changeable values
- **Black for formulas**: All calculations
- **Green for internal**: Links within same workbook
- **Red for external**: Links to other files
- **Yellow highlights**: Key assumptions needing attention

### Number Formatting
- **Specify units**: Always include in headers ("Revenue ($mm)")
- **Zero as dash**: Format all zeros as "-"
- **Consistent decimals**: 0.0% for percentages, 0.0x for multiples
- **Parentheses for negatives**: (123) not -123
- **Text for years**: "2024" not "2,024"

### Code Quality
- **Concise code**: Minimal Python without verbose comments
- **Avoid redundancy**: Don't repeat operations
- **Limited printing**: Essential feedback only
- **Clear names**: Meaningful but not overly verbose

### Formula Validation
- **Always recalculate**: Run recalc.py after creating/editing formulas
- **Fix all errors**: Zero errors required for delivery
- **Verify locations**: Check error_summary for specific cells
- **Retest after fixes**: Run recalc.py again after corrections

### Common Pitfalls to Avoid
- ❌ Hardcoding calculated values instead of using formulas
- ❌ Not running recalc.py after creating formulas
- ❌ Ignoring formula errors in recalc.py output
- ❌ Using wrong color coding (blue for formulas, black for inputs)
- ❌ Not specifying units in headers
- ❌ Hardcoding values in formulas instead of cell references
- ❌ Opening with `data_only=True` and saving (loses formulas permanently)
- ❌ Not testing formulas on sample cells first
- ❌ Assuming column numbers match (verify with Excel)
- ❌ Forgetting Excel uses 1-indexed rows
- ❌ Not checking for NaN values before using in formulas
- ❌ Creating circular references unintentionally
- ❌ Not documenting sources for hardcoded inputs

## Quick Reference

### Common Operations

| Task | Library | Code Example |
|------|---------|--------------|
| Read Excel | pandas | `pd.read_excel('file.xlsx')` |
| Create workbook | openpyxl | `Workbook()` |
| Add formula | openpyxl | `sheet['B2'] = '=SUM(A1:A10)'` |
| Format cell | openpyxl | `cell.font = Font(bold=True)` |
| Color coding | openpyxl | `Font(color='0000FF')` |
| Number format | openpyxl | `cell.number_format = '$#,##0'` |
| Insert row | openpyxl | `sheet.insert_rows(2)` |
| Recalculate | CLI | `python recalc.py file.xlsx` |
| Data analysis | pandas | `df.describe()` |
| Export to Excel | pandas | `df.to_excel('output.xlsx')` |

### Library Selection

**Use pandas when:**
- Analyzing data
- Bulk operations
- Statistical analysis
- Simple data export
- Reading CSV files
- Data manipulation

**Use openpyxl when:**
- Complex formatting needed
- Working with formulas
- Excel-specific features
- Multi-sheet workbooks
- Professional financial models
- Preserving existing formatting

## Dependencies

**Required Python Packages:**
```bash
pip install openpyxl
pip install pandas
```

**Required for Recalculation:**
- **LibreOffice** - Automatically configured by recalc.py script

**Installation (if needed):**
```bash
# Linux
sudo apt-get install libreoffice

# macOS
brew install libreoffice
```

## Additional Resources

**Scripts:**
- `recalc.py` - Formula recalculation and error detection

**Best Practices Documents:**
- Financial modeling standards (color coding, formatting)
- Formula construction guidelines
- Error prevention checklist

**Support:**
- openpyxl documentation
- pandas documentation
- Excel formula reference
