---
name: nic-html-preview
description: >-
  Preview a local .html file via localhost (never file://), then open it with an
  adaptive ladder: Cursor built-in browser → other browser MCP / IDE Simple
  Browser → OS system browser. Works with Cursor, Claude Code, Codex, and VS Code.
  Use when the user asks to preview/open/show local HTML, nic-html-preview,
  用内置浏览器打开, Simple Browser, 预览静态页, open in browser, or verify an
  HTML page visually in an Agent IDE.
version: 0.2.1
---

# nic-html-preview — Adaptive local HTML preview

Many Agent IDEs **reject or mishandle `file://`**. Always serve over `http://127.0.0.1`, then open with the best available viewer for the current host.

## Privacy (required)

- **Never** put real machine paths, home directories, usernames, emails, tokens, or API keys into this skill’s docs, examples, commit messages, or issue text.
- In `SKILL.md` / `examples/` use placeholders only: `${SKILL_DIR}`, `/ABS/PATH/to/page.html`, `http://127.0.0.1:PORT/page.html`.
- Runtime script JSON may include absolute `root` for the agent to work — **do not copy those paths back into skill source**.
- Prefer workspace-relative paths when talking to the user (e.g. `examples/demo.html`).
- Do not dump `os.environ`, credential files, or secret-bearing env values.

## Compatibility

| Platform | Support | Preferred open path |
|----------|---------|---------------------|
| **Cursor** | Full | MCP `cursor-ide-browser` → `browser_navigate` (`position: "side"`) |
| **Claude Code** | Adaptive | Browser MCP if connected → else system browser |
| **Codex** | Adaptive | Browser MCP if connected → else system browser |
| **VS Code / forks** | Adaptive | Simple Browser / preview command → else system browser |
| **Headless / CI** | URL-only | Serve + print URL; do not force a GUI unless asked |

## Goal & when to use

Preview a local `.html` page. Trigger on「打开看看」「预览这个 HTML」「用内置浏览器打开」「open this HTML in the browser」or `nic-html-preview`.

## Default behavior

- Serve the HTML file's **parent directory** (preferred port `8765`, auto-fallback if busy).
- **Never** navigate to `file://`.
- Prefer in-IDE / MCP browser; **fall back to system browser** when IDE tools are missing or fail.
- Non-interactive: if the user already named a path, serve and open without asking.
- Tell the user which open path was used (`cursor-ide-browser` / `browser-mcp` / `system-browser`).

## Workflow

Resolve `SKILL_DIR` as the directory containing this `SKILL.md`.

### 1. Resolve the HTML path

- Prefer the path the user named; else the workspace `.html` they are editing.
- Expand to an absolute path. Confirm the file exists.

### 2. Serve (required)

```bash
python3 "${SKILL_DIR}/scripts/serve_local_html.py" "/ABS/PATH/to/page.html"
```

- One JSON line: `url`, `root`, `port`, `pid`, `reused`.
- Always use the returned `url` (port may differ from `8765`).

### 3. Detect host (advisory)

```bash
python3 "${SKILL_DIR}/scripts/detect_host.py"
```

- Use `open_ladder` as a hint. **Live MCP / tool discovery beats `host_guess`.**

### 4. Open — adaptive ladder (try in order)

**Tier 1 — Cursor built-in browser** (when `cursor-ide-browser` MCP exists)

- `browser_navigate` with:
  - `url`: served `url`
  - `position`: `"side"` for casual preview; `"active"` if user asks to focus
  - `take_screenshot_afterwards`: `true` when verifying visuals
- For longer interaction: navigate → lock → act → unlock.
- Verify with snapshot/screenshot. If CSS/images 404, assets must live under the HTML parent dir.

**Tier 2 — Other browser MCP** (Claude Code / Codex / Cursor extension browsers)

- If any `browser_navigate` / equivalent MCP is available and connected, open the same `http` URL.
- If the tool errors with “not connected” / “server not found”, **do not retry endlessly** — go to Tier 3/4.

**Tier 3 — IDE Simple Browser / preview command**

- If the host exposes Simple Browser / “Preview” for http URLs, use that with the served URL.

**Tier 4 — System browser (required fallback)**

```bash
python3 "${SKILL_DIR}/scripts/open_system_browser.py" "http://127.0.0.1:PORT/page.html"
```

- macOS `open` / Linux `xdg-open` / Windows default handler.
- Use when higher tiers are unavailable **or** fail once.
- Report: `opened via system browser` + the URL.

### 5. Stop local server (only if asked)

- Kill the serve script's `pid` only when `reused: false` and you started it.

## Error handling

| Symptom | Fix |
|---------|-----|
| `file:// URLs are not allowed` | Serve first; never pass `file://` |
| `file not found` | Resolve path from workspace root |
| Styles/images 404 | Assets must be under HTML parent (server root) |
| Port conflict | Use returned `url` / port from serve script |
| Cursor MCP missing / not ready | Fall through ladder → system browser |
| Browser MCP “not connected” | Tier 4 system browser |
| CJK mojibake | Helper serves `charset=utf-8`; add `<meta charset="utf-8">` if needed |

## Do / Don't

| Do | Don't |
|----|--------|
| Use `http://127.0.0.1:<port>/file.html` | Pass `file:///...` to any browser tool |
| Fall back to system browser when IDE tools fail | Soft-fail with only “MCP unavailable” and stop |
| Say which tier opened the page | Assume every host has `cursor-ide-browser` |
| Re-run serve after move/rename | Hardcode port `8765` |
| Use path placeholders in skill source | Commit `/Users/...`, `~/.ssh`, tokens, or personal project paths |

## Common prompts → actions

- 「用内置浏览器打开」→ serve → Tier 1 if Cursor, else ladder → screenshot when possible
- 「预览这个 HTML」(Claude/Codex)→ serve → browser MCP or system browser
- 「刷新预览」→ same `url` again (server may `reused: true`)
- 「用系统浏览器打开」→ serve → Tier 4 directly
- 「停掉本地服务」→ kill serve `pid` when you started it

## Example

```bash
python3 "${SKILL_DIR}/scripts/serve_local_html.py" "/ABS/PATH/to/demo.html"
# → {"url":"http://127.0.0.1:8765/demo.html", ...}

python3 "${SKILL_DIR}/scripts/detect_host.py"
# → host_guess + open_ladder

# If no IDE browser MCP:
python3 "${SKILL_DIR}/scripts/open_system_browser.py" "http://127.0.0.1:8765/demo.html"
```
