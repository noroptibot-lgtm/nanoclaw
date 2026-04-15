---
name: figjam
description: Create visual diagrams, flowcharts, process maps, and system architecture in FigJam. Use when asked to "map this out", "visualize this", "diagram this", "show me the flow", "put this in FigJam", "create a chart", or to visualize any process, system, or business logic. Also use when mapping client processes, file systems, offer structures, funnels, or workflows.
---

# FigJam Diagram Builder

Create gorgeous, designer-grade diagrams in FigJam. Every diagram should look like a professional designer made it — bold saturated colors, clear hierarchy, generous whitespace, zero clutter.

---

## Core Design Principles (READ THESE FIRST)

1. **Identify the diagram TYPE first.** Each type has its own design system — colors, shapes, spacing, connectors. NEVER apply workflow styling to a mind map, or funnel styling to a tree. See the type table in Step 1 and the Design Templates section below.
2. **Color encodes category, not decoration.** Each diagram type has its own color strategy:
   - **Workflow/Pipeline:** White pipeline + colored endpoints (2-3 colors)
   - **Mind Map:** Color per BRANCH (3-6 saturated colors, all descendants inherit)
   - **Funnel:** Color per STAGE (4-5 bold colors, narrowing)
   - **Tree/Hierarchy:** Color per LEVEL (3-5 pastel colors)
   - **Grid/Journey:** Color per ROW TYPE (4-6 colors)
3. **Consistent node sizing within each tier/level.** All nodes of the same type must be the SAME size. No random variation. Only hero/title nodes and legend tags should differ.
4. **Generous whitespace.** Pro diagrams use 200-400px gaps between major elements. Trees need 310px between levels. Mind maps need 144px between branches. Never cram.
5. **Shape encodes meaning.** Use different shapes for different node TYPES or LEVELS. Same shape = same category throughout.
6. **Connectors never cross through nodes.** Route around. Use BOTTOM magnets for loop-back connectors. Stagger vertical spacing so diagonal connectors have clear room.
7. **If mapping an n8n workflow, pull real data.** Use `mcp__n8n__n8n_get_workflow` with `mode='structure'` to get exact node names, types, positions, and connections. NEVER guess at the workflow structure.

### Workflow/Pipeline-Specific Principles (apply ONLY to workflow/pipeline diagrams)
- **White pipeline + colored endpoints.** Middle/pipeline nodes are WHITE with dark outline. Only triggers and outputs get bold color fills. Max 2-3 colored categories.
- **Emoji prefixes for node identity.** ⏰ triggers, 🌐 HTTP/API, { } Code nodes, 🔄 loops, 🗄️ database writes.
- **ONE section wraps everything.** All nodes, legend, and stickies in one section.
- **Horizontal legend at top.** `LEGEND | Trigger | Pipeline | Output` — all inline.
- **Stickies in a designated zone.** Bottom of the section, horizontal row. Never scattered.

---

## Input

The user will describe what they want visualized. Could be:
- **Process map** — "map out the content pipeline"
- **Client workflow** — "diagram how the client onboarding works"
- **System architecture** — "map out my n8n workflows"
- **Funnel** — "map the DM funnel end to end"
- **Mind map** — "brainstorm ideas around X"
- **Comparison** — "current vs automated workflow"
- **Hierarchy/tree** — "break down the offer tiers"

## Step 1: Identify Type + Ask Where

Before building anything, determine the diagram type, then ask where to put it.

### 1a. Identify the diagram type — ALWAYS ASK

**You MUST present the type options and let the user choose.** Recommend one based on context, but show all options. Never assume.

Present it like this:
> "For [what you described], I'd recommend a **[recommended type]** because [reason]. But here are all the options — which one do you want?"

Then show the table:

| Type | When to use | What it looks like |
|---|---|---|
| **Workflow / Pipeline** | n8n flows, data pipelines, process sequences | White nodes with colored endpoints, left-to-right arrows |
| **Mind Map / System Map** | Brainstorming, concept maps, skills maps | Central hub radiating outward, color per branch |
| **Funnel** | Sales funnels, conversion flows, staged processes | Narrowing colored tiers stacking downward |
| **Tree / Hierarchy** | Business structures, org charts, offer tiers, breakdowns | Big pastel nodes, different shape per level, top-down |
| **Grid / Journey Map** | Customer journeys, matrices, comparison tables | Rows and columns, color-coded by row type |
| **Architecture** | System architecture, multi-tier tech stacks | Stacked tier sections, top-down layers |
| **Comparison** | Before/after, current vs future | Two side-by-side or stacked sections |

