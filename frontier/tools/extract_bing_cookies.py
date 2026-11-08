#!/usr/bin/env python3
"""Extract cookies for one domain from the local Microsoft Edge profile and write
them in Cookie Editor JSON format to ~/.cc-switch/cache/<domain-key>.json, the path
the web-search skill reads automatically.

Default domain: bing.com (for search-engine challenges). Also used for bilibili.com
and zhihu.com (JS-gated Chinese platforms; pass the domain as an argument).

Usage:
  /opt/miniconda3/envs/skills/bin/python tools/extract_bing_cookies.py bing.com
  /opt/miniconda3/envs/skills/bin/python tools/extract_bing_cookies.py bilibili.com
Runs fully local: reads Edge's cookie DB and decrypts with the keychain key. Never
prints cookie values. Requires cryptography (present in the skills conda env).
"""
import json
import os
import sqlite3
import subprocess
import sys

EDGE_DB = os.path.expanduser("~/Library/Application Support/Microsoft Edge/Default/Cookies")
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "bing.com"
EXPORT_DIR = os.path.expanduser(os.environ.get("WEBSEARCH_COOKIE_CACHE", "~/.cc-switch/cache"))
EXPORT_PATH = os.path.join(EXPORT_DIR, f"{DOMAIN.split('.')[0]}.json")
CHROMIUM_EPOCH_OFFSET = 11644473600  # microseconds since 1601 -> unix seconds
SAME_SITE = {0: "unspecified", 1: "lax", 2: "strict", -1: "unspecified"}


def get_keys() -> list:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    keys = []
    for svc in ("Microsoft Edge Safe Storage", "Chromium Safe Storage"):
        out = subprocess.run(
            ["security", "find-generic-password", "-w", "-s", svc],
            capture_output=True,
        ).stdout
        if not out:
            continue
        # Edge on macOS derives the AES key from the keychain password with
        # PBKDF2-SHA1 (classic Chromium scheme). Two service names exist; rows
        # are encrypted with one or the other depending on when they were
        # written (verified empirically 2026-09-09).
        keys.append(PBKDF2HMAC(
            algorithm=hashes.SHA1(), length=16, salt=b"saltysalt", iterations=1003
        ).derive(out.rstrip(b"\n")))
    if not keys:
        raise SystemExit("no Edge safe-storage keychain items found")
    return keys


def printable(b: bytes) -> bool:
    return bool(b) and all(32 <= c < 127 for c in b)


# Constant 16-byte header block of the newer Edge macOS scheme (v10 + iv16 + CBC),
# observed identical across all rows (2026-09-09).
NEW_FMT_HEADER = bytes.fromhex("d1da1697e2e696101f317ef301c731e3")


def decrypt(enc: bytes, keys: list) -> str:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    if not enc.startswith(b"v10"):
        raise ValueError(f"unsupported version prefix: {enc[:3]!r}")
    body = enc[3:]

    def cbc_raw(iv: bytes, ct: bytes):
        for key in keys:
            d = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
            pad = d.update(ct) + d.finalize()
            if 0 < pad[-1] <= 16:
                yield pad[: -pad[-1]]

    # 1) AES-GCM (authenticated): nonce(12) | ct | tag(16)
    for key in keys:
        try:
            v = AESGCM(key).decrypt(body[:12], body[12:], b"")
            if printable(v):
                return v.decode("ascii")
        except Exception:
            pass
    # 2) New scheme: v10 + iv(16) + ct, plaintext = constant header(16) + value
    if len(body) >= 32:
        for v in cbc_raw(body[:16], body[16:]):
            if len(v) >= 16 and v[:16] == NEW_FMT_HEADER and printable(v[16:]):
                return v[16:].decode("ascii")
    # 3) Classic scheme: v10 + ct, IV = 16 spaces, PKCS7
    for v in cbc_raw(b" " * 16, body):
        if printable(v):
            return v.decode("ascii")
    return "?"  # undecryptable with available keys; sanitized placeholder


def main() -> None:
    keys = get_keys()
    con = sqlite3.connect(f"file:{EDGE_DB}?mode=ro", uri=True)
    rows = con.execute(
        "SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly, "
        "has_expires, samesite, encrypted_value FROM cookies "
        "WHERE host_key LIKE '%' || ?", (DOMAIN,)
    ).fetchall()
    con.close()

    out = []
    for host, name, plain, path, exp, sec, httponly, has_exp, same, enc in rows:
        value = plain if plain else decrypt(enc, keys)
        # Cookie headers must be ASCII-encodable; real browser cookies are ASCII.
        value = value.encode("ascii", "replace").decode("ascii")
        out.append({
            "domain": host,
            "expirationDate": (exp / 1_000_000) - CHROMIUM_EPOCH_OFFSET if (has_exp and exp) else 0,
            "hostOnly": not host.startswith("."),
            "httpOnly": bool(httponly),
            "name": name,
            "path": path,
            "sameSite": SAME_SITE.get(same, "unspecified"),
            "secure": bool(sec),
            "session": not bool(has_exp),
            "storeId": "0",
            "value": value,
        })

    os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)
    with open(EXPORT_PATH, "w") as f:
        json.dump(out, f)
    print(f"exported {len(out)} {DOMAIN} cookies -> {EXPORT_PATH}")


if __name__ == "__main__":
    main()
