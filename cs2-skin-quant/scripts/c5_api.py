#!/usr/bin/env python3
"""Read-only helpers for the official C5GAME OpenAPI.

The C5 app-key is never accepted on the command line and is never printed.
This client intentionally exposes only read-only endpoints used by the
screening workflow; buying, listing, repricing, and delivery stay manual.
"""

from __future__ import annotations

import argparse
import gzip
import importlib
import json
import os
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


API_BASE = "https://openapi.c5game.com"
ENV_NAME = "CS2_C5_API_KEY"
SECRET_FILE = Path.home() / ".config" / "cs2-skin-quant" / "secrets.env"
COMMON_HEADERS = {
    "Accept": "application/json",
    # Required by the current official OpenAPI notice (June 17 update).
    "Accept-Encoding": "gzip, br, zstd, deflate",
    "User-Agent": "cs2-skin-quant/1.0 (read-only)",
}


def load_key() -> str:
    key = os.environ.get(ENV_NAME, "").strip()
    if key:
        return key

    if not SECRET_FILE.is_file():
        raise RuntimeError(
            f"Missing {ENV_NAME}; configure {SECRET_FILE} with file mode 0600"
        )
    mode = stat.S_IMODE(SECRET_FILE.stat().st_mode)
    if mode & 0o077:
        raise RuntimeError(f"Refusing to read {SECRET_FILE}: expected mode 0600")

    for line in SECRET_FILE.read_text(encoding="utf-8").splitlines():
        name, separator, value = line.partition("=")
        if separator and name.strip() == ENV_NAME and value.strip():
            return value.strip()
    raise RuntimeError(f"{ENV_NAME} is not present in {SECRET_FILE}")


def decode_body(raw: bytes, encoding: str) -> bytes:
    encoding = encoding.lower().strip()
    if not encoding or encoding == "identity":
        return raw
    if encoding == "gzip":
        return gzip.decompress(raw)
    if encoding == "br":
        try:
            return importlib.import_module("brotli").decompress(raw)
        except ImportError as exc:
            raise RuntimeError("C5 returned Brotli; install brotli to decode it") from exc
    if encoding == "zstd":
        try:
            return importlib.import_module("zstandard").ZstdDecompressor().decompress(raw)
        except ImportError as exc:
            raise RuntimeError("C5 returned Zstandard; install zstandard to decode it") from exc
    if encoding == "deflate":
        import zlib

        return zlib.decompress(raw)
    raise RuntimeError(f"Unsupported C5 response encoding: {encoding}")


def request_json(method: str, path: str, *, query: dict[str, Any] | None = None, body: Any = None) -> tuple[int, Any]:
    normalized = "/" + path.lstrip("/")
    if ".." in normalized:
        raise RuntimeError("Invalid C5 API path")
    params = {"app-key": load_key()}
    if query:
        params.update({k: v for k, v in query.items() if v is not None})
    url = API_BASE + normalized + "?" + urllib.parse.urlencode(params, doseq=True)
    headers = dict(COMMON_HEADERS)
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            raw = decode_body(response.read(), response.headers.get("Content-Encoding", ""))
            return response.status, json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        try:
            payload = json.loads(decode_body(raw, exc.headers.get("Content-Encoding", "")).decode("utf-8"))
        except Exception:
            payload = {"success": False, "errorCode": exc.code, "errorMsg": "HTTP request failed"}
        return exc.code, payload


def print_health() -> int:
    status, payload = request_json("GET", "/merchant/account/v1/balance")
    if not isinstance(payload, dict):
        print(json.dumps({"ok": False, "http_status": status}, ensure_ascii=False))
        return 1
    ok = status == 200 and payload.get("success") is True
    print(
        json.dumps(
            {
                "ok": ok,
                "http_status": status,
                "success": payload.get("success"),
                "error_code": payload.get("errorCode"),
                "message": payload.get("errorMsg"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Read from official C5GAME OpenAPI")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("health", help="validate app-key with account balance endpoint")
    stats = sub.add_parser("stats", help="query C5 stats for up to 100 CS2 market names")
    stats.add_argument("market_hash_names", nargs="+", metavar="MARKET_HASH_NAME")
    max_buy = sub.add_parser("max-buy", help="query C5 highest buy price")
    max_buy.add_argument("item_id", type=int)
    max_buy.add_argument("--style-id", type=int)
    args = parser.parse_args()

    try:
        if args.command == "health":
            return print_health()
        if args.command == "stats":
            if len(args.market_hash_names) > 100:
                parser.error("stats accepts at most 100 market names")
            status, payload = request_json(
                "POST",
                "/merchant/market/v2/item/stat/hash/name",
                body={"appId": 730, "marketHashNames": args.market_hash_names},
            )
        else:
            status, payload = request_json(
                "GET",
                "/merchant/purchase/v1/max-price",
                query={"itemId": args.item_id, "styleId": args.style_id},
            )
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    return 0 if status == 200 else 1


if __name__ == "__main__":
    sys.exit(main())
