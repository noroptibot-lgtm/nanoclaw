# GIF Maker (Slack GIF Creator)

## Overview

The GIF Maker skill provides a comprehensive toolkit for creating animated GIFs optimized specifically for Slack, with built-in validators for strict size constraints and composable animation primitives. This skill handles the technical challenges of GIF optimization while providing creative freedom through modular animation building blocks.

## Who Should Use This Skill

- **Team Communication Managers** creating custom Slack emojis and reactions
- **Community Managers** developing engaging visual content for team channels
- **Designers** producing animated content for Slack workspaces
- **Marketing Teams** creating branded animated GIFs for internal communications
- **Anyone** wanting to create custom animated GIFs or emoji for Slack

## Purpose and Use Cases

Use this skill when you need to:
- Create custom animated emojis for Slack (under 64KB)
- Build animated GIFs for Slack messages (under 2MB)
- Produce reaction GIFs with specific animations (shake, bounce, pulse, etc.)
- Generate team-specific visual content for Slack communication
- Create animated visual effects optimized for Slack's requirements

**Keywords that trigger this skill:** Slack GIF, emoji animation, "make me a GIF for Slack of X doing Y", animated emoji

## What's Included

### Slack Requirements Validation

**Message GIFs:**
- Max size: ~2MB
- Optimal dimensions: 480x480 pixels
- Recommended FPS: 15-20
- Color limit: 128-256 colors
- Duration: 2-5 seconds

**Emoji GIFs (Strict):**
- Max size: 64KB (strictly enforced by Slack)
- Optimal dimensions: 128x128 pixels
- Recommended FPS: 10-12
- Color limit: 32-48 colors (crucial for file size)
- Duration: 1-2 seconds
- **Note:** Emoji GIFs are very challenging due to 64KB limit

### Animation Primitives (Composable Building Blocks)

**Shake:** Trembling or vibrating motion in horizontal, vertical, or both directions

**Bounce:** Jumping or bouncing movement with realistic gravity and impact

**Spin/Rotate:** Clockwise, counterclockwise, or wobble rotation effects

**Pulse/Heartbeat:** Smooth scaling or double-pump heartbeat animations

**Fade:** Fade in, fade out, or crossfade between elements

**Zoom:** Dramatic zoom in/out with optional motion blur and explosion effects

**Explode/Shatter:** Burst explosions, shattering effects, particle dissolution

**Wiggle/Jiggle:** Jello wobbles, wave motion, excited wiggles

**Slide:** Slide in from directions with optional overshoot, multi-object staging

**Flip:** Horizontal or vertical flip transitions between states

**Morph/Transform:** Crossfade, scale, or spin morphs between different elements

**Move:** Linear, arc, circular, or wave movement patterns with easing

**Kaleidoscope:** Symmetric patterns and mirror effects for psychedelic visuals

### Helper Utilities

**GIF Builder:**
- Frame assembly and management
- Automatic color quantization
- Duplicate frame removal
- Size optimization for Slack limits
- Emoji mode (aggressive optimization)

**Text Rendering:**
- Text with outlines for readability
- Typography scaling for small GIFs
- Multiple font size presets

**Color Management:**
- Professional color palettes (vibrant, pastel, dark, neon, professional)
- Cohesive color schemes for visual consistency

**Visual Effects:**
- Particle systems (sparkles, confetti)
- Impact flashes
- Shockwave rings
- Motion blur

**Easing Functions:**
- Smooth motion interpolation (ease_in, ease_out, ease_in_out)
- Bounce effects
- Elastic/overshoot effects
- Back-out easing

## How It Works

### Development Philosophy

This toolkit provides **building blocks, not rigid recipes**. The approach is:

1. **Understand the creative vision** - What should happen? What's the mood?
2. **Design the animation** - Break into phases (anticipation, action, reaction)
3. **Apply primitives as needed** - Mix and combine animations freely
4. **Validate constraints** - Check file size, especially for emoji GIFs
5. **Iterate if needed** - Reduce frames/colors if over size limits

### Typical Workflow

**Step 1: Choose Animation Type**
- Determine if this is a Message GIF (2MB limit, more freedom) or Emoji GIF (64KB strict limit)
- Plan the animation phases and effects needed

**Step 2: Create Animation**
```python
from core.gif_builder import GIFBuilder
from templates.pulse import create_pulse_animation

# Create GIF builder
builder = GIFBuilder(width=128, height=128, fps=10)

# Generate animation frames using primitives
frames = create_pulse_animation(
    object_data={'emoji': '❤️', 'size': 100},
    pulse_type='heartbeat',
    num_frames=20
)

# Add frames to builder
for frame in frames:
    builder.add_frame(frame)
```

**Step 3: Save and Validate**
```python
# Save with optimization
info = builder.save('emoji.gif',
                   num_colors=48,
                   optimize_for_emoji=True)

# Automatic validation warnings appear if file exceeds limits
```

