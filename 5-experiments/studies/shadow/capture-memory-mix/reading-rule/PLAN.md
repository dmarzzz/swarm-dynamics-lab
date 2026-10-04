# Frozen-history reading-rule diagnostic v1

Prospective amendment, 2026-10-04, shadow/sol-cm2. Owner request replaces the earlier suggested Claude swarm replication with this bounded diagnostic. No new model calls preceded this plan. This is an exploratory instrument diagnostic, not a replication of collective recovery or an accepted hypothesis.

## TLDR

Query gpt-4o-mini through OpenRouter on the same frozen partner-name histories, changing only presentation order and representation. Compare chronological, reversed and shuffled display of indexed events, crossed with raw names versus a lossless count-and-position summary that preserves the true last event. The independent analysis unit is a history, not a call. Maximum 156 calls including qualification, USD 12 cumulative cap, finish before 2026-10-04 21:30Z. No Anthropic pool access.

## Question and prediction

Does gpt-4o-mini's coordination choice depend on display order or representation even when all event information is unchanged? This follows the post-hoc reading-rule lead in ../README.md; it does not test the causal explanation of the cross-model swarm result. No directional prediction: chronology sensitivity, recency, majority and representation effects are competing possibilities. Existing call logs contain counts but not complete histories, so they cannot support exact replay; these are explicitly synthetic histories, not reconstructed historical runs.

Primary endpoint: mean absolute change in normalized first-token probability of the true majority name, chronological raw versus reversed raw. A change >=0.10 is practically notable for this diagnostic; report paired 95% bootstrap interval, not a confirmatory p-value. Secondary: shuffled versus chronological raw, chronological summary versus chronological raw, majority probability and last-event alignment by length and recency conflict. These contrasts are descriptive and not multiplicity-adjusted.

## Setup

- Model: `openai/gpt-4o-mini`, OpenRouter only, temperature 0, max output 8 tokens, first-token logprobs/top 20 requested, provider must support parameters. Save returned model and provider; mismatch invalidates the call.
- Original coordination-game system instruction from ../src/model.py, with a transparent instruction that event indices encode chronology and display order can vary. No instruction to follow majority, no ground truth labels given.
- Scientific histories: lengths 16, 64, 256; majority Cedar or Raven; last event matches or conflicts with majority; two independent seeded permutations per combination. 3 x 2 x 2 x 2 = 24 histories. Majority count is exactly 5/8 of each length. Label, length and last-name status balanced. These are small synthetic strata, not 24 natural-world samples.
- Six paired renderings per history: raw/summary x chronological/reversed/shuffled. Every event retains its chronological index. Shuffled order deterministic per history. Summary groups by name, gives exact counts and the ordered list of event indices for each name; the group order follows first appearance in that display. It also includes explicit last-event index/name, as does raw. Position lists make the summary lossless for the entire indexed history, not merely its multiset. The summary is therefore not a pure count-only ablation.
- Summary may save tokens, but no cost/accuracy optimum is claimed. Both conditions disclose the same latest-event metadata so reversal never changes the true last event.
- Synthetic fixture seeds are disjoint from two unanimous qualification histories (16 Cedar; 16 Raven). Histories and all effective prompts frozen before calls; generated content/hash saved. No condition gets different prior conversation or agent memory.

## Protocol

1. Commit this plan before implementation, then freeze histories, effective requests and source hashes before launch. Run offline checks for exact reconstruction, counts, last-event preservation, label balance, assignment uniqueness, known-answer scoring and cap/restart behavior.
2. Publish and verify this exact plan at an immutable GitHub URL; save the URL, content hash and fetched-page receipt. Register the diagnostic with its own hub ID if supported. Do not alter the original experiment's run IDs or source inputs.
3. S0: 2 unanimous histories x 6 renderings = 12 calls. Pass only if all calls have valid model receipts, parsable choices and allowed first-token mass >=0.8, and >=11/12 responses choose the unanimous name. Failure blocks S1; report it without prompt repair in this version.
4. S1 after qualified S0 and a recorded stage pre-assessment: 24 histories x 6 renderings =144 calls. Deterministically randomize request order across histories/conditions. One call per assignment. No automatic retry of failed, interrupted or ambiguous calls; resume skips every durably started ID, not just successes.
5. Reserve USD 0.05 durably before every call; never release reservations in this small diagnostic, including errors. With 156 calls exposure is <=USD 7.80, below the USD 12 authority. Require request UTF-8 bytes <=20,000, price routing ceilings of USD 1/million prompt and 2/million completion tokens, max output 8 tokens. This bounds each request below its USD 0.05 reservation using bytes as a conservative token bound plus 512 wrapper tokens. Actual reported usage/cost recorded separately; missing cost remains unknown, not zero. No parallel paid calls. Exclusive file lock over execution and append-only start/terminal journal prevent duplicate dispatch on restart.
6. Hard stop before dispatch at 21:25Z, per-call timeout 45 seconds, with closeout by 21:30Z. Stop early on authorization/budget errors, model mismatch or three consecutive transport failures. No alternate model, pool or endpoint fallback. Cap remains USD 12 across all stages and resumes. The existing swarm pilot ledger is historical and separate from this newly authorized diagnostic, not reset.

## Metrics

Exact allowed-name response parser; first-token probability sums tokens whose stripped text equals the name or is its nonempty prefix (case-insensitive), then normalizes over both names. Save raw logprobs; fail validity if total allowed mass <0.8. Do not substitute sampled text for missing probabilities. Report assignment, started, terminal, valid and paired-history denominators separately. Unstarted/error/invalid remain visible. Compute primary only for histories valid in both primary cells, with worst-case missing-history sensitivity in [0,1]. If fewer than 20 primary pairs are valid, report an incomplete diagnostic only.

Bootstrap 10,000 times over history IDs with deterministic seed 20261004. All six renderings of a history travel together. Report the matched effects and intervals; within-stratum n=2 is too small for generalizable subgroup inference. No causal claim about previous swarm dynamics, other models, native unindexed list prompts or naturally occurring histories.

## Visualization mapping

One static paired-history dot plot of majority probabilities across the six conditions, plus a validity/missingness table. No meaningful swarm time axis exists in this one-shot diagnostic; a temporal replay would falsely imply interaction. The static plot and complete indexed histories are the supported fallback. Progress journal serves as a live view. Figure must match saved probabilities exactly.

## Pre-run assessment and previous lessons

Disposition: diagnostic-only, conditional on offline checks, public registration and S0. Owner explicitly requested frozen histories and OpenRouter-only USD 12. Same-author assessment, not independent review or formal hypothesis acceptance. Prior survey/hypothesis gates remain unresolved for formal claims. Previous relevant closeout: ../CORRECTIONS.md and dmarz's latest-results-review-2026-10-04/evidence.json. Accepted lesson: disclose every attempt and denominator, do not imply retries are independent samples; do not reuse a pool whose outages killed prior operational sessions. Revised next step: isolate input reading rather than add another confounded swarm replication. Rejected inference: last-valid versus first-valid equality does not establish first-attempt robustness.