### 1b. Ask where

1. **Which FigJam board?** Options:
   - Add to an existing board (ask for name/URL)
   - Create a new board (ask for a name)
2. **New page or existing page?** If adding to an existing board, should this be a new page?
3. **Quick overview or detailed breakdown?**

If the user already specified where (e.g., gave a URL), skip the questions and proceed.

## Step 2: Plan the Diagram

Before writing any FigJam code, plan:

1. **Pick the diagram type** (flow, tree, funnel, mind map, grid, comparison)
2. **Decide on sections** — see Section Rules below. Most flows = NO sections or ONE section.
3. **List all nodes** with their LEVEL/CATEGORY (this determines color + size)
4. **List all connections**
5. **Pick a color theme** (see Color Themes below) — ONE theme per diagram
6. **Assign each category to one theme color** (e.g., triggers = color1, processes = color2, outputs = color3)
7. **Choose layout strategy** (see Layout Templates below)

Write out the plan as a quick list before generating code.

## Step 3: Build in FigJam

### Authentication

- **Plan key:** `team::YOUR_PLAN_KEY` (your Figma team)
- **Known boards:** Add your board keys here after creating them
  - Example: `YOUR_BOARD_KEY`

If creating a new board:
```
mcp__claude_ai_Figma__create_new_file
  fileName: "<name>"
  planKey: "team::YOUR_PLAN_KEY"
  editorType: "figjam"
```

### FigJam API Rules (CRITICAL)

**DO use:**
- `figma.createShapeWithText()` — primary building block
- `figma.createSticky()` — for annotations in designated zones only
- `figma.createConnector()` — for arrows between nodes
- `figma.createSection()` — for grouping with colored backgrounds

**DO NOT use (they error in FigJam):**
- `figma.createFrame()` — DOES NOT WORK
- `figma.createText()` — DOES NOT WORK
- `connectorEndStrokeCap` — property does not exist, connectors auto-show arrows

**Font loading (REQUIRED before setting any text):**
```javascript
await figma.loadFontAsync({family: "Inter", style: "Medium"});
await figma.loadFontAsync({family: "Inter", style: "Bold"});
```

### Color Themes (Bold + Maximally Distinct)

Pick ONE theme per diagram. Each theme has 4 colors that are VISUALLY DISTINCT from each other at normal zoom — no two colors should look similar.

```javascript
const themes = {

  // BOLD — Maximum contrast. Use this as default. Bright, saturated, dopamine-inducing.
  bold: {
    c1: {r:0.30, g:0.36, b:0.90},  // Electric indigo — inputs, triggers
    c2: {r:0.20, g:0.76, b:0.45},  // Bright green — processes, automations
    c3: {r:0.98, g:0.60, b:0.05},  // Vivid orange — data, APIs, transforms
    c4: {r:0.92, g:0.20, b:0.45},  // Hot pink/red — outputs, destinations
    bg: {r:0.96, g:0.96, b:0.98},  // Near-white section bg
  },

  // STARTER — Works for everything. Deep but readable.
  starter: {
    c1: {r:0.30, g:0.36, b:0.83},  // Deep indigo — triggers, inputs
    c2: {r:0.18, g:0.72, b:0.53},  // Emerald green — processes, automations
    c3: {r:0.95, g:0.62, b:0.15},  // Warm amber — data, APIs, transformations
    c4: {r:0.76, g:0.24, b:0.45},  // Berry — outputs, destinations
    bg: {r:0.95, g:0.96, b:0.98},
  },

  // SUNSET — Warm, energetic. Good for funnels + marketing.
  sunset: {
    c1: {r:0.95, g:0.30, b:0.25},  // Coral red
    c2: {r:0.98, g:0.60, b:0.15},  // Orange
    c3: {r:0.93, g:0.82, b:0.10},  // Golden yellow
    c4: {r:0.55, g:0.20, b:0.80},  // Purple — visually distinct from the warm trio
    bg: {r:1.00, g:0.97, b:0.95},
  },

  // FOREST — Earthy, calm. Good for hierarchies + trees.
  forest: {
    c1: {r:0.20, g:0.65, b:0.45},  // Forest green
    c2: {r:0.20, g:0.40, b:0.80},  // Royal blue — distinct from green
    c3: {r:0.85, g:0.65, b:0.10},  // Gold
    c4: {r:0.75, g:0.25, b:0.55},  // Magenta/berry — distinct from all
    bg: {r:0.95, g:0.98, b:0.95},
  },

  // NEON — Bold, modern. Good for tech diagrams + dark/edgy brands.
  neon: {
    c1: {r:0.45, g:0.20, b:0.90},  // Electric purple
    c2: {r:0.00, g:0.85, b:0.65},  // Neon green
    c3: {r:0.98, g:0.35, b:0.45},  // Hot coral
    c4: {r:0.95, g:0.80, b:0.00},  // Bright yellow — distinct from the cool trio
    bg: {r:0.96, g:0.95, b:1.00},
  },

};

// Sticky colors — use FigJam built-in sticky colors (these are the ONLY ones that work)
// STICKY_YELLOW, STICKY_GREEN, STICKY_BLUE, STICKY_VIOLET, STICKY_RED, STICKY_ORANGE
// Or use CUSTOM and set fills manually

// Text on colored shapes — ALWAYS white
const white = {r:1, g:1, b:1};
// Text on light backgrounds — dark
const dark = {r:0.15, g:0.15, b:0.20};
```

