---
name: tavily
description: AI-optimized web search via Tavily API. Returns concise, relevant results for research and fact-checking.
metadata:
  tags: search, web, research, tavily, extract
---

# Tavily Search

AI-optimized web search using Tavily API. Designed for AI agents - returns clean, relevant content.

## Prerequisites

- Node.js installed
- `TAVILY_API_KEY` environment variable set (get one at https://tavily.com)

## Search

```bash
node {baseDir}/scripts/search.mjs "query"
node {baseDir}/scripts/search.mjs "query" -n 10
node {baseDir}/scripts/search.mjs "query" --deep
node {baseDir}/scripts/search.mjs "query" --topic news
```

## Options

- `-n <count>`: Number of results (default: 5, max: 20)
- `--deep`: Use advanced search for deeper research (slower, more comprehensive)
- `--topic <topic>`: Search topic - `general` (default) or `news`
- `--days <n>`: For news topic, limit to last n days

## Extract content from URL

```bash
node {baseDir}/scripts/extract.mjs "https://example.com/article"
```

## When to Use

- Use search for general web research, fact-checking, or finding current information
- Use `--deep` for complex research questions requiring comprehensive results
- Use `--topic news` for current events and recent news
- Use extract to pull full content from a specific URL

## Notes

- Requires `TAVILY_API_KEY` from https://tavily.com
- Tavily is optimized for AI - returns clean, relevant snippets
- Replace `{baseDir}` with the skill's base directory path when invoking
