# Outreach Hooks Skill

Domain knowledge for writing the cold_email_hook field on each lead card. This is the single most valuable output of the Lead Getter Rig -- the observation that turns a contact into a conversation.

## Purpose

The hook is NOT a pitch. It is the opening observation that earns the right to pitch. It should make the prospect think: "How did they know that? And is that actually a problem?"

A good hook is:
- **Specific to this business** (couldn't be copied to any other lead)
- **Based on observable fact** (something the prospect can verify themselves)
- **Problem-forward** (implies a gap without diagnosing it fully)
- **Curiosity-creating** (leaves the door open -- "I found X, curious if you're aware of it")

## Hook Templates by Source

### Google Maps Leads
```
[Business name] has [X] Google reviews -- [competitor] in [city] has [Y]+.
When I searched "[niche] in [city]" on [Google/ChatGPT/Perplexity], [business name] didn't appear.
```

```
[Business name]'s Google Maps listing is missing [hours/photos/description] --
it's one of the first things potential customers check before calling.
```

### Website / Funnel Leads
```
[Business name]'s website gets [traffic signals] but has no way to capture visitor emails --
every visitor who doesn't call is gone forever.
```

```
I checked [business name]'s site and the homepage sends ad traffic to a page
with no offer, no lead magnet, and no email form.
```

### Social Media / Content Leads
```
[Business name] last posted on [platform] [X] days ago.
Meanwhile [competitor] is posting 5x/week and growing their audience.
```

```
[Creator/business] has [X] [YouTube/podcast] subscribers but
their [Instagram/LinkedIn/newsletter] is basically empty --
the content is reaching [Y]% of where it could.
```

### Email Automation Leads
```
[Business name] has an email signup on their site with "[X] subscribers"
but there's no newsletter archive -- that list isn't being used.
```

```
I signed up for [business name]'s email list 48 hours ago and haven't received anything.
That's a warm audience that isn't hearing from them.
```

### LinkedIn / B2B Leads
```
[Business name] has [X employees] and [Y clients] but their LinkedIn page
has [Z] followers and the last post was [month].
Decision-makers are searching for [niche] solutions and finding competitors instead.
```

## Tone Guidelines

### Do
- Write as a peer making an observation, not a salesperson pitching
- Use specific numbers: "14 reviews" not "few reviews"
- Reference the platform or tool you used: "when I searched on ChatGPT..."
- Keep it to 1-2 sentences
- End with something that implies awareness, not alarm: "curious if you're tracking this" not "this is costing you thousands"

### Don't
- Mention your services or price in the hook
- Use superlatives: "amazing opportunity", "critical problem"
- Make claims you can't back with data from the scrape
- Write more than 2 sentences -- longer hooks get skipped
- Be condescending: "your website is terrible" -- observe, don't judge

## Cross-Rig Hand-Off Note

Each lead card includes a `next_rig` field with the recommended rig. When the member runs that rig, they can paste the hook directly into the cover letter opener. The hook language is already calibrated to match each rig's outreach style:

- AEO Audit hooks lead with AI search / review data (matches the audit's AEO-first framing)
- Funnel Builder hooks lead with traffic + conversion gap (matches the "you're losing leads" angle)
- Content Strategy hooks lead with inconsistency observation (matches "I built a plan for you")
- Content Repurposing hooks lead with distribution gap (matches "here's what you're missing")
- Email Automation hooks lead with list + silence observation (matches "your list isn't working for you")
