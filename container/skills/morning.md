---
name: morning
description: Daily morning briefing — full email triage with drafts, AI/Claude Code news with actionable context, task priorities, and account stats. Run this first thing or let the 10 AM cron handle it.
---

# Morning Briefing

Your daily command center. Spawns 4 parallel agents, combines their results into one briefing.

---

## Config

Read these from the project's `CLAUDE.md`:

| Key | Value |
|-----|-------|
| Timezone | YOUR_TIMEZONE |
| Brand Manager Email | YOUR_MANAGER_EMAIL |
| Brand Manager Name | YOUR_MANAGER_NAME |
| Your Name | YOUR_NAME |
| Output | Terminal only |
| Task Board | Airtable — see task management config in CLAUDE.md |

---

## Execution

**Spawn ALL 4 agents in a single message so they run in parallel.** Do NOT run them sequentially. Use the Agent tool 4 times in one response.

After all 4 agents return, combine their outputs into the final briefing format, then ask what to do next.

---

## Agent 1: Email Triage

Spawn a `general-purpose` agent with this prompt:

```
You are running Module 1 (Email Triage) of the morning briefing. Do the FULL email triage — not a scan.

STEPS:
1. Search Gmail for ALL unread inbox emails using multiple queries:
   - "is:unread in:inbox" (all unread — NO category filters) — maxResults: 50
   - "newer_than:2d subject:collab OR subject:partnership OR subject:sponsor OR subject:paid" (brand deal keywords)

2. PAGINATE THROUGH ALL RESULTS. The first search returns up to 50 emails and a nextPageToken. You MUST call again with that pageToken to get the next 50, and repeat until either:
   - There is no nextPageToken returned (you've reached the end), OR
   - You've gone back far enough that emails are older than 48 hours AND you've confirmed no brand deals or revenue emails remain
   - Typical inbox: 100-200+ unread emails. NEVER stop at page 1. Always get at least 2-3 pages.

3. Deduplicate results by message ID across all pages and both queries.

4. Read the FULL content of every email — not just subject lines. For bulk automated categories (new customer notifications, digest emails), you can categorize from the snippet/subject. But ALWAYS read the full body of: brand deal emails, emails from real people (not automated), emails marked IMPORTANT, and anything ambiguous.

5. Categorize every email into these buckets:
   - Brand Deals — partnership offers, paid collabs, sponsorships
   - Revenue — new customers, payments received, subscription notifications
   - Important — calls booked, replies from active threads, team emails
   - Community — community notifications, member questions
   - Noise — error alerts, login notifications, digests, marketing

6. Draft replies for ALL brand deal emails (CC your manager). Use gmail_create_draft.

7. After triage, collect message IDs for inbox cleanup:
   - All Brand Deal + Important + Revenue message IDs → for starring
   - ALL handled message IDs (every category) → for marking as read

CRITICAL RULES:
- Do NOT use -category: Gmail filters. They hide payment and notification emails.
- Actually READ every non-bulk email body.
- Actually DRAFT replies for brand deals with manager CC'd. No exceptions.
- Revenue is its own category — you want to see money coming in.
- Paginate all results (follow nextPageToken).

Return your results in this EXACT format:

## Email

### Brand Deals ([count]) — drafts created
- **[Brand]** ([Contact]) — [what they want] — Draft ready

### Revenue ([count])
- **[Source]** — [who paid / what] — $XX

### Important ([count])
- **[From]** — [Subject] — [action needed]

### Community ([count])
- [summary of community activity]

### Noise ([count])
- [errors, login alerts, digests — one-line summary]

### Inbox Cleanup
- Star: [count] emails (Brand Deals + Revenue + Important)
- Mark as read: [count] emails (all categories)
- Message IDs to star: [comma-separated list]
- Message IDs to mark read: [comma-separated list]
```

---

## Agent 2: AI News Brief

Spawn a `general-purpose` agent with this prompt:

