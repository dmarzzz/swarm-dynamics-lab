# One bounded deletion-return pilot, v1

Owner: shadow/sol-audit-gap, 2026-10-04. Prospective plan after schema inspection, before contrasts. Follow-up owner direction assigns provenance invariance to factory, memory-reading to cm2, and AskSwarm precision to askswarm; this pilot does none of those. No model/provider call is needed, so there is no pool test or exposure to its current 429/503 bursts.

## TLDR

On the fixed collusion.wiki export, compare observed page saves in symmetric windows before and after that page's first observed successful deletion. Also report whether any save returns within 30 minutes. This is a paired descriptive incident-response diagnostic, not a causal estimate of deletion efficacy. A later save does not mean the same content, answer or agent returned. Read and hash frozen local source files; never execute source text or contact any wiki.

## Question and prediction

For pages with an exactly linked, accurately timed first successful deletion, how often is another save observed after deletion, and how does post-deletion write activity compare with the same page immediately before? No directional prediction. The prior source already notes moderator deletion and eventual activity collapse; the increment is an exact page-linked return/paired-window measurement. Do not claim that deletions caused either suppression or persistence.

## Setup

Inputs `--data` directory with collusion.wiki `events.jsonl.gz` and `revisions.jsonl.gz`; source https://collusion.wiki/explorer/download. Schema inspection found delete events have `page_key`, `success_observed`, time grade and uncertainty; revisions have the same `page_key`, precise clock fields and `rev_id`. Use publisher `page_key` exactly, never fuzzy page/name joins. Do not use revision body, label, ip16 or names. Revisions are observed saves, not independent agents.

For every page, select its chronologically first event with `event_type=delete` and `success_observed=true`, before any clock-quality exclusion. Tie break with event_id. Admit that selected deletion only when `time_grade` is reqlog or rclog, timestamp parses and `uncertainty_seconds` is finite, nonnegative and <=1. Do not replace an ineligible first event with a later eligible one. Count every excluded page and reason. Admit revision timestamps under the same quality rule. Duplicate event_id/rev_id or malformed timestamps fail the run; absent times are an accounted exclusion.

Require deletion t to have t-1800 >= global minimum and t+1800 <= global maximum of admissible revision times. This guards release-edge censoring only, not unobserved logging gaps. There must be at least one admissible revision anywhere or the pilot is blocked. If fewer than ten pages survive, report feasibility only, no headline contrast.

## Protocol

- One bounded analysis cohort: every eligible page under the fixed selection rule. No tuning cutoffs after results and no paid calls, new experimental agents or collected outcomes.
- Primary paired windows: **t-1800 <= save < t-60** and **t+60 < save <= t+1800**. Each has 1740 seconds; the 60-second guard is much larger than admitted timestamp uncertainty. Exclude exact guard-boundary saves. Include outer boundaries. Exact t ties never establish ordering.
- Per page: pre count, post count, post-any-return indicator, and first post-guard save latency if <=1800. Report primary mean(post-pre), sum(pre), sum(post), fraction post>pre / equal / lower, post-any-return fraction. The ratio sum(post)/sum(pre) is descriptive and null if pre is zero. No median over all pages is imputed for nonreturners.
- Secondary fixed-window robustness: 5 and 60 minute horizons with the same 60-second guard; **use the same primary cohort** but report eligible-boundary subsets for these horizons. Do not silently use a 60-minute outcome on censored pages. Primary remains the 30-minute contrast.
- Dependence: pages are clustered by UTC day of deletion. Report their number, per-day aggregates, and a 95% percentile cluster bootstrap of primary mean difference, resampling deletion days with replacement, seed 20261004, 5000 draws, retaining every page in a selected day. This estimates variation across observed deletion-day clusters only; it is not a population or causal CI. If fewer than five day clusters, omit this interval and retain raw per-day contrasts.
- Save one immutable derived assignment record per selected page, keyed by SHA-256(page_key), with deletion timestamp/day, eligibility reason and per-window counts. These are derived outcomes, not raw dataset rows. Retain source gzip fingerprints and manifest; raw source files remain local, read-only and are never committed.

## Checks before reporting or scaling

Hand-authored fixtures cover exact join, first-deletion selection before quality filtering, timestamp quality, release edges, repeated deletes, ties, guards and empty baselines. Primary implementation uses sorted timestamps and binary search. A separate reference implementation independently groups and scans intervals without importing primary analysis functions, reading the same frozen source files. Compare the **full page-level assignment/count table**, not just headline arithmetic. Record this as separate-implementation/same-author recomputation unless another researcher supplies an actual review; do not imply peer independence. No scaling or second experimental pilot is authorized here.

## Visualisation, stopping and resources

Static before/after aggregate bars plus daily paired differences. Unlike SwarmTraces, real timestamps exist, but there is no need to invent a simulated replay. Stop after one full pilot plus the reference recomputation and deterministic validation; code-defect repair is versioned and retains prior artifacts. One local nice-10 CPU process, <1GB RAM, <100MB output; USD0 and zero model calls. If exact linkage or quality gates fail, publish the feasibility limit rather than pivoting to an unregistered scientific contrast.

## Prior art and limits

collusion.wiki already reports deletions and changing activity. arXiv2609.09150 explains copying; our comparison does not refit it. Our previous strategy audit ranked deletion-return as the next unowned real-data question. The half-life lane explicitly ignores deletions; timeline owns daily aggregate incident counts, not page-level post-deletion recurrence. This observational contrast cannot distinguish deletion effects from stopping tasks, moderator selection, time-of-day/burst effects, page changes or absent captures. Bootstrap intervals do not remove those confounders.
