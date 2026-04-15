# Product Strategy (Product Strategist)

## Overview

The Product Strategy skill provides a comprehensive toolkit for strategic product leadership at the executive level. This skill enables systematic OKR cascade generation, market analysis, product vision development, team scaling strategies, and metrics definition, ensuring alignment between company strategy and product execution while building high-performing product organizations.

## Who Should Use This Skill

- **Head of Product** setting strategic direction and organizational design
- **VP/CPO** aligning product strategy with business objectives
- **Product Leaders** scaling product teams and processes
- **Strategic Product Managers** working on company-level initiatives
- **Product Operations** establishing frameworks and systems
- **Executive Teams** aligning cross-functional product strategy

## Purpose and Use Cases

Use this skill when you need to:
- Cascade company OKRs to product and team levels
- Define product vision and multi-year strategy
- Conduct market and competitive analysis
- Design product team structure and scaling plans
- Establish product metrics and KPI frameworks
- Align product roadmap with business objectives
- Build product operating models
- Create strategic product narratives
- Design product portfolio strategy
- Set organizational goals with measurable outcomes

**Keywords that trigger this skill:** OKRs, product strategy, strategic planning, goal alignment, competitive analysis, product vision, team scaling, KPIs, product portfolio, strategic objectives

## What's Included

### OKR Cascade Generator

**Automatic Goal Alignment:**
- Cascades company-level OKRs to product and team levels
- Maintains strategic alignment across organization
- Calculates contribution percentages to parent OKRs
- Generates alignment scores for transparency
- Creates measurable key results at each level
- Tracks dependencies between objectives

**Strategy Types:**
- **Growth:** User acquisition, market expansion, revenue growth
- **Retention:** Engagement, churn reduction, customer success
- **Revenue:** Monetization, pricing, expansion revenue
- **Innovation:** New products, R&D, market creation
- **Operational:** Efficiency, quality, technical excellence

**OKR Structure:**
```
Company OKR (Strategic)
├── Product OKR (Tactical)
│   ├── Team OKR (Execution)
│   └── Team OKR (Execution)
└── Product OKR (Tactical)
    ├── Team OKR (Execution)
    └── Team OKR (Execution)
```

**Alignment Features:**
- Parent-child objective linking
- Contribution weighting (% impact on parent)
- Alignment score calculation (0-100%)
- Cross-functional dependency mapping
- Quarterly and annual planning support

### Market Analysis Framework

**Competitive Analysis:**
- Competitor positioning and strategy assessment
- Feature comparison matrices
- Pricing and packaging analysis
- Market share estimation
- Strengths/weaknesses evaluation
- Competitive differentiation opportunities

**Market Sizing:**
- TAM (Total Addressable Market) calculation
- SAM (Serviceable Addressable Market) definition
- SOM (Serviceable Obtainable Market) projection
- Market growth rate analysis
- Market segment identification

**Trends and Opportunities:**
- Technology trend analysis
- Customer behavior shifts
- Regulatory landscape changes
- Emerging market opportunities
- Disruption risk assessment

### Vision and Strategy Frameworks

**Product Vision Development:**
- Vision statement creation
- North Star metric definition
- Multi-year strategy roadmap
- Strategic pillars identification
- Differentiation strategy

**Strategy Templates:**
- Product-Market Fit assessment
- Blue Ocean strategy canvas
- Playing to Win framework
- Jobs-to-be-Done strategy
- Platform vs. Product strategy

**Strategic Narratives:**
- Compelling story structure
- Internal alignment presentations
- Board-level strategy decks
- Customer-facing vision
- Investment case narratives

### Team Scaling and Org Design

**Team Structure Models:**
- Feature teams vs. platform teams
- Squad/tribe/chapter models
- Product line organization
- Matrix team structures
- Centralized vs. decentralized models

**Scaling Frameworks:**
- Team size optimization (2-pizza rule)
- Span of control guidelines
- Hiring roadmap planning
- Skill matrix and gap analysis
- Onboarding and training programs

**Operating Models:**
- Product development lifecycle
- Decision-making frameworks (RACI, DACI)
- Ritual and ceremony design
- Communication protocols
- Escalation processes

### Metrics and KPI System

**North Star Metrics:**
- Leading indicator identification
- Value metric selection
- Activation metric definition
- Engagement metric frameworks
- Retention cohort analysis

