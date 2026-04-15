---
name: morning-visuals
description: Daily morning routine - 2 jobs sent to Telegram at 06:00. Job 1 - Reading visual breakdowns from Notion notes (8-10 concept graphics). Job 2 - POV manifestation images (10 first-person scenes). Trigger on /morning-visuals or via cron.
---

# Morning Visuals - Daily Telegram Delivery

Two daily jobs that generate images and send them to Albert's Telegram at 06:00.

## Environment

```bash
TELEGRAM_BOT_TOKEN="8289376147:AAHJe6Xd-qZvO8hiaG2F7niB9Rz9ywJnLyQ"
TELEGRAM_CHAT_ID="1973890232"
```

## Telegram Send Functions

Send photo with caption:
```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPhoto" \
  -F "chat_id=${TELEGRAM_CHAT_ID}" \
  -F "photo=@/path/to/image.png" \
  -F "caption=your caption" \
  -F "parse_mode=Markdown"
```

Send text:
```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -F "chat_id=${TELEGRAM_CHAT_ID}" \
  -F "text=your text" \
  -F "parse_mode=Markdown"
```

Sleep 2 seconds between each send to avoid rate limits.

---

## JOB 1: READING VISUAL BREAKDOWN

8-10 concept graphics from Notion reading notes.

### Step 1 - Fetch notes from Notion

Check which of these 3 pages was edited MOST RECENTLY using the Notion MCP:

- A Happy Pocket Full of Money: `311f1288-46d6-80de-9a39-f89b763e42bc`
- Essentialism: `324f1288-46d6-8080-b694-d902f2e381c5`
- My Goals - I AM: `321f1288-46d6-8113-a9fa-d8f8cca75750`

Use `mcp__notion__API-retrieve-a-page` for each to check `last_edited_time`.
Then use `mcp__notion__API-get-block-children` on the most recent one to get content.
Extract all paragraph and bullet text. These are Albert's reading notes.

### Step 2 - Generate 8-10 images

Extract 8-10 distinct concepts from the notes. For EACH, generate one image using the nano-banana skill (Gemini image generation).

### QUALITY RULES FOR EVERY GRAPHIC

- Someone who NEVER read this material must understand the concept just by looking at the image
- Minimal text but USE text when needed for clarity (labels, arrows, key words)
- Visual metaphors over abstract art. SHOW the concept, don't decorate it
- Dark backgrounds, clean lines, educational poster aesthetic
- ONE clear concept per image. Never cram multiple ideas
- Visual hierarchy. Most important thing = visually dominant
- Prefer: diagrams, flowcharts, layered scenes, before/after comparisons, metaphor scenes
- ALWAYS use a MALE figure/silhouette (Albert is a man)
- Prompt formula: Start with the CONCEPT then the VISUAL METAPHOR. Include "clean educational illustration" or "infographic style". Always "dark background". Use "labeled" when annotations help

### AVOID
Pure abstract art, too much text, too little context, generic spiritual imagery, multiple concepts per image

### Step 3 - Send each image to Telegram
Number them (1/8), (2/8) etc. Caption = core insight in 1-2 sentences. English only. No fluff.

### Step 4 - Clean up
```bash
rm /tmp/reading-*.png
```

---

## JOB 2: POV MANIFESTATION IMAGES

10 first-person scenes from Albert's desired reality.

### Albert's 5 Goals (map each image to 1-2)

1. Financial freedom - 1M NOK/month through Agentkontoret
2. Total freedom - schedule, location, company
3. Leadership - team of killer closers
4. Certainty - knowing, not hoping
5. Discipline - high ATFT score (Ability To Follow Through)

### CRITICAL - POV MEANS FIRST PERSON

- Camera IS Albert's eyes. He sees THROUGH his eyes
- Do NOT show Albert in the image. No third-person shots
- His hands/arms CAN be partially visible
- Frame it as what HE sees, not a photo OF him

### Prompt Rules for Every POV Image

- Always start with "POV first-person perspective:"
- Describe what Albert SEES, never Albert himself
- Include "Scandinavian male hands" when hands are in frame
- Map each scene to one of the 5 goals
- Include lighting and mood details (golden hour, dawn light, warm cinematic)
- End with "shallow depth of field, editorial quality"

### Example Prompt
"POV first-person perspective: Hands on Ferrari steering wheel driving through Norwegian coastal mountain pass, turquoise fjord visible ahead, warm golden light on leather wheel, exhilaration and control. Scandinavian male hands, shallow depth of field, editorial quality."

### Send each image to Telegram
Number them (1/10), (2/10) etc. Caption = which goal it maps to + short description. English only.

### Clean up
```bash
rm /tmp/pov-*.png
```
