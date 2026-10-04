# Common Thread: narrative convergence map

Owner: `shadow/sol-narrative`. Human-directed synthesis tool, not a new experiment. Zero model calls.

**Live:** https://swarm-narrative.pages.dev

The page asks where three researchers' work converges, rather than using commit volume as a proxy for scientific evidence. It shows a three-swimlane commit timeline, a theme graph, documented cross-researcher transfers, three candidate submission headlines, and a source-linked evidence ledger. Headline weights are editable in the browser. Candidate narratives are editorial proposals, not team endorsement.

## Reproduce

From the repository root (Python 3.10+, PyYAML, git):

```sh
git fetch origin
python3 researchers/shadow/notes/narrative/build_map.py --ref origin/main
python3 researchers/shadow/notes/narrative/test_map.py
python3 -m http.server 8080 --directory researchers/shadow/notes/narrative
```

Open `http://localhost:8080`. To reproduce the committed git source and activity window, pass `--ref <narrative.json source_commit> --as-of <narrative.json as_of> --offline`. The public hub is a separately timed observation; offline builds explicitly mark it unavailable. `--hub-receipt <path>` writes only an allowlisted projection of hub counts, not hosts, events or arbitrary run payloads. Sources are pinned to a single git commit; each consumed file, the configuration and builder have SHA256 receipts in `narrative.json`.

Deploy **only** `index.html`, `style.css`, `app.js` and `narrative.json` to a static host. No build step or frontend dependencies. Hosting credentials never enter the public directory. Refresh target is approximately every 45 minutes until 23:00 UTC, 4 October 2026; the page labels old snapshots and the end of the refresh window.

## Design context

Audience: the three researchers assembling one submission, and judges inspecting the claims. Job: choose a shared defensible headline, find source receipts and see what remains to land. Tone: dark editorial research observatory, neutral and precise; Doto display, Space Mono instrument labels, readable DM Sans body. Warm gold / muted blue / clay identify dmarz / vishesh / shadow consistently. Graph satellites are keyboard operable; the searchable ledger is a text alternative. Mobile retains every section and scrolls the wide scientific figures instead of shrinking labels beyond readability.

## Inputs and attribution

- Git log at `origin/main`, using **committer timestamps** for the rolling activity windows. Bracketed `[researcher/lane]` prefixes take precedence; fallback aliases are dmarzzz/dmarz, Ultron/cytonomy/Cytonomy/Codex, wakesync/shad0w. Bot index commits are excluded; unmapped authors are counted but not guessed. Attributed merges count.
- `tasks/*.md`: claimed owner, kind, topics, timestamp and explicit blocker excerpts. A claim older than three hours is marked stale. Recent commits and claims do not prove that a worker is running.
- `experiments/evidence-metadata.json`: each cohort's claim, independent-unit sample description, assessor status, evidence confidence and sources. Evidence source documents and result notes are read and hashed. Missing registry records for explicitly named new archive findings are discoverable from `FINDING.md`, labeled registry-pending.
- Researchers' note READMEs are indexed, with surveys, synthesis, the draft submission, Dmarz's overnight program/latest-results review and Vishesh's PI guide/review included as hashed context. The guide and results review are frozen assessments, not current worker telemetry.
- The public hub `/api/state` is fetched with a timeout and reduced to run-status counts. Hub `done` never promotes evidence quality. Active runs older than ten minutes are separately marked stale.
- The hackathon brief: understanding tools, tracing information spread, forensics, reusable questions and meta-science. Fit weights are **our editorial interpretation**, not an organizer-published judging rubric.

## Classification and limits

`editorial.json` contains the theme keywords, featured study mappings, candidate headline evidence sets, interpretation of brief fit, readiness estimates and documented transfer links. Generic nodes get at most two keyword-matched themes. Classification is navigation, not a semantic ground truth. Every registry cohort appears in the ledger and full graph; the focused graph shows featured studies, review artifacts and hub-active studies.

Scientific state is derived from the registry's **assessment status** and score, not inferred from arbitrary commit language. Claim and sample units stay attached. A registry may lag a more recent post-mortem: consult the pinned sources, not the badge, for operational decisions. Current note text provides bounded blocker excerpts, but those can also be historical. No teammates' experiments are changed or launched by this tool.

Independent arithmetic checks are explicitly scoped to each reviewer-owned report. The scaling audit checks aggregate outputs, not raw answers. Raw-answer replay does not independently validate provider identity, spend, preregistration or scientific design. A replication within Claude-family configurations is not evidence of generalization across all model families. Distinct registry cohorts are not necessarily independent studies.

## Transparent headline scoring

```
100 * evidence^wE * brief_fit^wB * coverage^wC * readiness^wR
```

Defaults: all exponents are 1. Browser edits affect presentation only, not `narrative.json`.

- Evidence: take the strongest selected artifact **per represented researcher**, then average those researcher scores. This deliberately avoids counting hundreds of related cells as independent support.
- Evidence tiers: design/review artifact 0; scripted 0.20; diagnostic/descriptive 0.40; pilot 0.55; aggregate arithmetic checked 0.65; cross-model replication 0.70; independently recomputed 0.80. These are editorial utility weights, separate from the registry's 0-4 rubric. Negative results count within their stated narrow scope. No tier means validated causality.
- Coverage: researchers with nonzero selected evidence / 3. A reviewer is credited in transfers and source links, not silently added as the experimental owner.
- Brief fit: explicit editorial number and explanation in each candidate.
- Readiness: explicit packaging-readiness estimate times the fraction of named evidence artifacts present. It is not a runtime or probability estimate.

No commit count, lane count, library size, model-call count or node degree enters headline scoring. No score is a probability of truth or of winning. The candidate evidence sets are selected editorially and do not exhaust the repository.

## Validation

`test_map.py` checks attribution, bot exclusion, failed/unrun separation, score arithmetic, missing-artifact penalties, design-only coverage, unique node IDs, pinned source URLs and transfer integrity. Browser smoke tests check 1440px / 390px layouts, absence of console errors, graph keyboard interaction, searchable ledger, editable scoreweights and parity with Python's scores. Deployment smoke tests verify HTTP 200 and the public snapshot source hash.
