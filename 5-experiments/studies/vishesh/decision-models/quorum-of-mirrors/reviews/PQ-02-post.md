# PQ-02 post-mortem: provider rejection interrupted semantic qualification

**Execution stopped; semantic qualification is inconclusive and did not pass.** The owner-approved fact-extraction repair was implemented, tested, published and launched. Of24 assigned calls,2 started: the first returned a fully correct valid answer; the second returned HTTP400 after0.70seconds;22 were not started. No retries or evaluation. [Frozen plan](https://github.com/dmarzzz/swarm-lab/blob/f091bc486efea93f8a7c43340181ee82f77cde1c/researchers/vishesh/notes/decision-models/quorum-of-mirrors/packet-study/native-v2/PLAN.md), [summary](../results/QM-PQ-02/summary.json), [all24 assigned trace view](../results/QM-PQ-02/traces.html), [machine-readable audit](../results/QM-PQ-02/audit.json).

## What changed and what we observed

The instrument now asks for source/report facts (entity, time, property, exact value, observation status and supporting quote). Deterministic code compares values and returns SUPPORTED, CONTRADICTED or NOT_ESTABLISHED, and computes the source-majority decision. Different quantities remain different even on the same side of a decision threshold. Offline tests correctly resolve all18 previous false flags, unit equivalences, missing evidence and same-threshold numeric contradictions. A same-input grammar parser solves24 development and24 fresh qualification fixtures; that is software evidence, not model superiority.

The one valid native response was a time-disambiguation case with one contradictory report copy. It returned all3 source facts and4 report facts correctly, all4 classifications correctly (two supported, one contradicted, one unestablished), relevant literal quotations and the correct ZERO decision. The trace was inspected in full and grades replayed. This is1 root/1 condition, not the planned12 paired roots. No complete pair exists, so no copy-invariance or family-wide estimate can be reported. Assigned-denominator exact packet success is1/24; observed valid-response success is1/1. Neither establishes accuracy in the intended qualification cohort.

## Failure and diagnostic limits

The second request was a polarity case with three copies and six report facts. The HTTP response code is retained; its error body was not. That loss is a runtime diagnostic defect. There is no returned answer, generation ID or usage receipt for the rejected call. Do not score it as a wrong semantic answer or claim zero charge.

A schema-compilation limit is plausible because the successful request contains seven nullable fact objects and the rejected request nine. Both are below the documented16-union count, but Anthropic also describes internal combined-grammar limits that can produce HTTP400. [Official structured-output documentation](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#schema-complexity-limits). This is a hypothesis, not a verified cause: other provider request errors remain possible. Offline schema validation does not reproduce the provider compiler.

The prospective [offline diagnostic repair](../packet-study/transport-repair/PLAN.md) adds bounded error-body classification into fixed safe categories plus HTTP code, byte count and digest. Four tests verify classification and that arbitrary messages/reflected secrets are not emitted. A patch against the frozen runner passes dry-run application; it is prepared, not retroactively installed or paid-tested. The missing historical body cannot be recovered by this patch. A future wire-format repair should use constant-size arrays of facts and strict local ID validation to avoid repetition also growing the schema; it must be separately frozen and admitted, preserving this stopped attempt.

## Assessment against run quality

| Dimension | Assessment |
|---|---|
| Question | Clear narrow check of false accusations and exact semantic extraction; not a swarm-efficacy study |
| Scenarios | Offline ready for authored grammar: six mechanisms,12 roots,24 paired packets; only1 root actually yielded a response |
| Controls | Strong parser preserved; source evidence fixed across copy pairs; repetition changes length and, undesirably, response-schema size |
| Capability | Unestablished:1 fully correct response cannot satisfy the24-call gate |
| Measurement | Separate extraction, comparison, unknowns and final decision; all saved scores replay; missing outcomes explicit |
| Sample size | Planned12 roots; observed1 valid root and1 provider failure from another; no completed pairs, no useful precision |
| Agent context | Frozen source-first stateless actor context, Anthropic-only Sonnet4.6 route; no evaluator or operator memory |
| Data integrity |24 assignments,2 dispatch intents,1 raw answer,1 accounting receipt,2 terminal receipts,22 unstarted; HTTP-body trace gap disclosed |
| Resources | Original ledger retained and migrated with old path fenced; new ownerUSD2 recorded separately; no allowance reset |
| Reproducibility | Seven remote artifacts downloaded/hash-verified; both dispatch request hashes and all scores replayed; underlying HTTP reason unavailable |
| Visualization | All24 assigned cases in expandable saved-data HTML;22 explicitly not started; no fake temporal behavior or hidden reasoning |

## Cost, allocation and process

[Reconciliation](../results/QM-PQ-02/closeout.json): cumulative75calls / USD0.905856 retained reservations; USD0.15611496 known actual. This attempt's known actual isUSD0.012552. Retain the fullUSD0.06 uncertain failed-request reservation plus historicalUSD0.001344 unknown upper bound. Known plus both unknown bounds isUSD0.21745896. API authority is nowUSD3; infrastructure remainsUSD1 (USD4 total), with the original six-hour time cap. Remaining reservation authority isUSD2.094144; this is not automatic retry authority.

Approved account and original resource inventory were verified. Because the original host was claimed elsewhere, the original73call ledger was transferred byte-identically to the new exclusively claimed host, with the prior SQLite path fenced as a directory before transfer. No duplicate spend authority exists; the local transfer copy is archival only. [Migration record](../results/QM-PQ-02/ledger-migration.json). Claim360 was merged before deployment; immutable public plan registration, live prices, exact source/request hashes and ledger history passed preflight. Worker exit verified and release361 merged. Seven run artifacts verified locally; public GitHub readback is checked after push. Hub status is not independently read back here, and no dashboard verification is claimed.

## Disposition

**FINISH the stopped attempt; HOLD native qualification/evaluation.** Researcher review remains waived. The owner requested fixes and a cheap follow-up; that follow-up was launched and obeyed its no-retry stop. It did not establish a stronger native baseline. Keep the useful semantic repair and all negative history. Next technical work is the prepared safe-error integration plus constant-size response schema, preserving fact semantics and testing exact ID coverage, then a newly registered bounded diagnostic before any qualification resumption. Do not automatically spend the remaining budget or reclassify the failed transport as model incapacity.
