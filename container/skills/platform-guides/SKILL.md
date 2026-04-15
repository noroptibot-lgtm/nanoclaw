---
name: Platform Guides
version: 1.0.0
description: Step-by-step setup instructions for the four most common email platforms: Mailchimp, ConvertKit (Kit), ActiveCampaign, and Beehiiv. Used by Email Strategist (for platform recommendations) and Sequence Writer (platform-setup-guide spawn only).
---

# Platform Guides Skill

This skill provides setup instructions for the four email platforms most commonly used by solopreneurs, freelancers, and small businesses. Each platform has different terminology, strengths, and limitations. Using the wrong feature name in a setup guide will frustrate the client.

## Platform Selection Guide

| Business Type | Recommended Platform | Why |
|--------------|---------------------|-----|
| Creator / Coach / Course | ConvertKit (Kit) | Built for creators, powerful visual automations, excellent tagging |
| Newsletter-first business | Beehiiv | Best newsletter UX, built-in growth tools, referral program |
| Complex B2B / CRM needs | ActiveCampaign | Advanced automation, conditional branches, CRM built-in |
| Simple small business / local | Mailchimp | Easiest to use, widely known, good free tier |
| E-commerce (Shopify) | Klaviyo (note: not covered here) | Klaviyo is the e-commerce standard -- refer client to Klaviyo docs |

**Important**: Always confirm the client's actual platform (from plan.md) before writing the setup guide. Use the correct feature names for their specific platform.

---

## Mailchimp

**Best for**: Small businesses, local services, beginners. Familiar interface, good free tier (up to 500 contacts).

**Key terminology**:
- **Audience**: Their contact list (one list per Mailchimp account in most setups)
- **Campaign**: A one-time email blast
- **Automation / Customer Journey**: Their automation builder
- **Tags**: Applied to contacts based on actions or manual assignment
- **Segments**: Dynamic groups based on tag criteria or behavior
- **Merge Tags**: Personalization variables (`*|FNAME|*` for first name)

### Setting Up a Welcome Sequence in Mailchimp

1. Go to **Automations → Customer Journey Builder**
2. Click **"Create from scratch"** (or start with the "Welcome new subscriber" starting point)
3. Set **starting point**: "Contact is added to audience" (or "Contact subscribes to a group" if you use groups)
4. Add **Journey Point → Send email** for each email in the sequence
5. Add **Journey Point → Wait** between each email (set the delay in days/hours)
6. Configure each email:
   - Subject line
   - Preview text: Click the send settings gear → "Preview text"
   - Email body in the drag-and-drop editor
7. Set **filters** if needed (e.g., "Only people who subscribed via [form name]")
8. **Review and publish** the Journey

**Personalization in Mailchimp**:
- First name: `*|FNAME|*`
- Email address: `*|EMAIL|*`
- Date: `*|DATE:d F Y|*`
- Custom merge field: Create in Audience → Manage contacts → Required email fields, then use `*|MMERGE3|*` (or whatever field number)

### Setting Up Tags in Mailchimp

1. Tags can be applied manually: **Contacts → Manage contacts → Tags**
2. Apply tags via automation: In Customer Journey, add a "Journey Point → Add/remove tag"
3. Tags appear on individual contact profiles
4. Create segments based on tags: **Audience → Segments → Create segment** → filter by "Tag is [tag name]"

### Mailchimp Limitations to Note

- One Audience per account (on lower-tier plans) -- all contacts are in one list
- Automation builder is less visual/powerful than ConvertKit or ActiveCampaign
- Conditional branching requires higher-tier plans
- Free tier is limited to 500 contacts and 1,000 sends/month
- Rebranded some features -- "Automation" is now "Customer Journeys"

---

## ConvertKit (Kit)

**Best for**: Creators, coaches, course sellers, bloggers. Most powerful visual automation at the creator price point. Excellent tag-based segmentation.

**Key terminology**:
- **Subscribers**: Their contact list
- **Tags**: Applied to subscribers; the primary segmentation tool
- **Segments**: Saved filter groups based on tag criteria
- **Sequences**: A linear series of emails (drip sequence, like a welcome or nurture)
- **Automations**: Visual workflow builder (triggers → actions → conditions → wait periods)
- **Broadcasts**: One-time email sends to segments
- **Forms / Landing pages**: Opt-in forms and standalone pages
- **Personalization**: `{{ subscriber.first_name }}`

