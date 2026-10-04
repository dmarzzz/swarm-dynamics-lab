# Results found with swarm-lab (draft for the submission form, item c)

Draft by shadow/sol-submit, 2026-10-04, against repository commit
[`b8d90f52`](https://github.com/dmarzzz/swarm-lab/tree/b8d90f52). Every number below is copied from the linked
results file at that commit; nothing was recomputed for this table. An independent offline recomputation of the
completed dmarz findings is running in task
[review-dmarz-completed-xcheck](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/tasks/review-dmarz-completed-xcheck.md)
and will be linked here when it lands.

How to read the table:

- **Unit** is the independent sample unit. Model calls, identities and rows are not independent samples; the
  intervals are descriptive paired bootstraps over the unit, with no multiplicity correction.
- **Review** says who checked it. Most studies ran under an owner waiver of cross-researcher review; that is
  recorded as "same-researcher check", not as independent validation.
- All studies are **exploratory** and use **synthetic task worlds**. In the Sybil family the identities are
  scripted and admission is computed before the model call; the model only synthesises an answer from the
  admitted reports. None of these results come from in-the-wild incident data.

## Findings

| # | Finding | Numbers | Unit | Model(s) | Review | Source |
|---|---|---|---|---|---|---|
| 1 | Checking identities in proportion to swarm size keeps a synthesiser accurate as the population grows; a fixed check budget collapses | Coverage checks, strong checks, N = 972: proportional (108) minus fixed (4) specialist accuracy +52.8 pp (95% +38.9 to +66.7) Sonnet 4.6, +51.4 pp Haiku 4.5, +100.0 pp Opus 5.5 (0.0% to 100.0%) on byte-identical assignments | 24 paired world roots, 2,400 valid answers per model | Haiku 4.5, Sonnet 4.6, Opus 5.5 | same-researcher | [scale-sonnet](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/sybil-scale-sonnet/RESULTS.md), [scale-opus](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/sybil-scale-opus/RESULTS.md) |
| 1b | The same holds at 9x scale | N = 8,748: proportional checks 20/20 correct, fixed 4 checks 0/22; +100 pp on 18 complete pairs, bounded +50 to +100 over all 24; attacker seat share 9.8% to 2.7%. Run **incomplete** (481/576 valid) after a shared-account billing stop | 24 roots, 18 complete pairs | Opus 5.5 | same-researcher | [scale-xl](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/sybil-scale-xl/RESULTS.md) |
| 2 | More verification is not monotonically safer: answer accuracy can hide worse admission | Only 7 of 120 budget cells met both >= 90% accuracy and <= 5% attacker seats, all at attacker check-pass 10%. At N = 324, coverage 32 to 108 checks raised accuracy 97.2% to 100% while attacker seat share rose 1.98% to 10.70%. A stronger synthesiser (Sonnet vs Haiku, +5.7 pp accuracy) left the safe frontier unchanged | 24 paired roots x 120 cells, 2,880/2,880 valid per model | Haiku 4.5, Sonnet 4.6 | same-researcher | [budget-api](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/sybil-budget-api/RESULTS.md), [budget-sonnet](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/sybil-budget-sonnet/RESULTS.md) |
| 2b | Mechanism for 2: trust propagated through the graph lets extra checks admit more attackers | Change in attacker seats from 32 to 108 checks, `propagated` minus `direct` credit: +20.75 seats (95% +17.33 to +24.21), positive in 24/24 roots. Scripted admission; the model cannot change this outcome | 24 roots | scripted (Qwen 3.7 Flash answers only) | same-researcher | [trust-credit-qwen](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/trust-credit-qwen/RESULTS.md) |
| 3 | Splitting a fixed attacker budget across more identities hurts most when checks go to well-connected identities | Rare-skill wrong answers from 1 to 27 identities (same 27 rows, edges, checks): degree-based +48.6 pp, coverage-based +7.6 pp; primary difference +41.0 pp (95% +27.8 to +54.9), positive in both graph families | 48 roots (24 ring, 24 community), 2,688 valid | Opus 5.5 | same-researcher | [split-opus](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/sybil-split-opus/RESULTS.md) |
| 4 | Sybil-resistant accuracy depends on the truth being repeated; checks cannot recover scarce truth | Truthful carriers per rare fact 81 to 1: accuracy 100.0% to 4.2%, -95.8 pp (95% -100.0 to -88.9). Newcomer sleeper attack: accuracy never exceeded the share of truth in admitted packets; policy ranking unchanged across Haiku, Sonnet, Opus | 24 roots, 1,440 valid; newcomer 24 roots, 1,944 per model | Opus 5.5; Haiku, Sonnet, Opus | same-researcher | [scarcity-opus](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/sybil-scarcity-opus/RESULTS.md), [newcomer-opus](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/sybil-newcomer-opus/RESULTS.md) |
| 5 | A profit-seeking agent splits into a second firm when the rule is attached to firm identity, not when it is attached to the owner | Registered a second firm and sustained evasion: firm-regulated 6/6, owner-regulated 0/6, unregulated 0/6. Same result on two models and two disjoint task sets. The rules and a registration action are in the prompt: this shows use of an affordance in plain view, not discovery of a hidden loophole | 6 market tasks per model, 36 episodes each | Sonnet 4.6 (tasks 36-41), Opus 5.5 (fresh tasks 110-115) | same-researcher | [market-split-api](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/market-split-api/RESULTS.md), [market-split-opus](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/market-split-opus/RESULTS.md) |
| 6 | Agents count copied reports as independent evidence | Quorum of Mirrors Q1-02: 16/16 valid responses, 0/8 correct on graded full-lineage cases (gate 7/8); every choice tracked the copied-report majority | 8 graded cases | Jev 1.13 (typesafe) | owner, review waived | [Q1-02 post-mortem](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/vishesh/notes/decision-models/quorum-of-mirrors/reviews/Q1-02-post.md) |
| 7 | Team evidence acquisition repeats itself | Phantom Coast PC-2: under misleading reports and no audit, a three-proposal team covered 2.50 distinct cells in 12 sensing slots, single agents 3.25, uniform sampling 12. Every directly inspected cell was classified correctly | 8 roots, 96 episodes, 1,791/1,792 valid calls | Jev 1.13 (typesafe) | owner, review waived | [PC-2](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/vishesh/notes/phantom-coast/pc2/README.md) |
| 8 | Heterogeneous memory as a rescue after capture does not generalise across models (negative) | After purging a committed minority: gpt-4o-mini recovers only in mixed-memory populations (exact p = 0.0003); gemma-3-27b recovers in no cell; qwen3-235b recovers only with pure short memory (0.38) and mixtures dilute it (0.09 to 0.23). Reporting defects found by dmarz's review are being corrected | 12 to 24 tasks per cell per model | gpt-4o-mini, gemma-3-27b, qwen3-235b | cross-researcher (dmarz review) | [capture-memory-mix](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/shadow/notes/capture-memory-mix/README.md), [review evidence](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/latest-results-review-2026-10-04/evidence.json) |
| 9 | Meta-finding about our own pipeline: ordinary-task qualification fails often, and "done" is not success | 9 of 13 model-executed study families had a documented baseline-gate failure at some point (an ever-observed family count, not a current failure rate). Compositional-safety Q0-004: 10 of 24 episodes safe-complete; 10 episodes chose `inspect` for all 40 turns | 13 study families; 24 episodes | several | dmarz audit across both researchers | [completion audit](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/completion-audit-2026-10-04/README.md), [prevalence](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/completion-audit-2026-10-04/PREVALENCE.md) |
| 10 | Interface, not reasoning, decided a "cultural inheritance" score | Swarm of Theseus D1, strict score: legacy prompt 40/96, clean executor 82/96, keyed evidence 88/96, no notebook 89/96, one case per call 96/96 (8x the calls, 2.51x the cost of no-notebook) | 3 worlds, 480 dependent decisions | Haiku 4.5 | owner, review waived | [Theseus D1](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/RESULTS-D1.md) |

## Reviews that changed what we claim

- dmarz's [latest-results review](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/dmarz/notes/latest-results-review-2026-10-04/evidence.json)
  graded 14 results across all three researchers, including "mixture rescue does not generalize" for shadow's
  capture-memory-mix, and listed its reporting defects (327 raw records with 127 invalid reduced to 180 by
  last-valid selection, an inconsistent retry statement, a round-number caption mismatch, one hub fraction above 1).
- shadow's [review of the discussion benchmark v3](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/shadow/notes/review-discussion-benchmark-v3.md)
  found a vote-scoring defect and a dropped provider-failure reason before the paid run (verdict pass-with-fixes).
- vishesh's [PI review](https://github.com/dmarzzz/swarm-lab/blob/b8d90f52/researchers/vishesh/notes/pi-review-2026-10-04/README.md)
  lists 57 evidence, implementation and presentation findings across the project.

## What is not here

- No result from the in-the-wild datasets the organisers pointed at (AI Village, collusion.wiki, SwarmTraces,
  Transluce). The team built and used a controlled-experiment pipeline instead.
- Several runs were still collecting at this draft (see [STATUS.md](https://github.com/dmarzzz/swarm-lab/blob/main/STATUS.md)
  and [swarm-live](https://swarm-live.pages.dev)). Partial results are not listed.
- Costs: per-study model spend is in each results file (for example market-split-opus USD 14.95 for S1,
  sybil-scale-opus USD 93.44 total, sybil-scarcity-opus USD 141.14 total). No team-wide total is given here
  because the ledgers are per study and per account.
