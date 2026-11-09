#!/usr/bin/env python3
"""Collect daily AI-digest videos from a watchlist of Bilibili uploaders.

The Bilibili "AI日报" ecosystem publishes minutes-to-hours-fresh roundups of the
day's AI news in Chinese — a discovery layer that repeatedly out-caught English
sweeps. This tool pulls each uploader's latest videos via Bilibili's public web
API (with your logged-in cookies) and emits a deduplicated Markdown digest.

Usage:
  python tools/bili_dailies.py                 # last 36h, watchlist defaults
  python tools/bili_dailies.py --since 2026-11-01 --json /tmp/bili.json --markdown /tmp/bili.md

Watchlist: data/bili_watchlist.json — list of {"name": "...", "uid": "..."} entries.
`uid` is optional; when missing the tool resolves it from the Bilibili user-search
API and writes it back. Cookies: $COOKIE_CACHE/bilibili.json (Cookie Editor JSON),
default ~/.cc-switch/cache/bilibili.json. Refresh with tools/extract_bing_cookies.py.

Caveat: relayed items are leads, not facts. A Bilibili-only product/news claim stays
a lead until a primary/vendor date anchor is found (see SOURCES.md).
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import httpx

CN_TZ = timezone(timedelta(hours=8))
COOKIE_CACHE = os.path.expanduser(
    os.environ.get("COOKIE_CACHE", os.environ.get("WEBSEARCH_COOKIE_CACHE", "~/.cc-switch/cache"))
)
COOKIE_PATH = os.path.join(COOKIE_CACHE, "bilibili.json")
WATCHLIST_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "bili_watchlist.json"
)
DEFAULT_WATCHLIST = [
    {"name": "一只AI风向标", "uid": "3706990266157265", "coverage": "AI日报"},
    {"name": "infinite灵感港", "uid": "", "coverage": "AI日报"},
    {"name": "黑鸦Heya", "uid": "", "coverage": "AI日报"},
    {"name": "飞铜壶", "uid": "", "coverage": "AI日报"},
    {"name": "花开花落两由之11", "uid": "", "coverage": "AI日报"},
    {"name": "heike07", "uid": "", "coverage": "AI日报"},
    {"name": "跟陈博士学AI", "uid": "", "coverage": "AI日报"},
    {"name": "RebabelAI", "uid": "", "coverage": "AI日报"},
]
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Referer": "https://search.bilibili.com/",
}


def load_cookies() -> dict:
    if not os.path.exists(COOKIE_PATH):
        raise SystemExit(f"cookie cache not found: {COOKIE_PATH} (run tools/extract_bing_cookies.py bilibili.com)")
    data = json.load(open(COOKIE_PATH))
    return {c["name"]: c["value"] for c in data}


def load_watchlist() -> list:
    if os.path.exists(WATCHLIST_PATH):
        return json.load(open(WATCHLIST_PATH))
    os.makedirs(os.path.dirname(WATCHLIST_PATH), exist_ok=True)
    json.dump(DEFAULT_WATCHLIST, open(WATCHLIST_PATH, "w"), ensure_ascii=False, indent=1)
    return DEFAULT_WATCHLIST


def save_watchlist(items: list) -> None:
    json.dump(items, open(WATCHLIST_PATH, "w"), ensure_ascii=False, indent=1)


def api_get(client: httpx.Client, url: str, params: dict | None = None) -> dict:
    for attempt in range(3):
        r = client.get(url, params=params or {})
        try:
            j = r.json()
        except ValueError:
            j = {"code": -1, "message": r.text[:120]}
        if j.get("code") == 0:
            return j
        # -799: too frequent; -352: risk control. Back off and retry.
        if j.get("code") in (-799, -352) and attempt < 2:
            time.sleep(3 * (attempt + 1))
            continue
        raise RuntimeError(f"bilibili API {url.split('?')[0]} -> code {j.get('code')}: {j.get('message')}")
    raise RuntimeError("unreachable")


def resolve_uid(client: httpx.Client, name: str) -> str:
    j = api_get(
        client,
        "https://api.bilibili.com/x/web-interface/search/type",
        {"search_type": "bili_user", "keyword": name},
    )
    results = (j.get("data") or {}).get("result") or []
    if not results:
        raise RuntimeError(f"no user found for {name!r}")
    # Prefer an exact name match; otherwise take the top result.
    for item in results:
        if item.get("uname") == name:
            return str(item["mid"])
    return str(results[0]["mid"])


def fetch_recent(client: httpx.Client, mid: str) -> list:
    j = api_get(
        client,
        "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space",
        {"host_mid": mid, "offset": ""},
    )
    out = []
    for item in (j.get("data") or {}).get("items") or []:
        if item.get("type") != "DYNAMIC_TYPE_AV":
            continue
        mods = item.get("modules") or {}
        author = mods.get("module_author") or {}
        archive = ((mods.get("module_dynamic") or {}).get("major") or {}).get("archive") or {}
        title = archive.get("title") or ""
        bvid = archive.get("bvid") or ""
        ts = author.get("pub_ts")
        if not title or not bvid or not ts:
            continue
        out.append(
            {
                "title": title,
                "bvid": bvid,
                "url": f"https://www.bilibili.com/video/{bvid}",
                "pub_ts": int(ts),
                "pub_cn": datetime.fromtimestamp(int(ts), CN_TZ).strftime("%Y-%m-%d %H:%M"),
                "desc": (archive.get("desc") or "")[:300].replace("\n", " "),
            }
        )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="", help="YYYY-MM-DD (default: last 36 hours)")
    ap.add_argument("--json", default="", help="write JSON digest here")
    ap.add_argument("--markdown", default="", help="write Markdown digest here")
    ap.add_argument("--max-per-up", type=int, default=6)
    args = ap.parse_args()

    since = (
        datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=CN_TZ)
        if args.since
        else datetime.now(CN_TZ) - timedelta(hours=36)
    )
    cookies = load_cookies()
    watchlist = load_watchlist()
    changed = False
    all_items, errors, seen_bvids = [], [], set()

    with httpx.Client(cookies=cookies, headers=HEADERS, timeout=20, follow_redirects=True) as client:
        for entry in watchlist:
            name = entry.get("name") or ""
            uid = entry.get("uid") or ""
            try:
                if not uid:
                    uid = resolve_uid(client, name)
                    entry["uid"] = uid
                    changed = True
                    time.sleep(1.5)
                videos = fetch_recent(client, uid)[: args.max_per_up]
                for v in videos:
                    if v["pub_ts"] < since.timestamp() or v["bvid"] in seen_bvids:
                        continue
                    seen_bvids.add(v["bvid"])
                    v["uploader"] = name
                    all_items.append(v)
                time.sleep(1.2)
            except Exception as exc:  # keep going; report per-UP failures
                errors.append(f"{name or uid}: {exc}")

    all_items.sort(key=lambda x: x["pub_ts"], reverse=True)
    if changed:
        save_watchlist(watchlist)

    generated = datetime.now(CN_TZ).strftime("%Y-%m-%dT%H:%M:%S%z")
    payload = {
        "generated_at": generated,
        "since": since.strftime("%Y-%m-%d %H:%M"),
        "count": len(all_items),
        "errors": errors,
        "items": all_items,
    }

    lines = [f"# Bilibili AI 日报汇总（{generated}，自 {since.strftime('%Y-%m-%d %H:%M')}）", ""]
    if not all_items:
        lines.append("无新日报。")
    for v in all_items:
        lines.append(f"- **{v['pub_cn']}** · {v['uploader']} · [{v['title']}]({v['url']})")
        if v["desc"]:
            lines.append(f"  - {v['desc']}")
    if errors:
        lines += ["", "抓取失败："] + [f"- {e}" for e in errors]
    markdown = "\n".join(lines) + "\n"

    if args.json:
        json.dump(payload, open(args.json, "w"), ensure_ascii=False, indent=1)
    if args.markdown:
        open(args.markdown, "w").write(markdown)
    print(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