### The Difference: Sequences vs. Automations

This is the most important ConvertKit distinction:

**Sequences** = Linear drip emails. Best for welcome sequences and nurture sequences.
- Set up at: **Automate → Sequences**
- Emails are added in order, with delay settings between them
- Subscribers move through them in order, one email at a time

**Automations** = Visual workflows with branches and conditions. Best for complex logic.
- Set up at: **Automate → Visual Automations**
- Drag-and-drop workflow builder
- Can trigger sequences, apply tags, send individual emails, add wait periods

**For most use cases**: Use Sequences for linear drips (welcome, nurture), use Automations to trigger those sequences and apply tags.

### Setting Up a Welcome Sequence in ConvertKit

1. Go to **Automate → Sequences**
2. Click **"New sequence"** and name it (e.g., "Welcome - [Client Name]")
3. Add each email:
   - Subject line
   - Email body
   - Set delay from previous email (click the clock icon)
4. Email 1 is typically "Send immediately" (0 day delay)
5. Set emails to **"Publish"** (draft = not sent)

**Connecting the sequence to a form (trigger)**:
1. Go to **Automate → Visual Automations**
2. Create new automation
3. Trigger: **"Subscribes to a form"** (choose the signup form)
4. Action: **"Subscribe to sequence"** (choose your welcome sequence)
5. Optional: Add **"Add tag"** action to track acquisition source

### Setting Up Tags and Automations in ConvertKit

**Link triggers** (apply tag when subscriber clicks a link):
1. In any email body, highlight a link
2. Click the link settings
3. Enable "Add tag when clicked" → choose or create a tag
4. This applies the tag when the subscriber clicks that specific link

**Automation branches**:
1. In Visual Automations, add a **"Condition"** step
2. Set the condition: "Has tag → [tag name]" = Yes/No
3. Each branch gets its own set of actions

### ConvertKit Personalization

- First name: `{{ subscriber.first_name }}`
- Email: `{{ subscriber.email_address }}`
- Custom field: `{{ subscriber.fields.field_name }}`
- Fallback value: `{{ subscriber.first_name | default: "friend" }}` (shows "friend" if no name)

### ConvertKit Limitations

- Not ideal for complex conditional branching at creator tier (upgrade required)
- Less suited for B2B or e-commerce with complex CRM needs
- Automation workflows can get complex to manage at scale
- Rebranded to "Kit" in 2024 -- interface may show either name

---

## ActiveCampaign

**Best for**: B2B, professional services, businesses with complex sales cycles, or those needing CRM functionality alongside email.