```
You are running Module 2 (AI News Brief) of the morning briefing. Give a thorough briefing on what's happening in AI right now — the last 24-48 hours.

This is NOT a content ideation list. This is a news brief so you stay informed. You'll decide if anything is worth filming separately.

SOURCES TO CHECK (use WebSearch + WebFetch):
1. WebSearch: "AI news today [current month year]" — get the latest headlines
2. WebSearch: "Claude Code update OR release OR changelog [year]" — Claude-specific
3. WebSearch: "OpenAI announcement OR launch OR update [current month year]"
4. WebSearch: "Gemini OR Google AI update [current month year]"
5. WebSearch: "n8n update OR release [year]"
6. WebSearch: "AI tools launch OR release this week"
7. WebFetch: https://github.com/trending — today's trending repos (scan for AI-related)
8. WebSearch: "site:reddit.com AI tool OR Claude OR ChatGPT" — community buzz

For EACH piece of news, go DEEP. Don't just say "X launched Y." Explain:
- What it actually does in plain terms
- Why it matters (or doesn't)
- How it connects to tools you already use (Claude Code, n8n, Supabase, MCP servers, etc.)

RULES:
- Only genuinely new items (last 48 hours). Don't pad with old news.
- If nothing major happened, say so honestly.
- Go deep on fewer items rather than shallow on many.
- Group by category: Major Releases, Tool Updates, Industry News, GitHub Trending, Community Buzz
- ALWAYS include a source URL for every item.

Return in this format:

## AI News Brief

### Major Releases
**[Name]** — [What it is in 1 sentence]
[Source](url)
[2-3 sentences going deep: what it does, how it works, why it matters.]

### Tool Updates
**[Tool] [version]** — [What changed]
[Source](url)
[Context on why this update matters]

### Industry News
**[Headline]** — [What happened and why anyone should care]
[Source](url)

### GitHub Trending (AI)
- **[repo name]** ([stars today]) — [what it does, 1 sentence] — [GitHub](url)

### Community Buzz
- [What people on Reddit/X are talking about in AI — 2-3 bullet points with links]

If a category has nothing new, skip it entirely.
```

---

## Agent 3: Today's Priorities

Spawn a `general-purpose` agent with this prompt:

```
You are running Module 3 (Today's Priorities) of the morning briefing. Today is [INSERT TODAY'S DATE AND DAY].

Pull from THREE sources:

1. Airtable Central Task Board — Pull all non-Done tasks.
   - Use the Airtable MCP tools
   - Read base ID and table ID from the project's CLAUDE.md (Task Management section)
   - Pull fields: Task, Due Date, Status, Priority, Project, Notes
   - Filter: Status != "Done", sort by Priority then Due Date
   - Categorize: Urgent (due today or overdue), This Week (due within 7 days), Backlog (everything else)

2. Google Calendar — Check today's calendar for calls, meetings, deadlines.

3. Community Pipeline (Friday Drop) — Pull records from Community Pipeline table.
   - Read base ID and table ID from CLAUDE.md
   - Pull ALL records where Status = "Planned" or Status = "In-Progress"
   - Show what's on deck for Friday's drop and what's currently being worked on

Return your results in this EXACT format:

## Today's Plan

**Urgent (Due Today / Overdue):**
- [ ] [Task from Airtable — priority, due date]

**This Week:**
- [ ] [Task] — due [date] — [project]

**Calls:**
- [Time] — [Who] — [What] — [Prep notes]

**Community Friday Drop:**
🔨 In-Progress:
- [Title] — [content type] — [notes summary]

📋 On Deck (Planned):
- [Title] — [content type]

**Backlog:**
- [Task] — [project]
```

---

## Agent 4: Account Stats + Funnel Metrics

Spawn a `general-purpose` agent with this prompt:

