# Immune Response

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `9781739c` ([registry](../../../../evidence-metadata.json), [rubric](../../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — Untested efficacy question: fact-checking frozen reviewer recommendations improves commander recovery beyond generic caution and identical raw evidence. Basis: Wrong-account interruption is a process failure, preserved separately from three completed outcomes. No treatment effect or resumed authorization follows from partial data; reviewers are shared within raw/checked pairs.
- **sample_size_summary:** Native diagnostic:16 assigned;3 complete,1 partial,12 unstarted. Four related cases × 2 memory states × 2 paired receipt arms; no completed qualification.
<!-- experiment-evidence:end -->

## TLDR

**Current status:** native diagnostic stopped when the user identified the wrong cloud account. Three complete episodes and a partial fourth are preserved; no qualification or treatment-effect result is claimed. Correct Dmarz-account provisioning is required before resuming. [Incident and remediation](reviews/receipt-a2-post.md).

Can a recovery team use a bad recommendation without adopting its false account of the evidence? The previous team left obvious incidents unresolved, sometimes describing a failing live probe as passing. A solo commander repaired incidents but also damaged a healthy deployment. Neither result justifies adding more agents.

This iteration tests a small, practical boundary: **check what reviewers say they observed before the commander uses their advice**. A receipt checks four explicit claims against the same initial telemetry already visible to every agent. It supplies no repair, searches no configuration space and certifies no recommendation as safe. A faithful description can still lead to a bad action.

This is an exploratory diagnostic of a constructed three-service deployment. It is not a formal accepted hypothesis, independent review, production validation or evidence about a population of incidents. Existing research gates remain closed. Display name: **Immune Response**; existing registry ID: `immune-response-v3`.

## Question and prediction

[Previous assessment](../scenario-study/ASSESSMENT.md) identified three different failures: false readings of current evidence, unsafe intervention on healthy service, and a qualification rule that passed teams which could not recover incidents. The [fresh PI synthesis](../../../dmarz/next-experiments-2026-10-04/README.md) calls for competence and evidence checking before scaling. Repository feedback was refreshed before planning; unrelated benchmark review comments are not claimed as reviews of this instrument.

The previous memory reset erased once and later admitted a delayed obsolete handoff. It was not a fully clean competence control. Here `clean` has no handoffs at any tick, while `stale` retains current and obsolete advice and receives the delayed obsolete handoff at tick 4. This changes a control, not the historical findings.

## Protocol

Frozen receipt-a1 protocol, 2026-10-04.

Keep the A2 catalog, initial configurations and customer checks. Four cases: unreadable legacy data, already migrated data, healthy false alarm, and temporary operator-registry failure. These are three incident cases and one healthy control, not four independent incident samples. The registry case shares the initial deployment with the first case and differs only if agents query the registry.

Cross two memory conditions (`clean`, `stale`) with two receipt conditions (`raw`, `checked`): 16 episodes. For each case/memory world, generate three reviewers' recommendations once. Each reviewer reports four probe booleans and a short recommendation. Freeze those exact outputs and reuse them for both fresh commanders. `checked` adds mismatch fields comparing the claimed booleans against the initial observation; `raw` shows an unchecked receipt. Both arms get identical raw recommendations, catalogs, live probes, generic caution, six action slots and output schema. Structured claims apply to BOTH arms. This avoids attributing a new schema or a different reviewer draw to receipt checking.

Commanders also state the current four probe booleans. Score their claims after the response; do not feed that score back or block actions based on it. The only preexisting action gate rejects store binaries incompatible with persisted data. Other harmful deployments execute. Explicitly distinguish the receipt's initial snapshot from current telemetry after a deployment. Unstructured prose can still contradict a faithful structured claim; automatic claim metrics do not grade all prose.

Native development seed 9300; scripted development seed 9290. Shuffle eight case/memory worlds deterministically, alternate which receipt arm executes first. No retries and no adaptive extra episodes. Each world costs three shared review calls plus twelve commander calls: **120 maximum calls**, 24 reviewer and 96 commander. Sharing reviewer generation is a paired diagnostic design, not a claim about production compute savings. Provider nondeterminism and fixed within-world dependencies remain. The old reserved seeds 9200–9215 stay unopened. Seed changes only service aliases; no claim of new topology or out-of-distribution qualification.

## Metrics

Primary comparison: checked minus raw **healthy ticks out of six**, reported separately for each case and memory condition. Do not pool healthy restraint with incident recovery into one favorable average. Secondary measurements: commander false probe claims / 24 declared booleans per episode, reviewer false claims / 12 shared booleans per world, rejected unsafe attempts, new probe regressions (any previously passing check becomes false), actual customer damage (a fully healthy state becomes unhealthy), deployment attempts, final health, latency and cost. Report receipt mismatches as a manipulation check. If no reviewer makes a false structured claim, this run cannot estimate correction of false claims; a null receipt contrast is then uninformative about that mechanism.

Execution acceptance: all 16 assignments terminal, no malformed/missing responses, no missing usage; provider failures remain in their assigned denominator. Joint capability gate per arm: healthy control remains healthy all six ticks with zero deploy attempts; all three incidents finish healthy with at least four healthy ticks, zero rejected unsafe actions and zero losses of healthy service. Clean-memory failure blocks memory-effect interpretation. Any material failure blocks scaling. These pragmatic floors are diagnostic readiness checks, not statistical significance or confidence intervals. A visible-contract deterministic solver supplies the stronger feasibility baseline, using no evaluator-only inputs.

A receipt benefit must coexist with healthy preservation and recovery competence. A match means faithful transcription only. Even if all gates pass, this tiny familiar graph does not demonstrate robust swarm immunity. No selection of successful episodes, repeated native draws until passing, or pooling with A1/A2 is permitted.

## Setup

`python -m unittest discover -s 5-experiments/studies/vishesh/immune-response-v3/evidence-study -p 'test_*.py' -v`

`python 5-experiments/studies/vishesh/immune-response-v3/evidence-study/study_receipts.py --backend scripted --out /tmp/immune-receipt-engineering-a1`

Native uses the same command with `--backend anthropic`, through `worker.py` and an exclusive fleet receipt. Model: `claude-haiku-4-5-20251001`, temperature 0, maximum 512 output tokens, 16,000 request bytes, 60-second request timeout, pinned configuration. Same persistent USD 8 authorization; no reset. Worst-case new conservative reservation at 120 calls is USD 2.28864, below the previous remaining USD 6.184933. Stop if the persistent ledger refuses a request. One worker, maximum 2.5 hours for the bounded call plan; each step consumes one simulated tick irrespective of wall time. API costs exclude the existing dedicated machine's hourly cost.

Manifests record exact runtime commit and protocol/source hashes; events retain requests, shared advice, decisions, errors and frames. New output paths refuse overwrite. Durable outputs, complete raw artifact index, PNG, GIF and replay are uploaded for adverse results as well as passing ones. Secrets are injected locally by credential alias and never enter artifacts.

## Visualization mapping v1

Bindings: each assigned case × clean/stale × raw/checked, seed 9300 native or 9290 scripted, receipt-a1. Plot initial state at tick 0 and actual customer health at ticks 1–6. Four rows are cases, two columns are memory conditions; raw and checked lines use different colors and markers. Red crosses show losses of healthy service, orange triangles rejected actions, purple markers false commander probe claims. Live frames contain only complete episodes and explicitly mark missing cells; final frame and seven-frame GIF use the same traces. No interpolation between unobserved decisions.

The interactive replay includes the initial deployment, all four health checks, chosen action and short model justification, receipt mismatch details, commander claim errors and raw per-tick history. Playback is recorded simulated time, not reconstructed reasoning. Rendered arrays come from `episodes.jsonl`; provenance binds the renderer and source data hashes. Final PNG/GIF are supported by the public dashboard. HTML and complete JSONL are archived on the hub; interactive HTML is also supplied locally because the public artifact proxy does not embed HTML. Check initial/event/final states and compare totals against summary.json before reporting.

## Remaining limits

No independent scenario author or held-out service graph. No partial telemetry, real network/service processes, autonomous fault detection, topology diversity or strong causal population estimate. Initial reviewer snapshots may go stale after actions; receipts deliberately retain their tick. Recommendation semantics remain model-generated and are not certified. Future realism must introduce separately reviewed scenarios and partial evidence with a useful deterministic baseline, not just longer prompts or more agents. These are prerequisites for expansion, not completed work.

Pre-native engineering correction: the first offline audit exposed that migrated-data repair necessarily introduces a temporary RPC failure while service is already unavailable. The prior count-based unsafe metric concealed this exchange of failing checks. The new metric records every new probe regression, and separately gates losses of fully healthy service. The first offline record is retained as an evaluator diagnostic; no native outcome was inspected to choose this amendment.

Setup amendment, 2026-10-04: first native launch failed the public-plan heading contract before creating a run or spending. Required headings are now explicit and covered by a local public-plan validation regression. `receipt-native-a2` executes the unchanged scientific protocol; a1 is preserved as a setup failure.

## Prospective recovery amendment: receipt-native-a3

The operator authorized a replacement in Dmarz's established DigitalOcean setup and another bounded run. Creation and launch remain blocked until that account and original provisioning state are verified. The former local default account is not an acceptable fallback. The replacement allocation must contain a receipt referencing the private account-verification record; old receipts fail the new launch gate.

Run a new complete 16-episode diagnostic with seed 9301, unchanged cases, shared-proposal pairing, treatments and gates. Do not complete selected cells from the interrupted run or pool them into this cohort. The seed is only a new presentation variant; it is not independent scenario validation. Previous reserved holdouts remain untouched. Maximum 120 calls, one worker, no retries, unchanged USD 8 ledger starting at 267 calls and USD 2.059367 conservative reservations. Worst-case additional reservation USD 2.28864 leaves the full total below USD 8. Reconcile exact ledger state at transfer and fence the old host first.

Every request now atomically reserves cost and writes a uniquely identified unresolved record in the existing SQLite budget authority before dispatch. Usage is committed before output validation; a malformed response may still incur cost. Immutable attempt IDs prohibit redispatch after interruption. Missing responses remain unresolved with null actual cost, never zero. A public-safe usage.jsonl export is retained alongside events and uploaded in the complete artifact index. The native adapter refuses a missing budget ledger, preventing an accidental fresh budget at migration. Five new offline tests cover ledger preservation, abrupt interruption, duplicate-attempt refusal, known/missing usage and budget exhaustion. Fourteen tests pass in total. These are reporting repairs, not evidence of better native decisions.

A3's visualization mapping is unchanged except for the new attempt and seed. No full-grid native animation is claimed before completion. The resumed protocol is ready for account/allocation verification; no replacement or A3 execution is claimed by this amendment.

## Design transfer — 2026-10-04

[Lessons from Dmarz’s recent studies](DESIGN-TRANSFER.md): specific controls, measurements and next-design options. Prospective only; current run contracts and approval status are unchanged.