**Step 4: Iterate if Needed**
- If file size too large: reduce frames, reduce colors, simplify design
- If animation not smooth: increase FPS or add more intermediate frames
- If colors look bad: adjust palette or use fewer colors

### Composing Multiple Primitives

Animations can be freely combined:

```python
# Example: Bounce + shake for impact effect
for i in range(num_frames):
    # Apply bounce motion
    y = interpolate(start_y, ground_y, t, 'bounce_out')

    # Add shake on impact
    if y >= ground_y - 5:
        shake_x = math.sin(i * 2) * 10
        x = center_x + shake_x
    else:
        x = center_x

    draw_emoji(frame, '⚽', (x, y), size=60)
```

## Optimization Strategies

### For Message GIFs (>2MB)
1. Reduce frames (lower FPS or shorter duration)
2. Reduce colors (128 → 64 colors)
3. Reduce dimensions (480x480 → 320x320)
4. Enable duplicate frame removal

### For Emoji GIFs (>64KB) - Be Aggressive
1. **Limit to 10-12 frames total** (critical)
2. **Use 32-40 colors maximum** (critical)
3. **Avoid gradients** - solid colors compress much better
4. **Simplify design** - fewer elements on screen
5. **Use optimize_for_emoji=True** in save method
6. **Test frequently** - validate file size after each change

**Emoji GIF Strategy:**
The 64KB limit is extremely strict. Successful emoji GIFs require:
- Minimal frame count (10-15 max)
- Very limited color palette (32-48 colors)
- Simple designs without gradients
- Aggressive optimization enabled

## Technical Details

### Dependencies

```bash
pip install pillow imageio numpy
```

### Core Modules

**core/gif_builder.py** - GIF assembly and optimization
**core/validators.py** - Slack size validation
**core/typography.py** - Text rendering with outlines
**core/color_palettes.py** - Professional color schemes
**core/visual_effects.py** - Particle systems and effects
**core/easing.py** - Motion interpolation functions
**core/frame_composer.py** - Drawing utilities

**templates/** - Animation primitive implementations (shake.py, bounce.py, pulse.py, etc.)

### File Size Calculation

The validators automatically check:
- File size in KB and MB
- Whether it meets Slack's limits
- Frame count and duration
- Dimensions and recommendations

```python
from core.validators import validate_gif, is_slack_ready

# Complete validation
all_pass, results = validate_gif('emoji.gif', is_emoji=True)

# Quick check
if is_slack_ready('emoji.gif', is_emoji=True):
    print("Ready to upload to Slack!")
```

## Example Use Cases

### Simple Reaction (Emoji)
Pulsing heart emoji for reactions - 12 frames, 40 colors, under 64KB

### Excited Celebration (Emoji)
Confetti burst with shake - 15 frames, 35 colors, optimized for 64KB

### Action with Impact (Message GIF)
Ball bouncing with flash effect - 30 frames, 128 colors, under 2MB

### Loading Indicator (Message GIF)
Spinning loader with smooth rotation - 24 frames, 64 colors

### Multi-Element Animation (Message GIF)
Multiple emojis sliding in sequence with stagger - 40 frames, 128 colors

## Best Practices

### Creative Approach
- **Design in phases** - anticipation, action, reaction
- **Use appropriate primitives** - shake for impact, pulse for attention, etc.
- **Combine effects thoughtfully** - don't overload with too many simultaneous animations
- **Test the mood** - does the animation convey the intended emotion?

### Technical Optimization
- **Start conservative** - easier to add frames than remove them
- **Validate early and often** - especially for emoji GIFs
- **Use solid colors when possible** - better compression
- **Limit color palette strategically** - group similar colors
- **Remove unnecessary frames** - duplicate frame removal helps

### Emoji GIF Specific
- **Keep it simple** - complex animations won't fit in 64KB
- **Minimal frames** - 10-15 is the sweet spot
- **Test different color counts** - sometimes 35 colors works, sometimes need 45
- **Avoid gradients entirely** - solid color transitions only
- **Consider pixel art style** - inherently simple and low color count

### Message GIF Specific
- **More freedom** - 2MB allows richer animations
- **Higher frame counts** - smoother motion with 20-30 frames
- **More colors** - 128-256 for better visual quality
- **Add effects** - particles, flashes, trails for impact

## Common Issues and Solutions

**Problem:** Emoji GIF exceeds 64KB
**Solution:** Reduce to 10-12 frames, use 32-40 colors, simplify design, remove gradients

**Problem:** Animation looks choppy
**Solution:** Increase FPS or add more intermediate frames with easing functions

**Problem:** Colors look wrong after optimization
**Solution:** Use pre-defined color palettes or manually select optimal color set

**Problem:** File size barely over limit
**Solution:** Try reducing color count by 10-20, or remove 1-2 frames

**Problem:** Text unreadable in small emoji
**Solution:** Use draw_text_with_outline with thick outline, or make text larger