# Reliable reopening under historical decisions and majority ballots

**Execution authorization update, 2026-10-04:** The owner approved this defined 18-request Q0 and conditional 144-request D0 scope, lifetime stop 650, within the unchanged cumulative USD 1 API / USD 1 infrastructure caps. The native implementation and 73 offline checks are complete. This update supersedes the earlier draft-status and implementation-pending statements below; the scientific inputs, assignment order, controls, endpoints, qualification threshold and stopping rules are unchanged. Actual launch still requires current admission evidence. See [run status](RUN-STATUS.md).

Prospective development diagnostic, RD6 Q0 and conditional D0. Written 2026-10-04 before implementing these cases. Owner and assessor: vishesh/codex-decision-models. **Draft for an owner decision; no native attempt is authorized or scheduled.** The authoritative study setup remains [RD5 SETUP](../rd5/SETUP.md); this is a versioned successor within Right Dissenter, with the original cumulative ledger. Researcher review is not required by owner direction.

## TLDR

Test whether an otherwise answerable decision becomes unreliable when an earlier opposite decision, opposing majority ballots, or time metadata accompanies new evidence. Deliver the evidence directly so acquisition policy cannot explain the result. Compare full context with source-only context, then isolate history, ballots, absolute clock and evidence age. Use correct action, wrong commitment, justified abstention and repeated-answer disagreement as separate outcomes. Proposed maximum: 18 qualification requests followed by 144 diagnostic requests, with no retries or subsequent policy experiment. All cases are authored development fixtures; this is neither an untouched holdout nor a population or emergent-swarm evaluation.

## Question and prediction

**On fixed answerable cases, does adding historical action and scripted opposing ballots reduce correct interpretation of current evidence, and which context component explains any observed loss?** Primary contrast: full context minus source-only correctness, paired within each case. A negative contrast would establish sensitivity for these inputs; it would not identify an internal cognitive mechanism or field failure rate.

The trace-motivated prediction is that some resume cases will degrade under full context. Stop cases test the opposite direction. Clock translation should preserve the answer when every absolute timestamp moves equally; an evidence-age change that remains within the declared freshness limit should also preserve the answer in these noiseless tasks. Same-input repeats measure observed response variability, not extra independent worlds. A null result is useful: it would not justify prompt repair or another reserve sweep.

## What the preceding experiments established

RD5 completed all 72 dependent decisions and 36 main-stage calls. Memory scored 8/24, fixed reservation 6/24; four decisive resume requests returned DEFER. Qualification passed 24/24 but lacked history and ballots. The retrospective numeric reference scored 6/10/12, showing a simple controller is sufficient for these authored semantics. The urgent-resume request difference combined clock and evidence age; it was not a causal ablation. [Report](../rd5/REPORT.md), [post-mortem](../rd5/reviews/H5-A1-POST.md), [quality assessment](../rd5/reviews/H5-A1-QUALITY.json), [saved difference](../rd5/results/h5-a1/urgent-resume-context-diff.json).

Keep RD5 closed as a valid adverse result. Its frozen plan, runtime, qualification and outputs remain unchanged. This diagnostic concerns interpreter behavior, not an attempt to recover a favorable reserve result. Source/prompt/route changes are new configuration choices, never retroactive repairs to RD5.

| Prior suggestion | Decision and reason |
| --- | --- |
| Run a bigger reserve comparison | Reject now. Interpretation is an unresolved bottleneck, and the fixed reserve already has a useful adverse result. |
| Qualify in the complete intended context | Adopt before any future policy comparison. Here, context competence is the diagnostic outcome; failure is retained, not a reason to select easier cases. |
| Isolate history, ballots, clock and age | Adopt with exact delivered-request differences and fixed action ordering. |
| More realistic, unseen scenarios | Build concrete new development cases now. Independently sourced, untouched evaluation is a later prerequisite for generalization; do not relabel inspected fixtures as held out. |
| Better precision through more calls | Revise. Repeated requests measure local variability; independent scenario diversity requires a different sample. This small stage has no population precision claim. |
| Use a simple rule as the main baseline | Adopt. It is the practical default for this finite grammar, and a semantic reference for checking labels. Native calls can only diagnose susceptibility, not demonstrate necessity of Jev. |

Existing [source and social map](../SOURCES.md) and [method-transfer review](../DESIGN-TRANSFER.md) motivate evidence-aware dissent and equal-resource controls. No new literature search or novelty claim is made here. Broader research promotion remains subject to the applicable prior-art process.

## Setup

One native Jev resolver per request, freshly initialized with no conversation, tools, hidden memory or cross-request state. Retain the RD5 model and requested provider route, with no fallback; verify the actual snapshot and price again before any future run. Scripted historical action and five supplied ballots are explicit treatment inputs. There are no independently reasoning peer agents. Native actor count is one, not five or six.

