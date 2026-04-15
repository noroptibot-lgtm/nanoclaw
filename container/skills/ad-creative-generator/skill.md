# Ad Creative Generator

Generate professional Facebook/Instagram ad images with perfect Norwegian text from competitor research in Airtable.

## When to Use

Use when the user wants to:
- Create ad images based on competitor research
- Generate social media ad creatives for a specific niche
- Build an ad library from Airtable research data

## Prerequisites

- **Gemini API key**: `GEMINI_API_KEY` in `~/.env`
- **Airtable API key**: `AIRTABLE_ACCESS_TOKEN` in `~/.env`
- **Dropbox credentials**: `DROPBOX_REFRESH_TOKEN`, `DROPBOX_APP_KEY`, `DROPBOX_APP_SECRET` in `~/.env`
- **ImageMagick v7**: `magick` command (installed via Homebrew)
- **Fonts**: System fonts at `/System/Library/Fonts/Supplemental/`

## Pipeline

### Phase 1: Research (Airtable)

1. Fetch all records from the specified Airtable base/table via API
2. Analyze patterns: angles, formats, ad types, page names
3. Identify the best-performing ad concepts:
   - **Pain-to-Transformation**: Before/after comparisons
   - **Profit Problem**: Cost savings, price hooks
   - **Authority**: Data, comparisons, trust signals
   - **Social Proof**: Reviews, customer counts, ratings
   - **Tips/Education**: Checklists, lead magnets, guides
   - **Scarcity/Urgency**: Seasonal campaigns, limited offers

### Phase 2: Background Generation (Gemini API)

Generate background images WITHOUT any text using Gemini `gemini-2.5-flash-image` model:

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=$GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [{"parts": [{"text": "PROMPT HERE. NO TEXT anywhere. No watermarks."}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
  }'
```

**CRITICAL**: Always include "NO TEXT anywhere. No watermarks." in prompts. AI-generated text in Norwegian is always wrong.

Run multiple generations in parallel with `&` and `wait`.

### Phase 3: Text Overlay (ImageMagick)

Use `magick` (not `convert`) to overlay perfect Norwegian text on backgrounds.

**Available fonts:**
- Headlines: `/System/Library/Fonts/Supplemental/Impact.ttf`
- Bold text: `/System/Library/Fonts/Supplemental/Arial Bold.ttf`
- Body text: `/System/Library/Fonts/Supplemental/Arial Narrow.ttf`

**Standard overlay pattern:**

```python
# Semi-transparent overlay for readability
subprocess.run([
    "magick", bg_path,
    "-resize", "1080x1080^", "-gravity", "center", "-extent", "1080x1080",
    "(", "-size", "1080x1080", "xc:black",
    "-alpha", "set", "-channel", "A", "-evaluate", "set", "35%", "+channel", ")",
    "-composite", tmp_path
], check=True)

# Text with stroke for contrast on photos
cmd = [
    "magick", tmp_path,
    "-gravity", "NorthWest", "-font", FONT_IMPACT, "-pointsize", "72",
    "-fill", "black", "-stroke", "black", "-strokewidth", "3",
    "-annotate", "+40+50", "HEADLINE TEXT",
    "-stroke", "none", "-fill", "white",
    "-annotate", "+40+50", "HEADLINE TEXT",
    out_path
]
```

### Phase 4: Quality Checks

Before uploading, verify every ad:

1. **Rettskriving**: All Norwegian text is perfectly spelled
2. **Kontrast**: Text is readable against background (use overlays + stroke)
3. **Lesbarhet**: Font sizes are large enough, spacing is clear
4. **Formatering**: Clear hierarchy — headline → subtext → bullets → CTA
5. **Faktasjekk**: All claims are accurate and verifiable

### Phase 5: Upload to Dropbox

Refresh token and upload:

```bash
# Refresh token
TOKEN=$(curl -s -X POST 'https://api.dropbox.com/oauth2/token' \
  -d grant_type=refresh_token \
  -d refresh_token=$DROPBOX_REFRESH_TOKEN \
  -d client_id=$DROPBOX_APP_KEY \
  -d client_secret=$DROPBOX_APP_SECRET | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])")

# Create folder
curl -s -X POST 'https://api.dropboxapi.com/2/files/create_folder_v2' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"path": "/Ad Creatives/FOLDER_NAME"}'

# Upload file
curl -s -X POST 'https://content.dropboxapi.com/2/files/upload' \
  -H "Authorization: Bearer $TOKEN" \
  -H "Dropbox-API-Arg: {\"path\": \"/Ad Creatives/FOLDER_NAME/FILE.png\", \"mode\": \"overwrite\"}" \
  -H 'Content-Type: application/octet-stream' \
  --data-binary @"local_file.png"
```

## Design Rules

- **Format**: 1080x1080 (square) for FB/IG feed
- **Overlay opacity**: 25-45% black for photo backgrounds
- **Headline font**: Impact, 60-90pt, white with black stroke (width 3)
- **Subtext font**: Arial Bold, 26-34pt
- **Body font**: Arial Narrow, 22-28pt
- **CTA**: Always at bottom, "→" arrow suffix
- **Checkmarks**: Use "✓" (not emoji ✅) for bullet points
- **Colors**: Green (#22c55e) for positive, Red (#ff6b6b/#ef4444) for negative, Yellow (#fbbf24) for highlights, Navy (#1e3a5f) for authority
- **Badge**: Green circle for "GRATIS BEFARING" etc.

## Ad Structure Template

Each ad should have:
1. **Headline** (1-3 words, Impact font, top-left or center)
2. **Sub-headline** (accent color, immediately below)
3. **Body copy** (2-4 lines max, clear benefit statements)
4. **Trust signals** (checkmarks, stars, numbers)
5. **CTA** (bottom, with arrow →)

## Language Rules

- All text in bokmål Norwegian (not nynorsk, not Swedish, not Danish)
- Use "opptil" not "optil", "Uforpliktende" not "Uforpliktende"
- Use Norwegian quotes: «tekst» not "tekst"
- Percent: "50 %" with space before %
- Prices: "18 995 kr" with space as thousands separator
- Verify all claims are factually accurate before including
