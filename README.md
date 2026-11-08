# skills

Reusable Claude Code skills and one copyable workflow, by Ame.

## Skills (invokable instruction packs)

- **arxiv-cs-digest** — daily arXiv CS digest workflow (fetch candidates, select 5–15,
  materialize PDFs, write a Chinese briefing with unit/author verification).
- **build-academic-poster-html** — dense, print-size academic posters as self-contained HTML.
- **web-search** — Clash-routed web search + page fetch (Bing / DuckDuckGo / Baidu, arXiv
  and GitHub APIs, Playwright rendering, optional cookie extraction).

Skills are stateless: an agent invokes them on demand. They contain instructions and
scripts, not your data.

## Workflow (NOT a skill)

- **frontier/** — a copyable, *stateful* daily frontier-intelligence workflow: scan a domain
  checklist, preserve weak signals in an append-only ledger, maintain a compact world
  model, and write a delta report. It is deliberately **not** a skill — the harness will
  not auto-invoke it; you copy it, configure `PROFILE.md`, and run it manually or on a
  schedule. See [frontier/README.md](frontier/README.md).

Use `frontier/` if you want a personal longitudinal observation system; use the skills if
you want a single task done.
