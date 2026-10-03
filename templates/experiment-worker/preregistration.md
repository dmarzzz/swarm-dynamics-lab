# Pre-registration: template-quorum

Committed before the first S2 run. `coordinator.py stage S2` refuses to queue while this file or
`design.yaml` has uncommitted edits or contains the word TODO, and it stamps their commit on every S2
run. Later changes go under **Amendments** with a date, and a changed design gets a new experiment id.

This file is filled in for the toy so you can see what "complete" looks like. Replace every section for
your experiment. The section numbers follow vishesh's design guide (`researchers/vishesh/notes/seo-poisoning/experimental-design.md`,
*Experimental design* §0–§8), and the headings map onto `templates/hypothesis.md` and `templates/experiment.md`.

## 1. Hypotheses, with directions

- **H1 (manipulation check).** With a wrong shared source in the evidence (W2_FALSE), plurality quorum
  (A0) commits to a wrong option more often than in the clean world (W0_CLEAN).
- **H2 (primary).** In W2_FALSE at dose 0.4, the provenance-aware quorum (A1) has a lower false-commit
  rate than plurality quorum (A0), paired per task.
- **H3 (cost).** A1 pays for H2 with higher delay. We report how much, rather than predicting a size.

Kill criterion: if A1's false-commit rate in the primary cell is not lower than A0's (the CI on A1 − A0
includes 0 or is above it), counting roots does not help under this exposure model, and we stop.

## 2. Contrasts declared in advance

- **Primary:** `design.yaml → primary_contrast`. Stage S2, world W2_FALSE, dose 0.4, false_commit, A1 − A0.
- **Secondary:** delay and regret in the same cell.
- Everything else (other cells, other metrics) is exploratory and labelled that way in the results.

## 3. Minimum meaningful effect and non-inferiority

- Minimum meaningful improvement: A1 − A0 ≤ −0.10 on false_commit in the primary cell.
- Clean-task non-inferiority: in S0 (W0_CLEAN), the arms' false-commit rates may differ by at most
  0.02. (They are identical by construction in the toy. A real experiment must check this.)
- Cost ceiling: mean delay for A1 ≤ n_agents (it must commit before the deadline on average).

## 4. Sample size from S1

S1 gives the discordant-pair rate ψ and the standard deviation σ_d of the per-task difference. For the toy,
S1 (W2_FALSE, dose 0.4) gave ψ ≈ 0.8, which makes the primary contrast trivially powered, so we keep the
default 300 holdout tasks × 3 seeds. In a real experiment, write the McNemar sample-size arithmetic here
from S1's numbers before S2, and set `stages.S2.tasks` to match.

## 5. Units and metrics, with denominators

- **Unit of assignment:** the task × seed draw. Every arm sees the same draw (common random numbers),
  so assignment to arms is within-draw and complete.
- **Unit of analysis:** the episode (one arm on one draw). **Cluster:** the task. Seeds within a task
  are not independent examples.
- **Metrics** (per episode; rates over all valid episodes of the arm in the cell):
  - `committed`: the arm committed before the deadline.
  - `false_commit`: committed to a wrong option.
  - `correct`: committed to the right option.
  - `delay`: reports received until commit, or n_agents if no commitment.
  - `regret`: 0 if correct, 1 if wrong, abstain_cost if no commitment.

## 6. Parse-failure and retry policy (identical across arms)

An episode that raises is recorded with `validity.ok = false`, counted per arm (`invalid`), and never
retried or dropped. A hub run that fails is visible as `failed`, and its tasks are re-queued only by
adding a dated amendment here.

## 7. Agent-population validity checks

The toy agents are not LLMs, so the guide's unawareness probe and minimal-control audit (§3.4) do not
apply. For LLM agents, name the probe and threshold here.

## 8. Seeds and splits

- Dev tasks 0–199 (S0, S1). Holdout tasks 1000–1999 (S2), never touched before S2.
- Seeds: S0 [1], S1 [1, 2], S2 [11, 12, 13]. Fixed in `design.yaml` before any run, and never chosen after
  looking at results.

## 9. What we may claim

A result here is about this exposure model: the shared source's identity is supplied by the environment
(`root`), not inferred from text. It does not show that provenance can be recovered in deployment
(guide §0, gate 5).

## Amendments

None.
