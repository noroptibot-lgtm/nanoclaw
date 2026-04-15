---
name: reddit
description: Browse Reddit — search subreddits, read posts and comments, view trending content, check user profiles. Social media browsing skill for Reddit.
---

# Reddit Browser Skill

Browse Reddit directly from Claude Code. Search subreddits, read posts and comments, view trending content, and check user profiles using Reddit's public JSON API.

## Setup

No setup needed. This skill uses Reddit's public JSON API which requires no authentication. Just run the commands below.

## Quick Reference

| Command | What it does |
|---|---|
| `posts <subreddit>` | List posts from a subreddit |
| `search <query>` | Search posts across Reddit or a specific subreddit |
| `comments <post_id>` | Read comments on a post |
| `trending` | Show popular posts across all of Reddit |
| `user <username>` | View a user's recent posts and comments |
| `subreddit <name>` | Get subreddit info (description, subscribers, etc.) |

## Commands

### List Posts

```bash
python3 ~/.claude/skills/reddit/scripts/reddit.py posts <subreddit> [--sort hot|new|top|rising] [--time hour|day|week|month|year|all] [--limit N]
```

- `--sort` defaults to `hot`. Use `top` with `--time` to get top posts for a time period.
- `--time` only applies when `--sort` is `top`. Defaults to `day`.
- `--limit` defaults to 10.

### Search Posts

```bash
python3 ~/.claude/skills/reddit/scripts/reddit.py search <query> [--subreddit <name>] [--sort relevance|hot|top|new] [--limit N]
```

- Omit `--subreddit` to search all of Reddit.
- `--sort` defaults to `relevance`.
- `--limit` defaults to 10.

### Read Comments

```bash
python3 ~/.claude/skills/reddit/scripts/reddit.py comments <post_id_or_url> [--limit N]
```

- Accepts a post ID (e.g., `abc123`) or a full Reddit URL.
- Shows top-level comments with author, score, and body text.
- `--limit` defaults to 10.

### Trending Posts

```bash
python3 ~/.claude/skills/reddit/scripts/reddit.py trending [--limit N]
```

- Shows popular posts from across all of Reddit via /r/popular.
- `--limit` defaults to 10.

### User Profile

```bash
python3 ~/.claude/skills/reddit/scripts/reddit.py user <username> [--type posts|comments|both] [--limit N]
```

- `--type` defaults to `both` (shows recent posts and comments).
- `--limit` defaults to 10 (applies per type when using `both`).

### Subreddit Info

```bash
python3 ~/.claude/skills/reddit/scripts/reddit.py subreddit <name>
```

- Shows subreddit description, subscriber count, creation date, and other metadata.

## Common Workflows

### Browse a subreddit's top posts this week
```bash
python3 ~/.claude/skills/reddit/scripts/reddit.py posts python --sort top --time week --limit 20
```

### Search for a topic and then read comments on an interesting post
```bash
python3 ~/.claude/skills/reddit/scripts/reddit.py search "rust vs go" --sort top --limit 5
python3 ~/.claude/skills/reddit/scripts/reddit.py comments <post_id_from_above>
```

### Check what's trending on Reddit right now
```bash
python3 ~/.claude/skills/reddit/scripts/reddit.py trending --limit 15
```

### Research a user's activity
```bash
python3 ~/.claude/skills/reddit/scripts/reddit.py user spez --type both --limit 10
```

### Get info about a subreddit before browsing it
```bash
python3 ~/.claude/skills/reddit/scripts/reddit.py subreddit machinelearning
```
