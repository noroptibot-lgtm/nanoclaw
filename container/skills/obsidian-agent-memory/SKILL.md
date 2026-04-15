---
name: obsidian-agent-memory
description: Set up a persistent markdown-based memory system for AI agents using Obsidian. Six folders, templates, CLAUDE.md routing, wiki links. Trigger on /obsidian-memory or when user asks to set up persistent agent memory.
---

# Persistent Agent Memory with Obsidian

Give any AI agent persistent memory across sessions using organized markdown files — no vector DB, no RAG, no cloud. Just folders, wiki links, and a routing file.

## Why Markdown Beats RAG / Vector DB

| RAG / Vector DB | Markdown Memory |
|-----------------|-----------------|
| Complex infrastructure | Just files in a folder |
| Chunks lose context | Full context in every note |
| Can't browse manually | Read and edit anything |
| Expensive at scale | Free, local, zero maintenance |

The agent doesn't need a "memory system." It needs a well-organized filing cabinet with a map taped to the front. `CLAUDE.md` is the map.

## Vault Structure

```
agent-memory/
├── CLAUDE.md              # Routing system (< 200 lines)
├── daily-notes/           # YYYY-MM-DD.md — timeline of your work
├── research/              # Deep dives on topics
├── projects/              # Active project context
├── people/                # Clients, team, contacts
├── decisions/             # Important decisions + reasoning
└── templates/             # Reusable note formats
```

### Folder Purposes

