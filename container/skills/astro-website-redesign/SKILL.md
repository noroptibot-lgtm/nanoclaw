---
name: astro-website-redesign
description: Use when user wants to rebuild or redesign an existing website using Astro and Tailwind CSS, especially when given a URL to an existing site, a reference design URL, and wants local images, working contact forms, and sub-pages.
---

# Astro Website Redesign

## Overview

Build a premium, multi-page Astro + Tailwind redesign of an existing website. Uses Playwright to extract content and image URLs, downloads images locally to avoid hotlink blocking, and produces a production-ready static site with a working contact form.

## When to Use

- User gives you a URL to an existing website and wants it rebuilt/redesigned
- User wants Astro + Tailwind with real images, sub-pages, and a working form
- User provides a reference design URL to match the style of

## Core Workflow

### 1. Setup Astro + Tailwind

```bash
mkdir -p /Applications/websites/my-site
cd /Applications/websites/my-site
echo "1" | npm create astro@latest my-site -- --template basics --no-install --no-git
cd my-site && npm install && npx astro add tailwind --yes
```

`src/styles/global.css` starts with `@import "tailwindcss";`

### 2. Analyze Existing Site with Playwright

```js
// Navigate and extract all image URLs
mcp__playwright__browser_navigate({ url: 'https://example.no/' })
mcp__playwright__browser_evaluate({
  function: `() => Array.from(document.querySelectorAll('img'))
    .map(i => i.src).filter(s => s.includes('wp-content'))`
})
// Also check the snapshot for: nav links, copy, product names, colors, phone/email
```

### 3. Download Images Locally (bypass hotlink protection)

```bash
mkdir -p public/images
for url in "https://example.no/wp-content/uploads/..."; do
  filename=$(basename "$url")
  curl -sL -o "public/images/$filename" \
    -H "Referer: https://example.no/" \
    -H "User-Agent: Mozilla/5.0" \
    "$url" && echo "✓ $filename"
done
```

Reference images as `/images/filename.jpg` in Astro.

### 4. Project Structure

```
src/
  layouts/Layout.astro     # Base with <Nav /> and <Footer />
  components/
    Nav.astro              # Sticky nav + top info bar
    Footer.astro           # 4-column footer
  pages/
    index.astro            # Home: hero, categories, why us, products, CTA
    produkter.astro        # Products catalog
    om-oss.astro           # About page
    kontakt.astro          # Contact with working form
  styles/global.css
public/images/             # All downloaded images
```

### 5. Design System (Lovable-style reference)

Match dark/light alternating sections:

```css
/* Dark sections */
bg-[#0f0f17]   /* hero, why-us, footer */
/* Light sections */
bg-white        /* product highlights */
bg-gray-50      /* product grid */
/* Accent */
text-orange-500 bg-orange-500 hover:bg-orange-400
/* Serif italic for hero headline accent */
font-family: 'Playfair Display', serif; font-style: italic;
```

**Nav pattern:**
- Top bar: address + phone + email (hidden on mobile)
- Sticky header: logo left, nav center, CTA button right (orange pill)

**Hero pattern:**
```astro
<section class="relative min-h-[92vh] flex items-center bg-[#0f0f17]">
  <img ...  class="absolute inset-0 w-full h-full object-cover opacity-50" />
  <div class="absolute inset-0 bg-gradient-to-r from-[#0f0f17] via-[#0f0f17]/70 to-transparent" />
  <!-- Content with: label, h1 with serif-italic accent, subtitle, 2 CTAs, slide dots -->
</section>
```

**Product card pattern:**
```astro
<a class="group bg-white border border-gray-200 hover:border-orange-300 rounded-2xl overflow-hidden">
  <div class="aspect-[4/3] overflow-hidden">
    <img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
  </div>
  <div class="p-4">
    <span class="text-orange-500 text-xs font-semibold uppercase">Category</span>
    <h3 class="font-bold text-sm mt-1">Product name</h3>
    <div class="text-orange-500 text-xs font-semibold">Be om tilbud →</div>
  </div>
</a>
```

### 6. Working Contact Form (Formspree)

```astro
<form action="https://formspree.io/f/USER@EMAIL.COM" method="POST">
  <!-- fields -->
</form>

<script>
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const res = await fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' },
    });
    if (res.ok) { showSuccess(); } else { showError(); }
  });
</script>
```

Formspree will ask user to verify email on first submission — no account needed for basic use.

### 7. Scroll Reveal Animation

In Layout.astro `<script>`:
```js
const observer = new IntersectionObserver(
  (entries) => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
  { threshold: 0.08 }
);
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

In CSS: `.reveal { opacity: 0; transform: translateY(24px); transition: ... }` `.reveal.visible { opacity: 1; transform: none; }`

### 8. Build & Serve

```bash
npm run build          # Verify all 4 pages build clean
pkill -f "astro dev"   # Kill old instances
npm run dev -- --port 4321
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Images blocked/broken | Always download locally with `curl -H "Referer: ..."` |
| Multiple dev servers | `pkill -f "astro dev"` before starting |
| Port already in use | Use `--port 4321` explicitly, kill old processes first |
| Tailwind v4 syntax | Use `@import "tailwindcss"` not `@tailwind base/components/utilities` |
| Form not sending | User must verify email with Formspree on first submission |
| Build errors with JSX in .astro | Use `{array.map(...)}` not `array.map(...).join('')` |

## Quick Reference

| Task | Command/Pattern |
|------|----------------|
| Create project | `echo "1" \| npm create astro@latest my-site -- --template basics --no-install --no-git` |
| Add Tailwind | `npx astro add tailwind --yes` |
| Download image | `curl -sL -o public/images/name.jpg -H "Referer: https://site.com/" URL` |
| Dev server | `npm run dev -- --port 4321` |
| Kill servers | `pkill -f "astro dev"` |
| Build check | `npm run build` |
