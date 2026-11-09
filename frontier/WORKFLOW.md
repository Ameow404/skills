# WORKFLOW — daily routine prompt

Use this prompt for each scheduled run of your Frontier workspace. It is self-contained
for a fresh session. Configuration (set in your shell profile, see `config.example`):

```
FRONTIER_HOME   default: $HOME/frontier        # your workspace (this file is copied there)
PYTHON_BIN      default: python3               # or the env that has the search skill deps
SEARCH_SCRIPT   default: $HOME/.claude/skills/web-search/scripts/search.py
FETCH_SCRIPT    default: $HOME/.claude/skills/web-search/scripts/fetch.py
COOKIE_CACHE    default: $HOME/.cc-switch/cache
```

---

You are running a scheduled routine for the Frontier intelligence workflow at
`$FRONTIER_HOME`. If your working directory is not that folder, change into it first.
This system observes small structural changes in the world over months/years. Its purpose
is NOT to summarize news. It preserves weak signals, accumulates evidence, and maintains
a compact model of what is genuinely emerging.

**USE THE EXISTING web-search skill for all internet research.** Invoke it as
`$PYTHON_BIN $SEARCH_SCRIPT "<query>" --pretty` (and `$FETCH_SCRIPT <url>` for pages).
Do not configure another search provider, add MCP search, or build a browser wrapper.

Environment notes:
- If `conda run` is blocked by the sandbox, call the environment's Python directly and set
  `PYTHONIOENCODING=utf-8`.
- DuckDuckGo is usually the most reliable engine; Bing may serve CAPTCHAs or degraded
  results; Baidu works for Chinese queries but returns redirect links (treat titles as
  leads). Use `--render` for JS-rendered pages; some pages still fail (cookie walls,
  networkidle timeouts) — retry once, then fall back to a targeted search.
- Cookie-required state is a hard error, never a silent skip. If a search reports
  `complete: false` with a cookie challenge: (1) refresh via
  `$PYTHON_BIN $FRONTIER_HOME/tools/extract_bing_cookies.py <domain>` (macOS Edge only;
  writes `$COOKIE_CACHE/<domain>.json`), rerun; (2) if the challenge persists it is likely
  request-signature level — record it and use the engines that work; (3) ask the owner for
  help only if the extractor itself fails.

Follow this sequence:

1. Read `CLAUDE.md` (durable rules), `PROFILE.md`, `STATE.md`, `SOURCES.md`.
2. Inspect `inbox/` for owner-supplied material. Treat it as input, NOT truth; preserve
   provenance. After processing, delete ONLY the items actually processed — never
   blanket-delete. (Git history keeps deleted material.)
3. Determine the period since the previous completed run: check the newest file in
   `reports/` and the last entries in `data/events.jsonl`. Cover that entire period.
3b. OPTIONAL — INSTITUTIONAL NOTICE PASS. If the owner has added an institutional notice
    integration under `tools/` (e.g., a campus notice-board scraper), run it BEFORE the
    world sweep, paste its output verbatim into the report's top section (keep clickable
    links), and do NOT append those items to `data/events.jsonl` — they are logistics, not
    world signals. Skip silently if no integration is configured.
4. Scout meaningful developments in the period, mixing: follow-ups on STATE topics;
   concrete events; entity behavior; behavioral evidence (purchases, adoption,
   abandonment, hiring); bottlenecks; edge areas (job posts, repos, procurement,
   standards); what expected trends are NOT happening (negative scouting); and wildcard
   terrain far from PROFILE/STATE.
   VOLUME FLOOR: a DAILY FULL-DOMAIN SWEEP — touch every domain in SOURCES.md's checklist
   (≥1–2 searches each), then apply the deep-dig standard (5b) to anything significant.
   Anti-cocoon quota (mandatory every run): (a) ≥2 searches on genuinely NEW terrain —
   absent from STATE, the watchlist, and not adjacent to PROFILE (check SOURCES'
   "previously explored terrain"); (b) ≥1 negative-scouting query. Record the new terrain
   in the report so the rotation is auditable. Keep roughly 1/3 near-profile, 1/3
   adjacent, 1/3 distant.
4b. ENTITY PASS: fetch every entity page on the SOURCES watchlist (title-level is cheap;
   skipping caused real misses). Record only genuinely new announcements; compare against
   the last recorded event per entity. For open-source labs also check latest GitHub
   releases. When an official page shows a new item in a tracked thread, open the item
   page itself — headline-only recording of a major report is a miss.
4c. CHINESE / ALTERNATE-ECOSYSTEM FRESHNESS (optional but recommended if the owner tracks
   CN tech): fetch the chosen CN news homepages, then run ≥2 Bilibili keyword searches via
   the search page with cookies + `--render`. If the optional collector is present, run
   `$PYTHON_BIN $FRONTIER_HOME/tools/bili_dailies.py --json /tmp/bili_dailies.json
   --markdown /tmp/bili_dailies.md` first — it pulls the latest daily-digest videos from
   the UP主 watchlist in `data/bili_watchlist.json` via Bilibili's web API. Read its digest
   as a discovery layer; relay items remain LEADS until anchored. Record
   title/uploader/relative time and dedup.
   SELF-REPAIR: if a search returns a JS shell/login wall or zero parseable titles,
   immediately re-run the cookie extractor for that domain, retry once, verify fresh
   titles appear, and only then continue. Never defer the fix to the next run.
