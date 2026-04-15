---
name: seo-audit
description: 7-Day SEO Action Plan audit framework covering website speed, title tags, meta descriptions, image optimization, SSL, mobile, design, and backlink building. Use when user wants to audit a website for SEO, fix technical SEO issues, optimize page speed, write title tags or meta descriptions, optimize images, build backlinks, or run a full SEO checklist.
license: MIT
metadata:
  version: 1.0.0
  category: seo
  domain: technical-seo
  updated: 2026-03-12
---

# SEO Audit Skill

Complete website SEO audit framework based on the 7-Day SEO Action Plan. Covers technical SEO, on-page optimization, image SEO, and site health.

## Keywords
SEO audit, website audit, page speed, title tags, meta descriptions, image optimization, alt tags, SSL, mobile optimization, technical SEO, Core Web Vitals, GTMetrix, PageSpeed Insights, SEO checklist

---

## Day 2 — Website Speed Audit

### Tools
- **Google PageSpeed Insights** — free speed + Core Web Vitals test
- **GTMetrix** — detailed waterfall, loading time, TTFB
- **SEO Wallet Chrome Extension** — on-page SEO overview

### Common Issues to Fix
| Issue | Fix |
|-------|-----|
| Oversized images | Convert to WebP, compress with TinyPNG |
| Bloated plugins | Deactivate unused plugins, lazy-load |
| Slow scripts | Defer/async JS, remove render-blocking resources |
| No caching | Enable browser caching, use CDN |

### Audit Process
1. Run URL through PageSpeed Insights → note scores for Mobile & Desktop
2. Run URL through GTMetrix → check waterfall for bottlenecks
3. Fix largest issues first (images → scripts → plugins)
4. Re-test to confirm improvement

### Organize with Checklist
Use the SEO Checklist Audit Google Sheet to track issues and fixes per page.

---

## Day 3 — Title Tags & Meta Descriptions

### What They Are
- **Title tag** = SEO headline shown in Google results (≤60 chars)
- **Meta description** = Digital sales pitch below the title (≤160 chars)

### Best Practices
| Element | Rule |
|---------|------|
| Title tag | Include primary keyword near the start, ≤60 chars |
| Meta description | Include keyword, CTA, benefit, ≤160 chars |
| Uniqueness | Every page must have a unique title + description |
| Avoid | Keyword stuffing, duplicate tags, truncation |

### Google Apps Script (Bulk Audit in Google Sheets)

Add Cheerio library first:
```
Library ID: 1ReeQ6WO8kKNxoaA_O0XEQ589cIrRvEBA9qcWpNqdOP17i47u6N9M5Xh0
```

```javascript
/**
 * Get page title from URL
 * @param {"https://example.com"} url
 * @return {string}
 * @customfunction
 */
function getPageTitle(url) {
  if (!url || !url.includes("http")) return "Error: Invalid URL";
  try {
    const fetch = UrlFetchApp.fetch(url, { muteHttpExceptions: true, followRedirects: false });
    if (fetch.getResponseCode() === 200) {
      const $ = Cheerio.load(fetch.getContentText());
      return $("title").text().trim();
    }
    return "Error: Cannot access URL";
  } catch (err) {
    return "Error: Cannot scrape URL";
  }
}

/**
 * Get title character count
 * @param {"https://example.com"} url
 * @return {number}
 * @customfunction
 */
function getPageTitleCharCount(url) {
  const title = getPageTitle(url);
  return title.startsWith("Error:") ? 0 : title.length;
}

/**
 * Get meta description from URL
 * @param {"https://example.com"} url
 * @return {string}
 * @customfunction
 */
function getMetaDescription(url) {
  if (!url || !url.includes("http")) return "Error: Invalid URL";
  try {
    const fetch = UrlFetchApp.fetch(url, { muteHttpExceptions: true, followRedirects: false });
    if (fetch.getResponseCode() === 200) {
      const $ = Cheerio.load(fetch.getContentText());
      return $("meta[name='description']").attr("content") || "";
    }
    return "Error: Cannot access URL";
  } catch (err) {
    return "Error: Cannot scrape URL";
  }
}

/**
 * Get meta description character count
 * @param {"https://example.com"} url
 * @return {number}
 * @customfunction
 */
function getMetaDescriptionCharCount(url) {
  const description = getMetaDescription(url);
  return description.startsWith("Error:") ? 0 : description.length;
}
```

### Audit Workflow
1. List all URLs in column A of Google Sheet
2. Use `=getPageTitle(A2)` and `=getMetaDescription(A2)` to bulk-fetch
3. Use `=getPageTitleCharCount(A2)` to flag titles >60 chars
4. Use `=getMetaDescriptionCharCount(A2)` to flag descriptions >160 chars
5. Rewrite flagged pages, prioritize high-traffic URLs first

---

## Day 4 — Image Optimization

### Why It Matters
- Large images = slow load = lower rankings + worse UX
- Missing alt tags = lost accessibility + missed keyword signals

### Format Priority
1. **WebP** — best compression + quality (always preferred)
2. **PNG** → convert to WebP
3. **JPEG** → convert to WebP

### Tools
- **TinyPNG** — compress PNG/JPEG without quality loss
- **PNG to WebP Converter** — batch format conversion
- **GTMetrix / PageSpeed** — identify heaviest images
- **SEO Wallet plugin** — audit alt tags across site

### Image SEO Checklist
- [ ] All images in WebP format
- [ ] File size <100KB where possible
- [ ] Descriptive file name (e.g. `haandverker-oslo.webp`, not `IMG_1234.webp`)
- [ ] Alt tag on every image — descriptive, keyword-relevant
- [ ] Image title set
- [ ] No images used for text (use real HTML text instead)
- [ ] Lazy loading enabled for below-the-fold images

