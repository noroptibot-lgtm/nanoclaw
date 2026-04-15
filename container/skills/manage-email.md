---
name: manage-email
description: Scan Gmail, categorize emails (brand deals, important, noise), draft partnership replies with manager CC, and manage your inbox. Use anytime you want to check or triage email.
---

# Manage Email

Inbox triage — scan recent emails, surface brand deal inquiries, draft templated replies that loop in your brand manager, highlight what matters, and flag the noise.

---

## Config

Read these from the project's `CLAUDE.md`:

| Key | Value |
|-----|-------|
| Brand Manager Email | YOUR_MANAGER_EMAIL |
| Brand Manager Name | YOUR_MANAGER_NAME |
| Your Name | YOUR_NAME |
| Scan Window | 24-48 hours |

---

## Process

### Step 1: Scan Recent Emails

Search Gmail for all emails from the last 48 hours using multiple queries in parallel:

**Query 1 — Brand deal keywords:**
```
newer_than:2d (collaboration OR partnership OR sponsorship OR sponsor OR "brand deal" OR "paid promotion" OR influencer OR campaign OR UGC OR "creator program" OR "paid collab" OR "paid partnership" OR "would love to work" OR "interested in working")
```

**Query 2 — All recent inbox emails:**
```
newer_than:2d in:inbox
```

Use the GWS CLI to search Gmail via Bash:
```bash
gws gmail users messages list --params '{"userId": "me", "q": "newer_than:2d (collaboration OR partnership OR sponsorship ...)", "maxResults": 50}'
```
Paginate if needed (use `pageToken` from response).

### Step 2: Read and Categorize

Read the full content of each email using the GWS CLI:
```bash
gws gmail users messages get --params '{"userId": "me", "id": "MESSAGE_ID", "format": "full"}'
```
Categorize every email into one of three buckets:

#### Brand Deal / Partnership Inquiry
Emails from brands, agencies, or creators proposing paid collaborations, sponsorships, UGC deals, or influencer campaigns. Match on:
- Keyword hits from the brand deal search
- Context clues: mentions of "rate card", "deliverables", "compensation", product pitches with partnership intent
- Sender domain is a company/agency (not a personal Gmail unless clearly a brand rep)

#### Important (Action Needed)
Non-brand emails that still need attention:
- Client communication
- Team messages
- Financial / legal (invoices, contracts, bank)
- Platform notifications that require action (account issues, policy changes)
- Personal emails from known contacts

#### Noise (Skip/Archive)
- Marketing newsletters you didn't opt into
- Automated promotional emails
- Generic SaaS upsells
- Social media digest notifications
- Spam that made it through filters

### Step 3: Present the Summary

Output a structured report:

```
## Email Report — [Date]

### Brand Deal Inquiries ([count])
For each:
- **From:** [Name] <[email]> — [Company/Brand]
- **Subject:** [subject line]
- **Summary:** [1-2 sentence summary of what they want]
- **Draft reply:** Ready / Needs review

### Important ([count])
For each:
- **From:** [Name] — [Subject]
- **Why it matters:** [1 sentence]
- **Action needed:** [what to do]

### Noise ([count])
- [Sender — Subject] (x[count] if multiple from same sender)

### Stats
- Total emails scanned: X
- Brand deals: X | Important: X | Noise: X
```

### Step 4: Draft Brand Deal Replies

For EACH brand deal email, create a threaded reply draft using the GWS CLI:

```bash
gws gmail users drafts create --params '{"userId": "me"}' --json '{
  "message": {
    "threadId": "THREAD_ID",
    "raw": "BASE64_ENCODED_EMAIL"
  }
}'
```

To build the raw email, encode this with `base64`:
```
From: YOUR_EMAIL
To: SENDER_EMAIL
Cc: MANAGER_EMAIL
Subject: Re: ORIGINAL_SUBJECT
In-Reply-To: ORIGINAL_MESSAGE_ID
References: ORIGINAL_MESSAGE_ID
Content-Type: text/plain; charset="UTF-8"

Hey [First Name],

Thanks for reaching out — appreciate the interest in working together.

I'm CCing my manager [MANAGER_NAME] ([MANAGER_EMAIL]) who handles all of my partnerships. He'll take it from here.

Hope to be working together soon!

Thanks,
[YOUR_NAME]
```

**Encode with:** `echo -n "RAW_EMAIL" | base64 | tr -d '\n' | tr '+/' '-_'`

The `threadId` comes from reading the original email — every email result includes a `threadId` field. This creates a properly threaded draft (the old Gmail MCP couldn't do this).

Present each draft for review before creating. If the user approves, create all drafts.

### Step 5: Inbox Cleanup & Organization (via n8n Webhooks)

After the user reviews the summary, take these actions with user confirmation.

**n8n Webhook URLs (update with your n8n instance):**
- **Star messages:** `POST https://YOUR_N8N_INSTANCE/webhook/gmail-star`
- **Mark as read:** `POST https://YOUR_N8N_INSTANCE/webhook/gmail-mark-read`

**Payload format (both endpoints):**
```json
{"messageIds": ["id1", "id2", "id3"]}
```

**Use Bash with curl:**
```bash
curl -s -X POST "https://YOUR_N8N_INSTANCE/webhook/gmail-star" \
  -H "Content-Type: application/json" \
  -d '{"messageIds": ["id1", "id2"]}'
```

**Actions:**
1. Collect all Brand Deal + Important message IDs → POST to `/webhook/gmail-star`
2. Collect ALL handled message IDs (Brand Deal + Important + Noise) → POST to `/webhook/gmail-mark-read`

**Rule: Every email shown in the report gets marked as read.** If we surfaced it and dealt with it, it's handled — mark it read.

Present the count before executing: "Ready to star X emails and mark Y as read. Proceed?"

---

## Edge Cases

- **Existing brand deal threads** — flag these as "Active Deal Update" rather than new inquiry. Do NOT send the template reply to ongoing conversations.
- **Ambiguous emails** — If unclear whether brand deal or spam, include in the summary with a "?" flag and let the user decide.
- **No brand deals found** — Still present the Important vs Noise breakdown.
- **Duplicate threads** — Group by thread, don't list each reply separately.

---

## Notes

- This skill uses the **GWS CLI** (`gws gmail ...`) for all Gmail operations — no MCP server needed
- **Reply drafts** are created directly via `gws gmail users drafts create` with proper threading (threadId + In-Reply-To headers)
- Starring and mark-as-read use n8n webhook workflows (GWS CLI can also do this via `gws gmail users messages modify` if n8n webhooks are unavailable)
- Brand manager email and template can be updated in the Config table above
