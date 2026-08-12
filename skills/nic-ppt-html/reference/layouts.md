# Slide layouts — nic-ppt-html

Aspect **16:9**. Use semantic sections: `<section class="slide" data-layout="…">`.

## Required chrome

Every deck:

1. Cover (`cover`)
2. Closing (`close`) — thank you / Q&A / next step
3. Progress: `current / total` + optional dots
4. Keyboard: Left/Right/Space/Home/End

## Layout catalog

### `cover`

- Brand or project name (hero-level)
- One headline (≤12 words)
- One supporting line
- Optional date / audience / confidentiality

### `agenda` / `section`

- Numbered sections
- Highlight current section when used as tracker (`consulting`)

### `title-body`

- Action title
- ≤5 short bullets OR short paragraph (≤3 lines)

### `two-column`

- Title + left/right equal panels (compare, before/after, problem/solution)

### `kpi-row`

- 3–4 oversized numbers + short labels (`midnight` / proof slides)

### `diagram`

- Title + full-bleed-ish SVG or Mermaid-rendered SVG
- Optional 2–4 caption notes under/beside

### `quote` / `statement`

- One large sentence (vision / principle)

### `code`

- Title + monospace block (≤16 lines); prefer highlight one idea

### `table`

- Compact comparison (≤5 rows × ≤4 cols)

### `close`

- Recap in 3 lines max OR single CTA
- Contact / repo / install one-liner

## Skeleton CSS (minimal)

Agents may expand, but keep this behavior:

```css
html, body { height: 100%; margin: 0; background: var(--bg); color: var(--fg); }
.deck { height: 100%; overflow: hidden; }
.slide {
  display: none;
  box-sizing: border-box;
  width: 100vw;
  height: 100vh;
  padding: var(--slide-pad);
  flex-direction: column;
  justify-content: center;
}
.slide.active { display: flex; }
@media print {
  .slide { display: flex; page-break-after: always; height: 100vh; }
  .chrome { display: none; }
}
```

## Content rules by layout

| Layout | Title style | Body |
|--------|-------------|------|
| consulting content | Full-sentence conclusion | Evidence under title |
| keynote | 3–8 word punch | Almost empty |
| tech-dark diagram | Noun + verb | Diagram first |
| midnight kpi | Short claim | Numbers dominate |

## Anti-patterns

- Cards-in-cards on cover
- More than one diagram + long bullets on same slide
- Footer competing with title
- Horizontal scroll inside a slide
