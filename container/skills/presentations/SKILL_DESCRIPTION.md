# Presentations (PPTX)

## Overview

The Presentations skill provides comprehensive capabilities for creating, editing, and analyzing professional PowerPoint presentations (.pptx files). This skill handles everything from creating sophisticated presentations from scratch with custom designs to editing existing presentations while preserving formatting, working with templates, and extracting content for analysis. Built on Office Open XML (OOXML) standards and modern presentation libraries, it enables complete presentation workflow automation with professional-quality output.

## Who Should Use This Skill

- **Business Professionals** creating pitch decks and presentations
- **Marketing Teams** developing branded presentation materials
- **Designers** producing visually sophisticated slide decks
- **Educators** building educational presentations and course materials
- **Consultants** generating client presentations and reports
- **Product Managers** creating product roadmaps and strategy decks
- **Sales Teams** preparing sales presentations and proposals
- **Anyone** needing to programmatically create or edit PowerPoint presentations

## Purpose and Use Cases

Use this skill when you need to:
- Create new presentations from scratch with custom designs
- Edit existing presentations while preserving formatting
- Use templates to generate multiple presentations
- Extract text and content from presentations
- Add speaker notes and comments to slides
- Work with slide layouts and master slides
- Convert presentations to images or other formats
- Automate presentation generation from data
- Implement consistent branding across presentations
- Create multi-page presentation series

**Keywords that trigger this skill:** pptx, powerpoint, presentation, slides, pitch deck, slide design, presentation editing

## What's Included

### Reading and Analysis Tools

**Text Extraction:**
- Convert PPTX to Markdown using markitdown
- Extract all text content from slides
- Preserve slide structure in markdown
- Analyze presentation content programmatically

**Visual Analysis:**
- Create thumbnail grids for quick visual overview
- Convert slides to individual images (JPEG/PNG)
- Zero-indexed slide numbering (Slide 0, Slide 1, etc.)
- Customizable grid layouts (3-6 columns, up to 42 slides per grid)

**Raw XML Access:**
- Unpack PPTX files to access underlying OOXML structure
- Read speaker notes, comments, and annotations
- Examine slide layouts and master slides
- Access theme and styling information
- Analyze embedded media and design elements

### Presentation Creation (Without Templates)

**html2pptx Workflow:**
- Create presentations from HTML slides
- Accurate positioning and layout control
- Professional design principles and color palettes
- Typography best practices
- Chart and table integration

**Design Philosophy Approach:**
- Content-informed design choices
- Subject-appropriate color palette selection
- Creative, non-generic design frameworks
- 18 example color palettes provided
- Extensive visual detail options

**Visual Validation:**
- Generate thumbnail grids for quality checking
- Inspect for text cutoff, overlap, positioning issues
- Verify contrast and readability
- Iterative refinement process

### Presentation Creation (With Templates)

**Template-Based Workflow:**
- Extract and analyze template structure
- Create visual thumbnail grids for template inventory
- Duplicate and rearrange template slides
- Replace placeholder text while preserving formatting
- Systematic text replacement with validation

**Advanced Template Features:**
- JSON-based text inventory and replacement
- Automatic shape clearing and text replacement
- Paragraph formatting preservation
- Bullet list handling
- Theme color support
- Overflow detection and validation

### Presentation Editing

**OOXML Editing:**
- Edit existing presentations at XML level
- Modify slide content while preserving formatting
- Update speaker notes and comments
- Change slide layouts and master slides
- Validation after each edit

**Structured Workflow:**
1. Unpack presentation to directory
2. Edit XML files directly
3. Validate changes immediately
4. Pack back to PPTX format

## How It Works

### Step-by-Step Process

**1. Reading and Analyzing Presentations**

*Text Extraction:*
```bash
python -m markitdown presentation.pptx
```
- Converts entire presentation to readable markdown
- Preserves slide structure and hierarchy
- Ideal for content analysis