The fixture builder reuses the frozen RD5 literal card extractor and request schema, then sets action order by case identity alone. RD5 derives action order from a task hash containing time; allowing it to change across clock variants would confound the comparison. The new case-locked ordering is counterbalanced across cases and remains identical across all variants and repeats of a case. The question wording is common to every condition; only the declared fields below vary.

Three semantic domains use the existing finite grammar: a process reading inside inclusive bounds, a certified bridge capacity sufficient for the stated load, and a required compatibility test whose optional telemetry is irrelevant. Two base task specifications per domain give six authored semantic families. Each has a reciprocal stop/resume pair, for 12 answerable cases. Include threshold-equality examples and optional-test disagreement. Values and IDs differ from RD5; grammar reuse is explicit and does not establish independence.

For each case, an earlier verified action and four of five ballots oppose what the new source establishes. The historical receipt predates the new source in every condition. Its historical validity is distinct from current authorization, which begins DEFER in all conditions. The full source, extracted literal spans, scope, version and timestamps are present. Evaluator action, family, direction, treatment name, assignment ID, repeat number and future information are excluded from actor payloads.

| Condition | History | Ballots | Time transformation | Comparator |
| --- | --- | --- | --- | --- |
| C00 source only | none | none | now 100, observation 99 | clean interpretation |
| C10 history only | earlier opposite action | none | unchanged | C00 |
| C01 ballots only | none | four opposite, one aligned | unchanged | C00 |
| C11 full context | same history | same ballots | unchanged | C00 primary; C10/C01 components |
| CT translated clock | same history | same ballots | add 100 to now, observation, historical observation/expiry, deadline and horizon; keep TTL and all durations fixed | C11 |
| CA older valid evidence | same history | same ballots | observation 99 to 97 in source and card only; now, history and deadline unchanged | C11 |

TTL is 7, historical observation 95 and expiry 102, deadline 101 and horizon 108. Both current observations (99 or 97) are newer than history and still fresh. Trusted observations are noiseless within TTL in this diagnostic; age is not assigned hidden evidential quality. Clock shifts alter no strings, action order or source values. Ballot removal is an intended content intervention, so any effect concerns the presence of that complete field; it does not separately identify content versus extra input length.

## Scenario and sample allocation

| Stage | Cases and nesting | Requests | Purpose |
| --- | --- | ---: | --- |
| Q0 clean competence | 12 separate answerable qualification cases, balanced stop/resume and domain; source-only, once each | 12 | Check the common task/card/action contract |
| Q0 uncertainty controls | six separate cases: stale-only and same-time conflicting sources in each domain, with full history/ballots | 6 | Check warranted DEFER and resistance to unsupported commitment |
| D0 context diagnostic | 12 development cases × six conditions × two identical-input repeats | 144 | Paired context contrasts and local response disagreement |
| Maximum | 18 Q0 plus conditional 144 D0 | **162** | No extra probes, repair calls or judging models |

The primary unit is an authored case, nested in six shared semantic families. Stop/resume partners share a task rule. There are no independently sampled field tasks; 144 answers are not n=144. Qualification cases are disjoint by effective source/task content, but use the same finite grammars and are not an independent semantic holdout.

The allocation covers every domain, direction and context component with two answers per identical packet. It is chosen for a bounded diagnostic, not statistical power. A second answer only detects some local variability; agreement does not establish reproducibility. Report every case and family contrast, domain/direction strata and the finite-cohort total; do not publish population confidence intervals or significance claims. A broader study must first define its source population, smallest useful difference and independent sample/precision rationale. No such stage is included here.

All generated inputs are inspected development material. No sealed holdout exists for this draft. A later generalization study would require new independently sourced or authored task families, frozen before model selection, and appropriate held-out qualification and evaluation. Renaming IDs is insufficient.

## Protocol