**Product Health Metrics:**
- Adoption and activation rates
- Feature usage and depth
- User satisfaction (NPS, CSAT)
- Quality metrics (bugs, performance)
- Velocity and throughput

**Business Metrics:**
- Revenue and bookings
- Customer acquisition cost (CAC)
- Lifetime value (LTV)
- Churn and retention rates
- Unit economics

## How It Works

### OKR Cascade Generation

**Step 1: Define Company Strategy**
Choose strategic focus area:
- Growth (expand market reach)
- Retention (keep customers engaged)
- Revenue (improve monetization)
- Innovation (create new value)
- Operational (improve efficiency)

**Step 2: Generate OKR Cascade**
```bash
python scripts/okr_cascade_generator.py growth
```

**Step 3: Output Structure**

The script generates:
```
COMPANY OBJECTIVE: Accelerate Market Leadership
├── Key Result 1: Achieve 40% market share
├── Key Result 2: Reach $100M ARR
└── Key Result 3: Enter 3 new verticals

  PRODUCT OBJECTIVE: Drive User Growth
  ├── Key Result 1: Acquire 500K new users
  ├── Key Result 2: Improve activation to 60%
  └── Key Result 3: Launch in 3 new markets
  Contribution: 70% to Company KR1
  Alignment Score: 95%

    TEAM OBJECTIVE: Optimize Onboarding
    ├── Key Result 1: Reduce time-to-value to 5 min
    ├── Key Result 2: Increase signup conversion to 45%
    └── Key Result 3: Achieve 80% feature adoption
    Contribution: 50% to Product KR2
    Alignment Score: 88%
```

**Alignment Calculation:**
- Direct alignment: Child explicitly supports parent
- Contribution weight: Percentage impact (0-100%)
- Overall alignment score: Weighted average across all OKRs
- Dependency tracking: Cross-team coordination needs

### Strategy Development Process

**Step 1: Market Assessment**
1. Analyze current market position
2. Identify competitive threats and opportunities
3. Evaluate customer trends and needs
4. Assess internal capabilities and gaps
5. Define strategic constraints and enablers

**Step 2: Vision Definition**
1. Articulate 3-5 year product vision
2. Define North Star metric
3. Identify strategic differentiators
4. Create compelling narrative
5. Align with company mission and values

**Step 3: Strategic Pillars**
Define 3-5 strategic pillars:
- What will we focus on?
- What will we NOT do?
- How will we differentiate?
- What capabilities do we need?
- What are our strategic bets?

**Step 4: Roadmap Translation**
1. Map strategy to quarterly themes
2. Define yearly milestones
3. Allocate resources and capacity
4. Set success metrics
5. Identify dependencies and risks

**Step 5: Alignment and Communication**
1. Present to executive team
2. Cascade to product organization
3. Align with cross-functional partners
4. Create public-facing narrative
5. Establish review cadence

### Team Scaling Approach

**Assess Current State:**
- Team size and structure
- Skill distribution
- Capacity vs. demand
- Quality and velocity metrics
- Employee satisfaction

**Define Future State:**
- Product complexity growth
- Market expansion needs
- Technology evolution
- Organizational maturity
- Strategic initiatives load

**Design Scaling Plan:**
```
Quarter 1:
- Hire 2 Senior PMs (enterprise features)
- Establish platform team (3 engineers)
- Promote 1 PM to Group PM

Quarter 2:
- Add Growth PM (acquisition focus)
- Expand platform team (+2 engineers)
- Hire Product Ops lead

Quarter 3:
- Regional PM for EMEA expansion
- Data Science PM for ML initiatives
- Split into 2 product groups
```

**Implementation:**
- Recruiting timeline and pipeline
- Onboarding program design
- Knowledge transfer planning
- Communication strategy
- Success metrics and checkpoints

## Technical Details

### OKR Best Practices

**Objective Quality:**
- Aspirational and inspiring
- Qualitative and directional
- Time-bound (quarterly or annual)
- Limited in number (3-5 per level)
- Aligned with strategy

**Key Result Quality:**
- Measurable and specific
- Outcome-based (not activity-based)
- Aggressive but achievable (60-70% target)
- Limited to 3-4 per objective
- Include baseline and target

**Good vs. Bad Examples:**

**Good Objective:**
"Become the preferred platform for small business accounting"

**Bad Objective:**
"Improve the product" (too vague)

**Good Key Result:**
"Increase Net Promoter Score from 45 to 65"

