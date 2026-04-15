---
name: hackernews
description: Browse Hacker News — top stories, search, comments, user profiles. Covers HN, tech news, startups, programming, Show HN, Ask HN, and job postings.
---

# Hacker News Skill

Browse and search Hacker News directly from Claude Code. Uses the free HN Algolia API and official Firebase API. No authentication required.

## Setup

No setup needed. The script uses Python 3 standard library only (urllib, json). Works out of the box.

## Quick Reference

```bash
# Browse front page
python3 ~/.claude/skills/hackernews/scripts/hackernews.py top

# Search for a topic
python3 ~/.claude/skills/hackernews/scripts/hackernews.py search "rust programming"

# Read comments on a story
python3 ~/.claude/skills/hackernews/scripts/hackernews.py comments 12345678

# Check a user profile
python3 ~/.claude/skills/hackernews/scripts/hackernews.py user pg
```

## Commands

### top

Show top stories from the HN front page.

```bash
python3 ~/.claude/skills/hackernews/scripts/hackernews.py top
python3 ~/.claude/skills/hackernews/scripts/hackernews.py top --limit 30
```

### new

Show newest stories.

```bash
python3 ~/.claude/skills/hackernews/scripts/hackernews.py new
python3 ~/.claude/skills/hackernews/scripts/hackernews.py new --limit 20
```

### best

Show best-rated stories.

```bash
python3 ~/.claude/skills/hackernews/scripts/hackernews.py best
python3 ~/.claude/skills/hackernews/scripts/hackernews.py best --limit 25
```

### ask

Show Ask HN posts.

```bash
python3 ~/.claude/skills/hackernews/scripts/hackernews.py ask
python3 ~/.claude/skills/hackernews/scripts/hackernews.py ask --limit 15
```

### show

Show Show HN posts.

```bash
python3 ~/.claude/skills/hackernews/scripts/hackernews.py show
python3 ~/.claude/skills/hackernews/scripts/hackernews.py show --limit 15
```

### jobs

Show job postings.

```bash
python3 ~/.claude/skills/hackernews/scripts/hackernews.py jobs
python3 ~/.claude/skills/hackernews/scripts/hackernews.py jobs --limit 20
```

### search

Search HN stories by keyword.

```bash
python3 ~/.claude/skills/hackernews/scripts/hackernews.py search "machine learning"
python3 ~/.claude/skills/hackernews/scripts/hackernews.py search "python" --sort date
python3 ~/.claude/skills/hackernews/scripts/hackernews.py search "startup funding" --sort popularity --limit 20
```

### comments

Show top-level comments on a story by its ID.

```bash
python3 ~/.claude/skills/hackernews/scripts/hackernews.py comments 39312953
```

### user

Show a user's profile — karma, about, account age, submission count.

```bash
python3 ~/.claude/skills/hackernews/scripts/hackernews.py user pg
python3 ~/.claude/skills/hackernews/scripts/hackernews.py user dang
```

## Common Workflows

- **Morning tech news**: Run `top` to see what is trending, then `comments` on interesting stories.
- **Research a topic**: Use `search` to find relevant HN discussions, then `comments` to read the conversation.
- **Track startup ecosystem**: Browse `show` for new launches, `ask` for community questions, `jobs` for hiring trends.
- **Check a person**: Use `user` to see their karma and activity level.
