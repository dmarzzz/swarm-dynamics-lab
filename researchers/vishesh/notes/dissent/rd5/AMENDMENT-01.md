# RD5 amendment 01 — prospective implementation contract

Written 2026-10-04 before RD5 experimental implementation or native calls. Read with [PLAN.md](PLAN.md); this amendment supersedes the affected details below. No RD4 evidence changes.

## TLDR

Test whether remembering an inconclusive inspection, and then protecting one future inspection, improve timely decisions under two checks. Compare B2 reservation with B1 memory and B1 with B0 bounded always-check. Six authored streams yield 24 assigned decisions per policy. This pilot uses one process-control domain to remove the original confounding between scenario mechanism and domain; it cannot establish general performance across domains.

## Question and prediction

When does an unresolved challenge deserve another scarce check? Memory should help when repeated messages expose the same acquisition. Reservation may additionally help when genuinely new but inconclusive acquisitions consume the budget before a useful change. It should delay an urgent early resolution. Report all three mechanisms separately, even if the aggregate threshold passes.

## Setup

H5 uses process readings with the same inclusive safe interval, 10–30, in all six streams. The three mechanisms remain repeat-then-change, new-but-inconclusive-then-change, and urgent-early-resolution, each paired in stop/resume directions. Bridge and build semantics remain in Q5 and offline regression controls; H5 makes no cross-domain efficacy claim. Q5 is 12 packets × raw/card representations, maximum 24 calls; H5 is six streams × three policies × at most two calls, maximum 36. The original 500 lifetime-call and $1 API/$1 infrastructure limits remain; 428 calls are already used.

All streams have decision ticks 0, 2, 4, 6, deadline tick+1, public horizon 8. The useful inspection becomes available at 4 in the first two mechanisms and 2 in the urgent mechanism. B2's fixed release time is 4, public and frozen, not tuned from model answers. This is a hand-selected mechanism test with known timing; unpredictable timing and adaptive reservation are the next research question, not a claim established here.

## Protocol

The environment issues trusted acquisition receipts; reports cite them. A report alias, requested action or rewritten message does not alter the trusted acquisition. A forged ID or modified receipt cannot authorize a check. One check acquires the currently available inspection, not an advance look at future evidence. B0 may reacquire an unchanged inspection; B1/B2 remember attempts at each unresolved frontier. All arms retain the same receipts and resolved closures. Inspection text is unknown to the resolver until acquired. The current report supplies only the inspection identifier and availability, never the evaluator's action.

Every new applicable frontier invalidates current authorization until resolved. Historical verified action remains visible as history only. A successful resolution stays authorized only for that frontier, object/version and freshness interval. The acquired record is stamped at acquisition time by the environment, not refreshed on each alias. A repeated unresolved frontier remains DEFER. A future independent measurement can reopen the question in either direction without a model admission veto.

Separate durable physical-acquisition events, saved receipts, inference reservations/dispatches, interpretations and decision outcomes. Probe the actual relay before any new physical check. A failed precheck leaves the current assignment unstarted and uses no physical or inference budget. A later inference failure preserves the acquired receipt/check cost and stops the attempt; no automatic replay or refund. Unknown dispatch outcomes retain their reservation. No automatic resume; a separately assessed continuation may select only never-started trajectories, preserving the original all-assigned denominator.

The structured adapter extracts only explicit finite lexical facts (reading/capacity numbers and required-test pass/fail), preserving full text and matched spans. Multiple incompatible values, unsupported phrasing or ambiguous negation remain unknown. It never supplies an action, truth label or inferred missing fact. Native Jev is still responsible for interpreting the task and choosing HOLD/PROCEED/DEFER. Qualifications are prepared explicitly after ordinary offline tests; test discovery must not construct reserved qualification packets.

Use a frozen Latin rotation of B0/B1/B2 within the six roots, with root order fixed by seed 51004. Actor requests omit arm, stream mechanism, direction, future frames, evaluator fields and operating-assistant context. Requests may include only the current task, five supplied ballots, own historical/current state, acquired source text and its deterministic card. No cross-arm native cache is planned: each assignment has a distinct dispatch identity; the 60-call envelope already covers all calls.

## Metrics

Keep the PLAN's all-assigned primary endpoint, B2−B1 primary contrast, B1−B0 secondary contrast, six paired root summaries, early/late and critical-event counts, unjustified action counts, check/call/receipt resource vector, adverse-action and noncompletion breakdown. The threshold remains ≥2/24 more correct for B2 without additional wrong PROCEED; the urgent scenario's delay cannot be hidden by that average. Qualifications score appropriate DEFER as correct; H5 counts it as noncompletion.

Report transport failures and descendants as unidentified rather than model errors. Save all 72 assignment slots before H5 and all 24 before Q5. Q5 qualification requires every nominated card valid/correct (12/12), including all six uncertainty controls. A complete validated raw diagnostic is also required to close the stage; its lower accuracy does not select the representation. Missing/invalid native output blocks escalation. No retry to improve a result.

## Launch and visualization

Prepare source/config/assignment/request hashes without dispatch. Runtime admission must bind the published plan and amendment, current stage assessment, public-page verification, current exclusive approved-fleet claim, remaining original budget, route/snapshot, and Q5 evidence for H5. Unit fixtures need no host. A local prepared packet is not live admission; allocate only immediately before the admitted attempt.

Record an event timeline and render current versus historical action, inspection receipts, checks remaining, physical/inference outcomes and evaluator truth in separate tracks. Missing assignments remain visible. Development previews are labelled SCRIPTED — NOT MODEL EVIDENCE. Never send the reader's truth overlay to an actor.
