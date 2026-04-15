---
name: negative-keyword-ai-v6-architecture
description: Architecture documentation and code for the v6 negative keyword classification system. Triggers when user wants to understand or implement the chain-based negative keyword AI system with mechanical pre-processing and AI classification.
---

⛓
Negative Keyword AI (v6
Architecture)
Platform Google Ads
Status✅ Live
Type🛠 Tool
👉 What this
doesAdvanced negative keyword classification with code-
driven chain
📚 Architecture Documentation
# Negative Keyword Agent — Chain Architecture v6.0
## Overview
**Goal:** Classify search terms for any Google Ads account wi
th maximum accuracy and minimum AI cost.
**Architecture:** Code-driven chain with single AI step for a
mbiguous terms only.
```
┌────────────────────────────────────────────────────────────
────┐
│                    MECHANICAL PRE-PROCESSING                   
│
│                      (Steps 1-5 — No AI)                       
Negative Keyword AI (v6 Architecture)

│
├────────────────────────────────────────────────────────────
────┤
│  Step 1: Conversion & Brand Protection → Instant KEEP          
│
│  Step 2: Primary Service Flagging → softProtected flag         
│
│  Step 2.5: Competitor Detection → Instant NEGATE               
│
│  Step 3: Universal Patterns → Instant NEGATE (if unprotecte
d)  │
│  Step 3.5: Cross-Modality Check → Instant NEGATE               
│
│  Step 4: Alternative-Seeker Detection → Flag for AI            
│
│  Step 5: Low-Value Filtering → SKIP (not worth analyzing)      
│
└────────────────────────────────────────────────────────────
────┘
                              ↓
                    ~40-60% of terms remain
                              ↓
┌────────────────────────────────────────────────────────────
────┐
│                     AI ANALYSIS (Step 6)                       
│
│              Single AI call for ambiguous terms                
│
│         Intent classification, competitor detection,           
│
│              service alignment, recommendation                 
│
└────────────────────────────────────────────────────────────
────┘
                              ↓
┌────────────────────────────────────────────────────────────
Negative Keyword AI (v6 Architecture)

────┐
│                 MECHANICAL POST-PROCESSING                     
│
│                   (Steps 6.5 & 7 — No AI)                      
│
├────────────────────────────────────────────────────────────
────┤
│  Step 6.5: CPC Context Enrichment → Add cost context           
│
│  Step 7: Final guardrails, override tracking, output           
│
└────────────────────────────────────────────────────────────
────┘
```
---
## Input Requirements
### Context (from Config)
```typescript
interface NegativeKeywordContext {
  // Business Identity
  brand_terms: string[];                    // ["acme denta
l", "acme"]
  primary_service_keywords: string[];       // ["dental impla
nts", "implants"]
  services_offered: string[];               // ["implants",  
"veneers", "crowns"]
  services_not_offered: string[];           // ["orthodontic
s", "braces"]
  adjacent_services_offered: string[];      // ["teeth whiten
ing"] - different campaigns
  buyer_persona: string;                    // "Adults 35-55  
seeking cosmetic dental work"
Negative Keyword AI (v6 Architecture)

  // Synonym Expansion
  synonym_groups?: string[][];              // [["liposuctio
n", "lipo"], ["tummy tuck", "abdominoplasty"]]
  industry?: string;                        // Auto-detected  
or override
  // Strategy Flags
  allow_competitor_terms: boolean;          // Default: false
  allow_cross_modality: boolean;            // Default: false
  price_positioning: string;                // "premium" | "b
udget"
  funnel_target: string;                    // "BOFU" | "MOF
U" | "Full"
  locations_served: string[];               // ["Austin, TX",  
"Dallas, TX"]
  languages_supported: string[];            // ["en"]
  // Analysis Settings
  target_cpa?: number;                      // Target cost pe
r acquisition
  expected_conv_rate?: number;              // Expected conve
rsion rate (0.03 = 3%)
  min_clicks_to_analyze: number;            // Default: 1
  min_impressions_to_analyze: number;       // Default: 20
  select_metric: string;                    // "cost" | "clic
ks" | "impressions"
  select_top_n: number;                     // Prioritize top  
N terms (default: 200)
  date_range_days: number;                  // Days in report  
period
  // Computed
  avg_cpc: number;                          // Calculated fro
m data
}
Negative Keyword AI (v6 Architecture)

```
### Search Term Data
```typescript
interface SearchTerm {
  term: string;
  impressions: number;
  clicks: number;
  cost: number;
  conversions: number;
  view_through_conversions?: number;
}
```
---
## Pre-Processing: Threshold Filtering & Prioritization
Before the pipeline runs:
```javascript
// 1. Filter by threshold
function filterTermsForAnalysis(terms, cfg) {
  return terms.filter(t =>
    t.clicks >= cfg.min_clicks_to_analyze ||
    t.impressions >= cfg.min_impressions_to_analyze
  );
}
// 2. Sort by priority metric
function selectTopTerms(terms, cfg) {
  const metric = cfg.select_metric || "cost";
  return terms.sort((a, b) => b[metric] - a[metric]);
}
Negative Keyword AI (v6 Architecture)

// 3. Apply top N if configured
const topN = cfg.select_top_n;
const priorityTerms = sorted.slice(0, topN);
const remainingTerms = sorted.slice(topN);
const workingTerms = [...priorityTerms, ...remainingTerms];
```
---
## Pre-Processing: Synonym Expansion
```javascript
const INDUSTRY_SYNONYMS = {
  medical_aesthetics: [
    ["liposuction", "lipo"],
    ["smart lipo", "laser lipo", "lipo laser", "laser liposuc
tion"],
    ["tummy tuck", "abdominoplasty"],
    ["coolsculpting", "coolsculpt", "cool sculpting"],
    ["brazilian butt lift", "bbl"],
    ["rhinoplasty", "nose job"]
  ],
  dental: [
    ["dental implants", "implants", "tooth implants"],
    ["invisalign", "clear aligners"],
    ["veneers", "dental veneers", "porcelain veneers"]
  ],
  // ... other industries
};
function expandWithSynonyms(keywords, synonymGroups) {
  const expanded = new Set(keywords.map(k => k.toLowerCase
()));
  for (const kw of keywords) {
    for (const group of synonymGroups) {
      if (group.some(s => s.toLowerCase() === kw.toLowerCase
Negative Keyword AI (v6 Architecture)

())) {
        group.forEach(s => expanded.add(s.toLowerCase()));
      }
    }
  }
  return Array.from(expanded);
}
```
---
## STEP 1: Conversion & Brand Protection
**Job:** Protect converting and brand terms (≤10 words: "Prot
ect proven converters and brand")
```javascript
function step1_conversionBrandProtection(term, context) {
  // Conversions ≥ 1 → Instant KEEP
  if (term.conversions >= 1) {
    return { action: "KEEP", category: term.conversions >= 3  
? "Optimal" : "Good",
             rationale: `Converting term (${term.conversions}  
conv)`, skipRemaining: true };
  }
  // View-through only → KEEP as Watch
  if ((term.view_through_conversions || 0) >= 1) {
    return { action: "KEEP", category: "Watch",
             rationale: "View-through conversions", skipRemai
ning: true };
  }
  // Brand match (with misspelling tolerance for 5+ char bran
ds)
  for (const brand of context.brand_terms) {
Negative Keyword AI (v6 Architecture)

    if (termMatchesBrand(term, brand)) {
      return { action: "KEEP", category: "Good", rationale:  
"Brand term", skipRemaining: true };
    }
  }
  return { skipRemaining: false };
}
```
**Expected impact:** ~5-15% instant KEEP.
---
## STEP 2: Primary Service Flagging
**Job:** Flag terms with primary service keywords (≤10 words:  
"Flag primary service terms")
```javascript
function step2_primaryServiceFlag(term, expandedPrimary, expa
ndedServices) {
  const termLower = term.term.toLowerCase();
  let softProtected = false;
  let matchedService = null;
  for (const kw of expandedPrimary) {
    if (new RegExp(`\\b${escapeRegex(kw)}\\b`).test(termLowe
r)) {
      softProtected = true;
      matchedService = "primary_keyword";
      break;
    }
  }
  if (!softProtected) {
Negative Keyword AI (v6 Architecture)

    for (const svc of expandedServices) {
      if (new RegExp(`\\b${escapeRegex(svc)}\\b`).test(termLo
wer)) {
        softProtected = true;
        matchedService = "service_offered";
        break;
      }
    }
  }
  // Commercial intent modifiers
  const COMMERCIAL = /\b(best|top|vs|versus|compare|cost|pric
e|near me|reviews?|quotes?)\b/i;
  const commercialIntent = COMMERCIAL.test(termLower);
  return { softProtected, matchedService, commercialIntent };
}
```
**Expected impact:** ~25% flagged as soft-protected.
---
## STEP 2.5: Competitor Detection
**Job:** Auto-negate competitor terms (≤10 words: "Negate com
petitor brand terms")
```javascript
const COMPETITOR_PATTERNS = [
  /\bsono\s?bello\b/i,
  /\bcool\s?sculpt(?:ing|ure)?\b/i,
  /\bemsculpt\b/i,
  /\btru\s?sculpt\b/i,
  /\bsculpsure\b|\bvanquish\b|\bzerona\b|\bvelashape\b/i,
  /\bmorpheus8\b|\bbodytite\b|\baccutite\b/i,
Negative Keyword AI (v6 Architecture)

  /\bcryolipolysis\b|\bcryoslimming\b|\bfat\s*freez/i,
  /\bkybella\b|\bfat[-\s]?dissolving\b/i
];
function step2_5_competitorDetection(term, cfg, flags) {
  if (cfg.allow_competitor_terms) return { action: "CONTINUE"  
};
  const termLower = term.term.toLowerCase();
  const isCompetitor = COMPETITOR_PATTERNS.some(rx => rx.test
(termLower));
  if (isCompetitor) {
    // Exception: alternative-seekers are valuable
    if (flags.alternativeSeeker) return { action: "CONTINUE"  
};
    return {
      action: "NEGATIVE_ADD",
      category: "Definite Waste",
      matchType: "PHRASE",
      rationale: "Competitor term",
      skipRemaining: true
    };
  }
  return { action: "CONTINUE" };
}
```
**Expected impact:** ~5-10% auto-negated.
---
## STEP 3: Universal Exclusion Patterns
Negative Keyword AI (v6 Architecture)

**Job:** Auto-negate universal waste patterns (≤10 words: "Ne
gate universal waste patterns")
```javascript
const UNIVERSAL_PATTERNS = {
  employment: {
    pattern: /\b(jobs?|careers?|hiring|salary|resume|employme
nt|intern(?:ship)?s?)\b/i,
    matchType: "BROAD", category: "Definite Waste", reason:  
"Employment intent"
  },
  navigation: {
    pattern: /\b(login|log in|sign in|account|portal|dashboar
d)\b/i,
    matchType: "PHRASE", category: "Definite Waste", reason:  
"Navigation intent"
  },
  forum: {
    pattern: /\b(reddit|quora|forum)\b/i,
    matchType: "BROAD", category: "Likely Waste", reason: "Fo
rum research"
  },
  diy: {
    pattern: /\b(diy|do it yourself|homemade|home remedy)\b/
i,
    matchType: "PHRASE", category: "Likely Waste", reason: "D
IY intent"
  },
  education: {
    pattern: /\b(certification|certified|degree|how to becom
e)\b/i,
    matchType: "PHRASE", category: "Likely Waste", reason: "C
areer/education intent"
  },
  informational: {
    pattern: /\b(what is|definition|meaning|wiki)\b/i,
Negative Keyword AI (v6 Architecture)

    matchType: "PHRASE", category: "Likely Waste", reason: "I
nformational intent"
  }
};
function step3_universalPatterns(term, flags) {
  for (const [key, config] of Object.entries(UNIVERSAL_PATTER
NS)) {
    if (config.pattern.test(term.term)) {
      // Protected terms → route to AI with conflict flag
      if (flags.softProtected) {
        return { action: "NEEDS_AI", conflict: { patternMatch
ed: key, reason: config.reason } };
      }
      return { action: "NEGATIVE_ADD", ...config, skipRemaini
ng: true };
    }
  }
  return { action: "CONTINUE" };
}
```
**Expected impact:** ~5-10% auto-negated, ~2% routed to AI wi
th conflict.
---
## STEP 3.5: Cross-Modality Check
**Job:** Negate wrong-service terms (≤10 words: "Negate adjac
ent service terms")
```javascript
function step3_5_crossModalityCheck(term, cfg, expandedOffere
d, expandedAdjacents) {
  if (cfg.allow_cross_modality) return { action: "CONTINUE"  
Negative Keyword AI (v6 Architecture)

};
  const termLower = term.term.toLowerCase();
  // Mentions adjacent service (different campaign)?
  const hitsAdjacent = expandedAdjacents.some(tok =>
    new RegExp(`\\b${escapeRegex(tok)}\\b`).test(termLower)
  );
  // Also mentions primary/offered service?
  const hitsPrimary = expandedOffered.some(tok =>
    new RegExp(`\\b${escapeRegex(tok)}\\b`).test(termLower)
  );
  // Adjacent but NOT primary → cross-modality waste
  if (hitsAdjacent && !hitsPrimary) {
    return {
      action: "NEGATIVE_ADD",
      category: "Definite Waste",
      matchType: "PHRASE",
      rationale: "Different modality from this ad group",
      skipRemaining: true
    };
  }
  return { action: "CONTINUE" };
}
```
**Expected impact:** ~2-5% auto-negated.
---
## STEP 4: Alternative-Seeker Detection
**Job:** Flag comparison shoppers (≤10 words: "Flag alternati
Negative Keyword AI (v6 Architecture)

ve-seeking intent")
```javascript
function step4_alternativeSeekers(term) {
  const ALTERNATIVE_SIGNALS = /\b(alternative|instead of|bett
er than|vs|versus|compared to|switch(?:ing)? from|similar to|
substitute)\b/i;
  const LIKE_BUT_PATTERN = /like .+ but/i;
  if (ALTERNATIVE_SIGNALS.test(term.term) || LIKE_BUT_PATTER
N.test(term.term)) {
    return { alternativeSeeker: true, note: "Comparison shopp
er — likely valuable" };
  }
  return { alternativeSeeker: false };
}
```
**Expected impact:** ~2-5% flagged as valuable.
---
## STEP 5: Low-Value Filtering
**Job:** Skip insignificant terms (≤10 words: "Filter statist
ical noise")
```javascript
function step5_lowValueFilter(term, context) {
  const { avg_cpc, date_range_days } = context;
  const impressionsPerDay = term.impressions / date_range_day
s;
  // Single impression
  if (term.impressions === 1) return { action: "SKIP", reaso
n: "Single impression" };
Negative Keyword AI (v6 Architecture)

  // No clicks + trivial spend
  if (term.clicks === 0 && term.cost < avg_cpc * 0.5) {
    return { action: "SKIP", reason: "No clicks, trivial spen
d" };
  }
  // No clicks + below daily threshold
  if (term.clicks === 0 && impressionsPerDay < 0.33) {
    return { action: "SKIP", reason: "Below impression thresh
old" };
  }
  return { action: "CONTINUE" };
}
```
**Expected impact:** ~15-30% skipped.
---
## STEP 6: AI Analysis
**Job:** Classify ambiguous terms (≤10 words: "Classify ambig
uous search intent")
### System Prompt
```
ROLE: Search term classifier for Google Ads negative keyword  
analysis.
TASK: Classify each term and recommend action.
CATEGORIES (waste → value):
- Definite Waste → NEGATIVE_ADD
Negative Keyword AI (v6 Architecture)

- Likely Waste → NEGATIVE_ADD
- Potential Waste → NEGATIVE_ADD (lower confidence)
- Questionable → MONITOR
- Watch → MONITOR
- Good → KEEP
- Optimal → KEEP
INTERPRETING FLAGS:
| Flag | Meaning | Guidance |
|------|---------|----------|
| softProtected: true | Contains primary service | Be VERY ca
utious negating |
| commercialIntent: true | Has buying signals | Weight toward  
KEEP |
| alternativeSeeker: true | Comparison shopping | Usually val
uable |
| conflict.patternMatched | Waste pattern + protected | Weigh  
both signals |
PRINCIPLES:
1. Intent over keywords
2. Service alignment
3. Competitor identification (if allow_competitor_terms=fals
e, competitors = waste)
4. Cross-modality (service NOT offered = waste)
5. Consistency (synonyms treated identically)
6. When uncertain → MONITOR
CONFIDENCE:
- 0.8+: Confident
- 0.6-0.8: Reasonable
- <0.6: Output "HUMAN_REVIEW"
OUTPUT: {"recommendations": [{"term", "category", "action",  
"match_type", "level", "suggested_negative", "rationale", "co
nfidence", "signals"}]}
Negative Keyword AI (v6 Architecture)

```
### Context Payload
```javascript
{
  brand_terms, services_offered, services_not_offered,
  primary_service_keywords, adjacent_services_offered,
  buyer_persona, allow_competitor_terms, allow_cross_modalit
y,
  price_positioning, funnel_target, locations_served, languag
es_supported,
  existing_negative_keywords,
  search_terms: [{ term, clicks, impressions, cost, conversio
ns, flags }]
}
```
---
## STEP 6.5: CPC Context Enrichment
**Job:** Add cost context to rationales (≤10 words: "Add cost  
efficiency context")
```javascript
function step6_5_cpcEnrichment(term, result, context) {
  if (term.clicks === 0) {
    if (term.impressions >= 50) {
      result.rationale += ` | No clicks across ${term.impress
ions} impr — check relevance.`;
    }
    return result;
  }
  const termCpc = term.cost / term.clicks;
Negative Keyword AI (v6 Architecture)

  const { target_cpa, expected_conv_rate, avg_cpc } = contex
t;
  // Break-even math if available
  if (target_cpa && expected_conv_rate) {
    const breakEven = target_cpa * expected_conv_rate;
    if (termCpc <= breakEven * 0.5) {
      result.rationale += ` | CPC $${termCpc.toFixed(2)} belo
w break-even — cheap to test.`;
    } else if (termCpc >= breakEven) {
      result.rationale += ` | CPC $${termCpc.toFixed(2)} abov
e break-even — monitor closely.`;
    }
  }
  // Fallback: compare to average
  else if (avg_cpc) {
    const ratio = termCpc / avg_cpc;
    if (ratio <= 0.5) result.rationale += ` | CPC ${Math.roun
d((1-ratio)*100)}% below avg.`;
    if (ratio >= 1.5) result.rationale += ` | CPC ${Math.roun
d((ratio-1)*100)}% above avg.`;
  }
  return result;
}
```
---
## STEP 7: Post-Processing Guardrails
**Job:** Final safety overrides (≤10 words: "Apply final safe
ty overrides")
```javascript
function step7_guardrails(term, result, flags, context) {
Negative Keyword AI (v6 Architecture)

  // 7.1: Conversion protection
  if (result.action === "NEGATIVE_ADD" && term.conversions >=  
1) {
    return override(result, "KEEP", "Good", "Has conversion
s", "conversion_protection");
  }
  // 7.2: Brand protection
  if (result.action === "NEGATIVE_ADD" && isBrandTerm(term, c
ontext)) {
    return override(result, "KEEP", "Good", "Brand term", "br
and_protection");
  }
  // 7.3: Service + commercial intent
  if (result.action === "NEGATIVE_ADD" && flags.softProtected  
&& flags.commercialIntent) {
    return override(result, "MONITOR", "Watch", "Service + co
mmercial", "service_commercial");
  }
  // 7.4: Cross-modality enforcement
  if (mentionsNotOffered(term, context) && !mentionsOffered(t
erm, context)) {
    if (result.action !== "NEGATIVE_ADD") {
      return override(result, "NEGATIVE_ADD", "Definite Wast
e", "Service not offered", "cross_modality");
    }
  }
  // 7.5: Alternative-seeker protection
  if (result.action === "NEGATIVE_ADD" && flags.alternativeSe
eker) {
    return override(result, "MONITOR", "Watch", "Alternative-
seeker", "alt_seeker");
  }
Negative Keyword AI (v6 Architecture)

  return result;
}
```
---
## Pipeline Orchestration
```javascript
async function analyzeSearchTerms(allTerms, context) {
  // Pre-filter by threshold
  const filtered = filterTermsForAnalysis(allTerms, context);
  const working = selectTopTerms(filtered, context);
  // Expand synonyms
  const synonyms = loadSynonyms(context);
  const expandedPrimary = expandWithSynonyms(context.primary_
service_keywords, synonyms);
  const expandedServices = expandWithSynonyms(context.service
s_offered, synonyms);
  const expandedAdjacents = expandWithSynonyms(context.adjace
nt_services_offered, synonyms);
  const results = { keep: [], monitor: [], negative: [], huma
nReview: [], skipped: [] };
  const forAI = [];
  // === MECHANICAL PRE-PROCESSING ===
  for (const term of working) {
    // Step 1
    const s1 = step1_conversionBrandProtection(term, contex
t);
    if (s1.skipRemaining) { results.keep.push({term, ...s1});  
continue; }
Negative Keyword AI (v6 Architecture)

    // Step 2
    const flags = step2_primaryServiceFlag(term, expandedPrim
ary, expandedServices);
    // Step 4 (needed for Step 2.5 exception)
    const s4 = step4_alternativeSeekers(term);
    Object.assign(flags, s4);
    // Step 2.5
    const s2_5 = step2_5_competitorDetection(term, context, f
lags);
    if (s2_5.skipRemaining) { results.negative.push({term,  
...s2_5}); continue; }
    // Step 3
    const s3 = step3_universalPatterns(term, flags);
    if (s3.skipRemaining) { results.negative.push({term, ...s
3}); continue; }
    if (s3.conflict) flags.conflict = s3.conflict;
    // Step 3.5
    const s3_5 = step3_5_crossModalityCheck(term, context, ex
pandedServices, expandedAdjacents);
    if (s3_5.skipRemaining) { results.negative.push({term,  
...s3_5}); continue; }
    // Step 5
    const s5 = step5_lowValueFilter(term, context);
    if (s5.action === "SKIP") { results.skipped.push({term,  
...s5}); continue; }
    forAI.push({ term, flags });
  }
  // === AI ANALYSIS ===
  forAI.sort((a, b) => b.term.cost - a.term.cost);
Negative Keyword AI (v6 Architecture)

  const aiResults = await batchAIAnalysis(forAI, context);
  // === POST-PROCESSING ===
  for (const { term, flags, aiResult } of aiResults) {
    const enriched = step6_5_cpcEnrichment(term, aiResult, co
ntext);
    const final = step7_guardrails(term, enriched, flags, con
text);
    if (final.action === "KEEP") results.keep.push({term, ...
final});
    else if (final.action === "MONITOR") results.monitor.push
({term, ...final});
    else if (final.action === "NEGATIVE_ADD") results.negativ
e.push({term, ...final});
    else results.humanReview.push({term, ...final});
  }
  return results;
}
```
---
## Output Schema
```typescript
interface ClassifiedTerm {
  term: SearchTerm;
  action: "KEEP" | "MONITOR" | "NEGATIVE_ADD" | "HUMAN_REVIE
W" | "SKIP";
  category: string;
  rationale: string;
  confidence?: number;
  matchType?: "BROAD" | "PHRASE" | "EXACT";
  suggestedNegative?: string;
Negative Keyword AI (v6 Architecture)

  overrideReason?: string;
}
```
---
## Cost Summary
| Metric | Without Pipeline | With Pipeline |
|--------|------------------|---------------|
| Terms to AI | 100% | ~40-60% |
| AI cost | $2.50/1000 terms | $1.00/1000 terms |
| False positives | Higher | Lower (guardrails) |
| Converting terms negated | Possible | Never (triple protect
ion) |
**Key wins:**
- 40-60% AI cost reduction
- Zero converting terms ever negated (Step 1 + Step 7.1)
- Brand terms never negated (Step 1 + Step 7.2)
- Competitors auto-negated mechanically (Step 2.5)
- Cross-modality auto-negated mechanically (Step 3.5)
- Alternative-seekers protected (Step 4 + Step 7.5)
- Low-value noise filtered (Step 5)
📥 Google Apps Script Code
/******************************************************
 * Negative Keyword AI — Chain Architecture (v6.1.0)
 *
 * v6.1.0 ENHANCEMENTS:
 * - Executive Summary with Spend at Risk at top of output
 * - Confidence stars visualization (★★★★★)
 * - What's Next guidance section at bottom
 * - Data validation before analysis starts
Negative Keyword AI (v6 Architecture)

 * - Parallel API calls (3x faster!) using fetchAll()
 * - Larger batch sizes (60 terms per batch)
 * - More aggressive mechanical filtering
 *
 * ARCHITECTURE:
 * ┌─────────────────────────────────────────────────────┐
 * │         MECHANICAL PRE-PROCESSING (Steps 1-5)      │
 * │  Step 1: Conversion & Brand Protection → KEEP      │
 * │  Step 2: Primary Service Flagging → softProtected  │
 * │  Step 3: Universal Patterns → NEGATE (unprotected) │
 * │  Step 4: Alternative-Seeker Detection → Flag       │
 * │  Step 5: Low-Value Filtering → SKIP                │
 * └─────────────────────────────────────────────────────┘
 *                         ↓
 *               ~40-60% of terms remain
 *                         ↓
 * ┌─────────────────────────────────────────────────────┐
 * │              AI ANALYSIS (Step 6)                   │
 * │       Single AI call for ambiguous terms only      │
 * └─────────────────────────────────────────────────────┘
 *                         ↓
 * ┌─────────────────────────────────────────────────────┐
 * │         MECHANICAL POST-PROCESSING (6.5 & 7)       │
 * │  Step 6.5: CPC Context Enrichment                  │
 * │  Step 7: Final guardrails & override tracking      │
 * └─────────────────────────────────────────────────────┘
 ******************************************************/
/* ===== Runtime & Batching Constants ===== */
const NK_MAX_RUNTIME_MS  = 280000;
const NK_BATCH_SIZE      = 30;  // 30 terms per batch - reduce
d to prevent truncation (was 40)
// NK_PARALLEL_BATCHES now calculated dynamically based on ve
ndor rate limits
const NK_DP             = PropertiesService .getDocumentProper
ties();
Negative Keyword AI (v6 Architecture)

/* ===== Shared Color Definitions (Single Source of Truth) ==
=== */
const ACTION_COLORS  = {
  "NEGATIVE_ADD" : "#f8b4b4" ,  // Red - needs action
  "HUMAN_REVIEW" : "#fef08a" ,  // Yellow - needs review
  "MONITOR" : "#fed7aa" ,       // Orange - watch
  "KEEP": "#86efac" ,          // Green - good
  "SKIP": "#d1d5db"            // Gray - filtered
};
/* ===== Get Parallel Batch Count (rate-limit aware) ===== */
function  getParallelBatchCount_ (cfg) {
  // User can override in config
  if(cfg.parallel_calls && Number(cfg.parallel_calls ) > 0) {
    return Math.min(Number(cfg.parallel_calls ), 5); // Max 5  
parallel
  }
  const vendor = String(cfg.api_vendor || "openai" ).toLowerCa
se();
  // Anthropic default tier: 8,000 output tokens/min - MUST u
se 1 parallel call
  // Even 1 call with max_tokens:8192 nearly maxes the limit
  // For speed, users should switch to Gemini (1M+ tokens/min  
free!)
  if(vendor === "anthropic" ) {
    return 1;
  }
  // Gemini has VERY generous rate limits (1M+ tokens/min on  
free tier!)
  // This is by far the fastest option for most users
  if(vendor === "gemini" ) {
    return 4;
Negative Keyword AI (v6 Architecture)

  }
  // OpenAI typically has decent rate limits
  return 3;
}
/* ===== Competitor/Device Patterns (from v5.3.1) ===== */
const COMPETITOR_PATTERNS  = [
  /\bsono\s?bello\b /i,
  /\bcool\s?sculpt(?:ing|ure)?\b /i,
  /\bemsculpt\b(?!\s*neo\s*deals) /i,
  /\btru\s?sculpt\b /i,
  /\blipo\s?cavitation\b|\bcavitation\s+(?:rf|and\s*radio\s*f
requency)\b|\bultrasonic\s*cavitation\b /i,
  /\binmode\s*fx\b|\bbodytite\b|\baccutite\b|\bface?tite\b|\b
morpheus8\b /i,
  /\bsculpsure\b|\bvanquish\b|\bzerona\b|\bv\s?shape\b|\bvela
shape\b|\bcooltech\b /i,
  /\blipolytic\s?injections\b|\bfat[-\s]?dissolving\b|\bk?ybe
lla\b/i,
  /\bcryolipolysis\b|\bcryoslimming\b|\bfat\s*freez /i,
  /\bonda\s*laser\b|\bemerald\s*laser\b /i,
  /\bemslim\b|\btrisculpt\b /i
];
/* ===== Industry Synonym Groups ===== */
const INDUSTRY_SYNONYMS  = {
  medical_aesthetics : [
    ["liposuction" , "lipo"],
    ["smart lipo" , "laser lipo" , "lipo laser" , "laser liposuc
tion"],
    ["tummy tuck" , "abdominoplasty" ],
    ["coolsculpting" , "coolsculpt" , "cool sculpting" ],
    ["brazilian butt lift" , "bbl"],
    ["rhinoplasty" , "nose job" ],
    ["blepharoplasty" , "eyelid surgery" ],
Negative Keyword AI (v6 Architecture)

    ["botox", "botulinum toxin" ],
    ["breast augmentation" , "breast implants" , "boob job" ],
    ["facelift" , "face lift" , "rhytidectomy" ],
    ["mommy makeover" , "mommy make over" ]
  ],
  dental: [
    ["dental implants" , "implants" , "tooth implants" ],
    ["invisalign" , "clear aligners" ],
    ["veneers" , "dental veneers" , "porcelain veneers" ],
    ["root canal" , "endodontic" ],
    ["teeth whitening" , "tooth whitening" , "bleaching" ],
    ["dentures" , "false teeth" ],
    ["dental crown" , "tooth crown" , "cap"]
  ],
  legal: [
    ["personal injury" , "pi"],
    ["car accident" , "auto accident" , "vehicle accident" ],
    ["slip and fall" , "premises liability" ],
    ["workers comp" , "workers compensation" , "workman's com
p"],
    ["wrongful death" , "fatal accident" ],
    ["medical malpractice" , "medical negligence" ],
    ["truck accident" , "18 wheeler accident" , "semi acciden
t"]
  ],
  hvac: [
    ["air conditioning" , "ac", "a/c"],
    ["heating" , "furnace" ],
    ["hvac", "heating and cooling" ],
    ["ductless" , "mini split" , "mini-split" ],
    ["heat pump" , "heatpump" ]
  ],
  home_services : [
    ["plumber" , "plumbing" ],
    ["electrician" , "electrical" ],
    ["roofing" , "roofer" , "roof repair" ],
Negative Keyword AI (v6 Architecture)

    ["remodel" , "remodeling" , "renovation" ],
    ["handyman" , "handy man" ]
  ],
  ecommerce : [
    ["buy", "purchase" ],
    ["shop", "store"],
    ["order", "checkout" ]
  ],
  events: [
    ["hen party" , "hen do" , "bachelorette party" , "bacheloret
te"],
    ["stag party" , "stag do" , "bachelor party" ],
    ["wedding" , "bridal" ]
  ]
};
/* ===== Industry Detection Patterns ===== */
const INDUSTRY_SIGNALS  = {
  medical_aesthetics : /\b(lipo(?:suction)?|botox|filler|cools
culpt|tummy tuck|facelift|rhinoplasty|bbl|mommy makeover|plas
tic surg|cosmetic surg|breast augment|body contour) /i,
  dental: /\b(dental|dentist|implant|veneer|invisalign|orthod
ont|root canal|crown|bridge|teeth|tooth) /i,
  legal: /\b(lawyer|attorney|law firm|personal injury|acciden
t|lawsuit|legal|litigation|malpractice) /i,
  hvac: /\b(hvac|air condition|heating|cooling|furnace|ac rep
air|ductless|heat pump) /i,
  home_services : /\b(plumb|electric|roof|remodel|renovation|c
ontractor|handyman|landscap) /i,
  ecommerce : /\b(shop|store|buy|purchase|order|shipping|cart|
checkout|product) /i,
  events: /\b(party|event|hen do|stag do|bachelorette|bachelo
r|wedding|celebration) /i
};
/* ===== Universal Exclusion Patterns (Step 3) ===== */
Negative Keyword AI (v6 Architecture)

const UNIVERSAL_PATTERNS  = {
  employment : {
    pattern: /\b(jobs?|careers?|hiring|recruitment|vacanc(?:y
|ies)|salary|salaries|resume|cv|employment|work from home|wfh
|intern(?:ship)?s?)\b /i,
    matchType : "BROAD",
    category : "Definite Waste" ,
    reason: "Employment intent"
  },
  navigation : {
    pattern: /\b(login|log in|sign in|signin|account|portal|d
ashboard|reset password|my account)\b /i,
    matchType : "PHRASE" ,
    category : "Definite Waste" ,
    reason: "Navigation intent"
  },
  forum: {
    pattern: /\b(reddit|quora|forum|forums)\b /i,
    matchType : "BROAD",
    category : "Likely Waste" ,
    reason: "Forum research"
  },
  diy: {
    pattern: /\b(diy|do it yourself|homemade|home remedy|at h
ome)\b/i,
    matchType : "PHRASE" ,
    category : "Likely Waste" ,
    reason: "DIY intent"
  },
  education : {
    pattern: /\b(certification|certified|degree|how to become
|become a|training course|classes|school)\b /i,
    matchType : "PHRASE" ,
    category : "Likely Waste" ,
    reason: "Career/education intent"
  },
Negative Keyword AI (v6 Architecture)

  informational : {
    pattern: /\b(what is|what are|definition|meaning|wiki|wik
ipedia|youtube|video|images?|photos?|pictures?)\b /i,
    matchType : "PHRASE" ,
    category : "Likely Waste" ,
    reason: "Informational/media intent"
  },
  free_seekers : {
    pattern: /\b(free|freebie|gratis|no cost|complimentary)
\b/i,
    matchType : "BROAD",
    category : "Likely Waste" ,
    reason: "Free-seeker intent"
  },
  complaints : {
    pattern: /\b(complaints?|lawsuit|sue|scam|rip\s*off|fraud
|warning|danger|death|died|gone wrong|horror|nightmare|regre
t)\b/i,
    matchType : "PHRASE" ,
    category : "Likely Waste" ,
    reason: "Negative research intent"
  },
  unqualified : {
    pattern: /\b(cheap|cheapest|bargain|discount|coupon|promo  
code|groupon|deal of)\b /i,
    matchType : "PHRASE" ,
    category : "Potential Waste" ,
    reason: "Discount-seeker (check price_positioning)"
  },
  wrong_intent : {
    pattern: /\b(sell|selling|for sale|buy used|second hand|d
onate|donation)\b /i,
    matchType : "PHRASE" ,
    category : "Definite Waste" ,
    reason: "Seller/resale intent"
  },
Negative Keyword AI (v6 Architecture)

  location_research : {
    pattern: /\b(in my area|near me locations|locations near|
find a|where can i find)\b /i,
    matchType : "EXACT",
    category : "Watch",
    reason: "Location research - may convert"
  }
};
/* ===== AI System Prompt (Optimized for Chain Architecture)  
===== */
const CHAIN_SYSTEM_PROMPT  = `ROLE: Search term classifier for  
Google Ads negative keyword analysis.
TASK: Classify EVERY term into one category and recommend act
ion.
CRITICAL REQUIREMENTS:
1. You MUST return EXACTLY the same number of recommendations  
as input terms - no skipping!
2. You MUST return each "term" field EXACTLY as provided - sa
me spelling, same case, same punctuation.
3. If you're unsure about a term, classify it as HUMAN_REVIEW  
- do NOT skip it.
4. Every input term MUST appear in your output recommendation
s array.
CATEGORIES (in order of waste → value):
- Definite Waste: Zero alignment, completely wrong intent → N
EGATIVE_ADD
- Likely Waste: Strong mismatch signals, low conversion poten
tial → NEGATIVE_ADD
- Potential Waste: Some waste signals but borderline → NEGATI
VE_ADD (lower confidence)
- Questionable: Mixed signals, genuinely unclear → MONITOR
- Watch: Relevant but deserves monitoring → MONITOR
Negative Keyword AI (v6 Architecture)

- Good: Solid service alignment, reasonable intent → KEEP
- Optimal: Perfect match, strong commercial intent → KEEP
INTERPRETING FLAGS (critical):
Each term includes flags from mechanical pre-processing. Use  
them:
| Flag | Meaning | Guidance |
|------|---------|----------|
| softProtected: true | Contains primary service keyword | Be  
VERY cautious negating. Needs strong counter-signal. |
| commercialIntent: true | Has buying signals (best, cost, ne
ar me) | Weight toward KEEP/Watch. Commercial intent = value.  
|
| alternativeSeeker: true | Comparison shopping (vs, alternat
ive) | Usually valuable even if mentions competitor. |
| conflict.patternMatched | Hit waste pattern BUT is protecte
d | Weigh both signals carefully. |
ADDITIONAL CONTEXT:
If "custom_context" is provided, it contains user notes — com
petitor names, campaign goals, special instructions. Factor t
his into your analysis.
CLASSIFICATION PRINCIPLES:
1. Intent over keywords — what does the human actually want?
2. Service alignment — does this match what advertiser offer
s?
3. Competitor identification — recognize competitor brands/tr
eatments. If allow_competitor_terms=false, competitors are Li
kely Waste (unless alternativeSeeker=true).
4. Cross-modality — if they want service NOT offered, it's wa
ste regardless of other signals.
5. CONSISTENCY RULE: Treat synonymous terms identically. Exam
ples: "hen party" = "hen do" = "bachelorette party".
6. When uncertain, MONITOR. Don't negate borderline traffic.
Negative Keyword AI (v6 Architecture)

MATCH TYPE SELECTION (when NEGATIVE_ADD):
- EXACT: Very specific phrase, don't want to block variants
- PHRASE: Block this phrase in any context
- BROAD: Block this concept entirely (most common)
suggestedNegative: Extract the core waste keyword.
CONFIDENCE:
- 0.8+: Clear signals, confident
- 0.6-0.8: Reasonable confidence
- <0.6: Uncertain → output action: "HUMAN_REVIEW"
CRITICAL OUTPUT FORMAT:
- Return ONLY raw JSON - no markdown, no \`\`\`, no explanati
on text
- Start your response with { and end with }
- Schema: {"recommendations": [{"term": "...", "category":  
"...", "action": "KEEP|MONITOR|NEGATIVE_ADD|HUMAN_REVIEW", "m
atch_type": "BROAD|PHRASE|EXACT|NONE", "level": "CAMPAIGN|AD_
GROUP|NONE", "suggested_negative": "...", "rationale": "Brief  
why (max 20 words)", "confidence": 0.85, "signals": []}]} `;
/* ===== UI Helpers ===== */
function  hasUi_(){ try{ SpreadsheetApp .getUi(); return true; 
}catch(e){ return false; } }
// NON-BLOCKING toast - use for success messages, doesn't cau
se "Working..." spinner
function  uiSuccess_ (msg, title){
  SpreadsheetApp .flush();
  try { SpreadsheetApp .getActive ().toast(msg, title || "✅ Do
ne", 10); }
  catch(e) { Logger.log("[SUCCESS] "  + msg); }
}
Negative Keyword AI (v6 Architecture)

// BLOCKING alert - use ONLY for errors that must be acknowle
dged
// ALWAYS flushes to clear "Working..." spinner after user di
smisses
function  uiAlert_ (msg){
  if(hasUi_()) {
    SpreadsheetApp .getUi().alert(msg);
    SpreadsheetApp .flush(); // Clear spinner after alert dism
issed
  } else {
    Logger.log("[ALERT] " +msg);
  }
}
function  rebuildMenu_ (){
  try{
    SpreadsheetApp .getUi().createMenu ("Neg Keyword Agent 🦹 ")
      .addItem("🔧 Setup All Templates" ,"setupAll" )
      .addSeparator ()
      .addItem("🔄 Normalize Pasted Data" ,"normalizeGoogleAds
Export")
      .addItem("✨ Auto-Fill Config with AI" ,"letAIAutofillCo
ntext")
      .addSeparator ()
      .addItem("🔑 Test API Connection" ,"testApiConnection" )
      .addItem("▶ Run Agent" ,"runAnalysis" )
      .addItem("⏹ STOP Everything" ,"stopEverything" )
      .addItem("🔄 Restart" ,"startFresh" )
      .addSeparator ()
      .addItem("📊 Export Negatives CSV" ,"makeNegativesCSV" )
      .addSeparator ()
      .addSubMenu (SpreadsheetApp .getUi().createMenu ("More")
        .addItem("View Pipeline Statistics" ,"viewPipelineStat
s")
        .addItem("Sort Output by severity" ,"sortOutputBySever
ity")
Negative Keyword AI (v6 Architecture)

        .addItem("Clear Current Output Tab" ,"clearOutput" )
        .addItem("Refresh Config template only" ,"createOrRefr
eshConfigTemplate" )
        .addItem("Refresh Data templates only" ,"createOrRefre
shDataTemplates" )
        .addItem("Create Instructions tab" ,"createOrRefreshIn
structions" ))
      .addToUi();
  }catch(e){ Logger.log("Menu build skipped (no UI)." ); }
}
function  onOpen(){ rebuildMenu_ (); }
/* ===== Setup ===== */
function  setupAll (){
  const ss = SpreadsheetApp .getActive ();
  createOrRefreshConfigTemplate ();
  createOrRefreshDataTemplates ();
  rebuildMenu_ ();
  uiSuccess_ ("Config and Terms templates created. Reload shee
t to refresh menu." , "✅ Setup Complete" );
}
/* ===== Industry Detection ===== */
function  detectIndustry_ (context) {
  if (context.industry ) return context .industry ;
  const keywords = [
    ...(context.primary_service_keywords || []),
    ...(context.services_offered || [])
  ].map(k => k.toLowerCase ()).join(' ');
  for (const [industry , pattern ] of Object.entries(INDUSTRY_S
IGNALS)) {
    if (pattern.test(keywords )) return industry ;
Negative Keyword AI (v6 Architecture)

  }
  return null;
}
/* ===== Synonym Management ===== */
function  loadSynonyms_ (context) {
  const industry = detectIndustry_ (context);
  const userSynonyms = context .synonym_groups || [];
  const industrySynonyms = industry ? (INDUSTRY_SYNONYMS [indu
stry] || []) : [];
  return deduplicateSynonymGroups_ ([...userSynonyms , ...indus
trySynonyms ]);
}
function  deduplicateSynonymGroups_ (groups) {
  const seen = new Set();
  const result = [];
  for (const group of groups) {
    const key = group.map(s => s.toLowerCase ()).sort().join
('|');
    if (!seen.has(key)) {
      seen.add(key);
      result.push(group);
    }
  }
  return result;
}
function  expandWithSynonyms_ (keywords , synonymGroups ) {
  const expanded = new Set(keywords .map(k => k.toLowerCase
()));
  for (const kw of keywords ) {
    const kwLower = kw.toLowerCase ();
    for (const group of synonymGroups ) {
      if (group.some(s => s.toLowerCase () === kwLower )) {
Negative Keyword AI (v6 Architecture)

        group.forEach(s => expanded .add(s.toLowerCase ()));
      }
    }
  }
  return Array.from(expanded );
}
/* ===== Helper Functions ===== */
function  escapeRegex_ (string) {
  return string.replace(/[.*+?^${}()|[\]\\] /g, '\\$&');
}
function  levenshteinDistance_ (a, b) {
  const matrix = Array(b.length + 1).fill(null)
    .map(() => Array(a.length + 1).fill(null));
  for (let i = 0; i <= a.length; i++) matrix[0][i] = i;
  for (let j = 0; j <= b.length; j++) matrix[j][0] = j;
  for (let j = 1; j <= b.length; j++) {
    for (let i = 1; i <= a.length; i++) {
      const indicator = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[j][i] = Math.min(
        matrix[j][i - 1] + 1,
        matrix[j - 1][i] + 1,
        matrix[j - 1][i - 1] + indicator
      );
    }
  }
  return matrix[b.length][a.length];
}
function  isBrandTerm_ (term, context ) {
  const termLower = term.toLowerCase ();
  return (context.brand_terms || []).some(brand => {
    const brandLower = brand.toLowerCase ();
    if (new RegExp(`\\b${escapeRegex_ (brandLower )}\\b`).test
(termLower )) return true;
Negative Keyword AI (v6 Architecture)

    if (brand.length >= 5) {
      const words = termLower .split(/\s+/);
      return words.some(w => levenshteinDistance_ (w, brandLow
er) <= 2);
    }
    return false;
  });
}
/* ===== Primary Service Variant Detection (from v5.3.1) ====
= */
function  isPrimaryServiceVariant_ (term) {
  const normalized = term.toLowerCase ().replace(/\s+/g, " ").
trim();
  const patterns = [
    /\b(smart\s*lipo|laser\s*lipo|lipo\s*laser|lipolaser|lase
r\s*liposuction)\b /,
    /\b(minimally?\s*invasive\s*lipo|micro\s*laser\s*lipo)
\b/,
    /\b(endolaser|laser\s*lipolysis)\b /,
    /\b(lipo\s*360|360\s*lipo)\b /
  ];
  return patterns .some(p => p.test(normalized ));
}
function  isCompetitorTerm_ (term) {
  const termLower = term.toLowerCase ();
  return COMPETITOR_PATTERNS .some(rx => rx.test(termLower ));
}
function  extractCompetitorKeyword_ (term) {
  const termLower = term.toLowerCase ();
  // Try to extract the specific competitor name
  const competitors = [
    /\b(sono\s?bello)\b /i,
    /\b(cool\s?sculpt(?:ing)?)\b /i,
Negative Keyword AI (v6 Architecture)

    /\b(emsculpt)\b /i,
    /\b(tru\s?sculpt)\b /i,
    /\b(sculpsure)\b /i,
    /\b(kybella)\b /i,
    /\b(morpheus8)\b /i,
    /\b(bodytite)\b /i,
    /\b(velashape)\b /i
  ];
  for (const rx of competitors ) {
    const match = termLower .match(rx);
    if (match) return match[1].replace(/\s+/g, ' ').trim();
  }
  return termLower ;
}
/* ===== Threshold Filtering ===== */
function  filterTermsForAnalysis_ (terms, cfg) {
  const minC = Number(cfg.min_clicks_to_analyze ?? 1);
  const minI = Number(cfg.min_impressions_to_analyze ?? 20);
  return terms.filter(t => {
    const clicks = Number(t.clicks || 0);
    const imps = Number(t.impressions || 0);
    return (clicks >= minC) || (imps >= minI);
  });
}
/* ===== Top N Prioritization ===== */
function  selectTopTerms_ (terms, cfg) {
  let metric = (cfg.select_metric || "cost").toLowerCase ();
  if (!["cost", "clicks" , "impressions" ].includes (metric)) me
tric = "cost";
  return terms.slice().sort((a, b) => {
    const av = Number(a[metric] || 0), bv = Number(b[metric] 
|| 0);
    if (bv !== av) return bv - av;
Negative Keyword AI (v6 Architecture)

    if (Number(b.clicks || 0) !== Number(a.clicks || 0)) retu
rn Number(b.clicks || 0) - Number(a.clicks || 0);
    if (Number(b.cost || 0) !== Number(a.cost || 0)) return N
umber(b.cost || 0) - Number(a.cost || 0);
    return Number(b.impressions || 0) - Number(a.impressions 
|| 0);
  });
}
/* ===== Cross-Modality Check ===== */
function  checkCrossModality_ (term, expandedOffered , expandedA
djacents , cfg) {
  const termLower = (term.term || "").toLowerCase ();
  // Check if term mentions an adjacent service (different ca
mpaign)
  const hitsAdjacent = expandedAdjacents .some(tok =>
    tok && new RegExp(`\\b${escapeRegex_ (tok)}\\b`, 'i').test
(termLower )
  );
  // Check if term also mentions a primary/offered service
  const hitsPrimary = expandedOffered .some(tok =>
    tok && new RegExp(`\\b${escapeRegex_ (tok)}\\b`, 'i').test
(termLower )
  ) || /\blipo|liposuction\b /i.test(termLower );
  // If it mentions adjacent but NOT primary → cross-modality  
waste
  if (hitsAdjacent && !hitsPrimary ) {
    // Find which adjacent service was matched
    const matched = expandedAdjacents .find(tok =>
      tok && new RegExp(`\\b${escapeRegex_ (tok)}\\b`, 'i').te
st(termLower )
    );
    return {
Negative Keyword AI (v6 Architecture)

      isWaste: true,
      keyword: matched || termLower ,
      reason: "Different modality from this ad group's focus"
    };
  }
  return { isWaste: false };
}
/* ===== STEP 1: Conversion & Brand Protection ===== */
function  step1_conversionBrandProtection_ (term, context ) {
  // Click-through conversions ≥ 1 → Instant KEEP
  if ((term.conversions || 0) >= 1) {
    return {
      action: "KEEP",
      category : term.conversions >= 3 ? "Optimal"  : "Good",
      rationale : `Converting term ( ${term.conversions } conv)
`,
      signals: ["conversion_protection" ],
      skipRemaining : true
    };
  }
  // View-through only → KEEP but flag as Watch
  if ((term.view_through_conversions || 0) >= 1 && (term.conv
ersions || 0) < 1) {
    return {
      action: "KEEP",
      category : "Watch",
      rationale : `View-through conversions ( ${term.view_throu
gh_conversions })`,
      signals: ["view_through_protection" ],
      skipRemaining : true
    };
  }
Negative Keyword AI (v6 Architecture)

  // Brand match (including misspellings for 5+ char brands)
  const termLower = (term.term || term.search_term || "").toL
owerCase ();
  for (const brand of (context.brand_terms || [])) {
    const brandLower = brand.toLowerCase ();
    // Exact word boundary match
    if (new RegExp(`\\b${escapeRegex_ (brandLower )}\\b`).test
(termLower )) {
      return {
        action: "KEEP",
        category : "Good",
        rationale : "Brand term" ,
        signals: ["brand_protection" ],
        skipRemaining : true
      };
    }
    // Misspelling tolerance (Levenshtein ≤ 2 for brands 5+ c
hars)
    if (brand.length >= 5) {
      const words = termLower .split(/\s+/);
      if (words.some(w => levenshteinDistance_ (w, brandLower ) 
<= 2)) {
        return {
          action: "KEEP",
          category : "Good",
          rationale : "Brand term (misspelling)" ,
          signals: ["brand_misspelling_protection" ],
          skipRemaining : true
        };
      }
    }
  }
  return { skipRemaining : false };
}
Negative Keyword AI (v6 Architecture)

/* ===== Plural/Singular Variant Matching ===== */
function  matchesKeywordFuzzy_ (term, keyword ) {
  // Generates singular/plural variants and checks if term ma
tches any
  const termClean = term.toLowerCase ().trim();
  const kwClean = keyword .toLowerCase ().trim();
  // Generate variants for both term and keyword
  const getVariants  = (s) => {
    const variants = [s];
    // Simple plural handling: add/remove trailing 's'
    if (s.endsWith ('s')) {
      variants .push(s.slice(0, -1)); // beds → bed
    } else {
      variants .push(s + 's'); // bed → beds
    }
    // Handle 'ies' → 'y' (e.g., queries → query)
    if (s.endsWith ('ies')) {
      variants .push(s.slice(0, -3) + 'y');
    } else if (s.endsWith ('y') && !s.endsWith ('ay') && !s.end
sWith('ey') && !s.endsWith ('oy') && !s.endsWith ('uy')) {
      variants .push(s.slice(0, -1) + 'ies');
    }
    return variants ;
  };
  const kwVariants = getVariants (kwClean);
  // Check if term contains any variant of the keyword
  for (const variant of kwVariants ) {
    if (new RegExp(`\\b${escapeRegex_ (variant)}\\b`).test(ter
mClean)) {
      return true;
    }
  }
  return false;
Negative Keyword AI (v6 Architecture)

}
/* ===== STEP 2: Primary Service Flagging ===== */
function  step2_primaryServiceFlag_ (term, expandedKeywords , ex
pandedServices ) {
  const termLower = (term.term || term.search_term || "").toL
owerCase ();
  let softProtected = false;
  let matchedService = null;
  // Check expanded primary keywords (includes synonyms) with  
plural/singular matching
  for (const kw of expandedKeywords ) {
    if (matchesKeywordFuzzy_ (termLower , kw)) {
      softProtected = true;
      matchedService = "primary_keyword" ;
      break;
    }
  }
  // Check expanded services offered (includes synonyms) with  
plural/singular matching
  if (!softProtected ) {
    for (const svc of expandedServices ) {
      if (matchesKeywordFuzzy_ (termLower , svc)) {
        softProtected = true;
        matchedService = "service_offered" ;
        break;
      }
    }
  }
  // Commercial intent modifiers
  const COMMERCIAL  = /\b(best|top|vs|versus|compare|cost|pric
e|pricing|near me|nearby|reviews?|quotes?|consultation)\b /i;
  const commercialIntent = COMMERCIAL .test(termLower );
Negative Keyword AI (v6 Architecture)

  return {
    softProtected ,
    matchedService ,
    commercialIntent
  };
}
/* ===== STEP 3: Universal Exclusion Patterns ===== */
function  step3_universalPatterns_ (term, flags) {
  const termLower = (term.term || term.search_term || "").toL
owerCase ();
  for (const [key, config] of Object.entries(UNIVERSAL_PATTER
NS)) {
    if (config.pattern.test(termLower )) {
      // Protected terms → route to AI instead of auto-negate
      if (flags.softProtected ) {
        return {
          action: "NEEDS_AI" ,
          conflict : {
            protectedBy : flags.matchedService ,
            patternMatched : key,
            reason: config.reason
          }
        };
      }
      // Unprotected → auto-negate
      return {
        action: "NEGATIVE_ADD" ,
        category : config.category ,
        match_type : config.matchType ,
        level: "CAMPAIGN" ,
        suggested_negative : extractNegativeKeyword_ (termLowe
r, key),
        rationale : config.reason,
Negative Keyword AI (v6 Architecture)

        signals: [`pattern: ${key}`],
        confidence : 0.95,
        skipRemaining : true
      };
    }
  }
  return { action: "CONTINUE"  };
}
function  extractNegativeKeyword_ (term, patternKey ) {
  // Extract the specific waste keyword based on pattern type
  const patterns = {
    employment : /\b(jobs?|careers?|hiring|salary|resume|emplo
yment)\b /i,
    navigation : /\b(login|sign in|account|portal|dashboard)
\b/i,
    forum: /\b(reddit|quora|forum)\b /i,
    diy: /\b(diy|do it yourself)\b /i,
    education : /\b(certification|degree|become a)\b /i,
    informational : /\b(what is|definition|wiki)\b /i
  };
  const pattern = patterns [patternKey ];
  if (pattern) {
    const match = term.match(pattern);
    if (match) return match[1].toLowerCase ();
  }
  return term;
}
/* ===== STEP 4: Alternative-Seeker Detection ===== */
function  step4_alternativeSeekers_ (term) {
  const termLower = (term.term || term.search_term || "").toL
owerCase ();
Negative Keyword AI (v6 Architecture)

  // Direct alternative signals
  const ALTERNATIVE_SIGNALS  = /\b(alternative|instead of|bett
er than|vs|versus|compared to|switch(?:ing)? from|mov(?:e|in
g) from|replace(?:ment)?|similar to|substitute)\b /i;
  // "like X but" pattern
  const LIKE_BUT_PATTERN  = /like .+ but /i;
  if (ALTERNATIVE_SIGNALS .test(termLower ) || LIKE_BUT_PATTER
N.test(termLower )) {
    return {
      alternativeSeeker : true,
      note: "Comparison shopper — likely valuable"
    };
  }
  return { alternativeSeeker : false };
}
/* ===== STEP 5: Low-Value Filtering ===== */
function  step5_lowValueFilter_ (term, context ) {
  const avgCpc = context .avg_cpc || 5;
  const dateRangeDays = context .date_range_days || 30;
  const impressions = term.impressions || 0;
  const clicks = term.clicks || 0;
  const cost = term.cost || 0;
  const impressionsPerDay = impressions / dateRangeDays ;
  const dailyThreshold = 10 / 30;  // 0.33/day baseline
  // Single impression — always skip
  if (impressions === 1) {
    return { action: "SKIP", reason: "Single impression"  };
  }
  // No clicks + spend below half a click
Negative Keyword AI (v6 Architecture)

  if (clicks === 0 && cost < avgCpc * 0.5) {
    return { action: "SKIP", reason: "No clicks, trivial spen
d" };
  }
  // No clicks + below daily impression threshold
  if (clicks === 0 && impressionsPerDay < dailyThreshold ) {
    return { action: "SKIP", reason: "Below impression thresh
old" };
  }
  // Single click with trivial spend (< 5% of avg CPC)
  if (clicks === 1 && cost < avgCpc * 0.05) {
    return { action: "SKIP", reason: "Single click, trivial s
pend" };
  }
  return { action: "CONTINUE"  };
}
/* ===== STEP 6.5: CPC Context Enrichment ===== */
function  step6_5_cpcEnrichment_ (term, result, context ) {
  const clicks = term.clicks || 0;
  const cost = term.cost || 0;
  const impressions = term.impressions || 0;
  const avgCpc = context .avg_cpc || 0;
  const targetCpa = context .target_cpa || null;
  const expectedConvRate = context .expected_conv_rate || nul
l;
  let enriched = false;
  let notes = [];
  // No clicks — check if high impressions (ad relevance issu
e)
  if (clicks === 0) {
Negative Keyword AI (v6 Architecture)

    if (impressions >= 50) {
      notes.push(`No clicks across ${impressions } impr — chec
k ad relevance. `);
      enriched = true;
    }
    if (notes.length) {
      result.rationale = (result.rationale || "") + " | " + n
otes.join(" ");
    }
    return { result, enriched };
  }
  // Guard against division issues
  if (cost <= 0) return { result, enriched : false };
  const termCpc = cost / clicks;
  // If we have target CPA + conversion rate → use break-even  
math
  if (targetCpa && expectedConvRate ) {
    const breakEven = targetCpa * expectedConvRate ;
    if (termCpc <= breakEven * 0.5) {
      notes.push(`CPC $${termCpc.toFixed(2)} well below break
-even $${breakEven .toFixed(2)} — cheap to test. `);
      result.signals = result.signals || [];
      result.signals.push("cpc:below_break_even" );
    } else if (termCpc >= breakEven ) {
      notes.push(`CPC $${termCpc.toFixed(2)} above break-even  
$${breakEven .toFixed(2)} — monitor closely. `);
      result.signals = result.signals || [];
      result.signals.push("cpc:above_break_even" );
    }
    enriched = notes.length > 0;
  }
  // Fallback: compare to account average
  else if (avgCpc && avgCpc > 0) {
Negative Keyword AI (v6 Architecture)

    const ratio = termCpc / avgCpc;
    if (ratio <= 0.5) {
      notes.push(`CPC $${termCpc.toFixed(2)} is ${Math.round
((1-ratio)*100)}% below avg — cheap traffic. `);
      result.signals = result.signals || [];
      result.signals.push("cpc:low_vs_avg" );
      enriched = true;
    } else if (ratio >= 1.5) {
      notes.push(`CPC $${termCpc.toFixed(2)} is ${Math.round
((ratio-1)*100)}% above avg — premium traffic. `);
      result.signals = result.signals || [];
      result.signals.push("cpc:high_vs_avg" );
      enriched = true;
    }
  }
  if (notes.length) {
    result.rationale = (result.rationale || "") + " | " + not
es.join(" ");
  }
  return { result, enriched };
}
/* ===== STEP 7: Post-Processing Guardrails ===== */
function  step7_guardrails_ (term, result, flags, context ) {
  const termText = term.term || term.search_term || "";
  const termLower = termText .toLowerCase ();
  // 7.1: Conversion protection (final check)
  if (result.action === "NEGATIVE_ADD"  && (term.conversions |
| 0) >= 1) {
    return override_ (result, "KEEP", "Good", "Has conversion
s", "conversion_protection" );
  }
Negative Keyword AI (v6 Architecture)

  // 7.2: Brand protection (final check)
  if (result.action === "NEGATIVE_ADD"  && isBrandTerm_ (termTe
xt, context )) {
    return override_ (result, "KEEP", "Good", "Brand term" , "b
rand_protection" );
  }
  // 7.3: Primary service + commercial intent
  if (result.action === "NEGATIVE_ADD"  && flags.softProtected  
&& flags.commercialIntent ) {
    return override_ (result, "MONITOR" , "Watch", "Service + c
ommercial intent" , "service_commercial" );
  }
  // 7.4: Cross-modality enforcement
  const mentionsNotOffered = (context.services_not_offered || 
[]).some(s =>
    new RegExp(`\\b${escapeRegex_ (s.toLowerCase ())}\\b`).test
(termLower )
  );
  const mentionsOffered = (context.services_offered || []).so
me(s =>
    new RegExp(`\\b${escapeRegex_ (s.toLowerCase ())}\\b`).test
(termLower )
  );
  if (mentionsNotOffered && !mentionsOffered && result.action 
!== "NEGATIVE_ADD" ) {
    return override_ (result, "NEGATIVE_ADD" , "Definite Wast
e", "Service not offered" , "cross_modality" );
  }
  // 7.5: Alternative-seeker protection
  if (result.action === "NEGATIVE_ADD"  && flags.alternativeSe
eker) {
    return override_ (result, "MONITOR" , "Watch", "Alternative
-seeker" , "alt_seeker_protection" );
Negative Keyword AI (v6 Architecture)

  }
  return result;
}
function  override_ (result, action, category , reason, type) {
  return {
    ...result,
    action,
    category ,
    rationale : `OVERRIDE: ${reason}. Original: ${result.ratio
nale || 'N/A'}`,
    overrideReason : type,
    originalAction : result.action,
    originalCategory : result.category ,
    signals: [...(result.signals || []), `override: ${type}`]
  };
}
/* ===== Config Template ===== */
function  createOrRefreshConfigTemplate (){
  const ss = SpreadsheetApp .getActive ();
  const sh = ss.getSheetByName ("Config" ) || ss.insertSheet ("C
onfig");
  sh.clearContents ();
  sh.clearFormats ();
  // Unfreeze any existing frozen rows/columns before merging
  sh.setFrozenRows (0);
  sh.setFrozenColumns (0);
  // Row 1: Title
  sh.getRange (1,1,1,4).merge().setValue ("Negative Keyword AI  
— Configuration" );
  sh.getRange (1,1).setFontSize (14).setFontWeight ("bold").setB
ackground ("#4a86e8" ).setFontColor ("white");
Negative Keyword AI (v6 Architecture)

  // Row 2: Compact billing note
  sh.getRange (2,1,1,4).merge().setValue ("⚠  API billing is sep
arate from ChatGPT Plus/Claude Pro. Use ' 🔑  Test API Connecti
on' to verify setup." );
  sh.getRange (2,1).setBackground ("#fff3cd" ).setFontColor ("#85
6404").setWrap(true);
  // Row 3: Headers
  sh.getRange (3,1,1,4).setValues ([["Setting" , "Value", "Requi
red?", "Description" ]]);
  sh.getRange (3,1,1,4).setFontWeight ("bold").setBackground ("#
f3f3f3");
  const rows = [
    // === API SETTINGS === (row 4)
    ["🔑 API SETTINGS" , "", "", ""],
    ["api_vendor" , "gemini" , "Required" , "Choose: gemini, ope
nai, or anthropic" ],
    ["model", "gemini-2.5-flash" , "Required" , "See MODEL OPTI
ONS below for choices" ],
    ["api_key" , "<<ADD YOUR KEY>>" , "Required" , "Get key fro
m: aistudio.google.com/apikey" ],
    ["target_url" , "", "Required" , "Your website URL (e.g., h
ttps://example.com)" ],
    ["project_name" , "", "Required" , "Name for your output ta
b (e.g., Jan_Campaign)" ],
    ["", "", "", ""],
    // === BUSINESS CONTEXT === (row 12)
    ["📋 BUSINESS CONTEXT" , "", "", ""],
    ["brand_terms" , "", "Important" , "Your brand names — NEVE
R negated. Example: Acme, AcmeCo" ],
    ["services_offered" , "", "Important" , "What you sell. Exa
mple: coolsculpting, body contouring" ],
    ["primary_service_keywords" , "", "Important" , "This campa
Negative Keyword AI (v6 Architecture)

ign's focus — protected from negation" ],
    ["services_not_offered" , "", "Optional" , "What you DON'T  
offer. Example: liposuction, surgery" ],
    ["adjacent_services_offered" , "", "Optional" , "Related se
rvices you also offer (AI auto-fills)" ],
    ["locations_served" , "", "Optional" , "Your service areas.  
Example: Austin TX, Dallas TX" ],
    ["buyer_persona" , "", "Optional" , "Target customer descri
ption (AI auto-fills)" ],
    ["industry" , "", "Optional" , "Your industry (AI auto-fill
s from: ecommerce, medical_aesthetics, etc.)" ],
    ["price_positioning" , "", "Optional" , "premium, budget, o
r unsure (AI auto-fills)" ],
    ["funnel_target" , "", "Optional" , "BOFU, MOFU, or Full (A
I auto-fills)" ],
    ["custom_context" , "", "Optional" , "Any other notes: comp
etitors, goals, special rules..." ],
    ["", "", "", ""],
    // === FILTERING === (row 24)
    ["🔍 FILTERING (which terms to analyze)" , "", "", ""],
    ["min_clicks_to_analyze" , "1", "Optional" , "Skip terms wi
th fewer clicks than this" ],
    ["min_impressions_to_analyze" , "20", "Optional" , "For 0-c
lick terms: skip if fewer impressions" ],
    ["select_top_n" , "", "Optional" , "Analyze highest-spend t
erms first (leave blank = no reordering)" ],
    ["", "", "", ""],
    // === ADVANCED === (row 29)
    ["⚙  ADVANCED" , "", "", ""],
    ["allow_competitor_terms" , "no", "Optional" , "Include com
petitor brand searches? (yes/no)" ],
    ["target_cpa" , "", "Optional" , "Your target cost per acqu
isition ($)" ],
    ["auto_resume" , "yes", "Optional" , "Auto-continue if anal
Negative Keyword AI (v6 Architecture)

ysis times out? (yes/no)" ],
    ["", "", "", ""],
    // === MODEL REFERENCE === (row 34)
    ["💡 MODEL OPTIONS" , "", "", ""],
    ["GEMINI" , "gemini-2.5-flash" , "$0.15/1M" , "⭐ Recommende
d — great balance" ],
    ["", "gemini-3-pro-preview" , "$1.25/1M" , "Latest flagship  
(preview)" ],
    ["", "gemini-2.0-flash" , "$0.10/1M" , "Budget — fast & che
ap"],
    ["OPENAI" , "gpt-4o-mini" , "$0.15/1M" , "Budget option" ],
    ["", "gpt-4o" , "$5.00/1M" , "Great all-rounder" ],
    ["", "gpt-5.1" , "$10.00/1M" , "Latest flagship (Nov 202
5)"],
    ["ANTHROPIC" , "claude-3-5-haiku-latest" , "$1.00/1M" , "Bud
get option" ],
    ["", "claude-sonnet-4-20250514" , "$3.00/1M" , "Great all-r
ounder"],
    ["", "claude-opus-4-5-20251101" , "$15.00/1M" , "Latest fla
gship"]
  ];
  sh.getRange (4,1,rows.length,4).setValues (rows);
  // Section header styling (green headers) - MUST match actu
al row positions
  // Row 4=API, 11=Business, 24=Filtering, 29=Advanced
  const sectionRows = [4, 11, 24, 29];
  sectionRows .forEach(row => {
    sh.getRange (row,1,1,4).setBackground ("#34a853" ).setFontCo
lor("white").setFontWeight ("bold");
  });
  // Model reference section - blue header + light blue backg
round (row 34)
Negative Keyword AI (v6 Architecture)

  sh.getRange (34,1,1,4).setBackground ("#1a73e8" ).setFontColor
("white").setFontWeight ("bold");
  sh.getRange (35,1,9,4).setBackground ("#e8f0fe" ); // 9 model  
rows
  // Required field styling (red text) - rows 5-9
  sh.getRange (5,3,5,1).setFontColor ("#cc0000" ).setFontWeight
("bold");
  // Important field styling (blue text) - rows 12-14
  sh.getRange (12,3,3,1).setFontColor ("#1a73e8" ).setFontWeight
("bold");
  // Custom context row - make it taller for multi-line input  
(row 22)
  sh.setRowHeight (22, 50);
  // Column widths
  sh.setColumnWidths (1,1,200);
  sh.setColumnWidths (2,1,250);
  sh.setColumnWidths (3,1,90);
  sh.setColumnWidths (4,1,380);
  // Wrap and freeze
  sh.getRange (1,1,rows.length+3,4).setWrap(true);
  sh.setFrozenRows (3);
  uiSuccess_ ("Config ready! Add your api_key and target_url,  
then run Test API Connection." , "✅ Config Ready" );
}
/* ===== Data Templates ===== */
function  createOrRefreshDataTemplates (){
  const ss = SpreadsheetApp .getActive ();
  const terms = getOrCreate_ (ss,"Terms");
  const raw   = getOrCreate_ (ss,"RawExport" );
Negative Keyword AI (v6 Architecture)

  terms.clearContents ();
  terms.appendRow (["term","impressions" ,"clicks" ,"cost","conv
ersions" ]);
  terms.appendRow (["example: smart lipo near me" ,"10","1","5.
25","0"]);
  raw.clearContents ();
  raw.getRange (1,1).setValue ("📋 PASTE YOUR GOOGLE ADS SEARCH  
TERMS REPORT HERE" );
  raw.getRange (2,1).setValue ("HOW TO GET IT:" );
  raw.getRange (3,1).setValue ("1. Go to Google Ads → Keywords  
→ Search terms" );
  raw.getRange (4,1).setValue ("2. Set your date range (e.g., L
ast 30 days)" );
  raw.getRange (5,1).setValue ("3. Click Download ↓ → CSV" );
  raw.getRange (6,1).setValue ("4. Open CSV, select all (Ctrl+
A), copy (Ctrl+C)" );
  raw.getRange (7,1).setValue ("5. Click cell A8 below, paste  
(Ctrl+V)" );
  raw.getRange (8,1).setValue ("6. Run menu: 🔄  Normalize Paste
d Data");
  raw.getRange (1,1,1,1).setBackground ("#34a853" ).setFontColor
("white").setFontWeight ("bold").setFontSize (12);
  raw.getRange (2,1,6,1).setBackground ("#e8f5e9" ).setFontColor
("#1b5e20" );
  raw.setColumnWidth (1, 500);
  raw.setFrozenRows (7);
  uiSuccess_ ("Data templates ready. NegativesCSV created on e
xport.", "✅ Templates Ready" );
}
/* ===== Normalizer ===== */
function  normalizeGoogleAdsExport (){
  const ss = SpreadsheetApp .getActive ();
Negative Keyword AI (v6 Architecture)

  const raw = ss.getSheetByName ("RawExport" );
  const terms = ss.getSheetByName ("Terms") || ss.insertSheet
("Terms");
  if(!raw){ SpreadsheetApp .flush(); uiAlert_ ("RawExport sheet  
not found." ); return; }
  const data = raw.getDataRange ().getValues ();
  if(data.length < 2){ SpreadsheetApp .flush(); uiAlert_ ("RawE
xport has no data. Paste your Google Ads export first." ); ret
urn; }
  let auto = findHeaderRowAndIndexes_ (data);
  let headerRowIdx = auto.headerRowIdx ;
  let idx = auto.idx;
  if(headerRowIdx === -1 || idx.term == null){
    const mapping = promptManualMapping_ (raw);
    if(!mapping){ SpreadsheetApp .flush(); uiAlert_ ("Could not  
find a Search term / Search query column. Manual mapping canc
elled."); return; }
    headerRowIdx = mapping .headerRowIdx ;
    idx = mapping .idx;
  }
  const rows = [];
  let filteredCount = 0;
  for(let r=headerRowIdx +1; r<data.length; r++){
    const row = data[r];
    const term = valStr_(row[idx.term]);
    if(!term) continue ;
    if(isReportingArtifact_ (term)){
      filteredCount ++;
      continue ;
    }
Negative Keyword AI (v6 Architecture)

    const imps   = idx.impressions != null ? toInt_(row[idx.i
mpressions ]) : null;
    const clicks = idx.clicks      != null ? toInt_(row[idx.c
licks])      : null;
    const cost   = idx.cost        != null ? toMoney_ (row[id
x.cost])      : null;
    const conv   = idx.conversions != null ? toNum_(row[idx.c
onversions ]) : null;
    rows.push([term, imps, clicks, cost, conv]);
  }
  terms.clearContents ();
  terms.appendRow (["term","impressions" ,"clicks" ,"cost","conv
ersions" ]);
  if(rows.length) terms.getRange (2,1,rows.length,5).setValues
(rows);
  const extra = filteredCount > 0 ? ` (filtered ${filteredCou
nt} reporting rows) ` : "";
  uiSuccess_ (`Normalized ${rows.length} rows into Terms ${extr
a}`, "✅ Normalized" );
}
function  isReportingArtifact_ (term){
  const normalized = term.toLowerCase ().trim();
  const patterns = [
    /^total:\s* /i,
    /^keyword[s]?\s+on\s+link /i,
    /^other\s+search\s+terms /i,
    /^search\s+terms /i,
    /^\s*--\s*$ /
  ];
  return patterns .some(p => p.test(normalized ));
}
Negative Keyword AI (v6 Architecture)

function  findHeaderRowAndIndexes_ (data){
  const MAX_SCAN  = Math.min(10, data.length);
  let headerRowIdx = -1, header = null;
  const norm = (s)=> String(s||"")
    .replace(/\u00A0/g," ").replace(/[""]/g,'"').replace(/
['']/g,"'").replace(/\s+/g," ")
    .trim().toLowerCase ();
  // Helper to check if a cell looks like a search term heade
r
  const isSearchTermHeader  = (h) => {
    const t = h.trim();
    return t === "search term"  || t === "search terms"  || t =
== "search query"  || t === "term";
  };
  // Helper to check for other expected columns (validates i
t's a real header row, not a report title)
  const isKnownHeader  = (h) => {
    const t = h.trim();
    const knownHeaders = [
      "impr", "impr.", "impressions" , "impression" ,
      "clicks" , "click", "interactions" , "interaction" ,
      "cost", "spend",
      "conversions" , "conversion" , "conv",
      "campaign" , "ad group" , "adgroup" ,
      "match type" , "matchtype"
    ];
    return knownHeaders .includes (t);
  };
  for(let r=0; r<MAX_SCAN ; r++){
    const row = data[r].map(norm);
    const hasSearchTermCol = row.some(isSearchTermHeader );
    const hasOtherCols = row.filter(isKnownHeader ).length >= 
1;
Negative Keyword AI (v6 Architecture)

    if(hasSearchTermCol && hasOtherCols ){
      headerRowIdx = r;
      header = row;
      break;
    }
  }
  if(headerRowIdx === -1) return { headerRowIdx :-1, idx:{} };
  // Find column indexes - use flexible matching
  const findCol = (matchers ) => {
    for(let i=0; i<header.length; i++){
      const h = header[i].trim();
      if(matchers .some(m => typeof m === "string"  ? h === m : 
m.test(h))) return i;
    }
    return null;
  };
  const idx = {
    term: findCol(["search term" , "search terms" , "search que
ry", "term"]),
    impressions : findCol(["impressions" , "impression" , "imp
r", "impr."]),
    clicks: findCol(["clicks" , "click", "interactions" , "inte
raction" ]),
    cost: findCol(["cost", "spend", "amount spent" ]),
    conversions : findCol(["conversions" , "conversion" , "con
v", "all conv" , "all conv." ])
  };
  return { headerRowIdx , idx };
}
function  promptManualMapping_ (rawSheet ){
  let headerRow = 1;
  if(hasUi_()){
Negative Keyword AI (v6 Architecture)

    const resp = SpreadsheetApp .getUi().prompt("Manual mappin
g","Enter header row number (usually 1):" ,SpreadsheetApp .getU
i().ButtonSet .OK_CANCEL );
    if(resp.getSelectedButton () !== SpreadsheetApp .getUi().Bu
tton.OK) { SpreadsheetApp .flush(); return null; }
    headerRow = parseInt ((resp.getResponseText ()||"1").trim
(),10); if(!(headerRow >0)) headerRow =1;
  }
  const ask = (label, required =false)=>{
    if(!hasUi_()) return null;
    const res = SpreadsheetApp .getUi().prompt("Manual mappin
g",`Enter column letter for " ${label}"${required ?" (require
d)":" (optional)" } — e.g. A `,SpreadsheetApp .getUi().ButtonSe
t.OK_CANCEL );
    if(res.getSelectedButton () !== SpreadsheetApp .getUi().But
ton.OK) { SpreadsheetApp .flush(); return null; }
    const txt = (res.getResponseText ()||"").trim(); if(!txt &
& required ) { SpreadsheetApp .flush(); return null; } return t
xt || null;
  };
  const termColL   = ask("Search term" , true);   if(!termCol
L) { SpreadsheetApp .flush(); return null; }
  const imprColL   = ask("Impressions" , false);
  const clicksColL = ask("Clicks" , false);
  const costColL   = ask("Cost", false);
  const convColL   = ask("Conversions" , false);
  const idx = {
    term: colLetterToIndex_ (termColL ),
    impressions : imprColL ? colLetterToIndex_ (imprColL ) : nul
l,
    clicks: clicksColL ? colLetterToIndex_ (clicksColL ) : nul
l,
    cost: costColL ? colLetterToIndex_ (costColL ) : null,
    conversions : convColL ? colLetterToIndex_ (convColL ) : nul
l
Negative Keyword AI (v6 Architecture)

  };
  const lastRow = rawSheet .getLastRow ();
  if(headerRow < 1 || headerRow > lastRow ){ SpreadsheetApp .fl
ush(); uiAlert_ ("Header row is outside sheet range." ); return 
null; }
  SpreadsheetApp .flush(); // Clear spinner after successful p
rompt sequence
  return { headerRowIdx : headerRow -1, idx };
}
function  colLetterToIndex_ (letters){
  const s = (letters||"").toUpperCase ().replace(/[^A-Z]/
g,""); if(!s) return null;
  let n=0; for(let i=0;i<s.length;i++){ n = n*26 + (s.charCod
eAt(i)-64); } return n-1;
}
/* ===== RUN FUNCTIONS ===== */
function  runAnalysis (){
  const ss = SpreadsheetApp .getActive ();
  const existingCursor = NK_DP.getProperty ("nk_cursor" );
  const existingTotal = NK_DP.getProperty ("nk_total" );
  if(existingCursor && Number(existingCursor ) > 0) {
    const pct = ((Number(existingCursor ) / Number(existingTot
al)) * 100).toFixed(1);
    if(hasUi_()) {
      const ui = SpreadsheetApp .getUi();
      const response = ui.alert(
        "Previous Analysis Found" ,
        `Found existing progress at ${pct}% (${existingCurso
r}/${existingTotal } terms).\n\n ` +
        `• YES = Resume from where you left off\n ` +
        `• NO = Start fresh (discards progress)\n ` +
        `• CANCEL = Do nothing `,
Negative Keyword AI (v6 Architecture)

        ui.ButtonSet .YES_NO_CANCEL
      );
      if(response === ui.Button.YES) {
        ss.toast("🔄 Resuming analysis..." , "Starting" , 3);
        SpreadsheetApp .flush(); // Force toast to show immedi
ately
        runChainAnalysis_ (true); // Resume
      } else if(response === ui.Button.NO) {
        ss.toast("🚀 Starting fresh analysis..." , "Starting" , 
3);
        SpreadsheetApp .flush(); // Force toast to show immedi
ately
        NK_DP.deleteAllProperties (); // Clear progress
        runChainAnalysis_ (false); // Fresh start
      } else {
        // CANCEL - MUST flush to clear "Working..." spinner
        SpreadsheetApp .flush();
      }
      return;
    }
    // No UI - just resume
    runChainAnalysis_ (true);
  } else {
    ss.toast("🚀 Starting analysis..." , "Starting" , 3);
    SpreadsheetApp .flush(); // Force toast to show immediatel
y
    runChainAnalysis_ (false);
  }
}
/**
 * STOP EVERYTHING - Emergency stop button
 * Cancels all scheduled triggers and clears all running stat
e
Negative Keyword AI (v6 Architecture)

 * Sets a stop flag that running code checks
 */
function  stopEverything (){
  const ss = SpreadsheetApp .getActive ();
  const logs = getOrCreate_ (ss, "Logs");
  // SET STOP FLAG FIRST - running code will check this
  NK_DP.setProperty ("nk_stop_flag" , "true");
  // Count triggers before canceling
  let triggersKilled = 0;
  try {
    // Cancel ALL project triggers (not just resume triggers)
    const triggers = ScriptApp .getProjectTriggers ();
    triggers .forEach(t => {
      try {
        ScriptApp .deleteTrigger (t);
        triggersKilled ++;
      } catch(e) {
        Logger.log("Failed to delete trigger: "  + e.message);
      }
    });
  } catch(e) {
    Logger.log("Error accessing triggers: "  + e.message);
  }
  // Clear all state (AFTER setting stop flag so running code  
sees it first)
  Utilities .sleep(500); // Give running code time to see the  
flag
  try {
    NK_DP.deleteAllProperties ();
  } catch(e) {
    Logger.log("Error clearing properties: "  + e.message);
  }
Negative Keyword AI (v6 Architecture)

  // Log the action
  logs.appendRow ([new Date(), "🛑 STOPPED" , `User stopped all  
operations. ${triggersKilled } trigger(s) cancelled. `]);
  // Provide feedback
  SpreadsheetApp .flush();
  ss.toast(
    `🛑 All operations stopped!\n\n ` +
    `✓ ${triggersKilled } scheduled trigger(s) cancelled\n ` +
    `✓ Stop flag set for running code\n ` +
    `✓ All progress state cleared\n\n ` +
    `You can now start fresh with "Run Agent" `,
    "⏹ Stopped" ,
    10
  );
  Logger.log("stopEverything: Killed "  + triggersKilled + " t
riggers, cleared all properties" );
}
/** Check if stop was requested */
function  shouldStop_ () {
  return NK_DP.getProperty ("nk_stop_flag" ) === "true";
}
function  startFresh (){
  const existingCursor = NK_DP.getProperty ("nk_cursor" );
  if(existingCursor && Number(existingCursor ) > 0) {
    let confirmed = true;
    if(hasUi_()) {
      const ui = SpreadsheetApp .getUi();
      const response = ui.alert(
        "Discard Existing Progress?" ,
        `This will discard your current progress and start ov
Negative Keyword AI (v6 Architecture)

er.\n\nAre you sure? `,
        ui.ButtonSet .OK_CANCEL
      );
      confirmed = (response === ui.Button.OK);
    }
    if(!confirmed ) {
      SpreadsheetApp .flush(); // Clear "Working..." spinner o
n cancel
      return;
    }
  }
  NK_DP.deleteAllProperties ();
  runChainAnalysis_ (false);
}
/* ===== Main Chain Analysis ===== */
function  runChainAnalysis_ (resume){
  // Clear any lingering "Working..." spinner from dialog han
dling
  SpreadsheetApp .flush();
  const started = Date.now();
  // Store start time for total elapsed calculation (only on  
fresh start)
  if(!resume) {
    NK_DP.setProperty ("nk_start_time" , String(started));
  }
  const ss = SpreadsheetApp .getActive ();
  const cfgSheet = ss.getSheetByName ("Config" );
  const termsSheet = ss.getSheetByName ("Terms");
  const existingSheet = ss.getSheetByName ("ExistingNegative
s");
  const logs = getOrCreate_ (ss,"Logs");
Negative Keyword AI (v6 Architecture)

  if(!cfgSheet || !termsSheet ){ SpreadsheetApp .flush(); uiAle
rt_("Missing Config or Terms sheet." ); return; }
  const cfg = readConfig_ (cfgSheet );
  // Data validation before analysis (skip on resume)
  if(!resume) {
    const validation = validateDataBeforeAnalysis_ (termsShee
t, cfg);
    if(!validation .valid) {
      SpreadsheetApp .flush();
      uiAlert_ ("❌ Cannot start analysis:\n\n"  + validation .i
ssues.join("\n"));
      return;
    }
    if(validation .issues.length > 0) {
      // Show warnings but continue
      logs.appendRow ([new Date(),"⚠  VALIDATION WARNINGS" ,vali
dation.issues.filter(i => !i.startsWith ("💡")).join(" | ")]);
    }
  }
  if(!cfg.api_key || cfg.api_key === "<<ADD YOUR KEY>>" ){ Spr
eadsheetApp .flush(); uiAlert_ ("Add your API key in Config." ); 
return; }
  const outTabName = cfg.project_name ? `Output_${cfg.project
_name}` : "Output" ;
  const outSheet = getOrCreate_ (ss, outTabName );
  const existingNegs = existingSheet ? readCol_ (existingShee
t,1).map(normalizeKW_ ) : [];
  const allTerms = readTerms_ (termsSheet );
  if(allTerms .length===0){ SpreadsheetApp .flush(); uiAlert_
("No rows in Terms." ); return; }
  // Welcome toast with term count
Negative Keyword AI (v6 Architecture)

  ss.toast(`🚀 Analyzing ${allTerms .length} search terms... `, 
"Starting Analysis" , 5);
  // Filter terms by threshold (min_clicks OR min_impression
s)
  const filteredTerms = filterTermsForAnalysis_ (allTerms , cf
g);
  // Calculate account average CPC
  cfg.avg_cpc = calcAvgCpc_ (filteredTerms );
  // Load synonyms based on detected industry
  const synonymGroups = loadSynonyms_ (cfg);
  const detectedIndustry = detectIndustry_ (cfg);
  // Pre-compute expanded keywords
  const expandedPrimaryKeywords = expandWithSynonyms_ (cfg.pri
mary_service_keywords || [], synonymGroups );
  const expandedServicesOffered = expandWithSynonyms_ (cfg.ser
vices_offered || [], synonymGroups );
  const expandedAdjacents = expandWithSynonyms_ (cfg.adjacent_
services_offered || [], synonymGroups );
  // Apply top N prioritization
  const topN = Number(cfg.select_top_n || 0);
  let priorityTerms = [];
  let remainingTerms = [];
  if (topN > 0 && topN < filteredTerms .length) {
    const sorted = selectTopTerms_ (filteredTerms , cfg);
    priorityTerms = sorted.slice(0, topN);
    remainingTerms = sorted.slice(topN);
  } else {
    priorityTerms = selectTopTerms_ (filteredTerms , cfg);
    remainingTerms = [];
  }
Negative Keyword AI (v6 Architecture)

  const workingTerms = [...priorityTerms , ...remainingTerms ];
  // Initialize statistics
  const stats = {
    total: allTerms .length,
    filtered : filteredTerms .length,
    belowThreshold : allTerms .length - filteredTerms .length,
    priorityCount : priorityTerms .length,
    step1_keep : 0,
    step3_negate : 0,
    step3_competitor : 0,
    step5_skip : 0,
    step3_conflict : 0,
    forAI: 0,
    aiAnalyzed : 0,
    cpcEnriched : 0,
    overrides : 0
  };
  if(!resume){
    NK_DP.deleteAllProperties ();
    initializeOutputSheet_ (outSheet );
    logs.appendRow ([new Date(),"═════════════════════════════
══════════════════════════════" ]);
    logs.appendRow ([new Date(),"🔗 CHAIN ANALYSIS v6.0" ,`Star
ting analysis of ${allTerms .length} total search terms `]);
    logs.appendRow ([new Date(),"📋 FILTERING" ,`${filteredTerm
s.length} terms meet threshold ( ${stats.belowThreshold } below 
min clicks/impressions) `]);
    if (remainingTerms .length > 0) {
      logs.appendRow ([new Date(),"🎯 PRIORITY" ,`Top ${priorit
yTerms.length} by ${cfg.select_metric }, then ${remainingTerm
s.length} remaining `]);
    }
Negative Keyword AI (v6 Architecture)

    logs.appendRow ([new Date(),"🏭 INDUSTRY" ,detectedIndustry  
? `Detected: ${detectedIndustry }` : "Not detected - using man
ual config only" ]);
    logs.appendRow ([new Date(),"📚 SYNONYMS" ,`Loaded ${synony
mGroups.length} synonym groups `]);
    logs.appendRow ([new Date(),"═════════════════════════════
══════════════════════════════" ]);
  }
  // === PREPARE ALL TERMS FOR AI ANALYSIS ===
  // No mechanical decisions - AI analyzes 100% of terms
  // We still collect flags to give AI context, but AI makes  
ALL decisions
  const forAI = [];
  logs.appendRow ([new Date(),"🤖 PREPARING" ,"Collecting conte
xt flags for AI analysis..." ]);
  for (const term of workingTerms ) {
    const flags = {};
    const termText = term.term || "";
    // Collect context flags (NOT making decisions, just info
rming AI)
    // Flag: Has conversions?
    if ((term.conversions || 0) >= 1) {
      flags.hasConversions = true;
    }
    // Flag: Is brand term?
    if (isBrandTerm_ (termText , cfg.brand_terms )) {
      flags.isBrandTerm = true;
    }
    // Flag: Primary service match?
Negative Keyword AI (v6 Architecture)

    const primaryMatch = step2_primaryServiceFlag_ (term, expa
ndedPrimaryKeywords , expandedServicesOffered );
    Object.assign(flags, primaryMatch );
    // Flag: Alternative seeker pattern?
    const altSeeker = step4_alternativeSeekers_ (term);
    Object.assign(flags, altSeeker );
    // Flag: Is competitor term?
    if (isCompetitorTerm_ (termText )) {
      flags.isCompetitor = true;
    }
    // Flag: Low impressions?
    if ((term.impressions || 0) < 10) {
      flags.lowImpressions = true;
    }
    // ALL terms go to AI - no exceptions
    forAI.push({ term, flags });
    stats.forAI++;
  }
  // Log summary
  logs.appendRow ([new Date(),"🤖 AI QUEUE" ,`${stats.forAI} te
rms queued for AI analysis (100% AI-processed) `]);
  // Calculate estimated time for AI phase
  const vendor = String(cfg.api_vendor || "openai" ).toLowerCa
se();
  const estParallelCount = getParallelBatchCount_ (cfg);
  const termsPerBatch = NK_BATCH_SIZE  * estParallelCount ;
  const estBatches = Math.ceil(stats.forAI / termsPerBatch );
  const secsPerBatch = vendor === "anthropic"  ? 35 : 20;
  const estTotalSecs = estBatches * secsPerBatch ;
  const estTimeStr = estTotalSecs > 120
    ? `${Math.ceil(estTotalSecs / 60)} minutes `
Negative Keyword AI (v6 Architecture)

    : `${estTotalSecs } seconds `;
  logs.appendRow ([new Date(),"⏱ ESTIMATE" ,`${estBatches } bat
ches × ${termsPerBatch } terms = ~ ${estTimeStr } total`]);
  // Warn about slow Anthropic rate limits
  if(vendor === "anthropic"  && stats.forAI > 200) {
    logs.appendRow ([new Date(),"💡 TIP",`Anthropic has strict  
rate limits. Switch to Gemini for 10x faster processing. `]);
  }
  // Clear progress message
  ss.toast(
    `🤖 Starting AI analysis\n\n ` +
    `${stats.forAI} terms to analyze\n ` +
    `⏱ Est. time: ~ ${estTimeStr }`,
    "Starting Analysis" , 8
  );
  // Store state for resume
  NK_DP.setProperty ("nk_total" , String(forAI.length));
  NK_DP.setProperty ("nk_stats" , JSON.stringify (stats));
  // Sort by spend (highest first) for AI analysis
  forAI.sort((a, b) => (b.term.cost || 0) - (a.term.cost || 
0));
  // === AI ANALYSIS (Step 6) ===
  let cursor = resume ? Number(NK_DP.getProperty ("nk_cursor" ) 
|| 0) : 0;
  if (forAI.length === 0) {
    logs.appendRow ([new Date(),"✅ COMPLETE" ,"No terms need A
I analysis - all handled mechanically!" ]);
    finishAnalysis_ (outSheet , logs, stats, cfg);
    return;
Negative Keyword AI (v6 Architecture)

  }
  // Calculate effective batch size for parallel processing  
(rate-limit aware)
  const parallelCount = getParallelBatchCount_ (cfg);
  const parallelBatchSize = NK_BATCH_SIZE  * parallelCount ;
  const totalBatches = Math.ceil(forAI.length / parallelBatch
Size);
  Logger.log(`Using ${parallelCount } parallel calls (vendor: 
${cfg.api_vendor })`);
  while(cursor < forAI.length){
    // Check for stop flag at start of each batch
    if(shouldStop_ ()) {
      logs.appendRow ([new Date(), "🛑 STOPPED" , "Stop request
ed by user - aborting analysis" ]);
      SpreadsheetApp .flush(); // Clear spinner before showing  
stop message
      ss.toast("🛑 Analysis stopped by user request" , "Stoppe
d", 5);
      return; // Exit immediately
    }
    if(Date.now() - started > NK_MAX_RUNTIME_MS ) break;
    // Get a "super batch" that will be split into parallel c
alls
    const superBatch = forAI.slice(cursor, cursor + parallelB
atchSize );
    const batchNum = Math.floor(cursor / parallelBatchSize ) + 
1;
    const progressPct = Math.floor((cursor / forAI.length) * 
100);
    // Split into sub-batches for parallel processing
    const subBatches = [];
Negative Keyword AI (v6 Architecture)

    for(let i = 0; i < superBatch .length; i += NK_BATCH_SIZE ) 
{
      subBatches .push(superBatch .slice(i, i + NK_BATCH_SIZ
E));
    }
    const batchStartTime = Date.now();
    logs.appendRow ([new Date(),"🤖 AI BATCH" ,`Batch ${batchNu
m}/${totalBatches }: ${subBatches .length} parallel calls, term
s ${cursor+1}-${cursor+superBatch .length} (${progressPct }%)
`]);
    ss.toast(`🤖 Processing batch ${batchNum } of ${totalBatch
es}...\n\n📊  ${progressPct }% complete\n🔍  Analyzing ${superBa
tch.length} terms`, "Working" , 30);
    let success = false;
    let rateLimitHit = false;  // Declare outside retry loop  
so it's accessible after loop
    let overloadedHit = false; // Track 503 overloaded errors
    const maxRetries = 3;  // Increased from 2 for transient  
errors
    for(let attempt = 1; attempt <= maxRetries ; attempt ++){
      try{
        // Build payloads for all sub-batches
        const payloads = subBatches .map(subBatch  => buildAIPa
yload_(cfg, existingNegs , subBatch ));
        // Execute parallel API calls
        const results = callLLMParallel_ (cfg, CHAIN_SYSTEM_PR
OMPT, payloads );
        // Process results from all parallel calls
        const processedRecs = [];
        let failedTermCount = 0;
        let totalUnmatchedCount = 0;  // Track unmatched term
Negative Keyword AI (v6 Architecture)

s (CRITICAL for data integrity)
        rateLimitHit = false;  // Reset for each attempt
        overloadedHit = false;
        let retriableFailures = 0;
        for(let bIdx = 0; bIdx < results .length; bIdx++) {
          const result = results [bIdx];
          const subBatch = subBatches [bIdx];
          if(!result.success) {
            const errorStr = result.error || "";
            const isRetriable = errorStr .includes ("429") ||
                               errorStr .includes ("503") ||
                               errorStr .toLowerCase ().include
s("rate") ||
                               errorStr .toLowerCase ().include
s("overload" ) ||
                               errorStr .toLowerCase ().include
s("capacity" );
            if(isRetriable ) {
              retriableFailures ++;
              if(errorStr .includes ("429") || errorStr .toLower
Case().includes ("rate")) {
                rateLimitHit = true;
              }
              if(errorStr .includes ("503") || errorStr .toLower
Case().includes ("overload" )) {
                overloadedHit = true;
              }
            }
            logs.appendRow ([new Date(),"⚠  SUB-BATCH FAILED" ,`
Sub-batch ${bIdx+1}: ${errorStr .substring (0, 150)}`]);
            failedTermCount += subBatch .length;
            continue ;
Negative Keyword AI (v6 Architecture)

          }
          // Extract recommendations - handle multiple possib
le response formats
          let recs = [];
          if (result.data) {
            if (Array.isArray(result.data.recommendations )) {
              recs = result.data.recommendations ;
            } else if (Array.isArray(result.data.results)) {
              recs = result.data.results; // Some AIs use "re
sults"
            } else if (Array.isArray(result.data)) {
              recs = result.data; // AI returned bare array
            } else if (result.data.data && Array.isArray(resu
lt.data.data.recommendations )) {
              recs = result.data.data.recommendations ; // Nes
ted structure
            }
          }
          // DIAGNOSTIC: Log AI response structure
          Logger.log(`Sub-batch ${bIdx+1}: result.data type =  
${typeof result.data}, isArray = ${Array.isArray(result.dat
a)}`);
          Logger.log(`Sub-batch ${bIdx+1}: result.data keys =  
${result.data && typeof result.data === 'object'  ? Object.key
s(result.data).join(", ") : "N/A"}`);
          Logger.log(`Sub-batch ${bIdx+1}: recs.length = ${re
cs.length}`);
          if(recs.length > 0) {
            Logger.log(`Sub-batch ${bIdx+1}: First rec keys =  
${Object.keys(recs[0]).join(", ")}`);
            Logger.log(`Sub-batch ${bIdx+1}: First rec.term =  
"${recs[0].term}", First rec.search_term = " ${recs[0].search_
term}"`);
            Logger.log(`Sub-batch ${bIdx+1}: First input term  
Negative Keyword AI (v6 Architecture)

= "${subBatch [0].term.term}"`);
          } else {
            // If recs is empty, log raw result.data to see w
hat AI actually returned
            const rawStr = JSON.stringify (result.data);
            Logger.log(`Sub-batch ${bIdx+1}: EMPTY RECS! Raw  
result.data (first 800 chars): ${rawStr.substring (0, 800)}`);
            logs.appendRow ([new Date(), "🔍 DEBUG", `Sub-batc
h ${bIdx+1}: AI returned 0 recommendations. Keys: ${result.da
ta && typeof result.data === 'object'  ? Object.keys(result.da
ta).join(", ") : "not an object" }`]);
          }
          // Log AI response stats (only if mismatch to reduc
e noise)
          if(recs.length !== subBatch .length) {
            logs.appendRow ([new Date(), "📊 AI RESPONSE" , `Su
b-batch ${bIdx+1}: Sent ${subBatch .length} terms, received 
${recs.length} recommendations `]);
          }
          let matchedCount = 0;
          let unmatchedCount = 0;
          // Build a lookup map using normalized terms for ro
bust matching
          const termLookup = new Map();
          for (let j = 0; j < subBatch .length; j++) {
            const normalizedTerm = normalizeKW_ (subBatch [j].t
erm.term);
            termLookup .set(normalizedTerm , { term: subBatch
[j].term, flags: subBatch [j].flags || {} });
          }
          for (let i = 0; i < recs.length; i++) {
            const rec = recs[i];
Negative Keyword AI (v6 Architecture)

            // Handle multiple possible field names for the t
erm
            const recTermRaw = rec.term || rec.search_term || 
rec.keyword || rec.searchTerm || "";
            const normalizedRecTerm = normalizeKW_ (recTermRa
w);
            // Try multiple matching strategies:
            // 1. Exact normalized match
            let matchedEntry = termLookup .get(normalizedRecTe
rm);
            // 2. If no exact match, try finding partial matc
h (AI might truncate long terms)
            if (!matchedEntry ) {
              for (const [key, value] of termLookup ) {
                // Check if one contains the other (handles t
runcation)
                if (key.includes (normalizedRecTerm ) || normal
izedRecTerm .includes (key)) {
                  matchedEntry = value;
                  Logger.log(`Sub-batch ${bIdx+1}: Partial ma
tch - AI returned " ${recTermRaw }", matched to " ${value.term.t
erm}"`);
                  break;
                }
              }
            }
            // 3. Fallback to positional match if term counts  
match and still no match
            if (!matchedEntry && subBatch .length === recs.len
gth && subBatch [i]) {
              matchedEntry = { term: subBatch [i].term, flags: 
subBatch [i].flags || {} };
              Logger.log(`Sub-batch ${bIdx+1}: Positional fal
Negative Keyword AI (v6 Architecture)

lback - AI returned " ${recTermRaw }", using position ${i} term 
"${subBatch [i].term.term}"`);
            }
            const termData = matchedEntry ?.term;
            const termFlags = matchedEntry ?.flags || {};
            if (!termData ) {
              unmatchedCount ++;
              Logger.log(`Sub-batch ${bIdx+1}: UNMATCHED - AI  
returned " ${rec.term}" but no input term matched `);
              // Log all input terms for debugging
              if (unmatchedCount === 1) {
                Logger.log(`Sub-batch ${bIdx+1}: Input terms  
were: ${subBatch .map(b => b.term.term).join(", ")}`);
              }
              continue ;
            }
            matchedCount ++;
            // Step 6.5: CPC Enrichment
            const { result: enrichedRec , enriched } = step6_5
_cpcEnrichment_ (termData , rec, cfg);
            if (enriched ) stats.cpcEnriched ++;
            // Step 7: Guardrails
            const finalRec = step7_guardrails_ (termData , enri
chedRec, termFlags , cfg);
            if (finalRec .overrideReason ) stats.overrides ++;
            processedRecs .push({
              term: termData .term,
              action: finalRec .action,
              method: "🤖 AI",
              category : finalRec .category ,
              suggested_negative : finalRec .suggested_negative  
Negative Keyword AI (v6 Architecture)

|| null,
              match_type : finalRec .match_type || "NONE",
              level: finalRec .level || "NONE",
              confidence : finalRec .confidence || 0.7,
              rationale : finalRec .rationale ,
              signals: finalRec .signals || [],
              performance : {
                impressions : termData .impressions ,
                clicks: termData .clicks,
                cost: termData .cost,
                conversions : termData .conversions
              }
            });
          }
          // Log match results and add to total
          if(unmatchedCount > 0) {
            totalUnmatchedCount += unmatchedCount ;
            // Log the specific unmatched terms for debugging
            const unmatchedTermsList = subBatch .slice(matched
Count).map(b => b.term.term).join(", ");
            logs.appendRow ([new Date(), "⚠  UNMATCHED" , `Sub-b
atch ${bIdx+1}: ${unmatchedCount } terms unmatched. Terms: ${u
nmatchedTermsList .substring (0, 200)}`]);
          }
        }
        // CHECK FOR RETRY - If ANY terms failed OR unmatche
d, retry the whole batch
        // We don't accept partial results - ALL terms must b
e analyzed
        const totalProblems = failedTermCount + totalUnmatche
dCount;
        if(totalProblems > 0 && attempt < maxRetries ) {
          // Exponential backoff with 60s cap to prevent time
out
Negative Keyword AI (v6 Architecture)

          const baseWait = overloadedHit ? 15000 : (rateLimit
Hit ? 10000 : 5000);
          const waitTime = Math.min(baseWait * Math.pow(2, at
tempt - 1), 60000);
          const reason = overloadedHit ? "Model overloaded (5
03)" :
                        (rateLimitHit ? "Rate limit (429)"  :
                        (totalUnmatchedCount > 0 ? "Term matc
hing failed"  : "API error" ));
          logs.appendRow ([new Date(), "🔄 RETRYING" , `${reaso
n} - ${failedTermCount } API failures, ${totalUnmatchedCount } 
unmatched. Waiting ${waitTime /1000}s before retry ${attempt + 
1}/${maxRetries }...`]);
          ss.toast(`⏳ ${reason}\n\nRetrying in ${waitTime /10
00}s...\n(Attempt ${attempt + 1} of ${maxRetries })`, "Retryin
g", 5);
          Utilities .sleep(waitTime );
          continue ; // Retry WITHOUT writing partial results
        }
        // If we still have failures after all retries, log b
ut continue
        // The batch will be re-processed on next run (cursor  
won't advance for failed batches)
        if(totalProblems > 0) {
          logs.appendRow ([new Date(), "⚠  INCOMPLETE" , `Batch 
${batchNum }: ${failedTermCount } API failures, ${totalUnmatche
dCount} unmatched after ${maxRetries } attempts `]);
        }
        // Track row count before write
        const rowsBefore = outSheet .getLastRow ();
        if(processedRecs .length) {
          try {
            writeOutputBatch_ (outSheet , processedRecs );
Negative Keyword AI (v6 Architecture)

            Logger.log(`Batch ${batchNum }: writeOutputBatch_  
completed `);
          } catch(writeErr ) {
            Logger.log(`Batch ${batchNum }: writeOutputBatch_  
FAILED: ${writeErr .message}`);
            logs.appendRow ([new Date(), "❌ WRITE ERROR" , wri
teErr.message]);
          }
          // NOTE: Sort/color moved to finishAnalysis_ for ef
ficiency
          // Sorting ALL rows after EVERY batch was causing O
(n*batches) overhead
          // Now we only sort once at the end
          SpreadsheetApp .flush();
        } else {
          Logger.log(`Batch ${batchNum }: NO RECS to write! `);
          logs.appendRow ([new Date(), "⚠  NO DATA" , `Batch ${b
atchNum} produced 0 recommendations `]);
        }
        // Track row count after write and verify
        const rowsAfter = outSheet .getLastRow ();
        const rowsAdded = rowsAfter - rowsBefore ;
        // Track how many terms were successfully analyzed (n
ever negative)
        const successfulTerms = Math.max(0, superBatch .length 
- failedTermCount );
        stats.aiAnalyzed += successfulTerms ;
        // Calculate timing
        const batchDuration = ((Date.now() - batchStartTime ) 
/ 1000).toFixed(1);
        const pctComplete = Math.floor(((cursor + superBatch .
Negative Keyword AI (v6 Architecture)

length) / forAI.length) * 100);
        const remaining = forAI.length - (cursor + superBatc
h.length);
        const batchesLeft = totalBatches - batchNum ;
        const estSecondsLeft = Math.round(batchesLeft * parse
Float(batchDuration ));
        const estTimeStr = estSecondsLeft > 60
          ? `~${Math.ceil(estSecondsLeft / 60)} min left `
          : `~${estSecondsLeft }s left`;
        // Log with timing AND row confirmation
        const rowConfirm = rowsAdded === processedRecs .length
          ? `✓ ${rowsAdded } rows written `
          : `⚠  Expected ${processedRecs .length} rows, wrote 
${rowsAdded }`;
        logs.appendRow ([new Date(), "✅ BATCH DONE" , `Batch 
${batchNum }/${totalBatches } in ${batchDuration }s | ${processe
dRecs.length} recs | ${rowConfirm } | Total: ${rowsAfter - 1} 
rows`]);
        // Encouraging toast with timing
        const encouragement = pctComplete >= 75 ? "Almost the
re! 🎯" : pctComplete >= 50 ? "Halfway there! 💪 " : "Making p
rogress! 🚀 ";
        ss.toast(
          `✅ Batch ${batchNum }/${totalBatches } done in ${bat
chDuration }s\n\n` +
          `📊 ${pctComplete }% complete\n ` +
          `⏱ ${estTimeStr }\n\n` +
          `${encouragement }`,
          "Progress" , 5
        );
        // ALL terms must be successfully processed AND match
ed - no partial results accepted
        // CRITICAL: Both API success AND term matching requi
Negative Keyword AI (v6 Architecture)

red for data integrity
        success = (failedTermCount === 0 && totalUnmatchedCou
nt === 0);
        if(success) break;
      }catch(e){
        const errorMsg = e.message || "";
        const isRateLimit = errorMsg .includes ("429") || error
Msg.toLowerCase ().includes ("rate");
        if(attempt < maxRetries ){
          // Brief wait before retry (longer for rate limit
s), capped at 60s
          const waitTime = Math.min(isRateLimit ? 10000 : Mat
h.pow(2, attempt ) * 1000, 60000);
          logs.appendRow ([new Date(),"⚠  RETRY",`Batch ${batch
Num} attempt ${attempt}. Retrying... `]);
          Utilities .sleep(waitTime );
        } else {
          logs.appendRow ([new Date(),"❌ FAILED" ,`Batch ${bat
chNum} failed: ${errorMsg .substring (0, 150)}`]);
        }
      }
    }
    // Only advance cursor if ALL terms were successfully pro
cessed AND matched
    if(success) {
      cursor += parallelBatchSize ;
      NK_DP.setProperty ("nk_cursor" , String(cursor));
      NK_DP.setProperty ("nk_stats" , JSON.stringify (stats));
      resetResumeRetries_ ();  // Reset retry counter on succe
ss
      // Brief delay between batches - rate limiting handled  
by sequential processing
Negative Keyword AI (v6 Architecture)

      Utilities .sleep(1000);
    } else {
      // BATCH INCOMPLETE: Some or all terms failed after max  
retries
      // DO NOT advance cursor - batch will be retried on nex
t run
      // NO fallback entries created - we keep retrying until  
we get real results
      const vendor = String(cfg.api_vendor || "openai" ).toLow
erCase();
      let failureReason = overloadedHit ? "Model overloaded  
(503)" :
                          rateLimitHit ? "Rate limit exceeded  
(429)" :
                          "API errors occurred" ;
      logs.appendRow ([new Date(), "⏸ BATCH PAUSED" , `Batch 
${batchNum }: ${failedTermCount }/${superBatch .length} terms fa
iled - ${failureReason }. Will retry on resume. `]);
      // Helpful tip for Anthropic users
      const tip = vendor === "anthropic"  && rateLimitHit
        ? "\n\n💡 TIP: Switch to gemini-2.0-flash for faster  
processing!"
        : "";
      ss.toast(
        `⏸ Batch ${batchNum } needs retry\n\n ` +
        `${failureReason }\n` +
        `${failedTermCount } terms will be retried ${tip}\n\n` 
+
        `Auto-resuming in 90 seconds... `,
        "⚠  Temporary Issue" , 15
      );
Negative Keyword AI (v6 Architecture)

      // Schedule auto-resume to retry this batch
      if(String(cfg.auto_resume ||"true").toLowerCase ()==="tru
e"){
        scheduleResumeOnce_ ();
        logs.appendRow ([new Date(), "🔄 AUTO-RESUME" , `Retry 
scheduled in 90 seconds - cursor NOT advanced `]);
      }
      Utilities .sleep(3000);
      break; // Exit batch loop - will resume from same posit
ion
    }
  }
  const done = (cursor >= forAI.length);
  if(done){
    finishAnalysis_ (outSheet , logs, stats, cfg);
  } else {
    const pct = ((cursor/forAI.length)*100).toFixed(1);
    const termsLeft = forAI.length - cursor;
    logs.appendRow ([new Date(),"⏸ PAUSED" ,`AI analysis ${pc
t}% complete. ${termsLeft } terms remaining. Will resume autom
atically. `]);
    // Clear spinner before showing pause message
    SpreadsheetApp .flush();
    if(String(cfg.auto_resume ||"true").toLowerCase ()==="tru
e"){
      scheduleResumeOnce_ ();
      ss.toast(`⏸ Progress saved: ${pct}% complete\n ${termsL
eft} terms remaining\n\n ✅  Will auto-resume in 90 seconds\n(Y
ou can close this tab) `, "Analysis Paused" , 15);
    }
  }
Negative Keyword AI (v6 Architecture)

}
function  finishAnalysis_ (outSheet , logs, stats, cfg) {
  NK_DP.deleteAllProperties ();
  cancelResumeTrigger_ ();
  const ss = SpreadsheetApp .getActive ();
  const rowCount = outSheet .getLastRow ();
  Logger.log("finishAnalysis_: Starting. Rows="  + rowCount );
  // Track any errors for user notification
  const errors = [];
  if (rowCount < 2) {
    logs.appendRow ([new Date(), "⚠  FINISH" , "No data rows to  
process" ]);
    Logger.log("finishAnalysis_: No data rows (rowCount="  + r
owCount + ")");
  }
  // Step 1: Sort results by severity (most wasteful at top)
  try {
    if(rowCount > 1) {
      ss.toast("📊 Sorting results by severity..." , "Finishin
g Up", 3);
      sortOutputBySeverityForSheet_ (outSheet );
      Logger.log("finishAnalysis_: Sorting complete" );
    }
  } catch(e) {
    errors.push("Sort");
    logs.appendRow ([new Date(), "❌ SORT ERROR" , e.message]);
    Logger.log("finishAnalysis_ sort error: "  + e.message);
  }
  // Step 2: Apply color coding to data rows BEFORE inserting  
Negative Keyword AI (v6 Architecture)

summary
  try {
    if(rowCount > 1) {
      ss.toast("🎨 Applying color coding..." , "Finishing Up" , 
3);
      applyColorCoding_ (outSheet );
      SpreadsheetApp .flush(); // Ensure colors are committed  
before structural changes
      Logger.log("finishAnalysis_: Color coding complete" );
    }
  } catch(e) {
    errors.push("Color coding" );
    logs.appendRow ([new Date(), "❌ COLOR ERROR" , e.messag
e]);
    Logger.log("finishAnalysis_ color error: "  + e.message);
  }
  // Step 3: Add Executive Summary at top (inserts rows, shif
ting colored data down)
  try {
    if(rowCount > 1) {
      ss.toast("📊 Adding Executive Summary..." , "Finishing U
p", 3);
      addExecutiveSummary_ (outSheet , stats, cfg);
      Logger.log("finishAnalysis_: Executive Summary added" );
    }
  } catch(e) {
    errors.push("Executive Summary" );
    logs.appendRow ([new Date(), "❌ SUMMARY ERROR" , e.messag
e]);
    Logger.log("finishAnalysis_ summary error: "  + e.messag
e);
  }
  // Step 4: Add What's Next at bottom
  try {
Negative Keyword AI (v6 Architecture)

    if(outSheet .getLastRow () > 1) {
      ss.toast("🎯 Adding What's Next guidance..." , "Finishin
g Up", 3);
      addWhatsNext_ (outSheet , stats);
      Logger.log("finishAnalysis_: What's Next added" );
    }
  } catch(e) {
    errors.push("What's Next" );
    logs.appendRow ([new Date(), "❌ WHATS_NEXT ERROR" , e.mess
age]);
    Logger.log("finishAnalysis_ whats_next error: "  + e.messa
ge);
  }
  SpreadsheetApp .flush();
  // Store errors for final notification
  stats.finishErrors = errors;
  // Calculate total elapsed time
  const startTime = Number(NK_DP.getProperty ("nk_start_time" ) 
|| Date.now());
  const totalElapsedMs = Date.now() - startTime ;
  const totalMins = Math.floor(totalElapsedMs / 60000);
  const totalSecs = Math.round((totalElapsedMs % 60000) / 100
0);
  const totalTimeStr = totalMins > 0 ? `${totalMins }m ${total
Secs}s` : `${totalSecs }s`;
  // Log final statistics - BATCHED for efficiency (was: 15+  
individual appendRow calls)
  const aiSavings = ((stats.filtered - stats.forAI) / stats.f
iltered * 100).toFixed(1);
  const actualOutputRows = rowCount - 1;
  const expectedRows = stats.filtered ;
  const now = new Date();
Negative Keyword AI (v6 Architecture)

  const logBatch = [
    [now, "══════════════════════════════════════════════════
═════════" , ""],
    [now, "🎉 ANALYSIS COMPLETE" , `Total time: ${totalTimeSt
r}`],
    [now, "══════════════════════════════════════════════════
═════════" , ""],
    [now, "📊 SUMMARY" , `${stats.total} total terms analyzed
`],
    [now, "✅ Instant KEEP" , `${stats.step1_keep } (conversion
s/brand terms) `],
    [now, "🚫 Auto-negated" , `${stats.step3_negate + stats.st
ep3_competitor } (waste patterns + competitors) `],
    [now, "⏭ Filtered out" , `${stats.step5_skip } (low-value/
irrelevant) `],
    [now, "🤖 AI analyzed" , `${stats.aiAnalyzed } terms`]
  ];
  if(stats.cpcEnriched > 0) logBatch .push([now, "💰 CPC enric
hed", `${stats.cpcEnriched } terms`]);
  if(stats.overrides > 0) logBatch .push([now, "🛡 Guardrail f
ixes", `${stats.overrides } AI decisions corrected `]);
  logBatch .push([now, "💡 EFFICIENCY" , `${aiSavings }% of term
s handled without AI (cost savings!) `]);
  logBatch .push([now, "══════════════════════════════════════
═════════════════════" , ""]);
  if (actualOutputRows >= expectedRows ) {
    logBatch .push([now, "✅ DATA CHECK" , `${actualOutputRows } 
rows in output ≥ ${expectedRows } expected terms - ALL ACCOUNT
ED FOR`]);
  } else {
    const missing = expectedRows - actualOutputRows ;
    logBatch .push([now, "⚠  DATA CHECK" , `${actualOutputRows } 
Negative Keyword AI (v6 Architecture)

rows in output vs ${expectedRows } expected - ${missing} terms 
may need re-processing `]);
    logBatch .push([now, "💡 TIP", `If terms are missing, chec
k logs above for UNMATCHED or FALLBACK entries `]);
  }
  logBatch .push([now, "══════════════════════════════════════
═════════════════════" , ""]);
  // Write all log rows in single batch operation
  const logsLastRow = logs.getLastRow ();
  logs.getRange (logsLastRow + 1, 1, logBatch .length, 3).setVa
lues(logBatch );
  // Store stats for viewing
  NK_DP.setProperty ("nk_final_stats" , JSON.stringify (stats));
  const mechanicalNegates = stats.step3_negate + stats.step3_
competitor ;
  // Nice completion toast - warn user if any finishing steps  
had issues
  const hasErrors = errors.length > 0;
  const errorWarning = hasErrors
    ? `\n\n⚠  Some formatting steps failed ( ${errors.join(", 
")}). Check Logs tab. `
    : "";
  // Final flush to clear spinner before showing completion t
oast
  SpreadsheetApp .flush();
  ss.toast(
    `🎉 Analysis complete!\n\n ` +
    `⏱ Total time: ${totalTimeStr }\n` +
    `📊 ${stats.total} terms processed\n ` +
Negative Keyword AI (v6 Architecture)

    `🤖 ${stats.aiAnalyzed } AI-analyzed\n\n ` +
    `Check the Executive Summary at the top of the Output ta
b!${errorWarning }`,
    hasErrors ? "⚠  Complete with Issues"  : "✅ Complete!" , 15
  );
}
/* ===== View Pipeline Statistics ===== */
function  viewPipelineStats () {
  const statsJson = NK_DP.getProperty ("nk_final_stats" );
  if (!statsJson ) {
    uiSuccess_ ("No analysis run yet. Run analysis first to se
e stats." , "ℹ No Stats" );
    return;
  }
  const stats = JSON.parse(statsJson );
  const aiSavings = stats.filtered > 0 ? ((stats.filtered - s
tats.forAI) / stats.filtered * 100).toFixed(1) : 0;
  const mechanical = stats.step1_keep + (stats.step3_negate |
| 0) + (stats.step3_competitor || 0) + (stats.step5_skip || 
0);
  uiSuccess_ (
    `Total: ${stats.total} | Mechanical: ${mechanical } | AI: 
${stats.aiAnalyzed } | Savings: ${aiSavings }%`,
    "📊 Pipeline Stats"
  );
}
/* ===== Build AI Payload ===== */
function  buildAIPayload_ (cfg, negs, batch) {
  return {
    // Business Context
    brand_terms : cfg.brand_terms || [],
    services_offered : cfg.services_offered || [],
Negative Keyword AI (v6 Architecture)

    services_not_offered : cfg.services_not_offered || [],
    primary_service_keywords : cfg.primary_service_keywords || 
[],
    adjacent_services_offered : cfg.adjacent_services_offered 
|| [],
    buyer_persona : cfg.buyer_persona || "",
    custom_context : cfg.custom_context || "",  // NEW: User's  
free-form notes
    // Strategy Settings
    allow_competitor_terms : !!cfg.allow_competitor_terms ,
    allow_cross_modality : !!cfg.allow_cross_modality ,
    price_positioning : cfg.price_positioning || "premium" ,
    funnel_target : cfg.funnel_target || "BOFU",
    locations_served : cfg.locations_served || [],
    languages_supported : cfg.languages_supported || ["en"],
    // Analysis Context
    target_url : cfg.target_url || "",
    existing_negative_keywords : negs,
    thresholds : {
      target_cpa : cfg.target_cpa || null
    },
    // Search Terms with Flags
    search_terms : batch.map(b => ({
      term: b.term.term,
      clicks: b.term.clicks,
      impressions : b.term.impressions ,
      cost: b.term.cost,
      conversions : b.term.conversions ,
      flags: {
        softProtected : b.flags.softProtected || false,
        matchedService : b.flags.matchedService || null,
        commercialIntent : b.flags.commercialIntent || false,
        alternativeSeeker : b.flags.alternativeSeeker || fals
Negative Keyword AI (v6 Architecture)

e,
        conflict : b.flags.conflict || null
      }
    }))
  };
}
/* ===== Calculate Average CPC ===== */
function  calcAvgCpc_ (terms) {
  const termsWithClicks = terms.filter(t => (t.clicks || 0) > 
0 && (t.cost || 0) > 0);
  if (termsWithClicks .length === 0) return 5; // Default fall
back
  const totalCost = termsWithClicks .reduce((sum, t) => sum + 
(t.cost || 0), 0);
  const totalClicks = termsWithClicks .reduce((sum, t) => sum 
+ (t.clicks || 0), 0);
  return totalClicks > 0 ? totalCost / totalClicks : 5;
}
/* ===== Output Sheet Functions ===== */
function  initializeOutputSheet_ (sheet){
  sheet.clearContents ();
  sheet.clearFormats ();
  const headers = ["term","action" ,"method" ,"category" ,"negat
ive_keyword" ,"match_type" ,"level","confidence" ,"conf_star
s","rationale" ,"signals" ,"impressions" ,"clicks" ,"cost","conve
rsions"];
  sheet.appendRow (headers);
  const headerRange = sheet.getRange (1, 1, 1, headers .lengt
h);
  headerRange .setBackground ("#4285f4" );
Negative Keyword AI (v6 Architecture)

  headerRange .setFontColor ("white");
  headerRange .setFontWeight ("bold");
  headerRange .setHorizontalAlignment ("center" );
  sheet.setColumnWidth (1, 200);  // term
  sheet.setColumnWidth (2, 110);  // action
  sheet.setColumnWidth (3, 100);  // method
  sheet.setColumnWidth (4, 120);  // category
  sheet.setColumnWidth (5, 160);  // suggested_negative
  sheet.setColumnWidth (6, 90);   // match_type
  sheet.setColumnWidth (7, 90);   // level
  sheet.setColumnWidth (8, 70);   // confidence
  sheet.setColumnWidth (9, 70);   // conf_stars
  sheet.setColumnWidth (10, 350); // rationale
  sheet.setColumnWidth (11, 180); // signals
  sheet.setColumnWidth (12, 80);  // impressions
  sheet.setColumnWidth (13, 60);  // clicks
  sheet.setColumnWidth (14, 70);  // cost
  sheet.setColumnWidth (15, 80);  // conversions
  sheet.setFrozenRows (1);
  sheet.getRange (2, 10, sheet.getMaxRows ()-1, 2).setWrap(tru
e);
}
function  writeOutputBatch_ (sh, recs){
  if(!recs || !recs.length) return;
  // Cache getLastRow() - avoid calling twice
  let lastRow = sh.getLastRow ();
  if(lastRow === 0){
    initializeOutputSheet_ (sh);
    lastRow = 1; // After init, header is row 1
  }
  const startRow = lastRow + 1;
Negative Keyword AI (v6 Architecture)

  const rows = recs.map(r=>[
    r.term || "",
    r.action || "",
    r.method || "",
    r.category || "",
    r.suggested_negative || "",
    formatMatchType_ (r.match_type ),
    formatLevel_ (r.level),
    r.confidence ?? "",
    renderConfidenceStars_ (r.confidence ),
    r.rationale || "",
    Array.isArray(r.signals)?r.signals.join("; "):"",
    r.performance ?.impressions ?? "",
    r.performance ?.clicks ?? "",
    r.performance ?.cost ?? "",
    r.performance ?.conversions ?? ""
  ]);
  sh.getRange (startRow , 1, rows.length, rows[0].length).setVa
lues(rows);
  // Apply color coding immediately for "wow factor" - BATCHE
D for efficiency
  // Uses shared ACTION_COLORS constant defined at top of fil
e
  // Build 2D backgrounds array and apply in single API call  
(was: per-row loop)
  const numCols = rows[0].length;
  const backgrounds = recs.map(r => {
    const action = (r.action || "").toUpperCase ();
    const color = ACTION_COLORS [action] || "#ffffff" ;
    return Array(numCols).fill(color);
  });
  sh.getRange (startRow , 1, recs.length, numCols ).setBackgroun
Negative Keyword AI (v6 Architecture)

ds(backgrounds );
  // Quick incremental sort after each batch for better UX
  // Users see organized results as they come in (NEGATIVE_AD
D at top)
  quickSortOutput_ (sh);
}
/**
 * Lightweight sort that runs after each batch - keeps output  
organized as results come in.
 * Optimized: single read, in-memory sort, single write. ~2-4  
seconds for 1000 rows.
 */
function  quickSortOutput_ (sh) {
  const lastRow = sh.getLastRow ();
  if (lastRow < 3) return; // Need at least 2 data rows to so
rt
  const lastCol = sh.getLastColumn ();
  const dataRange = sh.getRange (2, 1, lastRow - 1, lastCol );
  const data = dataRange .getValues ();
  const backgrounds = dataRange .getBackgrounds ();
  // Sort by action priority (NEGATIVE_ADD first), then by co
st (highest first)
  const actionPriority = { "NEGATIVE_ADD" : 1, "MONITOR" : 2, 
"KEEP": 3, "HUMAN_REVIEW" : 4 };
  const actionCol = 1;  // Column B (0-indexed)
  const costCol = 13;   // Column N (0-indexed)
  // Create index array to sort both data and backgrounds tog
ether
  const indices = data.map((_, i) => i);
  indices.sort((a, b) => {
    const actionA = String(data[a][actionCol ] || "").toUpperC
Negative Keyword AI (v6 Architecture)

ase();
    const actionB = String(data[b][actionCol ] || "").toUpperC
ase();
    const prioA = actionPriority [actionA] || 99;
    const prioB = actionPriority [actionB] || 99;
    if (prioA !== prioB) return prioA - prioB;
    const costA = Number(data[a][costCol]) || 0;
    const costB = Number(data[b][costCol]) || 0;
    return costB - costA; // Higher cost first within same ac
tion
  });
  // Reorder data and backgrounds using sorted indices
  const sortedData = indices .map(i => data[i]);
  const sortedBgs = indices .map(i => backgrounds [i]);
  // Write back in single operations (2 API calls total)
  dataRange .setValues (sortedData );
  dataRange .setBackgrounds (sortedBgs );
}
/* ===== Sorting ===== */
function  sortOutputBySeverity (){
  const ss = SpreadsheetApp .getActive ();
  const sh = ss.getActiveSheet ();
  if(!sh || sh.getLastRow ()<2){ SpreadsheetApp .flush(); uiAle
rt_("No data to sort." ); return; }
  sortOutputBySeverityForSheet_ (sh);
  uiSuccess_ ("Output sorted by severity (most wasteful at to
p).", "✅ Sorted" );
}
function  sortOutputBySeverityForSheet_ (sh){
  // Cache dimensions to avoid multiple API calls
  const lastRow = sh ? sh.getLastRow () : 0;
Negative Keyword AI (v6 Architecture)

  const lastCol = sh ? sh.getLastColumn () : 0;
  if(!sh || lastRow < 2) {
    Logger.log("sortOutputBySeverityForSheet_: No data to sor
t (lastRow="  + lastRow + ")");
    return;
  }
  const CAT = {
    "DEFINITE WASTE" : 0,
    "LIKELY WASTE" : 1,
    "POTENTIAL WASTE" : 2,
    "QUESTIONABLE" : 3,
    "WATCH": 4,
    "GOOD": 5,
    "OPTIMAL" : 6,
    "FILTERED" : 7
  };
  const ACT = {
    "NEGATIVE_ADD" : 0,
    "HUMAN_REVIEW" : 1,
    "MONITOR" : 2,
    "KEEP": 3,
    "SKIP": 4
  };
  const dataRange = sh.getRange (2, 1, lastRow - 1, lastCol );
  const values = dataRange .getValues ();
  const header = sh.getRange (1, 1, 1, lastCol ).getValues ()
[0];
  const col = (name) => header.findIndex (h => String(h).toLow
erCase().includes (name.toLowerCase ()));
  const iCat = col("category" );
Negative Keyword AI (v6 Architecture)

  const iAct = col("action" );
  const iConf = col("confidence" );
  const iCost = col("cost");
  // CRITICAL: Validate that required columns exist before so
rting
  // Using -1 as array index causes silent failures (a[-1] =  
undefined)
  if (iCat === -1 || iAct === -1 || iCost === -1) {
    Logger.log("sortOutputBySeverityForSheet_: CRITICAL - Mis
sing required columns! "  +
               "category="  + iCat + ", action="  + iAct + ", c
ost=" + iCost);
    Logger.log("sortOutputBySeverityForSheet_: Headers found:  
" + JSON.stringify (header));
    return; // Don't sort with invalid columns - data would b
e corrupted
  }
  values.sort((a,b)=>{
    const aCat = CAT[String(a[iCat]||"").toUpperCase ()] ?? 99
9;
    const bCat = CAT[String(b[iCat]||"").toUpperCase ()] ?? 99
9;
    if(aCat !== bCat) return aCat - bCat;
    const aAct = ACT[String(a[iAct]||"").toUpperCase ()] ?? 9
9;
    const bAct = ACT[String(b[iAct]||"").toUpperCase ()] ?? 9
9;
    if(aAct !== bAct) return aAct - bAct;
    const aCost = Number(a[iCost] || 0);
    const bCost = Number(b[iCost] || 0);
    return bCost - aCost;
  });
Negative Keyword AI (v6 Architecture)

  dataRange .setValues (values);
}
/* ===== Color Coding ===== */
function  applyColorCoding_ (sh) {
  Logger.log("applyColorCoding_: Starting for sheet "  + (sh ? 
sh.getName() : "null"));
  // Cache getLastRow() and getLastColumn() - avoid multiple  
calls
  const lastRow = sh ? sh.getLastRow () : 0;
  const lastCol = sh ? sh.getLastColumn () : 0;
  if (!sh || lastRow < 2) {
    Logger.log("applyColorCoding_: No data to color (lastRow
=" + lastRow + ")");
    return;
  }
  const header = sh.getRange (1, 1, 1, lastCol ).getValues ()
[0];
  Logger.log("applyColorCoding_: Header = "  + header.join(", 
"));
  const actionCol = header.findIndex (h => String(h).toLowerCa
se() === "action" ) + 1;
  if (actionCol === 0) {
    Logger.log("applyColorCoding_: 'action' column not foun
d!");
    return;
  }
  Logger.log("applyColorCoding_: actionCol = "  + actionCol );
  const numRows = lastRow - 1;
Negative Keyword AI (v6 Architecture)

  if (numRows < 1) {
    Logger.log("applyColorCoding_: No data rows (numRows="  + 
numRows + ")");
    return;
  }
  const actionRange = sh.getRange (2, actionCol , numRows , 1);
  const actions = actionRange .getValues ();
  // Log sample of action values for debugging
  const sampleActions = actions .slice(0, 5).map(a => String(a
[0] || "").toUpperCase ());
  Logger.log("applyColorCoding_: Sample actions (first 5): "  
+ sampleActions .join(", "));
  // Uses shared ACTION_COLORS constant defined at top of fil
e (single source of truth)
  // Build background color array for batch update (much fast
er)
  const backgrounds = [];
  const colorCounts = {};
  for (let i = 0; i < numRows ; i++) {
    const action = String(actions[i][0] || "").toUpperCase ();
    const color = ACTION_COLORS [action] || "#ffffff" ;
    backgrounds .push(Array(lastCol).fill(color));
    colorCounts [action] = (colorCounts [action] || 0) + 1;
  }
  // Log color distribution
  Logger.log("applyColorCoding_: Color distribution: "  + JSO
N.stringify (colorCounts ));
  // Apply all colors in one batch operation
  sh.getRange (2, 1, numRows , lastCol ).setBackgrounds (backgrou
nds);
Negative Keyword AI (v6 Architecture)

  Logger.log("applyColorCoding_: Applied colors to "  + numRow
s + " rows successfully" );
}
/* ===== Auto-Resume Triggers ===== */
const MAX_AUTO_RESUME_RETRIES  = 10;  // Max auto-resume attem
pts before giving up
function  scheduleResumeOnce_ (){
  try {
    // Check retry counter to prevent infinite loops
    const retryCount = Number(NK_DP.getProperty ("nk_resume_re
tries") || 0);
    const currentCursor = NK_DP.getProperty ("nk_cursor" ) || 
"0";
    if (retryCount >= MAX_AUTO_RESUME_RETRIES ) {
      const logs = SpreadsheetApp .getActive ().getSheetByName
("Logs");
      if (logs) {
        logs.appendRow ([new Date(), "❌ MAX RETRIES" , `Giving 
up after ${MAX_AUTO_RESUME_RETRIES } auto-resume attempts at c
ursor ${currentCursor }. Please check API settings and try man
ually.`]);
      }
      SpreadsheetApp .getActive ().toast(
        `❌ Analysis stopped after ${MAX_AUTO_RESUME_RETRIES } 
failed attempts.\n\n ` +
        `Check Logs tab for errors.\n ` +
        `You can restart manually from the menu. `,
        "⚠  Auto-Resume Limit" , 30
      );
      return; // Don't schedule another resume
    }
    // Increment retry counter
Negative Keyword AI (v6 Architecture)

    NK_DP.setProperty ("nk_resume_retries" , String(retryCount 
+ 1));
    cancelResumeTrigger_ ();
    ScriptApp .newTrigger ('triggerResumeAnalysis_' ).timeBased
().after(90*1000).create();
  } catch(e) {
    Logger.log("Failed to schedule auto-resume: "  + e.messag
e);
  }
}
// Reset retry counter when batch succeeds (called when curso
r advances)
function  resetResumeRetries_ () {
  NK_DP.setProperty ("nk_resume_retries" , "0");
}
// Public function called by time-based trigger
function  triggerResumeAnalysis_ () {
  runChainAnalysis_ (true);
}
function  cancelResumeTrigger_ (){
  try {
    ScriptApp .getProjectTriggers ().forEach(t=>{
      if(t.getHandlerFunction ()==="triggerResumeAnalysis_" ) {
        ScriptApp .deleteTrigger (t);
      }
    });
  } catch(e) {
    Logger.log("Failed to cancel triggers: "  + e.message);
  }
}
/* ===== AI Autofill Context ===== */
Negative Keyword AI (v6 Architecture)

function  letAIAutofillContext (){
  const ss = SpreadsheetApp .getActive ();
  const cfgSheet = ss.getSheetByName ("Config" );
  const logs = getOrCreate_ (ss,"Logs");
  if(!cfgSheet ){ SpreadsheetApp .flush(); uiAlert_ ("Config she
et missing." ); return; }
  const cfg = readConfig_ (cfgSheet );
  if(!cfg.api_key){ SpreadsheetApp .flush(); uiAlert_ ("Add you
r API key in Config." ); return; }
  if(!cfg.target_url ){ SpreadsheetApp .flush(); uiAlert_ ("Set 
target_url in Config." ); return; }
  let html="";
  try{
    const res = UrlFetchApp .fetch(cfg.target_url ,{ muteHttpEx
ceptions :true, followRedirects :true });
    if(res.getResponseCode ()>=400) throw new Error("HTTP "+re
s.getResponseCode ());
    html = res.getContentText () || "";
  }catch(e){
    logs.appendRow ([new Date(),"Autofill FAIL" ,"Fetch error:  
"+e]);
    SpreadsheetApp .flush();
    uiAlert_ ("Could not fetch URL." );
    return;
  }
  const pageText = stripHtml_ (html).slice(0,60000);
  const extractionPrompt = [
    "Return ONLY valid JSON. Infer PPC context from page tex
t.",
    "Schema: {" ,
    "  \"brand_terms\":[]," ,
    "  \"services_offered\":[]," ,
    "  \"services_not_offered\":[]," ,
    "  \"primary_service_keywords\":[]," ,
Negative Keyword AI (v6 Architecture)

    "  \"adjacent_services_offered\":[]," ,
    "  \"buyer_persona\":\"\"," ,
    "  \"industry\":\"medical_aesthetics|dental|legal|hvac|ho
me_services|ecommerce|events|null\"," ,
    "  \"price_positioning\":\"premium|budget|unsure\"," ,
    "  \"funnel_target\":\"BOFU|MOFU|Full|unsure\"," ,
    "  \"locations_served\":[]," ,
    "  \"languages_supported\":[\"en\"]," ,
    "  \"notes\":\"\"" ,
    "}",
    "Page text:" ,
    pageText
  ].join("\n");
  let json;
  try{
    json = callLLM_ (cfg, "", extractionPrompt );
  }
  catch(e){
    logs.appendRow ([new Date(),"Autofill FAIL" ,"LLM error: "  
+ e.message]);
    SpreadsheetApp .flush();
    uiAlert_ (`Autofill failed: ${e.message.substring (0, 200)}
`);
    return;
  }
  const writes = [
    ["brand_terms" , JSON.stringify (json.brand_terms ||[])],
    ["services_offered" , JSON.stringify (json.services_offered
||[])],
    ["services_not_offered" , JSON.stringify (json.services_not
_offered ||[])],
    ["primary_service_keywords" , JSON.stringify (json.primary_
service_keywords ||[])],
    ["adjacent_services_offered" , JSON.stringify (json.adjacen
Negative Keyword AI (v6 Architecture)

t_services_offered ||[])],
    ["buyer_persona" , String(json.buyer_persona ||"")],
    ["industry" , String(json.industry ||"")],
    ["price_positioning" , String((json.price_positioning |
|"").toLowerCase ())],
    ["funnel_target" , String(json.funnel_target ||"")],
    ["locations_served" , JSON.stringify (json.locations_served
||[])]
  ];
  writes.forEach(p=> upsertConfigValueForce_ (cfgSheet ,p[0],p
[1]));
  logs.appendRow ([new Date(),"Autofill OK" ,json.notes||""]);
  uiSuccess_ ("Context extracted from landing page! Review Con
fig before running analysis." , "✅ Autofill Done" );
}
/* ===== Test API Connection ===== */
function  testApiConnection () {
  const ss = SpreadsheetApp .getActive ();
  const cfgSheet = ss.getSheetByName ("Config" );
  if (!cfgSheet ) {
    SpreadsheetApp .flush();
    uiAlert_ ("❌ Config sheet not found.\n\nRun ' 🔧  Setup All  
Templates' first." );
    return;
  }
  const cfg = readConfig_ (cfgSheet );
  const vendor = String(cfg.api_vendor || "openai" ).toLowerCa
se();
  const model = cfg.model || "";
  const apiKey = cfg.api_key || "";
  // Basic validation
  if (!apiKey || apiKey === "<<ADD YOUR KEY>>" ) {
Negative Keyword AI (v6 Architecture)

    const keyUrls = {
      anthropic : "console.anthropic.com/settings/keys" ,
      openai: "platform.openai.com/api-keys" ,
      gemini: "aistudio.google.com/apikey"
    };
    const vendorNames = { anthropic : "Anthropic" , openai: "Op
enAI", gemini: "Google Gemini"  };
    SpreadsheetApp .flush();
    uiAlert_ (`❌ No API key found.\n\nAdd your ${vendorNames
[vendor] || vendor} API key in Config.\n\nGet your key at:\n
${keyUrls[vendor] || keyUrls .openai}`);
    return;
  }
  ss.toast("Testing API connection..." , "🔑 Testing" , 10);
  try {
    // Simple test prompt
    const testPrompt = "Reply with exactly: CONNECTION_OK" ;
    if (vendor === "anthropic" ) {
      testAnthropicConnection_ (cfg, testPrompt );
    } else if (vendor === "gemini" ) {
      testGeminiConnection_ (cfg, testPrompt );
    } else {
      testOpenAIConnection_ (cfg, testPrompt );
    }
    const vendorNames = { anthropic : "Anthropic" , openai: "Op
enAI", gemini: "Google Gemini"  };
    uiSuccess_ (`API connected! Provider: ${vendorNames [vendo
r] || vendor}, Model: ${model}. Ready to run analysis. `, "✅ 
Connection OK" );
  } catch (e) {
    const errorMsg = e.message || "Unknown error" ;
Negative Keyword AI (v6 Architecture)

    ss.toast("API connection failed" , "❌ Failed" , 5);
    // Provide helpful guidance based on error
    let guidance = "";
    const keyUrls = {
      anthropic : "console.anthropic.com/settings/keys" ,
      openai: "platform.openai.com/api-keys" ,
      gemini: "aistudio.google.com/apikey"
    };
    const vendorNames = { anthropic : "Anthropic" , openai: "Op
enAI", gemini: "Google Gemini"  };
    if (errorMsg .includes ("401") || errorMsg .includes ("invali
d") || errorMsg .includes ("Invalid" ) || errorMsg .includes ("API
_KEY")) {
      guidance = `\n\n🔧 FIX: Your API key is invalid.\n\nGet  
a valid key at:\n ${keyUrls[vendor] || keyUrls .openai}`;
    }
    else if (errorMsg .includes ("429") || errorMsg .includes ("r
ate") || errorMsg .includes ("quota") || errorMsg .includes ("ins
ufficient" ) || errorMsg .includes ("RESOURCE_EXHAUSTED" )) {
      if (vendor === "anthropic" ) {
        guidance = "\n\n🔧 FIX: No credits or rate limited.\n
\nAdd billing credits at:\nconsole.anthropic.com/settings/bil
ling";
      } else if (vendor === "gemini" ) {
        guidance = "\n\n🔧 FIX: Rate limited.\n\nGemini has g
enerous free tier - wait a minute and retry, or upgrade at:\n
console.cloud.google.com/billing" ;
      } else {
        guidance = "\n\n🔧 FIX: No credits or rate limited.\n
\n⚠  ChatGPT Plus does NOT include API credits!\n\nAdd API cre
dits ($5 min) at:\nplatform.openai.com/settings/organization/
billing" ;
      }
    }
Negative Keyword AI (v6 Architecture)

    else if (errorMsg .includes ("404") || errorMsg .includes ("n
ot found" ) || errorMsg .includes ("does not exist" )) {
      guidance = `\n\n🔧 FIX: Model " ${model}" not found.\n\n
Check the MODEL OPTIONS section in Config for valid model nam
es.`;
    }
    else if (errorMsg .includes ("permission" ) || errorMsg .incl
udes("access" )) {
      const fallbacks = { anthropic : "claude-3-5-haiku-202410
22", openai: "gpt-4o-mini" , gemini: "gemini-2.0-flash"  };
      guidance = `\n\n🔧 FIX: No access to this model.\n\nTr
y: ${fallbacks [vendor] || fallbacks .openai}`;
    }
    // Use toast instead of blocking alert to avoid "Workin
g..." spinner
    SpreadsheetApp .flush();
    ss.toast(`❌ FAILED: ${errorMsg .substring (0, 80)}${guidan
ce ? '\n' + guidance .substring (0, 100) : ''}`, "API Connectio
n Failed" , 30);
    Logger.log(`API Test Failed: ${errorMsg }${guidance }`);
  }
}
function  testOpenAIConnection_ (cfg, testPrompt ) {
  const url = "https://api.openai.com/v1/chat/completions" ;
  const model = String(cfg.model || "gpt-4o-mini" );
  const body = {
    model,
    messages : [{ role: "user", content: testPrompt }],
    max_tokens : 20
  };
  const res = UrlFetchApp .fetch(url, {
    method: "post",
Negative Keyword AI (v6 Architecture)

    contentType : "application/json" ,
    headers: { Authorization : "Bearer "  + cfg.api_key },
    payload: JSON.stringify (body),
    muteHttpExceptions : true
  });
  const statusCode = res.getResponseCode ();
  const txt = res.getContentText ();
  if (statusCode !== 200) {
    let data;
    try { data = JSON.parse(txt); } catch (e) {}
    const errorMsg = data?.error?.message || txt.substring (0, 
200);
    throw new Error(`(${statusCode }) ${errorMsg }`);
  }
}
function  testAnthropicConnection_ (cfg, testPrompt ) {
  const url = "https://api.anthropic.com/v1/messages" ;
  let model = String(cfg.model || "claude-opus-4-5-2025110
1");
  // Validate model format
  if (model && !model.startsWith ("claude-" )) {
    throw new Error(`Invalid model " ${model}". Anthropic mode
ls start with "claude-" `);
  }
  const body = {
    model,
    max_tokens : 20,
    messages : [{ role: "user", content: testPrompt }]
  };
  const res = UrlFetchApp .fetch(url, {
Negative Keyword AI (v6 Architecture)

    method: "post",
    contentType : "application/json" ,
    headers: { "x-api-key" : cfg.api_key, "anthropic-version" : 
"2023-06-01"  },
    payload: JSON.stringify (body),
    muteHttpExceptions : true
  });
  const statusCode = res.getResponseCode ();
  const txt = res.getContentText ();
  if (statusCode !== 200) {
    let data;
    try { data = JSON.parse(txt); } catch (e) {}
    const errorMsg = data?.error?.message || txt.substring (0, 
200);
    throw new Error(`(${statusCode }) ${errorMsg }`);
  }
}
function  testGeminiConnection_ (cfg, testPrompt ) {
  const model = String(cfg.model || "gemini-2.0-flash" );
  const url = `https://generativelanguage.googleapis.com/v1be
ta/models/ ${model}:generateContent?key= ${cfg.api_key}`;
  const body = {
    contents : [{ parts: [{ text: testPrompt }] }],
    generationConfig : { maxOutputTokens : 20 }
  };
  const res = UrlFetchApp .fetch(url, {
    method: "post",
    contentType : "application/json" ,
    payload: JSON.stringify (body),
    muteHttpExceptions : true
  });
Negative Keyword AI (v6 Architecture)

  const statusCode = res.getResponseCode ();
  const txt = res.getContentText ();
  if (statusCode !== 200) {
    let data;
    try { data = JSON.parse(txt); } catch (e) {}
    const errorMsg = data?.error?.message || txt.substring (0, 
200);
    throw new Error(`(${statusCode }) ${errorMsg }`);
  }
}
/* ===== LLM Calls ===== */
function  callLLM_ (cfg, systemPrompt , userContent ){
  const vendor = String(cfg.api_vendor ||"openai" ).toLowerCase
();
  if(vendor==="anthropic" ) return callAnthropicJSON_ (cfg, sys
temPrompt , userContent );
  if(vendor==="gemini" ) return callGeminiJSON_ (cfg, systemPro
mpt, userContent );
  return callOpenAIJSON_ (cfg, systemPrompt , userContent );
}
/* ===== Parallel LLM Calls using fetchAll ===== */
function  callLLMParallel_ (cfg, systemPrompt , payloads ) {
  const vendor = String(cfg.api_vendor ||"openai" ).toLowerCase
();
  const requests = payloads .map(payload => {
    if(vendor === "anthropic" ) {
      return buildAnthropicRequest_ (cfg, systemPrompt , JSON.s
tringify (payload));
    } else if(vendor === "gemini" ) {
      return buildGeminiRequest_ (cfg, systemPrompt , JSON.stri
ngify(payload));
Negative Keyword AI (v6 Architecture)

    } else {
      return buildOpenAIRequest_ (cfg, systemPrompt , JSON.stri
ngify(payload));
    }
  });
  // Execute all requests in parallel
  const responses = UrlFetchApp .fetchAll (requests );
  // Parse responses
  return responses .map((res, idx) => {
    let txt = "";
    let content = "";  // Declare outside try so catch can ac
cess it
    try {
      const statusCode = res.getResponseCode ();
      txt = res.getContentText ();
      if(statusCode !== 200) {
        let data; try { data = JSON.parse(txt); } catch(e) {}
        const errorMsg = data?.error?.message || txt.substrin
g(0, 200);
        throw new Error(`API error ( ${statusCode }): ${errorMs
g}`);
      }
      if(vendor === "anthropic" ) {
        const data = JSON.parse(txt);
        content = data?.content?.[0]?.text || "";
        const stopReason = data?.stop_reason || "unknown" ;
        if(stopReason === "max_tokens" ) {
          Logger.log("WARNING: Response truncated (max_tokens  
reached)" );
        }
        if(!content) {
          throw new Error(`Empty response (stop_reason: ${sto
pReason})`);
Negative Keyword AI (v6 Architecture)

        }
        return { success: true, data: safeJson_ (content), ind
ex: idx };
      } else if(vendor === "gemini" ) {
        const data = JSON.parse(txt);
        content = data?.candidates ?.[0]?.content?.parts?.
[0]?.text || "";
        const finishReason = data?.candidates ?.[0]?.finishRea
son || "unknown" ;
        if(!content) {
          throw new Error(`Empty response (finishReason: ${fi
nishReason })`);
        }
        return { success: true, data: safeJson_ (content), ind
ex: idx };
      } else {
        const data = JSON.parse(txt);
        content = data?.choices?.[0]?.message?.content || "";
        const finishReason = data?.choices?.[0]?.finish_reaso
n || "unknown" ;
        if(!content) {
          throw new Error(`Empty response (finish_reason: ${f
inishReason })`);
        }
        return { success: true, data: safeJson_ (content), ind
ex: idx };
      }
    } catch(e) {
      // Show actual AI content that failed to parse, not the  
API wrapper
      const preview = content ? content .substring (0, 150) : 
(txt ? txt.substring (0, 100) : "(empty)" );
      return { success: false, error: `${e.message} | AI sai
d: ${preview}...`, index: idx };
    }
  });
Negative Keyword AI (v6 Architecture)

}
function  buildOpenAIRequest_ (cfg, systemPrompt , userContent ) 
{
  const model = String(cfg.model||"gpt-4o-mini" );
  const messages = systemPrompt
    ? [{role:"system" ,content:systemPrompt },{role:"user",cont
ent:userContent }]
    : [{role:"user",content:userContent }];
  const body = { model, response_format :{type:"json_object" }, 
messages , temperature : 0.1 };
  return {
    url: "https://api.openai.com/v1/chat/completions" ,
    method: "post",
    contentType : "application/json" ,
    headers: { Authorization : "Bearer "  + cfg.api_key },
    payload: JSON.stringify (body),
    muteHttpExceptions : true
  };
}
function  buildAnthropicRequest_ (cfg, systemPrompt , userConten
t) {
  let model = String(cfg.model||"claude-opus-4-5-20251101" );
  const body = {
    model,
    max_tokens : 8192, // Must be enough for 40 terms × ~150 t
okens = 6000 tokens
    temperature : 0.1,
    system: systemPrompt || "",
    messages : [{role:"user",content:userContent }]
  };
  return {
Negative Keyword AI (v6 Architecture)

    url: "https://api.anthropic.com/v1/messages" ,
    method: "post",
    contentType : "application/json" ,
    headers: { "x-api-key" : cfg.api_key, "anthropic-version" : 
"2023-06-01"  },
    payload: JSON.stringify (body),
    muteHttpExceptions : true
  };
}
function  buildGeminiRequest_ (cfg, systemPrompt , userContent ) 
{
  const model = String(cfg.model || "gemini-2.0-flash" );
  const combinedPrompt = systemPrompt
    ? `${systemPrompt }\n\n---\n\n ${userContent }`
    : userContent ;
  const body = {
    contents : [{ parts: [{ text: combinedPrompt }] }],
    generationConfig : {
      temperature : 0.1,
      maxOutputTokens : 8192,  // Must be enough for 40 terms  
× ~150 tokens
      responseMimeType : "application/json"
    }
  };
  return {
    url: `https://generativelanguage.googleapis.com/v1beta/mo
dels/${model}:generateContent?key= ${cfg.api_key}`,
    method: "post",
    contentType : "application/json" ,
    payload: JSON.stringify (body),
    muteHttpExceptions : true
  };
}
Negative Keyword AI (v6 Architecture)

function  callGeminiJSON_ (cfg, systemPrompt , userContent ) {
  if(!cfg.api_key) throw new Error("Missing Gemini API key! G
et one at: aistudio.google.com/apikey" );
  const model = String(cfg.model || "gemini-2.0-flash" );
  const combinedPrompt = systemPrompt
    ? `${systemPrompt }\n\n---\n\n ${userContent }`
    : userContent ;
  const body = {
    contents : [{ parts: [{ text: combinedPrompt }] }],
    generationConfig : {
      temperature : 0.1,
      maxOutputTokens : 8192,  // Must be enough for 40 terms  
× ~150 tokens
      responseMimeType : "application/json"
    }
  };
  const url = `https://generativelanguage.googleapis.com/v1be
ta/models/ ${model}:generateContent?key= ${cfg.api_key}`;
  const res = UrlFetchApp .fetch(url, {
    method: "post",
    contentType : "application/json" ,
    payload: JSON.stringify (body),
    muteHttpExceptions : true
  });
  const statusCode = res.getResponseCode ();
  const txt = res.getContentText ();
  if(statusCode !== 200) {
    let data; try { data = JSON.parse(txt); } catch(e) {}
    const errorMsg = data?.error?.message || txt.substring (0, 
Negative Keyword AI (v6 Architecture)

200);
    throw new Error(`Gemini API error ( ${statusCode }): ${erro
rMsg}`);
  }
  const data = JSON.parse(txt);
  const content = data?.candidates ?.[0]?.content?.parts?.
[0]?.text || "";
  if(!content) {
    const finishReason = data?.candidates ?.[0]?.finishReason 
|| "unknown" ;
    throw new Error(`Empty Gemini response (finishReason: ${f
inishReason })`);
  }
  return safeJson_ (content);
}
function  callOpenAIJSON_ (cfg, systemPrompt , userContent ){
  if(!cfg.api_key) throw new Error("Missing OpenAI API ke
y!");
  const url = "https://api.openai.com/v1/chat/completions" ;
  const model = String(cfg.model||"gpt-4o-mini" );
  const messages = systemPrompt
    ? [{role:"system" ,content:systemPrompt },{role:"user",cont
ent:userContent }]
    : [{role:"user",content:userContent }];
  const body = { model, response_format :{type:"json_object" }, 
messages , temperature : 0.1 };
  const res = UrlFetchApp .fetch(url,{
    method:"post", contentType :"application/json" ,
    headers:{ Authorization :"Bearer " +cfg.api_key },
    payload: JSON.stringify (body), muteHttpExceptions :true
Negative Keyword AI (v6 Architecture)

  });
  const statusCode = res.getResponseCode ();
  const txt = res.getContentText ();
  if(statusCode !== 200) {
    let data; try { data = JSON.parse(txt); } catch(e) {}
    const errorMsg = data?.error?.message || txt.substring (0, 
200);
    throw new Error(`OpenAI API error ( ${statusCode }): ${erro
rMsg}`);
  }
  const data = JSON.parse(txt);
  const content = data?.choices?.[0]?.message?.content || "";
  return safeJson_ (content);
}
function  callAnthropicJSON_ (cfg, systemPrompt , userContent ){
  if(!cfg.api_key) throw new Error("Missing Anthropic API ke
y!");
  const url = "https://api.anthropic.com/v1/messages" ;
  let model = String(cfg.model||"claude-opus-4-5-20251101" );
  // Validate model name format - common mistake is using sho
rt names
  if(model && !model.startsWith ("claude-" )) {
    throw new Error(`Invalid model name " ${model}". Use full  
Anthropic model ID like: claude-opus-4-5-20251101, claude-son
net-4-20250514, or claude-3-5-sonnet-latest `);
  }
  const body = {
    model,
    max_tokens : 4000,
Negative Keyword AI (v6 Architecture)

    temperature : 0.1,
    system: systemPrompt || "",
    messages : [{role:"user",content:userContent }]
  };
  const res = UrlFetchApp .fetch(url,{
    method:"post", contentType :"application/json" ,
    headers:{ "x-api-key" :cfg.api_key, "anthropic-version" :"2
023-06-01"  },
    payload: JSON.stringify (body), muteHttpExceptions :true
  });
  const statusCode = res.getResponseCode ();
  const txt = res.getContentText ();
  if(statusCode !== 200) {
    let data; try { data = JSON.parse(txt); } catch(e) {}
    const errorMsg = data?.error?.message || txt.substring (0, 
200);
    if(statusCode === 404) {
      throw new Error(`Model "${model}" not found. Use: claud
e-opus-4-5-20251101, claude-sonnet-4-20250514, or claude-3-5-
sonnet-latest `);
    }
    throw new Error(`Anthropic API error ( ${statusCode }): ${e
rrorMsg}`);
  }
  const data = JSON.parse(txt);
  const content = data?.content?.[0]?.text || "";
  return safeJson_ (content);
}
/* ===== Negatives CSV Export ===== */
function  makeNegativesCSV (){
  const ss = SpreadsheetApp .getActive ();
Negative Keyword AI (v6 Architecture)

  const out = ss.getActiveSheet ();
  const cfgSheet = ss.getSheetByName ("Config" );
  if(!out || out.getLastRow () < 2){
    SpreadsheetApp .flush();
    uiAlert_ ("No output data. Switch to an Output tab firs
t.");
    return;
  }
  const cfg = cfgSheet ? readConfig_ (cfgSheet ) : {};
  const vals = out.getDataRange ().getValues ();
  if(vals.length<2){ SpreadsheetApp .flush(); uiAlert_ ("Output 
has no rows." ); return; }
  const head = vals.shift();
  const col = (name)=> head.indexOf(name);
  const idx = {
    term: col("term"),
    action: col("action" ),
    suggested : col("negative_keyword" ) !== -1 ? col("negative
_keyword" ) : col("suggested_negative" ), // backwards compatib
le
    match: col("match_type" ),
    level: col("level")
  };
  const rows = [];
  const seen = new Set();
  for(const r of vals){
    const action = String(r[idx.action]||"").toUpperCase ();
    if(action!=="NEGATIVE_ADD" ) continue ;
    // Parse level (handles both "CAMPAIGN" and "Campaign-lev
Negative Keyword AI (v6 Architecture)

el" formats)
    const levelRaw = String(r[idx.level]||"CAMPAIGN" ).toUpper
Case();
    const level = levelRaw .includes ("AD") ? "AD_GROUP"  : "CAM
PAIGN";
    // Parse match type (handles "[exact]", "[phrase]", "broa
d", "EXACT", "PHRASE", "BROAD")
    const matchRaw = String(r[idx.match]||"PHRASE" ).toLowerCa
se().replace(/[\[\]]/g, "");
    const matchType = matchRaw .toUpperCase ();
    const kw = String(r[idx.suggested ]||r[idx.term]||"").trim
().toLowerCase ().replace(/\s+/g," ");
    if(!kw) continue ;
    const matchLabel = (matchType ==="EXACT"?"Exact": matchTyp
e==="BROAD"?"Broad":"Phrase" );
    const key = [level,matchLabel ,kw].join("|");
    if(seen.has(key)) continue ; seen.add(key);
    const campaign = cfg.campaign_name || "";
    const adgroup = (level==="AD_GROUP" ) ? (cfg.ad_group_name
||"") : "";
    rows.push([campaign , adgroup , matchLabel , kw]);
  }
  const negSh = getOrCreate_ (ss,"NegativesCSV" );
  negSh.clearContents ();
  negSh.clearFormats ();
  negSh.appendRow (["Campaign" ,"Ad group" ,"Match type" ,"Negati
ve keyword" ]);
  negSh.getRange (1,1,1,4).setBackground ("#34a853" ).setFontCol
or("white").setFontWeight ("bold");
Negative Keyword AI (v6 Architecture)

  if(rows.length) {
    negSh.getRange (2,1,rows.length,4).setValues (rows);
    negSh.autoResizeColumns (1, 4);
    const csv = "Campaign,Ad group,Match type,Negative keywor
d\n" + rows.map(r=>r.map(csvEscape_ ).join(",")).join("\n");
    const name = "negatives_export_"  + Utilities .formatDate (n
ew Date(), Session .getScriptTimeZone (), "yyyyMMdd_HHmmss" ) + 
".csv";
    const file = DriveApp .createFile (name, csv, MimeType .CS
V);
    uiSuccess_ (`${rows.length} negatives exported!\n\n 📁  CSV 
saved to Google Drive\n 📋  NegativesCSV tab ready\n\nNEXT: Ope
n Google Ads Editor → Account → Import → Paste from clipboard
`, "✅ Export Done" );
  } else {
    uiSuccess_ ("No NEGATIVE_ADD rows found to export." , "ℹ N
othing to Export" );
  }
}
function  csvEscape_ (s){ const str=String(s==null?"":s); retur
n /[\",\n]/.test(str)?('"'+str.replace(/"/g,'""')+'"'):str; }
/* ===== Clear Output ===== */
function  clearOutput (){
  const ss = SpreadsheetApp .getActive ();
  const sh = ss.getActiveSheet ();
  if(!sh){ SpreadsheetApp .flush(); uiAlert_ ("No sheet selecte
d."); return; }
  let confirmed = true;
  if(hasUi_()) {
    const ui = SpreadsheetApp .getUi();
    const response = ui.alert(
      "Clear Output?" ,
Negative Keyword AI (v6 Architecture)

      `Clear all data in " ${sh.getName()}"?`,
      ui.ButtonSet .OK_CANCEL
    );
    confirmed = (response === ui.Button.OK);
  }
  if(!confirmed ) { SpreadsheetApp .flush(); return; }
  initializeOutputSheet_ (sh);
  uiSuccess_ ("Output cleared and ready for new analysis." , 
"✅ Cleared" );
}
/* ===== Instructions Tab ===== */
function  createOrRefreshInstructions (){
  const ss = SpreadsheetApp .getActive ();
  const sh = ss.getSheetByName ("Instructions" ) || ss.insertSh
eet("Instructions" );
  sh.clearContents ();
  sh.getRange (1,1).setValue ("Negative Keyword AI v6.1 — Chain  
Architecture Guide" );
  sh.getRange (1,1).setFontSize (16).setFontWeight ("bold").setB
ackground ("#4285f4" ).setFontColor ("white");
  const content = [
    ["ARCHITECTURE OVERVIEW" , "", ""],
    ["Step 1:" , "Conversion & Brand Protection" , "Instant KEE
P for converting terms and brand matches" ],
    ["Step 2:" , "Primary Service Flagging" , "Soft-protect ter
ms containing your services" ],
    ["Step 3:" , "Universal Patterns" , "Auto-negate employmen
t, navigation, forum, DIY terms" ],
    ["Step 4:" , "Alternative-Seeker Detection" , "Flag compari
son shoppers as valuable" ],
    ["Step 5:" , "Low-Value Filtering" , "Skip single impressio
Negative Keyword AI (v6 Architecture)

ns, trivial spend" ],
    ["Step 6:" , "AI Analysis" , "Only ambiguous terms go to AI  
(40-60% savings!)" ],
    ["Step 6.5:" , "CPC Enrichment" , "Add cost context to rati
onales"],
    ["Step 7:" , "Final Guardrails" , "Override unsafe AI recom
mendations" ],
    ["", "", ""],
    ["SETUP STEPS" , "", ""],
    ["1)", "Add API details in Config" , "api_vendor, model, a
pi_key, target_url, project_name" ],
    ["2)", "Paste Google Ads export into RawExport" , "Include  
the header row" ],
    ["3)", "Normalize pasted data" , "Menu: 🔄  Normalize Paste
d Data"],
    ["4)", "Auto-fill context (optional)" , "Menu: ✨  Auto-Fil
l Config with AI" ],
    ["5)", "Run analysis" , "Menu: ▶ Run Chain Analysis" ],
    ["6)", "Review results" , "Output tab auto-sorted by sever
ity"],
    ["7)", "Export negatives" , "Menu: Make Negatives CSV" ],
    ["", "", ""],
    ["NEW IN v6.1" , "", ""],
    ["📊", "Executive Summary" , "Spend at Risk and key stats  
at top of output" ],
    ["★★★★★", "Confidence Stars" , "Visual confidence indicato
rs for each recommendation" ],
    ["🎯", "What's Next Section" , "Actionable guidance at bot
tom of output" ],
    ["⚡", "Parallel API Calls" , "3x faster analysis using fet
chAll()" ],
    ["✅", "Data Validation" , "Validates config before starti
ng analysis" ],
    ["", "", ""],
    ["KEY IMPROVEMENTS IN v6" , "", ""],
    ["✅", "40-60% AI cost reduction" , "Mechanical steps hand
Negative Keyword AI (v6 Architecture)

le obvious cases" ],
    ["✅", "Triple protection for conversions" , "Step 1, Step  
6 flags, Step 7 guardrail" ],
    ["✅", "Synonym expansion" , "Auto-detects industry and lo
ads synonyms" ],
    ["✅", "Alternative-seeker protection" , "Comparison shopp
ers flagged as valuable" ],
    ["✅", "CPC context enrichment" , "Cost insights added to  
rationales" ]
  ];
  sh.getRange (2,1,content.length,3).setValues (content);
  sh.getRange (2,1,1,3).setFontWeight ("bold").setBackground ("#
34a853").setFontColor ("white");  // Architecture
  sh.getRange (12,1,1,3).setFontWeight ("bold").setBackground
("#34a853" ).setFontColor ("white"); // Setup Steps
  sh.getRange (21,1,1,3).setFontWeight ("bold").setBackground
("#1a73e8" ).setFontColor ("white"); // NEW in v6.1
  sh.getRange (28,1,1,3).setFontWeight ("bold").setBackground
("#34a853" ).setFontColor ("white"); // Key Improvements
  sh.setColumnWidths (1,1,100);
  sh.setColumnWidths (2,1,300);
  sh.setColumnWidths (3,1,400);
  sh.getRange (1,1,content.length+1,3).setWrap(true);
  sh.setFrozenRows (1);
  uiSuccess_ ("Instructions tab created with setup guide." , 
"✅ Instructions" );
}
/* ===== Config & Data I/O ===== */
function  readConfig_ (sh){
  const obj = {};
  if(!sh) return obj;
  sh.getDataRange ().getValues ().forEach(r=>{ if(r[0]) obj[Str
Negative Keyword AI (v6 Architecture)

ing(r[0]).trim()] = parseMaybeJson_ (r[1]); });
  // API Settings
  obj.api_vendor = obj.api_vendor || "anthropic" ;
  obj.model = obj.model || (obj.api_vendor ==="anthropic"  ? "c
laude-3-5-haiku-20241022"  : "gpt-4o-mini" );
  obj.project_name = obj.project_name || "";
  // Industry & Synonyms
  obj.synonym_groups = obj.synonym_groups || [];
  obj.industry = obj.industry || null;
  // Export Settings
  obj.campaign_name = obj.campaign_name || "";
  obj.ad_group_name = obj.ad_group_name || "";
  // Business Context
  obj.brand_terms = obj.brand_terms || [];
  obj.services_offered = obj.services_offered || [];
  obj.services_not_offered = obj.services_not_offered || [];
  obj.primary_service_keywords = obj.primary_service_keywords  
|| [];
  obj.adjacent_services_offered = obj.adjacent_services_offer
ed || [];
  obj.buyer_persona = obj.buyer_persona || "";
  obj.custom_context = obj.custom_context || "";  // NEW: Fre
e-form user notes
  // Strategy Settings
  obj.allow_competitor_terms = String(obj.allow_competitor_te
rms || "false").toLowerCase () === "true";
  obj.allow_cross_modality = String(obj.allow_cross_modality 
|| "false").toLowerCase () === "true";
  obj.price_positioning = obj.price_positioning || "premium" ;
  obj.funnel_target = obj.funnel_target || "BOFU";
  obj.locations_served = obj.locations_served || [];
Negative Keyword AI (v6 Architecture)

  obj.languages_supported = obj.languages_supported || ["e
n"];
  // Analysis Settings
  obj.target_cpa = Number(obj.target_cpa || 0) || null;
  obj.expected_conv_rate = (obj.expected_conv_rate !=null ? Nu
mber(obj.expected_conv_rate ) : null);
  obj.min_clicks_to_analyze = Number(obj.min_clicks_to_analyz
e ?? 1);
  obj.min_impressions_to_analyze = Number(obj.min_impressions
_to_analyze ?? 20);
  obj.select_metric = (obj.select_metric || "cost").toString
().toLowerCase ();
  obj.select_top_n = obj.select_top_n != null ? Number(obj.se
lect_top_n ) : 200; // Allow 0 to mean "all terms"
  obj.date_range_days = Number(obj.date_range_days || 30);
  obj.auto_resume = String(obj.auto_resume ?? "true").toLower
Case()==="true";
  return obj;
}
function  readCol_ (sh,col){
  if(!sh || sh.getLastRow ()<2) return [];
  const startRow = (sh.getName() === "ExistingNegatives" ) ? 6 
: 2;
  if(sh.getLastRow () < startRow ) return [];
  return sh.getRange (startRow ,col,sh.getLastRow ()-startRow +1,
1).getValues ().map(r=>r[0]).filter(Boolean);
}
function  readTerms_ (sh){
  if(!sh || sh.getLastRow ()<2) return [];
  const vals = sh.getDataRange ().getValues ();
  const head = vals.shift();
  const cols = {};
Negative Keyword AI (v6 Architecture)

  head.forEach((h,i)=> cols[String(h).trim()] = i);
  return vals.map(r=>{
    const t = String(r[cols["term"]]||"").trim();
    if(!t) return null;
    return {
      term: t,
      impressions : toNum_(r[cols["impressions" ]]),
      clicks: toNum_(r[cols["clicks" ]]),
      cost: toNum_(r[cols["cost"]]),
      conversions : toNum_(r[cols["conversions" ]]),
      view_through_conversions : toNum_(r[cols["view_through_c
onversions" ]] ?? r[cols["View-through conv." ]])
    };
  }).filter(Boolean);
}
/* ===== Executive Summary & UX Enhancements ===== */
function  addExecutiveSummary_ (outSheet , stats, cfg) {
  Logger.log("addExecutiveSummary_: Starting..." );
  const lastRow = outSheet .getLastRow ();
  const lastCol = outSheet .getLastColumn ();
  if (lastRow < 2) {
    Logger.log("addExecutiveSummary_: No data (lastRow="  + la
stRow + ")");
    return;
  }
  // Read only header row to find column indices (not entire  
sheet)
  const header = outSheet .getRange (1, 1, 1, lastCol ).getValue
s()[0];
  const actionCol = header.findIndex (h => String(h).toLowerCa
se() === "action" );
  const costCol = header.findIndex (h => String(h).toLowerCase
Negative Keyword AI (v6 Architecture)

() === "cost");
  if (actionCol === -1 || costCol === -1) {
    Logger.log("addExecutiveSummary_: Missing columns. action
=" + actionCol + ", cost="  + costCol );
    return;
  }
  // Read ONLY the two columns we need (not entire sheet - 7x  
more efficient)
  const numDataRows = lastRow - 1;
  const actionValues = outSheet .getRange (2, actionCol + 1, nu
mDataRows , 1).getValues ();
  const costValues = outSheet .getRange (2, costCol + 1, numDat
aRows, 1).getValues ();
  let spendAtRisk = 0;
  let negativeCount = 0;
  let reviewCount = 0;
  let keepCount = 0;
  for (let i = 0; i < numDataRows ; i++) {
    const action = String(actionValues [i][0] || "").toUpperCa
se();
    const cost = Number(costValues [i][0] || 0);
    if (action === "NEGATIVE_ADD" ) {
      spendAtRisk += cost;
      negativeCount ++;
    } else if (action === "HUMAN_REVIEW"  || action === "MONIT
OR") {
      reviewCount ++;
    } else if (action === "KEEP" || action === "SKIP") {
      keepCount ++;
    }
  }
Negative Keyword AI (v6 Architecture)

  // Insert summary rows at the top (after header)
  outSheet .insertRowsAfter (1, 5);
  // Calculate AI savings
  // BATCHED: Set all values in one call (was: 10+ individual  
setValue calls)
  const summaryValues = [
    ["📊 EXECUTIVE SUMMARY" , "", "", "", "", "", "", "", "", 
"", "", "", "", ""],
    ["💰 Spend at Risk:" , "", "", "$" + spendAtRisk .toFixed
(2), "", "", "", "", "", "", "", "", "", ""],
    ["🚫 To Negate: "  + negativeCount , "", "👀 Review: "  + re
viewCount , "", "✅ Keep: "  + keepCount , "", "", "", "", "", 
"", "", "", ""],
    ["🤖 " + stats.forAI + " terms analyzed by AI" , "", "", 
"", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]  
// Separator row
  ];
  outSheet .getRange (2, 1, 5, 14).setValues (summaryValues );
  // BATCHED: Apply all merges (grouped for clarity)
  outSheet .getRange (2, 1, 1, 14).merge();  // Title row
  outSheet .getRange (3, 1, 1, 3).merge();   // "Spend at Ris
k:" label
  outSheet .getRange (3, 4, 1, 3).merge();   // Spend value
  outSheet .getRange (4, 1, 1, 2).merge();   // Negate count
  outSheet .getRange (4, 3, 1, 2).merge();   // Review count
  outSheet .getRange (4, 5, 1, 2).merge();   // Keep count
  outSheet .getRange (5, 1, 1, 6).merge();   // AI savings row
  outSheet .getRange (6, 1, 1, 14).merge();  // Separator
  // BATCHED: Apply backgrounds in one call (was: 3 individua
l setBackground calls)
  const backgrounds = [
Negative Keyword AI (v6 Architecture)

    Array(14).fill("#1a73e8" ),  // Title - blue
    Array(14).fill("#ffffff" ),  // Spend row - white
    Array(14).fill("#ffffff" ),  // Stats row - white
    Array(14).fill("#ffffff" ),  // AI savings - white
    Array(14).fill("#e8eaed" )   // Separator - gray
  ];
  outSheet .getRange (2, 1, 5, 14).setBackgrounds (backgrounds );
  // Apply text formatting (these need individual calls for d
ifferent styles per row)
  outSheet .getRange (2, 1).setFontSize (14).setFontWeight ("bol
d").setFontColor ("white").setHorizontalAlignment ("center" );
  outSheet .getRange (3, 1).setFontWeight ("bold").setFontColor
("black");
  outSheet .getRange (3, 4).setFontSize (16).setFontWeight ("bol
d").setFontColor ("#d93025" );
  outSheet .getRange (4, 1, 1, 6).setFontWeight ("bold").setFont
Color("black");
  outSheet .getRange (5, 1).setFontStyle ("italic" ).setFontColor
("#5f6368" );
  Logger.log("addExecutiveSummary_: Complete - Spend at risk:  
$" + spendAtRisk .toFixed(2));
}
function  renderConfidenceStars_ (confidence ) {
  if (confidence == null || confidence === "") return "";
  const conf = Number(confidence );
  if (conf >= 0.9) return "★★★★★";
  if (conf >= 0.8) return "★★★★☆";
  if (conf >= 0.7) return "★★★☆☆";
  if (conf >= 0.6) return "★★☆☆☆";
  return "★☆☆☆☆";
}
function  addWhatsNext_ (outSheet , stats) {
Negative Keyword AI (v6 Architecture)

  const lastRow = outSheet .getLastRow ();
  const startRow = lastRow + 2;
  // Guidance content
  const guidance = [
    ["󾠮", "Review HUMAN_REVIEW items first" , "These need you
r expert judgment" ],
    ["󾠯", "Spot-check NEGATIVE_ADD recommendations" , "Especi
ally high-spend items at the top" ],
    ["󾠰", "Export negatives via menu" , "Menu → Make Negative
s CSV → Upload to Google Ads" ],
    ["󾠱", "Monitor WATCH items weekly" , "These may need futu
re action" ]
  ];
  // BATCHED: Build all values at once (was: 20+ individual s
etValue calls in a loop)
  const allValues = [
    // Row 0: Separator
    ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    // Row 1: Header
    ["🎯 WHAT'S NEXT" , "", "", "", "", "", "", "", "", "", 
"", "", "", ""],
    // Rows 2-5: Guidance items (icon in col 1, action in col  
2, description in col 6)
    [guidance [0][0], guidance [0][1], "", "", "", guidance [0]
[2], "", "", "", "", "", "", "", ""],
    [guidance [1][0], guidance [1][1], "", "", "", guidance [1]
[2], "", "", "", "", "", "", "", ""],
    [guidance [2][0], guidance [2][1], "", "", "", guidance [2]
[2], "", "", "", "", "", "", "", ""],
    [guidance [3][0], guidance [3][1], "", "", "", guidance [3]
[2], "", "", "", "", "", "", "", ""],
    // Row 6: Tip
    ["💡 Pro tip: Run this analysis monthly to catch new wast
e patterns!" , "", "", "", "", "", "", "", "", "", "", "", "", 
Negative Keyword AI (v6 Architecture)

""]
  ];
  outSheet .getRange (startRow , 1, 7, 14).setValues (allValues );
  // BATCHED: Apply all merges
  outSheet .getRange (startRow , 1, 1, 14).merge();      // Sepa
rator
  outSheet .getRange (startRow + 1, 1, 1, 14).merge();  // Head
er
  // Guidance rows: merge cols 2-5 for action, cols 6-10 for  
description
  for (let i = 0; i < 4; i++) {
    outSheet .getRange (startRow + 2 + i, 2, 1, 4).merge();   
// Action text
    outSheet .getRange (startRow + 2 + i, 6, 1, 5).merge();   
// Description
  }
  outSheet .getRange (startRow + 6, 1, 1, 14).merge();  // Tip 
row
  // BATCHED: Apply backgrounds in one call
  const backgrounds = [
    Array(14).fill("#e8eaed" ),  // Separator - gray
    Array(14).fill("#34a853" ),  // Header - green
    Array(14).fill("#ffffff" ),  // Guidance rows - white
    Array(14).fill("#ffffff" ),
    Array(14).fill("#ffffff" ),
    Array(14).fill("#ffffff" ),
    Array(14).fill("#fff3cd" )   // Tip - yellow
  ];
  outSheet .getRange (startRow , 1, 7, 14).setBackgrounds (backgr
ounds);
  // Apply text formatting (grouped by style)
  outSheet .getRange (startRow + 1, 1).setFontSize (14).setFontW
eight("bold").setFontColor ("white").setHorizontalAlignment ("c
Negative Keyword AI (v6 Architecture)

enter");
  // Guidance action text - bold
  outSheet .getRange (startRow + 2, 2, 4, 1).setFontWeight ("bol
d");
  // Guidance description text - italic gray
  outSheet .getRange (startRow + 2, 6, 4, 1).setFontStyle ("ital
ic").setFontColor ("#5f6368" );
  // Tip - italic
  outSheet .getRange (startRow + 6, 1).setFontStyle ("italic" );
}
function  validateDataBeforeAnalysis_ (termsSheet , cfg) {
  const issues = [];
  // Check for terms
  const terms = readTerms_ (termsSheet );
  if (terms.length === 0) {
    issues.push("❌ No search terms found in Terms sheet" );
    return { valid: false, issues };
  }
  // Check for API key
  if (!cfg.api_key || cfg.api_key === "<<ADD YOUR KEY>>" ) {
    issues.push("❌ API key not configured in Config" );
  }
  // Validate target_url format (UrlFetchApp requires full UR
L with protocol)
  if (cfg.target_url && !cfg.target_url .match(/^https?:\/\/.
+/i)) {
    issues.push(`❌ Add https:// to target_url — change to "h
ttps://${cfg.target_url }"`);
  }
Negative Keyword AI (v6 Architecture)

  // Check for reasonable data
  const hasClicks = terms.some(t => t.clicks > 0);
  const hasCost = terms.some(t => t.cost > 0);
  if (!hasClicks ) {
    issues.push("⚠  No terms have clicks - data may be incompl
ete");
  }
  if (!hasCost) {
    issues.push("⚠  No terms have cost data - spend analysis l
imited");
  }
  // Check for brand terms (recommended)
  if (!cfg.brand_terms || cfg.brand_terms .length === 0) {
    issues.push("💡 Tip: Add brand_terms in Config for better  
protection" );
  }
  // Check for services (recommended)
  if (!cfg.services_offered || cfg.services_offered .length ==
= 0) {
    issues.push("💡 Tip: Add services_offered in Config for b
etter classification" );
  }
  // Show billing reminder once per session (uses cache, expi
res after 6 hours)
  const vendor = String(cfg.api_vendor || "openai" ).toLowerCa
se();
  const cache = CacheService .getDocumentCache ();
  const billingShown = cache ? cache.get("billing_reminder_sh
own") : null;
  if (!billingShown ) {
Negative Keyword AI (v6 Architecture)

    const billingUrl = vendor === "anthropic"
      ? "console.anthropic.com/settings/billing"
      : "platform.openai.com/settings/organization/billing" ;
    const subNote = vendor === "openai"
      ? "Note: ChatGPT Plus subscription does NOT include API  
credits!"
      : "";
    issues.push(`💳 Reminder: API calls require credits at 
${billingUrl }. ${subNote}`.trim());
    if (cache) cache.put("billing_reminder_shown" , "true", 21
600); // 6 hours
  }
  const hasBlockingIssues = issues.some(i => i.startsWith
("❌"));
  return {
    valid: !hasBlockingIssues ,
    issues,
    termCount : terms.length,
    hasClicks ,
    hasCost
  };
}
function  updateProgressCell_ (outSheet , message ) {
  // Uses cell A1 temporarily during analysis to show live pr
ogress
  // This gets overwritten when the header is initialized
  try {
    const ss = SpreadsheetApp .getActive ();
    ss.toast(message, "Progress" , 3);
  } catch(e) {
    Logger.log("Progress: "  + message );
  }
}
Negative Keyword AI (v6 Architecture)

/* ===== Utils ===== */
function  getOrCreate_ (ss,n){ return ss.getSheetByName (n) || s
s.insertSheet (n); }
function  upsertConfigValueForce_ (sh,key,value){
  const vals = sh.getDataRange ().getValues ();
  for(let i=0;i<vals.length;i++){
    if(String(vals[i][0]).trim().toLowerCase ()===key.toLowerC
ase()){ sh.getRange (i+1,2).setValue (value); return; }
  }
  sh.appendRow ([key,value]);
}
function  safeJson_ (txt){
  if(!txt || typeof txt !== 'string' ) throw new Error("Empty 
or invalid response" );
  let lastError = null;
  // Try direct parse first
  try{
    return JSON.parse(txt);
  } catch(e) {
    lastError = e;
    Logger.log("safeJson_ direct parse failed: "  + e.messag
e);
  }
  // Strip BOM and control characters
  let cleaned = txt.replace(/^\uFEFF/, '').trim();
  // Strip markdown code blocks if present
  if(cleaned.startsWith ("```json" )) {
    cleaned = cleaned .slice(7);
  } else if(cleaned.startsWith ("```")) {
    cleaned = cleaned .slice(3);
  }
Negative Keyword AI (v6 Architecture)

  if(cleaned.endsWith ("```")) {
    cleaned = cleaned .slice(0, -3);
  }
  cleaned = cleaned .trim();
  // Try parsing cleaned version
  try{
    return JSON.parse(cleaned);
  } catch(e) {
    lastError = e;
    Logger.log("safeJson_ cleaned parse failed: "  + e.messag
e);
  }
  // Last resort: find first { and last }
  const s = cleaned .indexOf("{"), e2 = cleaned .lastIndexOf
("}");
  if(s>=0 && e2>s){
    const cand = cleaned .slice(s, e2+1);
    try{
      return JSON.parse(cand);
    } catch(e3) {
      lastError = e3;
      Logger.log("safeJson_ extracted JSON parse failed: "  + 
e3.message);
    }
  }
  // Check for truncated response (missing closing braces)
  const openBraces = (cleaned.match(/\{/g) || []).length;
  const closeBraces = (cleaned.match(/\}/g) || []).length;
  const openBrackets = (cleaned.match(/\[/g) || []).length;
  const closeBrackets = (cleaned.match(/\]/g) || []).length;
  if(openBraces > closeBraces || openBrackets > closeBracket
s) {
Negative Keyword AI (v6 Architecture)

    Logger.log("safeJson_ detected truncated response: braces
=" + openBraces + "/" + closeBraces + ", brackets="  + openBra
ckets + "/" + closeBrackets );
    // Strategy: Find the last complete object in the array b
y finding last "},\n" or "}\n  ]"
    // and truncate there, then close properly
    let truncateIdx = -1;
    // Look for patterns that indicate end of a complete arra
y element
    // Pattern 1: "},\n    {" - between array elements
    const betweenElementsMatch = cleaned .match(/\},\s*\n\s*\
{[^}]*$/);
    if (betweenElementsMatch ) {
      truncateIdx = cleaned .lastIndexOf (betweenElementsMatch
[0]);
      Logger.log("safeJson_ found incomplete element at posit
ion " + truncateIdx );
    }
    // Pattern 2: Find last complete "}" that's followed by a  
comma or end of array
    if (truncateIdx < 0) {
      // Find all positions of "}," which indicate complete o
bjects
      let lastCompleteObj = -1;
      let searchPos = 0;
      while (true) {
        const pos = cleaned .indexOf("},", searchPos );
        if (pos < 0) break;
        lastCompleteObj = pos;
        searchPos = pos + 1;
      }
      if (lastCompleteObj > 0) {
        truncateIdx = lastCompleteObj + 1; // Include the }
Negative Keyword AI (v6 Architecture)

        Logger.log("safeJson_ last complete object ends at po
sition "  + truncateIdx );
      }
    }
    if (truncateIdx > 0) {
      // Truncate to last complete object, then close the str
ucture
      let fixed = cleaned .substring (0, truncateIdx + 1); // I
nclude the }
      // Remove trailing comma if present
      fixed = fixed.replace(/,\s*$/, '');
      // Close any open arrays and braces
      const fixedOpenBrackets = (fixed.match(/\[/g) || []).le
ngth;
      const fixedCloseBrackets = (fixed.match(/\]/g) || []).l
ength;
      const fixedOpenBraces = (fixed.match(/\{/g) || []).leng
th;
      const fixedCloseBraces = (fixed.match(/\}/g) || []).len
gth;
      for(let i = 0; i < fixedOpenBrackets - fixedCloseBracke
ts; i++) {
        fixed += "]";
      }
      for(let i = 0; i < fixedOpenBraces - fixedCloseBraces ; 
i++) {
        fixed += "}";
      }
      Logger.log("safeJson_ attempting truncated parse, fixed  
length="  + fixed.length);
      try {
Negative Keyword AI (v6 Architecture)

        const result = JSON.parse(fixed);
        const recCount = result.recommendations ? result.reco
mmendations .length : 0;
        Logger.log("safeJson_ RECOVERED "  + recCount + " reco
mmendations from truncated response" );
        return result;
      } catch(e4) {
        Logger.log("safeJson_ truncation fix failed: "  + e4.m
essage);
      }
    }
    // Fallback: simple brace closing (old method)
    let fixed = cleaned ;
    for(let i = 0; i < openBrackets - closeBrackets ; i++) {
      fixed += "]";
    }
    for(let i = 0; i < openBraces - closeBraces ; i++) {
      fixed += "}";
    }
    try {
      return JSON.parse(fixed);
    } catch(e5) {
      Logger.log("safeJson_ simple fix also failed: "  + e5.me
ssage);
    }
  }
  // Log diagnostic info
  Logger.log("safeJson_ FINAL FAILURE. Length: "  + txt.length 
+ ", First 300 chars: "  + txt.substring (0, 300));
  Logger.log("safeJson_ Last 100 chars: "  + txt.substring (tx
t.length - 100));
  throw new Error("Invalid JSON: "  + (lastError ? lastError .m
essage : "unknown error" ));
}
Negative Keyword AI (v6 Architecture)

function  stripHtml_ (html){
  return html.replace(/<script[\s\S]*?<\/script> /gi,"")
             .replace(/<style[\s\S]*?<\/style> /gi,"")
             .replace(/<\/?[^>]+> /g," ")
             .replace(/\s+/g," ")
             .trim();
}
function  toNum_(v){ const n = Number(String(v).replace(/,/
g,"")); return Number.isFinite (n)?n:null; }
function  toInt_(v){ const n = parseInt (String(v).replace(/,/
g,""),10); return Number.isFinite (n)?n:null; }
function  toMoney_ (v){ const s = String(v).replace(/[^0-9.\-] /
g,""); const n = parseFloat (s); return Number.isFinite (n)?n:n
ull; }
function  valStr_(v){ const s = String(v||"").trim(); return s 
|| ""; }
function  normalizeKW_ (s){ return String(s||"").toLowerCase ().
trim().replace(/\s+/g," "); }
/**
 * Smart config value parser - accepts multiple formats for u
ser convenience:
 * - JSON arrays: ["item1", "item2"]
 * - Comma-separated: item1, item2
 * - Single values: item1
 * - Booleans: true/false/yes/no/1/0
 */
function  parseMaybeJson_ (v){
  if(typeof v !== "string" ) return v;
  const trimmed = v.trim();
  if(!trimmed) return trimmed ;
  // Try JSON first (handles proper arrays and objects)
  try { return JSON.parse(trimmed); } catch(e) { /* not valid  
JSON, continue */  }
  // Check for boolean-like values
Negative Keyword AI (v6 Architecture)

  const lower = trimmed .toLowerCase ();
  if(lower === "true" || lower === "yes" || lower === "1") re
turn true;
  if(lower === "false" || lower === "no" || lower === "0") re
turn false;
  // Check if it looks like a comma-separated list (has comma
s but isn't a number)
  if(trimmed.includes (",") && !/^\d[\d,]*\.?\d*$ /.test(trimme
d)) {
    // Split by comma, trim each item, filter empty strings
    const items = trimmed .split(",").map(s => s.trim()).filte
r(s => s.length > 0);
    if(items.length > 1) return items;
    if(items.length === 1) return items[0]; // Single item, r
eturn as string
  }
  // Return as-is (plain string)
  return trimmed ;
}
/** Format match type for user-friendly display: EXACT → [exa
ct], PHRASE → [phrase], BROAD → broad */
function  formatMatchType_ (mt){
  const upper = String(mt||"").toUpperCase ();
  if(upper === "EXACT") return "[exact]" ;
  if(upper === "PHRASE" ) return "[phrase]" ;
  if(upper === "BROAD") return "broad";
  if(upper === "NONE" || !upper) return "";
  return mt; // Return as-is if unknown
}
/** Format level for user-friendly display: CAMPAIGN → Campai
gn-level, AD_GROUP → Ad Group-level */
function  formatLevel_ (level){
Negative Keyword AI (v6 Architecture)

  const upper = String(level||"").toUpperCase ();
  if(upper === "CAMPAIGN" ) return "Campaign-level" ;
  if(upper === "AD_GROUP" ) return "Ad Group-level" ;
  if(upper === "NONE" || !upper) return "";
  return level; // Return as-is if unknown
}
Negative Keyword AI (v6 Architecture)