**Bad Key Result:**
"Ship 10 new features" (activity, not outcome)

### Alignment Scoring Algorithm

**Alignment Score Components:**
1. **Direct Alignment (40%):** Child directly supports parent
2. **Contribution Weight (30%):** Estimated % impact
3. **Strategic Fit (20%):** Aligns with strategic themes
4. **Dependency Clarity (10%):** Clear cross-team coordination

**Score Interpretation:**
- 90-100%: Excellent alignment, clear contribution path
- 75-89%: Good alignment, minor gaps in contribution
- 60-74%: Moderate alignment, consider refinement
- <60%: Poor alignment, requires strategic review

### Strategy Frameworks Reference

**Playing to Win:**
1. What is our winning aspiration?
2. Where will we play?
3. How will we win?
4. What capabilities must we have?
5. What management systems are required?

**SWOT Analysis:**
- Strengths: Internal advantages
- Weaknesses: Internal limitations
- Opportunities: External possibilities
- Threats: External challenges

**Porter's Five Forces:**
- Competitive rivalry
- Supplier power
- Buyer power
- Threat of substitution
- Threat of new entry

## Use Cases and Examples

### Scaling from Series A to Series B

**Scenario:** SaaS company growing from $5M to $20M ARR

**Current State:**
- 1 Head of Product
- 3 Product Managers
- 5 small engineering teams
- Founder-driven product decisions

**Future State:**
- 1 VP Product
- 2 Group Product Managers
- 8 Product Managers
- 12 engineering teams
- Data-driven product decisions

**Scaling Plan:**
```
Phase 1 (Q1-Q2):
- Hire VP Product (replace Head)
- Add 2 Senior PMs for enterprise
- Establish product ops function
- Implement OKR framework

Phase 2 (Q3-Q4):
- Promote 2 GPMs from Senior PMs
- Hire 3 additional PMs
- Split into Platform + Features
- Implement data infrastructure

Phase 3 (Year 2):
- Expand to 8 total PMs
- Add Growth and Analytics teams
- Regional expansion (EMEA PM)
- Mature product operations
```

**Key Transitions:**
- Founder to VP delegation
- Feature teams to platform + features
- Reactive to strategic planning
- Intuition to data-driven decisions

### OKR Cascade for Product-Led Growth

**Company OKR:**
```
Objective: Accelerate Product-Led Growth Motion
KR1: Achieve $50M in self-serve revenue (from $20M)
KR2: Reduce CAC by 40%
KR3: Increase viral coefficient from 0.3 to 0.8
```

**Product OKR (Acquisition):**
```
Objective: Drive Efficient Self-Serve Acquisition
KR1: Increase signup rate from 15% to 25%
KR2: Reduce time-to-value from 30min to 5min
KR3: Launch referral program with 30% participation
Contribution: 60% to Company KR1, 80% to KR2
Alignment: 92%
```

**Team OKR (Onboarding Squad):**
```
Objective: Optimize New User Activation
KR1: Improve Day-1 activation from 40% to 65%
KR2: Reduce drop-off in signup flow by 50%
KR3: Achieve 4.5/5 onboarding satisfaction score
Contribution: 70% to Product KR2
Alignment: 88%
```

**Team OKR (Growth Squad):**
```
Objective: Build Viral Growth Loops
KR1: Launch invite feature with 40% invite rate
KR2: Achieve 60% invite acceptance rate
KR3: Implement 3 viral sharing mechanisms
Contribution: 90% to Product KR3, 40% to Company KR3
Alignment: 95%
```

### Market Positioning Strategy

**Scenario:** B2B collaboration tool in crowded market

**Competitive Analysis:**
- Slack: Market leader, enterprise focus, high price
- Teams: Microsoft integration, enterprise only
- Discord: Gaming origins, free-first model
- Startup: Small budget, need differentiation

**Strategic Positioning:**
"The only collaboration platform built specifically for distributed creative teams, combining async-first communication with integrated creative review workflows."

**Strategic Pillars:**
1. **Async-First:** Time zone friendly, thoughtful communication
2. **Creative-Native:** Built-in review, feedback, and version control
3. **Small Team Focus:** Simple, affordable, quick setup
4. **Integration Hub:** Connect all creative tools

**Differentiation:**
- Don't compete on video (Zoom owns it)
- Don't compete on enterprise (Slack/Teams own it)
- Do compete on creative workflow integration
- Do compete on async-first philosophy

