# Bilag from Downloads

Automatically process new PDF/image files from ~/Downloads as bilag.

## How it works

1. Scan ~/Downloads for files newer than the last check (tracked in ~/.claude-remote/bilag-downloads-processed.txt)
2. For each new PDF/image that looks like a receipt/invoice/bilag:
   - Read the file to identify: leverandør, dato, beløp, hva det gjelder
   - Determine the correct month folder in Google Drive:
     - Des 2025: 1xg7T9ExRz8sN8sDqqMbpxkv1TRG-V8n1
     - Jan 2026: 1OhoCUFtoW9IvhVBtowWLLEKX7UBN_kPN
     - Feb 2026: 1w-I8SQ0pldVJdiyY5MZjHo2FlxSr-GcK
   - Upload: `source ~/.env && export GOG_KEYRING_PASSWORD && gog drive upload -a albert@noropti.com --parent <folder_id> "<file>" -j`
   - Find matching row in Airtable (appBqktdVLR6Ae7PH / tblvE52FHPYRZLSNZ) by vendor + amount + date
   - Update: Status=OK, add Bilagsfil attachment (Drive URL), update Bilagsdokument text
   - Remove from Manglende bilag (tblKma7Zs5lKzvAlF) if present
3. Mark file as processed
4. If new bilag found: send Telegram summary to 1973890232

## Run manually
Just ask: "Check Downloads for new bilag"

## State file
~/.claude-remote/bilag-downloads-processed.txt — list of already-processed filenames