### Node Size Scale

**ALL standard nodes must be the SAME size. No random variation.**

```javascript
const sizes = {
  // Hero / title bar — section titles, flow labels
  hero:     {w: 600, h: 65},
  // Standard node — ALL pipeline/process/trigger/output nodes
  standard: {w: 300, h: 90},   // 90px tall = "thicker" for readability
  // Annotation tag / legend swatch
  tag:      {w: 160, h: 35},
};
```

### Font Sizes

```javascript
const fonts = {
  hero:     {size: 18, style: "Bold"},    // Hero nodes
  standard: {size: 15, style: "Medium"},  // Standard nodes
  small:    {size: 14, style: "Medium"},  // Small nodes
  tag:      {size: 13, style: "Medium"},  // Tags, legend swatches
};
// NEVER use font size below 14px on nodes. 13px is absolute minimum for tags only.
```

### Spacing Constants

```javascript
const sp = {
  grid: 40,            // Everything snaps to 40px
  gapH: 40,            // Horizontal gap between nodes (edge-to-edge, since nodes are wider now)
  gapV: 120,           // Vertical gap between rows
  sectionPad: 60,      // Padding inside sections
  sectionGap: 120,     // Gap between sections
  stickyZoneGap: 200,  // Gap between main flow bottom and sticky annotation zone
};

// Snap helper — ALWAYS use this for positioning
function snap(v) { return Math.round(v / sp.grid) * sp.grid; }
```

### Section Rules — EVERY DIAGRAM GETS A SECTION

**EVERY diagram MUST be wrapped in a section.** The section name IS the diagram title — it serves as the headline for organizational purposes on the board.

| Diagram type | Section usage |
|---|---|
| Simple linear flow / pipeline | ONE section wrapping everything, named after the flow |
| Architecture with distinct tiers | ONE section per tier, each named |
| Comparison (before/after) | TWO sections: "Current State" + "Future State" |
| Funnel | ONE section per funnel stage, named after the stage |
| Mind map | ONE section wrapping the entire map, named after the topic |

**The section name = the diagram headline.** Make it descriptive. This is what people see when they zoom out on the board.

**NEVER leave nodes floating on the canvas without a section.** Everything belongs inside a named section.

**NEVER split a single linear flow into multiple sections.** A content pipeline that goes Capture > Edit > Post is ONE flow, not three sections.

### Section Coordinate Rules (CRITICAL BUG TO AVOID)

When you call `section.appendChild(node)`, **node coordinates become LOCAL to the section**. If you position nodes at absolute canvas coords (e.g., x=3000, y=500) and then append them, they'll render at section.x + 3000.

**Correct pattern — always convert absolute to local after appending:**

```javascript
function makeSection(name, nodes, bgColor, padding) {
  padding = padding || sp.sectionPad;
  const section = figma.createSection();
  section.name = name;

  // Calculate bounds from nodes (before appending — coords are still absolute)
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  for (const n of nodes) {
    minX = Math.min(minX, n.x);
    minY = Math.min(minY, n.y);
    maxX = Math.max(maxX, n.x + n.width);
    maxY = Math.max(maxY, n.y + n.height);
  }

  // Position and size the section
  section.x = snap(minX - padding);
  section.y = snap(minY - padding - 40); // 40px extra for section title bar
  section.resizeWithoutConstraints(
    snap(maxX - minX + padding * 2),
    snap(maxY - minY + padding * 2 + 40)
  );
  section.fills = [{type:"SOLID", color: bgColor}];

  // CRITICAL: After appendChild, set coords to LOCAL (relative to section)
  for (const n of nodes) {
    const absX = n.x;
    const absY = n.y;
    section.appendChild(n);
    n.x = absX - section.x;  // Convert absolute to local
    n.y = absY - section.y;
  }
  return section;
}
```

