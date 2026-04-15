---
name: obsidian
description: >
  Manage Obsidian vaults - create, search, and organize markdown notes, daily notes,
  tags, and wikilink backlinks. Trigger keywords: notes, obsidian, vault, daily note,
  knowledge base, second brain, zettelkasten, PKM, note-taking.
---

# Obsidian Vault Manager

Manage Obsidian vaults as plain markdown files using `scripts/obsidian.py` (Python 3, no dependencies).

## Setup

The script auto-detects your vault from `~/Library/Application Support/obsidian/obsidian.json`.

Override with:
- `--vault <path-or-name>` flag on any command
- `OBSIDIAN_VAULT` environment variable

Priority: `--vault` flag > `OBSIDIAN_VAULT` env > open vault from obsidian.json > first vault.

## Quick Reference

All commands below use the script at the path relative to this skill:

```
SCRIPT="$HOME/.claude/skills/obsidian/scripts/obsidian.py"
```

### Discover vaults

```bash
python3 "$SCRIPT" vaults
```

### List notes

```bash
python3 "$SCRIPT" notes
python3 "$SCRIPT" notes --search "meeting"
python3 "$SCRIPT" --vault "Work" notes
```

### Read a note

```bash
python3 "$SCRIPT" read "Projects/my-project.md"
python3 "$SCRIPT" read "Ideas/cool-idea"       # .md auto-added
```

### Create a note

```bash
python3 "$SCRIPT" create "Projects/new-idea" "Some initial content"
python3 "$SCRIPT" create "Projects/tagged" "Content here" --tags project active
python3 "$SCRIPT" create "Inbox/quick" --force   # overwrite if exists
```

Creates parent directories automatically. Adds `.md` extension if missing.

### Daily note

```bash
python3 "$SCRIPT" daily
```

Creates `Daily Notes/YYYY-MM-DD.md` with frontmatter and template. If it already exists, prints the contents.

### Full-text search

```bash
python3 "$SCRIPT" search "kubernetes"
python3 "$SCRIPT" search "TODO"
```

Case-insensitive. Shows `file:line: matching text` for every hit.

### List all tags

```bash
python3 "$SCRIPT" tags
```

Finds both `#inline-tags` and YAML frontmatter `tags:` arrays. Shows counts.

### Backlinks (wikilinks)

```bash
python3 "$SCRIPT" links "Projects/my-project"
```

Shows which notes link to the target via `[[wikilinks]]`.

### Recently modified

```bash
python3 "$SCRIPT" recent
python3 "$SCRIPT" recent --limit 20
```

## Common Workflows

### Morning routine
```bash
# Create today's daily note and see recent activity
python3 "$SCRIPT" daily
python3 "$SCRIPT" recent
```

### Research a topic
```bash
# Search for content, then check what links to a key note
python3 "$SCRIPT" search "machine learning"
python3 "$SCRIPT" links "Topics/Machine Learning"
```

### Create a linked note
```bash
# Create a new note that you'll reference from others via [[wikilinks]]
python3 "$SCRIPT" create "Concepts/New Concept" "Description of the concept.

## Related
- [[Other Note]]
- [[Another Note]]
" --tags concept draft
```

### Audit tags
```bash
python3 "$SCRIPT" tags
python3 "$SCRIPT" search "#abandoned"
```

## Notes

- Vault = a normal folder on disk. All notes are plain `.md` files.
- Hidden directories (`.obsidian/`, etc.) are automatically skipped.
- The script never modifies existing notes unless you use `create --force`.
- Obsidian will pick up any file changes automatically when it's running.
