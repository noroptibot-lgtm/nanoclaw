---
name: content-dashboard
description: Build a full content management dashboard interactively — Instagram manager, analytics, content calendar, competitor tracker, and news consolidator. Asks questions to customize the build to your niche, platforms, and preferences.
user_invocable: true
---

# Content Dashboard Builder

You build a fully customized content management dashboard for the user. The dashboard uses Next.js, Tailwind CSS, and shadcn/ui with a dark theme. It includes up to six sections: Instagram Manager, Analytics, Content Calendar, Competitor Tracker, and News Consolidator.

Instead of running through a rigid script, you ask the user what they need and build it piece by piece — tailored to their niche, platforms, and workflow.

## Startup Flow

When invoked, gather context from the user before building anything.

**Round 1 — Core setup questions.** Use `AskUserQuestion` to ask:

1. **What's your niche?** (Options: "AI / Tech", "Fitness / Health", "Business / Finance", "Other") — This customizes the news consolidator and content suggestions throughout.

2. **Which platforms do you create content for?** (multiSelect: true, Options: "Instagram", "YouTube", "TikTok", "Twitter / X") — This determines which platform-specific features to build and which filters to include in the calendar.

3. **Which dashboard sections do you want?** (multiSelect: true, Options: "Instagram Manager", "Analytics Dashboard", "Content Calendar", "Competitor Tracker") — The News Consolidator is always included. This lets users skip sections they don't need.

4. **Do you have a preferred analytics tool?** (Options: "Metricool (Recommended)", "Mock data for now", "I'll connect my own API later") — Determines how the analytics page sources its data.

**Round 2 — Confirmation.** Summarize what you're about to build based on their answers. List the sections, the niche, the platforms, and any integrations. Then ask:

1. **Ready to build?** (Options: "Yes, build it all at once", "Build it step by step so I can review each section", "Let me adjust something first")

If they choose step-by-step, build one section at a time and use `AskUserQuestion` after each to ask if they want changes before moving on.

## Build Sequence

Build in this exact order. Each step should be a complete, working implementation — not a placeholder.

### 1. Project Scaffold

Set up the Next.js project with Tailwind CSS and shadcn/ui. Create:
- Dark theme applied globally
- Shared sidebar navigation with links to all selected sections
- Placeholder pages for each selected section
- A `CLAUDE.md` file documenting the tech stack, folder structure, component conventions, and decisions made during setup

The CLAUDE.md file is critical — it gives context to every subsequent build step and ensures consistency.

### 2. Instagram Manager (if selected)

Build a content management view with:
- Card-based layout showing posts organized by status: Scheduled, Drafts, Published, Backlog
- Ability to add new post ideas with: caption, post type (reel, carousel, story, single), status, and scheduled date
- Filtering by status
- Dark UI, clean cards

If the user selected platforms beyond Instagram, adapt the post types to be platform-aware (e.g., include "Short" for YouTube, "Tweet thread" for Twitter).

### 3. Analytics Dashboard (if selected)

Build an analytics page with:
- Bar charts and line graphs for content performance metrics
- Metrics: total impressions, engagement rate, follower growth, top performing posts
- Date picker for filtering by time range
- Data source based on the user's earlier choice (Metricool integration, mock data, or stubbed API)
- Dark theme

### 4. Content Calendar (if selected)

Build a monthly calendar view with:
- Colored chips for each content item (color-coded by platform)
- Support for multiple items per day
- Platform filters based on the user's selected platforms
- Shows both scheduled and previously posted content
- Dark UI

### 5. Competitor Tracker (if selected)

Build a competitor tracking page with:
- Ability to add competitor handles/channels
- Display: recent posts, engagement metrics, posting frequency, growth trends
- Multi-platform tracking across the user's selected platforms
- Sortable table layout
- Publicly available data only
- Dark theme

### 6. News Consolidator (always included)

Build a news feed that:
- Aggregates news from RSS feeds relevant to the user's niche (use the niche from their earlier answer)
- Shows: headline, source, publish date, short summary
- Filtering by topic (tools, research, business — adjust categories based on niche)
- Card-based layout, dark theme

## After Building

Once everything is built, give the user a quick rundown:
- How to run the project (`npm run dev`)
- Where each section lives in the file structure
- How to add more sections or customize existing ones
- Remind them the CLAUDE.md file is there so future Claude Code sessions will understand the project

Then ask if they want any adjustments using `AskUserQuestion`:

1. **Anything you want to change?** (Options: "Looks good, I'm done", "Tweak the UI / layout", "Add another section", "Connect a real API")

Keep iterating until they're satisfied.

## Style Notes

- Every component uses shadcn/ui where applicable
- Dark theme everywhere — no light mode toggle needed unless requested
- Clean, minimal UI. Cards with subtle borders, good spacing, readable typography
- Use Recharts or a similar lightweight charting library for analytics
- Mobile-responsive layouts
- All data starts as local state or mock data — no backend required to get running
