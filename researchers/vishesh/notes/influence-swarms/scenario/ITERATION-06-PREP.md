# D6 preparation: stop and explain an acquisition failure

Prospective repair plan, 2026-10-04; written before the D6 implementation. **Offline preparation only. No allocation or paid attempt is approved by this document.** The failed D5 remains unchanged. Its post-mortem and all48 reservations persist.

## Decision and bounded next proposal

D5's24 reviewer requests all failed before a response; logging lost the safe HTTP codes and repeated retries consumed USD1.690512 of reservation. Build a transport journal that identifies the first failure without exposing credentials or raw error bodies, stops immediately, and retains unstarted assignments distinctly. An acquisition success is not successful reasoning.

Propose at most **two sequential acquisition requests**, the matrix and typed reviewer contracts from the first frozen D5 development case, both with original primary records/context and pinned model/caps. No chair, no new scenario, no fresh scientific sample, no architecture-effect estimate. These are two contract checks within one known case, not independent behavioral observations. The decision is whether each exact wire contract returns a parseable, contract-valid response with complete usage under the already authorized route. No intervention or task truth is changed. Expected outcomes: both succeed → review scope for later behavioral collection; first HTTP/transport/output/usage failure → stop and use retained diagnostics; no automatic cohort.

Reuse D5's32768-byte input envelope plus512 accounting bytes,3072 output tokens, pinned Haiku snapshot and verified USD1/M input plus5/M output assumption. Reverify pricing before any future dispatch. Maximum reservation USD0.097280 for two attempts, **zero retries**, within the existing USD3.131168 remainder. Original USD8 cap, USD4.868832 cumulative reservation and48 uncertain charges remain. No new ledger or stage allowance. One freshly admitted dedicated existing allocation suffices only after owner approval; no allocation now. Expected preparation20–40minutes, native dispatch under3minutes, review10–20minutes. Do not substitute another provider/model/account without corresponding decision.

## Offline repair acceptance checks

1. Before each physical transport, reserve conservative cost in the original existing ledger transaction; persist one attempt-start event and durable in-flight state. Never create a missing ledger. Enforce two attempts and per-request cap; refuse a second session on a used journal.
2. Retain allowlisted numeric HTTP status, retry decision(alwaysfalse), bounded numeric Retry-After, request ID if format-safe, exception category and usage-knownness. Never retain authorization/request headers, raw provider errors, key material, or freeform exception text. Error bodies are not read.
3. Any HTTP, timeout, transport, parse, contract-validation or missing-usage failure opens a durable circuit immediately. Remaining assignments stay unstarted. An interrupted in-flight journal cannot resume without an explicit later recovery decision; reopening a journal never clears state.
4. Preserve parseable response and validated token counts only on success; distinguish reported subtotal from known actual cost. Missing usage remains unknown, never zero. Preserve raw response only within native experimental artifacts, not diagnostic error logs.
5. Fault fixtures cover429/502/503/504, nontransient401, timeout, malformed content, missingusage, negativeusage, unsafe diagnostic headers, successful two-contract completion, journal reopen, ledger shortage and reservation-before-send. No network or secrets in tests.

## Limits and integration

The versioned D6 acquisition helper is separate from frozen D5 source and is not retrofitted into historical traces. Wire construction and exact contract validators must be bound to the future frozen packet during preparation; the helper accepts a validator callback and tested transport. No unvalidated response qualifies. Before a next-run decision, provide the resolved two-request packet, immutable public plan registration, runtime/credential-free probe qualification, exact ledger/host admission and source bindings. Native qualification remains unassessed. This proposal is not a backdoor to rerunning D5 within a smaller nominal budget.


## Implemented offline outcome

`analysis/acquisition_d6.py` now implements the bounded session, original-ledger reservation, durable in-flight/terminal journal, safe error allowlist and first-failure circuit breaker. It has no CLI, provider transport or credential lookup; only a later admitted launcher can supply those. `tests/test_acquisition_d6.py` exercises all listed failures with injected transports;70 scenario tests pass including8 new acquisition tests and3 D5 audit tests. The concrete two-contract request packet is in `reviews/D6-acquisition-packet.json` (wire19288 and25957bytes); no model calls were made. An initial test pass exposed SQLite connection warnings, repaired using explicit close contexts before the final clean pass. These facts qualify the offline primitive, not the model endpoint.

### Prospective trace-preservation addendum before repair

Offline review found that the initial D6 helper would lose a successful-HTTP response when parsing, usage or contract validation failed. Before changing it, extend the contract: save exact request bytes/hash before transport and exact bounded (≤1MB) response bytes/hash before parsing or validation, in the private0700 session with0600 artifact files. Never save HTTP error bodies or request/authentication headers. Numeric diagnostics reference artifact names/hashes, not body text. Artifact writer failures close the circuit; do not dispatch further requests. Add fixtures proving malformed/invalid-usage/rejected-contract responses survive, unstarted assignments have no invented body, and write failure forbids further transport. No live calls.
