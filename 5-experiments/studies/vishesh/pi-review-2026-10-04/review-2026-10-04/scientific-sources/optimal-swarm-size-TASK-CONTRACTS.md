# Task contracts and qualification review packet

Author: vishesh/codex-idea-scores. 2026-10-04 UTC.

**Proposed design, not a registered experiment.** This extends [README.md](README.md) and [PROTOCOL.md](PROTOCOL.md). The examples below are hand-worked specification examples, not measured agent outcomes. No scorer, task generator, model runner or experiment is implemented here.

## Shared success contract

One assigned episode produces one final artifact. Record these independent facts: artifact well formed, substantive contract satisfied, received before deadline, actor expenditure within cap, physical-memory constraint satisfied where measurable, and execution failure class. Primary success is their conjunction. Missing, refused, malformed and incomplete submissions have primary success zero. A correct late artifact retains its substantive quality score while receiving primary success zero.

A deterministic evaluator sees ground truth and hidden checks after submission; actors do not. No LLM judge decides the primary outcome. Quality in [0,1] is secondary and family-specific; report it within family rather than asserting that one repaired test equals one correct evidence claim. Evaluator costs belong to the study budget, not to an actor's allowance. A scorer/infrastructure defect is separately classified and triggers protocol review; it is not silently reassigned to the model or omitted from reporting.

The budget clock begins before policy selection and ends at submission or hard stop. Completion at exactly the deadline is allowed when a monotonic receipt timestamp is less than or equal to D. An artifact generated earlier but received afterward is late. Usage at exactly the cap is allowed. Raw usage and timestamps remain available for audit rather than only rounded display values.

## Evidence dossier: structured reconciliation

**Practical task:** reconcile a bounded set of records into a checked operations report, such as inventory availability across several locations. Records use synthetic entities and integer units; no actual customer or financial data.

Actor-visible input contains source IDs, retrieval handles, a public schema, the reconciliation rules, the requested output fields and any uncertainty/abstention rule. The actor can retrieve every admissible source. Output is JSON containing one value or explicitly permitted `unknown` per requested field and the source IDs supporting it. Invented IDs, omitted fields, duplicate output keys and values outside the schema fail validity. An actor does not receive hidden expected answers or a generator's ground-truth graph.

For each output, the evaluator stores the required value and a family of acceptable evidence sets. Accept a citation set only if every cited source is admissible and the set satisfies a declared proof rule, not just because it contains the right source somewhere. For the initial deterministic fixtures, exact minimal evidence sets are enumerated; a citation dump fails. Where several independent proofs are legitimate, enumerate all of them or use a verified symbolic proof checker before qualification. Unsupported correct guesses do not count as verified answers.

Primary substantive success requires every requested value and every supporting evidence set to pass. Secondary quality is the fraction of requested fields satisfying both. Report value-only accuracy and citation validity separately so citation failures are not mistaken for arithmetic failures. Freeze whether a missing-data case permits `unknown`; never reward abstention when a complete derivation exists.

**Illustrative case, not a held-out root:** sources `s1: opening=12`, `s2: received=7`, `s3: reserved=4`. The public rule is `available=opening+received-reserved`. The output `available=15, source_ids=[s1,s2,s3]` passes; `15` with only `s1` fails grounding; `14` with all three fails correctness. Adding an unrelated `s4` fails the initial minimal-evidence contract even if the value is correct. Alternative-evidence tasks require an explicit broader rule before use.

Independent and linked structures vary whether an intermediate answer is needed by another requested answer. Hold source count, requested output count and primitive operation count fixed where possible; record differences that remain. Do not mistake more arithmetic or longer prompts for a dependency effect. The generator's dependency labels are evaluator-only unless the real task description explicitly exposes those dependencies.

## Repository repair: behavioral correctness and permitted scope

