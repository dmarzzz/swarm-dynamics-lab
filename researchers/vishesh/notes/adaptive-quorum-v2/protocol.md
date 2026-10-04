# Version 2 exploratory protocol

Freeze before model qualification. No formal hypothesis acceptance; S0 and engineering checks only until qualification. S2 is disabled.

## Estimand and predictions

Candidate primary: adaptive minus fixed all-assigned loss, nine scouts, short deadline, late accurate evidence. Prediction is conditional: lowering the required unique supporting roots from three to two near deadline may reduce abstention, but may admit a wrong or ineligible provider. A practically useful treatment must improve loss without a rise in constraint violations. S0 cannot establish either claim.

Loss: zero for the cheapest eligible choice, one for an ineligible choice or invalid output, 0.5 for abstaining when a provider is eligible, 0.25 for a more expensive eligible provider, and zero for correctly returning NONE when all are ineligible. Report constraint violation and abstention separately. NONE is a task answer, WAIT is an epistemic deferral.

## Task and manipulation

Three fictional extraction APIs, four attributes: scanned-PDF support, zero retention, field accuracy, and per-document price. Requirements: scanned PDF, zero retention, accuracy at least 90; choose cheapest eligible. Provider labels and table row order are seeded; truth depends only on task ID. A batch has 20 synthetic invoice records. A mock API returns fields according to the provider's hidden accuracy; the scoring tool reports exact-match percentage. Test output cannot verify retention.

Qualification uses six tasks (7200–7205), clean evidence, five and nine scouts, deadlines three and six: 24 blocks. Every candidate answer appears among the tasks, including NONE. Development reserves tasks 7300–7335 with clean, stale-favorable, copied-favorable and conflicting reports; timing fast, late and stalled. Holdout 10000–10999 remains unopened. Exact executed design and code hashes accompany every run.

Nine scouts have distributed evidence, not different model weights or fabricated expertise. Five-agent controls partition the same document budget. At each round, scouts see the previous shared board plus their own current delivery; raw reports are shared one round later. The central solver sees the union at that round. This one-round information advantage is explicit; a central result is not a pure population-size effect.

Timing: the three evidence roots appear at rounds 1/2/3 (fast), 1/3/5 (late), or 1/3/never (stalled). Root zero may be stale or copied; root one supplies a newer factual table; root two supplies another table. All tables are observations, not guaranteed truth. Multiple documents from the same origin count once. Qualification is clean/fast. The development matrix is staged, not automatically launched.

## Policies

- majority: first strict majority among five or nine votes, WAIT excluded.
- fixed: strict majority plus at least three visible evidence roots across supporting scouts.
- adaptive: same, but only two roots required at the final round.
- vote-at-deadline: strict majority only at deadline; controls for merely waiting.
- central-at-deadline: one model at the deadline over all available evidence.
- central-targeted: central deadline answer, up to two local tests of its preferred provider and the lowest listed-price alternative, then one revised answer.
- central-random: same two-test budget, seeded random distinct providers, then one revised answer.

Team policies share a full locked tape so differences isolate the stopping rule. Full-tape inference costs are recorded separately from counterfactual consumed-prefix costs. No causal claim about interactive search, recruitment or social persuasion is made. The verification contrast is central-targeted versus central-random; do not attribute a bundled verification benefit to quorum.

## Quality gates, analysis and budget

All assignments are written before model load. No retries of model outcomes. Schema, finite probabilities, valid option set and context-length checks are mandatory. A failed team tape invalidates its four policies, while separate central decisions fail separately. Unknown/missing eligibility is not filled from evaluator truth.

S0 pass requires zero invalid outcomes and at least 80% correct selections in each arm/population/deadline clean cell. With six tasks this means five or six correct; report counts, not a precision claim. If any cell fails, publish it and stop before S1. Do not tune on these outcomes and silently repeat them. The independent unit is task; paired analysis retains worlds, deadlines and team sizes inside task clusters. No p-values or claims of robust improvement from S0.

Local CPU inference only, two threads, at most 30 minutes per qualification. No API spending or real supplier calls. Record source/checkpoint/dependencies, physical calls/input tokens/time and policy-prefix calls. Output directories are immutable attempts. Jev via OpenRouter requires a separately verified adapter and secure credentials; backend results are never pooled.

## Promotion plan

After a passing qualification: commit a bounded development matrix before running it, examine false commits versus delay and cost, estimate paired task variance, and test root mislabelling and label-order robustness. Deeper prior-art review and another researcher's acceptance precede a powered holdout. This revision does not inherit formal acceptance from any other experiment.