*Visual Analysis with Thumbnails:*
```bash
python scripts/thumbnail.py presentation.pptx
# Creates thumbnails.jpg with 5×6 grid (30 slides)

python scripts/thumbnail.py presentation.pptx analysis --cols 4
# Creates analysis-1.jpg with 4×5 grid (20 slides)
```
- Quick visual overview of entire deck
- Identify layout patterns and design elements
- Zero-indexed slide numbering (0, 1, 2...)
- Multiple grids for large presentations

*Raw XML Access:*
```bash
python ooxml/scripts/unpack.py presentation.pptx unpacked/
```
- Access complete OOXML structure
- Read `ppt/slides/slide{N}.xml` for content
- Check `ppt/notesSlides/notesSlide{N}.xml` for speaker notes
- Examine `ppt/theme/theme1.xml` for design theme

**2. Creating Presentations Without Templates**

*Design-First Approach:*

Step 1 - Develop Design Philosophy:
- Analyze content and subject matter
- Choose appropriate color palette (18 examples provided)
- Select design principles (geometric, chromatic, organic, etc.)
- State design approach before implementation

Step 2 - Read Documentation:
```bash
# Read html2pptx.md completely (mandatory)
# ~500 lines covering HTML to PPTX conversion
```

Step 3 - Create HTML Slides:
- Build HTML files for each slide (720pt × 405pt for 16:9)
- Use semantic HTML: `<p>`, `<h1>-<h6>`, `<ul>`, `<ol>`
- Add `class="placeholder"` for chart/table areas
- Rasterize gradients and icons as PNG using Sharp
- Use two-column layout for charts/tables

Step 4 - Convert to PPTX:
```javascript
// Use html2pptx.js library
// Add charts/tables using PptxGenJS API
// Save with pptx.writeFile()
```

Step 5 - Visual Validation:
```bash
python scripts/thumbnail.py output.pptx workspace/thumbnails --cols 4
```
- Inspect for text cutoff, overlap, positioning issues
- Check contrast and readability
- Adjust and regenerate if needed

*Design Principles:*
- Use web-safe fonts only
- Create clear visual hierarchy
- Ensure strong contrast and readability
- Be consistent across slides
- Match palette to content
- Consider audience and context

**3. Creating Presentations With Templates**

*Template-Based Workflow:*

Step 1 - Extract and Analyze Template:
```bash
# Extract text content
python -m markitdown template.pptx > template-content.md

# Create visual thumbnail grid
python scripts/thumbnail.py template.pptx
```

Step 2 - Create Template Inventory:
- Review thumbnail grid for visual structure
- Document each slide with index and description
- Save as `template-inventory.md`
- Note: Slides are zero-indexed (0, 1, 2...)

Example inventory:
```markdown
# Template Inventory Analysis
**Total Slides: 73**
**IMPORTANT: Slides are 0-indexed (first slide = 0, last = 72)**

## Title Slides
- Slide 0: Title/Cover slide
- Slide 1: Section intro layout

## Content Slides
- Slide 34: Two-column text layout
- Slide 50: Quote layout
...
```

Step 3 - Plan Content and Select Templates:
- Match content to appropriate layouts
- Verify placeholder count matches content
- Don't force content into wrong layouts
- Create `outline.md` with template mapping

Example mapping:
```python
template_mapping = [
    0,   # Title slide
    34,  # Two-column content
    34,  # Duplicate for second content slide
    50,  # Quote slide
    54,  # Closing slide
]
```

Step 4 - Rearrange Slides:
```bash
python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,54
```
- Duplicates, reorders, and removes slides automatically
- Creates new presentation with selected layouts

Step 5 - Extract Text Inventory:
```bash
python scripts/inventory.py working.pptx text-inventory.json
```
- Extracts all text shapes with properties
- JSON structure with slides, shapes, paragraphs
- Includes formatting: fonts, colors, bullets, alignment

Step 6 - Create Replacement JSON:
- Generate new content based on inventory structure
- Include paragraph formatting from original
- Only shapes with "paragraphs" get new text
- Unlisted shapes automatically cleared
- Save as `replacement-text.json`

