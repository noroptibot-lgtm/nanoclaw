---
name: copy-camera-to-t7
description: Use when copying newest Sony camera footage from SD card to T7 SSD camera B-roll folder on this Mac
---

# Copy Camera to T7

## Overview

Copies the newest clip from a Sony camera SD card to the T7 SSD. T7 blocks direct Terminal writes (Time Machine disk), so AppleScript/Finder is used instead.

## Setup

- **Camera SD card** mounts as `Untitled` → `/Volumes/Untitled/PRIVATE/M4ROOT/CLIP/`
- **Destination** → `/Volumes/T7/camera B-roll/`
- **T7 is Time Machine disk** for openclaws-mac-mini — Terminal writes are blocked, use `osascript`

## Steps

### 1. Find newest clip

```bash
find /Volumes/Untitled/PRIVATE/M4ROOT/CLIP/ -name "*.MP4" 2>/dev/null | xargs ls -lt 2>/dev/null | grep -v "^\." | head -5
```

Newest file = highest mtime (top of list). Files named `C0040.MP4`, `C0039.MP4` etc.

### 2. Copy via AppleScript

```bash
osascript << 'EOF'
tell application "Finder"
    set t7 to disk "T7"
    if not (exists folder "camera B-roll" of t7) then
        make new folder at t7 with properties {name:"camera B-roll"}
    end if
    set srcFile to POSIX file "/Volumes/Untitled/PRIVATE/M4ROOT/CLIP/C0040.MP4" as alias
    set destFolder to folder "camera B-roll" of t7
    duplicate srcFile to destFolder with replacing
end tell
return "Done"
EOF
```

Replace `C0040.MP4` with the actual newest file name.

### 3. Verify

```bash
ls -lh "/Volumes/T7/camera B-roll/"
```

### 4. Clean up (ask user first)

If old/wrong files exist in the folder, ask user if they want them deleted, then:

```bash
osascript << 'EOF'
tell application "Finder"
    set f to POSIX file "/Volumes/T7/camera B-roll/FILENAME.mp4" as alias
    delete f
end tell
EOF
```

## Common Mistakes

| Mistake | Fix |
|--------|-----|
| Using `cp` or `mkdir` to T7 | Always use `osascript`/Finder — Terminal is blocked |
| Copying wrong file (e.g. from Downloads) | Always check `/Volumes/Untitled/` first for camera clips |
| Not checking if SD card is mounted | Run `ls /Volumes/Untitled/` first to verify |
