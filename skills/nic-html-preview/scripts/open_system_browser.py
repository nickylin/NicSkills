#!/usr/bin/env python3
"""Open an http(s) URL in the OS default browser. Last-resort preview fallback.

Prints one JSON line: {ok, url, method, error?}.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import webbrowser
from urllib.parse import urlparse


def validate_url(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return "only http(s) URLs are allowed (never file://)"
    if not parsed.netloc:
        return "url missing host"
    return None


def open_url(url: str) -> tuple[bool, str, str | None]:
    """Return (ok, method, error)."""
    platform = sys.platform

    try:
        if platform == "darwin":
            subprocess.run(["open", url], check=True)
            return True, "macos-open", None
        if platform.startswith("linux"):
            # Prefer xdg-open; fall back to webbrowser
            if subprocess.call(["which", "xdg-open"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                subprocess.run(["xdg-open", url], check=True)
                return True, "xdg-open", None
            opened = webbrowser.open(url)
            return (True, "webbrowser", None) if opened else (False, "webbrowser", "webbrowser.open returned False")
        if platform in {"win32", "cygwin"}:
            os.startfile(url)  # type: ignore[attr-defined]
            return True, "windows-startfile", None
        opened = webbrowser.open(url)
        return (True, "webbrowser", None) if opened else (False, "webbrowser", "webbrowser.open returned False")
    except Exception as exc:  # noqa: BLE001 — surface any OS open failure as JSON
        return False, "exception", str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="http(s) URL to open")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print plan without opening",
    )
    args = parser.parse_args()

    err = validate_url(args.url)
    if err:
        print(json.dumps({"ok": False, "url": args.url, "error": err}, ensure_ascii=False))
        return 1

    if args.dry_run:
        print(
            json.dumps(
                {
                    "ok": True,
                    "url": args.url,
                    "method": "dry-run",
                    "would_open": True,
                    "platform": sys.platform,
                },
                ensure_ascii=False,
            )
        )
        return 0

    ok, method, error = open_url(args.url)
    payload = {"ok": ok, "url": args.url, "method": method}
    if error:
        payload["error"] = error
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