**Go-to-Market:**
- Target: Design agencies, creative studios, distributed creative teams
- Channel: Designer communities, creative tool partnerships
- Pricing: Free for small teams, per-project pricing
- Message: "Finally, a collaboration tool that works how creatives work"

### Metrics Framework for SaaS

**North Star Metric:**
"Weekly Active Teams Completing Creative Projects"
- Combines activation, engagement, and value delivery
- Leading indicator of retention and revenue
- Actionable by product and growth teams

**Supporting Metrics:**

**Acquisition:**
- Signup rate
- Organic vs. paid mix
- Cost per acquisition
- Source attribution

**Activation:**
- Time to first project
- Day 1 activation rate
- Aha moment completion
- Invitation rate

**Engagement:**
- DAU/MAU ratio
- Projects per team per week
- Features used per session
- Collaboration breadth

**Retention:**
- Week 1, 4, 12 retention cohorts
- Churn rate by segment
- Resurrection rate
- Net revenue retention

**Revenue:**
- MRR/ARR growth
- Expansion revenue
- CAC payback period
- LTV:CAC ratio

## Best Practices

### OKR Setting

**Do:**
- Start with company strategy, cascade down
- Make objectives inspirational
- Keep key results outcome-focused
- Limit to 3-5 OKRs per level
- Score quarterly and adjust
- Celebrate achieving 60-70% (stretch goals)

**Don't:**
- Set OKRs bottom-up without strategy
- Make objectives vague or unmeasurable
- Track activities instead of outcomes
- Create too many OKRs (spreads focus)
- Use OKRs for performance reviews directly
- Expect 100% achievement (not stretch goals)

### Strategy Development

**Effective Strategies:**
- Grounded in market reality
- Based on unique strengths
- Clear trade-offs (what NOT to do)
- Measurable success criteria
- Time-bounded (3-5 years)
- Compelling and inspiring

**Avoid:**
- Generic strategies (could be any company)
- Trying to serve everyone
- Copying competitor strategies
- No clear differentiation
- Strategy by PowerPoint (no execution)
- Set-and-forget planning

### Team Scaling

**Healthy Scaling:**
- Hire ahead of need (2-3 months lead time)
- Promote from within when possible
- Maintain product manager to team ratio (1:2-3 teams)
- Invest in onboarding and training
- Build diverse skill sets
- Create clear career paths

**Avoid:**
- Panic hiring without planning
- External hires for all senior roles
- Under-resourcing product management
- Assuming people will figure it out
- Homogeneous team composition
- Unclear growth opportunities

### Metrics and Measurement

**Good Metrics:**
- Aligned with business value
- Actionable by the team
- Simple to understand
- Leading indicators
- Comparable across time
- Resistant to gaming

**Metric Pitfalls:**
- Vanity metrics (look good, mean nothing)
- Lagging indicators only (too late to act)
- Too many metrics (analysis paralysis)
- Metrics without context (no baseline/target)
- Optimizing local vs. global (suboptimization)
- Gaming the metrics (Goodhart's Law)

## Integration Points

This skill integrates with:
- **OKR Tools:** Lattice, 15Five, Weekdone, Ally.io
- **Strategy Tools:** Cascade Strategy, Aha!, ProductPlan
- **Analytics:** Looker, Tableau, Mode, Amplitude
- **Roadmapping:** ProductBoard, Aha!, Roadmunk
- **Team Management:** Lever, Greenhouse (recruiting), Culture Amp (engagement)
- **Communication:** Notion, Confluence, Google Slides (strategy docs)

## Common Challenges and Solutions

### Challenge: Strategy-Execution Gap
**Solution:** Translate strategy into quarterly themes, cascade OKRs, review monthly, adjust roadmap, communicate relentlessly

### Challenge: OKR Alignment Confusion
**Solution:** Use cascade generator, visualize dependencies, regular alignment reviews, clear contribution percentages, simplify structure

### Challenge: Premature Scaling
**Solution:** Hire based on actual need, validate product-market fit first, build culture before scaling, invest in processes early

### Challenge: Too Many Metrics
**Solution:** Define North Star, limit to 3-5 key metrics per area, automate dashboards, focus reviews on insights not data dumps

### Challenge: Strategy Fatigue
**Solution:** Keep strategy visible, tell consistent story, celebrate wins aligned to strategy, refresh annually, make it real in decisions
