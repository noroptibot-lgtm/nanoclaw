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

Use `gmail_search_messages` for both queries. Paginate if needed to get all results.

### Step 2: Read and Categorize

Read the full content of each email using `gmail_read_message`. Categorize every email into one of three buckets:

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

For EACH brand deal email, create a reply draft using the n8n webhook (Gmail MCP's `gmail_create_draft` does NOT support threading — it creates standalone emails):

**Webhook:** `POST https://YOUR_N8N_INSTANCE/webhook/gmail-reply-draft`

**Payload:**
```json
{
  "to": "sender@example.com",
  "cc": "MANAGER_EMAIL",
  "subject": "Re: [original subject]",
  "body": "Hey [First Name],\n\nThanks for reaching out — appreciate the interest in working together.\n\nI'm CCing my manager [MANAGER_NAME] ([MANAGER_EMAIL]) who handles all of my partnerships. He'll take it from here.\n\nHope to be working together soon!\n\nThanks,\n[YOUR_NAME]",
  "threadId": "[threadId from the original email]"
}
```

**Important:** The `threadId` comes from `gmail_read_message` or `gmail_search_messages` — every email result includes a `threadId` field. This ensures the draft appears inside the existing conversation thread.

Use Bash `curl` to call the webhook. **Do NOT use WebFetch** (it only does GET).

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

- This skill uses Gmail MCP tools: `gmail_search_messages`, `gmail_read_message`
- **Reply drafts** use the n8n `gmail-reply-draft` webhook (Gmail MCP's `gmail_create_draft` has no `threadId` param)
- Starring and mark-as-read use n8n webhook workflows (Gmail MCP doesn't support label modifications)
- Brand manager email and template can be updated in the Config table above
