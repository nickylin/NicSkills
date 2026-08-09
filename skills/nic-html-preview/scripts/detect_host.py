#!/usr/bin/env python3
"""Guess the host Agent / IDE and print an open strategy ladder as JSON.

This is advisory for the agent. Prefer live MCP tool discovery over this guess.
"""

from __future__ import annotations

import json
import os
from collections.abc import Mapping


def _flag(env: Mapping[str, str], *keys: str) -> bool:
    """True if any key is set. Never return or log values (may contain secrets/paths)."""
    return any(bool(env.get(k)) for k in keys)


def guess_host() -> tuple[str, list[str]]:
    hints: list[str] = []
    env = os.environ
    term = env.get("TERM_PROGRAM", "").lower()

    # Presence-only checks — never echo env values (paths/tokens).
    # Cursor-specific signals
    if _flag(env, "CURSOR_TRACE_ID", "CURSOR_AGENT") or "cursor" in term:
        hints.append("cursor-env")

    # VS Code family (Cursor also sets some of these)
    if _flag(env, "VSCODE_PID", "VSCODE_CWD") or term == "vscode":
        hints.append("vscode-family")

    # Claude Code heuristics (env names vary by version; ignore API key envs)
    if _flag(env, "CLAUDE_CODE", "CLAUDECODE"):
        hints.append("claude-code-env")
    if "claude" in term:
        hints.append("term-program-claude")

    # Codex — presence only; CODEX_HOME may be a filesystem path
    if _flag(env, "CODEX_HOME", "CODEX_SHELL") or "codex" in term:
        hints.append("codex-env")

    if "cursor-env" in hints:
        return "cursor", hints
    if "claude-code-env" in hints or "term-program-claude" in hints:
        return "claude-code", hints
    if "codex-env" in hints:
        return "codex", hints
    if "vscode-family" in hints:
        return "vscode", hints
    return "unknown", hints


def ladder_for(host: str) -> list[dict]:
    """Ordered open strategies: try earlier tiers first."""
    common_tail = [
        {
            "tier": 3,
            "id": "ide-simple-browser",
            "platforms": ["vscode", "cursor", "claude-code"],
            "how": "If the host exposes a Simple Browser / preview command, open the http URL there.",
        },
        {
            "tier": 4,
            "id": "system-browser",
            "platforms": ["all"],
            "how": "Run open_system_browser.py with the http URL (macOS open / Linux xdg-open / Windows start).",
        },
    ]

    if host == "cursor":
        return [
            {
                "tier": 1,
                "id": "cursor-ide-browser",
                "platforms": ["cursor"],
                "how": "MCP cursor-ide-browser → browser_navigate(url, position=side).",
            },
            {
                "tier": 2,
                "id": "other-browser-mcp",
                "platforms": ["cursor", "claude-code", "codex"],
                "how": "Any available browser_* MCP (e.g. browsermcp) → navigate to url.",
            },
            *common_tail,
        ]
    if host in {"claude-code", "codex", "vscode"}:
        return [
            {
                "tier": 1,
                "id": "browser-mcp",
                "platforms": ["claude-code", "codex", "vscode", "cursor"],
                "how": "If a browser MCP is connected, navigate to the http URL.",
            },
            {
                "tier": 2,
                "id": "cursor-ide-browser",
                "platforms": ["cursor"],
                "how": "Only if cursor-ide-browser MCP is actually available.",
            },
            *common_tail,
        ]
    return [
        {
            "tier": 1,
            "id": "browser-mcp-or-ide",
            "platforms": ["all"],
            "how": "Discover browser MCP / IDE preview tools; use http URL (never file://).",
        },
        {
            "tier": 2,
            "id": "system-browser",
            "platforms": ["all"],
            "how": "Run open_system_browser.py with the http URL.",
        },
    ]


def compatibility() -> list[dict]:
    return [
        {
            "platform": "Cursor",
            "support": "full",
            "notes": "Preferred: cursor-ide-browser side panel + screenshot/snapshot.",
        },
        {
            "platform": "Claude Code",
            "support": "adaptive",
            "notes": "Use browser MCP if present; else system browser via open_system_browser.py.",
        },
        {
            "platform": "Codex",
            "support": "adaptive",
            "notes": "Same ladder: browser MCP → system browser. Always serve via localhost first.",
        },
        {
            "platform": "VS Code / other IDE",
            "support": "adaptive",
            "notes": "Simple Browser or system browser; never file:// for preview automation.",
        },
        {
            "platform": "Headless / CI",
            "support": "url-only",
            "notes": "Serve and print URL; skip GUI open unless --force-system.",
        },
    ]


def main() -> int:
    host, hints = guess_host()
    print(
        json.dumps(
            {
                "host_guess": host,
                "hints": hints,
                "open_ladder": ladder_for(host),
                "compatibility": compatibility(),
                "rule": "Live MCP discovery beats host_guess. Never open file://.",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
