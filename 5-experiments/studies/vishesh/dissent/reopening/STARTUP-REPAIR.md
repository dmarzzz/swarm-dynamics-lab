# RD6 startup repair proposal

Written prospectively on 2026-10-04 after Q0-A1 stopped with zero model requests. This is an execution repair for the existing scientific design, not a result or permission to retry. [The post-mortem](reviews/Q0-A1-POST.md) preserves the unsuccessful attempt.

## Observed defect and uncertainty

The deployed worker uses `mkdir(exist_ok=False)` for a nested output path whose parent did not exist. That error was reproduced on the allocated host before provider access. The original worker stderr was discarded; a concurrent admission-file restaging race remains an alternative explanation. We can verify the directory defect, but cannot establish it was the sole cause of the historical exit.

## Proposed execution changes

1. Create missing output parents while refusing to reuse an existing attempt directory. Record startup phases and a fixed, safe failure category; never log arbitrary exception strings, authentication details or provider bodies.
2. Bind the worker to the exact local admission-file digest supplied by its supervisor. Verify the remote receipt and all referenced evidence in a separate no-provider startup check before the local relay starts. Stage admission evidence in a unique directory, references first and admission last; never overwrite an admitted receipt. Retain a startup-check acknowledgment.
3. Preserve Q0-A1's stopped stage row. A separately authorized Q0-A2 may use one append-only replacement record only if the original authoritative ledger still contains **zero RD6 reservations of any status**, the previous attempt is stopped, its actual latest operational closeout and completed owning review match, and the updated owner decision explicitly names the predecessor and replacement. Any started, invalid, failed, completed or ambiguous model call blocks replacement. No second replacement, D0 replacement, automatic retry or journal reset is supported.
4. Keep the actual Q0-A1 operational handoff as the latest predecessor and RD5 H5-A1 as the scientific ancestor. Never substitute one for the other. A new packet/source revision and immutable public amendment are required; stale receipts fail closed.

## Scientific scope and resources

All 162 actor requests, labels, criteria order and the fixture manifest remain unchanged. Q0-A2 would contain the original 18 qualification requests; only an 18/18 valid-and-correct result plus owning postreview permits the original 144-request D0. The independent units remain 12 authored cases nested within six shared families, with no population precision claim or untouched holdout. Existing controls, all-assigned scoring, missingness bounds, first-failure stop and 60-second request/30-minute stage limits remain unchanged. A1 contributes no model sample.

The lifetime ceiling remains 650 calls, with at most 162 RD6 calls and the original USD1 API/USD1 infrastructure caps. Preserve the original 488 calls, USD0.022699069 committed API and all historical reservations. Released allocations consumed 1,357 seconds at the USD0.07143/hour ceiling, an estimated USD0.026925142, bringing estimated cumulative infrastructure to USD0.747173584. These are allocation estimates, not invoices.

The proposed replacement must still end by **2026-10-04 20:40:02 UTC**, the original allocation-window stop. Reserve the new exclusively claimed interval at its verified rate, carry the released costs forward, and keep committed plus reserved infrastructure at or below the original proposed USD0.827393442 maximum. At most USD0.080219858 remains within that infrastructure envelope; unused dollars do not extend time. Require 31 minutes remaining at each stage admission. No allocation is currently held, and this proposal does not itself authorize reclaiming one. A later window or larger resource envelope needs a separately updated decision.

## Offline acceptance checks

The repaired worker must complete synthetic Q0 from a missing nested parent; a reused output path must fail before a transport call. A startup admission failure must retain only safe diagnostics and make no provider or ledger access. Remote receipt or evidence changes must fail before relay creation. Fake supervisor failures must retain the failing phase and clean up owned children. The append-only replacement tests must preserve the old row, permit only an explicitly bound zero-dispatch Q0 successor, reject every nonzero/ambiguous case and reject duplicate replacement. All existing scenario, scoring, budget, admission, qualification and replay tests must continue to pass. The 162-request manifest must remain byte-identical.

## Decision required before another attempt

Complete and publish the repair and its offline evidence first. The owner must approve this concrete replacement execution contract before another allocation or launch; the earlier no-retry scope does not silently become permission to clear a stage fence. Researcher review remains not required. If the replacement is not approved or its live gates cannot be satisfied, finish with Q0-A1 blocked and retain the prepared repair without collecting data.
