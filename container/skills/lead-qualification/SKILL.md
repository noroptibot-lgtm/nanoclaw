# Lead Qualification Skill

Domain knowledge for identifying and scoring pain signals in prospect businesses. Used by the Qualifier Agent.

## What Makes a Good Lead

A lead is pitch-ready when it has:
1. **A verified pain signal** -- an observable, specific problem the member can fix
2. **A matched rig** -- the pain signal maps directly to one of the member's services
3. **Contact access** -- an email address, LinkedIn profile, or direct phone number
4. **Decision-maker access** -- the contact is the owner, founder, or marketing lead (not a receptionist)

## Pain Signal Library

### AEO Audit Rig Pain Signals
Signals that a business has SEO/AEO problems:
- Website was last updated 1+ years ago (visible in copyright year, blog dates, Wayback Machine)
- No SSL certificate or expired certificate
- Google Maps listing has fewer than 20 reviews while competitors have 100+
- Google Maps listing is incomplete (missing hours, photos, or description)
- No blog or last blog post 6+ months old
- Site loads slowly (visible via WebFetch response time or large page weight)
- No schema markup detectable in page source
- Not showing up for obvious local search queries
- Competitor has clear dominance in local results

### Funnel Builder Rig Pain Signals
Signals that a business has no conversion infrastructure:
- Website has no email signup form or lead magnet
- Website is purely a "brochure" (About, Services, Contact -- nothing to capture leads)
- No landing page for any specific offer or product
- No visible call-to-action above the fold
- Ecommerce site with no abandoned cart or post-purchase flow visible

### Content Strategy Rig Pain Signals
Signals that a business has inconsistent or absent content:
- Social profiles exist but last post was 30+ days ago
- Multiple social channels with inconsistent branding or voice
- LinkedIn company page with under 100 followers despite being established
- Website blog exists but posts are sporadic (3 in 2 years)
- No content calendar evidence -- posting random topics with no theme

### Content Repurposing Rig Pain Signals
Signals that a creator/business produces content but doesn't distribute it:
- Active YouTube channel or podcast but no Twitter/X or LinkedIn presence
- Long-form content (blog posts, videos) that gets no social promotion
- Same content format repeated with no variation across platforms
- YouTube channel with 10K+ views but 100 Instagram followers
- Podcast with no newsletter, no clips, no blog post per episode

### Email Automation Rig Pain Signals
Signals that a business has an email list they're not using:
- Email signup form on site but no newsletter archive visible
- ConvertKit/Mailchimp badge on site but no regular send cadence
- Ecommerce store with no visible email program (no unsubscribe footer, no campaign archive)
- Last email campaign visible in archive is 6+ months old
- No welcome sequence (sign up and watch your inbox -- if nothing arrives in 24 hrs, there's no automation)

## Pain Signal Scoring Rubric

Score each lead 1-10 on fit:

| Score | Meaning |
|-------|---------|
| 9-10 | Multiple strong pain signals + verified contact + clear rig match |
| 7-8 | 1-2 strong pain signals + contact found |
| 5-6 | Pain signal present but weak or unverified |
| 3-4 | Possible pain signal but unclear + contact missing |
| 1-2 | No clear pain signal or wrong type of business |

**Only include leads scoring 5+ in output.** Discard lower-scoring leads silently.

## How to Detect Pain Signals Without Deep Research

The Qualifier Agent should do a **shallow check** -- max 2 WebFetch calls per lead, max 3 minutes per lead. The goal is evidence, not a full audit.

### Quick checks by source:
- **Google Maps lead**: review count visible in raw data; check website URL for SSL (https vs http)
- **Social media lead**: last post date visible in scraped data; follower count vs. engagement ratio
- **Website scrape**: WebFetch homepage -- look for email signup form, last blog post date, page weight
- **B2B database lead**: use job title and company size from scraped data to infer pain; use LinkedIn URL if present

### WebFetch fallback → Apify fallback
1. Try `WebFetch(url)` first -- free, fast, good for homepage analysis
2. If WebFetch returns empty/blocked: try Apify `vdrmota/contact-info-scraper` on the URL
3. If both fail: mark contact_status as "manual-check" and still include the lead

## Writing the Hook

The hook is the single most compelling observation about why this prospect needs help. It becomes the opening line of the member's cold outreach.

### Hook Formula
```
[Specific observation] + [implied consequence] + [rig solution hint]
```

### Hook Examples by Rig

**AEO Audit:**
> "Peak Plumbing has 14 Google reviews while the top competitor has 200+ -- and their site doesn't show up at all when I ask ChatGPT for Denver plumbers."

**Funnel Builder:**
> "Mountain Yoga Studio runs Facebook ads to their homepage, which has no email capture and no offer -- every click is a dead end."

**Content Strategy:**
> "Fernwood Coffee last posted on Instagram 47 days ago and their LinkedIn page has 34 followers despite being open for 6 years."

**Content Repurposing:**
> "The Honest Advisor podcast has 8,000 episode downloads but zero clips on short-form video -- the content is doing nothing outside Apple Podcasts."

**Email Automation:**
> "Bloom Boutique has an email signup form with 'Join 3,200 subscribers!' but there's no newsletter archive and I received nothing after signing up."

### Hook Rules
- Must reference a **specific, observable fact** (not a guess)
- Must be **verifiable** by the prospect (they can't argue with it)
- No hyperbole -- understate rather than overstate
- 1-2 sentences maximum
- Never mention the member's services in the hook -- that comes in the pitch

## Recommended Rig Logic

Use this decision tree to recommend a rig:

1. **If pain signal = no/weak web presence or SEO problems** → AEO Audit
2. **If pain signal = website gets traffic but no conversions** → Funnel Builder
3. **If pain signal = inconsistent content or dead social** → Content Strategy
4. **If pain signal = active creator with no distribution** → Content Repurposing
5. **If pain signal = email list exists but unused** → Email Automation
6. **If multiple signals exist**: recommend the rig that matches the strongest signal; note secondary opportunity

Only recommend rigs the member has configured as active in `config/lead-criteria.md`.
