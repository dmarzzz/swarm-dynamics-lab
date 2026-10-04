# SP-02: quote-only repair qualification passed

**FINISH the repair qualification.** SP-02 quote-only repair qualification passed: 40/40 valid calls; 120/120 source and 280/280 report selections correct; 40/40 decisions; 20/20 exact paired roots. Native quotations and code-derived facts are distinct. New API cost USD0.314064; authored grammar only, not field reliability or swarm efficacy.

[Immutable prospective plan](https://github.com/dmarzzz/swarm-lab/blob/567cda03b17060649d9f8d7d4bc89bb133944f84/researchers/vishesh/notes/decision-models/quorum-of-mirrors/packet-study/span-v2/PLAN.md), [summary](../results/QM-SP-02/summary.json), [all-assignment traces](../results/QM-SP-02/traces.html), [replay](../results/QM-SP-02/audit.json), [cost](../results/QM-SP-02/closeout.json).

## What changed and why

R1's native traces exposed two errors hidden or mishandled by fact prediction: an operating quotation encoded as stopped, and unknown evidence paired with a definite zero. SP-01 changed the model output to literal evidence selection with deterministic normalization. It got all 400 decoded facts and all 40 decisions correct, but failed its strict source representation rule in 15 cases: it quoted a plan-only source instead of returning null. That original 25/40 exact-packet and 11/20 exact-pair qualification remains failed. See [SP-01 post-mortem](SP-01-post.md).

SP-02 prospectively asks for a source clause in every case. Select the corrected/current observation when available; otherwise retain the explicit plan clause. Code derives unknown/null from a plan and prevents it from voting. Reports retain assertions, hedges and plans independently of source support. The model predicts neither numeric values nor source status. Wrong selections are never replaced by the correct clause elsewhere in the packet, and a plan chosen despite an available observation still fails grounding.

This is a changed interface tested on a fresh cohort, not a rescoring of SP-01 into success or a randomized causal old/new comparison. The exact text parser remains a perfect same-input baseline; use it directly when this restricted grammar applies. Native qualification tests whether the model can follow the selection contract, not whether a model is needed for this grammar.

## Frozen acceptance and observed results

| Measure | Observed / assigned |
|---|---:|
| Started / valid / unstarted | 40 / 40 / 0 |
| Correct source clauses | 120/120 |
| Correct code-derived source facts | 120/120 |
| Correct report clauses | 280/280 |
| Correct code-derived report facts/modes | 280/280 |
| Correct label vectors | 40/40 |
| Correct source-majority decisions | 40/40 |
| Grounded clause/fact conjunction | 40/40 |
| Exact paired roots | 20/20 |
| Common-report invariance | 20/20 |

The unchanged SP-02 gate required every component and all 40 calls; it passed. Execution complete: `True`. Stop reason: `None`. No retry, fallback or main evaluation. All failures and missing assignments remain visible in the audit. No final-answer accuracy is substituted for clause/fact correctness.

Five families each contribute four roots: observed-positive, observed-negative, absent-positive claim and absent-negative claim, with one/three-copy variants. In a full cohort the 40 final targets are 10 ONE, 10 ZERO and 20 DEFER. The source evidence remains fixed within each pair. The saved mechanism audit found 20 plan-only source clauses decoded as unknown, 100 observed clauses, zero false observation promotions and zero false abstentions ([checks](../results/QM-SP-02/mechanism-checks.json)). Changed copies add length/order effects, so no pure identity-effect claim follows from the contrast.

## Evidence review and limitations

All 40 raw responses and all 40 assignment statuses were replayed against the frozen manifest, selected clauses and software-derived facts. Manual coverage is 10 actual responses: both variants of the first lexicographic root per family plus every miss; [coverage](../results/QM-SP-02/manual-trace-coverage.json). Raw `parsed` quotations, software `decoded` fields, actual usage and generation IDs remain separate. No hidden reasoning trace is available or claimed.

Twenty-two offline checks passed, including 1,000 packets across ten seeds and explicit negative tests for plan-vs-observation, null output, cropped markers/negation, wrong entity/time/initial clause, and launch/budget guards. Fresh native assignment labels were automatically validated with typed construction and a same-input parser before launch; the operator did not inspect individual fresh cases beforehand. Same-author construction/scoring is not independent annotation.

Twenty authored paired roots share five grammar mechanisms. No estimate of field reliability, authenticated real provenance or interacting swarm benefit is established. A hypothetical 20/20 IID success lower 95% bound is about 0.832; the authored dependence does not satisfy the population premise. Current inspected qualification data are development material; the historical 96-case evaluation remains unused. The quote-only contract covers explicit source statements, not empty or unsupported free-form source documents.

## Costs and operational closeout

SP-02 API cost USD0.314064; SP-01 cost USD0.310122. This repair cycle therefore used USD0.624186 API across 80 completed calls. Both attempts had separate USD1.92 worst-case envelopes and neither created new funds.

Cumulative known API charges are USD1.55619096, plus retained historical unknown reservations USD0.061344, for exposure USD1.61753496. Remaining API authority USD6.38246504; unchanged USD8 API/USD1 infrastructure cap. All 182 prior call rows, original reservation history, settlements and both original extension receipts were retained. No uncertain cost was released and no budget extension was added.

SP-01's ledger migration preserved exact bytes and fenced the old path. SP-02 reused that sole canonical ledger in place on the same approved-account machine under a fresh exclusive claim. Public immutable plan/TLDR, request/corpus/runtime hashes, workload/account, provider/pricing and cumulative allocation checks passed before calls. Worker exit, hub terminal state and 7 remote artifact hashes were verified before release. This allocation lasted 266s, estimated USD0.005278, not an invoice. Other experiments' workers were untouched.

The authored [scientific review](../results/QM-SP-02/scientific-review.json) separates execution, qualification, interpretation, reporting and cost; the shared finalize hook supplies operational metadata only. Researcher review was not required by owner direction.

## Next action

**FINISH this bounded repair cycle; no main evaluation or further paid retry.** Retain SP-01's failed null-selection gate and SP-02's observed result separately. The next useful preparation is an independently annotated free-form evidence-selection corpus with realistic conflicting updates, ambiguous/unsupported statements and strong parser/retrieval baselines. Verify normalization coverage and source-identity assumptions offline before a broader native claim. More aliases of these five grammars would not address that gap.
