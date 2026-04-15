---
name: pdf-to-kindle
description: Find free legal PDFs of books or papers online and deliver them to Albert's Kindle. Trigger on /pdf-to-kindle or when Albert asks to find a PDF/book/paper and send to Kindle.
---

# PDF to Kindle

Find a PDF online from legitimate sources and deliver it to Albert's Kindle via the Send to Kindle email service.

## When to use

- Albert says "find me a PDF of X", "get me the book Y", "send Z to my Kindle"
- Academic papers he wants to read later on the Kindle
- Public-domain books he wants to read offline
- The `/pdf-to-kindle <title>` slash command

## Hard rules (no exceptions)

- Only use legitimate, legal sources. Never Library Genesis, Z-Library, Sci-Hub, PDFDrive, or any torrent/piracy site.
- If a book is in copyright and not freely offered by the publisher/author, tell Albert it is not legally free and suggest the cheapest legal route (Kindle Store, library via Libby, used copy on Amazon).
- Do not bypass paywalls.

## Legitimate source priority

Search in this order, stop at the first hit that matches:

| # | Source | Best for | URL pattern |
|---|--------|----------|-------------|
| 1 | Project Gutenberg | Public domain books (pre-1929 US) | gutenberg.org |
| 2 | Standard Ebooks | Curated public domain, better formatting | standardebooks.org |
| 3 | Internet Archive / Open Library | Scanned books, borrowable titles | archive.org, openlibrary.org |
| 4 | arXiv | Physics, math, CS, stats papers | arxiv.org |
| 5 | Unpaywall / DOI.org | Open-access academic papers | unpaywall.org, doi.org |
| 6 | PubMed Central | Biomedical open-access papers | ncbi.nlm.nih.gov/pmc |
| 7 | SSRN | Economics, social sciences preprints | ssrn.com |
| 8 | Author's personal website | Authors often post free PDFs | google with `site:...` |
| 9 | Publisher open-access | Springer Open, O'Reilly OA, MIT Press Open | check publisher |
| 10 | Google Scholar | Links to free versions where they exist | scholar.google.com |

## Delivery methods

### Method 1: Send to Kindle email (preferred, fully automated)

Requires one-time setup by Albert:
1. Go to https://www.amazon.com/sendtokindle → Settings
2. Find his personal @kindle.com email (e.g. `albert_xxxx@kindle.com`)
3. Add `noroptibot@gmail.com` to approved sender list
4. Save the kindle email to `~/.env` as `KINDLE_EMAIL=albert_xxxx@kindle.com`

Once set up, automate:
1. Download the PDF with curl to `/tmp/pdf-to-kindle/<sanitized-title>.pdf`
2. Verify file size is reasonable (>50KB, <50MB, Kindle limit)
3. Send via Gmail with attachment using the Gmail MCP or Python smtplib
   - Subject: `convert` (to auto-convert to Kindle format) or the book title
   - From: noroptibot@gmail.com
   - To: `$KINDLE_EMAIL`
4. Confirm to Albert with title and delivery ETA (usually under 15 min on Kindle)

### Method 2: Web upload (fallback, requires Albert's Amazon login)

Use Playwright browser automation:
1. Navigate to https://www.amazon.com/sendtokindle
2. Albert must already be signed into Amazon in the browser session
3. Upload the PDF file
4. Confirm

Use this only if email delivery fails or setup is incomplete.

## Workflow

1. Parse the request: extract title, author, and whether it's a book or paper
2. Search legitimate sources in priority order (use WebSearch + WebFetch)
3. Verify the find: is it really free? Is it the right edition?
4. If found:
   a. Download to `/tmp/pdf-to-kindle/`
   b. Check file size and format
   c. Deliver via Method 1 (email) or Method 2 (browser)
   d. Confirm to Albert with source and delivery status
5. If NOT found legally free:
   a. Tell Albert honestly
   b. Suggest cheapest legal route: Kindle Store price, library via Libby/BookBeat, used paperback
   c. Do NOT fall back to piracy sites

## File management

- Download location: `/tmp/pdf-to-kindle/`
- Sanitize filenames: lowercase, replace spaces with dashes, strip special chars
- Clean up: delete files older than 24 hours at the start of each run

## Example interactions

**Example 1 - public domain book:**
Albert: "Get me Meditations by Marcus Aurelius on Kindle"
→ Found on Standard Ebooks (curated public domain) → download → email to Kindle → confirm

**Example 2 - academic paper:**
Albert: "Find the Attention Is All You Need paper and send to my Kindle"
→ Found on arXiv (arxiv.org/abs/1706.03762) → download PDF → email → confirm

**Example 3 - copyrighted book:**
Albert: "Get me the latest Huberman book free"
→ Not legally free. Tell Albert: "Not available free. Cheapest legal: Kindle Store 249 kr, or Libby via Deichman library free if you have a library card."

**Example 4 - paywalled paper:**
Albert: "Find this Nature paper, here's the DOI"
→ Check Unpaywall first for open-access version. If none exists, tell Albert and suggest the author's personal page or ResearchGate preprint if available. Do NOT use Sci-Hub.

## Gmail send helper

If using Gmail MCP is not available, use this Python one-liner pattern:

```python
import smtplib
from email.message import EmailMessage
from pathlib import Path
import os

msg = EmailMessage()
msg['Subject'] = 'convert'
msg['From'] = 'noroptibot@gmail.com'
msg['To'] = os.environ['KINDLE_EMAIL']
msg.set_content('Sent from pdf-to-kindle skill')

pdf_path = Path('/tmp/pdf-to-kindle/book.pdf')
msg.add_attachment(
    pdf_path.read_bytes(),
    maintype='application',
    subtype='pdf',
    filename=pdf_path.name,
)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
    s.login('noroptibot@gmail.com', os.environ['GMAIL_APP_PASSWORD'])
    s.send_message(msg)
```

Requires `GMAIL_APP_PASSWORD` in `~/.env` (Gmail app-specific password, not account password).

## Confirmation format (Telegram reply)

Keep it tight:

```
Fant: <title> av <author>
Kilde: <source>
Sendt til Kindle. Dukker opp innen 15 min.
```

If not found legally free:
```
<title> er ikke gratis lovlig.
Billigste lovlige: <option + price>
```