Critical formatting rules:
```json
{
  "slide-0": {
    "shape-0": {
      "paragraphs": [
        {
          "text": "Title Text",
          "alignment": "CENTER",
          "bold": true
        },
        {
          "text": "Bullet point text",
          "bullet": true,
          "level": 0
        },
        {
          "text": "Regular text"
        }
      ]
    }
  }
}
```

Step 7 - Apply Replacements:
```bash
python scripts/replace.py working.pptx replacement-text.json output.pptx
```
- Validates all shapes exist
- Clears ALL shapes from inventory
- Applies new text with formatting
- Detects overflow issues

**4. Editing Existing Presentations**

*OOXML Editing Workflow:*

Step 1 - Read Documentation:
```bash
# Read ooxml.md completely (mandatory)
# ~500 lines covering OOXML structure and editing
```

Step 2 - Unpack Presentation:
```bash
python ooxml/scripts/unpack.py presentation.pptx unpacked/
```

Step 3 - Edit XML Files:
- Modify `ppt/slides/slide{N}.xml` for content
- Update `ppt/notesSlides/notesSlide{N}.xml` for notes
- Edit `ppt/comments/modernComment_*.xml` for comments

Step 4 - Validate Changes:
```bash
python ooxml/scripts/validate.py unpacked/ --original presentation.pptx
```
- Fix any validation errors before proceeding

Step 5 - Pack Presentation:
```bash
python ooxml/scripts/pack.py unpacked/ edited-presentation.pptx
```

**5. Converting Presentations to Images**

*Two-Step Process:*

Step 1 - Convert to PDF:
```bash
soffice --headless --convert-to pdf presentation.pptx
```

Step 2 - Convert PDF to Images:
```bash
pdftoppm -jpeg -r 150 presentation.pdf slide
# Creates slide-1.jpg, slide-2.jpg, etc.

# Specific range
pdftoppm -jpeg -r 150 -f 2 -l 5 presentation.pdf slide
```

*Options:*
- `-r 150`: Resolution (DPI)
- `-jpeg` or `-png`: Output format
- `-f N`: First page
- `-l N`: Last page

### Quality Standards

**Design Quality:**
- Professional, sophisticated aesthetics
- Subject-appropriate design choices
- Strong contrast and readability
- Consistent visual language
- Never cartoony or amateur-looking

**Technical Quality:**
- High resolution for display
- Proper color management
- Clean, precise execution
- Format appropriate to content

**Template Quality:**
- Exact layout matching
- Formatting preservation
- No text overflow
- Proper bullet formatting
- Theme color consistency

## Technical Details

### PPTX Structure

**Key OOXML Files:**
- `ppt/presentation.xml` - Main metadata and slide references
- `ppt/slides/slide{N}.xml` - Individual slide content
- `ppt/slideLayouts/` - Layout templates
- `ppt/slideMasters/` - Master slide templates
- `ppt/theme/` - Theme and styling
- `ppt/notesSlides/notesSlide{N}.xml` - Speaker notes
- `ppt/comments/modernComment_*.xml` - Comments
- `ppt/media/` - Images and media

**Typography and Color:**
- `ppt/theme/theme1.xml` contains:
  - `<a:clrScheme>` - Color definitions
  - `<a:fontScheme>` - Font specifications
- Slide XML contains:
  - `<a:rPr>` - Font usage
  - `<a:solidFill>` - Fill colors
  - `<a:srgbClr>` - RGB colors

### Tools and Libraries

**Creation:**
- **html2pptx** - Convert HTML to PowerPoint
- **PptxGenJS** - Add charts and tables
- **Playwright** - HTML rendering
- **Sharp** - Image processing and SVG rasterization

**Editing:**
- **markitdown** - Text extraction
- **defusedxml** - Secure XML parsing
- OOXML scripts (unpack, pack, validate)

**Analysis:**
- **thumbnail.py** - Visual thumbnail grids
- **inventory.py** - Text shape extraction
- **rearrange.py** - Slide duplication and reordering
- **replace.py** - Systematic text replacement

**Conversion:**
- **LibreOffice** - Headless PDF conversion
- **Poppler (pdftoppm)** - PDF to image conversion

