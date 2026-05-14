# Design Generation Specification
# claude.ai/design equivalent — encode these rules into every generated design

This reference defines the exact constraints that make generated designs match claude.ai/design quality.
The design-generator agent MUST follow all rules below before producing any output.

---

## 1. Color System — oklch() mandatory

### Construction method
1. Pick a **hue seed** (0–360) from the brief's brand words
2. Build a **5-step lightness ramp** per hue: L = 20, 40, 60, 80, 92
3. Chroma by role:
   - Neutrals (bg, surface, text): C = 0.00–0.04
   - Secondary (borders, muted text): C = 0.04–0.08
   - Primary / accent (CTAs, highlights): C = 0.12–0.22
4. **Never** use pure `#000000` / `#ffffff` — tint blacks toward brand hue at L=12, whites at L=97

### 60-30-10 distribution
- 60%: dominant neutral (background, card surfaces)
- 30%: secondary (text, borders, secondary elements)
- 10%: accent (CTAs, highlights, interactive focus)

### Token naming
```css
:root {
  --ec-color-bg:            oklch(97% 0.01 [H]);
  --ec-color-surface:       oklch(93% 0.02 [H]);
  --ec-color-border:        oklch(82% 0.03 [H]);
  --ec-color-text-primary:  oklch(18% 0.02 [H]);
  --ec-color-text-secondary:oklch(42% 0.03 [H]);
  --ec-color-action:        oklch(55% 0.18 [H]);
  --ec-color-action-hover:  oklch(48% 0.20 [H]);
  --ec-color-action-text:   oklch(98% 0.01 [H]);
  --ec-color-danger:        oklch(50% 0.20 30);
  --ec-color-success:       oklch(52% 0.16 155);
}
```

### Dark mode (via `prefers-color-scheme: dark`)
- Flip L axis: bg → L=12, surface → L=18, text-primary → L=92
- Reduce chroma by ~20% (vibrant colors look harsher on dark)
- Recheck ALL contrast ratios (separate from light mode check)

---

## 2. CSS Namespace — ec-* mandatory

Every CSS class and custom property must use the `ec-` prefix. No exceptions.

```css
/* CORRECT */
.ec-card { ... }
.ec-btn-primary { ... }
--ec-space-4: 0.25rem;

/* WRONG */
.card { ... }
.btn-primary { ... }
--space-4: 0.25rem;
```

This prevents collision with Tailwind and any other framework.
When integrated into Next.js: CSS goes into `globals.css` at the end.

---

## 3. Typography — non-generic fonts required

### Font selection protocol
1. Extract 3 brand-voice adjectives from the brief
2. Map adjectives to font personality:
   - Precise / technical / minimal → Geist, Space Grotesk, Outfit
   - Warm / approachable / human → Plus Jakarta Sans, Nunito, Bricolage Grotesque
   - Bold / confident / editorial → Syne, Cabinet Grotesk, Bebas Neue (display only)
   - Elegant / premium / refined → Cormorant, Libre Baskerville, Lora (sparingly)
   - Playful / creative / energetic → Dela Gothic One, Unbounded (display only)

3. **Never use**: Inter, Roboto, DM Sans, System-ui, IBM Plex (overused defaults = AI-generic signal)

### Type scale — 5 steps, 1.25× ratio minimum
```css
--ec-text-xs:   0.75rem;   /* 12px */
--ec-text-sm:   0.875rem;  /* 14px */
--ec-text-base: 1rem;      /* 16px */
--ec-text-lg:   1.25rem;   /* 20px */
--ec-text-xl:   1.5rem;    /* 24px */
--ec-text-2xl:  2rem;      /* 32px */
--ec-text-3xl:  2.5rem;    /* 40px */
```

### Line height
- Body text: 1.5–1.6
- Headings: 1.1–1.2
- Light text on dark background: add 0.05–0.1 extra
- Body text max-width: `max-width: 65ch`

### Google Fonts import format
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## 4. Spacing — 4pt grid, rem-based tokens

Only these spacing values are allowed:

