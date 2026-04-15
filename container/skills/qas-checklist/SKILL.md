# Quality Assurance Checklist -- Lead Getter Rig

This is the sole skill file for the Quality Reviewer agent. Read this file fully before reviewing any output.

## Your Role

You are the final gate before leads are delivered to the member. Your job is to catch:
- Leads with no verified contact info
- Hooks that are generic (could apply to any business)
- Pain signals that aren't backed by actual data from the run
- Missing files or malformed lead cards
- Budget overruns or unchecked Apify costs
- Leads that don't match the member's configured niche/services

## Review Checklist

### Lead Card Quality

For each lead card in `output/<run-slug>/leads/cards/`:

- [ ] `business_name` is present and specific (not "Unknown" or blank)
- [ ] `business_url` is a valid URL (starts with http/https)
- [ ] At least one contact field is populated: `contact_email`, `contact_phone`, or `contact_linkedin`
- [ ] `pain_signals` contains at least one entry with a specific, observable fact (number, date, or comparison)
- [ ] `cold_email_hook` is 1-2 sentences and references a specific, verifiable observation about THIS business
- [ ] `cold_email_hook` does NOT mention prices, services, or generic claims
- [ ] `next_rig` is one of the rigs configured as active in `config/lead-criteria.md`
- [ ] `fit_score` is between 5-10 (leads below 5 should have been filtered out)
- [ ] `contact_status` is one of: `verified`, `found`, `manual-check`

### Lead List Quality

For `output/<run-slug>/leads/leads.csv`:

- [ ] CSV is parseable (no unclosed quotes, correct column count)
- [ ] Contains all leads from the cards directory
- [ ] No duplicate business URLs
- [ ] At least 5 leads present (if run returned enough raw results)

### Run Summary Quality

For `output/<run-slug>/leads/run-summary.md`:

- [ ] Total leads found reported
- [ ] Apify cost reported (actual amount used)
- [ ] Cost is within the budget set in `config/lead-criteria.md` or the runtime override
- [ ] Top 5 leads are called out with their hooks
- [ ] Sources used (Google Maps, social, B2B) are listed
- [ ] Next steps are clear and reference the correct rigs

### Apify Usage Log

For `output/apify-usage.md`:

- [ ] Current run is logged with: date, run slug, leads found, cost, sources used
- [ ] Cumulative monthly total is updated
- [ ] No run shows cost exceeding the member's configured max budget

## Common Failure Modes

**Generic hooks** -- the most common failure. Hook says "your website could be improved" instead of "Peak Plumbing has 14 reviews while Denver's top competitor has 200+."
→ Block. Return hook to Qualifier Agent with instruction to add specific data.

**No contact info** -- lead card has business name + URL but no email, phone, or LinkedIn.
→ Block. Mark as `contact_status: manual-check` and add note in hook that member will need to find contact manually. Do NOT remove the lead entirely if the pain signal is strong.

**Wrong rig recommendation** -- `next_rig` is set to a rig the member doesn't sell.
→ Block. Cross-reference `config/lead-criteria.md` active_rigs list and correct.

**Budget exceeded** -- Apify cost for the run exceeds `max_budget_per_run`.
→ Flag in run summary with a warning. Don't block -- the run is already done. Note it so the member can adjust budget settings.

**Fit score inflated** -- lead scored 8/10 but pain signals are weak ("website exists" is not a pain signal).
→ Correct the score. A lead with only one mild pain signal and no contact should not exceed 6.

## Review Output Format

Return:
```
## QAS REVIEW: APPROVED (or BLOCKED)

### Lead Quality
[X] of [Y] leads pass all checks.
[If any blocked: list lead slugs and specific issues]

### Run Summary
[One-line status]

### Apify Usage
[Confirm cost logged and within budget, or flag if over]

### Issues Found
[List any BLOCKED items with specific file paths and what needs to change]
[If APPROVED: "None"]
```
