# NicSkills

Atomic Agent Skills for **developer tooling** — script-first, dogfood-first, install on demand.

> Prefix: `nic-` · Positioning: [PROJECT.md](./PROJECT.md)

![NicSkills promo](./docs/promo/nicskills-promo.png)

![NicSkills features](./docs/promo/nicskills-features.png)

## Skills

| Skill | Status | What it does |
|-------|--------|----------------|
| [`nic-html-preview`](./skills/nic-html-preview/) | 0.2.1 | Serve local `.html` over localhost; open via Cursor / browser MCP / system browser (adaptive) |
| [`nic-image-gen`](./skills/nic-image-gen/) | 0.1.2 | Route AI bitmap gen to Cursor `GenerateImage` or Codex `$imagegen` → `nic-skills-artifacts/image-gen/` |
| [`nic-visual-code`](./skills/nic-visual-code/) | 0.1.3 | Mermaid / SVG / HTML visuals + icons (no image API); size/theme + no-mojibake → `nic-skills-artifacts/visual-code/` |

## Featured: `nic-visual-code`

Code-based visuals **without** image-generation APIs — editable, UTF-8 safe, git-friendly.

![nic-visual-code promo](./docs/visual-code/nic-visual-code-promo.svg)

**What it can do**

| Capability | Default | Notes |
|------------|---------|--------|
| Mermaid diagrams | structural charts | flow / architecture / sequence |
| SVG illustrations | vectors | posters, maps, feature boards |
| SVG icons | `1:1` · 1080×1080 | app icon / favicon / monogram |
| HTML one-pagers | `16:9` slides | preview with [`nic-html-preview`](./skills/nic-html-preview/) |
| Themes | `dark-dev` | also `light-clean` / `mono` / `brand` |
| Sizes | `16:9` or `1:1` | also `9:16` / `og` / custom `WxH` |

Install:

```bash
npx skills add nickylin/NicSkills --skill nic-visual-code
```

### Examples

**Icon** (`1:1` SVG)

![NicSkills icon](./docs/visual-code/nic-skills-icon.svg)

**Skill map** (SVG diagram)

![NicSkills skill map](./docs/visual-code/nicskills-skill-map.svg)

**Feature board** (Cursor 3.11 / July 2026, `16:9`)

![Cursor July 2026 features](./docs/visual-code/cursor-july-2026-features.svg)

More detail: [`skills/nic-visual-code/SKILL.md`](./skills/nic-visual-code/SKILL.md)

## Install (local / dogfood)

```bash
# Cursor personal skills (examples)
ln -sfn "$(pwd)/skills/nic-html-preview" ~/.cursor/skills/nic-html-preview
ln -sfn "$(pwd)/skills/nic-image-gen" ~/.cursor/skills/nic-image-gen
ln -sfn "$(pwd)/skills/nic-visual-code" ~/.cursor/skills/nic-visual-code
```

Or:

```bash
npx skills add nickylin/NicSkills --skill nic-html-preview
npx skills add nickylin/NicSkills --skill nic-image-gen
npx skills add nickylin/NicSkills --skill nic-visual-code
```

Prefer **single-skill** install. Full-repo install loads more context than you need.

## Design principles

1. One skill, one job
2. Deterministic logic lives in `scripts/` when needed; routers can be instruction-only
3. Keep `SKILL.md` lean
4. Use it yourself before open-sourcing

## License

MIT (planned — LICENSE file lands before public release)
