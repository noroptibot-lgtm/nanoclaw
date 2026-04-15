---
name: instagram-edit
description: Use when user wants to create an Instagram Reels edit from camera footage on this Mac
---

# Instagram Edit

## Overview

Creates a 25-sec Instagram Reels-ready edit from Sony camera footage using ffmpeg. Output: 9:16, warm color grade, no audio (user adds music in Instagram/CapCut).

## User Preferences

- **Include Alberto in the edit** — ask him which timestamps he appears in the footage, and prioritize those clips
- Output goes to `~/Desktop/`

## Setup

- **Source:** `/Volumes/T7/camera B-roll/` (or directly from SD card)
- **ffmpeg path:** `/Users/albertopdahl/.local/bin/ffmpeg`
- **Output format:** 1080x1920 (9:16), libx264, crf 22, no audio

## Steps

### 1. Get video info

```bash
/Users/albertopdahl/.local/bin/ffmpeg -i "INPUT.MP4" 2>&1 | grep -E "Duration|Video:|fps"
```

### 2. Ask user which timestamps they appear in

Before cutting, ask: *"Hvilke tidspunkter er du med i videoen?"* so those clips get prioritized.

### 3. Build the edit

**Strategy:** 8 clips × 3 sec = ~25 sec total. Distribute across full duration, prioritizing timestamps where Alberto appears.

**Crop 4K 16:9 → 9:16:** `crop=1215:2160:1312:0,scale=1080:1920`

```bash
/Users/albertopdahl/.local/bin/ffmpeg -y \
  -i "INPUT.MP4" \
  -filter_complex "
    [0:v]trim=START1:END1,setpts=PTS-STARTPTS,crop=1215:2160:1312:0,scale=1080:1920,eq=brightness=0.03:contrast=1.08:saturation=1.35[v0];
    [0:v]trim=START2:END2,setpts=PTS-STARTPTS,crop=1215:2160:1312:0,scale=1080:1920,eq=brightness=0.03:contrast=1.08:saturation=1.35[v1];
    ... (repeat for each clip)
    [v0][v1]...[vN]concat=n=N:v=1:a=0[outv]
  " \
  -map "[outv]" \
  -c:v libx264 -preset fast -crf 22 -pix_fmt yuv420p -an \
  "~/Desktop/FILENAME_instagram_edit.mp4"
```

### 4. Verify output

```bash
ls -lh ~/Desktop/*instagram_edit.mp4
```

## Color Grade

Current default (warm, Instagram-friendly):
`eq=brightness=0.03:contrast=1.08:saturation=1.35`

Alternatives:
- Moody/dark: `eq=brightness=-0.02:contrast=1.15:saturation=1.1`
- Fresh/clean: `eq=brightness=0.05:contrast=1.05:saturation=1.2`

## Common Mistakes

| Mistake | Fix |
|--------|-----|
| Not asking about Alberto's timestamps | Always ask before cutting |
| Using wrong crop for non-4K source | Recalculate: `w = height*(9/16)`, `x = (width-w)/2` |
| `split` filter with unconnected output | Remove `split` — use `[0:v]` directly for each trim |
| ffprobe not found | Only ffmpeg is installed, use `ffmpeg -i file 2>&1` for metadata |
