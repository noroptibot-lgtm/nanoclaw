# Post Content

Transcribe, generate captions, and publish a video across all platforms via Dropbox + Late API.

## Instructions

### Step 1: Get the video

**Default: Scan Dropbox `/Content/ready/` folder**

```bash
DROPBOX_TOKEN=$(grep DROPBOX_ACCESS_TOKEN .env | cut -d'=' -f2)

curl -s -X POST https://api.dropboxapi.com/2/files/list_folder \
  -H "Authorization: Bearer $DROPBOX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"path": "/Content/ready", "include_media_info": true}'
```

**For EVERY video in the list, generate a Dropbox preview link and include it in the table.** The user needs clickable URLs to watch each video before choosing.

```bash
DROPBOX_TOKEN=$(grep DROPBOX_ACCESS_TOKEN .env | cut -d'=' -f2)

# For each file, create or fetch a shared link
for FILE in "${FILES[@]}"; do
  PREVIEW_RESPONSE=$(curl -s -X POST https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings \
    -H "Authorization: Bearer $DROPBOX_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"path\": \"/Content/ready/$FILE\", \"settings\": {\"requested_visibility\": \"public\"}}")

  if echo "$PREVIEW_RESPONSE" | grep -q "shared_link_already_exists"; then
    PREVIEW_RESPONSE=$(curl -s -X POST https://api.dropboxapi.com/2/sharing/list_shared_links \
      -H "Authorization: Bearer $DROPBOX_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"path\": \"/Content/ready/$FILE\", \"direct_only\": true}")
    PREVIEW_URL=$(echo "$PREVIEW_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['links'][0]['url'])")
  else
    PREVIEW_URL=$(echo "$PREVIEW_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['url'])")
  fi
  echo "$FILE | $PREVIEW_URL"
done
```

**Display the queue as a table with columns: #, Filename, Size, Preview Link (clickable URL).**

Ask: **"Which video do you want to post? Click a link to preview, then give me the number."**

After the user picks, confirm and save the PREVIEW_URL for that file (reused in Step 7a). Only proceed to Step 2 after confirmation.

**Alternative sources (if user provides directly):**
- A Google Drive link → download with `yt-dlp` (use literal URL in single quotes)
- A video URL → download with `python3 ~/.claude/skills/video-downloader/scripts/download_video.py "URL" -o /tmp/post-content`
- A local file path → use directly

### Step 2: Download from Dropbox to local temp

```bash
mkdir -p /tmp/post-content
DROPBOX_TOKEN=$(grep DROPBOX_ACCESS_TOKEN .env | cut -d'=' -f2)

curl -s -X POST https://content.dropboxapi.com/2/files/download \
  -H "Authorization: Bearer $DROPBOX_TOKEN" \
  -H "Dropbox-API-Arg: {\"path\": \"/Content/ready/FILENAME\"}" \
  -o /tmp/post-content/video.mov
```

### Step 3: Extract audio and transcribe

```bash
ffmpeg -i "/tmp/post-content/video.mov" -ar 16000 -ac 1 -y /tmp/post-content/audio.wav

python3 -c "
import whisper
model = whisper.load_model('medium')
result = model.transcribe('/tmp/post-content/audio.wav')
print(result['text'])
"
```

### Step 4: Read voice guides and generate captions

Before writing ANY captions, read:
1. `reference/caption-voice.md` — How Noe ACTUALLY writes captions (data from 425+ posts)
2. `reference/scripting-voice.md` — Noe's speech patterns and language

### Step 5: Generate captions for all platforms

Using the transcript + caption voice guide, generate captions. Noe's captions are ONE LINE — the video does the talking. See `reference/caption-voice.md` for exact formats and examples.

**Format your output exactly like this:**

```
---
TRANSCRIPT:
[Full transcript text]

---

INSTAGRAM:
[One-line caption + #ai #claude]

TIKTOK:
[Same as IG or shorter]

YOUTUBE SHORTS:
[Title under 100 chars]

TWITTER/X:
[Same one-liner, no hashtags]

THREADS:
[Same energy, slightly more conversational]

LINKEDIN:
[2-3 lines max. Professional angle. Still tight.]
```

### Caption Rules

- **ONE LINE.** Noe's best posts are a single punchy sentence. Not a paragraph.
- **The video does the talking** — the caption is a label, not an explanation
- **Default hashtags:** `#ai #claude` at the end (inline, not on new line)
- **Never:** multi-paragraph, emoji spam, "Follow for more", "Save this", bullet points, corporate language, explaining what the video shows
- **LinkedIn** is the only platform that gets 2-3 lines
- **See `reference/caption-voice.md`** for the 5 caption formats with real examples

### Step 6: Revision loop

After presenting captions, ask: **"Want me to adjust any of these? Or ready to post?"**

Handle revisions per-platform:
- "Make Twitter spicier" → rewrite just Twitter
- "LinkedIn is too formal" → rewrite just LinkedIn
- "Shorter everything" → trim all

