# Miro Visual Board Builder

Turn any content into a structured Miro storyboard — YouTube videos, newsletters, podcasts, articles, or concepts.

## Trigger

Use this skill when the user wants to:
- Create a Miro board from a YouTube video URL
- Visualize a newsletter, article, or concept as a Miro board
- Build a storyboard for a YouTube explainer video
- Convert any content into visual Miro frames

---

## How to invoke (by input type)

### 1. YouTube video URL
```
User: "Make a Miro board from this video: https://youtube.com/watch?v=..."
```
Steps:
1. Run `yt-dlp --write-auto-sub --sub-lang en --skip-download --output "/tmp/yt_%(id)s" "URL"` to download the transcript `.vtt` file
2. Strip VTT timestamps: `sed 's/<[^>]*>//g' file.vtt | grep -v '^[0-9]' | grep -v '^$' | sort -u`
3. Parse cleaned transcript into 6-10 logical sections (topic shifts)
4. For each section: extract headline, 2-3 key points, any stats or quotes
5. Build Miro board — one frame per section

### 2. Newsletter / article text
```
User: "Make a Miro board from this newsletter: [pastes text]"
User: "Build a Miro board from this URL: https://..."
```
Steps:
1. If URL: fetch with `curl -s URL | sed 's/<[^>]*>//g'` or use WebFetch tool
2. Parse text into 6-10 sections by topic or paragraph structure
3. Build Miro board — one frame per section

### 3. Concept / idea
```
User: "Make a Miro board explaining [concept]"
```
Steps:
1. Plan 6-8 frames covering: intro → problem → solution → steps → outcome
2. Generate content for each frame
3. Build Miro board

---

## Board build process

### Step 1: Plan frames
Before calling the API, plan all frames:
```
Frame 1: [title] — [headline] — [3 bullet points]
Frame 2: ...
```

### Step 2: Create board
```bash
source ~/.config/meta-api.env
BOARD=$(curl -s -X POST https://api.miro.com/v2/boards \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "BOARD_TITLE", "description": "SOURCE_DESCRIPTION"}')
BOARD_ID=$(echo $BOARD | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
```

### Step 3: Create frames (one per scene)
```bash
curl -s -X POST "https://api.miro.com/v2/boards/$BOARD_ID/frames" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"title": "FRAME_TITLE", "format": "custom", "type": "freeform"},
    "style": {"fillColor": "#09090b"},
    "geometry": {"width": 1080, "height": 1920},
    "position": {"x": SCENE_X, "y": 0}
  }'
```

X positions: Scene 1 = 0, Scene 2 = 1300, Scene 3 = 2600, etc.

### Step 4: Add text and shapes

**Headline text:**
```bash
curl -s -X POST "https://api.miro.com/v2/boards/$BOARD_ID/texts" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"content": "<p><strong>HEADLINE</strong></p>"},
    "style": {"color": "#ffffff", "fontSize": "36", "textAlign": "left"},
    "geometry": {"width": 960},
    "position": {"x": SCENE_X + 60, "y": 120}
  }'
```

**Key point shapes (rectangles):**
```bash
curl -s -X POST "https://api.miro.com/v2/boards/$BOARD_ID/shapes" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"shape": "rectangle", "content": "<p>KEY POINT TEXT</p>"},
    "style": {"fillColor": "#1e1e2e", "borderColor": "#6366f1", "borderWidth": "2", "color": "#e2e8f0", "fontSize": "20"},
    "geometry": {"width": 900, "height": 100},
    "position": {"x": SCENE_X + 90, "y": Y_POSITION}
  }'
```

**CRITICAL: No emojis in bash JSON strings** — they corrupt the payload. Use plain text only.

### Step 5: Add connectors between flow shapes
```bash
curl -s -X POST "https://api.miro.com/v2/boards/$BOARD_ID/connectors" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "startItem": {"id": "SHAPE_ID_1"},
    "endItem": {"id": "SHAPE_ID_2"},
    "style": {"strokeColor": "#6366f1", "strokeWidth": "2"}
  }'
```

---

## Visual design system

| Element | Value |
|---------|-------|
| Background | `#09090b` |
| Accent | `#6366f1` (indigo) |
| Success | `#34d399` (green) |
| Warning | `#f87171` (red) |
| Card bg | `#1e1e2e` |
| Text | `#e2e8f0` |
| Muted text | `#94a3b8` |

**Frame layout (portrait, per scene):**
- Y=120: Scene number tag (small rectangle, accent color)
- Y=200: Main headline (large text, white)
- Y=400: 3-4 key point shapes, stacked 120px apart
- Y=1600: Bottom stat or CTA (large accent rectangle)

---

## Credentials

Stored in `~/.config/meta-api.env`:
```
MIRO_ACCESS_TOKEN=...
```

---

## Improvements TODO

- [ ] Add real connectors/arrows between flow boxes within a scene
- [ ] Image support: fetch relevant images from Unsplash or use SVG icons
- [ ] Scene number badges (small colored tag in top-left of each frame)
- [ ] Landscape format (16:9) for presentation boards
- [ ] Group elements inside frames (Miro parent/child API)
- [ ] Sticky notes for annotations
- [ ] Export board as PDF after creation
- [ ] Better transcript parsing: detect speaker changes, chapter markers

---

## API reference

```bash
POST https://api.miro.com/v2/boards               # Create board
POST https://api.miro.com/v2/boards/{id}/frames    # Create frame
POST https://api.miro.com/v2/boards/{id}/texts     # Create text widget
POST https://api.miro.com/v2/boards/{id}/shapes    # Create shape
POST https://api.miro.com/v2/boards/{id}/connectors # Create arrow/connector
```

Shape types: `rectangle`, `circle`, `triangle`, `rhombus`, `parallelogram`, `trapezoid`, `pentagon`, `hexagon`, `star`, `cross`, `cloud`, `arrow`, `callout`, `cylinder`
