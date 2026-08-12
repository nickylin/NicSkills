---
name: nic-ppt-html
description: >-
  Analyze a project or folder and produce a 16:9 PPT-style HTML slide deck for
  executive / architecture / product reporting. Built-in styles: project-brand,
  consulting, keynote, midnight, tech-dark. Single-file HTML with keyboard
  navigation. Use when the user wants PPT HTML, 汇报幻灯片, 项目总结PPT,
  架构宣讲, nic-ppt-html, slide deck from repo, or folder-to-presentation.
  Prefer over nic-visual-report when the deliverable is multi-slide flips, not a
  single long report page. Do not use for icon-only or AI photoreal asks.
version: 0.1.0
---

# nic-ppt-html — Project / folder → PPT HTML

Turn **repo or folder facts** into a **shareable 16:9 HTML slide deck**. Instruction-only. Zero-dependency single file by default (no Slidev/reveal required).

## Related skills

| Need | Skill |
|------|--------|
| Single-page report (not flips) | [`nic-visual-report`](../nic-visual-report/) |
| Extra Mermaid / SVG blocks | [`nic-visual-code`](../nic-visual-code/) |
| Preview the deck | [`nic-html-preview`](../nic-html-preview/) |
| AI atmosphere cover (rare) | [`nic-image-gen`](../nic-image-gen/) |

## Privacy (required)

- Never put secrets, tokens, API keys, private home paths, or credentials into slides.
- Prefer workspace-relative paths in the deck.
- Do not invent metrics, headcount, or revenue — only facts from the scoped tree / user notes. Missing → localized `未知` / `Unknown`.

## Language (required)

Match the **user's conversation language** for slide titles and body.

1. Detect from latest user messages.
2. Honor explicit overrides (`用英文` / `in Chinese`).
3. Keep skill names, code ids, product names, and paths untranslated.
4. Set `<html lang="zh-CN">` or `lang="en">` accordingly.

## Encoding

- UTF-8 + `<meta charset="utf-8">`.
- CJK stack when Chinese: `"PingFang SC", "Noto Sans SC", "Microsoft YaHei", …`
- No emoji decoration unless asked.

## Output location

```text
nic-skills-artifacts/ppt-html/
```

- `mkdir -p` if needed.
- Filename: `YYYYMMDD-<slug>-deck.html` (or user name).
- Ensure host `.gitignore` contains `nic-skills-artifacts/` when appropriate.
- README / docs embeds belong under `docs/` (never link gitignored artifacts from README).

## Workflow

Copy and track:

```text
PPT Progress:
- [ ] 1. Scope
- [ ] 2. Discover
- [ ] 3. Brand
- [ ] 4. Outline
- [ ] 5. Render
- [ ] 6. Preview (optional)
- [ ] 7. Report back
```

### 1. Scope

- Default: current workspace root.
- If user names a path/folder → analyze **only** that tree.
- Ask once if both “whole monorepo” vs “one package” is ambiguous.

### 2. Discover (read-only)

Skim, do not dump entire repos into chat:

- `README*`, `PROJECT.md`, `package.json` / `pyproject.toml` / `go.mod`
- Top-level dirs that signal product surface
- Theme sources: `globals.css`, `tailwind.config.*`, `theme.*`, CSS vars `--primary` / `--brand` / `--color-primary`
- Architecture docs / ADRs if present

### 3. Brand → style

1. Extract 1 primary + optional secondary hex (document in HTML comment: `/* brand-source: path #hex */`).
2. Choose style skeleton (see **Styles**).
3. Map primary → `--accent`; derive `--accent-2`; keep surfaces from the skeleton.
4. Never invent a purple-glow default palette.

User unspecified style:

| Signal | Style |
|--------|--------|
| Decision / board / consulting | `consulting` + brand accent |
| Launch / demo / keynote energy | `keynote` + brand |
| Pitch / fundraising tone | `midnight` + brand |
| Tech review / architecture (default for eng repos) | `tech-dark` + brand |
| Explicit “跟项目配色” | `project-brand` (tech-dark or consulting skeleton by UI light/dark) |

### 4. Outline (deck-type)

| Type | When | Suggested flow |
|------|------|----------------|
| `exec-brief` | Leadership update | Cover · Answer first · Context · Progress · Risks · Next |
| `architecture` | System / skill map | Cover · Problem · Overview diagram · Layers · Key paths · Trade-offs · Q&A |
| `product` | Feature narrative | Cover · Value · Capabilities · Flow · Proof · Roadmap |
| `retro` | Postmortem | Cover · Goal · Results · Wins · Issues · Actions |
| `pitch` | External intro | Cover · Pain · Solution · Differentiation · Proof · Close |
| `custom` | User outline | Follow user |

Unspecified: architecture docs / multi-module repo → `architecture`; otherwise `exec-brief` or `product`.

**Length:** 10–18 slides default; short ask → 6–8; deep dive → ≤25. One idea per slide.

### 5. Render

Write one self-contained HTML file:

- Viewport / slide frame **16:9**
- Full-screen `.slide` sections; keyboard `←` `→` `Space` `Home` `End`
- Optional click zones / progress dots
- Page indicator `n / N`
- `@media print` (or `?print`) — one slide per printed page
- CSS variables from [reference/themes.md](reference/themes.md)
- Layout patterns from [reference/layouts.md](reference/layouts.md)
- Inline SVG for architecture when it clarifies; optional compose `nic-visual-code`
- Footer: deck type · style · generated via nic-ppt-html · no secrets

### 6. Preview

Offer / run `nic-html-preview` when useful.

### 7. Report back

In the user's language: style + deck-type + slide count + relative path + 1–3 sentence verbal summary. Do **not** paste the whole deck into chat.

## Styles (built-in)

| Id | Vibe | Best for |
|----|------|----------|
| `project-brand` | Skeleton + project accent | Default when matching product UI |
| `consulting` | White, action titles, MBB-like | Exec / strategy |
| `keynote` | Black, huge type, sparse | Launch / vision |
| `midnight` | Deep navy, KPI glass | Pitch / metrics |
| `tech-dark` | Charcoal + cool accent | Engineering / NicSkills family |

Full tokens + Do/Don't: [reference/themes.md](reference/themes.md).  
Inspiration (do not vendor whole frameworks): [reveal.js](https://github.com/hakimel/reveal.js), [Slidev themes](https://github.com/slidevjs/themes), [SlideSpeak design prompts](https://github.com/SlideSpeak/presentation-design-prompts).

## HTML quality bar

- Action / conclusion titles preferred over topic labels (`我们选择脚本优先` not `设计原则`).
- ≤5 bullets or one primary visual per slide.
- Architecture decks **must** include at least one diagram slide.
- High contrast; readable from a projected room.
- Avoid: emoji spam, purple neon defaults, dense paragraph walls, fake charts.

## Error handling

| Symptom | Fix |
|---------|-----|
| Thin README / no facts | Ask for focus areas or mark Unknown — do not fabricate |
| No brand colors found | Fall back to `tech-dark` defaults; note in comment |
| User wants one long page | Hand off to `nic-visual-report` |
| User wants only an icon | Hand off to `nic-visual-code` |

## Examples

See [examples.md](examples.md).

Trigger phrases: `PPT HTML` / `项目汇报幻灯片` / `做成可翻页的HTML` / `架构宣讲PPT` / `nic-ppt-html` / `folder to slides`.
