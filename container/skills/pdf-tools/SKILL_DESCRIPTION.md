# PDF Tools (PDF Processing)

## Overview

The PDF Tools skill provides comprehensive capabilities for creating, manipulating, extracting, and analyzing PDF documents programmatically. This skill handles everything from basic operations like merging and splitting to advanced tasks like form filling, table extraction, OCR, and watermarking. Built on industry-standard Python libraries (pypdf, pdfplumber, reportlab) and command-line tools (qpdf, pdftotext), it enables complete PDF workflow automation.

## Who Should Use This Skill

- **Data Analysts** extracting tables and text from reports
- **Document Managers** merging, splitting, and organizing PDF files
- **Form Processors** programmatically filling PDF forms at scale
- **Developers** automating PDF generation and manipulation
- **Researchers** extracting data from academic papers and publications
- **Business Analysts** processing invoices, receipts, and financial documents
- **Content Creators** generating professional PDF reports and documents
- **Anyone** needing to automate PDF processing workflows

## Purpose and Use Cases

Use this skill when you need to:
- Extract text and tables from PDF documents
- Create new PDFs programmatically with custom content
- Merge multiple PDFs into a single document
- Split PDFs into separate pages or ranges
- Fill PDF forms programmatically
- Extract images and metadata from PDFs
- Add watermarks, headers, or footers to documents
- Rotate, crop, or manipulate PDF pages
- Apply or remove password protection
- Perform OCR on scanned documents
- Convert PDFs to other formats or images

**Keywords that trigger this skill:** pdf, pdf extraction, pdf forms, merge pdf, split pdf, pdf tables, pdf creation, document processing

## What's Included

### Text and Data Extraction

**pdfplumber:**
- Extract text with layout preservation
- Extract tables with structure intact
- Advanced table detection and parsing
- Convert tables to pandas DataFrames
- Export to Excel or CSV
- Page-by-page content analysis

**pdftotext (Poppler):**
- Fast text extraction from command line
- Layout-preserving mode
- Selective page ranges
- Simple integration with shell scripts

**OCR Capabilities:**
- Extract text from scanned PDFs using Tesseract
- Convert PDF pages to images for OCR processing
- Batch processing of scanned documents
- Multiple language support

### PDF Creation

**reportlab:**
- Create PDFs from scratch using Python
- Canvas-based drawing API for precise control
- Platypus framework for document flow
- Support for text, images, tables, and graphics
- Custom styling and formatting
- Multi-page document generation
- Headers, footers, and page numbers

**Features:**
- Professional typography and layout
- Vector graphics and shapes
- Image embedding
- Custom page sizes and orientations
- PDF/A compliance options

### PDF Manipulation

**pypdf Library:**
- Merge multiple PDFs
- Split PDFs by page or range
- Rotate pages (90°, 180°, 270°)
- Extract specific pages
- Reorder pages
- Delete pages
- Extract metadata (title, author, subject, creator)
- Add or remove password protection
- Apply watermarks and overlays

**qpdf Command-Line:**
- Advanced PDF linearization
- Repair damaged PDFs
- Merge and split operations
- Page rotation and selection
- Password removal with authorization
- PDF structure optimization

### Form Processing

**Comprehensive Form Support:**
- Fill PDF forms programmatically
- Extract form field information
- Set text fields, checkboxes, radio buttons
- Handle dropdown selections
- Flatten forms (make fields non-editable)
- Batch form processing

**Libraries:**
- pdf-lib (JavaScript) - Modern form filling
- pypdf (Python) - Form field manipulation
- Detailed form filling guide in `forms.md`

### Image Operations

**Extraction:**
- Extract all images from PDFs
- Save in JPEG or PNG format
- Preserve image quality and metadata

**Watermarking:**
- Apply watermarks to pages
- Custom positioning and opacity
- Image or text watermarks
- Batch watermark application

## How It Works

### Step-by-Step Process

**1. Text Extraction**

*Simple Text Extraction:*
```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()
```

*Layout-Preserving Extraction:*
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

*Command-Line Extraction:*
```bash
pdftotext -layout document.pdf output.txt
pdftotext -f 1 -l 5 document.pdf output.txt  # Pages 1-5
```

**2. Table Extraction**

*Basic Table Extraction:*
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

