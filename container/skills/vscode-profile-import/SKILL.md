---
name: vscode-profile-import
description: Import a VS Code .code-profile file — extracts settings, keybindings, and extensions and applies them. Use when the user shares a .code-profile file or wants to import VS Code settings from a profile export.
---

Import a `.code-profile` file into VS Code by extracting and applying settings, keybindings, and extensions.

## Steps

### 1. Parse the profile file

```python
import json, os

with open("<path-to-profile>") as f:
    data = json.load(f)

# Extract settings
settings_raw = data.get("settings", "")
settings_obj = json.loads(settings_raw)
actual_settings = json.loads(settings_obj.get("settings", "{}"))

# Extract keybindings
kb_raw = data.get("keybindings", "")
kb_obj = json.loads(kb_raw)
actual_kb = kb_obj.get("keybindings", "")

# Extract extensions
exts = json.loads(data.get("extensions", "[]"))
ext_ids = [e["identifier"]["id"] for e in exts]
```

### 2. Back up and apply settings

```bash
cp ~/Library/Application\ Support/Code/User/settings.json \
   ~/Library/Application\ Support/Code/User/settings.json.backup

# Write extracted settings
python3 -c "
import json
with open('/tmp/extracted_settings.json', 'w') as f:
    json.dump(actual_settings, f, indent=2)
"
cp /tmp/extracted_settings.json ~/Library/Application\ Support/Code/User/settings.json
```

### 3. Apply keybindings

Write `actual_kb` (string) to:
```
~/Library/Application Support/Code/User/keybindings.json
```

### 4. Install extensions

```bash
for ext in "${ext_ids[@]}"; do
    code --install-extension "$ext" --force
done
```

### 5. Reload VS Code

Tell the user to restart VS Code for all changes to take effect.

## Notes

- The `.code-profile` format nests JSON: `data.settings` → parse → `.settings` → parse again to get actual settings object. Same pattern for keybindings.
- Settings backup is always created as `settings.json.backup` before overwriting.
- `code` CLI must be available in PATH (VS Code → Command Palette → "Shell Command: Install 'code' command in PATH").
