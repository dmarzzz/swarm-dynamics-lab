# Antsy quality audit — 2026-10-04

Reviewed public repository at `951142a`, v2 source and recorded outcomes. This is an owner-requested engineering/methods review, not independent cross-researcher acceptance. Preserve v1/v2 findings and failures. No claim of an extremely high-quality experiment is warranted until the checks below pass.

| Dimension | Current evidence | Assessment / repair |
|---|---|---|
| Design | Explicit baselines and paired tapes; S0 contains only fast/clean arrivals | Good bookkeeping scaffold, weak test of adaptation. Cross accurate/misleading evidence with late/stalled arrival; include constant lower quorum and wait-until-deadline baselines. |
| Measurement | Six repeated tasks; missing B target; model token estimate described as actual tokens; full-tape failure invalidates even earlier successful commitment | Insufficient. Balance targets and failure strata, attach receipts to calls/contexts, use actual encoded token counts, score only faults that affect an arm's consumed prefix. |
| Visualization | Interactive local HTML, static public screenshot; every selected frame displays final outcome | Cannot show a faithful public temporal story. Render measured frame histories and public GIF; show a decision only after its commitment, mark unavailable data and evaluator overlays explicitly. |
| Specification | Repeated README sections; prose promises deadline misses and physical per-arm measurements that are absent | Consolidate current spec with explicit schemas, authority rules, costs, split definitions and one runbook. Label evidence time versus wall time. |
| Plan | Stopped after failed clean qualification; next noisy sweep correctly withheld | Continue bounded diagnosis/repair under the new review cycle. Allocate a dedicated host, freeze each diagnostic, preserve failures, then use disjoint qualification. |
| Controls and robustness | Scripted tests pass; fixed/adaptive tied; central test additions systematically hurt | Demonstrates instrument/model mismatch, not quorum efficacy. Test information-matched central rules, lower fixed threshold, missing evidence, copied sources, false late sources, and model/format sensitivity. |
| Agent reproducibility | Same pinned model, but shared contexts, no individualized receipts/citations and a mutable-source import | These are repeated decision invocations, not independent expert agents. Version observation/action schemas, prompts, checkpoint, actual source/runtime, encoding policy and deterministic guard; record each invocation and whether it was reused. |

## Concrete defects and limitations

- **R1 — missing versus ineligible:** no semantic guard stops a model voting NONE when it has seen no providers. Nine agents receive fewer private documents per agent, so the empty-context issue confounds the population-size comparison. Required: WAIT for incomplete candidate coverage, with an explicit comparison of any such guard to unguarded v2; do not feed evaluator truth to the guard.
- **R2 — provenance floor:** `select()` unions all roots in supporters' contexts. A root can contradict the choice and still satisfy its quorum. Required: compute candidate-specific supporting roots from observable facts, or rename the intervention as a mere available-document floor. Roots remain fixture-provided ancestry, not measured statistical independence.
- **R3 — tool semantics:** the prompt says probes override accuracy only, but the scripted baseline also overwrites scanned support. Align the declared authority of each tool field; probes cannot establish retention or price. Preserve old scores as historical results.
- **R4 — failures after commitment:** a later tape exception invalidates all earlier-stop policies. Required: record per-call/per-round errors and invalidate only the consumed prefix; never repair by deleting failed records.
- **R5 — context validation:** JSON token-length estimates do not establish that Laya's actual head/options/state encoding is intact. Inspect the pinned encoder's exact truncation stats and rendered option distinction; reject truncation explicitly.
- **R6 — evaluation label:** mock scoring counts complete invoice-record matches, not arbitrary field accuracy. Rename it record exact-match accuracy or implement a separately specified field metric. Use fixture variability rather than implying independent benchmark measurements from deterministic duplicates.
- **R7 — deadlines/probes:** terminal audits occur after evidence cutoff. Preserve that interpretation for v2; revised probes need charged logical ticks before commitment. Do not claim wall-clock service-level guarantees.
- **R8 — model failures versus infrastructure:** v2 had zero schema errors and a completed upload. Its clean-task failure is not evidence of an SSH/queue fault. Diagnose semantic integration before changing infrastructure. Setup-package failure in v1 is separate and resolved by pinned-source import.
- **R9 — reproducibility:** record design, prompt, runtime and fixture hashes, valid/invalid assignments, distinct task clusters, call purpose/agent/round/input hash and actual token usage. Avoid silently importing a moving sibling module.
- **R10 — figures:** public HTML is unsupported; GIF/PNG are supported. Store full replay history, verify frames against event records and separate a rendering failure from scientific execution.

## Claim boundaries

The intended claim is narrow: a supported-evidence stopping rule may trade completion against erroneous commitment under a declared synthetic API-selection environment. It is not autonomous ant behavior, independent model diversity, real supplier evaluation, privacy certification, optimal stopping, or a production-readiness benchmark. A fair negative result is useful. The biological analogy motivates the question; the earlier ant reading found search/recruitment changes important too, so a threshold-only effect must not be oversold.

## Completion evidence required

Regression tests for R1–R7/R9, clean balanced model qualification on fresh IDs, operational completion with no unresolved execution errors, reconciled numerical results, honest uncertainty/denominators, and measured PNG/GIF/replay checked at beginning/event/end. Model or design issues that fail remain open; this audit is not a completion certificate.