### Inventory JSON Structure

**Complete Structure:**
```json
{
  "slide-0": {
    "shape-0": {
      "placeholder_type": "TITLE",
      "left": 1.5,
      "top": 2.0,
      "width": 7.5,
      "height": 1.2,
      "default_font_size": 44.0,
      "paragraphs": [
        {
          "text": "Paragraph text",
          "bullet": true,
          "level": 0,
          "alignment": "CENTER",
          "space_before": 10.0,
          "space_after": 6.0,
          "line_spacing": 22.4,
          "font_name": "Arial",
          "font_size": 14.0,
          "bold": true,
          "italic": false,
          "underline": false,
          "color": "FF0000",
          "theme_color": "DARK_1"
        }
      ]
    }
  }
}
```

**Key Features:**
- Zero-indexed slides and shapes
- Placeholder types: TITLE, CENTER_TITLE, SUBTITLE, BODY, OBJECT, or null
- Optional properties only included when non-default
- Bullet lists include level (0, 1, 2...)
- Colors: RGB (`color`) or theme (`theme_color`)

## Use Cases and Examples

### Pitch Deck Creation
**Scenario:** Create investor pitch deck with custom branding

**Workflow:**
1. Develop design philosophy based on company brand
2. Select appropriate color palette
3. Create HTML slides with custom design
4. Convert to PPTX with charts and data
5. Generate thumbnails for review
6. Iterate based on feedback

**Key Features Used:** html2pptx, design philosophy, visual validation

### Template-Based Reports
**Scenario:** Generate 50 client reports from standard template

**Workflow:**
1. Analyze template and create inventory
2. Create outline mapping content to templates
3. Rearrange template slides
4. Extract text inventory
5. Generate replacement JSON for each client
6. Batch process with replace.py

**Key Features Used:** Template workflow, rearrange.py, inventory.py, replace.py

### Presentation Analysis
**Scenario:** Analyze content of 100 presentations for compliance

**Workflow:**
1. Convert all presentations to markdown
2. Extract text content programmatically
3. Search for specific keywords or patterns
4. Generate compliance report

**Key Features Used:** Text extraction, batch processing

### Design Updates
**Scenario:** Update company logo across 30 presentations

**Workflow:**
1. Unpack all presentations
2. Replace logo images in `ppt/media/`
3. Update references in slide XML
4. Validate and pack presentations

**Key Features Used:** OOXML editing, batch processing

### Educational Content
**Scenario:** Create course materials with consistent branding

**Workflow:**
1. Create master template with course branding
2. Generate thumbnails for visual reference
3. Use template workflow for each lecture
4. Apply consistent formatting across all decks

**Key Features Used:** Template creation, thumbnail grids, systematic formatting

## Best Practices

### Design Creation
- **State your approach first**: Explain design choices before implementation
- **Match content to design**: Choose colors and style based on subject
- **Use web-safe fonts**: Stick to reliable, cross-platform fonts
- **Ensure readability**: Strong contrast, appropriate sizing
- **Maintain consistency**: Repeat visual patterns across slides
- **Validate visually**: Always generate thumbnails and inspect

### Template Usage
- **Create visual inventory**: Use thumbnail grids to understand structure
- **Match layouts to content**: Don't force content into wrong layouts
- **Count placeholders**: Verify layout has right number of elements
- **Preserve formatting**: Include all paragraph properties in replacements
- **Validate replacements**: Check all shapes exist before applying
- **Test first**: Process one presentation before batch operations

### OOXML Editing
- **Read documentation first**: Always read ooxml.md before editing
- **Validate immediately**: Run validate.py after each XML change
- **Backup originals**: Keep copies before editing
- **Test incrementally**: Make small changes and test
- **Understand structure**: Examine unpacked files before modifying

### Text Replacement
- **Include formatting**: Provide paragraph properties, not just text
- **Handle bullets properly**: Use `bullet: true, level: 0`, no symbols in text
- **Preserve alignment**: Include alignment from original when needed
- **Use theme colors**: Prefer `theme_color` over hardcoded `color`
- **Check overflow**: Review validation warnings about text overflow

