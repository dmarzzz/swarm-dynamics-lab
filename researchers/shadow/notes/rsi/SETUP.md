# Setup record: RSI reporting replay R1

Adapted from the [setup template](../../../../tooling/agent-experiments/templates/experiment-setup.md). Follow the [setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). This is offline tooling over existing records, not a new experiment or an accepted hypothesis.

## Ownership and question

Owner: shadow. Operator/searcher/developer: shadow/sol-rsi2. No independent researcher review has occurred. Question and scope: [REPLAY-PLAN-v2.md](REPLAY-PLAN-v2.md). Prior work: [protocol validation](VALIDATION.md) and [R0 lessons](../rsi-loop/LESSONS.md). Those receipts establish metadata parsing only; they do not demonstrate research-quality improvement.

## Gate evidence

| Gate | Status | Evidence and next action |
|---|---|---|
| G0 question and research gates | offline scope only | Repair known reporting defects; no new scientific hypothesis. Formal scientific gates remain blocked. |
| G1 plan before implementation | pass | REPLAY-PLAN-v2.md committed before R1 implementation, 2026-10-04, sol-rsi2. |
| G2 instrument | pass, offline scope | 18 R1 unit tests, 14 protocol tests, source rederivation and full replay comparison; see R1-POSTMORTEM.md. |
| G3 attempt admission | not applicable to offline saved-data tooling | No model dispatch, simulation sweep, fresh experiment or external service. The owner explicitly requested this replay. |
| G4 qualification | blocked for science | Offline software tests do not qualify an agent/scientific intervention. |
| G5 closeout | complete, offline scope | All decisions, per-group checks, related-party credit receipts and visual/privacy checks retained; see R1-POSTMORTEM.md. |

## Design and instrument index

Plan and controls: REPLAY-PLAN-v2.md. Records are a convenience sample of known defective historical reporting, not held-out evidence. Counts are reporting groups and observations, not independent worlds. Searcher: current operating agent, with its bounded artifact saved explicitly. Builder/evaluator: deterministic local functions. No raw conversation or assistant memory goes into exported artifacts. Sources and evaluator hashes will be pinned in the replay manifest. Visualization: fixed pipeline frames built from measured replay output, with terminal JSON fallback.

## Current attempt admission

Operations: manual offline package; not registered as a new dispatched study. Inspect, replay and test commands will be documented in DEMO.md. No launcher, resume dispatch, provider credential, budget reservation, infrastructure claim, transfer or public-plan admission receipt is needed because there is no fresh dispatch. The engineering plan is public on shadow/rsi before implementation. Public scientific preregistration is explicitly not claimed.

## Attempt and repair history

R0 remains preserved in ../rsi-loop/. R1 retains all 327 episode records, including 127 invalid records. Source content never changes during evaluation. One test-only JSON-key-order assertion was corrected; no metric, source or candidate changed. Complete evidence and reconciliation: [R1-POSTMORTEM.md](R1-POSTMORTEM.md).

## Closeout and successor handoff

Current gate: G5 complete for offline tooling; G4 remains blocked for science. Exact next action: review [DEMO.md](DEMO.md) and run `python3 researchers/shadow/notes/rsi/replay_loop.py --verify`. Zero paid spend is consumed or requested. No persistent worker or fleet resource is launched. Branch-only PR; do not merge automatically. Any subsequent fresh-model or scientific-effect evaluation requires a new plan and appropriate authorization/review.