**Practical task:** fix a generated small software repository with a public bug report and public tests. The target language/runtime, dependency lock, allowed tools, sandbox limits and permitted file paths are part of the frozen manifest.

Actors receive an identical clean repository snapshot and public test command at every N. Hidden tests live outside the actor filesystem. No network, secrets or external side effects are needed. The output is a patch plus a machine-readable summary; execution occurs in a fresh evaluator sandbox. Changes to tests, evaluator configuration, dependencies or unapproved paths fail the scope contract. No-op patches may pass only if the public task explicitly permits a no-change resolution; initial fixtures require an actual bug repair.

Substantive success requires a patch that applies cleanly, satisfies the scope contract, passes every hidden required behavioral check, and preserves every designated regression invariant. Secondary quality is the fraction of prespecified behavioral categories passing, with equal category weights; validity/scope failure sets it to zero. Do not let a category with many near-duplicate tests dominate quality. Tests must probe behavior rather than a preferred patch spelling.

**Illustrative case:** public specification says `clamp(x, lo, hi)` returns x inside the inclusive interval and the nearest boundary outside. The broken implementation returns lo for any x below hi. For `(5,0,10)`, `(−2,0,10)`, `(12,0,10)`, the required results are `5,0,10`. A patch returning `5` unconditionally fails the latter cases. An equivalent correct implementation is allowed. Editing the tests to expect the broken behavior fails scope even if its visible suite passes. Invalid intervals and numeric types must have an explicit public contract before generating roots; they cannot be surprise hidden requirements.

For concurrent edits, each work item uses an isolated working copy based on a recorded base hash. A deterministic merge applies returned patches in item-ID order. Conflicts return to the coordinating context for charged resolution; no invisible human or reasoning agent merges them. The single agent has the same work-item/merge interface. Record merge attempts, conflicts and integration time. This rule is part of the solution method and its coordination costs, not an implementation convenience to remove selectively.

The parallel condition has independent module defects; the linked condition requires coordinated interface repairs. Match module/defect/test-category counts and report N=1 difficulty. Every root has its own generated identifiers and semantics; superficial paraphrases of the same root stay in one split.

## Incident triage: locked transfer contract

**Practical task:** diagnose a simulated service failure and propose an allowed repair sequence. Actor-visible tools return observations from a versioned deterministic service simulator; actions in this task are proposals, not commands against real infrastructure.

Substantive success requires an allowed diagnosis and a repair sequence that brings the simulator to its specified healthy state without violating safety invariants. Evaluate the sequence by state transitions rather than string matching one reference answer. Equivalent valid sequences must pass. Secondary quality reports prespecified restored-service fractions only for syntactically valid, permitted action sequences; unsafe/forbidden sequences score zero. An empty sequence passes only when the case contract permits a healthy/no-op case.

Freeze the contract and reviewer-visible development examples before the transfer generator and seed manifest are sealed. Do not publish or inspect transfer roots or expected diagnoses during tuning. This packet deliberately contains no transfer case. Evaluation may inspect the sealed truth after the frozen policies finish, as described in PROTOCOL.md.

## Fairness and information boundaries

| Item | All N values receive | Evaluator-only material |
| --- | --- | --- |
| Evidence | Same retrievable source union, public rules and output schema | Expected values, acceptable proof sets and latent dependency labels |
| Repository | Same base commit, bug report, public tests and tools | Hidden behavioral cases, regression oracle and ground-truth defect graph |
| Triage | Same observation interface, permitted repair actions and public health contract | Fault seed, transition oracle and held-out root manifest |

Each actor has the same per-context limit in a profile, but all contexts draw from one aggregate episode budget. More independent contexts can be a legitimate memory advantage of N; do not give them extra unique documents or uncharged summaries. A single agent can use the same retrieval, ledger and public test tools. Check the retrieval union directly in planned fixture tests rather than inferring equivalence from prompt length.