- **daily-notes/** — one file per day, `YYYY-MM-DD.md`. What happened, decisions made, follow-ups.
- **research/** — topic deep dives, lowercase-hyphen filenames (`youtube-algorithm-2025.md`).
- **projects/** — one file per project. Goals, status, key people, next steps.
- **people/** — `first-last.md`. Role, comms preferences, interaction history.
- **decisions/** — `YYYY-MM-DD-decision-title.md`. Context, decision, alternatives, reasoning.
- **templates/** — reusable structures. Daily, person, project, decision, research.

**Naming:** lowercase, hyphens, dates as `YYYY-MM-DD`. Consistency is what makes this scale.

## Templates

### daily-note-template.md
```markdown
# {{date}}

## Summary
<!-- 2-3 sentence overview -->

## What Happened
-

## Decisions Made
-

## Follow-ups Needed
-

## Links
- Projects:
- People:
- Research:
```

### person-template.md
```markdown
# {{name}}

## Role & Context
- **Company**:
- **Role**:
- **Relationship**: client | partner | team | contact
- **First Contact**: {{date}}

## Communication Preferences
- **Preferred Channel**:
- **Tone**: formal | casual | technical
- **Response Time**:

## Interaction History
### {{date}}
-

## Active Items
-
```

### project-template.md
```markdown
# {{project-name}}

## Status: active | paused | complete
## Started: {{date}}
## Last Updated: {{date}}

## Goal

## Current Status

## Key People
- [[person-name]] — role

## Recent Activity
### {{date}}
-

## Decisions
- [[decision-link]]

## Blockers

## Next Steps
```

### decision-template.md
```markdown
# {{date}} — {{decision-title}}

## Context

## Decision

## Alternatives Considered
1. **Option A**: pros / cons
2. **Option B**: pros / cons

## Reasoning

## Impact
- **Projects affected**: [[project-link]]
- **People affected**: [[person-link]]

## Review Date
```

### research-template.md
```markdown
# {{topic}}

## Last Updated: {{date}}
## Status: in-progress | complete | needs-update

## Summary

## Key Findings

## Sources

## How This Applies
- Relevant to: [[project-link]]

## Open Questions
```

## Wiki Links

Double-bracket `[[Sarah Chen]]` creates a link to `people/sarah-chen.md`. Obsidian tracks backlinks automatically — open Sarah's file and see every project, daily note, and decision that mentions her, without ever manually adding backlinks.

**Rule: link generously.** Every person, project, decision, research topic, and date should be a wiki link. The cost of linking is zero. The cost of not linking is lost context.

## CLAUDE.md — The Routing System

Under 200 lines. Pure routing, zero data. The agent reads this first thing in every session.

```markdown
# Agent Memory System — Routing Guide

## CRITICAL RULES
1. ALWAYS check existing notes before creating new ones
2. UPDATE notes when information changes — don't create duplicates
3. LINK related notes using [[wiki links]] every time
4. Use templates from templates/ when creating new notes
5. Keep daily notes in YYYY-MM-DD.md format

## WHERE TO FIND THINGS

### Daily Notes → daily-notes/
- Format: YYYY-MM-DD.md
- Template: templates/daily-note-template.md
- ALWAYS create or update today's daily note when doing work

### Research → research/
- Format: topic-name.md (lowercase, hyphens)
- BEFORE researching: check if a note already exists → update it

### Projects → projects/
- Format: project-name.md
- ALWAYS update the project file after project work

### People → people/
- Format: first-last.md
- ALWAYS update after meaningful interactions

### Decisions → decisions/
- Format: YYYY-MM-DD-decision-title.md
- CREATE for any significant decision

## BEFORE STARTING ANY TASK
1. Read the relevant project file
2. Check recent daily notes (last 3-5 days)
3. Look up people involved
4. Check decisions/ for relevant past decisions
5. Review research/ for background

## LINKING RULES
- Every person mention → [[first-last]]
- Every project mention → [[project-name]]
- Every decision reference → [[YYYY-MM-DD-decision-title]]
- Every research topic → [[topic-name]]
- Every date reference → [[YYYY-MM-DD]]

## FILE NAMING
- All lowercase, hyphens for spaces
- Dates: YYYY-MM-DD
```

## The Three Agent Rules

1. **Check Before Creating** — duplicates split information and break links
2. **Update When Things Change** — stale project status misleads every future session
3. **Link Everything** — unlinked notes are invisible from related files

## Connecting an Agent to the Vault

### Option A — Claude Code (recommended)
```bash
cd ~/Documents/agent-memory
claude
```
Claude Code auto-reads `CLAUDE.md` from the working directory.

### Option B — Cursor / Windsurf / VS Code
File → Open Folder → select your vault. The AI assistant reads/writes files through the editor.

### Option C — Python for Custom Agents

```python
from pathlib import Path
from datetime import datetime, timedelta

class VaultMemory:
    def __init__(self, vault_path):
        self.vault = Path(vault_path)
        self.routing = (self.vault / "CLAUDE.md").read_text()

    def read_note(self, folder, filename):
        path = self.vault / folder / filename
        return path.read_text() if path.exists() else ""

    def write_note(self, folder, filename, content):
        path = self.vault / folder / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def check_exists(self, folder, filename):
        return (self.vault / folder / filename).exists()

    def get_todays_note(self):
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{today}.md"
        content = self.read_note("daily-notes", filename)
        if not content:
            template = self.read_note("templates", "daily-note-template.md")
            content = template.replace("{{date}}", today)
            self.write_note("daily-notes", filename, content)
        return content

    def get_recent_daily_notes(self, days=5):
        notes = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            content = self.read_note("daily-notes", f"{date}.md")
            if content:
                notes.append({"date": date, "content": content})
        return notes

    def search_notes(self, query):
        results = []
        for md in self.vault.rglob("*.md"):
            text = md.read_text()
            if query.lower() in text.lower():
                results.append(str(md.relative_to(self.vault)))
        return results
```

## Seed the Vault (Day 1)

Don't start from empty. Spend 15 minutes creating:

1. **Today's daily note** — what you're working on, active projects
2. **1-2 project files** — your most active work
3. **2-3 person files** — key clients, partners, team members
4. **1 research note** — something you've recently explored
5. **1 decision note** — a recent call worth documenting

All with wiki links to each other from day one.

## The Compound Effect

| Day | Notes | Links | What the agent knows |
|-----|-------|-------|----------------------|
| 1 | ~8 | ~20 | Who you work with, what you're working on |
| 7 | ~40 | ~100 | Your rhythm, recent decisions, active threads |
| 30 | ~150 | ~400 | Every active project, key person, recent decision |
| 60 | ~300 | ~1,200 | Institutional memory — "last time we tried X it didn't work because Y" |
| 90 | ~450 | ~2,500 | More context than a new employee gets in a year |

Context compounds because every new note links to existing notes. The network effect is where the value lives.

## Complete Setup Checklist

- [ ] Vault folder created with six subfolders
- [ ] All five templates written
- [ ] `CLAUDE.md` in vault root, under 200 lines, routing only
- [ ] Seed notes created with real content and wiki links
- [ ] Agent connected (Claude Code, editor, or Python class)
- [ ] Agent reads `CLAUDE.md` as first action every session
- [ ] Commitment to daily updates for first 30 days
