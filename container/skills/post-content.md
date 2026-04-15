---
name: post-content
description: Transcribe, generate captions, and publish a video across all platforms via Dropbox + Late API. Use when you have a video ready to post.
---

# Post Content — End-to-End Video Publishing

Take a ready video → transcribe → generate captions in your voice → revision loop → publish to 6 platforms → archive.

**Your scope:** Video file → captions → publish → move to posted
**NOT your scope:** Scripting (/content-scripter), ideation (/content-ideator), filming (/post-record)

---

## Late API Config (reads from CLAUDE.md)

| Field | Value |
|-------|-------|
| Base URL | `https://getlate.dev/api/v1` |
| API Key | reads from `.env` `LATE_API_KEY` |

### Platform Account IDs (from CLAUDE.md)

| Platform | Account ID |
|----------|-----------|
| instagram | `YOUR_INSTAGRAM_ACCOUNT_ID` |
| tiktok | `YOUR_TIKTOK_ACCOUNT_ID` |
| youtube | `YOUR_YOUTUBE_ACCOUNT_ID` |
| twitter | `YOUR_TWITTER_ACCOUNT_ID` |
| threads | `YOUR_THREADS_ACCOUNT_ID` |
| linkedin | `YOUR_LINKEDIN_ACCOUNT_ID` |

### Dropbox Paths (from CLAUDE.md)

| Folder | Purpose |
|--------|---------|
| `DROPBOX_READY_PATH` | Where finished videos wait to be posted (e.g., `/Content/ready`) |
| `DROPBOX_POSTED_PATH` | Where posted videos get archived (e.g., `/Content/posted`) |

---

## Step 1: Get the Video

**Default: Scan Dropbox ready folder**

```bash
DROPBOX_TOKEN=$(grep DROPBOX_ACCESS_TOKEN .env | cut -d'=' -f2)

curl -s -X POST https://api.dropboxapi.com/2/files/list_folder \
  -H "Authorization: Bearer $DROPBOX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"path": "DROPBOX_READY_PATH", "include_media_info": true}'
```

**For EVERY video in the list, generate a Dropbox preview link and include it in the table.** The user needs clickable URLs to watch each video before choosing.

```bash
DROPBOX_TOKEN=$(grep DROPBOX_ACCESS_TOKEN .env | cut -d'=' -f2)

# For each file, create or fetch a shared link
for FILE in "${FILES[@]}"; do
  PREVIEW_RESPONSE=$(curl -s -X POST https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings \
    -H "Authorization: Bearer $DROPBOX_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"path\": \"DROPBOX_READY_PATH/$FILE\", \"settings\": {\"requested_visibility\": \"public\"}}")

  if echo "$PREVIEW_RESPONSE" | grep -q "shared_link_already_exists"; then
    PREVIEW_RESPONSE=$(curl -s -X POST https://api.dropboxapi.com/2/sharing/list_shared_links \
      -H "Authorization: Bearer $DROPBOX_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"path\": \"DROPBOX_READY_PATH/$FILE\", \"direct_only\": true}")
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
- A Google Drive link -> download with `yt-dlp` (use literal URL in single quotes)
- A video URL -> download with your video downloader skill or `yt-dlp`
- A local file path -> use directly

---

## Step 2: Download from Dropbox to Local Temp

```bash
mkdir -p /tmp/post-content
DROPBOX_TOKEN=$(grep DROPBOX_ACCESS_TOKEN .env | cut -d'=' -f2)

curl -s -X POST https://content.dropboxapi.com/2/files/download \
  -H "Authorization: Bearer $DROPBOX_TOKEN" \
  -H "Dropbox-API-Arg: {\"path\": \"DROPBOX_READY_PATH/FILENAME\"}" \
  -o /tmp/post-content/video.mov
```

---

## Step 3: Extract Audio and Transcribe with Whisper

```bash
ffmpeg -i "/tmp/post-content/video.mov" -ar 16000 -ac 1 -y /tmp/post-content/audio.wav

python3 -c "
import whisper
model = whisper.load_model('medium')
result = model.transcribe('/tmp/post-content/audio.wav')
print(result['text'])
"
```

---

## Step 4: Read Voice Guides

Before writing ANY captions, read your project voice guides:

1. **Caption voice guide** — How you ACTUALLY write captions (path from project CLAUDE.md)
2. **Scripting voice guide** — Your speech patterns and language (path from project CLAUDE.md)

If the project CLAUDE.md doesn't specify voice files, default to:
- Casual, conversational tone
- Short punchy captions (one line)
- No corporate language
- Platform-appropriate energy

---

## Step 5: Generate Captions for ALL Platforms

Using the transcript + caption voice guide, generate captions. Captions are ONE LINE — the video does the talking. See your caption voice guide for exact formats and examples.

**Format your output exactly like this:**

```
---
TRANSCRIPT:
[Full transcript text]

