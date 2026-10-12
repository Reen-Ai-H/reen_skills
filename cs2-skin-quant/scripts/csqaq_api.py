#!/usr/bin/env python3
"""Small read-only client for the official CSQAQ API.

The token is never accepted on the command line and is never printed.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


API_BASE = "https://api.csqaq.com/api/v1"
ENV_NAME = "CS2_CSQAQ_API_TOKEN"
SECRET_FILE = Path.home() / ".config" / "cs2-skin-quant" / "secrets.env"


def load_token() -> str:
    token = os.environ.get(ENV_NAME, "").strip()
    if token:
        return token

    if not SECRET_FILE.is_file():
        raise RuntimeError(
            f"Missing {ENV_NAME}; configure {SECRET_FILE} with file mode 0600"
        )

    mode = stat.S_IMODE(SECRET_FILE.stat().st_mode)
    if mode & 0o077:
        raise RuntimeError(f"Refusing to read {SECRET_FILE}: expected mode 0600")

    for line in SECRET_FILE.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        if separator and key.strip() == ENV_NAME and value.strip():
            return value.strip()
    raise RuntimeError(f"{ENV_NAME} is not present in {SECRET_FILE}")


def get_json(path: str, query: list[str]) -> tuple[int, object]:
    normalized = "/" + path.lstrip("/")
    if not normalized.startswith("/") or ".." in normalized:
        raise RuntimeError("Invalid API path")

    pairs: list[tuple[str, str]] = []
    for item in query:
        key, separator, value = item.partition("=")
        if not separator or not key:
            raise RuntimeError(f"Invalid query value: {item!r}; expected key=value")
        pairs.append((key, value))

    url = API_BASE + normalized
    if pairs:
        url += "?" + urllib.parse.urlencode(pairs)
    request = urllib.request.Request(
        url,
        headers={"ApiToken": load_token(), "Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as exc:
        try:
            body = json.load(exc)
        except Exception:
            body = {"code": exc.code, "msg": "HTTP request failed"}
        return exc.code, body


def main() -> int:
    parser = argparse.ArgumentParser(description="Read from the official CSQAQ API")
    parser.add_argument(
        "--health",
        action="store_true",
        help="check authentication using /current_data without printing response data",
    )
    parser.add_argument("--path", help="GET path relative to /api/v1")
    parser.add_argument(
        "--query", action="append", default=[], metavar="KEY=VALUE", help="query value"
    )
    args = parser.parse_args()

    if not args.health and not args.path:
        parser.error("choose --health or --path")

    try:
        status, payload = get_json("/current_data" if args.health else args.path, args.query)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1

    if args.health:
        code = payload.get("code") if isinstance(payload, dict) else None
        message = None
        if isinstance(payload, dict):
            message = payload.get("msg", payload.get("message"))
        ok = status == 200 and (code in (None, 200))
        print(
            json.dumps(
                {"ok": ok, "http_status": status, "code": code, "message": message},
                ensure_ascii=False,
            )
        )
        return 0 if ok else 1

    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    return 0 if status == 200 else 1


if __name__ == "__main__":
    sys.exit(main())
