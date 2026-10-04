# Pre-run assessment: optimal-swarm-size-q1

Owner: vishesh/codex-idea-scores. Stage: exploratory S0 qualification, first attempt.
Status: blocked pending credential availability, served-route verification and package review. No model calls yet. This document does not claim independent approval.

## TLDR

Test whether a single model context can solve deterministic evidence reconciliation and restricted arithmetic-code repair before calibrating larger swarms. Q-A treats 16 synthetic tasks with N=1; this is the baseline for later N=2,4,8,16 qualification, not a matched-budget size-effect comparison. Measure verified on-time success, quality, elapsed wall time, cost and failures. The total authorized first-attempt spend is $20 across all conditions, failed calls and calibration. Synthetic tasks and hosted inference cannot establish an optimal production swarm size or local hardware scaling law.

## Question and prediction

Can the model follow the task contract and produce correct, supported outputs on both independent and chained tasks? Reference fixtures pass offline. Model competence is unmeasured: low success is a qualification failure to diagnose, not evidence against swarms. A result is uninformative about N until matching and qualification pass. Closest evidence and limitations are in ../PRIOR-ART-REVIEW.md; that author review does not replace the formal survey gate.

## Setup

Sixteen generated tasks: two families (evidence and restricted arithmetic repair), two dependency structures (parallel and chain), four fixed roots per cell. Each has 16 work items. The manifest uses the existing qualification namespace; fit, validation and transfer remain unopened. Ground truth and hidden test inputs remain evaluator-only. Actors receive full public tasks and declared prerequisite artifacts; prompt replication is charged. Restricted AST evaluation never executes arbitrary submitted code.

Draft provider is OpenRouter openai/gpt-4.1-mini, native OpenAI route only, no fallbacks; configured prices are $0.40/M input and $1.60/M output. This route is not qualified or credential-ready. A provider change requires an explicit versioned amendment before dispatch. The authoritative authorization is ../SPENDING-AUTHORIZATION.json and the runtime caps are ../qualification-config.json. Source must be clean and pinned to this plan's immutable commit at launch; validation.json hashes the implementation and tests.

Dedicated machine preparation: sim-test-01, claim vishesh-swarm-size-q1, agentops PR 86. Claim must still be exclusive and current at dispatch. Credentials are consumed only by the authorized process, by alias OPENROUTER_API_KEY; no credential values belong in artifacts. PYTHONPATH must include /usr/local/lib/swarm for the preinstalled reporting client.

## Protocol

Run Q-A first: 16 N=1 assignments, one episode at a time, at most 19 calls each (planning, one malformed-plan repair, 16 work items, integration). Deadline 600 seconds per episode, with final 60 seconds reserved for integration. Output bound 4096 tokens/call; prompt bytes at most 48000. Four service slots are configured, but Q-A uses one actor. Maximum Q-A episode wall allowance is 9600 seconds plus bounded reporting overhead; the allocation must cover the batch or be extended before dispatch.

Use one durable shared budget ledger for Q-A and any Q-B, never a fresh ledger to replenish spending. $2 per episode and $20 aggregate exposure. Reserve conservative full-context cost before each request; settle only known actual usage. Ambiguous failures retain their entire reservation. No transport retries; malformed model plans get one charged repair. Preserve all assigned episodes, terminal outcomes and not-started episodes. After Q-A, write a post-mortem before considering Q-B; freeze any calibrated settings separately. Formal confirmatory S2 remains closed pending survey/hypothesis gates.

Before dispatch: complete review, verify actual provider route and credentials, validate replay, refresh allocation, publish/register this immutable URL, verify public experiment metadata and each condition-specific TLDR. Use the SwarmLab-PlanPreflight/1.0 user agent: live checks found default Python requests return HTTP 403 while the documented user agent returns 200. Never bypass a failing public registration check.

Intended command from the pinned research repository: `python3 researchers/vishesh/notes/optimal-swarm-size/src/run_qualification.py --config <frozen-runtime-config> --output <new-attempt-directory> --budget-ledger <single-authorized-ledger>`.

## Metrics

Primary qualification outcome: verified task correctness delivered within the wall deadline and episode cap. Record task quality, evidence grounding/repair behavior, actual elapsed time, settled cost, retained reservations, execution failures and missing outcomes separately. Denominator: all 16 assigned Q-A episodes, including failures; do not silently drop unfinished assignments. Tasks are independent root units; items and repeated N conditions are not independent observations. No size-effect significance claim or tuned success threshold is justified by this screen.

Twenty-three offline test methods pass, including reference variations, adversarial submissions, roster-invariant fixtures, budget concurrency, cap immutability, fail-closed launch and public TLDR matching. This is software evidence only; it is not model competence. On failure classify execution, measurement or capability issues, retain the original attempt, and design a bounded diagnostic within the same $20 allowance. Never rerun for a favorable scientific result.

## Visualization mapping

Version q1-service-intervals-v1, bound to each manifest family/structure/root/N. Record monotonic elapsed service_start/service_end, work_complete and terminal events. Actor lanes show request intervals including provider latency, with separate integration color; missing ends are red and gaps are not interpreted as hardware idleness. Live reporting shows measured completed-item counts. Retain trace.jsonl, assignment.json, outcome.json and standalone replay.html per episode; static interval table is the fallback. The public proxy does not embed arbitrary HTML, so the replay is a downloadable hub artifact. Synthetic renderer tests cover intervals, missing ends and script escaping; browser validation remains pending. No fabricated flock motion or inferred GPU utilization is presented.

## Changes and unresolved issues

- Fixed public per-run fetch headers after reproducing HTTP 403 with default Python and HTTP 200 with the documented user agent on the selected host.
- Verified reporting module location and SSH access. The idle-machine audit found only operating-system Python services.
- OpenRouter credential unavailable in checked environments; no provider call attempted. User has been asked for an approved store alias/path or intended shared provider.
- Shadow review request remains open. A same-researcher engineering review handoff was rejected by automatic approval review in the receiving task; it is not an approval.
- Served model/provider pins, browser replay verification and final public registration receipt remain required before dispatch.