```css
--ec-space-1:  0.25rem;  /* 4px */
--ec-space-2:  0.5rem;   /* 8px */
--ec-space-3:  0.75rem;  /* 12px */
--ec-space-4:  1rem;     /* 16px */
--ec-space-6:  1.5rem;   /* 24px */
--ec-space-8:  2rem;     /* 32px */
--ec-space-12: 3rem;     /* 48px */
--ec-space-16: 4rem;     /* 64px */
--ec-space-24: 6rem;     /* 96px */
```

Never use: 3px, 5px, 7px, 10px, 15px, 18px, 22px, 25px, etc.

---

## 5. Component States — all 8 required

Every interactive element (button, input, link, select, checkbox, radio, toggle) MUST implement:

| State | CSS mechanism |
|---|---|
| default | base styles |
| hover | `:hover` |
| focus | `:focus-visible` (never `outline: none` without replacement) |
| active | `:active` |
| disabled | `[disabled]` or `.ec-disabled` — visual + pointer-events: none |
| loading | `.ec-loading` class — spinner or skeleton |
| error | `.ec-error` class — danger color |
| success | `.ec-success` class — success color |

---

## 6. Output Formats

### Format A: Self-contained HTML (default)
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Design Name]</title>
  <!-- Google Fonts -->
  <link ...>
  <style>
    /* All CSS here — ec-* namespace + oklch() tokens */
  </style>
</head>
<body>
  <!-- Complete UI markup with ec-* classes -->
</body>
</html>
```
Opens directly in browser. Zero build step.

### Format B: Next.js component (`--next` flag)
```tsx
// [ComponentName].tsx
export function [ComponentName]() {
  return (
    <div className="ec-container">
      {/* markup */}
    </div>
  )
}
```
```css
/* Append to globals.css */
/* === [ComponentName] Design System === */
:root { --ec-color-*: ...; }
.ec-container { ... }
```

### Format C: Palette only (`--palette-only` flag)
Output only the CSS custom properties block + font import + a color swatch preview.

---

## 7. Responsive Design

- Mobile-first: base styles for mobile, `@media (min-width: ...)` for larger
- Use `min-width` queries, never `max-width`-only
- Replace `height: 100vh` → `height: 100dvh` (iOS Safari fix)
- Touch targets: minimum 44×44px
- No horizontal overflow (test at 375px width mentally)

---

## 8. Anti-Pattern Self-Check Gate

Before writing the final output, verify ZERO matches for each:

```
[ ] Inter / Roboto / DM Sans in font-family
[ ] #000000 or #ffffff (pure black/white)
[ ] background-clip: text (gradient text)
[ ] border-left: 3px+ or border-right: 3px+ as decorative stripe
[ ] Nested cards (card inside card with both having border/shadow)
[ ] Any spacing value not divisible by 4
[ ] outline: none without :focus-visible replacement
[ ] Input with only placeholder, no visible <label>
[ ] Error messages positioned above the field
[ ] 8+ font sizes with < 1.1× ratio between steps
[ ] body text wider than 75ch
[ ] rgb() or hsl() in palette (use oklch() instead)
[ ] CSS class without ec-* prefix (custom classes only)
[ ] Missing hover state on interactive element
[ ] Missing focus-visible state on interactive element
[ ] Missing disabled state on buttons/inputs
```

If any match: fix before outputting.

---

## 9. File Naming Convention

Generated files go to `design-results/` directory:
- `design-results/design-output.html` — Format A output
- `design-results/[ComponentName].tsx` — Format B component
- `design-results/globals-append.css` — Format B CSS block
- `design-results/palette.css` — Format C palette only

After generating, output a **Design Summary Card**:

```
┌─────────────────────────────────────────────────┐
│  Design: [Name]                                 │
│  Palette: oklch([L]% [C] [H]) + neutrals        │
│  Fonts: [Heading Font] / [Body Font]            │
│  Brand words: [word1] / [word2] / [word3]       │
│  Mode: [light / dark / both]                    │
│  Output: design-results/design-output.html      │
│  Anti-pattern violations: 0                     │
└─────────────────────────────────────────────────┘
```
