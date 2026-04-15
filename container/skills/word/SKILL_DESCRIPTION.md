# Word Documents (DOCX)

## Overview

The Word Documents skill provides comprehensive capabilities for creating, editing, and analyzing professional Microsoft Word documents (.docx files). This skill handles everything from simple document creation to complex document review workflows with tracked changes, comments, and sophisticated formatting preservation. Built on the Office Open XML (OOXML) standard, it enables programmatic manipulation of Word documents while maintaining full compatibility with Microsoft Word.

## Who Should Use This Skill

- **Legal Professionals** reviewing contracts and agreements with tracked changes
- **Business Analysts** creating formatted reports and documentation
- **Technical Writers** producing professional documentation with complex formatting
- **Contract Managers** making redlined edits to legal documents
- **Academic Researchers** working with scholarly documents and citations
- **Content Creators** building structured documents with consistent formatting
- **Anyone** needing to programmatically create or edit Word documents

## Purpose and Use Cases

Use this skill when you need to:
- Create new Word documents with professional formatting
- Edit existing documents while preserving original formatting
- Implement tracked changes (redlining) for document review
- Extract text and analyze document contents
- Add or modify comments in documents
- Work with document structure, headers, footers, and sections
- Convert documents between formats (DOCX to Markdown, PDF, images)
- Manipulate document metadata and properties

**Keywords that trigger this skill:** docx, word document, contract review, tracked changes, redlining, document editing, word processing

## What's Included

### Reading and Analysis Tools

**Text Extraction:**
- Convert DOCX to Markdown using Pandoc with tracked changes preserved
- Extract plain text from documents
- Analyze document structure and content
- Support for all tracked change visibility modes (accept/reject/all)

**Raw XML Access:**
- Unpack DOCX files to access underlying OOXML structure
- Read comments, complex formatting, and metadata
- Examine embedded media and document relationships
- Understand document structure at the XML level

### Document Creation

**docx-js Library:**
- Create new Word documents from scratch using JavaScript/TypeScript
- Build documents with Document, Paragraph, TextRun components
- Apply professional formatting and styles
- Export as .docx files using Packer.toBuffer()
- Full TypeScript type support for safe document construction

**Key Features:**
- Headers and footers
- Tables and lists
- Images and media
- Page numbering and sections
- Custom styles and themes

### Document Editing

**OOXML Document Library (Python):**
- Edit existing Word documents while preserving formatting
- High-level API for common document operations
- Direct DOM access for complex scenarios
- Automatic infrastructure setup and management
- Unpack, modify, and repack workflow

**Editing Capabilities:**
- Text replacement and modification
- Formatting changes
- Structure manipulation
- Comment addition and editing
- Metadata updates

### Redlining Workflow

**Professional Document Review:**
- Comprehensive tracked changes implementation
- Minimal, precise edits following best practices
- Batch processing for efficient change management
- RSID preservation for unchanged text
- Verification and validation of all changes

**Workflow Features:**
- Markdown-based planning before implementation
- Batched changes (3-10 changes per batch)
- XML-level change tracking
- Final verification with Pandoc conversion
- Support for legal, academic, business, and government documents

### Format Conversion

**Document to Images:**
- Two-step conversion: DOCX → PDF → JPEG/PNG
- Configurable resolution (DPI settings)
- Selective page ranges
- Multiple image formats supported

**Document to Markdown:**
- Structure-preserving conversion
- Tracked changes visibility control
- Excellent for text analysis and review

## How It Works

### Step-by-Step Process

**1. Reading/Analyzing Documents**

Choose your approach based on needs:

*Text Extraction:*
```bash
pandoc --track-changes=all document.docx -o output.md
```
- Best for: Reading content, analyzing text, understanding document flow
- Preserves: Document structure, tracked changes, basic formatting
- Output: Clean markdown file for easy reading

*Raw XML Access:*
```bash
python ooxml/scripts/unpack.py document.docx unpacked/
```
- Best for: Comments, complex formatting, embedded media, metadata
- Access: Complete OOXML structure
- Files: `word/document.xml`, `word/comments.xml`, `word/media/`

**2. Creating New Documents**

*Workflow:*
1. Read `docx-js.md` documentation completely (mandatory, ~500 lines)
2. Create JavaScript/TypeScript file using docx-js components
3. Build document with Document, Paragraph, TextRun
4. Export using Packer.toBuffer()

*Example Structure:*
```javascript
const doc = new Document({
  sections: [{
    properties: {},
    children: [
      new Paragraph({
        text: "Document content here",
        heading: HeadingLevel.HEADING_1,
      }),
    ],
  }],
});
```

**3. Editing Existing Documents**

