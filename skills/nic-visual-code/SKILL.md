---
name: nic-visual-code
description: >-
  Create visuals with editable code (Mermaid, SVG, or HTML) — no image-generation
  API. Supports app/favicon/monogram icons (SVG 1:1), diagrams, illustrations,
  size/aspect (1:1, 16:9, 9:16, og, WxH), and themes (dark-dev, light-clean, mono,
  brand). Use when the user wants 代码出图, 不用生图API, SVG图标, 小图标, icon,
  favicon, logo, 应用图标, SVG插图, Mermaid流程图, nic-visual-code, 16:9,
  浅色主题, vector illustration, or git-friendly graphics. Do not use for AI
  photoreal / style-heavy bitmaps — hand off to nic-image-gen.
version: 0.1.3
---

# nic-visual-code — Code-based visuals (no image API)

Produce **editable** visuals by writing Mermaid / SVG / HTML into the workspace. Instruction-only: no scripts, no `GenerateImage`, no Codex `$imagegen`, no third-party image APIs.

**Supported outputs include:** diagrams, SVG illustrations, **icons / favicons / monograms**, and HTML one-pagers.

## Encoding & text rendering (required — no mojibake)

Rendered text must stay readable. **Never ship mojibake or broken glyphs** (e.g. U+FFFD replacement character, tofu boxes).

1. **UTF-8 only** — save source as UTF-8.
   - SVG: start with `<?xml version="1.0" encoding="UTF-8"?>`
   - HTML: include `<meta charset="utf-8">`
   - Mermaid in Markdown: normal UTF-8 `.md` / `.mmd`
2. **Prefer safe punctuation in SVG/HTML labels** — use ASCII `-` `/` `|` or the word `to` instead of middle-dot / arrow / em-dash symbols when those may fail in the viewer font.
3. **Font stacks must cover the language in use**
   - Latin: `"Segoe UI", Helvetica, Arial, sans-serif`
   - Chinese present: put `"PingFang SC", "Noto Sans SC", "Microsoft YaHei"` **first**
4. **After writing, self-check** — re-read the file; if any replacement character or unexpected garbage appears, rewrite those labels with plain ASCII/CJK words and re-save UTF-8.
5. **Do not** rely on emoji or rare symbols for meaning in diagrams.

## Related skill

| Need | Skill |
|------|--------|
| AI bitmap / 宣传插画 / atmosphere | [`nic-image-gen`](../nic-image-gen/) |
| Editable diagram / SVG art / **icon** / HTML visual | **this skill** |

If the user clearly wants photoreal style or host image models, switch to `nic-image-gen`.

## Privacy (required)

- Never put real machine paths, home directories, usernames, emails, tokens, or API keys into skill docs or examples.
- Prefer workspace-relative paths when speaking to the user.
- Do not dump secrets into SVG/HTML comments.

## Format chooser (default)

| Intent | Format | Extension |
|--------|--------|-----------|
| Flow / architecture / sequence / ER | **Mermaid** | `.md` (fenced) or `.mmd` |
| Illustration, icon, decorative vector | **SVG** | `.svg` |
| Multi-block laid-out one-pager | **HTML** | `.html` |

- User names a format → honor it.
- Unspecified structural chart → Mermaid.
- Unspecified “插图 / icon / logo-ish vector” → SVG.
- Unspecified poster / card with several text blocks → HTML.

## Output directory (required)

```text
nic-skills-artifacts/visual-code/
```

- Brand-scoped — **do not** use generic `images/`, `output/`, `assets/`, or `diagrams/`.
- `mkdir -p nic-skills-artifacts/visual-code` if missing.
- Never write into this skill’s own directory.
- Optionally ensure host `.gitignore` contains `nic-skills-artifacts/`.

Subfolders by format are optional but encouraged when many files accumulate:

```text
nic-skills-artifacts/visual-code/mermaid/
nic-skills-artifacts/visual-code/svg/
nic-skills-artifacts/visual-code/html/
```

## Size & aspect ratio

Honor user size/ratio when stated; otherwise use defaults below.

| Token | Meaning | SVG / HTML canvas |
|-------|---------|-------------------|
| `1:1` | square | `1080 x 1080` |
| `4:3` | classic | `1280 x 960` |
| `16:9` | landscape / slide / banner | `1280 x 720` (default for wide diagrams) |
| `9:16` | portrait / phone | `720 x 1280` |
| `og` | Open Graph card | `1200 x 630` |
| custom `WxH` | e.g. `800x600` | use exact pixels |

How to apply:

- **SVG:** set `width` / `height` / `viewBox="0 0 W H"` to the chosen size.
- **HTML:** set page/`main` to that aspect (CSS `aspect-ratio` or fixed `width`/`min-height`); keep mobile-friendly when ratio is not portrait-locked.
- **Mermaid:** size is viewer-dependent; put intended ratio in a short HTML comment or Markdown note above the fence (e.g. `<!-- target: 16:9 -->`). Do not fake pixel size inside Mermaid syntax.

