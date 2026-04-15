---
name: Email Marketing
version: 1.0.0
description: Comprehensive email marketing methodology including sequences, automation, deliverability, segmentation, and ROI frameworks. Used by Business Researcher, Email Strategist, and Sequence Writer.
---

# Email Marketing Skill

This skill provides the methodology for designing and evaluating email marketing systems. Email remains the highest-ROI digital marketing channel -- average return is $36-42 for every $1 spent. But only when you actually send the emails, and only when the emails are structured correctly.

## The Core Problem This Rig Solves

Most small businesses and creators fall into one of three failure modes:

1. **The empty list**: They collect email signups but never send anything. The list goes cold. Every month that passes, it gets harder to restart.
2. **The spray-and-pray**: They send occasional emails but with no strategy. No sequences. No segmentation. No automation. Just random blasts when they remember.
3. **The generic sequences**: They set up a 3-email welcome sequence they copied from a template. It's not specific to their business, their voice, or their audience's journey.

A well-built email system solves all three.

---

## Email Sequence Types

### Welcome Sequence (5-7 emails, 14 days)

**Purpose**: Orient new subscribers, deliver on the signup promise, introduce the brand, and set expectations for the relationship.

**When triggered**: Immediately on signup or lead magnet download.

**Arc pattern**:
- Email 1 (Day 0): Deliver immediately. If they signed up for a guide, send the guide. No delays, no "coming soon."
- Email 2 (Day 1): Quick value. A tip, insight, or resource that makes them glad they subscribed.
- Email 3 (Day 3): Story. Your own journey, a case study, or a transformation story that builds credibility.
- Email 4 (Day 5): Address the #1 objection or fear your audience has about your product/service.
- Email 5 (Day 7): Soft offer introduction. "Here's how I help people like you."
- Email 6-7 (Day 10, 14, optional): Social proof / FAQ / clear offer.

**Success metrics**:
- Open rate: 40-60% (welcome emails are the most opened emails in any sequence)
- Click rate: 5-15%
- Unsubscribe rate: <0.5%

**Common mistake**: Starting with a long "about me" email. Nobody cares about your story until they've gotten value from you first.

### Nurture Sequence (8-12 emails, 45-60 days)

**Purpose**: Build trust over time, establish authority, and move subscribers toward a purchase without pressure.

**When triggered**: After completing the welcome sequence (or after 14 days if no explicit trigger).

**Arc pattern** (value escalation):
- Emails 1-3: Pure value. Teach something useful. Give away your best insights. Zero selling.
- Emails 4-6: Proof and social validation. Case studies, testimonials, specific results. Still low selling.
- Emails 7-9: Bridge emails. Connect their problem directly to your solution. Frame, don't pitch.
- Emails 10-12: Soft and direct offer. They've earned this pitch. Make it clear and specific.

**Key principle**: The nurture sequence is not a series of 12 random tips. It has an arc -- it takes the subscriber from "interested" to "ready to buy." Each email should move them one step closer.

**Success metrics**:
- Open rate: 20-35% (drops from welcome but should stabilize)
- Click rate: 2-5%

### Re-engagement Sequence (3-4 emails, 10 days)

**Purpose**: Reactivate inactive subscribers or get a clean unsubscribe.

**When triggered**: 30 days of no opens or clicks.

**Arc pattern**:
- Email 1: Warm re-connection. "We've missed you." Low pressure. Remind them why they signed up.
- Email 2: Give away value. "Here's something you might have missed." Make re-engaging feel rewarding.
- Email 3: Honest question. "Should we part ways?" Respectful. Give them an easy yes or no.
- Email 4 (optional): Final goodbye with auto-unsubscribe link.

**Why clean your list?**: Inactive subscribers hurt your deliverability. ISPs watch engagement rates. A list of 10,000 with 20% open rate performs better than 50,000 with 4% open rate. Smaller, engaged lists generate more revenue.

**Tone rules**: No fake urgency. No guilt. No desperation. Inactive subscribers aren't bad people -- they're busy. Treat them like adults.

### Promotional Campaigns

**Launch Campaign (3-5 emails, 5-7 days)**:
Used for new product/service launches, course launches, or major announcements.
- Announcement email → Social proof → Objection handling → Urgency reminder → Last chance
- Real deadlines only. If you say Friday, the offer ends Friday.

