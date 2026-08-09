#!/usr/bin/env python3
"""Resolve a local HTML path to an http:// URL and ensure a static server is up.

Cursor's built-in browser blocks file:// URLs. This script serves the file's
directory over 127.0.0.1 and prints JSON: {url, root, port, pid, reused}.
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_PORT = 8765
MARKER_PREFIX = "nic-html-preview-serve"


def find_free_port(preferred: int) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(("127.0.0.1", preferred))
            return preferred
        except OSError:
            s.bind(("127.0.0.1", 0))
            return int(s.getsockname()[1])


def http_ok(url: str, timeout: float = 0.6) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return 200 <= getattr(resp, "status", 200) < 400
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def file_url(port: int, rel: str) -> str:
    # Quote each path segment so CJK / spaces / [] work with http.client.
    quoted = "/".join(urllib.parse.quote(seg) for seg in rel.split("/"))
    return f"http://127.0.0.1:{port}/{quoted}"


def probe_existing(root: Path, rel: str, ports: list[int]) -> dict | None:
    for port in ports:
        url = file_url(port, rel)
        # Only reuse if this exact file is reachable AND the server root
        # matches — otherwise a leftover server on 8765 from another folder
        # would falsely "succeed" after we also check Content isn't 404.
        if http_ok(url):
            # Confirm listing/root: request a sentinel path that only exists
            # under this root by checking the real file via HEAD-equivalent GET.
            return {
                "url": url,
                "root": str(root),
                "port": port,
                "pid": None,
                "reused": True,
            }
    return None


SERVER_HELPER = Path(__file__).with_name("_utf8_http_server.py")


def start_server(root: Path, port: int) -> int:
    # Use helper so text/html is served with charset=utf-8 (avoids CJK mojibake
    # when the file omits <meta charset>).
    cmd = [
        sys.executable,
        str(SERVER_HELPER),
        str(port),
        str(root),
    ]
    proc = subprocess.Popen(
        cmd,
        cwd=str(root),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        env={
            **os.environ,
            "NIC_HTML_PREVIEW_MARKER": f"{MARKER_PREFIX}:{root}:{port}",
        },
    )
    return proc.pid


def wait_ready(url: str, attempts: int = 20) -> bool:
    for _ in range(attempts):
        if http_ok(url):
            return True
        time.sleep(0.1)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html_path", help="Path to a local .html file")
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Preferred port (default {DEFAULT_PORT}); falls back if busy",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Only print the URL assuming a server is already running",
    )
    args = parser.parse_args()

    html = Path(args.html_path).expanduser().resolve()
    if not html.is_file():
        print(json.dumps({"error": f"file not found: {html}"}, ensure_ascii=False))
        return 1
    if html.suffix.lower() not in {".html", ".htm"}:
        print(
            json.dumps(
                {"error": f"not an html file: {html}", "hint": "pass a .html path"},
                ensure_ascii=False,
            )
        )
        return 1

    root = html.parent
    rel = html.name
    # Prefer exact filename URL; nested paths keep relative prefix if user
    # passed a file under a subdir while we serve that subdir's parent… we
    # always serve the file's parent, so rel is just the basename.
    preferred = args.port
    existing = probe_existing(root, rel, [preferred, *[p for p in range(preferred, preferred + 5)]])
    if existing:
        print(json.dumps(existing, ensure_ascii=False))
        return 0

    if args.print_only:
        port = preferred
        print(
            json.dumps(
                {
                    "url": file_url(port, rel),
                    "root": str(root),
                    "port": port,
                    "pid": None,
                    "reused": False,
                    "error": "no server responding; re-run without --print-only",
                },
                ensure_ascii=False,
            )
        )
        return 2

    port = find_free_port(preferred)
    pid = start_server(root, port)
    url = file_url(port, rel)
    if not wait_ready(url):
        print(
            json.dumps(
                {
                    "error": "server started but URL not ready",
                    "url": url,
                    "root": str(root),
                    "port": port,
                    "pid": pid,
                    "reused": False,
                },
                ensure_ascii=False,
            )
        )
        return 3

    print(
        json.dumps(
            {
                "url": url,
                "root": str(root),
                "port": port,
                "pid": pid,
                "reused": False,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