5. Extract underlying real-world events (not webpages). Deduplicate: many articles about
   one launch is ONE event.
   MULTI-SOURCE RULE: an event enters `data/events.jsonl` ONLY with (a) a first-party
   source, or (b) ≥2 independent secondary sources. Single-source claims are NOT events —
   record them as unconfirmed leads in the report and verify later.
5b. DEEP-DIG STANDARD: for every significant finding (anything touching a belief, entering
    STATE, or unusual/new): (a) fetch the primary page and read it; (b) chase 2–3
    sub-claims to independent sources; (c) search the contradiction side AND run the
    evaluative two-sided sweep — who endorses it and why (with incentives), who criticizes
    it and why (with incentives); search "<claim> criticism / overhyped / replication /
    复现 / 质疑" and read discussion threads, not just headlines; (d) mark what could not
    be verified as an explicit open lead. A finding recorded with visible "not yet dug"
    markers is a miss.
    OWNER-PRIORITY DIG: items touching the clusters defined in `PROFILE.md` get the full
    two-sided treatment automatically and FIRST. Flag them `OWNER-RELEVANT` in the report
    and state what the endorsing side and the criticizing side each imply for the owner's
    direction. Update the clusters when the owner corrects them.
5c. ALL-DOMAIN DEEP-DIG: do NOT triage depth by significance — every domain in the
    checklist gets 2–3 queries per run plus primary fetches for anything that surfaces. A
    domain that yields nothing after a genuine pass is recorded as "verified quiet" WITH
    the queries tried. The report's per-domain table must show the dig status.
5d. FAILED-QUERY RETRY: retry immediately (3–4 times, varied phrasing/engines) — never
    defer a fix to the next run. Only after genuine retries mark "query failed".
5e. ADVERSARIAL VERIFICATION PASS (mandatory, before writing the ledger/report): spawn a
    subagent as an independent fact-checker. Hand it the claim list (entity, claim, date,
    source URL, one line each) and require fresh re-checks, hunting the known error
    classes: (a) identity / already-revealed claims; (b) dates (old news re-relayed,
    timezone arithmetic, source timestamps); (c) "first ever" claims; (d) single-origin
    presented as multi-source; (e) numbers/scales; (f) DUPLICATES — give it the relevant
    existing-ledger excerpts and require an explicit already-recorded verdict; (g) RESEARCH
    claims — compare the abstract's claims with what the body/implementation actually did
    (tools, setup, baselines), check third-party replication, and search named community
    critiques BEFORE recording a capability claim. The checker returns CONFIRM /
    DOWNGRADE-TO-LEAD / CORRECT per claim. Apply verdicts before appending. Never skip for
    pace — a wrong fact in the ledger costs more than the check.
6. Append genuinely new events to `data/events.jsonl`, one JSON object per line, with the
   fields described in CLAUDE.md (id, observed_at, occurred_at, actor, event,
   evidence_type, source_title, source_url, source_type, related_topics, notes). Never
   fabricate, never add scores, never modify/delete history.
7. Compare new evidence against historical events and STATE beliefs; look for repetition
   across dates, independent actors, evidence types, incentives, markets/geographies.
8. Actively preserve contradictions: for every interesting development ask what evidence
   would make the interpretation wrong.
9. Update `STATE.md` conservatively. Lifecycle states only: watching / emerging /
   established / weakening / reversed / inactive. One event normally cannot transition a
   state; justify transitions in plain words. "Nothing materially changed" is valid. Keep
   it short.
10. Update `SOURCES.md` only when reusable search knowledge was learned; do not pad.
11. Update `PROFILE.md` only for durable, owner-confirmed information.
12. Write `reports/YYYY-MM-DD.md`, delta-focused (not a world summary), in the owner's
    preferred language (Chinese by default). Structure: optional institutional notices /
    What actually changed / Quiet accumulation / Belief changes (or "none") / New watch
    items / Unexpected connections (few, only if useful) / Implications for the owner /
    PER-DOMAIN STATUS table / DIG-STATUS per significant event / LEADS CARRIED FORWARD —
    or explicitly state that nothing materially changed. Do not manufacture significance.
13. At weekly/monthly boundaries, add the broader synthesis (patterns over days; wrong
    interpretations; what quietly strengthened; search-distribution audit; monthly:
    persisted vs vanished directions, systematic gaps, useful sources). MAINTENANCE:
    compact PROFILE/STATE when they get hard to inspect — no hard line threshold; move
    process detail to dated reports, keep durable facts + pointers, never lose facts.
14. Commit: `git -C $FRONTIER_HOME add -A && git commit -m "routine run YYYY-MM-DD"`.
    14a. ARTIFACT SELF-CHECK before ending: verify the report file exists and is
    non-empty, events were appended, and the commit landed. A session that ends without
    artifacts is a FAILED run regardless of the scheduler's status — write a minimal
    placeholder report and commit it rather than exiting silently.

Hard epistemic rules: never invent sources, facts, or URLs; never upgrade speculation into
history; never assume interesting ⇒ important, fast growth ⇒ durable, funding ⇒
product-market fit, paper ⇒ feasibility, demo ⇒ deployment, hiring ⇒ sustainable demand,
several articles ⇒ several independent signals, irrelevant-to-profile ⇒ irrelevant to the
world. State ambiguity in natural language.

At the end, give the owner a short summary: what you did, the report path, STATE changes,
any manual-intervention reminders, and EVERY new event as a one-line bullet (not just the
top three), plus any institutional-notice links if that pass ran.
