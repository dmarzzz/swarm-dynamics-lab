# Setup record: wild-evidence-depth / v1

Owner/operator/assessor: shadow/sol-audit-gap. No independent reviewer is claimed. This adapted setup record follows [EXPERIMENT-SETUP](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). Scope is **analyze saved data**, not a new experimental dispatch. The formal survey/hypothesis gates remain unchanged and no accepted hypothesis is asserted.

## Ownership and question

Question and claim boundary: [PLAN](PLAN.md), a fixed-export forensic coverage census. No experimental agents, prompts, model provider, paid calls, new data collection or fleet allocation. Owner explicitly assigned the audit and an unowned analysis in Wave 4 item 15. Previous attempt/post-mortem: none, initial instrument. Known source limitations were read before planning. Initial next action was to publish the plan and ranking, implement fixture checks, then analyze the saved export. Current stage: A1 complete. Next action: publish and integrate the descriptive result; no further run needed.

## Gate evidence

| Gate | Status at plan publication | Evidence / next action |
|---|---|---|
| G0 Question and scope | pass for saved-data analysis only | PLAN; ranking audit; source report read; no formal hypothesis promotion |
| G1 Prospective design | pass | PLAN v1 written before implementation and aggregates |
| G2 Instrument | pending | Implement fixtures and separate direct-coverage recomputation |
| G3 Current operation | saved-data analysis only | Publish immutable plan before census; no model dispatch, dollar reservation or machine acquisition |
| G4 Model qualification | not applicable | No model or intervention; analyzer fixture checks required instead |
| G5 Reconciliation | pending | Source hash, all-row accounting, derived outputs, POST-MORTEM and FINDING |

## Instrument and admission index

- Input contract, fixed bins, metrics, claim boundaries and data handling: PLAN.
- Independent units: one selected incident export, no asserted independent agent/event count; no IID CI or statistical-power claim.
- Controls: hand-authored graph and text fixtures, plus separate reference arithmetic. No scientific holdout was opened because no intervention study is run.
- Operations: manual `python3 analyze.py --data /path/redacted.jsonl.gz --out results`; no prepare/dispatch/resume of models.
- Resource cap: one nice-10 local CPU process, no new infrastructure, API cap effectively USD 0 because analyzer has no network/model path. No credentials are read.
- Visualization v1: static bar/card uses row-kind counts, payload direct-response fraction and mutually exclusive descendant-coverage categories; null timestamps mean no animation/replay. HTML/SVG include metric denominators and artifact-not-success warning.
- Publication: immutable plan revision will be recorded in POST-MORTEM after push/readback. Source/analyzer checksums in generated results.
- No raw dataset rows/text committed. No payload strings executed. Id/hash aggregates allowed, but output should prefer counts over row-level listings.

## Attempt and repair history

A1 completed all 189,579 source rows; no failures or exclusions. Fifteen fixtures, ten separately recomputed metrics and deterministic rerun passed. See [POST-MORTEM](POST-MORTEM.md) for source/version, command, limitations and clarification history. The gate table above preserves the plan-publication state; G2 and G5 are now complete for the saved-data analysis only.

## Closeout and successor handoff

Census, response-link validation, static reporting and scientific scope review complete. Execution successful; model qualification not applicable; causal/success inference unsupported; process records preserved. USD 0, no workers or claims remain. This record is not independent research review or automatic launcher admission. Deliver FINDING.md with its missingness and selection limits; do not convert it to an unreviewed causal experiment or acquire machines.