*Basic Editing Workflow:*
1. Read `ooxml.md` documentation completely (mandatory, ~600 lines)
2. Unpack document: `python ooxml/scripts/unpack.py input.docx unpacked/`
3. Create Python script using Document library
4. Modify content using high-level API or direct DOM access
5. Pack document: `python ooxml/scripts/pack.py unpacked/ output.docx`

*Document Library Features:*
- High-level methods for common operations
- Direct DOM access for complex scenarios
- Automatic infrastructure management
- Preserves formatting and structure

**4. Redlining (Tracked Changes) Workflow**

*For Professional Document Review:*

Step 1 - Extract Current State:
```bash
pandoc --track-changes=all contract.docx -o current.md
```

Step 2 - Plan Changes:
- Review markdown to identify all needed changes
- Group into logical batches (3-10 changes per batch)
- Organize by section, type, or proximity
- Document location methods (section headings, grep patterns)

Step 3 - Prepare for Implementation:
- Read `ooxml.md` completely (mandatory, ~600 lines)
- Unpack document: `python ooxml/scripts/unpack.py contract.docx unpacked/`
- Note the suggested RSID from unpack output

Step 4 - Implement Changes in Batches:
For each batch:
- Grep `word/document.xml` to find exact XML structure
- Create Python script using Document library
- Use `get_node()` to find elements
- Implement tracked changes with proper XML tags
- Follow minimal edit principle (only mark what changed)

Step 5 - Pack and Verify:
```bash
python ooxml/scripts/pack.py unpacked/ reviewed.docx
pandoc --track-changes=all reviewed.docx -o verification.md
```

*Critical Principles:*
- **Minimal edits**: Only mark text that actually changes
- **RSID preservation**: Reuse original run's RSID for unchanged text
- **Batch processing**: Group 3-10 related changes together
- **Systematic verification**: Check all changes were applied correctly

**5. Format Conversion**

*DOCX to Images:*
```bash
# Step 1: Convert to PDF
soffice --headless --convert-to pdf document.docx

# Step 2: Convert PDF to images
pdftoppm -jpeg -r 150 document.pdf page
```

*DOCX to Markdown:*
```bash
pandoc document.docx -o document.md
```

### Quality Standards

**Document Creation:**
- Professional formatting and consistent styles
- Proper document structure (headers, sections, page numbers)
- Clean, maintainable code
- Concise implementation without verbose comments

**Document Editing:**
- Preserve original formatting unless specifically changed
- Maintain document structure and relationships
- Ensure all references remain valid
- Test changes before finalizing

**Tracked Changes:**
- Minimal, precise edits (mark only what changed)
- Professional appearance suitable for legal/business review
- All changes systematically verified
- Batch size of 3-10 changes for manageability

## Technical Details

### Document Structure

**OOXML Components:**
- `word/document.xml` - Main document content
- `word/styles.xml` - Styles and formatting definitions
- `word/comments.xml` - Comments and annotations
- `word/footnotes.xml` - Footnotes and endnotes
- `word/header*.xml` - Header content
- `word/footer*.xml` - Footer content
- `word/media/` - Embedded images and media
- `[Content_Types].xml` - Content type definitions
- `word/_rels/document.xml.rels` - Document relationships

**Tracked Changes XML:**
- `<w:ins>` - Insertions with author and timestamp
- `<w:del>` - Deletions with deleted text in `<w:delText>`
- `<w:rPr>` - Run properties (formatting)
- RSIDs for change tracking and identification

### Tools and Libraries

**Creation:**
- **docx-js** - JavaScript/TypeScript library for document creation
- Node.js environment with all dependencies installed
- TypeScript support for type-safe document construction

**Editing:**
- **Document library** - Python library for OOXML manipulation
- Automatic infrastructure setup and management
- High-level API with direct DOM access option

**Analysis:**
- **Pandoc** - Universal document converter with excellent DOCX support
- **defusedxml** - Secure XML parsing for OOXML files

**Conversion:**
- **LibreOffice** - Headless conversion to PDF
- **Poppler (pdftoppm)** - PDF to image conversion

### File Operations

**Unpacking:**
```bash
python ooxml/scripts/unpack.py <office_file> <output_directory>
```
- Extracts DOCX (ZIP archive) to directory structure
- Provides suggested RSID for tracked changes
- Preserves all XML relationships

**Packing:**
```bash
python ooxml/scripts/pack.py <input_directory> <office_file>
```
- Recreates DOCX from directory structure
- Validates XML structure
- Maintains proper ZIP compression and relationships

## Use Cases and Examples

### Legal Contract Review
**Scenario:** Attorney needs to redline a 50-page contract with 30 specific changes

