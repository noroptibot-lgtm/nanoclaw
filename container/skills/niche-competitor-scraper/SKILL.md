---
name: niche-competitor-scraper
description: Find competitors in any niche running Meta ads, scrape their ads via Apify, create dedicated Airtable tables with Competitor + Ad Research linked, classify ads, and mark top performers. Use when user wants to research a new niche/vertical's ad landscape.
---

# Niche Competitor Ad Scraper

End-to-end pipeline: find competitors in a specific niche who run Meta ads → scrape all their ads → push to dedicated Airtable tables → classify → mark top performers.

## When to use
- User wants to research competitors in a new niche (e.g., "finn varmepumpe konkurrenter", "find web design agencies running ads")
- User provides example companies/URLs and wants a full competitive ad database
- User says "finn konkurrenter" or "scrape ads" for a specific industry

## What you produce
1. **Competitors table** in Airtable with all companies, Facebook Page IDs, Ad Library URLs
2. **Ad Research table** linked to competitors with every active ad: copy, media, previews, classifications
3. **Top Performers** marked (longest-running ads = highest impressions)

---

## Step 1: Identify the Niche & Airtable Location

Ask/determine:
- What niche? (e.g., "nettsider", "varmepumpe service", "flyttebyrå")
- Which Airtable base? (check `appLs3xasebZJTvEp` or ask)
- Existing table to use, or create new?
- Which countries to search? (NO, SE, DK, GB, US, etc.)

## Step 2: Find Competitors via Ad Library Search

Search Facebook Ad Library for companies running ads in the niche:

```bash
curl -s -X POST "https://api.apify.com/v2/acts/curious_coder~facebook-ads-library-scraper/run-sync-get-dataset-items?token={TOKEN}&timeout=300" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      {"url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={COUNTRY}&media_type=all&search_type=keyword_unordered&q={KEYWORDS}"}
    ],
    "maxItems": 200
  }'
```

**CRITICAL:** Only include companies that actually appear in Ad Library with active ads. Never add a competitor without verifying they have ads.

**Multiple keyword searches:** Run 5-8 different keyword combinations per country to catch all players. Example for "nettside" niche in Norway:
- `nettside bedrift webdesign`
- `gratis mockup nettside`
- `hjemmeside lage design firma`
- `webutvikling nettbutikk webside`

Group results by page, sort by ad count. Companies with most ads = most serious advertisers.

## Step 3: Get Facebook Page IDs via Apify

For each competitor found, scrape their Facebook page to get the **Ad Library ID** (NOT profile ID):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/apify~facebook-pages-scraper/run-sync-get-dataset-items?token={TOKEN}&timeout=180" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": [{"url": "https://www.facebook.com/profile.php?id={PAGE_ID}"}]}'
```

Extract: `pageAdLibrary.id` (this is the correct ID for Ad Library URLs).

## Step 4: Create Airtable Tables

### Competitors Table
Create with these fields:
- Name (singleLineText) — primary
- Category (singleSelect: Micro-Niche, Macro-Niche, Ad Leader)
- Niche / Industry (singleLineText)
- Description (multilineText)
- Status (singleSelect: Active, Inactive)
- Facebook Page URL (url)
- Facebook Page ID (singleLineText)
- Ad Library URL (url)
- Website (url)
- Instagram URL (url)
- Date Added (date)

### Ad Research Table
Create with Competitor field linked to the Competitors table:
- Ad Archive ID (singleLineText) — dedup key
- Page Name (singleLineText)
- Page ID (singleLineText)
- Competitor (multipleRecordLinks → Competitors table)
- Ad Library URL (url)
- Start Date (date)
- Is Active (checkbox)
- Platforms (multipleSelects: Facebook, Instagram, Messenger, Audience Network)
- Display Format (singleSelect: Video, Image, Carousel, DCO)
- Body Text (multilineText)
- Title (singleLineText)
- CTA Text (singleLineText)
- Link URL (url)
- Video URL (url)
- Image URL (url)
- Angle Category (singleSelect)
- Ad Format Type (singleSelect)
- Scrape Date (date)
- Scrape Batch ID (singleLineText)
- Preview (multipleAttachments)
- Top Performer (checkbox)

## Step 5: Populate Competitors

Insert all found competitors with:
- Correct Ad Library URLs: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={COUNTRY}&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id={AD_LIB_ID}`
- Category classification (Micro-Niche for direct competitors, Ad Leader for best advertisers)
- Description noting ad count and key messaging angles

## Step 6: Scrape All Ads

For each competitor, scrape via Apify sorted by impressions:

```bash
curl -s -X POST "https://api.apify.com/v2/acts/curious_coder~facebook-ads-library-scraper/run-sync-get-dataset-items?token={TOKEN}&timeout=600" \
  -d '{"urls": [{"url": "...view_all_page_id={ID}"}], "maxItems": 500}'
```

Batch competitors by country (NO, SE, DK, etc.) to optimize scraping.

## Step 7: Transform & Push to Airtable

For each ad:
- Convert start_date from unix timestamp
- Map platforms (filter out "THREADS" — not a valid Airtable select option)
- Extract video/image URLs and preview thumbnails
- Build Ad Library URL: `https://www.facebook.com/ads/library/?id={archive_id}`
- Link to Competitor record

Insert in batches of 10.

## Step 8: Quality Check — CRITICAL

After inserting, audit ALL ads:
- **Remove ads not relevant to the niche.** Example: if niche is "web design", remove coaching/consulting ads from companies that also sell websites.
- **Check by Page Name** — review sample body text per competitor
- **Delete template/empty ads** where Body Text = `{{product.brand}}` AND no meaningful link

## Step 9: Classify Ads

For every ad, classify:

**Angle Category:** Social Proof, Pain-to-Transformation, Tips/Education, Growth Problem, Profit Problem, Authority, Scarcity/Urgency, Behind-the-Scenes

**Ad Format Type:** UGC Testimonial, UGC Talking Head, Motion Graphics, Static Image, Screenshot/UI Demo, Other

## Step 10: Mark Top Performers

Sort by Start Date ascending (oldest = most impressions). Pick top 25 with:
- Max 3 per competitor
- Unique copy (skip duplicates)
- Skip DCO/template ads
- Set `Top Performer = true`

## Step 11: Summary

Print:
```
=== Niche Competitor Scrape Complete ===
Table: {table_name} ({table_id})
Competitors: X
Ads scraped: X
Ads after cleanup: X
Top Performers marked: X

By competitor:
  CompanyA: X ads (XV, XI, XD)
  ...
```

---

## Key Lessons

1. **Always verify ads exist in Ad Library before adding a competitor.** No ads = don't add.
2. **Ad Library URL format matters.** Use correct country code (NO, SE, US etc.), not ALL.
3. **Jordan Lee problem:** Some companies sell multiple products. Only keep ads relevant to YOUR niche.
4. **Apify tokens rotate.** If one hits rate limit, try APIFY_API_TOKEN_2 through _5.
5. **Airtable can't create views via API.** Tell user to create Gallery/Grid views manually.
6. **Create SEPARATE Ad Research tables per niche** so Competitor links work correctly.
7. **DCO ads** (`{{product.name}}`) have no real copy — classify as "Other" format.
8. **Facebook Page ID vs Ad Library ID:** Apify `pageAdLibrary.id` is the correct one for Ad Library URLs. `pageId` is the profile ID and won't work.
