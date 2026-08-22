---
name: nic-visual-report
description: >-
  Turn the current conversation (or user-provided notes) into a visual report:
  test reports, solution results, technical comparisons, decision briefs, or
  session summaries. Output HTML one-pager (default) or Cursor Canvas
  (.canvas.tsx). Use when the user wants 可视化报告, 对话总结可视化,
  测试报告, 方案对比, 技术方案对比, 结果汇报, nic-visual-report, visual
  report, HTML report, or canvas report. Prefer this over dumping long markdown
  tables when a standalone report artifact is needed. Report language follows the
  user's conversation language unless they specify otherwise. Do not use for pure
  icon/diagram-only asks (nic-visual-code) or AI photoreal images (nic-image-gen).
version: 0.1.1
---

# nic-visual-report — Visualize conversation into a report

Consolidate scattered chat findings into **one visual report artifact**. Instruction-only. Does not call image-generation APIs.

## Modes (user choice)

| Mode | When | Deliverable |
|------|------|-------------|
| **`html`** (default) | Shareable page, archive, preview in browser | `nic-skills-artifacts/visual-report/html/*.html` |
| **`canvas`** | Interactive view beside chat in Cursor | `.canvas.tsx` under the host Canvas directory (see below) |

- User says `html` / `网页` / `页面` → HTML.
- User says `canvas` / `画布` → Canvas.
- Unspecified → **HTML**.

## Report types (pick one structure)

| Type | Use when | Core sections |
|------|----------|---------------|
| `test-report` | 测试报告 / QA results | Summary · Environment · Cases · Pass/Fail · Issues · Next |
| `solution-result` | 方案结果 / 落地结论 | Goal · What shipped · Evidence · Risks · Follow-ups |
| `tech-compare` | 技术方案对比 | Criteria · Options · Comparison table · Recommendation |
| `session-brief` | 对话总结 / 决策纪要 | Context · Decisions · Open questions · Action items |
| `custom` | User names a structure | Follow user outline |

Infer type from the conversation; if ambiguous, ask once or default to `session-brief`.

## Related skills (optional compose)

| Need | Skill |
|------|--------|
| Extra Mermaid / SVG / icon blocks inside HTML | [`nic-visual-code`](../nic-visual-code/) |
| Plain-language picture explainer (not a report) | [`nic-eli5`](../nic-eli5/) |
| Teach via a strength they already know well | [`nic-like-you-know`](../nic-like-you-know/) |
| Preview HTML in browser | [`nic-html-preview`](../nic-html-preview/) |
| AI atmosphere bitmap (rare) | [`nic-image-gen`](../nic-image-gen/) |
| Canvas SDK rules | Cursor built-in **canvas** skill — **read it before writing `.canvas.tsx`** |

Composition is optional. This skill can generate a complete HTML report alone (inline SVG/simple CSS diagrams OK).

## Privacy (required)

- Never put secrets, tokens, API keys, private home paths, or credentials into the report.
- Prefer workspace-relative paths in the report body.
- Do not invent metrics or test results — only use facts from the conversation / user files. If data is missing, omit the section or mark a localized “unknown” label (do not fabricate).

## Language (required)

Match the **user's conversation language** for the report UI and prose.

1. **Detect** from the latest user messages / dominant language in this thread (not from the skill author’s language).
2. **Honor explicit overrides** — e.g. `用英文输出` / `in Chinese` / `中英双语`.
3. **Default**
   - Mostly Chinese chat → Chinese headings, summary, tables, footer.
   - Mostly English chat → English throughout.
   - Mixed thread → follow the **latest user instruction**; if still mixed, use the language of the request that triggered this skill.
4. **Keep as-is (do not translate)** — skill names (`nic-visual-report`), code identifiers, file paths, product names (Cursor, GitHub), and user-quoted proper nouns.
5. **Missing data labels** — localize too (`未知` / `Unknown` / etc.), never invent facts.
6. **HTML** — set `<html lang="zh-CN">` or `lang="en">` (or other) to match the chosen language.

## Encoding & text (required)

- UTF-8; HTML must include `<meta charset="utf-8">`.
- CJK font stack when Chinese is present: `"PingFang SC", "Noto Sans SC", "Microsoft YaHei", …`
- Prefer safe punctuation in SVG labels (`-` `/` `to`) to avoid mojibake.
- No emoji decoration unless the user asks.