**Alternative — position nodes with local coords from the start (simpler for single-section diagrams):**
```javascript
// If you only have ONE section and know it starts at (sectionX, sectionY),
// just use local coords directly when creating nodes:
// node.x = 40   (not node.x = sectionX + 40)
// Then position the section after creating all nodes.
```

### Shape Guide (Figma Official Flowchart Symbols)

Use standardized shapes to encode node TYPE. Same symbol = same meaning throughout.

| Node Type | Figma Standard | FigJam shapeType |
|---|---|---|
| Start / End (terminator) | Oval / Ellipse | `ELLIPSE` |
| Process / Action | Rectangle (rounded) | `ROUNDED_RECTANGLE` |
| Decision / Branch | Diamond | `DIAMOND` |
| Input / Output | Parallelogram | `PARALLELOGRAM_LEFT` or `PARALLELOGRAM_RIGHT` |
| Database / Data store | Cylinder | `ENG_DATABASE` |
| Document / File | Document shape | `ENG_FILE` |
| Collection / Folder | Folder | `ENG_FOLDER` |

**Rule: Within a hierarchy, use ONE shape per level.** E.g., tree: Level 1 = ELLIPSE, Level 2 = ROUNDED_RECTANGLE, Level 3 = SQUARE.

### Code Patterns (PROVEN — use these exactly)

**Pipeline node (WHITE fill, dark outline, dark text):**
```javascript
function mkPipe(parent, x, y, text) {
  const s = figma.createShapeWithText();
  s.shapeType = "ROUNDED_RECTANGLE";
  s.resize(300, 90);
  s.fills = [{type:"SOLID", color: {r:1,g:1,b:1}}];
  s.strokes = [{type:"SOLID", color: {r:0.35,g:0.35,b:0.40}}];
  s.strokeWeight = 2;
  s.text.fontName = {family:"Inter", style:"Medium"};
  s.text.characters = text;
  s.text.fontSize = 14;
  s.text.fills = [{type:"SOLID", color: {r:0.15,g:0.15,b:0.20}}];
  parent.appendChild(s);
  s.x = x; s.y = y;
  return s;
}
```

**Colored endpoint node (triggers, outputs — bold fill, white text):**
```javascript
function mkColor(parent, x, y, text, color) {
  const s = figma.createShapeWithText();
  s.shapeType = "ROUNDED_RECTANGLE";
  s.resize(300, 90);
  s.fills = [{type:"SOLID", color: color}];
  s.text.fontName = {family:"Inter", style:"Bold"};
  s.text.characters = text;
  s.text.fontSize = 14;
  s.text.fills = [{type:"SOLID", color: {r:1,g:1,b:1}}];
  parent.appendChild(s);
  s.x = x; s.y = y;
  return s;
}
```

**Default endpoint colors:**
```javascript
const TRIGGER = {r:0.90, g:0.20, b:0.20};  // Red — entry points
const OUTPUT  = {r:0.90, g:0.22, b:0.50};  // Hot pink — destinations
```

**Connector (arrow):**
```javascript
function cn(a, b) {
  const c = figma.createConnector();
  c.connectorStart = {endpointNodeId: a.id, magnet: "AUTO"};
  c.connectorEnd   = {endpointNodeId: b.id, magnet: "AUTO"};
  return c;
}
```

**Loop-back connector (use BOTTOM magnets to avoid overlapping nodes):**
```javascript
const lb = figma.createConnector();
lb.connectorStart = {endpointNodeId: nodeA.id, magnet: "BOTTOM"};
lb.connectorEnd   = {endpointNodeId: nodeB.id, magnet: "BOTTOM"};
```

**Horizontal legend (top of section, inline):**
```javascript
function mkTag(parent, x, y, w, text, fill, txtColor, hasBorder) {
  const s = figma.createShapeWithText();
  s.shapeType = "ROUNDED_RECTANGLE";
  s.resize(w, 35);
  s.fills = [{type:"SOLID", color: fill}];
  if (hasBorder) { s.strokes = [{type:"SOLID", color: {r:0.35,g:0.35,b:0.40}}]; s.strokeWeight = 2; }
  s.text.fontName = {family:"Inter", style:"Medium"};
  s.text.characters = text;
  s.text.fontSize = 13;
  s.text.fills = [{type:"SOLID", color: txtColor}];
  parent.appendChild(s);
  s.x = x; s.y = y;
  return s;
}

// Usage — horizontal row at top of section:
mkTag(section, 60, 55, 120, "LEGEND", {r:.9,g:.9,b:.92}, dark, false); // title
mkTag(section, 190, 55, 140, "Trigger", TRIGGER, white, false);
mkTag(section, 340, 55, 140, "Pipeline", {r:1,g:1,b:1}, dark, true);  // white + border
mkTag(section, 490, 55, 180, "Output", OUTPUT, white, false);
```

