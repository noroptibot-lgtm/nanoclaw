---
name: AEO Optimization
version: 1.0.0
description: Answer Engine Optimization -- the star skill. Assessment framework for how businesses appear in AI search engines (ChatGPT, Perplexity, Google AI Overviews, Bing Copilot). Covers structured data for AI, answer-ready content formats, entity authority, topical authority, citation-worthiness, and scoring methodology. Used by AEO Analyst, Report Writer, SEO Strategist, and Quality Reviewer agents.
---

# AEO Optimization Skill (Answer Engine Optimization)

This is the centerpiece skill of the audit. AEO -- Answer Engine Optimization -- assesses how well a business is positioned to appear in AI-generated search results. This is the differentiator that makes the audit stand out. Most SEO agencies still don't assess this.

## Why AEO Matters

AI search engines are changing how people find businesses:
- **Google AI Overviews** appear above traditional search results for ~30% of queries
- **ChatGPT with browsing** and **SearchGPT** are used by millions for recommendations
- **Perplexity AI** provides cited, synthesized answers from multiple sources
- **Bing Copilot** integrates AI answers directly into search results
- **Claude** (via web search) provides researched recommendations

Traditional SEO optimizes for ranking in a list of links. AEO optimizes for being **cited as a source** in AI-generated answers. The mechanics are fundamentally different.

## How AI Search Engines Select Sources

Understanding this is critical to the assessment. AI engines don't rank pages -- they select sources to cite.

### Selection Criteria (What AI Engines Look For)

1. **Direct answer availability** -- Content that directly answers a question gets cited. AI engines prefer pages that contain clear, concise answers in the first few paragraphs, not pages that bury the answer under 1000 words of preamble.

2. **Structured data** -- JSON-LD schema helps AI engines understand what a page is about, what entity it describes, and what questions it answers. Pages with rich schema are more parseable.

3. **Entity clarity** -- AI engines need to understand what entity (business, person, concept) a page represents. Clear entity definitions through schema, consistent NAP, and Knowledge Panel presence help.

4. **Topical authority** -- AI engines assess whether a source is authoritative on a topic by looking at content depth, breadth of coverage, internal linking patterns, and external citations.

5. **Recency and freshness** -- AI engines prefer current information. Dated content, especially for queries with time-sensitive answers, gets deprioritized.

6. **Citation-worthiness** -- Content that contains original data, unique research, expert opinions, or specific claims with evidence is more likely to be cited than generic advice.

7. **Content format** -- Certain formats are more easily extractable by AI:
   - Definition paragraphs ("X is a...")
   - Numbered/bulleted lists
   - Comparison tables
   - Q&A format
   - Step-by-step instructions
   - Statistics with sources

### How Each AI Engine Differs

| Engine | Primary Source Behavior | Key Factors |
|--------|----------------------|-------------|
| **Google AI Overviews** | Synthesizes from top-ranking pages | Traditional SEO ranking matters most; structured data helps |
| **ChatGPT/SearchGPT** | Browses web, synthesizes from multiple sources | Prefers clear, authoritative, well-structured content |
| **Perplexity AI** | Cites specific sources with links | Values unique data, specific claims, and authoritative sources |
| **Bing Copilot** | Draws from Bing index + partner data | Bing SEO factors matter; structured data heavily weighted |
| **Claude (web search)** | Searches and synthesizes from multiple results | Values comprehensive, nuanced, well-sourced content |

## AEO Assessment Framework

### Criterion 1: Structured Data for AI (Weight: 15%)

**What to assess:**
- JSON-LD schema presence and completeness
- Business-relevant schema types (LocalBusiness, Service, Product, FAQPage, HowTo, Review)
- Schema accuracy (does it match actual page content?)
- Missing schema opportunities

**Scoring:**

| Score | Description |
|-------|-------------|
| 9-10 | Comprehensive schema covering all business entities, services, FAQs. Validated and accurate. |
| 7-8 | Core business schema present (Organization/LocalBusiness), some service/product schema |
| 5-6 | Basic schema present (Organization only) or schema has errors |
| 3-4 | Minimal schema (just website or breadcrumb) |
| 1-2 | No structured data at all |

### Criterion 2: Answer-Ready Content (Weight: 20%)

**What to assess:**
- Does the site have content that directly answers common questions about their services?
- Are answers formatted for extraction (short paragraphs, lists, tables)?
- Does the site have a FAQ page or FAQ sections on service pages?
- Are there "definition" paragraphs that explain what the business does?
- Are there how-to guides, comparison pages, or educational content?