**Flash Sale Campaign (3-4 emails, 24-72 hours)**:
Time-limited discount or offer.
- Sale opens → Reminder + proof → Ending soon → Last hours (optional)
- Urgency must be honest. Fake countdown timers train subscribers to ignore urgency forever.

**Seasonal Campaign (3-5 emails)**:
Holiday or seasonal promotions tied to relevant events for the business.
- Works best when the seasonal connection is genuine (a fitness coach doing a January "fresh start" campaign makes sense; a B2B SaaS doing a Valentine's Day sale is awkward)

---

## Subscriber Lifecycle Stages

| Stage | Definition | Primary Sequence | Goal |
|-------|-----------|-----------------|------|
| **New** | Just subscribed, first 14 days | Welcome | Orient + first value |
| **Engaged Lead** | Completed welcome, opens regularly | Nurture | Build trust + drive purchase |
| **Customer** | Has purchased at least once | Post-purchase or ongoing newsletter | Retention + upsell |
| **Lapsed Customer** | Purchased but inactive 60+ days | Win-back campaign | Reactivate |
| **Inactive Subscriber** | 30+ days no engagement | Re-engagement | Reactivate or clean |
| **Churned** | Unsubscribed or hard bounce | [None] | Clean the list |

---

## Segmentation Methodology

### Why Segment

Sending the same email to everyone is leaving money on the table. A subscriber who just bought your $97 course should not get your "introductory offer" email. A subscriber who's been on your list for 3 years should not get the same nurture sequence as a new subscriber.

### Tag-Based Segmentation

Tags are applied to individual contacts based on behavior. They're flexible and additive -- a contact can have many tags.

**Acquisition tags** (how they joined):
- `source-lead-magnet-name` -- specific to the magnet they used
- `source-webinar`, `source-checkout-upsell`, `source-social-bio`, etc.
- Why: Different acquisition sources have different intent levels. Webinar leads are warm. Bio link leads are cold.

**Interest tags** (what they engaged with):
- `interest-product-category-name` -- based on link clicks
- `clicked-pricing-page`, `clicked-about-page`, etc.
- Why: Reveals intent before purchase. Someone who clicked pricing is closer to buying.

**Behavioral tags** (what they've done):
- `purchased`, `purchased-2x`, `vip-customer`
- `completed-welcome`, `completed-nurture`
- `inactive-30`, `inactive-60`
- Why: Enables automation -- apply tag → trigger next sequence

### Segment-Based Campaigns

Segments are dynamic groups built from combinations of tags. Common segments:
- **Active leads**: subscribed + no `purchased` tag + opened in 30 days
- **Warm buyers**: `purchased` + not `vip`
- **VIP customers**: `purchased-2x` or high spend threshold
- **Inactive leads**: subscribed + no `purchased` + `inactive-30`
- **Re-engagement candidates**: `inactive-30` + no `inactive-60`

---

## Automation Fundamentals

### Trigger Types

- **Form submission**: Someone fills out a signup form → welcome sequence begins
- **Tag applied**: When tag `inactive-30` is applied → re-engagement sequence begins
- **Link click**: Someone clicks a specific link → apply interest tag
- **Date-based**: 30 days after purchase → post-purchase upsell email
- **Purchase event** (via integration): Checkout complete → apply `purchased` tag, exit nurture sequence, trigger post-purchase

### Goal-Based Exits

In a nurture sequence, you don't want someone to receive a "you should consider buying X" email after they've already bought X. Set goal-based exits:
- If contact achieves goal (makes purchase, applies tag) → exit current sequence, enter next appropriate sequence

### Conditional Branches

More advanced automation:
- If they clicked yes on re-engagement → remove `inactive-30` tag, add to active segment
- If they didn't open the last 3 emails → escalate re-engagement

---

## Deliverability Basics

### Why Deliverability Matters

If your emails don't reach the inbox, nothing else matters. Deliverability is the unsexy foundation of email marketing.

**The three main threats**:
1. **Spam filters**: Triggered by spam words, suspicious content, or poor sender reputation
2. **Low engagement**: ISPs (Gmail, Outlook) watch open rates. Low engagement = more spam folder routing
3. **Hard bounces**: Invalid email addresses damage your sender reputation

**What members should do**:
- Set up SPF and DKIM records (most email platforms guide you through this)
- Clean the list regularly (re-engagement sequences + removing hard bounces)
- Don't buy email lists (illegal in many jurisdictions, destroys deliverability)
- Warm up new sender domains slowly (don't blast 5,000 emails on day 1)

### Legal Compliance (CAN-SPAM, GDPR)

**CAN-SPAM (US)**:
- Physical mailing address required in every email
- Clear "unsubscribe" link in every email
- Honor unsubscribe requests within 10 days
- Subject lines must not be deceptive

**GDPR (EU/UK)**:
- Need explicit consent (not pre-checked boxes)
- Double opt-in is best practice
- Must be able to show proof of consent

**Practical advice**: Every reputable email platform (Mailchimp, ConvertKit, etc.) handles unsubscribe compliance automatically. The member's job is to get explicit opt-in and include a real physical address.

---

## Email Frequency Guidelines

| Business Type | Welcome Seq | Nurture Seq | Newsletter | Notes |
|--------------|-------------|-------------|------------|-------|
| Creator / Coach | Daily or every other day | Weekly | Weekly | High personal connection expected |
| SaaS / Software | Daily for first week | Bi-weekly | Monthly | Focus on value/onboarding |
| E-commerce | Daily for 5 days | Weekly | Bi-weekly + campaigns | Product-focused, purchase-oriented |
| Local Service Business | 3 emails over 2 weeks | Monthly or event-based | Monthly | Lower tolerance for email frequency |
| B2B / Professional Services | 3-5 emails over 2 weeks | Bi-weekly | Monthly | Professional context, high tolerance for value |

---

## ROI Framing for Sales Conversations

When a member is pitching email services, these numbers help:

- Average email ROI: $36-42 per $1 spent (DMA research)
- A list of 1,000 subscribers generating $1/subscriber/month = $1,000/month recurring from email alone
- Welcome sequence open rates: 40-60% (vs. 20-25% for regular broadcasts)
- Welcome sequence click rates: 5-15%

**Revenue calculation for a prospect**:
If they have [X] subscribers and you get them to a $1/subscriber/month result:
- 500 subscribers → $500/mo additional revenue
- 2,000 subscribers → $2,000/mo additional revenue
- 10,000 subscribers → $10,000/mo additional revenue

This math is conservative. Well-built systems generate $3-5/subscriber/month in some niches.

---

## Email Audit Methodology

When researching a prospect, look for these signals:

**Green flags** (they have something to work with):
- Email signup form exists on the website
- Lead magnet or opt-in incentive visible
- Newsletter archive exists (means they've been building a list)
- Some automation indicated (post-signup confirmation page mentions "you'll receive...")

**Red flags** (sleeping asset):
- No email signup form at all
- Signup form exists but no incentive ("subscribe for updates" -- low conversion)
- Newsletter archive exists but last email was 3+ months ago
- No mention of email marketing on website or social
- Platform detected (Mailchimp badge) but no visible content

**The pitch**: Red flags ARE the sales opportunity. A sleeping asset is more valuable than an absent list because the list already exists.

---

## Anti-Patterns (What Breaks Email Systems)

| Anti-Pattern | Why It Fails | Better Approach |
|-------------|-------------|----------------|
| Sending from personal Gmail | Terrible deliverability, no automation | Use an email platform (Mailchimp, ConvertKit, etc.) |
| No welcome sequence | Missed window -- new subscribers are most engaged in first 24 hours | Build a 5-7 email welcome sequence |
| Welcome sequence = 1 email | One email is not a sequence; subscribers forget you | Minimum 5 emails over 14 days |
| Batch-and-blast only | Requires constant effort, no compounding | Build automation sequences that run forever |
| Same email to everyone | Irrelevant emails create disengagement and unsubscribes | Basic segmentation by lifecycle stage |
| No re-engagement | List bloat, deliverability decay, wasted spend | 30-day re-engagement trigger |
| Fake urgency ("LAST CHANCE!" every week) | Trains subscribers to ignore urgency | Real deadlines, used sparingly |
| Subject lines in ALL CAPS | Spam filter trigger + aggressive tone | Standard capitalization |
| Buying email lists | Terrible deliverability, likely illegal, zero ROI | Organic list building only |
