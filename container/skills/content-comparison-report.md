---
name: content-comparison-report
description: Compare your short-form content against competitors — find gaps in hooks, topics, and structures. Shows what competitors do better and what to steal. Use after running /shortform-analysis-report and /competitor-analysis-report.
---

# Content Comparison Report

Compare your IG content vs competitor content. Find what they're doing that you're not, which hooks to steal, and where you're winning.

Supabase project: `YOUR_SUPABASE_PROJECT_ID`
Your content: `WHERE platform = 'instagram' AND account_id IS NOT NULL`
Competitor content: `WHERE platform = 'instagram' AND account_id IS NULL`

## When Invoked

Run ALL queries in parallel where possible.

### Section 1: Head-to-Head Stats

```sql
-- Your stats
SELECT 'You' as who, COUNT(*) as videos, ROUND(AVG(views)::numeric) as avg_views,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY views) as median_views
FROM content WHERE platform = 'instagram' AND account_id IS NOT NULL AND views > 0;

-- Competitor stats (aggregated)
SELECT 'Competitors' as who, COUNT(*) as videos, ROUND(AVG(views)::numeric) as avg_views,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY views) as median_views
FROM content WHERE platform = 'instagram' AND account_id IS NULL AND views > 0;
```

Output: Side-by-side table. Analysis bullets on where you stand.

### Section 2: Topic Gaps — What They Cover That You Don't

```sql
-- Competitor topics that you have zero or few posts about
WITH comp_topics AS (
  SELECT topic, COUNT(*) as comp_count, ROUND(AVG(views)::numeric) as comp_avg_views
  FROM content WHERE platform = 'instagram' AND account_id IS NULL AND topic IS NOT NULL
  GROUP BY topic HAVING COUNT(*) >= 2
),
your_topics AS (
  SELECT topic, COUNT(*) as your_count
  FROM content WHERE platform = 'instagram' AND account_id IS NOT NULL AND topic IS NOT NULL
  GROUP BY topic
)
SELECT ct.topic, ct.comp_count, ct.comp_avg_views, COALESCE(yt.your_count, 0) as your_count
FROM comp_topics ct
LEFT JOIN your_topics yt ON ct.topic = yt.topic
WHERE COALESCE(yt.your_count, 0) <= 1
ORDER BY ct.comp_avg_views DESC
LIMIT 10;
```

Output: Table showing topics competitors win at that you barely cover. Analysis bullets on which gaps are worth filling.

### Section 3: Hook Framework Gaps — Patterns They Use That You Don't

```sql
-- Competitor hook frameworks ranked by performance
WITH comp_hooks AS (
  SELECT hook_framework, COUNT(*) as comp_count, ROUND(AVG(views)::numeric) as comp_avg_views
  FROM content WHERE platform = 'instagram' AND account_id IS NULL AND hook_framework IS NOT NULL
  GROUP BY hook_framework HAVING COUNT(*) >= 2
),
your_hooks AS (
  SELECT hook_framework, COUNT(*) as your_count, ROUND(AVG(views)::numeric) as your_avg_views
  FROM content WHERE platform = 'instagram' AND account_id IS NOT NULL AND hook_framework IS NOT NULL
  GROUP BY hook_framework
)
SELECT ch.hook_framework, ch.comp_count, ch.comp_avg_views,
  COALESCE(yh.your_count, 0) as your_count, yh.your_avg_views
FROM comp_hooks ch
LEFT JOIN your_hooks yh ON ch.hook_framework = yh.hook_framework
ORDER BY ch.comp_avg_views DESC
LIMIT 15;
```

Output: Table showing which hook frameworks competitors use vs you. Flag frameworks where they get high views but you've never used them or underperform.

### Section 4: Structure Comparison

```sql
-- Content structure comparison
WITH comp AS (
  SELECT content_structure, COUNT(*) as count, ROUND(AVG(views)::numeric) as avg_views
  FROM content WHERE platform = 'instagram' AND account_id IS NULL AND content_structure IS NOT NULL
  GROUP BY content_structure
),
yours AS (
  SELECT content_structure, COUNT(*) as count, ROUND(AVG(views)::numeric) as avg_views
  FROM content WHERE platform = 'instagram' AND account_id IS NOT NULL AND content_structure IS NOT NULL
  GROUP BY content_structure
)
SELECT COALESCE(c.content_structure, y.content_structure) as structure,
  COALESCE(c.count, 0) as comp_count, c.avg_views as comp_avg_views,
  COALESCE(y.count, 0) as your_count, y.avg_views as your_avg_views
FROM comp c
FULL OUTER JOIN yours y ON c.content_structure = y.content_structure
ORDER BY COALESCE(c.avg_views, 0) DESC;
```

Output: Table comparing structure usage and performance. Analysis on what formats to try.

### Section 5: Hooks to Steal

The most actionable section. Find the top 10 competitor hooks that:
- Got high views
- Use a framework you haven't tried OR underperform on
- Cover a topic relevant to your niche

```sql
SELECT c.handle, c.spoken_hook, c.hook_framework, c.topic, c.views, c.url
FROM content c
WHERE c.platform = 'instagram' AND c.account_id IS NULL
  AND c.hook_framework IS NOT NULL
  AND c.views > (SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY views) FROM content WHERE platform = 'instagram' AND account_id IS NULL AND views > 0)
ORDER BY c.views DESC
LIMIT 10;
```

For each hook: show the full hook, the framework template, which competitor used it, views it got, and a 1-line suggestion on how to adapt it to your content.

### Section 6: Key Takeaways

Synthesize into grouped recommendations:

**Topics to Start Covering (3-5 bullets)**
- Topics competitors win at that you don't cover

**Hook Frameworks to Test (3-5 bullets)**
- Specific frameworks with the mad-lib template ready to fill in

**Structures to Try (2-3 bullets)**
- Content formats that work for competitors but you underuse

**What You're Already Winning (2-3 bullets)**
- Where you outperform competitors — double down

## Output Rules

1. Full hook text — never truncate
2. URLs on every entry
3. Handle on every competitor entry
4. 3-5 analysis bullets per section focused on actionable gaps
5. Median-based calculations using PERCENTILE_CONT(0.5)

## Save Location

Save the report to your project's content analysis folder with today's date:

```
[your-project]/content-analysis/reports/comparison-YYYY-MM-DD.md
```

After saving: "Comparison saved. Your biggest gaps and hooks to steal are in the Key Takeaways section."