Distinguish the actor's proposed dependency graph from the evaluator's true one in traces and visualizations. Replay layouts may show actor plans by default. A separate hindsight overlay can show evaluator structure after completion, clearly labeled; it cannot enter selector features or actor prompts.

## Make the 80-episode qualification non-circular

The existing allocation is 2 families × 2 structures × 4 roots × 5 roster sizes = 80 episodes. It is a staged engineering qualification, not a matched size-effect study:

1. **Q-A: 16 single-agent calibration episodes.** One for each development root. Before any of these calls, pin the model/runtime, a generous but finite screening deadline and spending cap, turn/tool limits and an approved total stage ceiling. These cannot be inferred from results of the same runs. Deterministic reviewer fixtures and scorer mutation checks precede model calls.
2. **Calibration decision.** Proposed D0 is 1.5 times the nearest-rank 75th percentile of time to a contract-valid submission among successful Q-A episodes. Proposed B0 is 1.5 times the corresponding percentile of actual actor cost, computed separately. Require at least two successful roots out of four in every family/structure cell and at least eight successful roots overall before computing these pooled values. Publish all failures/censoring and label this as success-conditioned calibration. It is a proposed choice requiring review before Q-A, not a general statistical optimum.
3. **Q-B: 64 multi-agent engineering episodes.** The same development roots at N=2,4,8,16 under the resulting P0 envelope. Check metering, orchestration, scoring and trace completeness. These are not paired performance comparisons with the Q-A screening runs because their caps differ. Baseline-versus-swarm claims start only in the main matched core map on disjoint roots, where every N, including N=1, uses identical caps within a profile.

If the derived limits exceed the approved ceilings, stop for a scope/budget decision; do not silently clip them and call them the prescribed quantiles. If too few Q-A successes exist, record qualification failure and revise task difficulty/model choice prospectively. A replacement qualification attempt requires a new manifest, a separate quote and retention of earlier outcomes. No automatic repeat-until-pass allocation is included in the 80 episodes.

The success-conditioned calibration tends to favor solvable instances. Report that limitation and all Q-A success/failure counts. The matched core outcomes establish whether the chosen envelope is useful across its full assigned set. A ceiling/floor effect in core is a reported exploratory limitation; it does not authorize changing budgets after seeing transfer outcomes.

Four roots per cell cannot estimate a stable upper-tail service distribution. These quantiles set an exploratory operating point, not a service-level guarantee. Qualification pass certifies engineering readiness only, never superiority of a roster size.

## Proposed qualification acceptance checks

Before Q-A, independent review must verify oracle correctness, evidence access parity and scope isolation on hand-worked cases. Planned mutation cases must reject a correct unsupported answer, a wrong supported answer, a hard-coded repair, a forbidden file edit, a late correct answer and a malformed artifact. Also include multiple equivalent correct patches/proofs/actions, which must be accepted under their declared contracts.

Before core, require zero known accounting race, hidden-truth exposure, split-leakage or scorer validity defects; every assigned qualification episode must have a final outcome record with usage and timestamps, including failures. Trace gaps require a classified reason and must not erase an episode. At least one N>1 roster must produce a valid solution in each development family/structure cell. This is an engineering check, not a demand that every size win. Failure of N=16 under the budget is an informative infeasible candidate, not grounds to secretly expand its cap.

If scorer defects are found after model calls, preserve artifacts, version the corrected scorer and rescore all affected artifacts when possible. Report which judgments changed. Rerun only when recorded outputs cannot answer the corrected question, under a new approved attempt. Preserve execution outcomes separately from compliance findings.

## Remaining decisions before implementation

The contract is now specific enough to review, but the generator distributions and exact prompts still need specification. The budget quote requires a pinned model/provider or local runtime, metering/pricing basis, screening ceilings and stage cap. The task-family survey/hypothesis gates and independent design review remain incomplete. These are launch prerequisites, not reasons to fabricate a cost estimate or claim a pilot has started.

