---
name: SEO Report Structure
version: 1.0.0
description: AEO-first report structure (25-35 pages), scoring display formats, visual conventions, writing tone guidelines, action plan format, and competitor comparison table format. Used by Report Writer, Report Designer, Report Builder, and SEO Strategist agents.
---

# SEO Report Structure Skill

This skill defines the structure, formatting, scoring methodology, and writing conventions for the AEO & SEO Audit report. The report leads with AEO -- this is the differentiator that makes prospects open the email.

## Report Structure (AEO First)

The report is 25-35 pages (standard) or 15-20 pages (condensed). AEO is the lead section, not a subsection of technical SEO.

### Page Allocation (Standard 25-35 Pages)

| Section | Pages | Report File |
|---------|-------|-------------|
| Cover Page | 1 | Built by Report Builder |
| Executive Summary | 1 | Built by Report Builder |
| AEO Assessment | 6-8 | `report/aeo-assessment.md` |
| Technical SEO Audit | 8-10 | `report/technical-audit.md` |
| On-Page Content Analysis | 6-8 | `report/content-analysis.md` |
| Local SEO Scorecard | 4-6 | `report/local-seo-scorecard.md` |
| Competitor Comparison | 3-5 | `report/competitor-comparison.md` |
| Prioritized Action Plan | 2-3 | Built by Report Builder from audit-framework.md |
| Appendix | 1-2 | Built by Report Builder |

### Section Order Rationale

1. **AEO first** because it's the most novel and attention-grabbing. The prospect has likely seen SEO audits before but never an AI search readiness assessment.
2. **Technical SEO second** because it has the hardest data (PageSpeed scores, SSL grades) that builds credibility.
3. **Content analysis third** because it connects the technical to the strategic -- what the site says and how well.
4. **Local SEO fourth** because it's highly tangible for local businesses (reviews, directories, map presence).
5. **Competitor comparison fifth** because it provides context for everything above.
6. **Action plan last** because it's the "what to do about it" summary that drives the sales conversation.

## Scoring Display Formats

### Overall Score (Executive Summary)

```
OVERALL AUDIT SCORE: 47/100 (Needs Significant Work)

AI Search Readiness (AEO):  C+ (5.4/10)  ████▌░░░░░
Technical SEO:              B  (6.8/10)   ██████▊░░░
Content Quality:            C  (4.5/10)   ████▌░░░░░
Local SEO:                  B+ (7.2/10)   ███████▏░░
```

### Section Scores

Each section uses the same 1-10 scale with letter grade:

| Score | Grade | Label | Color (for HTML report) |
|-------|-------|-------|------------------------|
| 9.0-10.0 | A+ | Excellent | Green (#16a34a) |
| 8.0-8.9 | A | Very Good | Green (#22c55e) |
| 7.0-7.9 | B+ | Above Average | Light Green (#84cc16) |
| 6.0-6.9 | B | Average | Yellow (#eab308) |
| 5.0-5.9 | C+ | Below Average | Orange (#f97316) |
| 4.0-4.9 | C | Needs Work | Orange-Red (#ef4444) |
| 3.0-3.9 | D | Major Gaps | Red (#dc2626) |
| 1.0-2.9 | F | Critical | Dark Red (#991b1b) |

### Overall Score Calculation

The overall score is out of 100, calculated as a weighted average:

| Category | Weight |
|----------|--------|
| AEO Readiness | 25% |
| Technical SEO | 25% |
| Content Quality | 25% |
| Local SEO | 25% |

Overall = (AEO score + Technical score + Content score + Local score) / 4 * 10

### Sub-Category Score Display

Within each section, show sub-scores:

```
### Technical SEO: B (6.8/10)

| Category | Score | Status |
|----------|-------|--------|
| Site Speed (Mobile) | 67/100 | Needs Improvement |
| Site Speed (Desktop) | 84/100 | Good |
| Core Web Vitals | 7/10 | Above Average |
| SSL Security | A+ | Excellent |
| Meta Tags | 5/10 | Below Average |
| Heading Structure | 8/10 | Very Good |
| Schema Markup | 3/10 | Major Gaps |
| HTML Validity | 6/10 | Average |
| Crawlability | 7/10 | Above Average |
| Mobile Usability | 8/10 | Very Good |
```

## Visual Conventions for HTML Report

### Score Visualizations

**Progress bars:** Use colored bars (10 segments) to show scores visually.
```html
<!-- Example: 6.8/10 score -->
<div class="score-bar">
  <span class="filled" style="width: 68%"></span>
</div>
```

**Color coding:** Apply the color scale above to scores, headings, and visual indicators.

**Score badges:** Large, prominent badges for overall and section scores.

### Section Formatting

- **Each section starts on a new page** (CSS page-break-before)
- **Section header** includes: section title, score badge, one-line summary
- **Findings** are presented as cards or callout boxes with an icon indicating severity
- **Tables** use consistent styling (alternating row colors, bordered)
- **Recommendations** are highlighted in accent-colored boxes
- **Screenshots or examples** are referenced by description (actual screenshots not included in the audit)

### Action Item Formatting

Throughout the report, action items are highlighted:
```
💡 RECOMMENDATION: [Specific action to take]
Impact: [High / Medium / Low]
Effort: [Quick Win / Medium / High Effort]
```

In the HTML report, these are styled as callout cards.

## Writing Tone and Style

### Executive Summary Tone

- **Non-technical.** A business owner with no marketing background should understand every sentence.
- **Opportunity-framed.** "Your site has significant room to improve AI search visibility" not "Your site fails at AEO."
- **Specific.** "Your mobile PageSpeed score is 45/100 -- competitors average 72" not "Your site is slow."
- **Action-oriented.** End with "Here are the top 3 things to do first."

### Section Tone

- **Factual first, interpretation second.** Present the data, then explain what it means.
- **Business impact language.** "This means..." followed by what happens to leads/revenue/visibility.
- **Evidence-based.** Every claim references a specific finding from the audit.
- **Professional but not academic.** Clear, direct sentences. No jargon without explanation.

### What to Avoid

- Generic statements that could apply to any business
- Technical jargon without explanation
- Accusatory or negative framing ("your site is terrible")
- Vague recommendations ("improve your SEO")
- False urgency or fear-based language
- Promises about specific ranking outcomes

### Tone Examples

**Bad:** "Your website has numerous SEO issues that need immediate attention."
**Good:** "Your site scores 47/100 overall, with the biggest opportunities in AI search readiness (C+) and content optimization (C). Quick wins in schema markup and FAQ content could improve your AI visibility within weeks."

**Bad:** "You need to fix your meta tags."
**Good:** "Your homepage title tag is 'Home | Business Name' -- this misses the opportunity to target 'dentist in Portland.' Updating the title to 'Family Dentist in Portland, OR | Business Name' could improve click-through rates for your most valuable search term."

## Competitor Comparison Table Format

The competitor comparison section uses side-by-side tables:

```markdown
## Competitor Comparison

### Overall Scores

| Metric | [Client] | [Competitor 1] | [Competitor 2] | [Competitor 3] |
|--------|----------|----------------|----------------|----------------|
| Overall Score | 47/100 | 62/100 | 71/100 | 38/100 |
| AEO Readiness | C+ (5.4) | B (6.5) | B+ (7.8) | D (3.2) |
| Technical SEO | B (6.8) | B+ (7.2) | A (8.5) | C (4.1) |
| Content Quality | C (4.5) | B (6.0) | B (6.2) | C+ (5.0) |
| Local SEO | B+ (7.2) | A (8.5) | B+ (7.0) | B (6.5) |
| Google Reviews | 12 (4.2★) | 87 (4.7★) | 45 (4.5★) | 23 (3.8★) |

### Key Takeaways
- Where the client leads competitors
- Where the client trails competitors
- Biggest competitive gaps to close
- Opportunities competitors are missing
```

## Action Plan Format

The Prioritized Action Plan uses an impact/effort matrix:

### Priority Levels

| Priority | Impact | Effort | Label |
|----------|--------|--------|-------|
| P1 | High | Low | Quick Wins -- Do First |
| P2 | High | Medium | Strategic Priorities |
| P3 | High | High | Major Initiatives |
| P4 | Medium | Low | Easy Improvements |
| P5 | Medium-Low | Any | Backlog |

### Action Plan Table Format

```markdown
## Prioritized Action Plan

### Quick Wins (Do This Week)
| # | Action | Category | Expected Impact |
|---|--------|----------|-----------------|
| 1 | Add FAQ schema to existing FAQ content | AEO | Improved AI search extraction |
| 2 | Update homepage title tag to include primary keyword + city | Technical | Better search visibility |
| 3 | Add LocalBusiness JSON-LD schema | AEO + Technical | Better entity recognition |

### Strategic Priorities (Next 30 Days)
| # | Action | Category | Expected Impact |
|---|--------|----------|-----------------|
| 4 | Create comprehensive FAQ page targeting top 10 customer questions | AEO + Content | AI answer eligibility |
| 5 | Claim and optimize Google Business Profile | Local | Local Pack visibility |

### Major Initiatives (Next 90 Days)
[Continue format...]
```

### AEO Actions Highlighted

AEO-related actions should be visually highlighted or tagged in the action plan. In the HTML report, AEO actions get a special badge or accent color to reinforce the differentiator.

## Appendix Content

The appendix includes:
- **Methodology:** Brief description of how the audit was conducted
- **Scoring definitions:** The 1-10 scale and letter grades explained
- **Tool data sources:** List of APIs and tools used (PageSpeed Insights, SSL Labs, W3C Validator, etc.)
- **Glossary:** Key terms defined (AEO, Core Web Vitals, Schema Markup, NAP, etc.)
- **Disclaimer:** "Scores and recommendations are based on data collected on [date]. Search engine algorithms change. Regular re-audits are recommended."