If unspecified: structural diagrams → comfortable landscape (`16:9` or content-driven SVG around `960 x 560`); icons → `1:1`.

## Icons (first-class)

This skill **explicitly supports icons** — not only flowcharts.

| Trigger (examples) | Default |
|--------------------|---------|
| 图标 / 小图标 / icon / favicon / app icon / logo / 应用图标 / monogram | SVG · `1:1` · `1080x1080` |

Icon rules:

1. **Format:** SVG (real vectors — no embedded raster PNG).
2. **Size:** `1:1` unless the user asks otherwise (`512x512`, `256x256`, etc.).
3. **Shape:** full-bleed square canvas; optional rounded app-tile (`rx` ~20–22% of side) when it is an app/icon mark.
4. **Readability at small sizes:** few shapes, strong contrast, limited text (prefer monogram / 1–2 letters); avoid tiny hairlines that vanish at 16–32px.
5. **Filename:** `*-icon.svg` or `*-favicon.svg` under `nic-skills-artifacts/visual-code/svg/`.
6. **Hand off:** photoreal / textured / 3D-looking icon art → [`nic-image-gen`](../nic-image-gen/).

## Theme / style

Honor an explicit theme; otherwise default **`dark-dev`**.

| Theme id | Look |
|----------|------|
| `dark-dev` (default) | charcoal bg, cool blue/teal accents, high contrast light text |
| `light-clean` | white/off-white bg, dark text, thin borders, minimal shadows |
| `mono` | grayscale only, print-friendly |
| `brand` | follow colors the user pasted or linked (CSS variables); do not invent a purple glow theme |

Rules:

- Express theme with **CSS variables** in HTML/SVG (`--bg`, `--fg`, `--accent`, `--muted`).
- One theme per file unless the user asks for variants (then separate files: `*-dark-dev.svg`, `*-light-clean.svg`).
- Avoid default AI clichés: purple-on-white gradients, glow soup, emoji decoration (unless requested).
- Chinese labels → CJK-capable font stack (see Encoding section).

## Workflow

1. Pick format with the table above.
2. Resolve **size/ratio** and **theme** (user override → else defaults).
3. Ensure the output directory exists.
4. Write a single clear source file (descriptive kebab-case name; optional suffix `-{theme}` / `-{ratio}`).
5. Keep source self-contained; use CSS variables for theme tokens.
6. **Preview (optional)**
   - HTML → offer / use [`nic-html-preview`](../nic-html-preview/) when the user wants to open it.
   - SVG → open as file or embed in a tiny HTML wrapper only if needed for preview.
   - Mermaid → leave in Markdown/`.mmd`; render depends on the host viewer (GitHub, IDE preview). Do not invent an image API to rasterize unless the user explicitly asks for a bitmap (then consider `nic-image-gen` or host export — do not silently call image APIs from this skill).
7. Report: format + theme + size/ratio + workspace-relative path.

## Quality bar

- One primary idea per file.
- Adequate contrast; avoid purple-glow clichés unless requested.
- SVG: real vector shapes/text, not a giant base64 PNG dump; **no mojibake**.
- Mermaid: valid syntax; prefer `flowchart` / `sequenceDiagram` / `C4` only when appropriate.
- HTML: single file when possible; UTF-8 meta; works at mobile width.

## Error handling

| Symptom | Fix |
|---------|-----|
| User wants AI photo / style bitmap | Hand off to `nic-image-gen` |
| Mermaid fails to parse | Fix syntax; do not fall back to image API |
| Labels show boxes / mojibake | Replace fancy unicode punctuation; ensure UTF-8 + CJK font stack; rewrite file |
| “导出成 PNG” | Ask whether they want a screenshot of HTML/SVG via preview tools, or true AI raster via `nic-image-gen` |

## Do / Don't

| Do | Don't |
|----|--------|
| Ship editable Mermaid/SVG/HTML | Call GenerateImage / `$imagegen` / paid image APIs |
| Use `nic-skills-artifacts/visual-code/` | Dump into generic `images/` |
| UTF-8 + safe labels + CJK-capable fonts | Leave `·` `→` `↔` if they render as garbage |
| Cross-link `nic-image-gen` when needed | Pretend code output is an AI photo |

## Examples

**Diagram**

User: 用代码画一个 NicSkills 关系图，16:9，dark-dev，不要走生图 API

1. Format → Mermaid or SVG · Size `16:9` · Theme `dark-dev`  
2. Write under `nic-skills-artifacts/visual-code/…`  
3. Reply with format + theme + ratio + relative path  

**Icon**

User: svg 输出一个 nic-skills 小图标 icon

1. Format → SVG · Size `1:1` (`1080x1080`) · Theme `dark-dev`  
2. Write `nic-skills-artifacts/visual-code/svg/nic-skills-icon.svg`  
3. Reply with format + theme + ratio + relative path  

Trigger phrases to honor: `图标` / `icon` / `favicon` / `16:9` / `方形` / `light-clean` / `浅色主题` / `OG图尺寸`.