*Export to Excel:*
```python
import pandas as pd
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

**3. PDF Creation**

*Simple PDF:*
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf", pagesize=letter)
width, height = letter

c.drawString(100, height - 100, "Hello World!")
c.line(100, height - 140, 400, height - 140)
c.save()
```

*Multi-Page Document:*
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("Report Title", styles['Title']))
story.append(Spacer(1, 12))
story.append(Paragraph("Content here...", styles['Normal']))

doc.build(story)
```

**4. Merging PDFs**

*Python Approach:*
```python
from pypdf import PdfWriter

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

*Command-Line Approach:*
```bash
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
```

**5. Splitting PDFs**

*Split to Individual Pages:*
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

*Extract Page Range:*
```bash
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf
```

**6. Form Filling**

*Read forms.md for detailed instructions:*
```python
# See forms.md for complete form filling guide
# Supports text fields, checkboxes, radio buttons, dropdowns
# JavaScript (pdf-lib) and Python (pypdf) approaches
```

**7. OCR Processing**

*Extract Text from Scanned PDFs:*
```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('scanned.pdf')
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"
```

**8. Watermarking**

*Apply Watermark:*
```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

**9. Password Protection**

*Add Password:*
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

*Remove Password:*
```bash
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### Quality Standards

**Text Extraction:**
- Verify extracted text accuracy
- Handle special characters and encodings properly
- Preserve layout when needed
- Test on sample pages before batch processing

**PDF Creation:**
- Professional formatting and typography
- Proper page margins and spacing
- Consistent styling across pages
- Valid PDF structure

**Form Filling:**
- Verify all required fields are filled
- Validate data formats (dates, numbers, etc.)
- Test filled forms open correctly
- Flatten forms when appropriate

## Technical Details

### Python Libraries

**pypdf:**
- PDF reading and writing
- Page manipulation
- Metadata extraction
- Basic text extraction
- Form field access
- Encryption/decryption

**pdfplumber:**
- Advanced text extraction
- Table detection and parsing
- Layout analysis
- Visual debugging capabilities
- Character-level text positioning

**reportlab:**
- PDF generation from scratch
- Canvas API for drawing
- Platypus for document flow
- Typography and styling
- Graphics and images

**Supporting Libraries:**
- **pytesseract** - OCR engine interface
- **pdf2image** - Convert PDF pages to images
- **pandas** - Data manipulation for extracted tables

### Command-Line Tools

**pdftotext (Poppler):**
```bash
pdftotext [options] <pdf_file> [output_file]
Options:
  -layout    Preserve layout
  -f N       First page
  -l N       Last page
```

**qpdf:**
```bash
qpdf [options] <input.pdf> <output.pdf>
Common operations:
  --empty --pages file1.pdf file2.pdf -- merged.pdf
  --pages . 1-5 -- pages1-5.pdf
  --rotate=+90:1
  --decrypt
```

**pdfimages (Poppler):**
```bash
pdfimages -j input.pdf output_prefix
```

### Form Field Types

**Supported Field Types:**
- Text fields (single and multi-line)
- Checkboxes
- Radio buttons
- Dropdown lists
- Buttons
- Signatures (basic support)

**Operations:**
- Read field values
- Set field values
- Get field properties
- Flatten forms

## Use Cases and Examples

### Invoice Processing
**Scenario:** Extract data from 1000 PDF invoices for analysis

**Workflow:**
1. Use pdfplumber to extract tables from each invoice
2. Convert tables to pandas DataFrames
3. Standardize and validate data
4. Export to Excel or database

**Key Features Used:** Table extraction, batch processing, data validation

### Report Generation
**Scenario:** Generate monthly reports as PDFs from database data

**Workflow:**
1. Query database for report data
2. Use reportlab to create PDF with custom styling
3. Add charts, tables, and formatted text
4. Generate multi-page document with headers/footers

**Key Features Used:** PDF creation, formatting, multi-page documents

### Form Processing
**Scenario:** Fill 500 government forms programmatically

**Workflow:**
1. Read forms.md for form filling guide
2. Extract field names from template form
3. Map data to field names
4. Fill forms using pdf-lib or pypdf
5. Flatten and save filled forms

**Key Features Used:** Form filling, batch processing, validation

### Document Archival
**Scenario:** Merge and organize 1000 PDF documents by category

