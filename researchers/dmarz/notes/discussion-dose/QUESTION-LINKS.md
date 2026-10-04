# Research question links

The authoritative records remain in the [question atlas](../question-atlas/candidates.json). This file is an experiment-side cross-reference; it does not change their review status or hashes.

| Question | Exact title | Connection and boundary |
| --- | --- | --- |
| SEC-47 | Where does the full fork-and-return chain actually fail? | Primary. Track exposure, private endorsement, returned report, discussion, final vote, memory admission and fresh-parent consequence. Vary discussion dose. Controlled initial exposure is not autonomous discovery; the original preseeded-state versus exposure hypothesis is not fully tested. |
| SOC-07 | Protect private judgments before public discussion | Related measurement design. Private initial ballots and nonfeedback checkpoint probes preserve a record of disagreement. We do not manipulate public versus private disclosure of initial ballots, so this is not a direct SOC-07 test. |
| SEC-52 | Do small per-merge failures accumulate across generations? | Related extension. One restart detects immediate inheritance. Multiple generations, regrowth and long-run accumulation remain future work. |

Working hunch: discussion duration changes the probability and timing of correction versus amplification of a false fact introduced through one child. This fits SEC-47 without another near-duplicate atlas entry. Formal promotion requires the existing survey and independent hypothesis-review gates; the present submission is an exploratory environment and plan.

## Original pilot evidence

The [results and reflection](RESULTS-AND-REFLECTION.md) localize two SEC-47 stages: four of six attacked acquisitions initially adopted and returned the false value, but contamination was absent before discussion; separately, one parent answered incorrectly after the required fact was omitted from an otherwise true merged memory. The six-world pilot does not isolate a causal discussion effect, directly test SOC-07, or test the cross-generation accumulation in SEC-52. No formal hypothesis status changes.

The [implemented v3 benchmark](benchmark-v3/README.md), based on the [v3 plan](V3-EVAL-PLAN.md), keeps SEC-47 as the primary question and adds answerability, matched-call private work, provenance tracing and parent-memory diagnostics. It is offline-qualified software, not a model finding. The optional multi-generation v4 remains a future SEC-52 test. No new atlas entry or formal hypothesis is needed; independent review and the separate model launch remain pending.

## D1 stronger-model diagnostic

The [completed D1 comparison](benchmark-v3/RESULTS-D1.md) isolates model identity on 60 identical saved requests/model. Sonnet improves some decision and memory behavior but fails both clean gates; both models propagate all six locally supported false memory values. This refines SEC-47’s baseline-versus-return/merge distinction without identifying a discussion effect. The [D2 proposal](benchmark-v3/D2-PLAN.md) studies canonical decisions and atomic predicates before fresh qualification. It is published but unstarted; no atlas or formal hypothesis status changes.
