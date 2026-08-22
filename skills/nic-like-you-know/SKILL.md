---
name: nic-like-you-know
description: >-
  Explain a new topic by mapping it onto a field the user already knows well
  (Android, law, cooking, basketball, or any strength). Optional visual skin
  (pets, anime cast, familiar characters). Default HTML page; Markdown if the
  user wants text only. Use when the user types /nic-like-you-know, 同比讲解,
  用我熟悉的, 擅长领域, 用 Android 讲, like I know, explain via, 类比讲解, 从我会的说,
  or asks to learn X in terms of Y. Do not use for "knows nothing" picture
  books (nic-eli5) or conversation reports (nic-visual-report).
version: 0.1.0
---

# nic-like-you-know — Teach via what they already know

Explain the **new** thing through a **strength** — a field the user already knows well. Instruction-only.

This is not eli5. eli5 assumes they know nothing and invents a picture language. This skill assumes they are already fluent in something — build a counterpart map, walk the new topic through that map, and say where the analogy **breaks**.

Do not call this axis 家乡 / home / hometown. The label is **擅长领域** (EN: **Strength**).

## Two axes (do not mix them up)

| Axis | What it is | Required? |
|------|------------|-----------|
| **Strength** (擅长领域) | The field they already know well (Android, courtroom, kitchen, soccer, WeChat…) | Yes — infer, ask once, or fall back |
| **Skin** | How to draw/narrate it (their cat, One Piece crew, office comics) | Optional — never invent a forced cute cast |

Strength is the **conceptual mapping**. Skin is costume only. A cat can act out `Activity` vs `ViewController`; the cat must not replace the map.

## Inputs

Parse from the latest user message + this thread:

1. **Topic** — what they are learning (required).
2. **Strength** — what they already know well.
3. **Skin** — optional cast / drawing style.
4. **Mode** — `html` (default) or `md` when they say 只要文字 / Markdown / 对照表就行.

If strength is missing:

1. Infer from the conversation (they said they are an Android engineer, a chef, a litigator…).
2. If still unclear, **ask once**.
3. If they still do not name one, use **shared commons** (kitchen, traffic, school, mailbox) — not a random niche fandom.

Any strength is valid: tech, professional, hobby, or everyday commons. Do not refuse non-tech.

## Related skills

| Need | Skill |
|------|--------|
| They know nothing; big pictures, few words | [`nic-eli5`](../nic-eli5/) |
| Preview the HTML page | [`nic-html-preview`](../nic-html-preview/) |
| Extra SVG / Mermaid blocks | [`nic-visual-code`](../nic-visual-code/) |
| Conversation → report | [`nic-visual-report`](../nic-visual-report/) |

## Privacy / language / encoding

- No secrets, tokens, machine home paths, or credentials in the artifact.
- Match the **user's conversation language** (same rules as `nic-visual-report`). Keep skill names, APIs, and proper nouns as-is.
- UTF-8. HTML: `<meta charset="utf-8">`. Chinese present → `"PingFang SC", "Noto Sans SC", "Microsoft YaHei"` first.
- Prefer safe punctuation in SVG labels (`-` `/` `to`). No emoji unless they ask.
- Localized axis labels: 擅长领域 / 新题 (not 家乡). English: Strength / New.

## Output locations

```text
nic-skills-artifacts/like-you-know/html/
nic-skills-artifacts/like-you-know/md/
```

- `mkdir -p` if needed.
- Filename: `YYYYMMDD-<slug>.html` or `.md` (or a name they give).
- Never write into this skill's own directory.
- Ensure host `.gitignore` contains `nic-skills-artifacts/` when appropriate.

## Artifact shape

Every deliverable has these four blocks (names localize):

1. **Strength / New** — one line each. Chinese: **擅长领域 / 新题**. Never 家乡.
2. **Counterpart map** — 5–12 rows: strength term → new term → one-line "same job".
3. **Walk** — 3–7 beats. Each beat uses an object from their strength to move one new idea.
4. **Breaks** — 2–5 **false friends**. Where the analogy lies or stops. This block is required.

Optional last line: **one next thing to try** (a command, a screen, a drill) — not a syllabus.

### HTML (default)

- One self-contained page. Inline SVG for the map and 1–3 beat pictures.
- Invent the picture language **from their strength** (Android tiles, mise en place, courtroom benches). If they named a skin, those characters act out the same map.
- Do not clone a canned card-grid, a previous page, or leftover eli5 art.
- Theme: `dark-dev` unless they ask `light-clean` / `mono` / `brand`.
- CSS variables: `--bg`, `--fg`, `--accent`, `--muted`, `--ok`, `--warn`.
- Footer: `nic-like-you-know` + strength + topic. No secrets.
- After writing, offer / run `nic-html-preview`.

### Markdown (`md`)

Same four blocks as tight Markdown. A table for the map. No HTML chrome. Do not dump the whole page into chat after writing the file.

## Quality bar

- The map must be **operational** (same job), not punny word-match.
- Prefer fewer, sharper counterparts over a 30-row glossary.
- **Breaks** must be specific ("Intents carry extras; SwiftUI navigation is a stack of values — not a mailbox").
- Skin never overrides accuracy. If a character gag fights the map, drop the gag.
- One primary idea per beat. Reader should feel "I already knew this shape."

## Workflow

1. Resolve topic / strength / skin / mode / language.
2. Draft the counterpart map silently; drop weak rows.
3. Write the artifact under `nic-skills-artifacts/like-you-know/`.
4. Preview HTML when useful.
5. Reply with: mode + strength + topic + relative path + 2–4 sentence verbal hook in the user's language. Do not paste the whole artifact.

## Do / Don't

| Do | Don't |
|----|--------|
| Map from a named strength | Pretend they know nothing (that's `nic-eli5`) |
| Call the axis 擅长领域 / Strength | Call it 家乡 / hometown / home |
| Call out false friends | Force a 1:1 that is not true |
| Honor optional skin | Invent a pet/anime cast they did not ask for |
| Default HTML; honor Markdown | Ship only a chat essay |
| Accept any field they know well | Refuse cooking / law / sports as "out of scope" |

## Examples

**Tech strength**

User: `/nic-like-you-know` 我是 Android，讲 SwiftUI 导航

1. strength=`Android` · topic=`SwiftUI navigation` · mode=`html` · no skin  
2. Map: Activity / Intent / back stack → View / NavigationStack / value  
3. Write `nic-skills-artifacts/like-you-know/html/<date>-swiftui-nav.html`  
4. Breaks: Intent extras vs typed path values; no `onActivityResult` twin  

**Skin + non-tech strength**

User: 用我厨房的思路讲 Git，画成我的猫和柯基

1. strength=`kitchen` · skin=`cat + corgi` · topic=`Git` · mode=`html`  
2. Map: mise en place → working tree; tasting spoon → commit; pass dish → push  
3. Characters act out the map; breaks: rebase is not "replating the same steak"  

**Text only**

User: 只要 Markdown 对照表，用诉讼流程讲 HTTP

1. mode=`md` · strength=`litigation` · topic=`HTTP`  
2. Write `nic-skills-artifacts/like-you-know/md/<date>-http-via-court.md`  

Trigger phrases: `/nic-like-you-know` / `同比讲解` / `用我熟悉的` / `擅长领域` / `like I know` / `用 Android 讲` / `类比` / `宠物讲解` / `动漫角色来讲`.
