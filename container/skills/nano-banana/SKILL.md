---
name: nano-banana
description: Generate and edit images using Nano Banana (Gemini CLI) with access to 6000+ pro prompts. Use this skill whenever the user asks to create, generate, make, draw, design, or edit any image — thumbnails, icons, diagrams, social graphics, product shots, avatars, patterns, illustrations. Also use when user wants prompt inspiration or recommendations for image generation.
allowed-tools: Bash(gemini:*), Grep, Read, Glob
---

# Nano Banana — Image Generation + Pro Prompts

Generate professional images via the Gemini CLI's nanobanana extension, powered by a library of 6000+ curated pro prompts.

## When to Use This Skill

ALWAYS use this skill when the user:
- Asks for any image, graphic, illustration, or visual
- Wants a thumbnail, featured image, banner, or social graphic
- Requests icons, diagrams, patterns, or avatars
- Asks to edit, modify, or restore a photo
- Wants prompt inspiration or recommendations for image generation
- Uses words like: generate, create, make, draw, design, visualize

---

## Setup Check (First Use Only)

1. Verify extension is installed:
   ```bash
   gemini extensions list | grep nanobanana
   ```
2. If missing, install it:
   ```bash
   gemini extensions install https://github.com/gemini-cli-extensions/nanobanana
   ```
3. Verify API key:
   ```bash
   [ -n "$GEMINI_API_KEY" ] && echo "API key configured" || echo "Missing GEMINI_API_KEY"
   ```

---

## Two Modes

### Mode 1: Direct Generation
User describes what they want → generate immediately (or search prompts first for inspiration).

### Mode 2: Pro Prompt Recommendation
User wants prompt ideas → search the 6000+ prompt library → present top 3 → user picks → optionally remix for their content → generate.

**Default behavior:** If the user gives a clear request, search the prompt library first for a matching pro prompt. If found, offer it. If not, generate with a custom prompt. Always bias toward using the curated library — the prompts are battle-tested.

---

## Available Commands

**Always use the `--yolo` flag to auto-approve all tool actions.**

| Command | Use Case |
|---------|----------|
| `gemini --yolo "/generate 'prompt'"` | Text-to-image generation |
| `gemini --yolo "/edit file.png 'instruction'"` | Modify existing image |
| `gemini --yolo "/restore old_photo.jpg 'fix scratches'"` | Repair damaged photos |
| `gemini --yolo "/icon 'description'"` | App icons, favicons, UI elements |
| `gemini --yolo "/diagram 'description'"` | Flowcharts, architecture diagrams |
| `gemini --yolo "/pattern 'description'"` | Seamless textures and patterns |
| `gemini --yolo "/story 'description'"` | Sequential/narrative images |
| `gemini --yolo "/nanobanana prompt"` | Natural language interface |

### Common Options
- `--count=N` — Generate N variations (1-8)
- `--preview` — Auto-open generated images
- `--styles="style1,style2"` — Apply artistic styles
- `--format=grid|separate` — Output arrangement

### Common Sizes

| Use Case | Dimensions | Flag |
|----------|------------|------|
| YouTube thumbnail | 1280x720 | `--aspect=16:9` |
| Blog featured image | 1200x630 | Social preview friendly |
| Square social (IG, LinkedIn) | 1080x1080 | `--aspect=1:1` |
| Twitter/X header | 1500x500 | Wide banner |
| Vertical story (Reels, TikTok) | 1080x1920 | `--aspect=9:16` |

### Model Selection
Default: `gemini-2.5-flash-image` (~$0.04/image)

For higher quality (4K, better reasoning):
```bash
export NANOBANANA_MODEL=gemini-3-pro-image-preview
```

---

## Pro Prompt Library (6000+ Prompts)

Reference files live in `references/` next to this skill file:

