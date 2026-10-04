# Post-mortem: request-contract rejection, then blocked paid fallback

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by shadow/sol-factory; source `76f42cdd` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — No model answer or treatment contrast observed; two qualification requests refused. Basis: Pool HTTP400 with unsupported wire-schema bounds identified; paid fallback HTTP403. All main cells unstarted. Same-author recomputation does not establish model competence or independent review.
- **sample_size_summary:** Observed:2 HTTP attempts,0 valid answers,0 complete paired roots. Planned:12 synthetic numeric roots with12 main calls/root; six qualification calls/route.300 potential conditional assignments are fully enumerated; max151 actual HTTP requests across routes. Calls/copies are not independent worlds.
<!-- experiment-evidence:end -->

**Scientific status: unqualified, no treatment evidence.** This is the first-priority provenance diagnostic, not another scope. Two HTTP requests were made, one per route. No model answer was received. Both routes stopped at their first clean qualification item. Do not describe this as a negative duplication result, a competence failure, or confirmation that the pool still has the earlier429/503 outage.

## Exact outcomes

- Pool: first qualification request returned **HTTP400**, not429/503. One failed attempted assignment;149 not run, including all144 main cells.
- OpenRouter: the predeclared initial-provider-failure fallback returned **HTTP403** on its first qualification request. One failed attempted assignment;149 not run, including all144 main cells. The shared key had already exhausted its lower daily quota in the previous factory lineage; this new403 is consistent with that blocker, but its response body was not retained and the exact new403 reason is not independently established.
- Total: **2 HTTP attempts,0 valid answers,0 main observations,0 complete paired task roots**. The300 terminal files cover both conditional150-assignment route plans, not300 attempted calls or24 independent worlds. The scientific target remains the same12 roots.
- Paid liability: **USD0.044376**, conservatively unresolved. No charge is established from the refusal alone. Existing factory liability rose fromUSD1.806969 toUSD1.851345, including earlier unresolved reservations. No limit or credential changed.
- Saved-data recomputation: **2,026 checks pass**, using a separate standard-library implementation with no runner/generator/scorer imports. Same author; not an independent researcher review. Independently reviewed complete contrasts/hour remains **0**. No scaling.

## Failure diagnosis and ownership

The pool request contains a concrete implementation defect: the wire JSON schema for confidence sends `minimum:0` and `maximum:1`. Anthropic's [structured-output documentation](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), opened after the failure on2026-10-04, explicitly describes those constraints as unsupported on the wire: SDK helpers remove them and validate them locally. This runner constructed raw requests without that transformation. The source and immutable init receipt show the unsupported fields.

That is a **confirmed request/schema incompatibility and a likely cause of HTTP400**, not a confirmed server diagnostic: the generic error handler retained the HTTP status but not an allowlisted provider error code/message. We cannot recover the exact reason from the saved HTTP record alone. Do not blame model capability, burst limits or a scientific treatment. The builder owns the missed schema-compatibility check. The eighteen mock-based tests verified gates and dataflow but did not check the provider's supported-schema subset.

The paid fallback was authorized by the frozen initial-failure rule, but switching providers cannot repair a malformed request schema. For a future revision, distinguish transport/availability failures from HTTP400 contract errors, repair the latter offline, and do not spend a paid fallback on a known local contract defect. That is a prospective operational-rule change, not a retrospective rewrite of this attempt.

## What worked and what did not

- Public plan and implementation were committed before requests, then raw/rendered public plan and hub registration were read back. Frozen assignment and admission files were pushed before dispatch.
- Two initialized request bodies, requested-model/config/context hashes, source identities and fresh-memory facts are preserved. Served model remains explicitly unknown for both refusals.
- Each request reserved before transport. No retries, no key rotation, no quota escalation. Unknown paid liability stayed in the original shared ledger.
- Numeric outcomes were create-once and written before reports. All conditional unstarted assignments remain visible. The same saved data reproduce counts, scoring contracts, missingness bounds and cost accounting.
- The real no-copy competence gate never obtained an answer. Model efficacy, ancestry benefit, false confidence and decision flips are all unmeasured.
- No temporal visualization is meaningful: there are no model trajectories. Use the error table and terminal-category counts; do not generate an empty effect chart that resembles a null result.

## Next decision, no automatic rerun

1. Independent agent recomputes/inspects the frozen raw package, exact request schema and2,026-check receipt. Completed scientific contrasts remain zero even if it confirms the diagnostic bookkeeping.
2. Prepare a small reviewed code repair: remove unsupported wire bounds while retaining strict local [0,1] checks; add an offline provider-schema test; retain an allowlisted diagnostic code for future errors. Do not alter this source revision, init receipt, failed rows or paid reservation.
3. Only after review, prepare a prospective **same-question** operational amendment with a fresh cohort ID/qualification stream, explicit remaining cumulative HTTP/dollar allowance and a rule for400 versus429/503. It cannot reuse/delete this admission to relaunch. The existing pilot's151-request ceiling is not silently reset or enlarged by naming a new cohort.
4. No other factory spec, no headcount sweep and no main batch before a clean gate. If the remaining route is unavailable or the next attempt is not admitted, stop with this diagnostic rather than hide it.

The source revision actually dispatched is `76f42cddddbffca75ddffb818415182b202e7e7f`; pre-dispatch assignment/admission publication is `72af5629`. Original plan remains unchanged. Current code source drift must fail closed if an offline repair is later merged.
