---
name: nic-image-gen
description: >-
  Generate raster images via host built-in tools only: Cursor GenerateImage or
  Codex built-in $imagegen / image_gen. Saves outputs under
  nic-skills-artifacts/image-gen/ (brand-scoped; avoids generic images/output folders).
  Use when the user asks to generate/create/draw an image, 生图, 生成图片,
  nic-image-gen, icon/illustration/banner mockup as a bitmap file in the workspace.
  Do not use for Mermaid/SVG/HTML code visuals or “不用生图API” requests — hand
  off to nic-visual-code. Do not invent third-party image APIs (not in v0.1).
version: 0.1.2
---

# nic-image-gen — Built-in image generation router

Cross-host **routing + workspace placement** for AI bitmap images. Instruction-only: no scripts. Does **not** reimplement Codex `$imagegen` or call third-party APIs in v0.1.

## Related skill

| Need | Skill |
|------|--------|
| AI bitmap / 宣传插画 / atmosphere | **this skill** |
| Editable Mermaid / SVG / HTML（不用生图 API） | [`nic-visual-code`](../nic-visual-code/) |

## Privacy (required)

- Never put real machine paths, home directories, usernames, emails, tokens, or API keys into this skill’s docs or examples.
- Use placeholders: `${WORKSPACE}`, `$CODEX_HOME/generated_images/…`.
- Prefer workspace-relative paths when speaking to the user (e.g. `nic-skills-artifacts/image-gen/…`).

## Compatibility

| Platform | Support | Engine |
|----------|---------|--------|
| **Cursor** | Full | Built-in `GenerateImage` tool |
| **Codex** | Full | Built-in `$imagegen` / `image_gen` tool (system skill) |
| **Claude Code / others** | Unsupported (v0.1) | No third-party API fallback — explain and stop |
| **API / MiniMax / CLI keys** | Out of scope (v0.1) | Do not invent |

## Output directory (required)

Always place final assets under the **current workspace**:

```text
nic-skills-artifacts/image-gen/
```

- Brand-scoped on purpose — **do not** use generic `images/`, `output/`, `assets/`, or `generated/`.
- Create the folders with a normal `mkdir` if missing.
- Never write generated binaries into this skill’s directory.
- Optionally ensure the host project `.gitignore` contains `nic-skills-artifacts/` (add only that line if the file exists and the pattern is missing).

## Workflow

1. **Ensure output dir** — `mkdir -p nic-skills-artifacts/image-gen` under the workspace.
2. **Generate with the host built-in tool**
   - **Cursor:** use `GenerateImage`. Prefer a clear `filename` (no directory path in the filename arg).
   - **Codex:** use built-in `$imagegen` / `image_gen`. Do not copy or modify Codex system skill files. Prefer built-in tool; do not silently switch to Codex CLI / `OPENAI_API_KEY` unless the user explicitly asks in Codex’s own flow.
   - **Other hosts:** stop — unsupported in v0.1.
3. **Place into workspace** — move or copy the result into `nic-skills-artifacts/image-gen/`, using a descriptive name (timestamp prefix optional). Prefer **copy** when the source lives under `$CODEX_HOME/…` cache.
4. **Report** — engine used + workspace-relative path.

## Prompting tips (short)

- Subject, composition, style, lighting, and what to avoid.
- Aspect: mention `1:1`, `16:9`, `9:16`, etc. when the tool supports it.
- One clear deliverable per call; batch = multiple calls.

## Error handling

| Symptom | Fix |
|---------|-----|
| No GenerateImage / no image_gen | Stop — unsupported host in v0.1 |
| Codex only offers CLI key path | Ask user; do not auto-enable API fallback from this skill |
| Source file missing after gen | Re-check host output location; do not invent paths |

## Do / Don't

| Do | Don't |
|----|--------|
| Use `nic-skills-artifacts/image-gen/` | Dump into `images/` or `output/` |
| Prefer built-in Cursor/Codex tools | Reimplement Codex `$imagegen` or add API scripts |
| Report engine + relative path | Commit secrets or absolute home paths into docs |
| Copy from Codex cache when unsure | Delete the user’s Codex cache without asking |

## Example

User: 生成一张深色背景的 NicSkills 宣传图

1. `mkdir -p nic-skills-artifacts/image-gen`
2. Cursor → `GenerateImage` **or** Codex → `image_gen`
3. Place file at `nic-skills-artifacts/image-gen/nicskills-promo.png`
4. Reply with that relative path