**Emoji prefix guide (use in node text for type identity):**

| Node type | Emoji | Example text |
|---|---|---|
| Scheduled trigger | ⏰ | `⏰  Daily 5AM PT` |
| Webhook | 🔗 | `🔗  Webhook Manual` |
| HTTP Request / API | 🌐 | `🌐  Get Uploads\nGET: googleapis.com` |
| Code / Transform | { } | `{ }  Extract Video IDs\nCode Node` |
| Loop / Batch | 🔄 | `🔄  Loop Videos\nSplitInBatches` |
| Database write | 🗄️ | `🗄️  DB: Upsert Content\nPOST: supabase.co` |
| Decision | ❓ | `❓  Is Approved?` |
| File / Document | 📄 | `📄  Generate Report` |

### Layout Templates

**Left-to-right flow (pipelines, n8n workflows):**
```
[Hero START] → [Step 1] → [Step 2] → [Step 3] → [Hero END]
                               ↓
                          [Branch A] → [Output A]

Stickies: Row below the flow, at stickyZoneGap below last row
Legend: Top-right corner
```
- Hero nodes at start and/or end: ELLIPSE, w=500, h=80
- Standard nodes: ROUNDED_RECTANGLE, w=300, h=70
- gapH=40 between nodes (edge-to-edge)
- Branches drop with gapV=120 between rows
- ALL nodes in a row share the same Y coordinate
- Stickies: dedicated row BELOW the flow at stickyZoneGap=200 below last row

**Top-down architecture (tiers, systems):**
```
           [Hero — entry point, ELLIPSE]
           /          |           \
    [Client Tier]  [Router]   [Webhook]      <- Section: Client Layer
           |          |
    [Processor A] [Processor B]              <- Section: Backend
           |          |
    [DB]      [API]    [API]                 <- Section: APIs
```
- ONE section per tier (this is the ONLY case for multiple sections)
- Each tier section gets a soft background color
- Hero at top, sections stack vertically below it
- gapV=120 between tier sections

**Top-down tree (org charts, offer tiers):**
```
        [Root — hero size, ELLIPSE]
        /         |          \
  [Child 1]  [Child 2]  [Child 3]
   /    \        |
[Leaf] [Leaf] [Leaf]
```
- Center root horizontally over children
- Each level: ONE color, ONE shape
- Consistent sizing within each level
- gapV between levels, children spread with gapH

**Funnel (sales, conversion):**
```
+------------- Stage 1 (widest) -------------+
|  [Hero label]  [sticky] [sticky] [sticky]  |  <- Section
+----------- Stage 2 (narrower) ------------+
|  [Hero label]  [sticky] [sticky]           |  <- Section
+-------- Stage 3 (narrower) ---------------+
|  [Hero label]  [sticky]                    |  <- Section
+------ Stage 4 (narrowest) ----------------+
```
- Each stage is ONE section, progressively narrower
- Stage label is hero-sized node at top of each section
- Stickies INSIDE each section, color-matched
- Descriptions OUTSIDE to the left with arrows

**Comparison (current vs future, before/after):**
```
+--- CURRENT STATE (red-tinted section) ------+
|  [Start] → [Manual Step] → [Output]         |
+---------------------------------------------+

+--- FUTURE STATE (green-tinted section) -----+
|  [Start] → [Automated Step] → [Output]      |
+---------------------------------------------+
```
- TWO sections stacked vertically with sectionGap=120 between them
- Same inputs on the left for visual comparison
- Red-tinted section for current; green-tinted for future
- Bottleneck/manual nodes highlighted in current state

**Mind map (brainstorming, concepts):**
```
              topic1 — detail
  branch1 — topic2 — detail
 /
[CENTER] — branch2 — topic3
 \
  branch3 — topic4
```
- Central node: hero-sized, ELLIPSE
- Branches radiate outward (right for main, left for secondary)
- Color per branch, NOT per node
- Connectors are simple lines (no arrowheads for mind maps)

