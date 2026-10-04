# Knowledgeable newcomers versus a trusted Sybil coalition

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `b51e3f1f` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — The 36-packet qualification passed; the newcomer-trust main study has launched but no final comparison is reported at this cutoff. Basis: Qualification is complete and the tracked deployment record now confirms S1 launch. The audit-policy comparison has no reconciled final counts here. Reports, attacks and trust remain simulated and the model only synthesizes selected packets; dispatch does not establish a treatment effect.
- **sample_size_summary:** Q0: 6 worlds, 36/36 valid packets. S1 launched: 24 paired worlds × 81 cells = 1,944 assigned answers across 3 sampled rounds; completed count not reconciled in repo.
<!-- experiment-evidence:end -->

Exploratory follow-up to [the scaling study](../sybil-scale-api/RESULTS.md). The previous study achieved 98.6% specialist accuracy while rejecting 62.8% of honest specialists because specialist facts were repeated. This study makes each attacked specialist fact available from exactly one honest newcomer and asks whether continued verification preserves that scarce information after a previously useful coalition starts lying.

This is an owner-authorized S0/Q0/S1 study in `notes/`. It is not an accepted hypothesis, a completed novelty survey, an independently reviewed protocol, or a formal S2 experiment. The owner explicitly waived independent review for this launch; see [the waiver](WAIVER.md). Engineering qualification, cost limits, preregistration, raw evidence, and truthful reporting remain in force.

## Question

Can continuing audits of established trust while investigating little-audited identities recover unique honest information after a coordinated attack, under the same verification and message budgets?

## Setup

Python 3.12; pinned dependencies in requirements.txt; Haiku `claude-haiku-4-5-20251001`, temperature zero. All identities and eight-round audit histories are simulated; the API synthesizes selected packets at rounds 4, 5 and 8. The parent operator supplies an isolated runtime on the exclusively claimed fleet host; no private inventory is published.

## Protocol

There are 18 honest veterans and six honest newcomers arriving in round 4. Three newcomers carry one unique current fact each; three carry common facts. One controller produces exactly 16 report messages per round while splitting them across 1, 4, or 16 identities. With 4 or 16 identities, half arrive in round 4 and the rest are veterans. At one identity the controller remains a veteran. Newcomer status therefore does not identify honesty. All role labels and controller membership remain evaluator-only; visible identity codes and report order are shuffled.

Each world runs eight simulated rounds. All reports are useful before round 4. The sleeper coalition lies from round 4 onward; the relapse stress test lies in rounds 4, 7, and 8. The clean counterfactual uses the same identity structure and tells the truth throughout. Values change every round, so earlier correct values cannot answer the current question. The controller's current rare values are truth plus or minus seven, counterbalanced deterministically.

Three policies receive four independent claim checks and admit exactly 12 report messages each round:

- **Random:** choose four currently active identities uniformly, then one report per selected identity.
- **Reputation:** check the four identities with the highest observed Beta(1,1) audit-pass score.
- **Renewal:** check two highest-reputation identities and two other identities with the fewest observed checks.

All policies use the same admission rule: exclude current failed messages, prioritize currently passed messages, then rank by public identity reputation, with matched random tie breaking. One check concerns one claim, not every claim or the identity as a whole. There is no per-identity admission cap. External audits are simulated: true claims pass with probability 0.95 and false claims with probability 0.05. Policies see only selected audit outcomes. Distinct identities do not certify independent evidence.

The pinned Haiku model synthesizes current admitted packets at rounds 4, 5, and 8. It receives public audit counts and current message check status, but no hidden ownership, true answers, future reports, or outputs from other rounds. The actors, audits, reputation state, and attacks are scripted; there is no model memory, autonomous model attacker, learning policy, or independent model per identity. Controller model computation is identically zero in every condition, and controller messages remain 16 per round. More identities alter per-identity exposure and reputation concentration; those are measured mechanisms, not extra controller message/computation resources.

## Metrics

The primary outcome is exactly correct answers for three specialist facts divided by three. Secondary measures include false specialist outputs, harmful report share, common-controller report share, unique contributors, honest specialist retention, and available truthful evidence. The predeclared identity contrasts compare 16 versus 1 identities and the renewal-versus-reputation interaction across those counts. See preregistration.md for denominators, missing-data bounds and paired-world analysis.

## Design and outputs

The complete paired matrix is 24 fresh world clusters × 3 identity counts × 3 policies × 3 strategies × 3 sampled rounds = **1,944 S1 model calls**. Q0 uses 36 clean packets with full, partial, and sparse information; S0 uses the same 36 qualification packets plus 162 scripted study observations. Full histories for all eight rounds are retained. The world, not each identity, round, or API call, is the analysis unit.

The predeclared primary contrast is renewal minus reputation for specialist accuracy at round 8 with 16 controller identities under the sleeper attack. Random auditing is a strong equal-cost comparator. Relapse is a predeclared stress test, not an independent confirmatory holdout. We report all cells and descriptive paired-world bootstrap intervals, including null and adverse results. No policy is tuned on S1 results.