1. Publish this prospective plan before writing the builder. Construct the cases, actor/evaluator separation, fixed condition masks, literal reference, assignment manifest and scorer offline. Use known-answer and deliberately wrong policy fixtures; they are software checks, not model results.
2. Freeze the full plan, generator, inherited extractor/request dependency hashes, request order, response contract and scoring definitions. Fix seed 62004. Interleave D0 cases and conditions in two independently shuffled repeat blocks; every cell appears once per block. Repeats have distinct assignment identities but exactly identical actor requests. No response cache or shared native answer tape.
3. After a concrete owner decision, implement and validate the native execution integration against this contract. Preserve the original ledger and old duplicate fences. A request hash alone cannot identify repeats; ledger keys must include stage/assignment identity. The current draft contains no native launcher or functioning admission receipt.
4. Obtain fresh exclusive approved-account allocation only after scope approval and runtime readiness. Publish/register an immutable readable plan and condition TLDRs. Verify account/resource, source/runtime, public page, snapshot, original ledger and real relay health. Register Q0 separately from conditional D0. No paid provider smoke call sits outside the 162 requests.
5. Run Q0 once, requiring all 18 valid and correct, including six DEFER controls. A failure or missing result closes Q0 without D0. Preserve its actual outputs and write the post-mortem; no automatic repair batch. This is a clean/uncertainty qualification only, never claimed as full-context decisive competence.
6. If Q0 passes, complete its review, refresh D0 admission and run the entire 144-request diagnostic once. Context-induced errors are intended measurements and do not trigger easier replacement cases. The D0 clean C00 answers are collected in the same randomized blocks as the other conditions, not borrowed from the earlier Q0 stage.
7. Stop dispatch on the first ambiguous, invalid-route/schema or provider failure, expired admission, quota excess or lease loss. Preserve the failed assignment and all later unstarted assignments; never silently retry. No automatic resume. A later continuation would require its own assessment and unchanged original accounting.
8. Retain append-only per-assignment before/after events: exact request/hash and order; full visible validated response; requested/served route; reservation, usage, latency and terminal state. Keep safe allowlisted errors, never arbitrary headers, secrets or operator conversations. This stateless diagnostic has no hidden evolving trajectory to reconstruct.
9. Reconcile assigned/started/terminal/valid/graded/analyzed counts, inspect every miss and all repeated disagreements, recompute scores independently from actions and labels, verify figures and uploaded bytes, then finalize operationally and complete the eleven-dimension scientific post-mortem. Stop workers and release the allocation. No successor auto-dispatch.

## Metrics

Primary: the mean paired difference in action correctness, C11 minus C00, over the 12 cases, averaging the two repeats within each case. Also show both counts out of 24 assigned responses. Correctness requires the declared action from the current available source. Do not silently pool Q0 with D0.

Report PROCEED/HOLD/DEFER, wrong PROCEED, unnecessary HOLD, unexpected DEFER and valid/invalid/unstarted separately. Q0 stale/conflict cases require DEFER; D0 answerable cases count DEFER as unresolved service. There is one terminal judgment per assignment; no four-epoch propagation inflates the number of interpretation failures.

Secondary descriptive contrasts: C10−C00, C01−C00, the combined-context interaction, CT−C11 and CA−C11. Report by stop/resume and domain without treating six contrasts as independent discoveries. The manipulation isolates delivered field changes, not latent model mechanisms. Clock and age probes are deliberately separate.

Repeated-input disagreement: number of cells whose two valid actions differ / cells with two valid responses, alongside paired-cell completeness / 72. Missing answers never become agreement. Preserve all 144 assignments in completion reporting. For each paired effect, bound missing correctness as either 0 or 1 instead of assigning an unknown paired difference zero. Report strict all-assigned correct fraction as an operational quantity, and valid-only accuracy as secondary.

The deterministic literal rule is computed from actor-visible source, applicability and task thresholds; no treatment label or evaluator action enters it. It should solve all declared fixtures, including uncertainty controls. This establishes label consistency in the finite grammar, not a general semantic baseline or native result. The model is being evaluated for context susceptibility; it has no demonstrated advantage over this controller.

## Decisions and stopping after the diagnostic

| Outcome | Decision |
| --- | --- |
| Repeated full-context degradation while all 24 C00 answers are correct | Localize affected components/cases; draft one narrowly justified interface repair for a separate evaluation. A reproducible pattern means both C00 repeats correct and both relevant context repeats wrong in at least two cases from different base families; this is an engineering trigger, not a significance test. |
| No consistent degradation and high correctness | Finish the component diagnostic. Do not enlarge the grid merely to reproduce RD5 errors; use the simple controller for these tasks. |
| Mixed directions or repeated-answer disagreement | Report the instability and all contrasts; do not assert a single mechanism. A fixed packet replication would answer a different, separately planned reliability question. |
| Q0 failure or D0 clean errors | Record a competence limitation. Context contrasts remain descriptive, but do not claim that a cleanly competent model was degraded. No allocation-policy escalation. |
| Transport/missingness prevents a decision | Close as incomplete with bounds and exact missing assignments. A provider failure is not inability to interpret evidence. |

Neither a positive nor a negative diagnostic supports an emergent swarm claim. A future collective study would need actual peer information exchange and controls for reconsideration, added compute and evidence availability. Independently sourced semantics and evidence-changing challenges would be needed before claiming practical usefulness or a learned model advantage.

## Implementation and acceptance