**Grid / Table (journey maps, matrices):**
```
+----------+----------+----------+
| Header 1 | Header 2 | Header 3 |
+----------+----------+----------+
|  Cell    |  Cell    |  Cell    |
+----------+----------+----------+
```
- Consistent column widths
- Headers: bold/hero style
- Row labels on the left

### Design Templates by Type

Each diagram type has its own design system. Use the correct template for the identified type.

#### Mind Map / System Map Template

Use for: skills maps, brainstorming, concept maps, topic exploration, system overviews.

**Nodes:** `figma.createShapeWithText()` — ELLIPSE for root, ROUNDED_RECTANGLE for branches.
- Root: 300x80, 18pt Bold, tinted fill (branch color at 0.15 opacity)
- Branch nodes: 160-200px wide x 50px tall, white fill, colored border matching branch color
- Auto-width: `Math.max(160, text.length * fontSize * 0.55)`

**Color strategy:** Color per BRANCH. All descendants inherit the parent branch color.
```javascript
const branchColors = [
  {r:0.25, g:0.60, b:0.30}, // Green
  {r:0.90, g:0.55, b:0.15}, // Orange
  {r:0.55, g:0.30, b:0.80}, // Purple
  {r:0.20, g:0.55, b:0.85}, // Blue
  {r:0.85, g:0.25, b:0.25}, // Red
  {r:0.80, g:0.60, b:0.10}, // Gold
];
```

**Connectors:** NO arrowheads. Lines only (association, not direction). Set `connectorEndCap: "NONE"`.

**Spacing:**
- Center to Level 1: 300px horizontal
- Level N to Level N+1: 200px horizontal
- Primary branches: 144px vertical gap
- Sub-items within a branch: 72px vertical gap

**Section:** ONE section wrapping the entire map, or no section at all.

```javascript
function mkMindNode(text, x, y, fontSize, color, isRoot) {
  const s = figma.createShapeWithText();
  s.shapeType = isRoot ? "ELLIPSE" : "ROUNDED_RECTANGLE";
  const w = isRoot ? 300 : Math.max(160, text.length * fontSize * 0.55);
  const h = isRoot ? 80 : 50;
  s.resize(w, h);
  s.fills = isRoot
    ? [{type:"SOLID", color: {r: color.r, g: color.g, b: color.b}, opacity: 0.15}]
    : [{type:"SOLID", color: {r:1,g:1,b:1}}];
  s.strokes = [{type:"SOLID", color: color}];
  s.strokeWeight = isRoot ? 3 : 1.5;
  s.text.characters = text;
  s.text.fontSize = fontSize;
  s.text.fills = [{type:"SOLID", color: color}];
  s.x = x; s.y = y;
  return s;
}

function cnMind(a, b) {
  const c = figma.createConnector();
  c.connectorStart = {endpointNodeId: a.id, magnet: "AUTO"};
  c.connectorEnd = {endpointNodeId: b.id, magnet: "AUTO"};
  c.connectorEndCap = "NONE"; // NO arrowheads for mind maps
  return c;
}
```

#### Funnel Template

Use for: sales funnels, conversion flows, staged processes.

**Structure:** Each stage is a colored SECTION, progressively narrower. Center-aligned.
- Stage 1 (top): widest (e.g., 2400px)
- Each subsequent stage: narrower (1800, 1200, 600...)
- Stage height: 400px each, gap: 40px between stages

**Colors:** Bold, saturated, maximally distinct per stage.
```javascript
const funnelStages = [
  {name: "Awareness",     color: {r:0.98,g:0.82,b:0.10}, stickyColor: "STICKY_YELLOW", count: 5},
  {name: "Interest",      color: {r:0.24,g:0.81,b:0.56}, stickyColor: "STICKY_GREEN",  count: 4},
  {name: "Consideration", color: {r:0.29,g:0.56,b:0.85}, stickyColor: "STICKY_BLUE",   count: 2},
  {name: "Decision",      color: {r:0.97,g:0.44,b:0.44}, stickyColor: "STICKY_RED",    count: 1},
];
```

**Stickies:** INSIDE each section, color-matched to stage. 240x240px.
**Descriptions:** OUTSIDE the funnel (to the left) with arrows.
**Connectors:** NONE between stages -- the narrowing shape implies flow.

