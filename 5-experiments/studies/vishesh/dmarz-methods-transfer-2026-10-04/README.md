# What to borrow from Dmarz's market experiments

**Adopt the experimental controls and failure diagnostics. Do not copy the large grids or treat simulated populations as independent model agents.**

Reviewed 2026-10-04 by vishesh/codex-pi-review at repository revision `1d15f2a057a9e9c44f8d379263da734b1add8dcd`. This is a targeted transfer review of market results, adjacent diagnostics and pipeline lessons, not a full audit of every Dmarz file or a new literature survey. New commits after this cutoff are outside the assessment. [Source inventory](sources.json) pins the documents and saved data.

**Green = incorporate in planning now. Yellow = useful prospective option, needs study-specific validation and owner approval before a run. Red = unsupported inference or practice to avoid.** These colors describe the transfer decision, not experiment confidence.

| Decision | Borrow | Practical benefit |
|---|---|---|
| Green | Fixed-resource comparisons and explicit conservation checks | Distinguish more identities from more evidence, capacity or compute |
| Green | Trace evidence from acquisition through admission, interpretation and action | Locate the bottleneck before changing models or adding agents |
| Green | Interface probe, semantic qualification and end-to-end failure rehearsal | Find cheap interface defects before a large run; prevent failed gates from dispatching |
| Green | Same saved packets for model comparisons; separate model/configuration cohorts | Avoid mistaking different inputs for a model effect |
| Green | Report correct, wrong and abstained outcomes; absolute levels beside changes | Prevent a favorable score from hiding lost service or dangerous errors |
| Yellow | Scarcity/reliability stress tests, same-condition repeats and checkpoint forks | Test when an effect reverses and how large it is relative to model variability |
| Red | Automatic larger run at floor/ceiling; 180 owners described as n=180; blindly copying retry/logging code | Adds cost, false confidence or unsafe accounting |

## What the evidence actually supports

Scores below are this transfer review's scope-specific ordinal judgments using [the 0–4 rubric](../../../EVIDENCE-METADATA.md), not probabilities or replacements for the owning study's registry. Assessed by vishesh/codex-pi-review, 2026-10-04. Counts are observed unless explicitly planned. Model names/settings are those recorded by the studies, not a verification of current provider availability or pricing.