[Design](design.yaml), [preregistration](preregistration.md), [visualization mapping](VISUALIZATION.md), and [run instructions](RUN.md) specify the implementation. The UI will show recorded reputation and rare-newcomer admission through logical rounds 1–8, model measurements only where sampled, and the final accuracy/influence tradeoff. Detailed histories are retained privately; supported final PNG and animated GIF are public.

## Interpretation limits

This tests a small constructed information-selection problem, with a fixed audit model and synthetic changing integers. It does not establish real-world Sybil resistance. Unique honest truth is scarce only during attack-active rounds; the clean coalition supplies additional correct rare reports. Unequal age composition across identity counts and concentrating the same audit resources over different numbers of identities are explicit manipulation features. Correct values missing from admitted reports may be guessed; the evaluator-only available-truth diagnostic is an evidence ceiling, not an absolute bound on lucky guessing. The three-round warm-up permits only twelve checks across the veteran population; many veterans therefore remain sparsely audited. Reputation/audit-exposure diagnostics make that limited trust formation visible. The result can be useful even if renewal loses to random checking or every policy fails.

## Results

**S1 completed and verified: 1,944/1,944 observations across 24 paired worlds, with zero invalid or missing calls.** In the predeclared sixteen-identity sleeper condition at round eight, specialist accuracy was 26.4% with random audits, 20.8% with renewal and 12.5% with reputation audits.

Renewal minus reputation was +8.3 percentage points (descriptive 95% paired-world interval −2.8 to +19.4). The point estimate is below the predeclared +10-point useful-effect marker, and uncertainty includes both zero and larger useful effects. Renewal minus equal-cost random auditing was −5.6 points (−16.7 to +5.6). These results do not establish an accuracy advantage for renewal.

Only 25.0% of unique honest specialist reports survived admission under renewal; random retained 30.6% and reputation 23.6%. The low surviving truth availability shows that selection itself loses much of the needed information. The short three-round warm-up supplies only twelve total audits, so this tests sparsely established trust. Fixed-budget identity-count effects are mixed and uncertain; no universal amplification or resistance claim follows.

[Full results](RESULTS.md), [all cell measurements](results-cells.csv), [complete analysis](results-summary.json), [verification receipt](verification-summary.json), and [S1 post-mortem](reviews/s1-001-post.md). Clean qualification passed 36/36 exact packets. Q0+S1 used 1,980 calls and cost **$3.132219 actual**, with usage known for every call. The final image and eight-frame replay were verified publicly; raw data and ledgers are archived, the claim is released, and the temporary dedicated host has been destroyed. Formal S2 remains disabled.

## Allocation correction — 2026-10-04 UTC

The owner's updated inbox requires a dedicated host for each experiment. S0 and Q0 historically completed on sim-dmarz-4 under dmarz-sybil-followups; those completed results and runtime fingerprints are preserved. Before S1, this study moves to the dedicated host sim-dmarz-sybil-newcomer under claim dmarz-sybil-newcomer. Provisioning, claim exclusivity, migration and ledger continuity remain pending the parent operator's verification. S1 is not launched by this correction. No simulator, assignment, model, evaluator or source/configuration fingerprint changes.

Across the separate hosts, the existing $60 bundle cap is partitioned into at most $50 total for sybil-budget-api and $10 total for sybil-newcomer-api. Both hosts retain the same settled 52-call checkpoint ($0.366548). The budget host permanently reserves the $10 peer allocation; the newcomer host permanently reserves the $50 peer allocation. Historical charges are not reset. Duplicating the settled checkpoint in both guard copies makes the aggregate bound stricter, rather than creating extra spending authority.

These permanent peer reservations are inter-host allocations, not API charges, model calls or unknown-billing failures. Do not count them as actual experiment spending. Final actual cost is the sum of the separate per-study usage ledgers. Existing per-study conservative reservation/call limits still apply, with the new partition providing the tighter real-spend limit. The parent must verify the guard state and exclusive allocation before launch; this document does not claim that provisioning or migration is complete.

## Verified closeout — 2026-10-04 UTC

The parent verified durable local/hub S0/Q0/S1 evidence and private hashed archives of both ledgers and the allocation record. Claim dmarz-sybil-newcomer was released (agentops PR130; hub release event 34510), with no active claim remaining. The temporary sim-dmarz-sybil-newcomer host was destroyed through the established Dmarz backend/account using a reviewed saved plan limited to its five resources and inventory; twelve other host entries were unchanged. Fleet removal PR131 merged. Publication of the generated inventory update remains a parent bookkeeping step.

The [filed final figure](../../../../artifacts/sybil-newcomer-api-s1/sybil-newcomer-api-s1-v1.png) preserves provenance in the project. Flight Deck strict validation passed with thirty artifacts, zero errors and zero warnings. The scientific result remains exploratory and the historical public-plan preflight evidence gap remains documented; closeout does not remove it.

Final infrastructure receipt (2026-10-04 UTC): generated inventory PR132 merged as `751c72fbf2b7464e91de2f321f0a18a2aca2b365`; all other twelve entries unchanged. The newcomer allocation is fully closed. See [records/closeout.json](records/closeout.json).
