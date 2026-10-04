# D1 results and postmortem

D1 completed144/144calls and480/480assigned decisions with zero model retries, zero provider errors, zero missing usage records and zero disagreements between the instrument and independent decoder. The worker exited; terminal reporting and rendering completed. Model cost from returned token usage is USD0.178341. Infrastructure cost is separate and fits the reserved USD0.50 hold inside the existing USD5 authority.

## Results

| Interface | Correct / assigned | Valid response decisions | Model calls | Model cost |
|---|---:|---:|---:|---:|
| A: legacy learner instructions |40/96 (41.7%)|48/96|12|$0.029679|
| B: clean executor instructions |82/96 (85.4%)|96/96|12|$0.027618|
| C: keyed evidence |88/96 (91.7%)|96/96|12|$0.032591|
| D: no notebook |89/96 (92.7%)|96/96|12|$0.025189|
| E: one case per call |96/96 (100%)|96/96|96|$0.063264|

Each arm has32decisions per world. World610/611/612 correct totals: A16/11/13; B26/25/31; C32/27/29; D32/28/29; E32/32/32. These are three worlds, not96independent replications. All prespecified cell and paired-contrast results remain in summary.json.

E alone meets the prespecified candidate gate:8/8correct in every world/context, with all outputs valid. This qualifies E for separately planned held-out confirmation, not a culture pilot or general reliability claim. E improves on matched D by0/4/3decisions across the three worlds, at8times as many calls and2.51times the recorded model cost. Compute is not matched.

## What the large legacy gap actually means

All six invalid A responses occur in release or migration-old. They emit bare ship/hold rather than documented console commands. The frozen strict scoring correctly marks those48assigned decisions wrong. There is no provider error or missing response: this is command-contract failure.

Post-hoc diagnostic, not replacement scoring: interpreting those bare words as actions matches43/48truth labels. Together with40strictly correct decisions, that would give83/96semantic matches, compared with B's82/96. This unregistered alias interpretation cannot promote A, but shows why the large A-to-B strict-score gain must not be sold as evidence of better reasoning. Renaming the console also changes A's command compliance, so its old/new gap is not evidence of cultural transfer.

Keyed evidence improves pooled strict accuracy by6/96 over B, but world changes are+6,+2,-2. Removing the notebook adds only1/96 overall. Neither result establishes a generally beneficial intervention. One-case calls eliminate all seven errors seen in D in this small screen. Incident equivalent-input inconsistencies by arm: A3,B2,C2,D1,E0.

## Process assessment

Prospective source:6b3f708d3cf69640a967f8b0b73c6af6069fef22. PLAN.md and D1-PRE.md were published before calls. The exact immutable plan was registered, its hash and public page verified, and every call received its condition TLDR before start. All19offline tests passed locally and on the dedicated host. The owner waived researcher review; none is claimed. Execution used the owning operator on registered, exclusively claimed sim-theseus-d1 under the published owner-directed routing amendment. One allocation,144calls maximum,one worker,two-hour deadline,zero retries. Credential values were delivered only through encrypted SSH stdin to process memory; none is in these records.

The earlier blocked assessment and v2 failures remain historical. No stopped v2 ledger was restarted. Native D1 adapter validation is now measured for this pinned model and route. An instrument command-compliance weakness remains visible in A; no saved score was changed to improve the outcome.

## Next plan change

Freeze E as the candidate executor and D as its matched batching comparator. Confirm on fresh held-out worlds with separately reported command validity and semantic correctness. Avoid presenting A-to-B as a reasoning improvement; use explicit command schemas and audit aliases diagnostically without accepting them after the fact. Preregister the next seeds, repeated sampling, budget and gate before new calls. Only after competent execution replicates should inheritance/turnover be reintroduced. D1 tests execution reliability, not survival of swarm culture.

No next-stage model calls are included in D1 or launched automatically by its candidate gate.