| Quality gap | Offline change | Required check |
| --- | --- | --- |
| Context mismatch | Explicit six-condition matrix, reciprocal actions and fresh qualification cases | Exact counts; correct source-only targets; per-field context diffs |
| Clock and age confounding | Answer-preserving translation and age-only transform | Relative ages/slack invariant under CT; CA changes only source/card observation time and stays newer than history |
| Action-order confounding | Case-locked ordering | Identical question and criteria ordering across all variants/repeats |
| Label or cohort leakage | Separate evaluator case metadata from actor request | Strict allowlists, source spans checked, no expected/direction/condition/repeat in payload |
| Misleading scoring | All-assigned statuses, case pairing, missingness bounds, repeated disagreement | Known-answer, missing/invalid, duplicate/unexpected assignment and wrong-policy mutation checks |
| Weak comparator | Literal rule on the same source and declared applicability | Rule solves expected cases; always-DEFER, historical-action and ballot-majority controls visibly fail where expected |
| Missing trace history | Full stateless request plus append-only assignment events in future runner | Offline report can reconstruct every assignment; partial outcomes remain visible |

The offline builder, fixture audit and scorer are the authorized implementation work now. The native ledger/relay integration, safety review of the launch path, public registration and fresh machine receipts remain future work; do not call this draft launch-ready.

## Visualization mapping

The offline preview is labelled **DEVELOPMENT FIXTURES — NO NATIVE RESULTS**. Show source text, historical action, ballots and timestamp transformations beside expected actions; evaluator labels live only in the reader's view. Native reporting would replace expectations with both observed repeat actions in a case-by-condition grid, with distinct correct, wrong, DEFER, invalid and unstarted cells. Link each cell to exact delivered input and visible response. Add a chronological request/cost strip; do not animate a swarm that was never instantiated.

## Cumulative resources and machine needs

RD5 ended at 488 lifetime calls. Committed API exposure is USD 0.022699069 including USD 0.004032 unresolved historical exposure; cumulative infrastructure estimate is USD 0.720248442. The original total cap remains USD 2, split USD 1 API / USD 1 infrastructure. Historical invoices remain unresolved estimates, not settled zeros. [Accounting](../rd5/results/h5-a1/resources.json).

This proposal requests a new maximum of 162 calls, ending at lifetime 650: **150 above the original 500-call ceiling**, and outside the completed RD5 stop of 488. The 12 unallocated historical slots do not authorize it. No dollar-cap increase is proposed. Reuse the conservative prior per-call envelope only if a fresh route check still supports it: USD 0.001344 × 162 = USD 0.217728 maximum new API reservation, giving USD 0.240427069 cumulative API exposure. This assumes at most 32,000 input tokens/request, no completion charge and no fallback; fail closed if the current route violates any bound. The maximum input-token envelope is 5,184,000, not a prediction of usage.

One exclusively claimed CPU host is sufficient, no GPU, one worker and one in-flight call. Minimum runtime needs are Python, 1 vCPU and 512 MiB RAM; existing authorized fleet sizes may be larger. Proposed allocation ceiling is 90 minutes at no more than USD 0.07143/hour, reserving USD 0.107145. Cumulative infrastructure estimate becomes at most USD 0.827393442, and combined proposed exposure USD 1.067820511. Refresh time/rate evidence and keep the original split caps; do not infer current availability from RD5's released host.

Budget/lease limits dominate timing: at most 60 seconds per request and 30 minutes per stage, with no retries; 90 minutes includes preparation and collection. Preparation estimate 2–4 operator hours, analysis/reporting 1–2 hours and launch/closeout 0.5–1 hour, including existing workflow reuse. These are planning estimates. An outage or setup delay can leave assignments unstarted; it cannot extend the cap or silently renew the machine.

## Owner decision and handoff

Disposition: **DECISION NEEDED after the offline draft is validated**, with native integration still required before admission. The concrete decision is whether this component diagnostic is worth up to 162 new calls and the revised lifetime call ceiling of 650 under the unchanged USD 2 cumulative cap. It is not approval for another reserve-policy study, held-out generalization study or model comparison.

The [owner-update rule](../../../../../tooling/agent-experiments/RUN-REVIEW.md) requires the updated plan decision before allocation or launch. The current request authorizes improving and drafting the design; no native approval receipt is created from it. Do not hold a machine while this proposal is under consideration. Existing reviewer waiver remains in force.

## Startup execution amendment

Q0-A1 stopped before any provider request; all18assignments remain unstarted and D0 is unrun. The [post-mortem](reviews/Q0-A1-POST.md) and [execution repair](STARTUP-REPAIR.md) preserve its original immutable plan and failed record. The scientific requests, labels, conditions, ordering,18/18qualification and analysis are unchanged. A proposed explicitly approved, append-only zero-dispatch Q0-A2 replacement is a new execution contract, not an automatic retry. It must preserve the actual latest closeout, original ledger/caps and original allocation window. The repair is prepared offline; no replacement has been approved or admitted.