### Step 7: Create Dropbox shared link and publish via Late API

When the user says "post" or "ready", publish to all platforms using Dropbox direct link + Late API.

**Late API Config:**
- Base URL: `https://getlate.dev/api/v1`
- Auth: `Authorization: Bearer $LATE_API_KEY` (from `.env`)

**Account IDs (all connected to @your-handle):**

| Platform | Account ID |
|----------|-----------|
| instagram | `YOUR_INSTAGRAM_ACCOUNT_ID` |
| tiktok | `YOUR_TIKTOK_ACCOUNT_ID` |
| youtube | `YOUR_YOUTUBE_ACCOUNT_ID` |
| twitter | `YOUR_TWITTER_ACCOUNT_ID` |
| threads | `YOUR_THREADS_ACCOUNT_ID` |
| linkedin | `YOUR_LINKEDIN_ACCOUNT_ID` |

**Step 7a: Get Dropbox direct link for full-quality video**

Reuse the shared link already created in Step 1 (the preview URL). Just convert it to a direct download link:

```bash
# Convert the preview URL from Step 1 to a direct download link
DIRECT_URL=$(echo "$PREVIEW_URL" | sed 's/dl=0/dl=1/')
```

If the preview URL variable is no longer available, re-fetch it:

```bash
DROPBOX_TOKEN=$(grep DROPBOX_ACCESS_TOKEN .env | cut -d'=' -f2)

SHARE_RESPONSE=$(curl -s -X POST https://api.dropboxapi.com/2/sharing/list_shared_links \
  -H "Authorization: Bearer $DROPBOX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"path": "/Content/ready/FILENAME", "direct_only": true}')
SHARE_URL=$(echo "$SHARE_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['links'][0]['url'])")
DIRECT_URL=$(echo "$SHARE_URL" | sed 's/dl=0/dl=1/')
```

**Step 7b: Create post with platform-specific captions**

```bash
LATE_API_KEY=$(grep LATE_API_KEY .env | cut -d'=' -f2)

curl -s -X POST "https://getlate.dev/api/v1/posts" \
  -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "publishNow": true,
    "mediaItems": [{"url": "DROPBOX_DIRECT_URL", "type": "video"}],
    "platforms": [
      {"platform": "instagram", "accountId": "YOUR_INSTAGRAM_ACCOUNT_ID", "customContent": "INSTAGRAM_CAPTION"},
      {"platform": "tiktok", "accountId": "YOUR_TIKTOK_ACCOUNT_ID", "customContent": "TIKTOK_CAPTION"},
      {"platform": "youtube", "accountId": "YOUR_YOUTUBE_ACCOUNT_ID", "customContent": "YOUTUBE_TITLE"},
      {"platform": "twitter", "accountId": "YOUR_TWITTER_ACCOUNT_ID", "customContent": "TWITTER_CAPTION"},
      {"platform": "threads", "accountId": "YOUR_THREADS_ACCOUNT_ID", "customContent": "THREADS_CAPTION"},
      {"platform": "linkedin", "accountId": "YOUR_LINKEDIN_ACCOUNT_ID", "customContent": "LINKEDIN_CAPTION"}
    ]
  }'
```

**NOTE:** Facebook excluded — Page connection has content flagging issues. Add back when resolved.

**CRITICAL: Post all platforms in ONE call if possible. If the multi-platform call 500s, post each platform INDIVIDUALLY — but NEVER re-post a platform that already succeeded. Track which platforms are done.**

**Late API quirks:**
- Batching 5+ platforms in one call can 500 — post individually with 2s delay between as fallback
- Use `raw=1` instead of `dl=1` for Dropbox direct URLs (Late needs `raw=1`)
- Large videos may timeout on the HTTP response but still publish — check for 409 "already posted" before retrying
- Always use Python `urllib` or `requests` for posting (shell `curl` mangles `$` in captions)

**Step 7c: Report results**

After posting, show the user:
- Which platforms succeeded/failed
- Links to each published post (from `platformPostUrl` in response)
- Any errors to retry

Check status after a few seconds if any platforms are still "pending":
```bash
curl -s -H "Authorization: Bearer $LATE_API_KEY" "https://getlate.dev/api/v1/posts/POST_ID"
```

**IMPORTANT:** Always confirm with the user before posting. Never auto-post without explicit approval.

### Step 8: Move file to /posted/

After successful posting, move the video from `ready/` to `posted/`:

```bash
DROPBOX_TOKEN=$(grep DROPBOX_ACCESS_TOKEN .env | cut -d'=' -f2)

curl -s -X POST https://api.dropboxapi.com/2/files/move_v2 \
  -H "Authorization: Bearer $DROPBOX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"from_path": "/Content/ready/FILENAME", "to_path": "/Content/posted/FILENAME"}'
```

### Cleanup

When done, clean up temp files:
```bash
rm -rf /tmp/post-content
```

$ARGUMENTS