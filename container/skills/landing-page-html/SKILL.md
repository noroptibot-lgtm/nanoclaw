---
name: landing-page-html
version: 2.0.0
description: Technical requirements reference for building single-file, Tailwind-based landing pages and thank-you pages from scratch. Covers Tailwind setup with extended palettes, Google Fonts integration, responsive strategy, accessibility, form configuration, performance constraints, and conversion optimization. The Page Builder constructs each page from a visual design brief -- no fixed template. Used by the Page Builder and Front-End Designer agents.
---

# Landing Page HTML -- Technical Requirements Reference

Every landing page and thank-you page is a single, self-contained HTML file. No build step, no external dependencies beyond Tailwind CDN and Google Fonts. The Page Builder reads a visual design brief (`design/visual-brief.md`) and copy documents, then constructs `index.html`, `thank-you.html`, and `deliverables.html` from scratch.

**There is no fixed template.** Section order, layout patterns, color palettes, and visual treatments are specified per-client in the visual design brief. This document covers the technical constraints and requirements that every page must meet regardless of design.

## Tailwind CSS Setup

Every generated page starts with this `<head>` structure, customized per the visual design brief:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Page Title]</title>
  <meta name="description" content="[Meta description from copy]">

  <!-- Google Fonts (max 2 families) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[Font1]:wght@[weights]&family=[Font2]:wght@[weights]&display=swap" rel="stylesheet">

  <!-- Tailwind CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: 'var(--color-primary)',
            'primary-dark': 'var(--color-primary-dark)',
            'primary-light': 'var(--color-primary-light)',
            accent: 'var(--color-accent)',
            'accent-light': 'var(--color-accent-light)',
            surface: 'var(--color-surface)',
            'surface-dark': 'var(--color-surface-dark)',
          },
          fontFamily: {
            heading: ['[Heading Font]', /* fallback stack */],
            body: ['[Body Font]', /* fallback stack */],
          }
        }
      }
    }
  </script>

  <style>
    /* CSS Custom Properties -- set from visual design brief palette */
    :root {
      --color-primary: #XXXXXX;
      --color-primary-dark: #XXXXXX;
      --color-primary-light: #XXXXXX;
      --color-accent: #XXXXXX;
      --color-accent-light: #XXXXXX;
      --color-surface: #XXXXXX;
      --color-surface-dark: #XXXXXX;
    }

    html { scroll-behavior: smooth; }

    /* Custom CSS from visual design brief:
       - Gradients
       - CSS animations (@keyframes)
       - Decorative elements (clip-paths, shapes)
       - Hover transitions
       - Scroll-triggered animations
    */
  </style>
</head>
```

Key points:
- CSS custom properties in `:root` set the full palette from the visual design brief (6-10 colors, not just primary/accent)
- Tailwind config extends colors so utility classes like `bg-primary`, `text-accent-light`, `bg-surface` all work
- Font families configured in Tailwind so `font-heading` and `font-body` utility classes work
- Google Fonts loaded via `<link>` with `display=swap` for performance
- Custom CSS in `<style>` block handles gradients, animations, decorative elements per the design brief
- `scroll-behavior: smooth` on `html` enables smooth scroll to `#signup` anchors

## Performance Constraints

These are hard limits. Every page must respect them:

1. **Single file**: Each page (`index.html`, `thank-you.html`) is one self-contained HTML file. No external CSS files, no external JS files.
2. **Max 2 Google Font families**: Load only 2 font families from Google Fonts (but can load multiple weights per family). Specify only the weights actually used.
3. **No JavaScript beyond Tailwind config**: No custom JS. No JavaScript animation libraries. All animations must be CSS-only (`@keyframes`, `transition`, `animation`). The only JS allowed is the `tailwind.config` script block.
4. **Tailwind CDN only**: Use `https://cdn.tailwindcss.com`. No PostCSS, no build step.
5. **No external images in markup**: Do not reference external image URLs. Client logos are local files (`logo.png`). All decorative visuals must be CSS-only (gradients, shapes, shadows, borders).
6. **Reasonable file size**: The HTML file should stay under ~50KB. Avoid excessive inline SVGs or deeply nested elements.

## Responsive Strategy

- Mobile-first: base styles target phones (< 768px)
- `md:` breakpoint (768px) for tablets and small laptops
- `lg:` breakpoint (1024px) for desktops
- `xl:` breakpoint (1280px) -- use sparingly, only when the design brief specifies wide layouts
- Common patterns:
  - Section padding: `py-16 px-6` minimum, adjust per design brief
  - Content containment: `max-w-[value] mx-auto` per the brief's content max-width
  - Grid layouts: stack on mobile (`grid-cols-1`), expand on desktop (`md:grid-cols-2`, `md:grid-cols-3`)
  - Typography scales: use Tailwind responsive prefixes (e.g., `text-3xl md:text-4xl lg:text-5xl`)
  - Split/asymmetric layouts: stack on mobile, side-by-side on `md:` or `lg:`
  - Hide decorative elements on mobile if they crowd the layout: `hidden md:block`

## Accessibility Requirements

Every page must meet these accessibility standards:

- Semantic structure: `<html lang="en">`, `<main>`, `<section>`, `<footer>`
- Single `<h1>`, proper `<h2>`/`<h3>` hierarchy (no skipped levels)
- Color contrast: text on colored backgrounds must meet WCAG AA (4.5:1 ratio minimum for normal text, 3:1 for large text). Verify contrast for every text/background combination in the design brief palette.
- All `<img>` tags include descriptive `alt` attributes
- Form inputs have `id` attributes matching their `<label for="">` values (use `sr-only` labels if the design uses placeholders only)
- Submit button uses `type="submit"`
- Focus states visible: `focus:ring-2 focus:ring-[color]` or equivalent visible focus indicator on all interactive elements
- Interactive elements (`<a>`, `<button>`, `<details>`) are keyboard-navigable by default with native HTML
- No `tabindex` manipulation unless necessary
- `prefers-reduced-motion` media query: wrap CSS animations in `@media (prefers-reduced-motion: no-preference) { }` so users who prefer reduced motion don't see them