**Answer-ready formats to look for:**
- **FAQ sections** with clear Q&A pairs
- **Definition paragraphs** ("Kitchen remodeling is the process of...")
- **Comparison tables** (Service A vs. Service B, or "What to look for in a...")
- **Numbered steps** ("How to choose a plumber: 1. Check licensing, 2. Read reviews...")
- **Statistics or data points** with sources
- **Expert quotes or opinions** attributed to named professionals

**Scoring:**

| Score | Description |
|-------|-------------|
| 9-10 | Multiple answer-ready content pieces, FAQ pages, how-to guides, comparison tables. Content is formatted for AI extraction. |
| 7-8 | Some FAQ content, a few answer-ready pages. Room for more structured answers. |
| 5-6 | Limited answer-ready content. Information exists but isn't formatted for extraction. |
| 3-4 | Minimal content. No FAQs, no structured answers. Content is marketing-focused, not answer-focused. |
| 1-2 | No content that an AI engine could extract a direct answer from. |

### Criterion 3: Entity Authority (Weight: 20%)

**What to assess:**
Entity authority is about whether AI engines recognize this business as a known, trusted entity.

- **Google Knowledge Panel**: Does the business have one? (Search for the business name in Google)
- **Directory presence**: Is the business listed on major directories (Google Business Profile, Yelp, BBB, industry-specific directories)?
- **Consistent NAP**: Is the business name, address, and phone number consistent across the web?
- **Authoritative mentions**: Is the business mentioned on news sites, industry publications, or authoritative blogs?
- **Social profiles**: Are official social media profiles linked and active?
- **Wikipedia/Wikidata**: For larger businesses -- is there an entry?

**Scoring:**

| Score | Description |
|-------|-------------|
| 9-10 | Knowledge Panel present, consistent directory listings, authoritative mentions, active social profiles |
| 7-8 | Strong directory presence, some authoritative mentions, no Knowledge Panel but strong entity signals |
| 5-6 | Listed on major directories, some inconsistencies, limited authoritative mentions |
| 3-4 | Few directory listings, inconsistent information, no authoritative mentions |
| 1-2 | Minimal or no web presence beyond the website itself |

### Criterion 4: Topical Authority (Weight: 20%)

**What to assess:**
Topical authority measures whether the site demonstrates deep knowledge on its core topics.

- **Content depth**: Does the site have comprehensive coverage of its core topics, or just surface-level service descriptions?
- **Content clusters**: Are there groups of related content linked together (pillar + supporting pages)?
- **Internal linking**: Do pages link to related pages on the same site?
- **Original data/research**: Does the site publish unique information, case studies, or original insights?
- **Content breadth**: Does the site cover the topic from multiple angles (how-to, comparison, cost, FAQ, case study)?
- **Publication consistency**: Is new content published regularly?

**Scoring:**

| Score | Description |
|-------|-------------|
| 9-10 | Deep content clusters, original data, regular publishing, comprehensive internal linking. Clear subject matter authority. |
| 7-8 | Good content depth on core topics, some clusters, moderate internal linking |
| 5-6 | Adequate content on core topics but no depth. No clusters or original data. |
| 3-4 | Thin content. Service descriptions only, no supporting content. |
| 1-2 | Minimal content. One-page or brochure-style site. |

### Criterion 5: Citation-Worthiness (Weight: 15%)

**What to assess:**
Citation-worthiness is about whether an AI engine would trust this site enough to cite it as a source.

- **Original data**: Does the site publish statistics, research, or data that doesn't exist elsewhere?
- **Expert credentials**: Are content creators identified with relevant expertise?
- **Specific claims**: Does the content make specific, verifiable claims (not vague generalities)?
- **Source attribution**: Does the site cite its own sources?
- **Unique perspective**: Does the content offer insights not available on competing sites?
- **Content quality**: Is the writing professional, factual, and well-organized?

**Scoring:**

| Score | Description |
|-------|-------------|
| 9-10 | Original data, named experts, specific claims with evidence, professional writing. Highly citable. |
| 7-8 | Some unique content, professional writing, some specific claims. Reasonably citable. |
| 5-6 | Professional but generic content. Nothing uniquely citable. |
| 3-4 | Thin or generic content with no unique value. Unlikely to be cited. |
| 1-2 | Poor quality, no unique information. Would not be cited. |

### Criterion 6: AI Search Visibility (Weight: 10%)

**What to assess:**
Attempt to test actual AI search visibility by considering:

- What would a user ask an AI assistant to find this type of business?
- Based on the site's content and authority, would it likely be surfaced?
- Are there obvious barriers (thin content, no schema, poor authority)?

**Test queries to consider:**
- "Best [service] in [city]"
- "How much does [service] cost in [city]?"
- "[Service provider] near me recommendations"
- "What should I look for in a [service provider]?"

**Scoring:**

| Score | Description |
|-------|-------------|
| 9-10 | Strong signals across all criteria. Likely to appear in AI search results for relevant queries. |
| 7-8 | Good signals. May appear for some queries, especially branded or specific ones. |
| 5-6 | Mixed signals. Unlikely to appear in AI results except for branded queries. |
| 3-4 | Weak signals. Very unlikely to appear in AI search results. |
| 1-2 | No AI search readiness. Invisible to AI engines. |

## AEO Scoring Methodology

### Per-Criterion Score: 1-10

Each criterion scored individually with evidence and justification.

### Overall AEO Score

Weighted average of all 6 criteria, mapped to 1-10 scale.

### Letter Grade Mapping

| Score | Grade | Label |
|-------|-------|-------|
| 9.0-10.0 | A+ | AI Search Leader |
| 8.0-8.9 | A | AI Search Ready |
| 7.0-7.9 | B+ | Above Average |
| 6.0-6.9 | B | Moderate Readiness |
| 5.0-5.9 | C+ | Below Average |
| 4.0-4.9 | C | Significant Gaps |
| 3.0-3.9 | D | Major Gaps |
| 1.0-2.9 | F | AI Search Invisible |

### Score Display Format

```
AI Search Readiness: C+ (5.4/10)

Structured Data:     ██░░░░░░░░  3/10  -- No schema markup found
Answer-Ready Content: ████░░░░░░  5/10  -- Some FAQ content, not optimized for extraction
Entity Authority:     ██████░░░░  7/10  -- Strong directory presence, no Knowledge Panel
Topical Authority:    ████░░░░░░  5/10  -- Service pages only, no depth content
Citation-Worthiness:  █████░░░░░  6/10  -- Professional writing, no original data
AI Search Visibility: ████░░░░░░  5/10  -- Mixed signals, limited discoverability
```

## AEO Recommendations Library

Organized by effort level. When writing the action plan, select recommendations based on the specific gaps found.

### Quick Wins (1-2 hours each)

- Add FAQ schema to existing FAQ content
- Add LocalBusiness/Organization JSON-LD schema
- Write a definition paragraph at the top of each service page
- Add comparison tables to service pages
- Create a "What to expect" section on service pages with numbered steps
- Add review schema for customer testimonials on the site
- Ensure Google Business Profile is fully completed and linked

### Medium Effort (1-2 days each)

- Create a comprehensive FAQ page targeting common questions
- Publish a "How to choose a [service provider]" guide
- Create a cost/pricing guide for services
- Add case studies with specific metrics and outcomes
- Build a resource center or knowledge base
- Optimize existing content for answer-ready formatting
- Create comparison content (your service vs. alternatives)

### High Effort (1-2 weeks each)

- Build content clusters around core service topics (pillar + supporting pages)
- Develop original research or data (e.g., annual industry survey, local market report)
- Create a comprehensive content calendar targeting AEO-relevant topics
- Build authoritative backlinks through expert contributions, PR, and partnerships
- Develop video content optimized for AI search (transcripts, structured descriptions)
- Pursue Google Knowledge Panel verification

## Report Writing Guidelines for AEO

1. **Lead with the score.** The AEO score is the first thing the prospect should see in this section. It's the attention-grabber.
2. **Explain what AEO is.** Most business owners have never heard of it. Include a brief (2-3 sentence) explanation before diving into the assessment.
3. **Show, don't just tell.** "When someone asks ChatGPT 'best dentist in [city],' your practice doesn't appear -- but your competitor [Name] does. Here's why."
4. **Be specific about what's missing.** "Your site has no FAQ schema, no FAQ content, and no how-to guides. AI engines have nothing to extract when answering questions about [service]."
5. **Connect to revenue.** "AI search is handling an estimated 20% of discovery queries in your market. Every month you're invisible to AI search, you're losing potential customers to competitors who are visible."
6. **Prioritize recommendations.** The action plan should clearly indicate which AEO improvements give the biggest lift for the least effort.
7. **The AEO section should be 6-8 pages.** This is the lead section, not an afterthought. Each criterion gets its own subsection with evidence and recommendations.
