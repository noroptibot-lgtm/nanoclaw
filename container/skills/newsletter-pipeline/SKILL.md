---
name: newsletter-pipeline
description: Automated 7-stage newsletter pipeline — research, write, infographic, assemble, human review, send, archive. Trigger on /newsletter-pipeline or when user asks to build or run a newsletter system.
---

# Automated Newsletter Pipeline

Turn a 4-hour weekly newsletter grind into a 10-minute review by automating everything except the human-review step.

## The 240-Minute Problem

Manual newsletter process bleeds time across 7 stages: research, writing, visuals, HTML assembly, proofreading, sending, archiving. Most newsletters die because the weekly workload isn't sustainable. The fix is automation with a human checkpoint — not full autonomy.

## The 7 Stages

| # | Stage | Tool | Time | Notes |
|---|-------|------|------|-------|
| 1 | Research | Perplexity (or similar) | ~5 min | Pull the week's most relevant stories for your niche |
| 2 | Writing | Claude | ~60 sec | Uses `prompts/newsletter-voice.md` to match house voice |
| 3 | Infographic | Image gen (DALL-E/Midjourney/Nano Banana) | ~90 sec | One hero image or data viz per issue |
| 4 | HTML Assembly | Template fill | ~10 sec | Inject copy + image into pre-built responsive template |
| 5 | Human Review | **PAUSE** | as long as you need | Only manual step. Read, correct, approve |
| 6 | Send | Gmail API / ESP | ~60 sec | Batch of 500 at a time with rate limiting |
| 7 | Archive | Google Sheets | instant | Log issue, subject, send date, open rate hooks |

## Schedule

Cron job: `0 8 * * MON` (Monday 08:00 local time). Pipeline runs stages 1–4 automatically, then drops the HTML preview in your review queue. You approve → stages 6–7 execute.

## Skill File Layout

```
skills/newsletter-pipeline/
├── SKILL.md                 ← this file, orchestrator
├── prompts/
│   ├── newsletter-voice.md  ← house voice/style reference
│   ├── research-brief.md    ← Perplexity/search prompt
│   └── image-brief.md       ← visual generation prompt
├── templates/
│   └── newsletter.html      ← responsive email template with {{placeholders}}
└── state/
    └── archive.csv          ← log of every issue sent
```

## Orchestrator Flow

1. **Research** — Call Perplexity API (or web search) with the brief from `prompts/research-brief.md`. Extract 5 top stories.
2. **Write** — Feed stories + `prompts/newsletter-voice.md` to Claude. Output: subject line + body in markdown.
3. **Image** — Generate hero visual with prompt from `prompts/image-brief.md`. Save to `state/images/{YYYY-MM-DD}.png`.
4. **Assemble** — Read `templates/newsletter.html`, substitute `{{subject}}`, `{{body_html}}` (markdown → HTML), `{{image_url}}`.
5. **Review** — Post the preview to a Slack/Telegram channel or save to `state/pending/{YYYY-MM-DD}.html`. Wait for explicit approval.
6. **Send** — Only after approval. Use Gmail API batch send with 500-per-batch limit and 2-second delays between batches.
7. **Archive** — Append a row to the archive sheet: date, subject, recipients, status.

## Human Review Rules

- Never auto-send. The review gate is what makes this ship without embarrassment.
- If the pipeline runs but review doesn't happen by EOD Monday, skip the week instead of pushing a stale issue.

## Why This Works

Research + writing + assembly is the expensive part of manual workflow. The review is where your judgment actually matters. Automating the first four stages frees your attention for the one step a machine shouldn't own.
