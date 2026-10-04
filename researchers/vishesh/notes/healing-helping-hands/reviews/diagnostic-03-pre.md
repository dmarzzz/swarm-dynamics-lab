# Pre-run assessment: diagnostic-03

- Experiment / owner / stage: Healing Helping Hands / vishesh/codex-regrowth-docs / S0 diagnostic.
- Parent: [pilot-02 post-mortem](pilot-02-post.md).
- Status: diagnostic-only. Broader worlds remain blocked by failed competence.
- Question: is failed report extraction sensitive to output encoding, reasoning availability or Laya's unknown-class description?
- Expected result: a more explicit interface may repair negation and unknown confusion. A valid negative result is that the requested small models remain unsuitable. This diagnostic cannot establish generalization.

## Design and assessment

Use 18 previously exposed development items: six SUPPORT, six REFUTE, six UNCERTAIN, balanced between pilot-02 error forms and earlier forms. Same items and rotated option order for all configurations. Two Qwen variants: neutral A/B/C outcome codes with a one-sentence explanation before the label; original SUPPORT/REFUTE/UNCERTAIN with thinking enabled. One Laya variant: concrete report-outcome criteria including no measurement, unevaluated effects and no results. Compare descriptively to retained failed interfaces; old observations are not new controlled executions.

Unit is a report/configuration pair. Outcomes: class counts, total correct, transport/schema errors, latency and generated tokens. No claim-level propagation or heterogeneous superiority is evaluated. Truth stays in evaluator records. Qwen configurations tie-break by fewer total generated tokens, then variant order. Only a configuration with at least 16/18 correct and at least 5/6 per class can proceed to a new qualification. No lowering of the pilot gate. If none passes, report capability limits and retain exact controls while revising the next plan.

## Changes and unresolved issues

| Issue | Diagnostic | Prediction | Acceptance | Owner |
|---|---|---|---|---|
| Q2 negative confusion | Neutral codes vs enabled reasoning | Negation improves | >=16/18 and >=5/6 per class; no errors | vishesh/codex-regrowth-docs |
| L2 unknown confusion | Explicit criteria | Unknown paraphrases improve | Same development criterion, then fresh qualification | vishesh/codex-regrowth-docs |
| P2 allocation | Dedicated fleet worker | Isolated reproducible execution | Merged exclusive claim + idle check | same |

## Frozen execution plan

- Source is the immutable commit registered before launch; run checks tracked source hashes against that commit. Original model digests and Laya pins unchanged. Qwen Ollama 0.30.5; CPU runtime versions recorded.
- Entry point: `src/diagnose.py --out <new diagnostic-03 directory> --run-tldr <purpose>`.
- Maximum 36 Qwen and 18 Laya calls, 90 seconds per call, 20 minutes whole attempt, one inference process at a time, four CPU threads maximum. No paid model APIs and no new machine creation. Existing fleet allowance only.
- No transport retries; every call has append-only start and terminal event. Stop a configuration on a provider fault; all remaining cells become not-run. No pilot scenarios in this attempt.
- Fresh exclusive allocation: sim-vishesh, claim `vishesh-healing-helping-hands`, merged before deployment. Expiry and runtime recorded in deployment manifest; private inventory never published. Verify exclusive claim immediately before inference. No reuse of another experiment's worker.
- Regression checks: existing instrument tests plus schema/choice mapping checks. Previous qualification failures are why this is diagnostic-only. Next step is a separately frozen qualification using previously untested language fixtures, or another diagnosed repair if these criteria fail.

## Visualization mapping

Mapping D1 binds diagnostic-03/configuration/case to the append-only call journal. Show a class confusion matrix (rows expected, columns observed; raw counts 0–6) and a completion counter (0–18), with failed/not-run shown explicitly. Time is case order, not swarm rounds. Expected labels are evaluator-only; only claim/report reaches models. No spatial animation is meaningful for independent classification probes. Live view is local progress JSON; final confusion-matrix image is the public fallback, alongside latency/token totals. No fabricated swarm frames. At most 54 records; rendering after execution cannot affect model inputs. Validate row totals and counts against qualification records, including missing cases.
