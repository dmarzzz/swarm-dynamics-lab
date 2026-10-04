# Post-mortem: v3-q0-a1

- Experiment / owner / stage / date: discussion-dose-v3; dmarz/discussion-bench-v3; S0 qualification; 2026-10-04 UTC.
- Parent/pre-run: [v3 review repairs](v3-vishesh-fixes-post.md), [assessment](v3-q0-a1-pre.md), [frozen launch](../benchmark-v3/launches/v3-q0-a1.json).
- Runtime: `883d310b37a2fcaca7612e85d150febd49200e82`; Haiku `claude-haiku-4-5-20251001`; Python 3.12.3.
- Results, hashes and reproduction: [RESULTS-Q0](../benchmark-v3/RESULTS-Q0.md), [analysis receipt](../benchmark-v3/results/v3-q0-a1/analysis.json).
- Disposition: **diagnostic**. Execution complete; qualification failed; no expanded sweep or holdout.

## What ran and what happened

96 planned → 96 started → 96 terminal → 96 graded → 96 analyzed cases; 636 planned/started/terminal physical requests. Zero provider or validation failures, zero missing assignments/usage, zero duplicates, zero unresolved calls. All 1,790 events and saved requests replayed. Ten uploaded artifacts and 17 downloaded files matched hashes. Model usage: 3,580,812 input / 161,285 output tokens; $4.387237; approximately 34 minutes. No resource pressure on the dedicated 2-vCPU/4-GB machine.

Full-evidence clean decisions were 2/6; clean reports-only majority decisions 1/6; the frozen requirement was 5/6 each. All six clean diagnostics extracted every value correctly. Four then selected an infeasible option. Both R3 clean arms reached 6/6, but we retain the failed declared gate. Attack adoption/return was 6/6. Reports-only abstained in 6/6 attacked votes while passing false memory into 4/6 parents. Private/board wrong parents were 1/6 and 0/6. Both declared contrasts were zero across their three assigned worlds. The six-world mixture and failed clean competence preclude broad efficacy claims.

Memory fixtures yielded 23/36 justified responses, 13/36 unsupported answers and 6/36 locally grounded wrong inheritances. These harms are measured outcomes. Conflict/copy-counting behavior should not be conflated with malformed outputs. Nine unsupported clean swarm-parent answers were correct numbers with extra agreeing lower-priority citations; the strict support rule is disclosed separately.

## Visualization review

Mapping `v3-fleet-stage-ledger-1`: live three-agent checkpoints, votes, contested-value endorsements and majority memory were delivered during execution. The saved public replay has 252 swarm frames without thinning, covering all 48 swarm episodes. Aggregate progress covers 96 cases; full local HTML includes diagnostics and memory fixtures. The last swarm frame precedes the memory fixture block and is not the terminal batch counter.

Local browser verification after artifact retrieval checked evidence steps, automatic playback, a terminal swarm outcome and a memory fixture outcome against saved rows. The public replay endpoint returned 404 although the artifact was downloadable with the private hub client and hash-verified. This prevents claiming working embedded public playback. Raw/local replay is the verified fallback. Preserve it; repair delivery separately without restarting a shared hub during unrelated runs.

## Experiment quality

The instrument executed the intended contrasts and exposed a useful vote-versus-memory separation. It did not qualify this model configuration for a broader causal experiment. Board/private share checkpoints, work rounds, call/output ceilings and barrier semantics; board consumes more actual input tokens and cost. Independent-arm zero harm reflects target omission and no parent utility. Three worlds per evidence stratum provide no useful broad uncertainty estimate. All ambiguous raw target conflicts were lost at merge, including cases with correct retained values. Parent support is intentionally local to its packet.

The independent instrument review subsequently passed and its source hashes match all 15 frozen files. That review does not certify model capability. No formal hypothesis changed status. Confirmation remains unopened.

## Failure and repair ledger

| ID / kind | Evidence and cause confidence | Action and acceptance criterion | Owner / status |
|---|---|---|---|
| Q0-C1 / capability | 4/6 infeasible clean full-evidence choices despite exact extracted values; verified behavior, underlying model/prompt cause unknown | Atomic constraint and claim-to-vote probes; compare stronger permitted model. Then ≥5/6 on both fresh disjoint qualification gates with complete accounting | dmarz/discussion-bench-v3; open, no repaired-model result claimed |
| Q0-C2 / capability | Reports omit facts and abstain inconsistently with their own claims | Separate extraction coverage from decision consistency; version any response-contract change and requalify | Same owner; open |
| Q0-M1 / measured design limitation | 4/6 attacked reports-only votes abstain but parent inherits false fact | Preserve baseline outcome; a future uncertainty-preserving or vote-gated merge is a new treatment, paired against this baseline, not a retroactive fix | Same owner; documented, extension deferred |
| Q0-M2 / measurement interpretation | 9/24 clean parents penalized for extra agreeing secondary citation despite correct numbers | Keep frozen labels and publish citation-specific diagnostic; review intended citation contract before any successor scoring amendment | Same owner; disclosed, decision open |
| Q0-R1 / audit portability | Python 3.9 changes five aggregate float last bits, ≤4.44e-16; exact Python 3.12 replay passes | Frozen audit uses 3.12. Version stable aggregation/comparison in successor; regression across supported Python versions, identical discrete results | Same owner; current audit verified, portability repair open |
| Q0-R2 / visualization delivery | Public replay route 404; private ten-artifact retrieval/hash check passes | Diagnose deployed allowlist/version mismatch without disturbing active runs; acceptance: public replay loads and plays all recorded swarm frames | Same owner; open, local fallback verified |
| Q0-R3 / preparation | Reporter environment absent before first call; explicit age-key provisioning fixed it | Reporter role applied and preflight passed before dispatch; no paid response lost | Same owner; closed before launch |

## Next run

The user explicitly permitted a smarter model after seeing the capability concern. Prioritize a small model-only diagnostic, preserving prompt/evaluator initially, then a separate explicit constraint-checking response probe if needed. A better response contract, more output/reasoning allowance, or model capability could each explain improvement; changing them simultaneously would not identify the cause. Finite-domain abstention instructions may also contribute; test them rather than asserting a diagnosis.

Q0's six worlds are now development material. Any readiness claim requires a newly frozen disjoint qualification split, unchanged ≥5/6 clean gates, complete usage/assignment reconciliation and zero invalid/provider-failed outputs. Keep the 24 confirmation worlds closed. A new attempt must name `v3-q0-a1` as parent and freeze source/model/configuration, budget and stopping conditions before execution. There is no automatic successor. This heartbeat ends with durable records, a committed candid report and retirement of the unused temporary host.

## Dated follow-up to both reviews, 2026-10-04 UTC

Read Shadow's independent pass-with-fixes review during successor planning. Add Q0-R4 (invalid-ballot vote metrics can erase a two-vote majority) and Q0-R5 (provider_failure omits its safe reason). Both are open successor repairs, owned by dmarz/discussion-bench-v3, with exhaustive quorum and allowlisted-reason tests specified in [NEXT-RUN](../benchmark-v3/NEXT-RUN.md). Neither affects Q0's fully valid, provider-successful observations. Vishesh's pass remains its own verdict; do not describe the two reviews as unanimous. Conflict loss under this majority single-value merge is structural, not an identified model behavior.
