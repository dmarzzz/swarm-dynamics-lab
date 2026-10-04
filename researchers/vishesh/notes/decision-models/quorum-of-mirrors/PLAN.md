# Quorum of Mirrors: QM-2 design

2026-10-04. Owner: vishesh/codex-quorum-mirrors. Exploratory design, written before its offline reference implementation. No accepted hypothesis, native qualification or Quorum of Mirrors result exists in the inspected repository. This is a revision of DM-02, not adaptive-quorum. Publication of this document alone is not run registration or launch clearance.

## Question and practical decision

Can a source-aware decision instruction reduce errors caused by uneven repetition of the same evidence when some ancestry is unavailable? The practical output is a decision about whether to invest in provenance capture before adding more judges. A later, separately priced comparison will ask whether to buy an observation or another judgment. Neither effect is assumed.

Primary comparison: change in the source-aware-minus-standard accuracy difference between skewed and balanced repetition, reported separately for full and partial ancestry. Distinct observations, report slots, judges and call ceilings remain fixed. A secondary lineage interaction tests whether the defense loses value when ancestry is concealed. This identifies the effect of the instruction package in this synthetic task, not a universal optimal swarm size or a uniquely Jev failure.

## Evidence audit and revisions

The handoff at upstream c1aca0b29b7f5fca0e84f32aef0373563341fde3 records no native qualification or scientific outcome. The local scientific review, SCI-QUORUM-OF-MIRRORS, calls out missing generative dependence, partial-lineage contracts, resource estimands and calibration. Prior design language conflated changing overlap with fixed distinct evidence. QM-2 uses a fixed set of three roots and manipulates their multiplicities instead. A different-root-count comparison is deferred and must be labelled an information acquisition contrast.

The survey remains in progress. The current gate reports zero of five full paper reads and zero of eight structured search rounds; no accepted hypothesis exists. Earlier literature summaries retain their actual reading depths. This revision supplies no new novelty claim or independent research review.

## World and observation contract

A world is a binary incident diagnosis Y with prior P(Y=1)=1/2. Two prespecified difficulty strata have sensor accuracy q=0.65 or 0.80. Generate three root observations X1,X2,X3 independently conditional on Y and q, with P(Xi=Y)=q. All roots within a world use the same declared q. Root IDs name observations, not organizations; the conditional-independence assumption is explicit and disclosed to actors. Different organizations do not imply independence in reality.

For every root realization, construct nine reports in two paired conditions:

- Balanced: multiplicities (3,3,3).
- Skewed: multiplicities (7,1,1), with the favored root selected uniformly without consulting Y or observed signs.

All three roots remain represented. Each report preserves its root's bit and q. Permute report order independently of truth and retain the permutation. Report IDs and root IDs are opaque, do not encode truth, and use separate namespaces. Exact copies with distinct transport IDs are the initial condition; no model-generated paraphrases. A later frozen template restatement control must prove semantic equivalence before use.

Full lineage exposes the root ID for every report. Partial lineage selects two of the three roots uniformly without replacement, independently of truth and favored-root choice, then replaces their root IDs on every descendant with null. Revision during offline design review: hiding only one root made the capped heuristic recover its likelihood contribution exactly; two concealed roots create a real information-loss tradeoff. The mask is paired across repetition and policy arms. The actor is told that ancestry is incomplete and opaque reports may share ancestors with other reports. Neither hidden root ID nor number of actual hidden roots is disclosed. Consequently an actor cannot identify every independent observation; this is an information limit. The evaluator retains the complete ancestry graph separately.

The exact full-information posterior is logistic(sum over distinct roots of (2Xi-1)*log(q/(1-q)))). It is exact only under the declared conditional-independence generator. Shared-sensor/common-cause dependence is a required later robustness study with its own generator and likelihood; do not apply this formula there as an oracle. The offline reference checks the specified grammar, not natural-language reasoning.

## Actors, policies and comparisons

Five judges, two scheduled decision rounds, no tool access and no persistent cross-world memory. At round 0 each judge sees the same nine-report packet and the same task criteria, with prespecified judge-specific order permutations reused across policies. At round 1 each receives that packet plus all five round-0 decisions. Use a barrier: no judge sees another round-1 output. No new evidence enters at round 1. Every response is a strict object with choice ZERO, ONE or DEFER and a probability p_one in [0,1]. Peer messages contain only valid typed choices and probabilities, with failures marked unavailable. No free-text rationale channel in QM-2.