```
You are running Module 4 (Account Stats + Funnel Metrics) of the morning briefing. Pull account metrics and DM funnel stats from Supabase.

Use the Supabase MCP tools with your project ID from CLAUDE.md.

Query 1 — Latest follower counts with day-over-day delta:
SELECT platform, follower_count, snapshot_date
FROM account_snapshots
WHERE platform IN ('instagram', 'tiktok', 'youtube')
  AND snapshot_date >= CURRENT_DATE - INTERVAL '3 days'
ORDER BY platform, snapshot_date DESC;

Query 2 — DM funnel stats (all-time per flow):
SELECT * FROM crm.funnel_stats;

Query 3 — DM funnel daily stats (last 7 days):
SELECT * FROM crm.funnel_stats_daily
WHERE date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY date DESC;

Query 4 — Latest funnel snapshot (for trending):
SELECT * FROM crm.funnel_snapshots
ORDER BY snapshot_date DESC
LIMIT 2;

IMPORTANT: For CRM schema queries, the tables are in the crm schema. Reference crm.funnel_stats, crm.funnel_stats_daily, and crm.funnel_snapshots.

Return your results in this EXACT format:

## Account
- IG: XX,XXX (+/- XX from yesterday)
- TikTok: XX,XXX (+/- XX)
- YouTube: XXX (+/- XX)

## DM Funnel
- DMs Sent: XXX (all-time)
- Emails Captured: XXX (XX% capture rate)
- Notion Clicks: XXX
- Skool Clicks: XXX (DM: XX, Notion: XX)
- 7-day trend: [up/down/flat] — [brief note on what changed]

If any CRM queries return empty results, note "Funnel data not yet populated" and move on.
```

---

## After All Agents Return

Once all 4 agents have returned their results:

### 1. Combine into briefing

```
# Morning Briefing — [Date] ([Day of Week])

## Email
[Agent 1 output — full triage with all categories]

## AI News Brief
[Agent 2 output — detailed with content angles]

## Today's Plan
[Agent 3 output — tasks, calendar, community pipeline]
**From email:**
- [ ] [Any urgent items surfaced from Agent 1 results — brand deal deadlines, payments needing action, etc.]

## Stats
[Agent 4 output — account stats + DM funnel]
```

### 2. Auto-Research Consulting Call Prospects

Check Agent 3's calendar output for any consulting calls today (look for "Consultation", "Consulting", "AI Consultation" in event titles, or booking events with non-team attendees).

For each consulting call found:
1. Extract the prospect's name and email from the calendar event description
2. Check if a research brief already exists for this prospect
3. If NO brief exists → run `/prospect-researcher` with the name, email, and booking notes
4. If a brief already exists → skip, just mention "Brief ready for [Name]"

Present it as:

```
## Consulting Call Prep
- [Time] — [Name] ([Company]) — Researching now...
```

### 3. Inbox Cleanup

After presenting the briefing, use the message IDs from Agent 1 to clean up the inbox.

If you have n8n webhooks configured for inbox cleanup in your CLAUDE.md, use them:

```bash
# Star important emails
curl -s -X POST "YOUR_N8N_WEBHOOK_URL/gmail-star" \
  -H "Content-Type: application/json" \
  -d '{"messageIds": ["id1", "id2"]}'

# Mark all handled emails as read
curl -s -X POST "YOUR_N8N_WEBHOOK_URL/gmail-mark-read" \
  -H "Content-Type: application/json" \
  -d '{"messageIds": ["id1", "id2"]}'
```

Present the count: "Ready to star X emails and mark Y as read. Proceed?"

If no webhook URLs are configured, skip this step.

### 4. Ask what's next

```
---
What do you want to tackle first?
- /manage-email — Re-run email triage or handle new emails
- /daily-content-researcher — Find today's content topics
```

---

## CRITICAL RULES

1. **All 4 agents MUST launch in parallel.** One message, 4 Agent tool calls. This is the whole point — speed.
2. **PAGINATE ALL UNREAD EMAILS.** Agent 1 must follow nextPageToken for ALL pages. Never stop at page 1.
3. **Never use `-category:` Gmail filters.** They hide payment and notification emails.
4. **Draft replies for ALL brand deal emails automatically.** CC your manager. No exceptions.
5. **Revenue is its own category.** New customers, payments, subscriptions.
6. **AI News needs depth, not breadth.** Agent 2 is a news brief, NOT a content ideation list. Go deep on fewer items.
7. **If any agent fails, include the error and continue.** Don't block the whole briefing.
8. **After combining, cross-reference email with tasks.** Surface any urgent email items in the Today's Plan section.
9. **Inbox cleanup after presenting.** Use webhooks if configured.
10. **Present everything in terminal.** No file writing needed.
11. **End by asking what to do next.** Always give the action menu.
12. **The full flow is: spawn 4 agents → combine results → present briefing → consulting call prep → inbox cleanup → ask what's next.**
