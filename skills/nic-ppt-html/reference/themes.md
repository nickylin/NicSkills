# Built-in themes — nic-ppt-html

Apply via CSS variables on `:root` (and optional `[data-style="…"]`).  
**Always** allow `project-brand` to override `--accent` / `--accent-2` from discovered product colors.

## Shared contract

```css
:root {
  --bg: …;
  --fg: …;
  --muted: …;
  --accent: …;
  --accent-2: …;
  --surface: …;
  --border: …;
  --font-display: …;
  --font-body: …;
  --font-mono: ui-monospace, "JetBrains Mono", Menlo, monospace;
  --slide-pad: clamp(2.5rem, 5vw, 4.5rem);
}
```

## `tech-dark` (engineering default / NicSkills family)

```css
--bg: #0f1419;
--fg: #e7ecf1;
--muted: #8aa0b5;
--accent: #3d9cf0;      /* brand-source example: demo.html */
--accent-2: #5eb1ff;
--surface: #1a2a3a;
--border: #2a3a4a;
--font-display: "IBM Plex Sans", "PingFang SC", "Noto Sans SC", system-ui, sans-serif;
--font-body: "IBM Plex Sans", "PingFang SC", "Noto Sans SC", system-ui, sans-serif;
```

Do: code/architecture friendly, cool blue accents, subtle radial atmosphere.  
Don't: purple glow, neon grids, glassmorphism overload.

## `project-brand`

Not a fixed palette. Pick skeleton by UI:

- Dark product UI → start from `tech-dark` or `keynote`
- Light product / docs UI → start from `consulting`

Then set:

```css
--accent: <primary from theme files>;
--accent-2: <lighter or secondary>;
```

HTML comment required:

```html
<!-- brand-source: path/to/theme #3d9cf0 -->
```

If no color found → `tech-dark` defaults + comment `brand-source: fallback tech-dark`.

## `consulting` (MBB / decision)

Inspired by consulting deck conventions (e.g. SlideSpeak McKinsey-style prompts).

```css
--bg: #ffffff;
--fg: #051c2c;
--muted: #4e5b66;
--accent: #2251ff;      /* replace with project primary when branding */
--accent-2: #2251ff;
--surface: #f0f4f8;
--border: #d6dee6;
--font-display: "Gelasio", "Noto Serif SC", Georgia, serif;
--font-body: "Arimo", "PingFang SC", "Noto Sans SC", system-ui, sans-serif;
```

Do: full-sentence **action titles**; one accent hit per slide; hairline rules; takeaway bar with 3px left accent.  
Don't: gradients, drop shadows, large radius cards, decorative imagery.

## `keynote` (Apple Basic energy)

Inspired by Slidev `theme-apple-basic` / Keynote Minimal.

```css
--bg: #000000;
--fg: #f5f5f7;
--muted: #a1a1a6;
--accent: #2997ff;
--accent-2: #64d2ff;
--surface: #1c1c1e;
--border: #2c2c2e;
--font-display: "SF Pro Display", "PingFang SC", system-ui, sans-serif;
--font-body: "SF Pro Text", "PingFang SC", system-ui, sans-serif;
```

Do: huge title, vast negative space, one idea.  
Don't: dense bullets, chrome UI chrome, multi-column clutter.

## `midnight` (pitch / KPI)

Inspired by SlideSpeak Midnight Pitch + dark enterprise decks.

```css
--bg: #0a1838;
--fg: #ffffff;
--muted: #94a8cc;
--accent: #2e6bff;
--accent-2: #22d3ee;
--surface: rgba(255, 255, 255, 0.05);
--border: rgba(255, 255, 255, 0.12);
--font-display: "Sora", "PingFang SC", system-ui, sans-serif;
--font-body: "Inter", "PingFang SC", system-ui, sans-serif;
```

Do: oversized metrics; restrained frosted panels; one gradient text highlight max.  
Don't: light backgrounds, hard opaque card farms, >2 accent hues.

## Upstream references (read when needed)

| Source | Why |
|--------|-----|
| https://github.com/hakimel/reveal.js | Keyboard / print / PDF patterns (~72k★) |
| https://github.com/slidevjs/themes | apple-basic, seriph, default |
| https://github.com/SlideSpeak/presentation-design-prompts | Copyable theme prompts (McKinsey, Midnight, …) |

Do **not** require npm install of Slidev/reveal for the default deliverable. CDN reveal.js is optional only if the user asks.
