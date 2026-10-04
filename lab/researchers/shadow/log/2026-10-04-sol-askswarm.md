# shadow/sol-askswarm, 2026-10-04

- Human-directed Wave 3 build. Created and claimed wild-askswarm; measurement plan committed
  before computing outcomes. Shipped importable v0.1 at 5afc526a, comfortably inside 90 minutes.
- Full census: wiki 14,591 revisions / 3,102 known labels; SwarmTraces 189,579 artifacts /
  no top-level actors / every clock null; frozen swarm-lab 2,673 non-merge commits / 161 agent
  prefixes. Missing values stay missing. No social-cascade claim from the artifact corpus.
- Delivered generic CSV/JSONL, wiki, SwarmTraces and git/task adapters; deterministic MinHash
  lexical clustering, first movers/ties, unique adopters, censoring, reuse credit, marker proxies,
  Gini and observed spans. Three HTML reports + comparison, compressed derived cluster tables,
  figure, source/code hashes, sensitivity runs, findings and novelty check. No raw dataset rows.
- 18 offline tests pass; pairwise Gini and cluster-count reconciliation pass for all 7 reports.
  Full baseline+sensitivity regeneration: 102.924 seconds, one process, nice 10; $0/model calls 0.
  Desktop/mobile Playwright check: no page errors, 390px mobile document width at 390px viewport.
- Hub wild-askswarm: three completed baseline runs, each with metrics.json/report.html; readback
  verified done and two artifacts. This is post-run publication, not retroactive preregistration.
- Flight Deck blocker: fd.py add rejected the first SVG because it reads the 800px viewBox
  rather than the 1600px output size; re-rendered to a true 1600x820 viewBox, which passed.
  However fd.py add globally rewrote 40+ unrelated attestations and ~5,600 lockfile lines.
  Restored ALL those unrelated tracked changes, moved only the newly generated own artifact
  copies to /tmp/askswarm-flightdeck-generated, and retained the valid figure under notes/results.
  No other researcher's provenance changes are included. Final artifact registration needs a
  scoped Flight Deck fix/maintainer action; the figure and reports are already usable.

## Priority robustness follow-up (Shadow, 2026-10-04)

Shipped importable variants/root/dedup/clock/rank helpers at bba7e9e3. Recomputed all questions
on 3 corpora x 5 arms in 383.768 sec, zero study API/model calls. Original outputs preserved.
Wiki records 14591 -> 11943 exact-dedup / 4579 root / 14482 conservative fallback-clock;
root credit top-10 overlap 1/10. Git 2673 -> 1736 exact-dedup, multi-identity clusters 34 -> 8,
credit recipients 26 -> 3 (original top-10 overlap zero). SwarmTraces root rows 128454,
all actor/time endpoints still unavailable. Partially blinded direct assistant review of
30 links locked before key: 15/15 git sync boilerplate; wiki 10/15 cross-root task-specific
repeats (66.7%, nominal Wilson 41.7-84.8%), 5 same-page snapshots. Semantic adoption/endorsement
precision unavailable, not zero. 30 unit tests and 15 full-report arithmetic checks pass.
See ROBUSTNESS.md, AUDIT.md, POSTMORTEM-ROBUSTNESS.md; helper ready for halflife/identity.
