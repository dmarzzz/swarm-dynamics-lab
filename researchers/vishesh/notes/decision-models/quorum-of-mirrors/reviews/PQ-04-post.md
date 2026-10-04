# PQ-04: report assertions remain intact when source evidence disappears

**The targeted qualification passed all of its stricter checks.** Eight assigned calls all returned valid, accounted responses, with no transport errors or retries. Source facts24/24, report assertions32/32, exact classification vectors8/8, decisions8/8, literal quotations8/8 and quotations consistent with correct extracted facts8/8. [Frozen prospective plan](https://github.com/dmarzzz/swarm-lab/blob/7489e37ef377d7bf45428d5fdcadb7560bd72d8e/researchers/vishesh/notes/decision-models/quorum-of-mirrors/packet-study/native-v4/PLAN.md), [summary](../results/QM-PQ-04/summary.json), [full audit](../results/QM-PQ-04/audit.json), [paired trace explorer](../results/QM-PQ-04/traces.html).

## What the preceding traces changed

Replayed all24 PQ-03 request/score records and reviewed its sole intermediate extraction miss: a report asserting stopped was extracted as unknown because its bound source had only a plan. The final classification was still correct. The old quote checker also accepted the literal relevant sentence even though the extracted fact was wrong. Neither observation reveals hidden reasoning, but both identify observable contract/measurement gaps.

The implemented repair separates two questions: what does the report assert, and what does the authenticated source establish? Sources retain observed/unknown status and nullable values. Reports must provide their asserted value, entity, time, property and quote. Because all reports in this declared task assert definite observations, the internal claim type is assigned by code; it is not another learned field and does not assert that a report is true. Native extraction still supplies every claimed value. The new gate rejects wrong facts even if a correct final label or verbatim quote conceals them. Ten offline tests included exactly that masked-error counterexample, the prior native error, unsupported abstention, wrong source inference, ID faults and safe error diagnostics.

## What happened in the paired cases

Each pair retained identical reports and other sources. Only the focal source lost its observation and retained its plan; two remaining observed sources disagreed. All four pairs preserved exact report assertions and changed the source-majority decision appropriately:

| Authored root | With focal observation | With plan only | Report assertions preserved |
|---|---|---|---|
| Running, positive | ONE | DEFER | Yes |
| Running, negative | ZERO | DEFER | Yes |
| Mass above threshold | ONE | DEFER | Yes |
| Mass below threshold | ZERO | DEFER | Yes |

All32 report-occurrence classifications matched truth:8 supported,4 contradicted,20 not established. No false accusations, missed contradictions or unknown-classification mistakes. The numerical cases correctly distinguished3000g from4000g and6000g from7000g even though each pair lies on the same side of the decision threshold. Equivalent grams/kilograms and operating/running wording remained equivalent. Claims about an unseen entity stayed unestablished.

All8 actual source/report texts, returned facts and decisions were manually inspected; all request hashes, raw-response parsing and scores were replayed automatically. No component misses or missing outcomes were found. The frozen random order happened to place all four observation conditions before the four plan-only conditions. Calls were stateless and isolated, but this small sequence is not an independently counterbalanced replication or a test of provider-time effects.

## Practical interpretation and limits

This interface can retain a claim without endorsing it: removing support changes the evidence judgment, not what the report says. That is useful for evidence aggregation because an unsupported allegation should neither become an established fact nor disappear from the record. With insufficient independent observed votes, this controlled system abstained instead of inferring a result from a plan or repeated claims.

This is targeted engineering evidence on four authored paired roots. It is not population reliability, field utility, provenance authentication or evidence that a swarm helps. The same-input deterministic grammar parser solves all these cases too. The separate report schema eliminates a redundant ambiguous field by contract, so the result does not show the model learned a universal distinction between all kinds of assertions and uncertainty. Explicitly uncertain reports, multi-claim prose, unreliable source identities and natural field text remain outside this task. Final votes and classifications are deterministic outputs derived from native extracted facts, not direct model judgments. Preserve prior negative results and do not pool unlike cohorts to claim improvement.

## Scientific review

| Dimension | Assessment |
|---|---|
| Question | Clear targeted check of the previously masked assertion/evidence error |
| Scenarios | Pass for scoped defect screen: Boolean/mass, both directions, numeric contradictions, equivalent wording, missing evidence and DEFER; authored grammar limits realism |
| Controls | Reports/IDs/order and other sources fixed within pairs; focal evidence/content/length changes intentionally; strong parser retained; no causal old/new-prompt comparison |
| Capability | All stricter prospective gates passed; learned report-value fields distinguished from code-assigned claim type |
| Measurement | Exact component facts, separate quote checks, labels, decisions and paired invariance; wrong-but-correctly-classified fixture fails offline |
| Sample size | Four authored roots/eight dependent calls; no broad accuracy estimate or rare-error claim |
| Agent context | Same fixed Sonnet4.6 Anthropic-only route, stateless actor-only payload, no gold/operator memory, fixed schema |
| Data integrity |8 assigned/started/valid/accounted,0 missing; all traces inspected/replayed; no hidden reasoning requested or invented |
| Resources | Existing cumulative ledger/one extension preserved; both previous unknown bounds retained; no additional budget this turn |
| Reproducibility | Immutable plan/source/request hashes and original ledger digest checked before launch; seven downloaded artifacts hash-verified; hosted outputs not guaranteed deterministic |
| Visualization | Four paired outcome rows plus all8 expandable actual traces, structural counts and values verified; no browser visual QA claimed |

Case readiness is scoped; qualification passed; broad scientific efficacy remains untested. Researcher review was waived by owner direction, never represented as independent validation. All8 current qualification cases are released after analysis and must be development material in any future tuning. Old96-packet evaluation is still unused and not silently adapted.

## Process, costs and closeout

The first public-plan preflight returned a registration mismatch and correctly blocked dispatch. A follow-up read confirmed the exact immutable URL and content hash; preflight passed before any model call. No cost or assignment was consumed by those read-only checks. Current approved-account/resource identity, exclusive claim, clear workload, exact source/requests, original ledger digest and model/prices were verified. Original99call ledger was transferred byte-identically to the available exclusively allocated host with its old path fenced first. [Migration receipt](../results/QM-PQ-04/ledger-migration.json).

New API cost **USD0.074124**. Cumulative ledger:107calls,USD2.825856 retained reservations,USD0.47386296 known actual plusUSD0.061344 prior unknown upper bounds, total conservative known-plus-unknown exposureUSD0.53520696. No new uncertain charge. API capUSD3, infrastructureUSD1, unchanged totalUSD4; remaining API reservation authorityUSD0.174144. These reservations are not actual spend and have not been refunded or reset. [Reconciliation](../results/QM-PQ-04/closeout.json). Allocation cost/time is recorded separately in [release](../results/QM-PQ-04/release.json), not claimed as an invoice.

Worker exit and seven remote artifacts verified; [hub readback](../results/QM-PQ-04/hub-readback.json) confirms done. Claim379 released after verification. Standard offline finalize hook plus this authored assessment complete the attempt; no automatic successor or evaluation.

**FINISH this targeted repair iteration.** The previously observed assertion/evidence failure did not recur under the stricter matched cases. Use the separated interface and component-level gates for this grammar. The useful next scientific step would be an offline corpus of multi-claim/explicitly uncertain reports with independently defensible labels and a strong baseline, before proposing a broader paid evaluation. Repeating this solved fixture family would add little practical evidence.
