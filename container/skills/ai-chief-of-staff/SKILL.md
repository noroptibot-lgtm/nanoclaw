---
name: ai-chief-of-staff
description: Build a personal AI Chief of Staff (Executive Assistant) in 4 phases — Home, Life, Hands, Growth. Context files + onboarding interview + daily skills + compounding flywheel. Trigger on /chief-of-staff or when user asks to build a personal AI executive assistant.
---

# Your AI Chief of Staff

A personal executive assistant that knows your priorities, your people, and your preferences — and gets smarter every day.

## Phase 1 — HOME: Set Up the Foundation

Give the AI a place to live. One folder, five context files, one master instructions file.

### Folder Structure

```
executive-assistant/
├── context/
│   ├── me.md           ← Who you are
│   ├── work.md         ← What you do
│   ├── team.md         ← Who you work with
│   ├── priorities.md   ← What matters right now
│   └── goals.md        ← Where you're heading
├── skills/             ← Agent capabilities (Phase 3)
└── AGENT.md            ← Master instructions
```

### The Five Context Files

- **me.md** — personal background, communication style, preferences, pet peeves, decision-making patterns
- **work.md** — business context, products, revenue model, tech stack, daily tools
- **team.md** — team, collaborators, key contacts, who you report to / manage
- **priorities.md** — current top 3 priorities, blockers, what you'd do with 5 extra hours
- **goals.md** — 90-day, 12-month, north-star metric

### Action Checklist
- [ ] Create `executive-assistant/` folder
- [ ] Create `context/` subfolder
- [ ] Create all five .md files (empty for now)
- [ ] Create `skills/` folder
- [ ] Create `AGENT.md` with master instructions

## Phase 2 — LIFE: The Onboarding Interview

Don't fill out the context files by hand. Let the AI interview you. 15–20 minutes.

### Why an interview instead of manual?
When someone asks you questions, you surface details you'd never write down on your own. Preferences, quirks, context, nuance. The mess is what makes it personal.

### Sample Interview Prompt

```
You are an executive onboarding specialist. Your job is to
interview me and build 5 context files for my AI executive
assistant. The files are: me.md, work.md, team.md,
priorities.md, and goals.md.

Rules:
- Ask ONE question at a time
- Go deep before moving to the next topic
- Write each file as we finish that section
- Ask follow-up questions when my answers are vague
- The interview should take 15-20 minutes
- Be conversational, not robotic

Start with me.md — ask about who I am.
```

### Questions to Expect

**me.md** — communication style, pet peeves, decision-making
**work.md** — what your business actually does, revenue model, daily tools
**team.md** — who you work with regularly, report to, manage
**priorities.md** — top 3 this week, blockers, 5-extra-hours question
**goals.md** — 90 days, 12 months, north star metric

### Action Checklist
- [ ] Block 20 minutes on your calendar
- [ ] Run the interview prompt
- [ ] Answer naturally, don't overthink
- [ ] Review the five generated files
- [ ] Edit and add anything the interview missed

## Phase 3 — HANDS: Build the Skills

Three high-impact skills you'll use daily. Each one reads your context files so it stays aligned with your priorities and voice.

### Skill 1: Morning Coffee

Daily briefing that knows what you care about. Reads `priorities.md` and `goals.md`, outputs a stand-up.

```
Read context/priorities.md and context/goals.md.

Generate my Morning Coffee briefing:
1. Top 3 focus items for today
2. Upcoming deadlines this week
3. Blockers or decisions needed
4. One suggestion to move the needle

Keep it under 200 words. Be direct.
```

### Skill 2: Research Summaries with Sub-Agents

Main agent breaks a research task into sub-tasks and delegates to faster, cheaper sub-agents for scraping, summarizing, compiling. Main agent synthesizes everything.

**Main agent (powerful model — Claude Opus/Sonnet):** orchestrates, reads context, makes decisions
**Sub-agents (fast model — Haiku/mini):** scraping, data processing, drafting

Keeps cost low and speed high where it doesn't matter, intelligence where it does.

### Skill 3: Content Generation in Your Voice

Reads `me.md` for voice/style/values and `work.md` for business context. Drafts content that sounds like you.

```
Read context/me.md for my voice and style.
Read context/work.md for business context.

Draft a [type of content] about [topic].

Rules:
- Match my communication style exactly
- Reference my actual business/products
- Keep my values front and center
- Give me a first draft I can edit, not a final copy
```

### Action Checklist
- [ ] Build Morning Coffee, test with real priorities
- [ ] Pick main model + fast model for sub-agent strategy
- [ ] Build Research Summary skill, test on a real question
- [ ] Build Content Generation, compare output to your voice
- [ ] Save all three to `skills/`

## Phase 4 — GROWTH: The Flywheel

The assistant gets better the more you use it. Each interaction, correction, and context update makes it smarter. Not set-and-forget. A flywheel.

### The Compounding Loop

**Use it daily → refine context → smarter outputs → use it more**

### Context Depth Over Time

| Time | Depth | State |
|------|-------|-------|
| Week 1 | 20% | Basic context. Generic-but-decent outputs |
| Week 4 | 50% | Knows your voice, decision patterns, team dynamics. Outputs feel personal |
| Month 3 | 85% | Anticipates your needs. Flags things you'd miss. Real chief of staff |

### The Daily Habit

- **Every Friday (5 min):** update `priorities.md`
- **Every month (15 min):** review `me.md` and `goals.md`
- **After any wrong output:** note what it got wrong and update context

### Action Checklist
- [ ] Use Morning Coffee daily for one week straight
- [ ] After each interaction, note corrections and update context
- [ ] Recurring Friday reminder: "Update priorities.md"
- [ ] Recurring monthly reminder: "Review all context files"
- [ ] Add one new skill per week as needs emerge

## The Principle

Context files like a living document, not a one-time setup. The people who get the most from this treat it as a daily operating system. The ones who set it up and walk away get a mediocre chatbot.
