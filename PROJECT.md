# NicSkills — Project Positioning

## Brand & prefix

| Item | Value |
|------|--------|
| Brand | NicSkills |
| Skill prefix | `nic-` |
| GitHub | [nickylin/NicSkills](https://github.com/nickylin/NicSkills) |
| Install | `npx skills add nickylin/NicSkills --skill nic-xxx` |

## Core scenario (v1)

**Developer tooling for Agent workflows** — small, script-first skills that remove friction when coding with Cursor / Claude Code / Codex.

Also includes a thin **built-in image router** (`nic-image-gen`) that delegates to Cursor/Codex native tools and parks files under a brand-scoped artifact folder.

## Design principles

1. **Atomic** — one skill, one job
2. **Script-first** — deterministic steps live in `scripts/`
3. **Progressive disclosure** — keep `SKILL.md` lean; put detail in `references/` only when needed
4. **Dogfood first** — use daily before open-sourcing
5. **On-demand install** — document single-skill install; never push full-repo install as default
6. **No private leakage** — skills must not contain real home paths, usernames-as-paths, emails, tokens, API keys, or personal machine details; examples use placeholders only

## Initial skill candidates (priority)

1. **`nic-html-preview`** — serve local HTML over localhost; adaptive open (Cursor → browser MCP → system browser) *(v0.2)*
2. **`nic-image-gen`** — Cursor `GenerateImage` / Codex `$imagegen` router → `nic-skills-artifacts/image-gen/` *(v0.1)*
3. `nic-screenshot` — capture desktop / window / region when browser tools are insufficient
4. `nic-port-check` — find free ports / diagnose "port already in use"
5. `nic-gh-pr-ready` — status + diff + CI summary before opening a PR
6. `nic-env-doctor` — quick Node/Python/Git/tooling health check for a workspace

## Top pain points (dev)

1. Cursor browser rejects `file://` — previewing static HTML is awkward every time
2. Ad-hoc `python -m http.server` leaves zombie processes and wrong cwd
3. Screenshots / visual checks need a repeatable agent workflow
4. Port conflicts waste minutes across projects
5. PR prep is a repetitive git/gh ritual
