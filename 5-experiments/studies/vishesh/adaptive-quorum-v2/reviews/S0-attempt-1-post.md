# Post-mortem: API v2 S0 attempt 1

Retrospective review under the new run-review standard, 2026-10-03. Owner: vishesh/codex-methods.
Disposition: **diagnostic / repair required**, not scientific success.

## Assessment and execution record

The original pre-run assessment is [protocol.md](../protocol.md), frozen with code `4f20626`;
no separate pre-run form existed then. Do not backdate one. [Results](../results/laya-analysis.md),
[manifest](../results/laya-manifest.json), and [verification flips](../results/verification-flips.json)
record the completed run. Hub: `adaptive-quorum-api-v2/laya-S0-f33c7506b93f`.

24 assigned blocks produced 168 arm outcomes, all completed and scored, with zero schema-invalid
outcomes. Six tasks repeat across two agent counts and two deadlines; this is six task clusters,
not 168 independent observations. Physical local inference: 828 calls, 322,404 estimated input tokens,
238.68 episode seconds, no hosted API spend. Model initialization time is excluded.

The scripted instrument passed. The local Laya decision layer failed its clean competence screen:
central 12/24 correct, fixed/adaptive each 16/24. Targeted terminal testing changed 12 initially correct
central decisions to wrong and corrected zero initially wrong decisions. Random testing corrupted 8
and corrected zero. These paired repetitions diagnose this fixture/prompt/backend setup; they do not
establish a general effect of testing or model scale.

## Quality assessment

This run demonstrates a competence prerequisite failure, not whether urgency adaptation is useful.
The more informative contamination/timing matrix remains unexecuted. The original task implementation
and publication completed, but experiment qualification did not. None of the failures below are resolved
merely because the hub upload succeeded. Exact root causes of model errors are still unverified.

| ID / kind | Evidence | Cause confidence | Repair/diagnostic | Acceptance evidence required | Status |
|---|---|---|---|---|---|
| Q1 capability | Clean conjunction/selection screen failed | Suspected evidence integration or prompt/interface mismatch; not established | Isolate attribute extraction, constraint conjunction, ranking and NONE/WAIT handling; compare model receipts to scripted answers | Fixed diagnostic cases plus disjoint balanced qualification meeting frozen per-cell competence thresholds | Open |
| Q2 capability | Adding test results corrupted initially correct choices | Suspected tool-output interpretation or authority conflict; not established | Paired no-test / redundant truthful test / contradictory accuracy-only test probes; keep retention facts fixed | Preserve unaffected constraints and select correctly on clean tool-integration controls | Open |
| Q3 design | No B target in six-task qualification | Verified task generator coverage omission | Use stratified task selection and a coverage assertion before launching | All required labels and failure types covered; fresh tasks after any tuning | Open; balanced development IDs proposed, not executed |
| Q4 design | Deadline is an evidence cutoff; probes occur afterward | Verified protocol limitation | Either retain that narrower estimand explicitly or implement charged inference/probe latency before claiming dispatch deadlines | Executable timing assertions and no action after a real deadline in any wall-time study | Open for wall-time claims; limitation disclosed |
| Q5 inference | Six clusters; several identical central contexts repeat | Verified small/dependent sample | Keep pilot descriptive; size a later task-disjoint study from development evidence | No agent-count or repeated-call sample inflation; reviewed analysis/power plan before holdout | Open for efficacy claims |

## Next pre-run assessment

Bounded diagnostic only: use the existing Laya pin and synthetic evidence; no new hosted API spend
and no holdout access. Before any new model qualification, follow the subsequently published dedicated-machine
allocation directive in AGENTS.md. Offline local unit tests remain available without that allocation. First test the model's interpretation of one attribute at a time
and its response to an added truthful test. An alternative explanation is that the formatting or adapter,
rather than the task reasoning, drives the errors; compare semantically matched structured and plain-text
inputs without choosing variants on holdout results. Record all variants and costs.

If extraction works but conjunction fails, evaluate deterministic constraint checking over cited,
model-extracted facts as a separately named architecture. Do not feed hidden fixture truth into that
checker. If a model remains inadequate, report that fact and qualify another authorized backend;
Jev/OpenRouter is still contingent on secure credentials and route verification. Model replacement
is not an implicit waiver of competence checks.

Each repair needs its own pre-run record, new attempt ID and acceptance evidence. Broader S1 remains
blocked. This retrospective document does not claim a repair or rerun has occurred.
