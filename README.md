# NicSkills

Atomic Agent Skills for **developer tooling** — script-first, dogfood-first, install on demand.

> Prefix: `nic-` · Positioning: [PROJECT.md](./PROJECT.md)

## Skills

| Skill | Status | What it does |
|-------|--------|----------------|
| [`nic-html-preview`](./skills/nic-html-preview/) | 0.2.1 | Serve local `.html` over localhost; open via Cursor / browser MCP / system browser (adaptive) |

## Install (local / dogfood)

Until the repo is public on GitHub, point your agent at this path or symlink:

```bash
# Cursor personal skills (example)
ln -sfn "$(pwd)/skills/nic-html-preview" ~/.cursor/skills/nic-html-preview
```

Later (planned):

```bash
npx skills add nickylin/NicSkills --skill nic-html-preview
```

Prefer **single-skill** install. Full-repo install loads more context than you need.

## Design principles

1. One skill, one job
2. Deterministic logic lives in `scripts/`
3. Keep `SKILL.md` lean
4. Use it yourself before open-sourcing

## License

MIT (planned — LICENSE file lands before public release)
