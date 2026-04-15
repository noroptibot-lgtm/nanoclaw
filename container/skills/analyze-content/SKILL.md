---
name: analyze-content
description: Analyze content in bulk across Instagram, TikTok, and YouTube — download, transcribe (Whisper), extract hooks (Claude/GPT), visual analysis (Gemini), generate embeddings, and write to Supabase + Airtable. Use when backfilling content analysis or processing new unanalyzed videos.
---

# Analyze Content

Bulk-analyze short-form videos across all platforms: download video, transcribe with Whisper, extract hooks/topics, visual analysis via Gemini, generate embeddings, and update Supabase + Airtable.

**Supports:** Instagram, TikTok, YouTube

---

## Prerequisites

API keys must be set in `~/Noe-Work/YourChannelAI/.env` (or as environment variables):

| Key | Required | Used For |
|-----|----------|----------|
| `OPENAI_API_KEY` | Yes | Whisper transcription + embeddings |
| `GEMINI_API_KEY` | Yes | Visual analysis (text hook, visual format, audio hook) |
| `ANTHROPIC_API_KEY` | Optional | Hook extraction (falls back to OpenAI GPT-4o-mini) |
| `META_GRAPH_API_TOKEN` | IG only | Instagram video download via Meta Graph API |

**Tools:** `yt-dlp` and `ffmpeg` must be installed (used for TikTok/YouTube download + audio extraction).

**Cost:** ~$0.004/video ($2.75 total for ~700 videos)

---

## Platform Config

| Platform | Handle | Download Method | Airtable Table | ID Field |
|----------|--------|----------------|----------------|----------|
| Instagram | `your-handle` | Meta Graph API | `tblXXXXXXXXXXXXX` | IG Media ID |
| TikTok | `your-handle` | yt-dlp | `tblXXXXXXXXXXXXX` | Content ID |
| YouTube | `YourChannel` | yt-dlp | `tblXXXXXXXXXXXXX` | Content ID |

All platforms write to the **same Supabase `content` table** (project `dtxosfdjdozapwbpubom`), differentiated by `platform` column.

---

## When Invoked

### Step 1: Check API Keys

Run a quick check that required keys are available:

```bash
python3 -c "
import os
env_path = os.path.expanduser('~/Noe-Work/YourChannelAI/.env')
keys = {}
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                keys[k.strip()] = bool(v.strip())
for k in ['OPENAI_API_KEY', 'GEMINI_API_KEY', 'ANTHROPIC_API_KEY', 'META_GRAPH_API_TOKEN']:
    status = 'SET' if keys.get(k) or os.environ.get(k) else 'MISSING'
    print(f'{k}: {status}')
"
```

If OPENAI_API_KEY or GEMINI_API_KEY is MISSING, stop and tell the user to add them to `~/Noe-Work/YourChannelAI/.env`.

### Step 2: Query Supabase for Unanalyzed Videos

Determine which platform(s) to analyze. Default: `tiktok` + `youtube` (IG is already done).

Use the Supabase MCP (`execute_sql`, project `dtxosfdjdozapwbpubom`):

```sql
SELECT platform, COUNT(*) as unanalyzed
FROM content
WHERE handle IN ('your-handle', 'your-handle', 'YourChannel')
  AND is_analyzed IS NOT true
GROUP BY platform
```

Tell the user the counts per platform.

If user specifies a platform (e.g., `/analyze-content tiktok`), only process that one.
If user specifies a number (e.g., `/analyze-content 50`), use that as the LIMIT per platform.

### Step 3: Process Videos with Sub-Agents

Spawn **5 sub-agents in parallel**, each processing 1 video. Each sub-agent:

#### 3a. Run the Analysis Script

```bash
python3 ~/.claude/skills/analyze-content/scripts/analyze_reel.py \
  --url "VIDEO_URL" \
  --media-id "CONTENT_ID" \
  --caption "CAPTION_TEXT" \
  --platform "PLATFORM"
```

The script outputs JSON to stdout with all analysis fields.

#### 3b. Update Supabase

Parse the script's JSON output. Update the `content` table:

```sql
UPDATE content SET
  transcript = 'TRANSCRIPT',
  spoken_hook = 'SPOKEN_HOOK',
  spoken_hook_framework = 'HOOK_FRAMEWORK',
  spoken_hook_structure = 'HOOK_STRUCTURE',
  topic = 'TOPIC',
  topic_summary = 'TOPIC_SUMMARY',
  content_structure = 'CONTENT_STRUCTURE',
  content_type = 'CONTENT_TYPE',
  call_to_action = 'CALL_TO_ACTION',
  text_hook = 'TEXT_HOOK',
  visual_hook_graphic = 'VISUAL_HOOK_GRAPHIC',
  visual_hook_movement = 'VISUAL_HOOK_MOVEMENT',
  visual_hook_layout = 'VISUAL_HOOK_LAYOUT',
  visual_format = 'VISUAL_FORMAT',
  audio_hook_structure = 'AUDIO_HOOK_STRUCTURE',
  audio_hook_specifics = 'AUDIO_HOOK_SPECIFICS',
  duration = DURATION,
  topic_summary_embedding = 'EMBEDDING_ARRAY',
  is_analyzed = true,
  analyzed_at = now()
WHERE id = 'CONTENT_ID'
```

