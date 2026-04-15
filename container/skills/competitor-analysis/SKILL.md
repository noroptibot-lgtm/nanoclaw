---
name: competitor-analysis
description: Competitor analysis skill — research and analyze competitors' messaging, positioning, ads, content, pricing, and weaknesses. Use when you need to understand what competitors are doing, find gaps to exploit, write positioning that wins against them, or build a competitive intelligence report.
---

# Competitor Analysis Skill

Research competitors, find their weaknesses, and identify positioning gaps you can own.

---

## What This Skill Covers

- **Messaging & positioning** — what they say and how they say it
- **Ad creative** — what ads are running, what hooks they use
- **Content strategy** — what they publish, what performs
- **Pricing & offers** — how they structure their deals
- **Weaknesses** — what customers complain about (reviews, forums)
- **Gap analysis** — what nobody is saying that you could own

---

## Step 1: Define Competitors

Ask the user for:
1. **Direct competitors** — same product/service, same target customer
2. **Indirect competitors** — different product, same problem they solve
3. **Aspirational competitors** — bigger players you want to learn from

If unknown, search: `[industry] + [location] + [service type]` and find top 3-5 results.

---

## Step 2: Messaging Audit

For each competitor, analyze their homepage:

**Questions to answer:**
- What's their headline promise?
- Who is their target customer?
- What's their main differentiator?
- What proof do they use? (numbers, logos, testimonials)
- What's their CTA?
- What fear/pain do they address?
- What do they NOT say? (Gaps = your opportunity)

**Output format:**
```
Competitor: [Name]
URL: [homepage]
Headline: "[exact headline]"
Promise: [transformation they offer]
Target: [who they're talking to]
Differentiator: [what makes them "unique"]
Proof: [type of social proof]
CTA: [primary call to action]
Gap: [what they're NOT saying]
```

---

## Step 3: Ad Intelligence

### Meta Ad Library
Search: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=NO&q=[competitor name]`

For each active ad, note:
- Format (image/video/carousel)
- Hook (first line or first 3 seconds)
- Offer being promoted
- How long it's been running (longer = working)

### Google Ads
Search for their core keywords and note:
- Headline structure
- What benefits they lead with
- Any promotions or offers

---

## Step 4: Review Mining

Find what real customers say on:
- Google Reviews
- Trustpilot
- Reddit: `site:reddit.com "[competitor name]"`

**Mine for:**
- **Positive reviews** → Use this language in your own copy
- **Negative reviews** → Your opportunity to be better
- **Repeated complaints** → A market-wide problem you can solve

---

## Step 5: Gap Analysis

After auditing all competitors, answer:

1. **What is everyone saying?** → Avoid this (you'll sound like everyone else)
2. **What is nobody saying?** → Your positioning opportunity
3. **What are customers complaining about?** → Solve this and lead with it

**Positioning formula:**
> "We're the only [category] that [unique mechanism] for [specific customer] who [specific problem], without [common objection]."

---

## Output Format

```
# Competitive Analysis — [Market/Industry]
Date: [today]

## Competitor Profiles
[One block per competitor]

## What Everyone Is Saying
[Common claims across all competitors]

## Gaps Nobody Is Owning
[3 specific positioning angles available]

## Customer Complaints (Market-wide)
[Top 3 recurring complaints from reviews]

## Recommended Positioning
[Your positioning formula]
```
