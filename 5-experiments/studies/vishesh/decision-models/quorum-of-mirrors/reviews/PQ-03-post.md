# PQ-03: fixed schema runs successfully and passes the bounded qualification

**All 24 calls completed without HTTP or schema errors, and the predeclared qualification conjunction passed.** All 24 source-majority decisions and exact report-classification vectors were correct. Source facts:72/72 correct. Report facts:119/120 correct. Relevant literal quotation checks:24/24. The one extraction miss did not affect the final classification; retain it as a real component error. [Frozen plan](https://github.com/dmarzzz/swarm-lab/blob/ba2a74afaf34a36b39474d1062ab6fea14b28077/researchers/vishesh/notes/decision-models/quorum-of-mirrors/packet-study/native-v3/PLAN.md), [summary](../results/QM-PQ-03/summary.json), [full audit](../results/QM-PQ-03/audit.json), [all-case trace view](../results/QM-PQ-03/traces.html).

## What the fix establishes

The output schema now has two arrays of fact objects rather than a different object definition for each source/report ID. IDs are validated locally for exact coverage, with duplicates, missing IDs and unknown IDs rejected. Schema bytes are identical across case IDs and report counts; nullable definitions fall from seven/nine to two. Maximum conservative request token bound fell from7330 to4741. Safe HTTP diagnostics are integrated and tested with synthetic error fixtures, retaining fixed categories and bounded-body digests without arbitrary provider text or reflected secrets.

The first assignment used three copies, exercising the packet size that failed in PQ-02. All 24 requests succeeded; no retry or fallback occurred. This demonstrates that the revised interface worked in this run. It does not prove schema complexity caused the original HTTP400: its error body is unavailable and this was not a randomized matched transport comparison. No new HTTP failure occurred, so the new error handler has offline fault-test evidence, not a live-error demonstration.

## Accuracy and the remaining extraction error

Across120 dependent report occurrences:48 supported,48 contradicted and24 not established were classified correctly, with no false accusations, missed contradictions or unknown-classification errors. All12 paired roots preserved classifications and decisions between one and three contradiction copies. Pair invariance concerns these derived outputs, not perfect invariance of intermediate extracted facts.

The single report-fact error occurred in QM-PQ-03-020, the one-copy plans/observations case. A source contained only a plan to run. Its bound report nevertheless asserted that the device was stopped. The report extractor returned null/unknown instead of extracting the report's asserted value0/observed. It did correctly quote the report verbatim. The source extractor correctly returned unknown. Consequently deterministic comparison still returned NOT_ESTABLISHED, the correct label.

This localizes the observable mismatch to the report's value/status extraction. It is consistent with conflating what a report asserts with what its source establishes, but hidden reasoning is not known. The matching three-copy variant extracted the report correctly. A correct final label therefore masked one incorrect intermediate representation. The frozen gates did not require perfect report-fact extraction; keep the pass and this limitation separately. Quote validity here means literal text containing the gold evidence span, not proof that the model's associated fact is correct.

Practical consequence: the interface is qualified for its declared synthetic decision/classification screen, while raw extracted report facts are not error-free. A useful offline refinement would distinguish report assertion status from source evidence status, or deterministically assign the declared observation-claim type to reports. That is a prospective refinement, not a post-hoc rewrite or a reason to launch another paid run automatically.

## Review against the run-quality rubric

| Dimension | Evidence and boundary |
|---|---|
| Question/usefulness | Clear engineering check: can semantic extraction plus exact comparison avoid unwarranted accusations and request failures? It passed this bounded screen. |
| Scenarios | Twelve fresh authored roots across six known grammar mechanisms, each with two copy counts; equivalents, real contradictions and missing evidence included. No natural-field language claim. |
| Controls | Strong same-input deterministic parser solves the fixtures. Source evidence fixed within pairs. Schema now fixed; repetition still changes input/output length. No randomized old-prompt arm. |
| Capability | All predeclared gates passed;72/72 source facts and119/120 report facts. One real component error is preserved, not concealed by24/24 correct derived outcomes. |
| Measurement | Saved raw JSON independently re-parsed and scores recomputed; confusion, source/report facts, quotes and decisions separate. Same-author audit, not independent validation. |
| Sample/precision | Twelve paired authored roots within six reused mechanisms;24 calls and120 report occurrences are not independent world samples. Feasibility/defect-screen evidence only. |
| Agent context | Frozen stateless source-first Sonnet4.6, Anthropic-only route, temperature0; actor-only payload, no gold or operator memory. |
| Data integrity |24 assigned/started/terminal/valid/accounted,0 missing/unstarted. Request/response/accounting/generation IDs retained. All24 automatically replayed; sole extraction miss manually inspected in full. |
| Resources | Original ledger migrated byte-identically with previous path fenced; previous unknown costs retained; no repeated budget extension. All costs below cumulative authority. |
| Reproducibility | Immutable plan and request/source hashes, seven remote artifacts hash-verified locally, hub done independently read back. Hosted outputs are not guaranteed reproducible. |
| Visualization | All24 actual cases in expandable HTML, correct counts and missingness handling structurally verified; static display appropriate for stateless calls. No separate visual browser QA claimed. |

Case readiness, native qualification, scientific inference and future-run admission remain distinct. Researcher review was waived by the owner, not fabricated. All24 PQ-03 cases are released in the public audit after analysis and must be treated as development material for future tuning. The old96-packet evaluation corpus remains unchanged, unopened and incompatible with the revised interface pending deliberate redesign.

## Cost and closeout

New actual API cost: **USD0.243624**. Cumulative ledger:99calls,USD2.345856 retained reservations,USD0.39973896 known actual plusUSD0.061344 prior unknown upper bounds; combined known-plus-unknown exposureUSD0.46108296. API cap remainsUSD3, infrastructureUSD1, totalUSD4. The owner's earlierUSD2 addition exists exactly once. Remaining API reservation authorityUSD0.654144; no reservation refund or allowance reset. [Reconciliation](../results/QM-PQ-03/closeout.json).

The original75call ledger was moved byte-identically to the exclusively claimed approved-account resource because its previous host was occupied. The former canonical path was fenced before enabling the new one. [Migration](../results/QM-PQ-03/ledger-migration.json). Claim365 preceded deployment, live admission passed, worker exit and all seven artifacts were verified, and release is recorded in [release.json](../results/QM-PQ-03/release.json). [Hub readback](../results/QM-PQ-03/hub-readback.json) verified done. No evaluation, fallback, automatic retry or successor remains.

**FINISH this repair qualification.** The HTTP problem did not recur, and the declared narrow baseline is stronger than the incomplete PQ-02 evidence. Preserve PQ-01's failed fidelity result and PQ-02's provider failure. No causal improvement, field generalization or swarm-efficacy claim follows from these different cohorts. Future scientific evaluation requires a concrete compatible design; a pass does not automatically launch the old evaluation.
