# Knowledgeable newcomers versus a trusted Sybil coalition

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

Local zero-key engineering preparation passed all 198 assigned scripted observations and 36 exact clean qualification packets. API qualification and the 1,944-observation scientific comparison have not yet run at this handoff; the parent operator will add measured results after gated deployment.