| File | Category | Count |
|------|----------|-------|
| `profile-avatar.json` | Profile / Avatar | 836 |
| `social-media-post.json` | Social Media Post | 4833 |
| `infographic-edu-visual.json` | Infographic / Edu Visual | 390 |
| `youtube-thumbnail.json` | YouTube Thumbnail | 131 |
| `comic-storyboard.json` | Comic / Storyboard | 236 |
| `product-marketing.json` | Product Marketing | 2575 |
| `ecommerce-main-image.json` | E-commerce Main Image | 269 |
| `game-asset.json` | Game Asset | 259 |
| `poster-flyer.json` | Poster / Flyer | 392 |
| `app-web-design.json` | App / Web Design | 143 |
| `others.json` | Uncategorized | 730 |

### Category Signal Mapping

| User Request Signals | File |
|---------------------|------|
| avatar, profile picture, headshot, portrait, selfie | `profile-avatar.json` |
| post, instagram, twitter, facebook, social, viral | `social-media-post.json` |
| infographic, diagram, educational, data viz, chart | `infographic-edu-visual.json` |
| thumbnail, youtube, video cover, click-bait | `youtube-thumbnail.json` |
| comic, manga, storyboard, panel, cartoon story | `comic-storyboard.json` |
| product, marketing, advertisement, promo, campaign | `product-marketing.json` |
| e-commerce, product photo, white background, listing | `ecommerce-main-image.json` |
| game, asset, sprite, character design, item | `game-asset.json` |
| poster, flyer, banner, announcement, event | `poster-flyer.json` |
| app, UI, website, interface, mockup | `app-web-design.json` |

### CRITICAL: Token Optimization

**NEVER fully load category files.** Use Grep to search:
```
Grep pattern="keyword" path="~/.claude/skills/nano-banana/references/category-name.json"
```
- Search multiple category files if the need spans categories
- Load only matching prompts, not entire files

---

## Workflow

### Step 1: Understand the Request

If vague, ask:
- What style? (realistic, illustration, cartoon, abstract, editorial)
- What mood? (professional, playful, dramatic, minimal)
- What dimensions? (square, landscape, portrait, thumbnail)
- What's it for? (social post, thumbnail, product shot, avatar)

If clear, proceed directly.

### Step 2: Search Pro Prompts

1. Identify target category from signal mapping
2. Use Grep to search relevant file(s) with keywords from user's request
3. If no match in primary category, search `others.json`
4. If still no match, craft a custom prompt (mark it as AI-generated)

### Step 3: Present Results

**Max 3 prompts per request.** For each:

```markdown
### [Prompt Title]
**Description**: [Brief description]
**Prompt**:
\`\`\`
[Exact prompt from content field]
\`\`\`
**Sample Images**: [sourceMedia URLs if available]
**Requires Reference Images**: [Yes/No based on needReferenceImages]
```

Then ask: "Want me to generate one of these? Pick 1/2/3, or describe what you want and I'll customize."

### Step 4: Remix (If User Provides Content)

When user provides article/video/content for illustration:
1. Extract core theme, key concepts, emotional tone, visual metaphors
2. Keep the style/structure from selected template
3. Replace subject matter with elements from user's content
4. Adjust details based on any personalization answers

### Step 5: Generate

Run the appropriate `gemini --yolo` command with the final prompt.

After generation:
1. List contents of `./nanobanana-output/` to find generated files
2. Present the image(s) to the user
3. Offer to regenerate with variations if needed

### Refinement Shortcuts
- **"Try again" / "Options"**: Regenerate with `--count=3`
- **"Make it more [adjective]"**: Adjust prompt and regenerate
- **"Edit this one"**: Use `/edit nanobanana-output/filename.png 'adjustment'`
- **"Different style"**: Add `--styles="requested_style"`

---

## Prompt Crafting Tips

1. **Be specific**: Include style, mood, colors, composition details
2. **Add "no text"**: If you don't want text rendered in the image
3. **Reference styles**: "editorial photography", "flat illustration", "3D render", "watercolor"
4. **Specify aspect ratio context**: "wide banner", "square thumbnail", "vertical story"

## Output Location

All generated images save to `./nanobanana-output/` in the current directory.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `GEMINI_API_KEY` not set | `export GEMINI_API_KEY="your-key"` |
| Extension not found | Run install command from setup section |
| Quota exceeded | Wait for reset or switch to flash model |
| Image generation failed | Check prompt for policy violations, simplify request |