**Key terminology**:
- **Contacts**: Their list
- **Tags**: Applied to contacts; primary segmentation tool
- **Lists**: Can segment contacts into different lists (vs. ConvertKit's one list)
- **Automations**: Their workflow builder -- very powerful
- **Campaigns**: One-time email sends
- **Deals / CRM**: Sales pipeline (built-in CRM)
- **Site Tracking**: Tracks what pages contacts visit
- **Custom Fields**: Additional data about contacts
- **Personalization**: `%FIRSTNAME%`

### ActiveCampaign Automation Builder

ActiveCampaign's automation builder is the most powerful of the four platforms covered here. It supports:
- Multiple triggers per automation
- Conditions and branching (if/else logic)
- Goal-based exits (subscriber achieves goal → jump to specific step or exit)
- Wait steps (time-based or "wait until condition is met")
- Webhooks and integrations
- CRM pipeline actions (create deal, move deal stage)

### Setting Up a Welcome Sequence in ActiveCampaign

1. Go to **Automations → New automation**
2. Choose **"Start from scratch"** or use the "Welcome new contact" template
3. Set trigger: **"Subscribes to list"** or **"Submits a form"** (more precise)
4. Add **"Send email"** action for Email 1 (create/select the email)
5. Add **"Wait"** action → specify delay (e.g., "Wait 1 day")
6. Repeat for each email in the sequence
7. Optionally add:
   - **"If/Else"** after each email to branch based on behavior
   - **"Goal"** -- if contact makes a purchase, skip to a different step
   - **"Apply tag"** -- add tags based on where they are in the sequence
8. **Set automation to "Active"** when ready

### Setting Up Goal-Based Exits

This is a key ActiveCampaign differentiator:
1. In an automation, add a **"Goal"** step at any point
2. Set the condition: e.g., "Contact has tag: purchased"
3. This means: if the subscriber achieves this condition at any point during the automation, they skip to the goal step
4. Use this to prevent nurture emails from going to people who already bought

### ActiveCampaign Personalization

- First name: `%FIRSTNAME%`
- Last name: `%LASTNAME%`
- Email: `%EMAIL%`
- Custom field: `%CUSTOM_FIELD_NAME%`
- Fallback: Set in the personalization settings for each field

### ActiveCampaign Limitations

- Steeper learning curve than Mailchimp or ConvertKit
- Higher price point ($15-29/mo for basic, more for CRM features)
- Can be overkill for simple creator/solopreneur use cases
- Interface can feel dense/complex for beginners

---

## Beehiiv

**Best for**: Newsletter-first businesses, creators who publish a regular newsletter and want audience growth tools. NOT ideal as a primary automation platform for complex sequences.

**Key terminology**:
- **Subscribers**: Their reader list
- **Newsletters**: Individual issues (both web and email)
- **Segments**: Groups of subscribers based on criteria
- **Automations**: Limited compared to other platforms -- basic welcome and re-engagement
- **Referral Program**: Built-in referral system (subscribers refer others, get rewards)
- **Boosts**: Paid subscriber acquisition via other Beehiiv newsletters
- **Web3 Features**: Optional token gating and NFT perks (advanced)

### What Beehiiv Does Well

- Beautiful newsletter publishing experience (web + email in one)
- Built-in subscriber analytics (open rates, click rates, subscriber growth)
- Referral program is the best in class for newsletter growth
- Archive/web version looks professional automatically
- Growth tools (Boosts, referrals) are unique to Beehiiv

### What Beehiiv Does NOT Do Well

- Complex automation sequences (welcome sequence is limited to basic drip on paid plans)
- Advanced segmentation and conditional branching
- If the client needs a 7-email welcome sequence with tag-based triggers, Beehiiv alone may not suffice
- No CRM functionality

### Setting Up Automation in Beehiiv (Scale Plan Required)

Basic automations available on Scale plan ($42/mo+):
1. Go to **Automations** in dashboard
2. Available automation types: Welcome email series, custom event triggers
3. For welcome sequence: Set up a multi-step welcome drip (limited to simpler logic)
4. Delays between emails: Set in days

**Beehiiv + ConvertKit pairing**: Some newsletter operators use Beehiiv for the newsletter experience and distribution, while using ConvertKit for automation and sequences. The platforms integrate via API or Zapier.

### Beehiiv Setup Steps

1. **Account setup**: Business name, publication name, sender address
2. **Connect domain**: For deliverability, connect a custom sending domain
3. **Create signup form**: Embedded on website or standalone Beehiiv page
4. **Enable referral program** (optional but recommended): Go to Grow → Referral Program
5. **Write and schedule first issue**: Content → New Post → write in their editor
6. **Automation** (Scale plan): Automations → New automation → welcome series

---

## Platform-Agnostic Setup Checklist

Regardless of platform, every email setup should include:

### 1. Sender Authentication (Deliverability)
- **SPF record**: DNS record that authorizes your platform to send from your domain
- **DKIM record**: Cryptographic signature that verifies email authenticity
- **DMARC record**: Policy for how to handle emails that fail SPF/DKIM

Each platform provides the exact DNS records to add. This takes 15-30 minutes but significantly improves deliverability.

Most platforms guide you through this in Settings → Domains or Settings → Sending domains.

### 2. Physical Address
Legal requirement (CAN-SPAM). Add a real mailing address or a PO box in:
- Settings → From information or
- Email footer template

### 3. Unsubscribe Link
Handled automatically by all four platforms -- it's in every email footer by default. Do not remove it.

### 4. Test Email Before Activating
Send yourself a test of every automation email before making it live. Check:
- Subject line and preview text render correctly
- Personalization fields populate (`*|FNAME|*` should show a name, not the code)
- Links work
- CTA buttons are clickable
- Email looks correct on mobile (most platforms have a mobile preview)

### 5. Signup Form Integration
Connect the email platform to the website:
- Use the platform's native embed code, OR
- Integrate via Zapier/Make if using a different form tool
- Test the form: submit a test signup and verify you receive the welcome email

### 6. Activate Automations Last
Set up all sequences and campaigns in draft first. Activate all automations only after testing. Activating a welcome sequence with a broken link on day 1 means every new subscriber sees the error.