**IMPORTANT:** Escape single quotes in all text fields using `''` (double single-quote) for SQL safety.

For the embedding, format as: `'[0.123, -0.456, ...]'::vector`

#### 3c. Update Airtable

Use the Airtable MCP to update the correct platform table.

- **Base:** `appXXXXXXXXXXXXX`
- **Instagram table:** `tblXXXXXXXXXXXXX` (match on `IG Media ID`)
- **TikTok table:** `tblXXXXXXXXXXXXX` (match on `Content ID`)
- **YouTube table:** `tblXXXXXXXXXXXXX` (match on `Content ID`)

Use `search_records` to find the record by ID, then `update_records` with these fields:

| Airtable Field | Source |
|----------------|--------|
| Transcript | transcript |
| Spoken Hook | spoken_hook |
| Hook Framework | hook_framework |
| Hook Structure | hook_structure |
| Content Type | content_type |
| Topic | topic |
| Topic Summary | topic_summary |
| Content Structure | content_structure |
| Call to Action | call_to_action |
| Visual Hook | visual_hook_movement |
| Visual Layout | visual_hook_layout |
| Visual Graphic | visual_hook_graphic |
| Text Hook | text_hook |
| Audio Hook | audio_hook_structure |
| Duration | duration |
| Analyzed | true |

#### 3d. Handle Failures

If the script returns `{"success": false, "error": "..."}`:
- Log the error
- Continue to next video (don't stop the batch)
- Include in final report

### Step 4: Report Results

After all sub-agents complete:

```
## Analysis Complete

**Platforms:** [list]
**Processed:** X/Y videos
**Succeeded:** X
**Failed:** Y (list failures with errors)
**Remaining:** Z unanalyzed videos

**Cost estimate for this batch:** ~$X.XX
```

---

## Sub-Agent Prompt Template

When spawning each sub-agent, use this prompt:

```
Analyze this {platform} video and update Supabase + Airtable with results.

Video: {url}
Content ID: {content_id}
Caption: {caption}
Platform: {platform}

Steps:
1. Run: python3 ~/.claude/skills/analyze-content/scripts/analyze_reel.py --url "{url}" --media-id "{content_id}" --caption "{caption}" --platform "{platform}"
2. Parse the JSON output
3. If success=true: Update Supabase content table (project dtxosfdjdozapwbpubom) with all analysis fields via execute_sql
4. If success=true: Find and update the Airtable record in base appXXXXXXXXXXXXX, table {table_id} (match on {id_field} = {content_id})
5. Report: success/failure + any errors

For the Supabase UPDATE, escape single quotes in text with ''. Format embedding as '[...]'::vector.
For Airtable, use search_records to find the record, then update_records.
```

---

## Batch Script (Walk-Away Mode)

For large backfills, use the batch script directly:

```bash
# Analyze all TikTok + YouTube (default)
python3 ~/.claude/skills/analyze-content/scripts/batch_analyze.py

# Just TikTok
python3 ~/.claude/skills/analyze-content/scripts/batch_analyze.py --platform tiktok --threads 10

# Just YouTube
python3 ~/.claude/skills/analyze-content/scripts/batch_analyze.py --platform youtube --limit 373

# Just Instagram (new unanalyzed)
python3 ~/.claude/skills/analyze-content/scripts/batch_analyze.py --platform instagram
```

---

## Options

| Arg | Example | What |
|-----|---------|------|
| (platform) | `/analyze-content tiktok` | Process only one platform |
| (number) | `/analyze-content 50` | Process N videos per platform instead of default 20 |
| `--skip-visual` | Pass to script | Skip Gemini visual analysis |
| `--oldest` | Query with `ORDER BY post_date ASC` | Process oldest first |

---

## Supabase Column → Airtable Field Map

| Supabase Column | Airtable Field |
|-----------------|----------------|
| transcript | Transcript |
| spoken_hook | Spoken Hook |
| spoken_hook_framework | Hook Framework |
| spoken_hook_structure | Hook Structure |
| content_type | Content Type |
| topic | Topic |
| topic_summary | Topic Summary |
| content_structure | Content Structure |
| call_to_action | Call to Action |
| text_hook | Text Hook |
| visual_hook_graphic | Visual Graphic |
| visual_hook_movement | Visual Hook |
| visual_hook_layout | Visual Layout |
| visual_format | (no direct field — use Visual Layout) |
| audio_hook_structure | Audio Hook |
| audio_hook_specifics | (no direct field) |
| duration | Duration |
| is_analyzed | Analyzed |