**Workflow:**
1. Categorize documents based on metadata or content
2. Merge documents within each category
3. Add cover pages and table of contents
4. Apply consistent metadata and properties

**Key Features Used:** Merging, metadata, batch processing

### Data Extraction Research
**Scenario:** Extract tables from academic papers for meta-analysis

**Workflow:**
1. Use pdfplumber to extract tables from papers
2. Convert to structured data format
3. Validate and clean extracted data
4. Export to Excel for analysis

**Key Features Used:** Table extraction, data cleaning, export

## Best Practices

### Text Extraction
- **Test first**: Extract from sample pages before batch processing
- **Choose right tool**: pdfplumber for layout, pdftotext for speed, pypdf for simplicity
- **Handle encoding**: Be aware of special characters and encoding issues
- **Verify accuracy**: Spot-check extracted text against original

### Table Extraction
- **Visual inspection**: Check extracted tables match PDF layout
- **Handle edge cases**: Empty cells, merged cells, split tables across pages
- **Validate data**: Ensure numbers and dates extracted correctly
- **Clean data**: Remove extra whitespace, standardize formatting

### PDF Creation
- **Plan layout**: Design page structure before coding
- **Use styles**: Define consistent styles for typography
- **Test incrementally**: Build and test pages progressively
- **Optimize file size**: Balance quality and file size

### Form Filling
- **Read documentation**: Always read forms.md before filling forms
- **Validate data**: Ensure data matches field types and constraints
- **Test sample**: Fill one form and verify before batch processing
- **Flatten when done**: Make forms non-editable if appropriate

### Batch Processing
- **Handle errors gracefully**: Use try/except for file operations
- **Log progress**: Track which files processed successfully
- **Validate inputs**: Check files exist and are valid PDFs
- **Test on subset**: Process small batch before full run

### Common Pitfalls to Avoid
- ❌ Not checking if PDFs are scanned (need OCR) vs. digital (text extraction works)
- ❌ Assuming all tables extract perfectly (always validate structure)
- ❌ Hardcoding page numbers or layout assumptions
- ❌ Not handling password-protected PDFs
- ❌ Ignoring file size when creating PDFs (uncompressed images bloat files)
- ❌ Filling forms without reading forms.md documentation
- ❌ Not testing form fills before batch processing
- ❌ Assuming merged PDFs maintain original metadata
- ❌ Not validating extracted data before using

## Quick Reference

### Common Operations

| Task | Best Tool | Code Example |
|------|-----------|--------------|
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDF | reportlab | `canvas.Canvas()` |
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDF | pypdf | One page per file |
| Fill forms | pdf-lib/pypdf | See forms.md |
| Add password | pypdf | `writer.encrypt()` |
| Rotate pages | pypdf | `page.rotate(90)` |
| Extract images | pdfimages | `pdfimages -j` |
| OCR scanned PDF | pytesseract | Convert to image first |

### Library Selection Guide

**Use pypdf when:**
- Merging or splitting PDFs
- Basic text extraction sufficient
- Manipulating page order
- Adding/removing passwords
- Extracting metadata

**Use pdfplumber when:**
- Extracting tables from PDFs
- Need layout-preserved text
- Analyzing page structure
- Working with complex documents

**Use reportlab when:**
- Creating new PDFs from scratch
- Need precise layout control
- Generating reports programmatically
- Custom styling required

**Use command-line tools when:**
- Simple one-off operations
- Shell script integration
- Quick text extraction
- PDF repair needed

## Dependencies

**Required Python Packages:**
```bash
pip install pypdf
pip install pdfplumber
pip install reportlab
pip install pandas  # For table data manipulation
```

**Optional (for advanced features):**
```bash
pip install pytesseract  # OCR
pip install pdf2image    # PDF to image conversion
```

**Command-Line Tools:**
```bash
sudo apt-get install poppler-utils  # pdftotext, pdfimages
sudo apt-get install qpdf           # Advanced PDF operations
sudo apt-get install tesseract-ocr  # OCR engine
```

## Additional Resources

**Documentation Files:**
- `reference.md` - Advanced features and detailed API reference
- `forms.md` - Complete guide to PDF form filling

**Support:**
- Python library documentation (pypdf, pdfplumber, reportlab)
- Poppler utilities manual pages
- qpdf documentation
