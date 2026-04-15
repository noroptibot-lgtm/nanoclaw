---
name: scroll-animation-masterclass
description: Build scroll-driven product animations like Apple's AirPods/iPad pages. Generate product images, animate with AI video, extract frames, and drive them from scroll position. Trigger on /scroll-animation or when user asks about scroll-scrubbed video or Apple-style product pages.
---

# Scroll Animation Masterclass

Build Apple-style scroll-scrubbed product animations end-to-end using AI tools. The scroll position drives playback of an image sequence — no video element, no autoplay, no jank.

## The Big Picture

1. Generate a 3D-ish product image with AI (Midjourney/DALL-E/Flux/Ideogram)
2. Animate it in AI video (Runway Gen-3/Kling/Pika/Luma) as a short rotation/reveal
3. Extract frames as WebP
4. Build a scroll page that maps `scrollY` to `frame index`
5. Polish with synced copy and preloading

## Step 1 — Generate Product Image

Use any strong image model. Prompt for a clean isolated product on neutral background, studio lighting, straight-on or 3/4 angle. You want a single hero frame you can animate.

## Step 2 — AI Video Animation

Feed the image into Runway Gen-3 (or Kling, Pika, Luma). Prompt for a short rotation (360°), reveal, or parts-separation animation. 2–5 seconds is plenty. Export as MP4.

## Step 3 — Extract Frames

```bash
ffmpeg -i product_rotation.mp4 \
  -vf "fps=30,scale=1200:-1" \
  -c:v libwebp -quality 85 \
  frames/frame_%04d.webp
```

- `fps=30` — smooth scrubbing
- `scale=1200:-1` — cap width at 1200px, preserve aspect
- `libwebp` + `quality 85` — ~60% smaller than JPEG at equivalent quality

At 30fps for 3 seconds you get 90 frames. Total payload target: under 2.5MB.

## Step 4 — Scroll Page Skeleton

```html
<section class="scroll-section" style="height: 300vh;">
  <div class="sticky-wrap">
    <canvas id="scroll-canvas"></canvas>
  </div>
</section>
```

```css
.scroll-section { position: relative; }
.sticky-wrap {
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
#scroll-canvas { max-width: 100%; height: auto; }
```

```js
const canvas = document.getElementById('scroll-canvas');
const ctx = canvas.getContext('2d');
const FRAME_COUNT = 90;
const frames = [];

// Preload
for (let i = 0; i < FRAME_COUNT; i++) {
  const img = new Image();
  img.src = `frames/frame_${String(i + 1).padStart(4, '0')}.webp`;
  frames.push(img);
}

frames[0].onload = () => {
  canvas.width = frames[0].width;
  canvas.height = frames[0].height;
  ctx.drawImage(frames[0], 0, 0);
};

window.addEventListener('scroll', () => {
  const section = document.querySelector('.scroll-section');
  const rect = section.getBoundingClientRect();
  const total = section.offsetHeight - window.innerHeight;
  const progress = Math.min(Math.max(-rect.top / total, 0), 1);
  const frameIdx = Math.min(FRAME_COUNT - 1, Math.floor(progress * FRAME_COUNT));
  if (frames[frameIdx].complete) {
    ctx.drawImage(frames[frameIdx], 0, 0);
  }
});
```

## Step 5 — Polish & Copy

Overlay text at specific scroll positions. Define copy cues as `{ atProgress: 0.2, text: 'Crystal clear audio' }` and fade them in/out as `progress` crosses their range. Keep copy under 8 words per cue.

## Step 6 — Performance

- **WebP conversion is non-negotiable** — JPEG sequences are 2–3x larger
- **Smart preloading** — load the first 10 frames eagerly, rest lazily as user scrolls
- **Budget** — total sequence under 2.5MB, first paint under 1.2s
- **Throttle scroll handler** with `requestAnimationFrame`

### FrameManager Class

```js
class FrameManager {
  constructor(count, pathFn, eagerCount = 10) {
    this.count = count;
    this.pathFn = pathFn;
    this.frames = new Array(count);
    this.loaded = new Array(count).fill(false);
    // Eager load first N
    for (let i = 0; i < Math.min(eagerCount, count); i++) this.load(i);
  }
  load(i) {
    if (this.frames[i]) return;
    const img = new Image();
    img.onload = () => { this.loaded[i] = true; };
    img.src = this.pathFn(i);
    this.frames[i] = img;
  }
  get(i) {
    if (!this.frames[i]) this.load(i);
    // Prefetch neighbors
    this.load(Math.min(this.count - 1, i + 1));
    this.load(Math.min(this.count - 1, i + 5));
    return this.loaded[i] ? this.frames[i] : null;
  }
}
```

## Checklist

- [ ] Hero image generated at 1200px+ width
- [ ] Video animation 2–5 seconds, smooth loop or single rotation
- [ ] Frames extracted at 30fps as WebP
- [ ] Sticky scroll section with 300vh height
- [ ] Scroll handler driven by `requestAnimationFrame`
- [ ] Copy cues synced to scroll progress
- [ ] Total payload under 2.5MB
- [ ] First 10 frames eager, rest lazy
