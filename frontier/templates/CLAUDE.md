# Frontier — Personal Frontier Intelligence Workspace

Longitudinal weak-signal observation system. Purpose: observe small structural changes in
technology, science, industry, business, labor, capital, policy, society, consumer
behavior, infrastructure; preserve weak signals; accumulate evidence; maintain a compact,
continuously revised model of what is genuinely emerging; surface career/research/startup/
time-investment and cross-domain opportunities. NOT a news summarizer.

## Layers (never collapse)
- EVENT — something that actually happened → `data/events.jsonl`
- SIGNAL — a possible implication of one or more events
- BELIEF — a broader judgment supported by accumulated signals → `STATE.md`
Facts stay distinguishable from interpretations.

## Core principles
- Prefer accumulation over interpretation. One event is an observation, not a trend.
- No numerical scores. Lifecycle states only: watching / emerging / established /
  weakening / reversed / inactive. Transitions require justification; one event normally
  cannot cause a major transition.
- Evidence counts most when it repeats across dates, independent actors, evidence types,
  incentive structures, markets/geographies.
- Resistant to: hype, one-day narratives, repeated coverage of one event, fixation,
  hindsight rewriting, fake precision.
- Actively seek and preserve contradictions. For every interesting development ask: what
  evidence would make this interpretation wrong? Is growth only publicity? Are all signals
  downstream of one source? Are actors copying each other? Is it economically sustainable?
  Is it geographically narrow? Are there failed attempts receiving less attention?

## What to look for (structural changes, not "news")
What became cheaper? What became scalable? What specialist task can now be done by
non-specialists? What impossible product became merely expensive? Where is a bottleneck
moving (software→hardware, model→data, inference cost, regulation, distribution, trust,
physical infrastructure, labor→automation, automation→supervision)? Strange hiring,
startup clusters, talent migration, what companies BUY vs what they say, pricing changes,
capex/infrastructure, unexpected convergence, research→deployment, industry merges,
enabling tech before a market, recurring failure modes, low-attention/high-activity areas.

## Exploration balance (anti-bias principle, not mechanical)
Roughly: 1/3 close to the owner's profile · 1/3 adjacent · 1/3 distant. `PROFILE.md`
informs interpretation, never filters discovery. Owner-project entries must never narrow
discovery: the new-terrain/negative-scouting quotas apply regardless, and society-wide
watching continues in parallel.

## Anti-fixation
Search abundance ≠ real-world importance. Do not keep deepening subjects already in
`STATE.md`. Reserve effort for new terrain. Deduplicate: many articles about one launch =
ONE event. Hard anti-cocoon quota per run: ≥2 searches on genuinely new terrain + ≥1
negative-scouting query (details in `WORKFLOW.md` step 4). The system must not converge on
its own past.

## Hard epistemic rules
Never invent sources, facts, or URLs. Never upgrade speculation into history. Never assume
interesting ⇒ important · fast growth ⇒ durable · funding ⇒ product-market fit · paper ⇒
feasibility · demo ⇒ deployment · hiring ⇒ sustainable demand · several articles ⇒ several
independent signals · unrelated-to-profile ⇒ unimportant. State ambiguity in natural
language.

Multi-source rule: a claim enters `data/events.jsonl` ONLY with (a) a first-party/official
source, or (b) ≥2 INDEPENDENT secondary sources. A single-source claim is NOT an event —
record it as an unconfirmed lead and verify in a later pass. Exceptions only for
owner-supplied primary material (provenance recorded) and expert first-person reports,
still flagged.

Deep-dig rule: significant findings must be dug clean before being recorded as facts —
read the primary page, chase sub-claims to independent sources, search the contradiction
side, mark unverifiable parts as explicit open leads. Skimming is not observation.

Two-sided rule: for every significant claim, paper, product or actor evaluation, survey
BOTH sides — who endorses it and why (with incentives), AND who criticizes it and why
(with incentives). Search "<claim> criticism / overhyped / replication / 复现 / 质疑" and
read the discussion threads, not just headlines. A one-sided picture is not a verified one.

Adversarial verification pass (MANDATORY): before ANY batch of new findings enters the
ledger or a report — routine runs AND interim digs — spawn a subagent as an adversarial
fact-checker. Hand it the claim list (entity, date, claim, source URL) and require
independent re-checks of the known error classes: (a) identity/already-revealed claims;
(b) dates; (c) "first ever"; (d) single-origin presented as multi-source; (e) numbers;
(f) duplicates — give it the relevant ledger excerpts and require an explicit
already-recorded verdict; (g) research claims — abstract-vs-body/implementation check,
third-party replication status, named community critiques. Apply CONFIRM / CORRECT /
DOWNGRADE-TO-LEAD before writing. The owner's own knowledge must never be a load-bearing
error filter.

Owner-priority dig: items touching the clusters defined in `PROFILE.md` get the two-sided
treatment automatically and first, and are flagged `OWNER-RELEVANT` with both-sides
implications. The clusters in the profile example are just examples — replace them.

## Files
- `PROFILE.md` — evolving capability/resource/constraint map of the owner (never a filter).
- `STATE.md` — compact current world model; detail lives in the ledger + reports.
- `SOURCES.md` — evolving map of where early evidence appears.
- `WORKFLOW.md` — the exact routine prompt (self-contained for fresh sessions).
- `data/events.jsonl` — append-only ledger, one valid JSON line per real-world event.
  Deduplicate coverage. Never delete or rewrite history. Never add scores.
- `inbox/` — owner drops URLs/PDFs/notes. Treat as input, not truth. Delete only items
  actually processed; never blanket-delete. Git history retains deleted material.
- `reports/YYYY-MM-DD.md` — delta-focused report per run.
- Git (local archive by default): commit after each run so history preserves prior STATE,
  events, reports, and processed inbox material. Add a remote only if the owner asks.

## Search
Use the existing web-search skill in this environment for all internet research. Do not
configure another search provider, MCP search, browser wrapper, or framework. Scouting
mix: event / entity / behavioral / bottleneck / edge / negative / wildcard / follow-up,
plus a full pass over the official-channel entity watchlist in `SOURCES.md`.

## Periodic synthesis
- Weekly: patterns visible only over days; which interpretations were wrong; what quietly
  strengthened or failed.
- Monthly: persisted vs vanished directions; systematic search gaps; useful sources;
  which opportunity assessments materially changed.

## System evolution
Evolve only when an observed limitation demands it. Do not preemptively add databases,
vector stores, RAG, agents, orchestration, or other infrastructure.