### Alt Tag Formula
```
[What is shown] + [context/keyword if natural]
Example: "elektriker sjekker sikringsskap i Oslo leilighet"
```

---

## Day 5 — Final Audit: SSL, Design, Mobile & Typography

### SSL & Security
- [ ] Site uses HTTPS (padlock in browser)
- [ ] No mixed content warnings (HTTP resources on HTTPS page)
- [ ] SSL certificate valid and not expired
- Tool: **SSL Checker**

> Missing SSL = Google flags site as "not secure" → major trust + ranking loss

### Design & Conversion Checklist
- [ ] Clear headline above the fold (what you do + who for)
- [ ] Prominent CTA button visible without scrolling
- [ ] Trust signals present: reviews, logos, certifications
- [ ] No cluttered layout or confusing navigation
- [ ] Consistent branding (colors, fonts, logo)
- [ ] Contact info easy to find

### Mobile Optimization
- [ ] Site passes Google Mobile-Friendly Test
- [ ] Buttons large enough to tap (≥44px)
- [ ] No horizontal scrolling
- [ ] Text readable without zooming
- Tool: **Mobile Simulator Chrome Extension**

### Typography & Readability
- [ ] Body font ≥16px
- [ ] Line height 1.5–1.8
- [ ] Max line width ~70 characters
- [ ] High contrast text on background
- [ ] Headings create clear visual hierarchy (H1 → H2 → H3)

---

## Full SEO Audit Checklist Summary

### Technical
- [ ] PageSpeed score >80 Mobile, >90 Desktop
- [ ] HTTPS enabled, no mixed content
- [ ] No broken links (404s)
- [ ] XML sitemap submitted to Google Search Console
- [ ] robots.txt configured correctly
- [ ] Core Web Vitals passing (LCP, CLS, FID)

### On-Page
- [ ] Unique title tag per page (≤60 chars, keyword near start)
- [ ] Unique meta description per page (≤160 chars, includes CTA)
- [ ] One H1 per page with primary keyword
- [ ] Proper heading hierarchy (H1 → H2 → H3)
- [ ] Internal linking between related pages
- [ ] Primary keyword in first 100 words

### Images
- [ ] WebP format
- [ ] Compressed <100KB
- [ ] Descriptive alt tags
- [ ] Descriptive file names

### Mobile & UX
- [ ] Mobile-friendly layout
- [ ] Fast load on 3G/4G
- [ ] Clear CTAs
- [ ] Trust signals visible

---

---

## Day 6 — Backlink Building

### Hva er backlinks og hvorfor de er viktige
Backlinks = andre nettsider som lenker til deg. Google tolker dette som stemmer — jo flere kvalitetslenker, desto høyere autoritet og rangering.

### Typer backlinks

| Type | Beskrivelse | Kvalitet |
|------|-------------|---------|
| **Organisk** | Andre linker til deg fordi innholdet er bra | Høyest |
| **Guest post** | Du skriver artikkel på en annen nettside, får lenke | Høy |
| **Outreach** | Du kontakter nettsider og ber om lenke | Middels-høy |
| **Submission sites** | Gratis kataloger og bloggnettverk | Lav-middels |
| **Kjøpte lenker** | Betaler for plassering | Risikabelt (Google-straff) |

### Strategi: Rask start med submission sites
Gratis nettsteder der du kan laste opp innhold med lenke tilbake til ditt nettsted:
- **Blog Uploading Website** — last opp bloggartikler med dofollow-lenker
- Finn bransjerelevante kataloger og submit nettstedet ditt

### Strategi: Outreach (mest effektivt over tid)
1. Finn nettsider i din nisje med god autoritet
2. Skriv personlig e-post — forklar verdien din innhold gir deres lesere
3. Tilby guest post eller be om lenke til relevant innhold
4. Følg opp én gang etter 5–7 dager

### Strategi: Betalt lenkebygging (tjenester)
| Tjeneste | Beskrivelse |
|----------|-------------|
| **Get Me Links** | Backlink-byrå, 10% rabatt tilgjengelig |
| **The Hoth** | SEO-byrå med link building-pakker |
| **Rhino Rank** | Niche-relevante guest posts og lenker |

> Bruk betalte tjenester med forsiktighet — kun på nettsider med høy domenautoritet og relevant innhold.

### Strategi: Innhold som tiltrekker lenker (long-term)
Innholdstyper som naturlig får backlinks:
- Statistikk og datadrevne artikler
- Ultimate guides / komplette veiledninger
- Verktøy, kalkulatorer, sjekklister
- Originale undersøkelser eller case studies

### Backlink Checklist
- [ ] Nettstedet er listet i relevante bransjekataloger
- [ ] Minst 1–2 guest posts publisert per måned
- [ ] Outreach-kampanje i gang (5–10 kontakter/uke)
- [ ] Innhold av høy verdi publisert (guide, statistikk, verktøy)
- [ ] Sjekk backlink-profil månedlig (Google Search Console → Lenker)
- [ ] Ingen kjøpte lenker fra lavkvalitets-nettsteder

---

## Tools Reference

| Tool | Purpose |
|------|---------|
| Google PageSpeed Insights | Speed + Core Web Vitals |
| GTMetrix | Detailed load analysis |
| SEO Wallet Chrome Extension | On-page SEO overview |
| TinyPNG | Image compression |
| PNG to WebP Converter | Format conversion |
| SSL Checker | HTTPS validation |
| Mobile Simulator Chrome Extension | Mobile layout preview |
| Google Search Console | Rankings, indexing, errors |
| SEO Checklist Audit Google Sheet | Organize audit findings |
| Meta Description Optimiser GPT | AI-assisted meta writing |