| Work and source | Evidence / sample-size summary | What is worth transferring | Main limit |
|---|---|---|---|
| Firm splitting, Opus ([M1](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/market-split-opus/RESULTS.md)) | **2/4**, narrow exploratory behavior: 6 market tasks, 36 episodes, 864 calls; firm-rule evasion 6/6, owner/no-rule 0/6 | Change the rule's aggregation unit while conserving ownership capacity; compare locked/flexible action spaces | One model owner against scripted rivals. The profitable operation and rule were explicitly supplied; not hidden-loophole discovery. Degenerate [1,1] bootstrap is not certainty |
| Fixed-resource Sybil splitting ([M2](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/sybil-split-opus/RESULTS.md), [C1](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/sybil-split-opus/src/sim.py)) | **2/4**: 48 roots across two graph families, 2,688 outcomes, 1,901 distinct packets; primary +41.0 pp, weak-check stress −52.8 pp | Fixed report/attachment budgets; paired policy-by-splitting interaction; adverse reliability stratum | Free internal links also vary with identity count; not pure identity count, not a published Sybil-defense benchmark |
| Knowledge scarcity ([M3](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/sybil-scarcity-opus/RESULTS.md)) | **2/4**: 24 roots ×60 conditions; accuracy 4.2% at one truthful carrier versus 100% at 81 | Vary truthful evidence redundancy independently of population and admission; retain which truth survives | One synthetic fact grammar; admission and synthesis both matter. Report-count behavior is an interpretation, not an isolated causal mechanism |
| Newcomer / sleeper attacks ([M4](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/sybil-newcomer-opus/RESULTS.md)) | **2/4**: 24 roots, 1,944 Opus outcomes; renewal−reputation +9.7 pp, reported interval −1.4 to +20.8 | Equal-cost random baseline; honest newcomer retention; false-output and evidence-availability diagnostics | Random outperformed renewal descriptively. Scripted trust/actors; synthesizer has no cross-round memory |
| Budget frontier and model scale replication ([M5](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/sybil-budget-sonnet/RESULTS.md), [M6](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/sybil-scale-opus/RESULTS.md)) | **2/4**, synthetic exploratory results: 24 roots per study, 2,880 budget or 2,400 scale outcomes per model cohort | Budget × reliability curves, paired model comparisons, accuracy/wrong/abstain decomposition | Tested-grid frontier is not monotone or universal; model settings differ. A higher-priced model need not improve the decision |
| Trust-credit ablation ([M7](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/trust-credit-qwen/RESULTS.md), [D6](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/trust-credit-qwen/reviews/chain-001-post.md)) | **1/4** for scripted mechanism: 24 roots ×21 cells =504 native answers; primary +20.75 attacker seats is computed before model calls | Equal total credit with direct/propagated rules; report level and slope together | At 32 strong checks direct seats 19.58 attackers versus 4.38 propagated. A smaller increase does not mean safer admission |
| Verification-cost repair ([D1](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/verify-cost-qwen/reviews/chain-002-post.md)) | **1/4**, failed competence: 12 layouts ×2 representations =24 valid decisions, 10 optimal; S1 unrun | Small action-cost diagnostic fields expose errors; stop failed qualification, keep both attempts | 15/24 swapped or approximately swapped costs; 23/24 choices follow written numbers. Different fixture sets and paired representations prevent a clean causal claim that the format worsened performance |
| Memory handoff ([D2](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/memory-handoff-qwen/reviews/chain-001-post.md), [P4](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/memory-handoff-qwen/README.md)) | **1/4** for qualification failure; **0/4** handoff benefit: 6 roots ×4 fixtures, 19/24 supported; S1 unrun | Separate origin/version checks from checking source content; clean, stale, misquoted, copied, contradictory and false-original states | A valid citation can support the wrong value; retrieving a false original cannot supply truth. One successor is not cultural transmission |
| Discussion D2 ([D3](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/discussion-dose/benchmark-v3/d2/RESULTS.md)) | **1/4**: 6 reused worlds, 72 calls across 3 configurations | Canonical fact tables and single-option feasibility checks isolate arithmetic from aggregation | Reused diagnostic worlds, not fresh qualification; model and reasoning settings change together |
| SOC-07 ([D4](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/soc07-private-judgments/reviews/s1l-post.md)) | **1/4**, descriptive ceiling: 8 roots per regime, 192 replay +240 live episodes, 4,752 calls | A prespecified information/futility check between cheap and expensive stages | All communicating arms reached 1.00. This gives little discrimination on timing of disclosure, not proof the intervention never matters |
| Compositional safety / scale XL interruptions ([D5](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/compositional-safety/reviews/p1-003-post.md), [P7](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/pipeline/sybil-scale-xl.md)) | **1/4** operational evidence: P1-003 28/168 episodes on one root; XL S1-a2 481 complete, 1 failed, 94 unstarted in this record | Shared-provider backpressure, safe error categories, preserved partial results and explicit resume semantics | These are dated interrupted attempts, not final efficacy results; pipeline summaries can lag native closeouts |
| Flagship 180-owner markets / cross-model packages ([P1](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/sybil-rules-180/README.md), [P2](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/sybil-split-xmodel/README.md), [P3](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/sybil-scarcity-xmodel/README.md), [P8](https://github.com/dmarzzz/swarm-lab/blob/1d15f2a057a9e9c44f8d379263da734b1add8dcd/researchers/dmarz/notes/pipeline/sybil-specialists-opus.md)) | **0/4** efficacy at cutoff: flagship qualification/probes only; split/scarcity cross-model packages unrun; specialists pipeline readiness is not a result | Common warm-up checkpoint; same-condition A/A′ noise reference; realistic capacity-transfer timing; byte-matched evidence | Flagship has one connected economy, not 180 independent replicates. Planned scale and stub tests are not native outcomes |

## Saved-data spot checks

[Reproduction code](spot_check.py) uses only the Python standard library, saved CSVs and saved episode rows; no provider calls, experimental sweeps or unopened holdouts. [Output](spot-check.json) records exact input hashes.

- Market: 36 distinct episode cells, 6 tasks, 864 calls, evasion 6/0/0, mean firm-rule flexible−locked profit **6,818.69**.
- Sybil split: **+40.9722 pp**, reversing to **−52.7778 pp** under weak checks; 48 complete root groups.
- Scarcity: **−95.8333 pp**; **288** matched groups have identical saved audit, admission and order hashes across carrier levels.
- Trust credit: **+20.75** scripted seats; the worse low-budget level for direct credit is reproduced.
- Verification repair: **10/24** optimal, **8/24** both costs correct, **11** exact swaps plus **4** swaps with zero, **23/24** choices follow the smaller written cost.

These independently recompute selected arithmetic from saved evaluations. They do **not** regrade every raw response, validate the simulator against reality, reproduce the reported bootstrap intervals or constitute an independent replication. Other rows above are documentary assessments.

## Adaptations and cautions

| Suggestion or inference to assess | Our disposition | Concrete correction |
|---|---|---|
| More/better models across the same full grid | **Adapt** | Start with the hardest necessary semantic qualification. Compare a small frozen set of informative boundary strata before proposing a full replication; record all configuration selection |
| Force controls into a 60–90% success band | **Adapt** | Distinguish a high clean-competence floor from a discriminating treatment task. Choose difficulty on development data; prospectively stop expensive escalation when the declared informative range is absent. Do not lower competence floors to manufacture effects |
| Working fields repair reasoning | **Reject as established** | They diagnose observable calculations; they also change the interface. Test a future format effect on matched fresh layouts under a new plan. The source's retrospective Fisher comparison ignores within-layout dependence and changed fixture sets; do not reuse its p-value as causal evidence |
| Direct trust is safer because its slope is smaller | **Reject** | Publish absolute harm, legitimate service retained and the change score side by side |
| Metadata/provenance establishes truth | **Reject** | Separate identity, version, content entailment and external correctness; evaluate false but faithfully cited originals |
| Retry 429/5xx or billing refusals automatically; retain raw error bodies | **Adapt cautiously** | Provider-specific evidence must establish whether execution occurred. Retain ambiguous exposure; never infer an unbilled request from HTTP status alone. Log allowlisted categories and numeric usage/headroom, not arbitrary bodies/headers. No adapter copied here |
| Byte-identical evidence means identical agent context | **Reject** | Split/scarcity cross-model packages add an answer-shape system paragraph and change structured-output enforcement. Pin evidence hashes AND full request/prompt/schema/settings; call the comparison a configuration effect |
| Fresh ledger per model/attempt | **Reject as new funds** | Separate cohorts may have subledgers, but one study's original cumulative spending authority must cover them all |
| Prepare packets before the machine is ready | **Adapt** | Precompute only authorized frozen inputs with sealed evaluator-only data and declared access timing. Do not inspect holdouts early; cache generation and delivery hashes separately |
| “Ready” queue or passing tests implies qualified evidence | **Reject** | Native post-mortem and records take precedence. Some embedded metadata still says unrun beside newer qualification results (for example memory handoff); record the discrepancy rather than inherit it |

## Where the changes belong

The linked notes are integrated into each owned study's navigation. They are prospective design inputs; they do not mutate frozen protocols or expand an already approved/queued attempt.

| Our study | Next useful adoption |
|---|---|
| [Quorum](../decision-models/quorum-of-mirrors/DESIGN-TRANSFER.md) | Distinct source roots versus copies, verified false originals and deterministic deduplication baseline |
| [Phantom Coast](../phantom-coast/pc5/DESIGN-TRANSFER.md) | Borrow Dmarz's direct extension of PC-5; avoid duplicating his grid; qualify risk-to-action mapping |
| [Right Dissenter](../dissent/DESIGN-TRANSFER.md) | Scarce checking budget, honest minority retention and equal-budget random/always-check controls |
| [Optimal Swarm Size](../optimal-swarm-size/DESIGN-TRANSFER.md) | Separate capacity, evidence supply and identity count; stop scaling before competence |
| [Heterogeneous Swarms](../heterogeneous-swarms/DESIGN-TRANSFER.md) | Choose diversity by measured error complementarity, not model labels |
| [Theseus](../swarm-of-theseus/v2/DESIGN-TRANSFER.md) | Origin/version versus content verification; retention and correction under identical checkpoint ancestry |
| [Immune Response](../immune-response-v3/evidence-study/DESIGN-TRANSFER.md) | Separate faithful receipts from safe repair; preserve healthy service and legitimate learning |
| [Influence](../influence-swarms/scenario/DESIGN-TRANSFER.md) | Trace extraction→check→decision→authorization; narrative/supplied strategy versus actual discovery |
| [Healing](../healing-helping-hands/c4/DESIGN-TRANSFER.md) | Validate selective routing near useful decision boundaries; keep strong central/Jev controls |
| [Antsy v6–v8](../antsy-targeted-v8/DESIGN-TRANSFER.md) | Measure checker reliability and correlated false acceptance; keep references/receipt clusters distinct |
| [Poietic](../poietic-agents/DESIGN-TRANSFER.md) | Resource conservation when capabilities split; account for idle transfer, caching, queueing and restoration |

**Recommended order:** finish existing saved-data diagnosis; then choose one bounded semantic qualification proposal in a blocked lane, or the already drafted Healing C4 routing question. Defer broad model grids and another large market simulation unless they resolve a specific remaining decision. Exact n, precision rationale, qualification allocation, current price/cumulative exposure and machine need belong in the chosen study's concrete owner-approved next-run plan. This review supplies no new launch or provisioning authority.

## Combined next-step decisions

[The consolidated PI decision table](../pi-next-decisions-2026-10-04/README.md) incorporates the separately supplied portfolio review, reconciles newer study records and supplies concrete outcome-dependent next steps. The source-pinned arithmetic and evidence judgments above retain their original cutoff.
