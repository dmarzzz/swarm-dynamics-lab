# Response to engineering review 273e35ed

2026-10-04 UTC. Repair implementation follows q1-repair-plan.md. Thirty-one offline tests pass. No paid calls, credentials, fleet allocations or scientific observations were used for these repairs. Formal review remains open for dmarz; this response is an author statement awaiting re-review.

## E1 — failure classification and stopping

New failures.py defines a fixed public error vocabulary. Provider child sends only allowlisted categories or a numeric HTTP status; no body, URL, header or exception text is returned. Missing usage retains reservations. Stage and episode budget exhaustion are distinct. Engine preserves safe codes, never repairs a provider failure as a malformed plan, stops integration on fatal worker faults, and exposes fatal status to the batch. Route/configuration/credential/billing faults and stage exhaustion stop further batch admission. Already in-flight requests remain charged/held; no remote cancellation guarantee is claimed. Tests cover six distinct failure codes, one-dispatch fatal stopping, HTTP 429/timeout/credential child boundaries and secret-text exclusion.

## E2 — reporting separation and receipts

The inspected shared client contract is report(): boolean acknowledged; False can mean spooled. upload(): acknowledgment dictionary, with spooled=True denoting deferred delivery. Its upload retry timeout can reach 600 seconds per try, so the wrapper now isolates every operation in a spawn child, bounded by a 30-second parent wait plus a 2-second termination join. It uses sr.report and sr.upload directly; no periodic background heartbeat is claimed. Q-A's 600-second episode bound is below the hub's 20-minute stale-worker interval.

Initial start acknowledgment and public TLDR validation remain fail-closed. During execution, at most one asynchronous progress update is in flight; further progress is coalesced. Failed progress produces a safe reporting event and cannot replace the model outcome. The model wall-time record excludes the final wait for that reporting future. Final outcome is durably written before replay/upload. publication.json retains per-file acknowledgment/spooled/timeout state and terminal acknowledgment; queued or unknown sends are not successful publication. Missing/failed publication stops the next episode. Unknown-delivery files stay locally available for explicit reconciliation; no automatic paid rerun or unlimited upload retry is added.

Regression mocks show throwing progress no longer stops after item one, failed upload preserves a terminal local outcome and reports incomplete publication, and false/spooled acknowledgments are persisted. The new process wrapper still needs a separately preregistered synthetic end-to-end host check. Previous registration-only evidence is not relabeled as validation of this new wrapper.

## E3 — full denominator and partial completion

All 16 assignment records are created before admission. A finally reconciler writes reconciliation.json plus per-episode state.json with execution status, reason, exposure, outcome presence and publication status. Admission-failed, interrupted, not-started and terminal states stay separate. Unstarted episodes receive no fabricated quality score. Terminal model outcomes survive reporting failure. Output explicitly reports partial completion and a nonzero exit. Fault tests cover admission failure, fatal transport and incomplete upload; each preserves the 16-row denominator and stops additional paid admission.

## Still closed

The approved model credential, route qualification and non-vishesh package approval remain missing. This repair does not open Q-B or change its chain-edge issue. Obtain a pinned re-review, run the synthetic reporting diagnostic under a current exclusive allocation and public plan, then freeze amended source/config and refresh the model-run registration before any paid request. The $20 total shared cap and canonical-ledger requirement are unchanged.
