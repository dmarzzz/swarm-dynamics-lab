# S0 protocol freeze — adaptive quorum

Status: exploratory hunch. Formal survey and cross-researcher hypothesis gates remain unmet. S2 is disabled. This protocol is committed before the first model run. Engineering checks may precede that commit.

## Question and competing outcomes

An urgency-adaptive evidence quorum may reduce deadline abstention compared with a fixed evidence quorum, but may increase false commitments. The interesting result is a quality/coverage/cost frontier, not speed alone. A centralized solver may dominate every swarm arm; that is a useful negative result. This study tests stopping under fixed evidence delivery, not autonomous exploration, emergent recruitment, independent minds, biological fidelity or real-world provider quality.

## Assignment, visibility and pairing

A task is a fictional provider-selection job with a best provider fixed by task ID. Six S0 tasks (7000–7005), one seed (1), two deadlines (3 and 6 rounds), and three worlds (clean, copied-true, late-correction) yield 36 task/world/deadline blocks and 144 arm outcomes. Task is the independent analysis cluster; agents, rounds, deadlines and worlds are repeated measurements. Holdout task IDs 9000–9999 remain unopened.

Five scouts receive fixed root-labelled recommendation reports. Round one supplies two roots; round two repeats those roots; from round three a third root is available. In copied worlds the first two rounds repeat one root. In late-correction that repeated root recommends the wrong provider; new roots from round three recommend the truth. These are deliberate boundary fixtures, not realistic error-frequency estimates. Each agent sees its private report plus preceding public reports. Root labels do not establish statistical independence. Each root has exactly one report, deduplicated in the model context. Models do not see world names, truth, task ID, arm, deadline or the hypothesis.

All team policies consume the same locked ballot tape. That makes the stopping-rule contrast exact and avoids attributing model sampling variation to thresholds. The full tape is computed for counterfactual replay; reported policy-call cost is the prefix consumed before commitment, while physical inference cost is separately reported for the full tape. Centralized decisions are a separate tape with the union of available reports. This is a stronger-information comparator with the same maximum information budget, not equal actual token cost. No discussion of peer ballots occurs in this version.

## Arms and endpoints

Majority requires three of five ballots. Fixed requires that majority plus three unique roots among the current reports of its supporters. Adaptive differs only at the deadline, when the root floor falls to two. Root support is measured from currently assigned reports, not assumed causal attribution of the model's answer. A central solver commits on its first non-abstention. Ties cannot meet a strict three-of-five majority. No arm consults the truth or changes a ballot to force completion.

Candidate primary contrast for later promotion: adaptive minus fixed in all-assigned loss at the short deadline in late-correction. Loss is 0 for correct commitment, 1 for wrong commitment, 0.3 for deadline abstention and 1 for invalid outcome. Secondary: false commitment/all assigned, coverage/all assigned, accuracy/committed, rounds to commitment (deadline assigned for abstentions), policy calls and physical inference time. Invalid outputs remain in the assigned denominator. No significance claim from S0, no threshold tuning on the eventual holdout.

The schedule may produce no adaptive advantage because three roots arrive by the deadline. This is intentional: S0 validates mechanics, including targeted boundary unit tests with only two roots. S1 must add independent evidence-arrival timing variation before testing a substantive urgency claim. Do not infer a useful adaptation from a scenario constructed to reward it.

## Qualification and stopping

S0 must finish all assignments, emit schema-valid records, preserve identical evidence between policies, and achieve at least 80% correct commitments in clean fixtures for the central solver and each team policy. This is an engineering screening criterion, not a precision statement. On failure, publish it and revise the instrument before S1; never silently rerun or substitute a better model. No automatic S1 or S2. Abort unresponsive local inference after an outer 30-minute run limit; partial records and the manifest identify incomplete assignments.

Model failures invalidate all policies sharing that failed tape; central failures invalidate only its outcome. Exceptions are stored by class, not arbitrary message text. No outcome retries. A new attempted qualification after a fix gets a new output directory and amendment. Confidence/probabilities are not treated as calibrated correctness.

## Analysis and promotion

Report per-world/deadline counts and paired task differences, including invalid and abstention counts. S1 will estimate task-level variance/discordance for sample sizing, add noisy independent roots, variable arrival times, root-label corruption, and token-accounted centralized/self-check controls. Before S2: reviewed survey, accepted hypothesis, fixed minimum decision value, explicit clean-task margin, sample size, frozen provider/template-disjoint holdout and budget. The existing S0 generator alone cannot establish generalization.

## Sources and amendments

[Pratt and Sumpter primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC1635101/) supplies the urgency motivation. Consulted abstract and methods, not a new full-paper review. Template and design-guide methods are reused; published effects are not imported as calibration constants.

2026-10-03: owner selected local Laya now and Jev via OpenRouter later. Backend migration is documented in BACKENDS.md; no hosted credentials or calls are required for this pilot.
