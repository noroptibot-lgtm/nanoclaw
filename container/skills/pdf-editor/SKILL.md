---
name: pdf-editor
description: Edit PDFs with natural-language instructions from the terminal. Use when the user wants to modify, update, or fix content in a PDF file.
metadata:
  tags: pdf, editing, documents
  requires_bin: nano-pdf
---

# PDF Editor

Edit PDF files using plain-English instructions from the command line.

## Install

```bash
uv tool install nano-pdf
```

Or with pip:
```bash
pip install nano-pdf
```

## Usage

```bash
nano-pdf edit <file.pdf> <page_number> "<instruction>"
```

## Examples

```bash
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"
nano-pdf edit report.pdf 3 "Update the date to March 2026"
nano-pdf edit proposal.pdf 1 "Replace 'Draft' with 'Final' in the header"
```

## Notes

- Page numbers may be 0-based or 1-based depending on version; if the edit lands on the wrong page, retry with the other numbering
- Always review the output PDF before sending it out
