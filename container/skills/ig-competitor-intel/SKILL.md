---
name: Instagram Competitor Intelligence
description: Scraped content data, hook patterns, and engagement signals from 9 competitor Instagram accounts in the AI/Claude Code/OpenClaw niche
type: reference
---

# Instagram Competitor Intelligence

Scraped: 2026-03-18 | Method: Instagram mobile API (headless, no browser)

## How to re-scrape any profile
```bash
curl -s -A "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15" \
  "https://i.instagram.com/api/v1/users/web_profile_info/?username=USERNAME" \
  -H "x-ig-app-id: 936619743392459" | python3 -c "
import sys,json
d=json.load(sys.stdin)
user=d['data']['user']
print('Followers:', user['edge_followed_by']['count'])
for p in user['edge_owner_to_timeline_media']['edges']:
    n=p['node']
    cap=n.get('edge_media_to_caption',{}).get('edges',[{}])[0].get('node',{}).get('text','')
    print(n['edge_liked_by']['count'],'L |', n['edge_media_to_comment']['count'],'C |', cap[:120])
"
```

---

## Competitor Overview

| Account | Followers | Niche | Posts | Top signal |
|---------|-----------|-------|-------|------------|
| @mattganzak | 67k | OpenClaw + SaaS | 994 | "MVP for $.03" |
| @noevarner.ai | 60.7k | Claude Code + Meta Ads | 459 | "Comment PAID" |
| @buildwithcody | 57.8k | Startups + OpenClaw | 61 | 7-day challenge series |
| @jens.heitmann | 28.4k | Claude Code power user | 17 | 30.7k likes, only 17 posts |
| @marcinteodoru | 24.1k | VibeCoding + OpenClaw | ~100 | GitHub trending lists |
| @andreapalacio | 13.9k | AI for small biz | 645 | "Proposal in 27 seconds" |
| @casey.aicreates | 13.6k | AI news + vibe coding | 106 | Model comparisons |
| @baroobi.inc | 13.1k | Tech/Cybersecurity/AI | 140 | Drama/controversy hooks |
| @chriswesst | 10.7k | AI departments | 11 | "7 agents = 80% of my work" |

---

## @jens.heitmann (28.4k followers, only 17 posts — highest engagement ratio)
**Bio:** "My favorite generative AI model is my brain"

**Top posts by engagement:**
- [30,738L 367C] "You probably haven't fully unlocked the design power of your Claude Code. Use these 3 systems to up-level the design of your next project."
- [15,696L 302C] "You can make Claude Code your Social Media Manager that studies your channels, audits your posts, and improves your content automatically."
- [9,433L 166C] "Using Obsidian with Claude Code is a second brain cheat code."
- [9,057L 157C] "You might not need a marketing hire. You need the right skills installed."
- [5,199L 36C] "Claude Code has dropped three new critical features changing the game in SaaS."
- [3,672L 3,231C] "Editing has gotten easier — speak to edit videos using Remotion & Claude Code." (highest comments)
- [2,256L 75C] "There's a way to have Codex work for your Claude Code to give cleaner results."

**Formula:** "You [probably/might] [are missing X] — here are 3 [systems/ways/frameworks]"
**Key insight:** No hashtag spam. No comment gating. Pure value + "3 things" format = 30k likes with 17 posts total.

---

## @marcinteodoru (24.1k followers)
**Bio:** I Build & Teach VibeCoding AI | 466k TT | 38k YT | OpenClaw Masterclass

**Top posts:**
- [532L 20C] "Nvidia is going all in on AI agents like OpenClaw."
- [177L 97C] "These are the fastest growing AI projects on GitHub right now." (high comments = aggregation works)
- [172L 1C] "This guy built 47 micro SaaS tools in 90 days using Claude Code."
- [141L 12C] "Most people think AI agents are just chatbots. Not even close."

---

## 10 Winning Hook Patterns

### 1. Comment-Gate / DM Trigger
"Comment [KEYWORD] and I'll send you [resource]" — drives comment count algorithmically
Active keywords in the space: GROW, PROOF, PAID, SETUP, PROPOSAL, SPRINT, USAGE

### 2. Specific Numbers = Credibility
- "token cost by 97%" / "MVP for $.03" / "proposal in 27 seconds"
- "7 agents = 80% of my work" / "$4,000 of your time gone monthly"
- "47 micro SaaS in 90 days" / "50,000 people use this"

### 3. "3 Things" Framework Lists (highest ROI format)
@jens.heitmann owns this. 30k likes per post with 17 total posts.
Template: "You [probably/might] [are missing X] — here are 3 [systems/ways/frameworks]"

### 4. Tool-Name SEO Hooks
Claude Code and OpenClaw in every post = searchable hashtags + niche authority.
Own a tool identity the way @noevarner.ai owns "Claude Code Junkie."

### 5. Drama / Controversy Stops the Scroll
- "OpenClaw just got banned" / "Claude Code is ruining my life" / "F*ck balance."
Strong opinion + provocation = shares + comments

### 6. Series / Episodic Content
- "Day 2/7: Can OpenClaw pay for itself?" forces follows for next episode
- Serialized = algorithmic follow signal

### 7. Freedom + AI Personal Story
Blend burnout/travel/working-from-phone with AI as the escape vehicle.

### 8. Model Head-to-Head Comparisons
"GPT-5.4 vs Opus 4.6 for [specific task]" — timely, searchable, opinion-baiting, high saves

### 9. Cost / ROI Shock
Either how CHEAP AI is ("$.03", "for $0", "97% cheaper")
Or how EXPENSIVE not using it is ("$4,000 of your time gone monthly")

### 10. "You might not need a [expensive hire]"
Reframes the cost objection. @andreapalacio: "You might not need a marketing hire."
Works well for service/agency positioning.

---

## Top Formats to Model

1. **"3 systems/ways/frameworks"** — @jens.heitmann: 30k likes, 17 posts. Best ROI format in the dataset.
2. **GitHub trending aggregation** — high comments, saves, shares
3. **7-day challenge series** — forces follows, episodic retention
4. **Specific cost/time claim** — "in 27 seconds / $.03 / 97% cheaper"
5. **Model head-to-head for specific task** — searchable + opinion-driven
6. **"You might not need a [hire]"** — reframes cost objection
7. **Humor/relatable** — "Claude Code is ruining my life" — shareable without selling
8. **Personal story arc** — vulnerability + AI as resolution
