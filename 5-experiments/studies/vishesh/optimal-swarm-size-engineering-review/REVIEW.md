# Optimal swarm size: bounded engineering review

**Verdict: REVISE before the planned paid Q-A batch.** The offline evaluator and reservation tests pass, but failure classification and reporting/reconciliation need repairs so the first paid screen can distinguish model capability from infrastructure failure. These findings do not prohibit a separately planned, minimal transport diagnostic within the same authorized cap after its prerequisites are met.

Reviewer: vishesh/codex-independent-reviews, 2026-10-04 UTC. Direct user approval was obtained in this task after the initial delegated request was rejected by automatic approval review. This is a same-researcher engineering review, **not formal cross-researcher approval**. The formal task `review-swarm-size-qualification` remains open and is currently directed to dmarz, superseding older references to Shadow. No author implementation, other researcher's files, or task claims were changed.

Reviewed checkout: `ae7563d0d88cecfb19a05b5b029cd83ed1800356`. [Exact file hashes](source-receipt.json) define the review. Source remained unchanged during diagnostics. [Prospective plan](PLAN.md) was published and publicly verified before execution; [registration](registration.json) records its immutable URL and hash. No model calls, secrets, fleet operations, fit/validation/transfer roots, or spending were involved.

## Evidence

All **23 existing unit tests passed** in this clone. [Log](unit-tests.log). Coverage includes all five rosters under scripted responses, reference task variations, adversarial JSON/AST inputs, concurrent reservations, shared cap persistence, overrun refusal, replay escaping, and public TLDR refusal. These are software tests, not real transport or model competence evidence.

[Reviewer checks](checks.py), [results](checks.json) and [log](checks.log) establish:

- Evidence-chain root 0 was recomputed from public records and declared dependencies without reading evaluator truth: first value 13, last value 27004. Its answer passes; changing the first value fails.
- For parallel and chain repository root 0, correcting the visible subtraction defect to addition passes, while the original buggy files fail. Submitted code is parsed into a restricted AST and interpreted; it is not executed as arbitrary Python.
- Four distinct failures become the identical terminal `RuntimeError`.
- A mocked progress exception causes all 16 offline assignments to terminate after the first work item, with infrastructure failure indistinguishable from other runtime errors.
- A mocked registration failure leaves the full 16-row assigned manifest, one per-episode assignment and zero outcomes. The denominator is recoverable, but no reconciliation classifies the unstarted remainder.
- Mocked false returns from all four artifact uploads and the terminal update are ignored by `finish()`.
- A plan deleting every public chain edge is accepted by `validate_plan`.

The failure checks are injected offline behavior, not claims that the installed hub client necessarily throws or returns false in those exact circumstances. Its host-specific contract and live transport remain unverified by this reviewer.

## Repairs before the Q-A batch

### E1 — Preserve safe failure categories and stop on fatal transport configuration errors

`src/provider.py:35–36` reduces child failures to exception class; line 68 discards even that class. `src/engine.py` catches every call exception and replaces it with `RuntimeError("transport_failed")`; the terminal record retains only its class. The existing `test_provider_error_preserved` confirms the generic class, not preservation of a useful reason. Budget exhaustion, a served-route mismatch, deadline expiry and unavailable credential are therefore indistinguishable in terminal outcomes. Route mismatch does leave match flags in the charge journal, but it does not stop the batch; later episodes may repeatedly make requests against the same bad route.

Minimal repair: define an allowlisted, non-secret failure code propagated child → provider → engine → outcome/trace. Record safe numeric HTTP status separately from bodies, URLs or headers. Keep exact actual/held cost treatment. Credential/configuration failures, route mismatches and stage exhaustion should stop further batch admission and reconcile the remaining assignments as not started. Worker-specific recoverable failures can remain within the frozen protocol; do not add transport retries implicitly. Acceptance: inject timeout, rate limit, missing usage, route change, missing credential and cap exhaustion; assert distinct safe codes and no additional dispatch after a fatal error. Retain unknown billing reservations.

### E2 — Make reporting outcomes explicit and prevent reporting faults from masquerading as model failures

`src/reporting.py` verifies the initial public TLDR, which is good, but `progress()` and `finish()` do not validate delivery results. The reviewer mock shows `finish()` returning normally after four failed uploads and a failed terminal update. A raising progress call occurs synchronously inside the engine's work-completion callback; it aborts the model episode and records a generic runtime failure. Thus telemetry can invalidate qualification without an identifiable reporting cause, or evidence publication can silently remain incomplete.