Standard instruction: assess the reports and peer decisions against the task criteria. Source-aware instruction: additionally count repeated visible root IDs once, treat peer agreement as no new measurement, and explicitly acknowledge unresolved ancestry. Both receive exactly the same factual payload and output schema. Preserve exact prompts. This tests a prompt intervention, not a separately verified deduplication algorithm. Both arms have equal maximum calls and output tokens; input tokens and actual consumption are measured, not claimed equal. Primary timing is logical round; provider latency is an operational metric.

The committee commits ZERO or ONE only if at least three of the five scheduled judges support it. DEFER, malformed and missing responses do not shrink the quorum. Report all five slots. No commitment is DEFER, with failure status retained separately. Majority is the aggregation rule in both instruction arms.

Comparators:

| Comparator | Information and purpose | Cost interpretation |
|---|---|---|
| Round-0 committee | Same private decisions before communication | No-discussion diagnostic, five calls; shared collection cost counted once |
| Pooled solver | Same nine reports and lineage; two self-review calls, no peers | Lower-call reference; not falsely described as matched model compute |
| Naive accumulator | Treat each report as independent | Deliberately misspecified dependence reference, zero model calls |
| Visible-source accumulator | Count known roots once; opaque reports separately | Implementable deduplication baseline; output is a score under uncertain lineage, not a calibrated posterior |
| Capped opaque accumulator | Known roots once; total opaque signed log-odds clipped to one observation's log-odds magnitude | Conservative implementable heuristic; can discard genuinely new information |
| Exact root oracle | True root graph, three independent likelihood contributions | Evaluator-only ceiling; never a defense given hidden truth |

The main design has 2 repetition x 2 lineage x 2 instructions = 8 trajectories per world, each ten model calls. Four pooled trajectories add eight calls. The no-discussion comparison is obtained at round 0 without extra calls. Total main-screen ceiling is 88 calls per world, excluding separately budgeted competence and provider-repeat checks. Deterministic comparators consume no model calls. Equal ceilings do not establish equal realized cost or latency.

## Metrics and uncertainty

Primary endpoint is correct committed decisions / all assigned worlds for each arm. DEFER, unavailable and unstarted worlds contribute zero correct commitments. Also report wrong commitments, defer, validity and execution completion separately so unavailable execution cannot be confused with scientific failure.

Paired primary effect within each lineage stratum: (source-aware correct - standard correct) under skewed repetition minus that difference under balanced repetition. Report both underlying policy differences; a favorable interaction alone can hide an inferior intervention. Analyze worlds, never judge calls, as independent units. Resample complete world blocks for a paired interval after a sufficiently sized study; qualification is descriptive. Average difficulty strata with declared equal weights, retaining stratum estimates. A later power calculation must use a development estimate of world-level paired variance and a declared useful-effect threshold before held-out assignment.

Secondary: wrong unanimity / all assigned worlds (requires five valid matching wrong choices); agreement among all five scheduled slots; Brier score on valid p_one with valid-count denominator plus missing fraction; selective error at fixed probability thresholds 0.6, 0.8, 0.9 with coverage; round-0 to round-1 probability change without new observations; tokens, reports, root observations, calls, latency and cost. Do not call returned distributions calibrated. Fit any calibration on a separate calibration split, freeze it, and evaluate Brier/reliability on untouched cases; no accuracy-selected binning or thresholds.

A useful deployment recommendation requires the underlying accuracy gain, wrong-commitment change and resource cost together, with an explicit loss sensitivity. Report loss = wrong_commitments + d*deferrals for d in {0.1,0.25,0.5}; failures are reported separately and included as unresolved in this loss. These are illustrative preferences, not real incident costs. A defense that abstains everywhere cannot appear best merely by dropping unanswered cases.

## Staging and acceptance

1. Offline contract validation only: duplicate invariance of full-root accumulation; naive sensitivity; hand-derived posterior; truth/hidden-ancestry isolation; opaque ambiguity; fixed quorum and denominator; corrupt ancestry rejected. This is software testing, not an experiment run.
2. After gates: separate clean-task qualification with both labels, both q strata, mixed signs and permuted identifiers; valid responses >=95%, clean full-lineage choice agreement with exact MAP >=85% overall and >=75% in every label-by-q cell. Record counts and uncertainty; these are provisional screening criteria, not evidence of efficacy. On clean cases require ZERO/ONE; ties do not arise with three equally reliable roots. Qualification partitions must be fixed before dispatch.
3. Separate provider-repeat probes compare identical requests without changing evidence to measure service variability. Model identity, interface distribution semantics, usage accounting, failure classes and request isolation must pass before a scientific comparison. No result-selected retries.
4. A small paired native screen can then test whether the mechanism discriminates. Valid null or adverse results remain results. If ordinary deduplication explains everything, publish that narrow result. If baseline task competence fails, repair on development cases and use fresh qualification cases.

