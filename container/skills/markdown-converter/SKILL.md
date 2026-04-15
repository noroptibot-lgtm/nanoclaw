---
name: markdown-converter
description: Convert documents and files to Markdown using markitdown. Use when converting PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls), HTML, CSV, JSON, XML, images (with EXIF/OCR), audio (with transcription), ZIP archives, YouTube URLs, or EPubs to Markdown format for LLM processing or text analysis.
metadata:
  tags: markdown, converter, pdf, docx, pptx, xlsx, html, csv, json, xml
  requires_bin: uvx
  optional_env:
    - AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
---

# Markdown Converter

Convert files to Markdown using `uvx markitdown`.

## Prerequisites

- Python 3.10+ installed
- `uvx` (part of the `uv` Python package manager)

### Install uv

```bash
# macOS
brew install uv

# Or via the official installer
curl -LsSf https://astral.sh/uv/install.sh | sh
```

`uvx` comes bundled with `uv`. First run of `uvx markitdown` will automatically download and cache the markitdown package.

## Basic Usage

```bash
# Convert to stdout
uvx markitdown input.pdf

# Save to file
uvx markitdown input.pdf -o output.md
uvx markitdown input.docx > output.md

# From stdin
cat input.pdf | uvx markitdown
```

## Supported Formats

- **Documents**: PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls)
- **Web/Data**: HTML, CSV, JSON, XML
- **Media**: Images (EXIF + OCR), Audio (EXIF + transcription)
- **Other**: ZIP (iterates contents), YouTube URLs, EPub

## Options

```bash
-o OUTPUT      # Output file
-x EXTENSION   # Hint file extension (for stdin)
-m MIME_TYPE    # Hint MIME type
-c CHARSET     # Hint charset (e.g., UTF-8)
-d             # Use Azure Document Intelligence (sends file to Azure — see warning below)
-e ENDPOINT    # Document Intelligence endpoint
--use-plugins  # Enable 3rd-party plugins (see warning below)
--list-plugins # Show installed plugins
```

## Examples

```bash
# Convert Word document
uvx markitdown report.docx -o report.md

# Convert Excel spreadsheet
uvx markitdown data.xlsx > data.md

# Convert PowerPoint presentation
uvx markitdown slides.pptx -o slides.md

# Convert with file type hint (for stdin)
cat document | uvx markitdown -x .pdf > output.md
```

## Azure Document Intelligence (Optional)

For complex PDFs with poor extraction, you can use Azure's Document Intelligence service. This **sends your file contents to Azure** for processing.

```bash
# Set your endpoint as an environment variable
export AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT="https://your-resource.cognitiveservices.azure.com/"

uvx markitdown scan.pdf -d -e "$AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"
```

You'll need an Azure account with a Document Intelligence resource. Do not use this with sensitive documents unless you trust Azure with that data.

## Warnings

- **`-d` flag (Azure)**: Sends your document to Microsoft Azure for processing. Only use with files you're comfortable uploading to a cloud service.
- **`--use-plugins`**: Enables third-party plugins that may execute code or make network requests. Only use plugins you've reviewed and trust. Run `--list-plugins` first to see what's installed.
- **YouTube URLs**: Fetches content from YouTube, which involves network requests to Google's servers.

## Notes

- Output preserves document structure: headings, tables, lists, links
- First run caches dependencies; subsequent runs are faster
- All local conversions (PDF, DOCX, etc.) run entirely on your machine — no data leaves your computer unless you use `-d` or YouTube URLs