**Workflow:**
1. Convert to markdown to identify all changes
2. Group changes into 5 batches (6 changes each)
3. Unpack document and read ooxml.md
4. Implement each batch with tracked changes
5. Pack and verify all changes applied correctly

**Key Features Used:** Redlining workflow, batch processing, minimal edits, verification

### Business Report Creation
**Scenario:** Create quarterly report with tables, charts, and formatted sections

**Workflow:**
1. Read docx-js.md documentation
2. Create JavaScript file with Document structure
3. Build sections with headers, tables, and content
4. Apply professional formatting and styles
5. Export to .docx file

**Key Features Used:** Document creation, formatting, tables, sections

### Document Analysis
**Scenario:** Extract and analyze content from 100 Word documents

**Workflow:**
1. Convert all documents to markdown using Pandoc
2. Read and analyze markdown files programmatically
3. Extract key information and generate report

**Key Features Used:** Text extraction, batch conversion, markdown analysis

### Template-Based Document Generation
**Scenario:** Generate personalized contracts from template

**Workflow:**
1. Unpack template document
2. Create Python script to modify specific fields
3. Use Document library to replace placeholders
4. Pack final documents

**Key Features Used:** Document editing, text replacement, batch processing

## Best Practices

### Reading and Analysis
- **Use Pandoc for text**: Convert to markdown for easy reading and analysis
- **Use XML for complexity**: Access raw XML only when needed (comments, metadata, complex formatting)
- **Preserve tracked changes**: Use `--track-changes=all` to see all edits
- **Verify structure**: Check document.xml to understand organization before editing

### Document Creation
- **Read documentation first**: Always read docx-js.md completely before coding (mandatory)
- **Plan structure**: Design document hierarchy before implementation
- **Use components**: Leverage Document, Paragraph, TextRun for clean code
- **Test incrementally**: Build and test sections progressively
- **Keep code concise**: Avoid verbose variable names and unnecessary comments

### Document Editing
- **Read documentation first**: Always read ooxml.md completely before editing (mandatory)
- **Understand before modifying**: Unpack and examine structure before changes
- **Use Document library**: Leverage high-level API for common operations
- **Preserve formatting**: Only change what's necessary
- **Test changes**: Verify edits before finalizing document

### Redlining Best Practices
- **Plan comprehensively**: Identify ALL changes before implementation
- **Batch logically**: Group 3-10 related changes together
- **Mark minimally**: Only mark text that actually changes
- **Preserve RSIDs**: Reuse original run's RSID for unchanged text
- **Verify systematically**: Convert to markdown and check all changes applied
- **Use grep first**: Always grep document.xml before writing scripts
- **Professional appearance**: Changes should look like human Word edits

### Code Quality
- **Concise code**: Write minimal Python/JavaScript without verbose comments
- **Avoid redundancy**: Don't repeat operations unnecessarily
- **No excessive printing**: Limit print statements to essential feedback
- **Meaningful names**: Use clear but not overly verbose variable names
- **Test edge cases**: Verify code works with various document structures

### Common Pitfalls to Avoid
- ❌ Editing documents without reading documentation first
- ❌ Making changes without unpacking to examine structure
- ❌ Implementing all redlines in one massive script (use batches instead)
- ❌ Marking entire sentences when only one word changed
- ❌ Not preserving RSIDs for unchanged text in tracked changes
- ❌ Failing to verify all changes were applied correctly
- ❌ Using markdown line numbers to locate XML elements (doesn't map correctly)
- ❌ Hardcoding values instead of using Document library methods
- ❌ Not testing changes before packing final document

## Dependencies

**Required (should be installed):**
- **pandoc** - Document conversion and text extraction
- **docx** (npm) - JavaScript library for creating documents
- **LibreOffice** - Headless PDF conversion
- **Poppler utilities** - PDF to image conversion (pdftoppm)
- **defusedxml** (Python) - Secure XML parsing

**Installation Commands (if needed):**
```bash
# Pandoc
sudo apt-get install pandoc

# docx-js (npm package)
npm install -g docx

# LibreOffice
sudo apt-get install libreoffice

# Poppler
sudo apt-get install poppler-utils

# defusedxml
pip install defusedxml
```

## Additional Resources

**Documentation Files:**
- `docx-js.md` - Complete docx-js library reference (~500 lines)
- `ooxml.md` - OOXML editing guide and Document library API (~600 lines)

**Scripts:**
- `ooxml/scripts/unpack.py` - Extract DOCX to directory
- `ooxml/scripts/pack.py` - Compress directory to DOCX

**Support Files:**
- Templates and examples in skill directory
- Reference implementations for common operations