Development seeds 11000-11099 are reserved for instrument work. Qualification 21000-21099, calibration 31000-31099 and held-out study 61000-61999 are reserved, not generated or inspected in this revision. Reserved ranges are not approved sample sizes. The future run manifest must select exact seeds, cells, counts, model snapshot, prompt hashes, token caps, retry ceiling, wall deadline and maximum authorized spend before dispatch. This document intentionally does not invent a paid sample size or budget.

## Later practical extensions

The Right Dissenter: fork a frozen pre-injection checkpoint; compare no new source, a copy and a fresh q-reliable source using identical presentation and decision opportunities. Report correct and incorrect fresh measurements separately without revealing that classification to actors. Either enumerate both measurement outcomes and weight by their generator probabilities, or sample naturally and retain all cases; do not pool artificially balanced cases as natural prevalence. RD-1 owns challenge admission and withdrawal; this experiment owns evidence dependence.

The Next Observation: compare another q-reliable source with another model judgment at explicitly priced total budgets. Observation count necessarily changes. Use measured call cost and latency and a range of observation prices; publish a cost-quality frontier. Do not merge this estimand into QM-2 or generalize it to optimal swarm size.

Common-cause errors, unknown reliability, factual restatements and domain transfer are later robustness questions. A clear synthetic success does not establish them. They must not be silently added after inspecting held-out effects.

## Visualization mapping QM-V2

Each future attempt binds this mapping to its own run ID, world, arm, seed and version hashes. Saved events are the sole source for visuals; this revision implements neither a native replay nor live reporting.

| Signal | Encoding and denominator | Access / missing states |
|---|---|---|
| report_id, visible_root, bit | Nine report cards; visible ancestry links | Actor-visible; missing lineage shown as unknown |
| true_root | Revealable ancestry overlay | Evaluator-only; never in request serializer |
| round, judge_slot, choice, p_one | Five fixed judge rows on two-round timeline | Pending, DEFER, invalid and timeout are distinct |
| correct, unanimous_wrong | Separate truth overlay and world outcome panel | Evaluator-only; no fabricated decisions |
| assigned, completed, committed | Counters with all-assigned denominator | Unstarted cases remain visible |
| calls, tokens, latency | Separate cost panel | Missing usage marked unknown, never zero |

Render after round barriers and at terminal failure, using logical rounds as the primary time axis and wall time as a separate display. Retain every report exposure, request hash, model result, status and aggregation event with stable IDs. No downsampling of these two-round traces. Planned bounds: three frames per trajectory, maximum 200 KB/frame, render overhead timed separately. Replay supports play/pause, step and arm comparison; static final-frame fallback includes a visible event cursor. Validate initial, post-discussion and failure frames against saved events and exact metric counts, plus actual browser playback. Color is redundant with text/shape. The illustrative fixture is never labelled a run. Public artifacts contain only synthetic IDs and evidence, no credentials or fleet addresses. DMars/CD owns Swarm Live deployment.

## Launch boundary

No live adapter or runnable native study is delivered in this revision. Before any run: complete applicable research gates, independent review, pre-run assessment, immutable readable public plan, condition-specific TLDR registration and public-page verification, exact frozen assignment manifest, exclusive authorized host and experiment-specific spending authorization. Default paid budget is zero. Publication is not registration. Offline tests need no fleet allocation. Future implementation must refuse dispatch on absent or mismatched receipts and retain failures and previous attempts.

A condition TLDR must spell out question; standard/source-aware instruction; balanced/skewed repetition; full/partial ancestry; comparator; all-assigned accuracy and wrong commitments; and synthetic-task/unknown-lineage limitations. Eight condition-specific registrations may reference one immutable plan, but cannot share a generic TLDR that hides the treatment.

## S0 preparation amendment, 2026-10-04

The shared worker template explicitly allows exploratory S0/S1 under owned notes before formal gate completion; S2 remains closed. The owner requested that established drill. [QM-S0-01](reviews/S0-01-pre.md) is the first bounded competence screen and supersedes this document's blanket statement that all native diagnostics wait for the survey gate. Public registration, allocation and separate budget requirements remain. No result or independent review is implied.

The inspected Jev native interface returns probabilities over typed choices, including DEFER. Such a score is not a binary-world posterior. For this backend, preserve raw choice scores and use them only as diagnostics; defer the proposed Brier/calibration endpoint until a separately validated binary probability elicitation contract exists. S0 uses exact MAP choice correctness and repeat agreement.
