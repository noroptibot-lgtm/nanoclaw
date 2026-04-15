---
name: wikipedia
description: Search and read Wikipedia articles — encyclopedia, knowledge, research, facts, reference. Access the world's encyclopedia for articles, summaries, and information lookup.
---

# Wikipedia Skill

Search and read Wikipedia, the free encyclopedia. Look up articles, get summaries, explore references, and discover knowledge on any topic.

## Setup

No setup needed. Uses the free MediaWiki API with no authentication required. Python 3 standard library only.

## Quick Reference

| Command | Description |
|---------|-------------|
| `search` | Search Wikipedia articles by query |
| `summary` | Get article intro/summary |
| `article` | Get full article text |
| `sections` | List article sections |
| `random` | Get a random article summary |
| `today` | Featured article and "On this day" events |
| `links` | Show internal links from an article |
| `langs` | Show available languages for an article |

## Commands

### search
Search Wikipedia for articles matching a query.
```bash
python3 ~/.claude/skills/wikipedia/scripts/wikipedia.py search "artificial intelligence"
python3 ~/.claude/skills/wikipedia/scripts/wikipedia.py search "quantum computing" --limit 5
```

### summary
Get the introductory summary of a Wikipedia article.
```bash
python3 ~/.claude/skills/wikipedia/scripts/wikipedia.py summary "Python (programming language)"
python3 ~/.claude/skills/wikipedia/scripts/wikipedia.py summary "Albert Einstein"
```

### article
Get the full article text (truncated to 5000 chars). Optionally specify a section.
```bash
python3 ~/.claude/skills/wikipedia/scripts/wikipedia.py article "Rust (programming language)"
python3 ~/.claude/skills/wikipedia/scripts/wikipedia.py article "Rust (programming language)" --section 2
```

### sections
List all sections of an article with index numbers.
```bash
python3 ~/.claude/skills/wikipedia/scripts/wikipedia.py sections "Machine learning"
```

### random
Get a random Wikipedia article summary.
```bash
python3 ~/.claude/skills/wikipedia/scripts/wikipedia.py random
```

### today
Show today's featured article and "On this day" events.
```bash
python3 ~/.claude/skills/wikipedia/scripts/wikipedia.py today
```

### links
Show internal Wikipedia links from an article.
```bash
python3 ~/.claude/skills/wikipedia/scripts/wikipedia.py links "Python (programming language)"
python3 ~/.claude/skills/wikipedia/scripts/wikipedia.py links "Python (programming language)" --limit 10
```

### langs
Show what languages an article is available in.
```bash
python3 ~/.claude/skills/wikipedia/scripts/wikipedia.py langs "Python (programming language)"
```

## Common Workflows

### Research a topic
1. `search` to find relevant articles
2. `summary` to get an overview
3. `sections` to see the article structure
4. `article --section N` to read specific sections

### Explore connections
1. `summary` on a topic
2. `links` to see related articles
3. `summary` on linked articles of interest

### Discover something new
1. `random` to get a random article
2. `today` to see featured content and historical events

### Check multilingual availability
1. `langs` to see which languages an article exists in
