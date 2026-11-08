# Frontier — a copyable personal frontier-intelligence **workflow** (not a skill)

Frontier is a stateful, long-running observation workflow: once a day it scans a set of
domains, preserves weak signals, appends evidence to an append-only ledger, revises a
compact world model, and writes a short delta report. It is designed to be **copied,
configured, and owned by one person** — not invoked as a reusable skill.

> **This is NOT a skill.** Skills in this repository are stateless instruction packs that
> an agent invokes on demand. Frontier is a workflow with persistent state
> (`PROFILE.md`, `STATE.md`, `data/events.jsonl`, `reports/`). The skills harness will not
> auto-invoke it; you run it manually, by cron, or via a scheduled Claude Code task.

## Relationship to the other skills

Frontier *uses* the `web-search` skill (`../web-search/`) for all internet research.
Nothing else is shared: your data stays in your own workspace directory, and this folder
contains only the framework.

## What's in the box

```
frontier/
  README.md                  ← this file
  WORKFLOW.md                ← the daily routine prompt (the core; self-contained for a fresh session)
  config.example             ← environment variables to copy into your shell profile
  scripts/init.sh            ← create a workspace from the templates
  tools/extract_bing_cookies.py  ← optional macOS Edge cookie extractor (for Bing/Bilibili challenges)
  templates/
    CLAUDE.md                ← durable operating rules (goes to your workspace root)
    PROFILE.example.md       ← your profile + owner-priority clusters (edit this first)
    STATE.example.md         ← empty world model
    SOURCES.example.md       ← domain checklist + source map
```

## What is deliberately NOT included

- **Personal data**: the author's `PROFILE.md`, `STATE.md`, ledger, reports, inbox.
- **Institutional integrations** (e.g., campus notice boards) — add your own under
  `tools/` if you want; they are optional and stay in your private workspace.
- **Credentials / cookies**: never stored here. The cookie extractor reads your local
  browser profile at runtime and writes to your own cache directory.

## Quick start

```bash
cp config.example ~/.frontier.env       # edit paths
source ~/.frontier.env
bash scripts/init.sh ~/frontier          # or $FRONTIER_HOME
cd ~/frontier
$EDITOR PROFILE.md                       # fill in who you are + your priority clusters
$EDITOR SOURCES.md                       # adjust the domain checklist + watchlist
```

Then run the workflow by hand once:

```bash
claude   # in ~/frontier
# paste: "Read WORKFLOW.md and run today's routine."
```

Schedule it however you like (cron, launchd, a Claude Code scheduled task). The workflow
expects the workspace to be a git repository and commits every run (local archive by
default; add a private remote if you want off-machine backup).

## How to personalize

1. **PROFILE.md** — the most important file. Its "priority clusters" drive which items get
   the full two-sided deep-dig automatically. The example lists five clusters; replace
   them with yours.
2. **SOURCES.md** — the domain checklist (17 domains by default) and your entity
   watchlist. Add/remove domains freely; keep the anti-cocoon quotas (new terrain +
   negative scouting every run).
3. **WORKFLOW.md** — quotas, report language, verification depth. The defaults are
   intentionally demanding (full-domain sweep, adversarial verification subagent); trim
   them if you want a lighter loop, but keep the multi-source and two-sided rules.
4. **Language** — reports are written in Chinese by default; change the instruction in
   WORKFLOW.md step 12.
