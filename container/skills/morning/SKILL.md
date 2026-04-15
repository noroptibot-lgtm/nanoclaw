---
name: morning
description: Daily morning briefing — full email triage with drafts, AI/Claude Code news with actionable context, task priorities, and account stats. Run this first thing every day.
---

# Morning Briefing

Your daily command center. Runs 4 modules, presents a single briefing in terminal.

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

---

## Process

### Module 1: Full Email Triage

**This is NOT a scan — run the FULL `/manage-email` process:**

1. Search Gmail for last 48 hours using **multiple queries** to catch everything:
   - `is:unread in:inbox` (all unread inbox — NO category filters)
   - `newer_than:2d subject:collab OR subject:partnership OR subject:sponsor OR subject:paid` (brand deal keywords)
2. **Deduplicate** results by message ID
3. **Read the full content** of every email using `gmail_read_message` — not just subject lines
4. Categorize every email into these buckets:
   - **Brand Deals** — partnership offers, paid collabs, sponsorships
   - **Revenue** — new customers, payments received, subscription notifications
   - **Important** — calls booked, replies from active threads, team emails
   - **Community** — community platform notifications, member questions
   - **Noise** — error alerts, login notifications, digests, marketing
5. **Draft replies** for all brand deal emails (CC your manager)

**CRITICAL: Do NOT use `-category:` Gmail filters.** These exclude payment confirmations and notification emails that Gmail auto-categorizes. Search `is:unread in:inbox` to get EVERYTHING.

**Output for briefing:**
```
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
```

**Do NOT skip reading emails.** The whole point is that you open Claude and your email is handled.

### Module 2: AI & Tech News

Check for new releases, features, and announcements from the last 24-48 hours relevant to your niche.

**Sources to scrape (use WebFetch + WebSearch):**

1. **Tool changelogs** — WebFetch the changelogs of your primary tools
2. **Industry blogs** — WebSearch for relevant announcements
3. **General AI news** — WebSearch for `AI news update release launch` + today's date

**For EACH news item, provide 3 things:**

```
### [Feature/Release Name]

**What:** [2-3 sentences explaining what it actually does]

**Why it matters:** [How this affects your workflow or business]

**Content angle:** [One specific video/post idea you can create about this]

---
```

**Evaluation criteria:**
- Is this actually new (last 48h)?
- Is it relevant to your work?
- Could you make content about this?
- Does this change how you work day-to-day?

If nothing new: "No major news in the last 24 hours."

### Module 3: Today's Tasks

Read the project's `TASKS.md` file. Identify:

1. What phase/section is marked as top priority?
2. What are the next 3-5 actionable tasks?
3. Any deadlines or time-sensitive items from email (contracts to sign, payments failing, etc.)?

**Output for briefing:**
```
## Tasks
**Priority:** [current top priority phase]
**Today's focus:**
- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]
**From email:**
- [ ] [Any urgent items surfaced from Module 1]
```

### Module 4: Account Stats

Pull latest account metrics from your data source (Supabase, Airtable, etc.).

```sql
-- Example: Latest follower counts
SELECT platform, follower_count, snapshot_date
FROM account_snapshots
WHERE snapshot_date >= CURRENT_DATE - INTERVAL '2 days'
ORDER BY platform, snapshot_date DESC;

-- Example: This month's top content
SELECT caption, views, likes, shares, saves, platform, post_date
FROM content
WHERE post_date >= date_trunc('month', CURRENT_DATE)
ORDER BY views DESC
LIMIT 5;
```

**Output for briefing:**
```
## Account
- Platform 1: XX,XXX (+/- XX)
- Platform 2: XX,XXX (+/- XX)
- Platform 3: XXX (+/- XX)

Top content this month:
1. "caption..." — XX,XXX views (platform)
```

---

## Final Output

Combine all modules into one clean briefing:

```
# Morning Briefing — [Date] ([Day of Week])

## Email
[Module 1 output — full triage with all categories]

## News
[Module 2 output — detailed with content angles]

## Tasks
[Module 3 output — priorities + urgent items from email]

## Account
[Module 4 output]

---
Actions available:
- /manage-email — Re-run email triage or handle new emails
- /daily-content-researcher — Find today's content topics
```

---

## CRITICAL RULES

1. **Actually read every email.** Don't just scan subject lines. Use `gmail_read_message` on each one.
2. **Never use `-category:` Gmail filters.** They hide payment and notification emails. Always search `is:unread in:inbox`.
3. **Actually draft replies.** Brand deal emails get a draft reply with your manager CC'd. No exceptions.
4. **Revenue is its own category.** New customers, payments, subscriptions — you want to see money coming in.
5. **News needs depth.** Every item gets: what it is, why it matters to you, and a content angle.
6. **If any module fails, skip it and note the error.** Don't block the whole briefing.
7. **News should be genuinely new.** Don't surface week-old announcements.
8. **Present everything in terminal.** No email delivery needed.