### Common Pitfalls to Avoid
- ❌ Creating presentations without stating design approach first
- ❌ Using generic color palettes without considering content
- ❌ Not generating thumbnails for visual validation
- ❌ Forcing content into layouts with wrong placeholder count
- ❌ Creating replacement JSON without checking inventory first
- ❌ Not preserving paragraph formatting in replacements
- ❌ Including bullet symbols (•, -, *) in bullet text
- ❌ Editing XML without validating changes
- ❌ Not using zero-indexed slide numbers (0, 1, 2...)
- ❌ Hardcoding slide indices without verifying total slide count
- ❌ Referencing shapes that don't exist in inventory
- ❌ Not testing on single presentation before batch processing

## Color Palette Examples

**18 Creative Palettes:**

1. Classic Blue: #1C2833, #2E4053, #AAB7B8, #F4F6F6
2. Teal & Coral: #5EA8A7, #277884, #FE4447, #FFFFFF
3. Bold Red: #C0392B, #E74C3C, #F39C12, #F1C40F, #2ECC71
4. Warm Blush: #A49393, #EED6D3, #E8B4B8, #FAF7F2
5. Burgundy Luxury: #5D1D2E, #951233, #C15937, #997929
6. Deep Purple & Emerald: #B165FB, #181B24, #40695B, #FFFFFF
7. Cream & Forest Green: #FFE1C7, #40695B, #FCFCFC
8. Pink & Purple: #F8275B, #FF574A, #FF737D, #3D2F68
9. Lime & Plum: #C5DE82, #7C3A5F, #FD8C6E, #98ACB5
10. Black & Gold: #BF9A4A, #000000, #F4F6F6
11. Sage & Terracotta: #87A96B, #E07A5F, #F4F1DE, #2C2C2C
12. Charcoal & Red: #292929, #E33737, #CCCBCB
13. Vibrant Orange: #F96D00, #F2F2F2, #222831
14. Forest Green: #191A19, #4E9F3D, #1E5128, #FFFFFF
15. Retro Rainbow: #722880, #D72D51, #EB5C18, #F08800, #DEB600
16. Vintage Earthy: #E3B448, #CBD18F, #3A6B35, #F4F1DE
17. Coastal Rose: #AD7670, #B49886, #F3ECDC, #BFD5BE
18. Orange & Turquoise: #FC993E, #667C6F, #FCFCFC

## Dependencies

**Required (should be installed):**
- **markitdown** - Text extraction from presentations
- **pptxgenjs** - Presentation creation
- **playwright** - HTML rendering
- **sharp** - Image processing and SVG rasterization
- **LibreOffice** - PDF conversion
- **Poppler** - PDF to image conversion
- **defusedxml** - Secure XML parsing

**Installation Commands (if needed):**
```bash
# markitdown
pip install "markitdown[pptx]"

# pptxgenjs
npm install -g pptxgenjs

# playwright
npm install -g playwright

# sharp
npm install -g sharp

# LibreOffice
sudo apt-get install libreoffice

# Poppler
sudo apt-get install poppler-utils

# defusedxml
pip install defusedxml
```

## Additional Resources

**Documentation Files:**
- `html2pptx.md` - Complete HTML to PPTX conversion guide (~500 lines)
- `ooxml.md` - OOXML structure and editing guide (~500 lines)

**Scripts:**
- `ooxml/scripts/unpack.py` - Extract PPTX to directory
- `ooxml/scripts/pack.py` - Compress directory to PPTX
- `ooxml/scripts/validate.py` - Validate XML structure
- `scripts/thumbnail.py` - Generate visual thumbnail grids
- `scripts/inventory.py` - Extract text shape inventory
- `scripts/rearrange.py` - Duplicate and reorder slides
- `scripts/replace.py` - Apply text replacements
- `scripts/html2pptx.js` - Convert HTML to PPTX

**Support Files:**
- Templates and examples in skill directory
- Reference implementations for common operations
