# AskSwarm robustness amendment, 2026-10-04

Status: post-hoc saved-data analysis requested by Shadow, not a new experimental launch.
Written before implementing the robustness helper or inspecting its results. No API/model calls.
Original sources and git ref remain frozen. Original results are preserved in results/.

## Contrasts and denominators

Recompute EVERY answer with the same .7 clustering and 100-step window after each independent
transformation of baseline records: (1) remove byte-identical nonempty text duplicates globally,
keeping the earliest observed row (not normalized duplicates); (2) retain one earliest
representative per provenance root, wiki page or recursive SwarmTraces parent chain, git commit
(no artifact-root relation is defined for unrelated commits); (3) exclude explicitly imputed
clocks and wiki fallback-clock rows (anything except reqlog). Treat rclog/write_date as a
conservative sensitivity, not proof those clocks are wrong or imputed. Null clocks remain null.
Also report a combined arm applying all three. Deduplication deliberately removes later
repeaters; root reduction deliberately removes later edits. These are sensitivity estimands,
not corrected truth. Root identity/time/text come from a real retained row, never a composite
fictional actor. No root information means singleton with missing-root coverage disclosed.

Show record, known-identity, dated, jointly observed, nonempty-text and temporal-cluster
counts; observed identity counts, coverage fractions and absolute baseline differences.
Recompute first observers, adopter curves, time-to-k, marker fractions, reuse credit, Gini,
identity spans and task subsets. Rank movements: tie-aware ranks, common-support correlation,
mean/max displacement and top-10 overlap with ties; entries/exits explicit. Compare participation,
first-observer counts, raw/per-record reuse credit, spans, marker counts and cluster breadth /
time-to-k. Match clusters via shared retained event IDs, greedy largest overlap, and report
unmatched clusters and changed first-observer sets. All full transformed answers saved.

## Blinded link review

Draw a fixed seeded random sample of 30 claimed directed near-term reuse links, stratifying
15 wiki and 15 git (or all available if fewer), before reading any sampled content. SwarmTraces
has no identity/clock links to audit. Show only randomized A/B text, hiding actor labels,
clock order, source IDs, scores, cluster/rank and root relationship. Strip known actor strings
from text. Review the full pair where feasible; disclose truncation. Judge (a) substantive
shared wording rather than template-only overlap, and (b) whether text alone establishes
endorsement/adoption. Then unblind root/source context to distinguish inherited snapshots and
administrative templates. Save sample IDs, judgements, reasons and population sizes, no raw
corpus rows. Reviewer is the operating assistant doing direct close reading, NOT a human or
independent reviewer. Blinding is partial because source genre may be recognizable. Report
per-stratum precision and Wilson intervals for lexical-link judgement; not a causal validation
or population IID CI. No invented human review and no claimed verified endorsement from copies.

## Claim limits and checks

Copied text is not endorsement. Absent outcomes are not failures. Synthetic identity counts
are not autonomous agent counts, explicitly for collusion.wiki labels and SwarmTraces names.
No identities/names are extracted from SwarmTraces attack text by this package. Unit-test
recursive roots, cycles, duplicate semantics, unknown-clock handling, ties and ranking loss.
Share importable transformation/ranking helpers for halflife and identity. Static paired tables
and before/after HTML are the visualization: these offline transformations are not evolving
runs, so no live animation is meaningful. Resource cap one local process, zero paid calls.