## Form Configuration

- `action` URL uses the `{{FORM_ACTION_URL}}` placeholder -- each client's ESP is configured post-build
- Use `action="{{FORM_ACTION_URL}}"` and add an HTML comment: `<!-- TODO: Replace {{FORM_ACTION_URL}} with the client's email platform endpoint -->`
- Method is always `POST`
- Required fields: `name` (text), `email` (email type with validation)
- Each input has a visible `placeholder` and an `sr-only` label for screen readers
- Button text matches the CTA from the copy document
- Form `id="signup"` so the hero CTA can anchor-link to it

## CSS Custom Properties Pattern

Use CSS custom properties for the extended palette so values are centralized and Tailwind can reference them:

```css
:root {
  --color-primary: #XXXXXX;
  --color-primary-dark: #XXXXXX;
  --color-primary-light: #XXXXXX;
  --color-accent: #XXXXXX;
  --color-accent-light: #XXXXXX;
  --color-surface: #XXXXXX;
  --color-surface-dark: #XXXXXX;
  --color-text-primary: #XXXXXX;
  --color-text-secondary: #XXXXXX;
  --color-background: #XXXXXX;
}
```

All hex values come from the visual design brief's color palette table. Never hard-code color values in HTML class attributes -- always reference the custom properties through Tailwind utility classes (`bg-primary`, `text-accent`, etc.) or CSS variables in the `<style>` block.

## Conversion Optimization Checklist

The Page Builder applies these rules to every landing page regardless of design:

1. **Single CTA**: The same call-to-action appears in the Hero (as anchor link to `#signup`) and in the signup form section (as the form submit button). No other CTAs, no competing actions.
2. **No navigation**: No `<nav>`, no header links, no footer links beyond copyright. One page, one goal.
3. **Smooth scroll**: Hero CTA links to `#signup` with `scroll-behavior: smooth` on `<html>`.
4. **Above-the-fold impact**: Hero section loads with headline, subheadline, and CTA visible without scrolling on desktop.
5. **Visual hierarchy**: Primary heading (h1) largest, section headings (h2) clearly smaller, body text comfortable reading size. The design brief typography specs enforce this.
6. **Whitespace**: Generous padding per section (minimum `py-16`). The design brief may specify more.
7. **Social proof before commitment**: Testimonials/proof elements appear before the final signup form.
8. **FAQ reduces friction**: Common objections addressed before the final signup form.
9. **Form simplicity**: Only two fields (name, email). No phone, no address, no dropdowns. Fewer fields means higher conversion.
10. **Privacy reassurance**: Short text below the submit button (e.g., "We respect your privacy. Unsubscribe anytime.").

## What NOT to Do

- **Do not use a fixed HTML template.** Build every page from scratch following the visual design brief.
- **Do not default to centered-text-on-solid-background for every hero.** The design brief specifies the hero treatment.
- **Do not use the same section order for every client.** The design brief specifies section ordering.
- **Do not hard-code colors.** Always use CSS custom properties.
- **Do not add JavaScript.** All interactivity must be CSS-only or native HTML (like `<details>` for accordions).
- **Do not skip the design brief.** If no brief exists, do not proceed -- report the issue.
- **Do not add agency branding.** Landing pages and thank-you pages are the client's brand only.

## Page Structure Rules

These structural rules apply to every page regardless of design:

- No `<nav>` element. Landing pages have a single focus -- no navigation links.
- The CTA button appears exactly twice: once in the Hero (links to `#signup`), once in the Final CTA section (the form submit button).
- `<main>` wraps all content sections. `<footer>` sits outside `<main>`.
- Heading hierarchy: one `<h1>` in Hero, `<h2>` for each section, `<h3>` for sub-items within sections.
- Section markup follows the visual design brief's section-by-section direction, not a fixed pattern.

## Thank-You Page

Same `<head>` setup as the landing page (Tailwind CDN, same Google Fonts, same color palette). The design brief's "Thank-You Page Direction" specifies the visual treatment.

Required elements:
- Confirmation message (headline + subtext)
- Lead magnet download section (button or text fallback if no URL)
- "What happens next" numbered steps
- Footer matching the landing page
- Client branding only (no agency attribution)

If no `lead_magnet_url` is available, omit the download button and replace it with a text message: "Check your email for the download link."

## Deliverables HTML (deliverables.html)

A print-optimized document containing all copy deliverables. The member opens it in a browser and uses Print > Save as PDF. **This file does NOT use the visual design brief** -- it is a clean print document with the member's agency branding.

Structure requirements:
- Use inline/embedded CSS (no Tailwind) for maximum print compatibility
- Print styles via `@media print { }` (page breaks, font size, hidden elements)
- "Save as PDF" button visible on screen, hidden in print via `.no-print`
- Table of contents on screen, hidden in print
- Each deliverable section uses `page-break-before: always` after the first
- `section { page-break-inside: avoid; }` keeps short sections together
- Print footer visible only in print via `.print-only`
- All link styling stripped in print
- MEMBER/AGENCY branding (header, footer, colors from `config/member-profile.md`)
- All 5 copy deliverables: landing page, lead magnet outline, email sequence, thank-you page, ad copy
- Content inserted as rendered HTML, not raw markdown
