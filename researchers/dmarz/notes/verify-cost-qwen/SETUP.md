# Experiment setup record: verify-cost-qwen, attempt 001

Status: in preparation, not launched. This record follows [the setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and is not launch authorization. A run starts only when the orchestrator takes a request from the private run queue after dmarz/fleet-monitor's same-researcher check. Nothing has run on a server and no model call has been made.

## Ownership and question

- Owner dmarz. Builder dmarz/pipeline-verify (Claude Code, offline on dmarz's Mac), working for the pipeline lead dmarz/pipeline. Operator: whoever takes the queued request; the server is a launcher parameter. Review independence: none. As relayed to this builder by dmarz/pipeline on 2026-10-04: dmarz directed this program himself (research program v5, written with him by a Codex session on 2026-10-04; his instruction to ship it was relayed by dmarz/fleet-monitor). The design is the program's; this package implements line V as specified there. Cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more; the run is not independently reviewed.
- Question: can an agent choose checking versus exploration when the optimal action changes with report reliability and the cost of leaving a cell unknown, and does an action-consequence table change that choice relative to explicit prose with the same information? Primary contrast: per-layout mean table-minus-prose expected regret (24 paired values). Claim boundary: a one-step policy assay on one model with stated calibrated probabilities and scripted consequences; not multi-step sensing, not a swarm result, no novelty claim.
- Research status: exploratory instrument in researcher notes. No survey gate, no hypothesis file; S2 is disabled.
- Prior work this builds on: phantom-coast PC4 and PC5 (Vishesh), whose [post-mortem](../../../vishesh/notes/phantom-coast/pc5/reviews/S1-A1-POST.md) and [next-iteration note](../../../vishesh/notes/phantom-coast/pc5/NEXT-ITERATION.md) propose this threshold study. This builder ran no new literature search.
- Previous study and lessons used: no earlier attempt of this study. From PC5's post-mortem: its qualification offered a single legal cell and so screened interface compliance only (repaired here by two-legal-action clear-dominance fixtures); a favourable average hid a regression in the reliable-source stratum (every stratum is reported here and regressions are flagged). From [the pipeline lessons](../pipeline/LESSONS.md): caps and timeouts sized for the whole chain before qualification (item 1); a one-call probe before any paid stage (item 3); read failing answers before any repair (item 6); small gates misclassify, so ambiguous items are removed before the run (item 7); a design can sit at ceiling, so S0 reports the comparator regrets and the analysis reports each stratum (item 9).
- Current stage and next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass (exploratory scope only) | README and preregistration, 2026-10-04, dmarz/pipeline-verify | Formal survey and hypothesis gates not met; S2 stays disabled |
| G1 Plan written before implementation | pass | README, preregistration, design.yaml, experiment.yaml and this record committed before any study code existed (first commit of this directory) | none |
| G2 Instrument and offline checks | pending | none yet | implement; selftest; offline S0; rehearsal; manifest check |
| G3 Current attempt admission | pending | none yet | pre-run review with the pinned commit and source hash; dmarz/fleet-monitor's same-researcher check; run-queue request; exclusive server claim; launcher setup |
| G4 Qualification before scientific escalation | pending | P0 and Q0 are stages of the chain; the software gate admits S1 only after Q0 passes at the same source hash | run |
| G5 Reconciliation and closeout | pending | none | run |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml); history in git.
- Independent units: 24 layouts for S1 (3000 to 3023), 12 per qualification set (2800 to 2811, 2900 to 2911), 4 engineering layouts (2600 to 2603). Per S1 layout: 12 cases × 2 representations = 24 paired single calls.
- Sample size: 24 layouts × 12 cases × 2 representations is the program's count. Not powered for small differences; the practical marker is 0.03 expected-loss units and intervals are descriptive.
- Splits: engineering, qualification a, qualification b and main layouts are disjoint; holdout 10000 to 19999 unopened. Qualification (e, U) pairs are disjoint from the main grid and between the two sets.
- Agent definition: one stateless call per assignment; a fixed system prompt and one user message; no tools, no memory.
- Versions: `qwen/qwen3.7-flash` via OpenRouter, provider Alibaba, reasoning disabled; requirements.txt pinned; the runtime source hash covers design.yaml, experiment.yaml, requirements.txt and `src/*.py`.
- Visualization: VISUALIZATION.md, mapping v1 (written with the implementation).

## Current attempt admission

Not admitted. Operations entry: manual, through the private generic launcher described in RUN.md (written with the implementation).

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| 001 / none | S0, P0, Q0, S1 planned | pending | nothing has run | none |

## Closeout

Nothing to close: no run exists.
