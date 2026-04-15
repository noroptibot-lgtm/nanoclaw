# Upload to Google Drive B-roll

## Overview

Uploads files from `/Volumes/T7/camera B-roll/` (or Desktop) to the **B-roll** folder in Google Drive (`albert@noropti.com`).

## Key Details

- **Google Drive account:** albert@noropti.com
- **Target folder:** B-roll (Min disk)
- **Folder ID:** `1zopRor4umIWBtTOkiYBnfimoHkIey9Oc`
- **Drive URL:** `https://drive.google.com/drive/folders/1zopRor4umIWBtTOkiYBnfimoHkIey9Oc`
- **Playwright allowed root:** `/Applications/Claude Code/` — files must be copied here before upload

## Steps

### 1. Copy files to allowed root (if not already there)

```bash
cp /path/to/file.mp4 "/Applications/Claude Code/"
```

### 2. Navigate to B-roll folder in Drive

```js
await page.goto('https://drive.google.com/drive/folders/1zopRor4umIWBtTOkiYBnfimoHkIey9Oc');
```

### 3. Click Ny → Filopplasting

Click the "Ny" button (ref changes per session), then click "Filopplasting".

### 4. Upload files via file chooser

```js
await fileChooser.setFiles(["/Applications/Claude Code/file1.mp4", ...]);
```

### 5. Wait for upload to complete

Take screenshot to verify green checkmarks on all files.

### 6. Clean up temp files

```bash
rm "/Applications/Claude Code/"*.mp4
```

## Common Mistakes

| Mistake | Fix |
|--------|-----|
| File outside allowed roots | Copy to `/Applications/Claude Code/` first |
| Double-clicking folder (opens new tab, loses page) | Always navigate via direct URL with folder ID |
| Page goes blank after interaction | Re-navigate to folder URL directly |
| Ref IDs change between sessions | Always snapshot before clicking |
