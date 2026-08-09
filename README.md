# NicSkills

Atomic Agent Skills for **developer tooling** — script-first, dogfood-first, install on demand.

> Prefix: `nic-` · Positioning: [PROJECT.md](./PROJECT.md)

![NicSkills promo](./docs/promo/nicskills-promo.png)

![NicSkills features](./docs/promo/nicskills-features.png)

## Skills

| Skill | Status | What it does |
|-------|--------|----------------|
| [`nic-html-preview`](./skills/nic-html-preview/) | 0.2.1 | Serve local `.html` over localhost; open via Cursor / browser MCP / system browser (adaptive) |
| [`nic-image-gen`](./skills/nic-image-gen/) | 0.1.1 | Route image gen to Cursor `GenerateImage` or Codex `$imagegen`; save under `nic-skills-artifacts/image-gen/` (instruction-only) |

## Install (local / dogfood)

```bash
# Cursor personal skills (examples)
ln -sfn "$(pwd)/skills/nic-html-preview" ~/.cursor/skills/nic-html-preview
ln -sfn "$(pwd)/skills/nic-image-gen" ~/.cursor/skills/nic-image-gen
```

Or:

```bash
npx skills add nickylin/NicSkills --skill nic-html-preview
npx skills add nickylin/NicSkills --skill nic-image-gen
```

Prefer **single-skill** install. Full-repo install loads more context than you need.

## Design principles

1. One skill, one job
2. Deterministic logic lives in `scripts/` when needed; routers can be instruction-only
3. Keep `SKILL.md` lean
4. Use it yourself before open-sourcing

## License

MIT (planned — LICENSE file lands before public release)