---

INSTAGRAM:
[One-line caption + default hashtags]

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

---

## Caption Rules

- **ONE LINE.** Your best posts are a single punchy sentence. Not a paragraph.
- **The video does the talking** — the caption is a label, not an explanation
- **Default hashtags:** Add your standard hashtags at the end (inline, not on new line). Configure these in your CLAUDE.md.
- **Never:** multi-paragraph, emoji spam, "Follow for more", "Save this", bullet points, corporate language, explaining what the video shows
- **LinkedIn** is the only platform that gets 2-3 lines
- **See your caption voice guide** for the caption formats with real examples

---

## Step 6: Revision Loop

After presenting captions, ask: **"Want me to adjust any of these? Or ready to post?"**

Handle revisions per-platform:
- "Make Twitter spicier" -> rewrite just Twitter
- "LinkedIn is too formal" -> rewrite just LinkedIn
- "Shorter everything" -> trim all

**STOP HERE. Wait for user to approve before publishing.**

---

## Step 7: Create Dropbox Shared Link and Publish via Late API

When the user says "post" or "ready", publish to all platforms using Dropbox direct link + Late API.

### Step 7a: Get Dropbox Direct Link for Full-Quality Video

Reuse the shared link already created in Step 1 (the preview URL). Convert it to a direct download link:

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
  -d '{"path": "DROPBOX_READY_PATH/FILENAME", "direct_only": true}')
SHARE_URL=$(echo "$SHARE_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['links'][0]['url'])")
DIRECT_URL=$(echo "$SHARE_URL" | sed 's/dl=0/dl=1/')
```

### Step 7b: Create Post with Platform-Specific Captions

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

### Late API Quirks (CRITICAL)

- **Batching 5+ platforms in one call can 500** — post each platform INDIVIDUALLY with 2s delay between as fallback. NEVER re-post a platform that already succeeded. Track which platforms are done.
- **Use `raw=1` instead of `dl=1`** for Dropbox direct URLs (Late needs `raw=1`)
- **Large videos may timeout** on the HTTP response but still publish — check for 409 "already posted" before retrying
- **Always use Python `urllib` or `requests` for posting** (shell `curl` mangles `$` in captions)
- **NEVER auto-retry failed posts.** Report failures to the user and wait for explicit confirmation before retrying. Duplicate posts = ban risk.

### Step 7c: Report Results

After posting, show the user:
- Which platforms succeeded/failed
- Links to each published post (from `platformPostUrl` in response)
- Any errors to retry

Check status after a few seconds if any platforms are still "pending":

```bash
curl -s -H "Authorization: Bearer $LATE_API_KEY" "https://getlate.dev/api/v1/posts/POST_ID"
```

**IMPORTANT:** Always confirm with the user before posting. Never auto-post without explicit approval.

---

## Step 8: Move File to Posted Folder

After successful posting, move the video from ready to posted:

```bash
DROPBOX_TOKEN=$(grep DROPBOX_ACCESS_TOKEN .env | cut -d'=' -f2)

curl -s -X POST https://api.dropboxapi.com/2/files/move_v2 \
  -H "Authorization: Bearer $DROPBOX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"from_path": "DROPBOX_READY_PATH/FILENAME", "to_path": "DROPBOX_POSTED_PATH/FILENAME"}'
```

---

## Cleanup

When done, clean up temp files:

```bash
rm -rf /tmp/post-content
```

---

## Voice & Tone

The skill does NOT define a specific voice. Each project's CLAUDE.md specifies:
- Caption style and patterns
- Hashtag defaults
- Platform-specific language rules
- Winner/loser caption examples

If no voice guide exists in the project, default to:
- Casual, conversational tone
- One-line captions (the video does the talking)
- No emoji spam, no corporate language
- Platform-appropriate energy

---

## Part of the Content Engine

```
/content-scripter → (film) → /post-content (this skill)
```

- **`/content-scripter`** — writes the script and filming card
- **(film)** — you record the video
- **`/post-content`** (this skill) — transcribe, caption, publish, archive
