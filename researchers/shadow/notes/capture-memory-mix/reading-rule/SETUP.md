# Experiment setup record: capture-memory-reading-rule / v1

Adapted from [setup template](../../../../../tooling/agent-experiments/templates/experiment-setup.md). Follow [runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and [operations](../../../../../tooling/agent-experiments/OPERATIONS.md). This is a manual runner, not a supported shared dispatch adapter.

## Ownership and question

Owner/operator/assessor shadow/sol-cm2; same-author review, no independent-review claim. Owner approved this bounded frozen-history diagnostic on 2026-10-04, OpenRouter only, USD 12 ceiling. Does presentation change choices on identical indexed histories? See [PLAN.md](PLAN.md). Research status exploratory instrument diagnostic, not an accepted hypothesis or swarm replication. Prior-art and formal review limitations remain as in the parent README. Previous closeout [CORRECTIONS.md](../CORRECTIONS.md), accepted attempt-accounting lessons in PLAN.md.

## Gate evidence

| Gate | Status | Evidence / next action |
|---|---|---|
| G0 question / research scope | diagnostic-only | PLAN.md; formal inference not admitted |
| G1 prospective plan | pass | PLAN.md written before new implementation or calls |
| G2 offline instrument | pass | 8 offline tests; S0-PRE.md and input.json |
| G3 stage admission | pass for S0 only | results/admission-S0-155040161364.json; immutable public bytes verified, hub registered |
| G4 qualification | blocked | First request HTTP403; 0 valid; S1 never admitted |
| G5 closeout | complete-blocked | POSTMORTEM.md; 1 terminal access failure, 155 unstarted; USD0.05 retained |

## Design and instrument index

PLAN.md defines scenario strata, controls, prompts, six renderings, independent history units, 24 scientific histories, 2 disjoint S0 histories, fixed 156-call ceiling and missingness rules. Implementations will live here, frozen effective assignments in input.json and receipts/journal under results/. Scientific seeds are a feasibility set, not a held-out generalization benchmark. No tools, retrieval, prior assistant conversation or mutable shared memory are visible to the model. Visualization is a static paired-history plot, because this is not a temporal swarm execution.

## Current attempt admission

Manual entry points planned: `python3 reading_rule.py freeze`, `test_reading_rule.py`, `reading_rule.py run S0 --revision COMMIT`, `reading_rule.py run S1 --revision COMMIT`, `analyze.py`. Public immutable plan and instrument hashes must match before dispatch. S1 requires qualified S0 plus a fresh recorded pre-assessment. One worker on the owner-authorized local machine, no provisioning, no fleet changes, sequential HTTP calls. Dedicated fleet rule applies to Vishesh, not this lane. Credentials consumed from local OpenRouter key file only, never exported; no credential transfer. Budget USD 12 including qualification, failures and ambiguous dispatch; durable per-call USD 0.05 retained reservation, no retry or reset. Current go/no-go: STOPPED after S0 HTTP403. No further dispatch authorized by this completed v1 closeout.

## Attempt and repair history

One qualification request returned HTTP403 at 15:50:40Z, no model output. Earlier swarm records remain untouched. The inherited untracked pool_probe.py is not part of this diagnostic and must not run. No repair iteration is authorized by this plan; qualification failure ends v1 with a blocked report.

## Closeout

Execution stopped on access denial; validity 0; qualification blocked; scientific effect untested; preregistration and stop rule followed; reporting complete in POSTMORTEM.md. Save raw response/logprob receipts, assignment/started/terminal counts, actual costs separate from retained reservation exposure, hash inventory and missingness. No persistent workers or external channel posts.

## Completion and successor handoff

Next action: retain blocked v1; owner must resolve authorized OpenRouter access and declare a fresh qualification attempt before further calls. Carry USD0.05 reserved exposure forward. No scientific null was observed. No automatic expansion or new run is implied by remaining funds.
