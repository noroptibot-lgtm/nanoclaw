---
name: ig-dashboard
description: Use when building or extending an Instagram analytics dashboard with the Instagram Graph API on this Mac
---

# Instagram Dashboard

## Overview

A local Node.js + HTML dashboard for Instagram analytics. Proxy server handles API calls, static HTML renders everything client-side. No npm required.

## File Structure

```
ig-dashboard/
  proxy.js              # Node.js server (port 3001)
  content-dashboard.html # Frontend dashboard
  .env                  # API credentials
```

## .env Variables

```
IG_ACCESS_TOKEN=
IG_USER_ID=
IG_APP_ID=
IG_APP_SECRET=
```

## Starting the Server

```bash
node ig-dashboard/proxy.js
# → http://localhost:3001/content-dashboard.html
```

To start and keep running in background:
```bash
node ig-dashboard/proxy.js &
```

## API Endpoints (proxy.js)

| Endpoint | Description |
|----------|-------------|
| `GET /api/ig/account` | Profile: id, username, biography, followers_count, media_count, profile_picture_url |
| `GET /api/ig/media` | Last 50 posts with insights per post |
| Static files | Serves HTML/CSS/JS from same directory |

### Media Insights by Type

- **VIDEO:** `reach, saved, views, shares, total_interactions, ig_reels_avg_watch_time, ig_reels_video_view_total_time`
- **IMAGE / CAROUSEL_ALBUM:** `impressions, reach, saved, shares, total_interactions`

## Dashboard Sections (content-dashboard.html)

1. **Overview** — avatar, @username, bio, followers/posts/reach rate
2. **Summary Stats** — 6 cards: avg likes, comments, reach, saves, eng rate, total reel views
3. **Reel Watch Time** — only shown if VIDEO posts have watch time data (ig_reels_avg_watch_time in ms ÷ 1000)
4. **Algorithm Signals** — saves rate + shares rate with notes
5. **Top / Bottom Performers** — top 3 and bottom 3 by engagement rate
6. **Engagement Over Time** — bar chart of last 20 posts (likes + comments)
7. **Best Time to Post** — horizontal bar charts by day of week and time bucket
8. **Hashtag Performance** — only shown if any hashtag used 2+ times, sorted by avg engagement
9. **All Posts Grid** — sort pills, thumbnail cards, gold border on top 3

## Key Formulas

```
Engagement Rate = (likes + comments + saves + shares) / reach × 100
  - VIDEO: use reach
  - IMAGE/CAROUSEL: use impressions (fallback to reach)

Reach Rate = avgReach / followers × 100
Saves Rate = totalSaves / totalReach × 100
Shares Rate = totalShares / totalReach × 100
```

## Design System

```css
--bg: #06080D  --bg2: #0C0F1A  --bg3: #111827  --bg4: #1A2235
--accent: #C8A84B  --green: #34D399  --blue: #60A5FA
--purple: #A78BFA  --pink: #F472B6
--text: #DDE1EA  --text2: #6B7A90  --text3: #2E3A4E
Fonts: Bricolage Grotesque (body) + JetBrains Mono (numbers)
```

Engagement tiers: ≥5% green · ≥2% gold · below grey

## Notes

- Data does NOT auto-refresh — user clicks "Refresh Data" in sidebar
- T7 / proxy uses only built-in Node.js modules (no npm)
- `open "http://localhost:3001/content-dashboard.html"` to launch from terminal
- Instagram Graph API requires a valid long-lived access token
