# Firehose — Real-time Web Monitoring

Firehose monitors the web in real-time. Create rules (Lucene queries), and every crawled page matching a rule is delivered via SSE stream.

## Credentials

Stored in `~/.config/meta-api.env`:
```
FIREHOSE_API_KEY=fhm_WAmQmjhhSPxU1rWEyi4Fc5LuiumaNqjziLeoMl8X
```

Load with:
```bash
KEY=$(grep FIREHOSE ~/.config/meta-api.env | cut -d= -f2)
```

> DO NOT use `source ~/.config/meta-api.env && curl...` — env vars don't persist across `&&`. Always use `$(grep ...)` inline.

## Base URL

```
https://api.firehose.com
```

## Authentication

Two key types:
- **Management Key** (`fhm_` prefix): Create/list/manage taps. Get from dashboard.
- **Tap Token** (`fh_` prefix): Create rules within a tap and stream data.

Both use: `Authorization: Bearer <key>`

## Active Taps

| Tap | Token | Purpose |
|-----|-------|---------|
| Openclaw Brand Mentions | `fh_nkAlY0a5U4EpWUNuwNfCHt2diwlnknE4tf5sgTbn` | Monitor openclaw + noropti mentions |
| AI Cold Outreach & Lead Gen | `fh_hJxZyAJIUPX3pXZhERZ67Jdczysa4yQ1UfI5VYN4` | Cold email AI content + Claude Code articles |

## Active Rules

| Rule ID | Tap | Query | Tag |
|---------|-----|-------|-----|
| 9ea1e19f | Openclaw | `openclaw OR noropti` | brand-mentions |
| d95cbb65 | AI Outreach | `"cold email" AND (AI OR "artificial intelligence") AND language:"en"` | ai-cold-email |
| e64a29f3 | AI Outreach | `"Claude Code" AND page_type:"/Article" AND language:"en"` | claude-code-mentions |

## Common Operations

### List taps (management key)
```bash
KEY=$(grep FIREHOSE ~/.config/meta-api.env | cut -d= -f2)
curl -s -H "Authorization: Bearer $KEY" "https://api.firehose.com/v1/taps" | python3 -m json.tool
```

### List rules for a tap
```bash
TAP_TOKEN="fh_nkAlY0a5U4EpWUNuwNfCHt2diwlnknE4tf5sgTbn"
curl -s -H "Authorization: Bearer $TAP_TOKEN" "https://api.firehose.com/v1/rules" | python3 -m json.tool
```

### Create a rule
```bash
TAP_TOKEN="fh_..."
curl -s -X POST "https://api.firehose.com/v1/rules" \
  -H "Authorization: Bearer $TAP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"value": "your lucene query here", "tag": "optional-label"}'
```

### Stream events (SSE)
```bash
TAP_TOKEN="fh_..."
curl -N -H "Authorization: Bearer $TAP_TOKEN" \
  "https://api.firehose.com/v1/stream"
```

Or stream with a specific rule:
```bash
curl -N -H "Authorization: Bearer $TAP_TOKEN" \
  "https://api.firehose.com/v1/stream?rule_id=RULE_ID"
```

### Delete a rule
```bash
TAP_TOKEN="fh_..."
curl -s -X DELETE -H "Authorization: Bearer $TAP_TOKEN" \
  "https://api.firehose.com/v1/rules/RULE_ID"
```

## Lucene Query Syntax

| Pattern | Example | Meaning |
|---------|---------|---------|
| Any mention | `openclaw` | Page contains "openclaw" |
| Exact phrase | `"cold email"` | Exact phrase match |
| Title only | `title:tesla` | Matches page title |
| Domain | `domain:techcrunch.com` | From specific site |
| Category | `page_category:"/News"` | ML-classified news |
| Type | `page_type:"/Article"` | Article pages |
| Language | `language:"en"` | English only |
| Boolean | `ahrefs AND semrush` | Both terms |
| OR | `ahrefs OR semrush` | Either term |
| NOT | `NOT promotional` | Exclude keyword |
| Date range | `publish_time:[2026-01-01 TO 2026-03-01]` | Date range |

## Dashboard
https://firehose.com/management-keys