Minimal repair: document the installed client's exact success/failure contract; check artifact and final-status acknowledgments, retain a durable upload receipt/outbox, and surface publication failure. Keep initial public registration fail-closed. After admission, handle progress failure as an explicit reporting event rather than an unclassified actor failure: either spool bounded updates without interrupting the task, or stop safely with a reporting-specific status under a predeclared policy. Bound reporting waits. Acceptance: false and throwing client mocks preserve local outcomes and costs, flag incomplete publication, and never claim successful publication from unacknowledged sends. Verify one synthetic per-run end-to-end publication on the selected host before model dispatch.

### E3 — Reconcile every assignment on every batch exit

`src/run_qualification.py:90` constructs Reporter outside an episode exception/reconciliation boundary; rendering and uploading at lines 106–107 can also stop the batch. `assigned.json` preserves the correct denominator, but no final reconciliation marks remaining episodes not started, terminal or missing. An overrun breaks the loop and still prints “Q-A terminal.” Local completed outcomes survive upload failures, so this is a status/recovery gap rather than proof of lost completed data.

Minimal repair: add a batch-finally reconciler against the immutable 16-row manifest. Persist per-episode execution state, reason, known exposure, missingness and publication state; classify unstarted assignments without assigning them fabricated model scores. An early stop must report partial completion. Keep raw attempts and the canonical ledger; never rerun under a fresh ledger to replenish funds. Acceptance: initial public-preflight failure, mid-batch fatal error and upload failure each yield a complete 16-row reconciliation, with completed outcomes untouched and no unapproved retry.

## What is adequate, and what remains conditional

SQLite `BEGIN IMMEDIATE` makes concurrent reserve/settle operations atomic; stage and episode caps cannot be raised merely by reopening the same database. Unknown calls retain their maximum exposure, and an overrun blocks further reservation. The supplied prices produce an upward-rounded reservation of **425,584 microdollars per call**. This is conservative under the configured token and rate assumptions, not an independently verified provider billing guarantee. No live pricing or account evidence was checked. One canonical ledger on one exclusively claimed host remains essential; arbitrary new database paths are not a global account cap. A timeout terminates the local child, not necessarily remote inference, so retaining the reservation is appropriate.

The served route is compared after charging, fallback is disabled in the request, output length is bounded, and actor inputs come only from public tasks plus their histories/artifacts. Missing or malformed cost data cannot silently release the reservation. Review did not exercise process spawning, real network cancellation, provider usage schema or enforced price ceilings. Those need transport qualification before treating the dollar bound as established in practice.

The evaluator rejects malformed artifacts, extra fields, duplicate citations/JSON keys and forbidden Python syntax. Repository correctness is checked on public inputs plus 12 hidden integers; describe this as test-based qualification, not a proof of behavior for every input or a general software-repair benchmark. Current arithmetic fixtures and restricted grammar are suitable for a small competence screen, subject to the above execution repairs.

Q-A is explicitly N=1 across 16 synthetic assignments and does not establish an optimal swarm size. Q-B is not implemented by this entry point and requires its own frozen calibration assessment. Core/transfer and formal scientific claims remain gated. The author setup post-mortem reports synthetic browser replay validation, public experiment registration and released machine allocation; these are read as author evidence, not repeated here. Our text assertions have no meaningful agent trajectory requiring a replay.

## Before Q-B or a size-effect interpretation

`validate_plan` enforces an acyclic graph over known items but does not require public task prerequisites. An empty-edge plan is legal for a public chain. Because every actor already sees the entire task, a worker can recompute its own prerequisite values. This can be an intentionally flexible model-planning protocol, but then the chain/parallel label does not guarantee the claimed scheduling bottleneck. It does not block an N=1 competence screen by itself. Before Q-B, either enforce required prerequisite edges (extra legal planning dependencies may be allowed) or explicitly measure plan deviations and narrow the structural claim. Do not treat a public chain label alone as evidence that serialized scheduling occurred.

## S0 eligibility and launch checklist

Engineering review does not fill `independent_review_commit`. The current checked-in configuration correctly refuses readiness. Before paid Q-A: repair E1–E3; obtain the required non-vishesh package verdict; resolve authorized credential availability privately; pin and qualify the served route and rate/usage contract; reacquire a current exclusive machine allocation; freeze source/config and refresh immutable public registration and each run TLDR; verify the canonical shared $20 ledger and live reporting. Existing setup success at source `1002752` cannot stand in for verification of amended source. No external state or provider route was changed here.

A valid poor model result should be retained as qualification evidence. Infrastructure errors must first be identifiable and reconciled; they must not be reinterpreted as lack of model competence or silently replaced. After repairs, re-run these counterexamples plus the affected existing tests and publish a source-pinned amendment before claiming launch readiness.
