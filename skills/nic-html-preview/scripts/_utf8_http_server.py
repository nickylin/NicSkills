#!/usr/bin/env python3
"""Tiny static server: text/* responses always include charset=utf-8."""

from __future__ import annotations

import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class Utf8Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **getattr(SimpleHTTPRequestHandler, "extensions_map", {}),
        ".html": "text/html; charset=utf-8",
        ".htm": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".mjs": "text/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".txt": "text/plain; charset=utf-8",
        ".svg": "image/svg+xml; charset=utf-8",
    }

    def end_headers(self) -> None:
        ctype = self.headers.get("Content-Type") if hasattr(self, "headers") else None
        # SimpleHTTPRequestHandler sets Content-Type before end_headers via send_header.
        super().end_headers()


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: _utf8_http_server.py <port> <directory>", file=sys.stderr)
        return 2
    port = int(sys.argv[1])
    root = Path(sys.argv[2]).resolve()
    handler = partial(Utf8Handler, directory=str(root))
    with ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        httpd.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