## Output locations

**HTML**

```text
nic-skills-artifacts/visual-report/html/
```

- `mkdir -p` if needed.
- Filename: `YYYYMMDD-<slug>-report.html` (or user-provided name).
- Ensure host `.gitignore` contains `nic-skills-artifacts/` when appropriate.

**Canvas**

- Write exactly one `*.canvas.tsx` to the Cursor canvases directory for this workspace:
  - Placeholder: `${CURSOR_PROJECTS}/<workspace-id>/canvases/<slug>-report.canvas.tsx`
  - Do **not** invent helper files; import only from `cursor/canvas`.
- Follow the Canvas skill: embed data inline, no `fetch`, no empty slots, no slop (gradients / emoji / box-shadow spam).
- When telling the user about the canvas, link the `.canvas.tsx` file path in markdown.

## Workflow

1. **Collect** — From the current conversation (and any paths the user cited), extract goals, facts, options, numbers, decisions, risks, actions. Do not pad with guesses.
2. **Choose** — `mode` (html/canvas) + `report type` + **language** (follow user context) + theme (`dark-dev` default for HTML; Canvas uses host theme tokens).
3. **Outline** — Build a tight section list (see types above), in the chosen language. Drop empty sections.
4. **Visualize** — Prefer:
   - Summary strip / KPI chips (only real numbers)
   - Comparison tables
   - Status lists (pass / fail / blocked)
   - One diagram when it clarifies (flow / architecture / decision) via inline SVG or `nic-visual-code`
5. **Write artifact** — HTML file or Canvas file.
6. **Preview (HTML)** — Offer / run `nic-html-preview` when useful.
7. **Report back** — mode + type + language + relative/link path + 1–3 sentence verbal summary in the same language (do not paste the whole report into chat).

## HTML defaults

- Theme: `dark-dev` unless user asks `light-clean` / `mono` / `brand`.
- Readable single page; mobile-friendly stacking.
- CSS variables: `--bg`, `--fg`, `--accent`, `--muted`, `--ok`, `--warn`, `--bad`.
- Include a small footer: report type, generated for NicSkills visual-report, no secrets.

## Canvas defaults

- Self-contained analytical layout: title, summary, tables/charts as needed.
- Use `cursor/canvas` components; colors from `useHostTheme()`.
- Never render placeholder “TODO” / “No data” blocks — omit instead.

## Quality bar

- One primary narrative: reader understands outcome in under a minute.
- Visual hierarchy: verdict / recommendation first.
- Tables over walls of prose for comparisons.
- Diagrams only when they reduce confusion.
- If embedding samples into GitHub README later: icon `128`, diagram `640`, banner `720` via `<img width>`.

## Error handling

| Symptom | Fix |
|---------|-----|
| Not enough facts in chat | Ask for the missing piece or generate a brief with Unknown fields — do not invent |
| User wants only a small SVG icon | Hand off to `nic-visual-code` |
| User wants AI photo cover | Optional `nic-image-gen`; do not block the report |
| Canvas type/SDK errors | Re-read Canvas skill + SDK `.d.ts`; fix imports |

## Do / Don't

| Do | Don't |
|----|--------|
| Consolidate the conversation into one artifact | Dump a huge markdown table in chat as the only deliverable |
| Default to HTML; honor canvas when asked | Put `.canvas.tsx` under random repo folders |
| Write the report in the user's language | Default to English when the user spoke Chinese (or vice versa) |
| Cite only real conversation facts | Fabricate pass rates or benchmark numbers |
| Optionally compose visual-code / html-preview | Hard-require other skills to function |

## Examples

**HTML test report**

User: 把这次测试结果做成可视化报告

1. mode=`html`, type=`test-report`  
2. Write `nic-skills-artifacts/visual-report/html/<date>-test-report.html`  
3. Preview with `nic-html-preview` if useful  

**Canvas comparison**

User: 用 canvas 对比刚才两个技术方案

1. mode=`canvas`, type=`tech-compare`  
2. Read Canvas skill → write `${CURSOR_PROJECTS}/…/canvases/<slug>-tech-compare.canvas.tsx`  
3. Link the canvas path for the user to open beside chat  

Trigger phrases: `可视化报告` / `方案对比报告` / `对话总结做成页面` / `canvas 报告` / `html 报告`.
