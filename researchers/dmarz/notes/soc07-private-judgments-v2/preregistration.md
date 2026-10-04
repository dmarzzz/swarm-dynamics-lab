# Preregistration: SOC-07 v2 (exploratory)

Written 2026-10-04 UTC by dmarz/orbital-orchestrator before any v2 run. Exploratory: there is no reviewed survey or accepted hypothesis for this question, and cross-researcher review is waived by dmarz. Nothing here is confirmatory.

## Frozen comparison

- Primary: PRIVATE minus PUBLIC public-team success over all assigned S1-L episodes (240 assigned; an episode that does not complete counts as a failed decision), regimes weighted equally, 95% world-cluster bootstrap stratified by regime, 10,000 repetitions.
- Reported with it, in this order: the manipulation check (share of minority-regime PUBLIC episodes whose valid first answers are not unanimous), team success per arm and regime with the `at_ceiling` flag, the per-regime differences, and the secondary measures listed in the README.
- Interpretation rule, fixed now: if the manipulation check is below 50%, or PRIVATE and PUBLIC are both at 1.00 in every regime, the primary difference is reported but described as uninformative about disclosure. A difference whose interval includes zero is not evidence of equivalence.

## Stop rules

- S0 must pass every check; P0 must parse and match the key; S1-Q needs at least 10 of 12 correct and 11 of 12 valid; S1-R needs the v1 validity gates and clean-regime competence (at least 13 of 16 in PRIVATE and in PUBLIC); S1-L needs the v1 validity gates and the `informative` check. A failed gate stops the chain; no stage is rerun to obtain a different result.
- Hard call caps: P0 1, S1-Q 12, S1-R 672, S1-L 4,080. Ledger cap USD 150. Stage time limit 6 hours. A stage halts on authentication, permission or malformed-request errors, a response from a different model, unexpected cache usage, a billed amount above its reservation, a detected truth leak, exhaustion of the public-path budget, or five consecutive provider failures (as v1).
- **Futility rule (added 2026-10-04 ~09:45 UTC, before any v2 data, on dmarz/fleet-monitor's same-researcher check):** v1 showed that a replay at team success 1.00 in both arms makes the live stage a null by construction. If S1-R ends with PRIVATE and PUBLIC team success both 1.00 in every regime (the `at_ceiling` flag), S1-L is not launched; the study stops there, that is reported as the result, and a harder generator is a new design version. The chain is therefore launched in parts: A `s0`; B `p0,s1q,s1r`; C `s1l`, only after the operator has read S1-R's hub metrics and `at_ceiling` is 0. The S1-Q gate is unchanged.
- If S1-Q fails: read every miss's rendered prompt and returned text before any change (lessons item 6), then decide between a generator repair and stopping. The model stays Opus 5.5.

## Budget

Estimate about USD 55 for the whole chain (README). Cost is not a gate per dmarz; actual calls, tokens and dollars are reported to the hub and in each post-mortem.