```javascript
const stageHeight = 400;
const stageGap = 40;
const maxWidth = 2400;
let y = 0;
for (const stage of funnelStages) {
  const section = figma.createSection();
  section.name = stage.name;
  section.x = (maxWidth - stage.w) / 2; // Center each stage
  section.y = y;
  section.resizeWithoutConstraints(stage.w, stageHeight);
  section.fills = [{type:"SOLID", color: stage.color}];
  // Add stickies inside
  const stickyGap = 280;
  for (let i = 0; i < stage.count; i++) {
    const sticky = figma.createSticky();
    sticky.color = stage.stickyColor;
    section.appendChild(sticky);
    sticky.x = 60 + i * stickyGap;
    sticky.y = 120;
  }
  y += stageHeight + stageGap;
}
```

#### Tree / Hierarchy Template

Use for: org charts, offer tiers, decision trees, taxonomy, breakdowns.

**Key rule:** Different SHAPE and PASTEL COLOR per hierarchy level.

```javascript
const treePalette = {
  level0: {fill: {r:1.0, g:0.95, b:0.75}, shape: "PREDEFINED_PROCESS", w: 548, h: 369},
  level1: {fill: {r:0.85, g:0.78, b:0.95}, shape: "SQUARE",             w: 491, h: 320},
  level2: {fill: {r:0.78, g:0.95, b:0.82}, shape: "ROUNDED_RECTANGLE",  w: 443, h: 320},
  level3: {fill: {r:0.78, g:0.88, b:1.0},  shape: "ELLIPSE",            w: 443, h: 443},
};
```

**Nodes are LARGE:** 443-548px wide, 320-443px tall. No squinting.
**Vertical gap between levels:** ~310px edge-to-edge.
**Connectors:** Arrow from BOTTOM of parent to TOP of child.
**Layout:** Center children horizontally under parent.

```javascript
function mkTreeNode(text, level, x, y) {
  const cfg = treePalette["level" + level];
  const s = figma.createShapeWithText();
  s.shapeType = cfg.shape;
  s.resize(cfg.w, cfg.h);
  s.fills = [{type:"SOLID", color: cfg.fill}];
  s.text.characters = text;
  s.text.fontSize = 24;
  s.text.fills = [{type:"SOLID", color: {r:0.15, g:0.15, b:0.20}}];
  s.x = x; s.y = y;
  return s;
}

function connectTree(parent, child) {
  const c = figma.createConnector();
  c.connectorStart = {endpointNodeId: parent.id, magnet: "BOTTOM"};
  c.connectorEnd = {endpointNodeId: child.id, magnet: "TOP"};
  return c;
}

function centerChildren(parentX, parentW, children, childW, gap) {
  const totalW = children.length * childW + (children.length - 1) * gap;
  const startX = parentX + (parentW - totalW) / 2;
  return children.map((_, i) => startX + i * (childW + gap));
}
```

#### Grid / Journey Map Template

Use for: customer journeys, matrices, comparison tables, feature grids.

**Grid rules:**
- Consistent row height: 128px for ALL content rows
- Row labels: 323px wide, with icon/emoji prefix
- Color-coded by row type (one color per row category)
- Title: 64pt Bold. Column headers: 36pt Bold. Cell text: 16pt.
- Row gap: ~22px (tight)

```javascript
const gridConfig = {
  labelColW: 323, cellH: 128, cellGap: 22, colGap: 16,
  headerH: 80, titleH: 128, sectionPadX: 144, sectionPadY: 96,
};
const rowColors = {
  goals:      {r:0.70, g:0.85, b:1.0},  // Light blue
  stages:     {r:0.30, g:0.75, b:0.40},  // Green
  activities: {r:0.95, g:0.95, b:0.95},  // Light gray
  data:       {r:0.95, g:0.85, b:0.20},  // Yellow
  opps:       {r:1.00, g:1.00, b:1.00},  // White
};

function mkGridCell(text, x, y, w, h, color) {
  const s = figma.createShapeWithText();
  s.shapeType = "SQUARE";
  s.resize(w, h);
  s.fills = [{type:"SOLID", color: color}];
  s.text.characters = text;
  s.text.fontSize = 16;
  s.text.fills = [{type:"SOLID", color: {r:0.15,g:0.15,b:0.20}}];
  s.x = x; s.y = y;
  return s;
}
```

### Connector Routing Rules

1. **NEVER let a connector pass through another node.** If the path would cross a node, offset the source/destination to create a clear path.
2. **Stagger parallel connections.** If multiple connectors flow to the same target, offset their source nodes vertically so lines don't overlap.
3. **Same-row connections go straight.** Nodes in the same row connect horizontally with no vertical jog.
4. **Cross-row connections drop cleanly.** Use enough vertical gap (gapV=120) so diagonal connectors have clear room.
5. **Bi-directional connections (loops):** Offset one connector above and one below the node pair.

