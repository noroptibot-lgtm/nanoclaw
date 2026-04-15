# Content Dashboard Builder — Claude Code Skill

An interactive Claude Code skill that builds a full content management dashboard customized to your niche, platforms, and workflow.

## What It Builds

- **Instagram Manager** — Manage scheduled posts, drafts, published content, and backlog with card-based UI
- **Analytics Dashboard** — Bar charts, line graphs, engagement metrics, follower growth with date filtering
- **Content Calendar** — Monthly view with colored chips per platform, multi-item days, platform filters
- **Competitor Tracker** — Add competitor handles, track engagement, posting frequency, and growth trends
- **News Consolidator** — RSS-powered news feed filtered by topic, customized to your niche

Tech stack: Next.js, Tailwind CSS, shadcn/ui. Dark theme. No backend required.

## Installation

### Option 1: Add to your project

Copy the `content-dashboard.md` file into your project's `.claude/skills/` directory:

```bash
mkdir -p .claude/skills
cp content-dashboard.md .claude/skills/
```

### Option 2: Add globally

Copy it to your global Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills
cp content-dashboard.md ~/.claude/skills/
```

## Usage

In any Claude Code chat, run:

```
/content-dashboard
```

The skill will ask you a few questions to customize the build — your niche, which platforms you use, which sections you want — then build the entire dashboard for you.

## Customization

The skill file is just a markdown prompt. Open `content-dashboard.md` and edit it to:

- Change the default sections
- Add new dashboard pages
- Swap out the tech stack
- Adjust the UI style