### Legend Pattern

**Place legends as a HORIZONTAL row at the top of the section.** NOT stacked vertically. NOT in a corner overlapping content. See the `mkTag` code pattern above for the working implementation.

Layout: `[LEGEND] [Trigger] [Pipeline] [Output]` — all at the same Y, spaced horizontally.

## Step 4: Self-QC (MANDATORY — do NOT skip)

**After building, you MUST screenshot and fix issues BEFORE showing the user.** This is not optional.

1. **Screenshot the section** with `mcp__claude_ai_Figma__get_screenshot` using the section's node ID
2. **Visually inspect** for ALL of these — if ANY fail, fix and re-screenshot:
   - [ ] **Overlapping nodes** — no text truncated, no nodes stacked on each other
   - [ ] **Disconnected connectors** — every connector visually touches its source and target
   - [ ] **Old content not deleted** — if replacing a diagram, the old one must be gone
   - [ ] **Section wraps everything** — no nodes floating outside the section
   - [ ] **Text readable** — no "..." truncation, font sizes large enough
   - [ ] **Correct content** — node labels match what was planned, nothing missing
3. **If ANY issue found:** delete the broken parts and rebuild from scratch at correct positions. Do NOT try to move nodes — that breaks connectors.
4. **Re-screenshot after fixes** to confirm the fix worked
5. **Only THEN** share the result with the user

## Step 5: Iterate

If the user wants changes:
- "Move X to the right" — adjust coordinates
- "Add a node for Y" — create new shape and connector
- "Change colors" — swap to a different theme
- "Add more detail to Z" — expand that section

Always read the current page state before making changes to avoid overwriting existing content.

---

## Anti-Patterns (NEVER DO THESE)

### Universal (all diagram types)
- **NEVER apply one type's design to another type.** Workflow styling on a mind map = broken. Funnel styling on a tree = broken. Match the template to the type.
- **NEVER move nodes after creating connectors.** Moving nodes breaks connector endpoints permanently. If layout is wrong, DELETE everything and rebuild from scratch at correct positions.
- **ALWAYS create ALL nodes first, THEN create all connectors.** Connectors reference node IDs — every node must exist before any connector is created.
- **NEVER make nodes different sizes within the same tier/level.** Consistency is the design.
- **NEVER use font size below 14px** on any node. 13px only for legend tags.
- **NEVER let connectors route through nodes.** Use BOTTOM magnets for loop-backs.
- **NEVER forget to convert absolute coords to local after section.appendChild().**
- **When deleting, remove shapes first, then connectors.** Wrap connector removal in try/catch — they may reference already-deleted nodes.

### Workflow/Pipeline specific
- **NEVER color ALL nodes.** Only triggers and outputs get color fills. Pipeline/middle nodes are WHITE with dark outline.
- **NEVER use more than 3 fill colors** (trigger + output + white pipeline).
- **NEVER split a simple linear flow into multiple sections.** One flow = one section.
- **NEVER guess at n8n workflow structure.** Pull real data with `mcp__n8n__n8n_get_workflow`.
- **NEVER skip emoji prefixes in workflows.** Every node needs a type emoji.

### Mind Map specific
- **NEVER use arrowheads in mind maps.** Mind maps show association, not directed flow. Lines only.
- **NEVER color each node independently.** Color the entire BRANCH — all descendants inherit one color.
- **NEVER use sections INSIDE the mind map.** One section wrapping the whole map at most.
- **NEVER make the root node small.** Root should be 1.5-2x the size of branch nodes.

### Tree/Hierarchy specific
- **NEVER make all nodes the same shape.** Shape encodes hierarchy level.
- **NEVER make all nodes the same color.** Color reinforces level distinction.
- **NEVER use tiny nodes.** Trees need big readable nodes (443-548px wide) since you zoom out.
- **NEVER space parent nodes by their OWN width.** Space them by the WIDEST CHILD GROUP width + 60px buffer. If 3 children at 260px + 40px gaps = 860px, parent pillars need 920px+ spacing. This is the #1 cause of child overlap.
- **NEVER space levels too close.** Minimum 250px vertical gap between levels.

### Funnel specific
- **NEVER make stages equal width.** The narrowing IS the message.
- **NEVER use connectors between funnel stages.** The funnel shape itself implies flow.
- **NEVER put stickies in a different color than their stage.**

### Grid/Journey Map specific
- **NEVER vary row heights.** All content rows should be the same height (128px).
- **NEVER skip the header column.** Row labels provide essential context.
