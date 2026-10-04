# Optimal swarm-size qualification review

Reviewer: dmarz/inbox-design-feedback, 2026-10-04 UTC. **PASS for the repaired offline Q-A package, with launch prerequisites still closed. Q-B/core are not approved.** This independent non-vishesh review checks the current E1–E3 repairs, not the stale 23-test version. Exact reviewed revision and hashes: [receipt](package-receipt.json). Independent [probe](check_swarm_size.py) and [results](swarm-size-checks.json).

## Evidence

All 31 author tests pass on Python 3.12 ([log](swarm-size-tests-py312.log)), including safe provider failure codes, stop-on-fatal behavior, throwing progress, failed uploads and all-16 reconciliation. The Mac's default Python 3.9 produced one error while closing a mocked HTTPError with no response body ([retained log](swarm-size-tests.log)); it is not evidence of a failed live HTTP response. Pin the intended 3.12 runtime and test it on the deployment host rather than claiming unspecified-python portability.

I independently reconstructed evidence answers from public records/rules, without `reference_answer`: opening 6, first value 6×1+7=13; final parallel value 15 and chain value 27,004. Both supported artifacts pass. Wrong values, omitted support, extra support and booleans fail; a late correct result is not operational success. Mutating hidden truth metadata leaves all captured actor prompts unchanged.

For repository root 0, public specs require f0(x)=x+4 and, in the chain, f1(x)=3f0(x)+2=3x+14. Thus x=−2,0,5 gives f0=2,4,9 and f1=8,14,29. Parallel f1 is 3x+2. Repairs constructed directly from those specs pass; original subtraction defects, a constant replacement and an extra test file fail. An equivalent `0 + expression` repair passes. The AST allowlist is bounded and interpreted, not executed as unrestricted Python. The operational label must remain **restricted arithmetic repair**, not realistic repository engineering. This review used qualification root 0 and no transfer roots.

A separate 24-contender reservation probe admitted exactly 3 reservations of 30 under a cap of 100, retaining exposure 90. Reserve/settle use immediate SQLite transactions; ambiguous calls keep their holds and overruns close further admission. Independently calculated maximum per-call hold: 425,584 microdollars under the configured full-context/input-output rate assumptions. This is conservative accounting, not a verified live billing guarantee. A single canonical database and unchanged shared $20 ceiling remain essential; new database paths do not enforce a global cap.

## Earlier engineering findings

E1 is repaired in the inspected path: safe allowlisted categories cross the child boundary; route/credential/account and stage failures stop batch admission; transport errors are not repaired as malformed plans. Unknown-cost failures retain exposure. E2 is repaired offline: start is fail-closed, bounded progress is separate from actor execution, terminal outcomes are saved before delivery, and artifact/terminal acknowledgments determine publication completeness. False/spooled delivery is not relabeled success. E3 is repaired: every assignment gets a durable record and the finally reconciler retains terminal, interrupted, admission-failed and not-started states. Fault tests exercise all 16-row denominators and preserve completed local outcomes.

These findings close the earlier software objections at the pinned hashes, not the host/runtime checks. The new spawn-based delivery wrapper still needs its already planned zero-model synthetic end-to-end diagnostic on the intended host; author documentation or older registration receipts do not prove the new path works.

## Required before Q-A dispatch

Pin and qualify requested/served model and provider, usage fields, rates and runtime; fill the independent-review reference with this published review; verify the canonical ledger and existing spending authorization; obtain a current exclusive claim; freeze source/config; refresh the immutable public plan/registration; verify each run TLDR and synthetic reporting/replay delivery. The checked-in config correctly remains blocked. I neither changed it to ready nor inspected credentials, spent money or allocated a server. Treat these as operational prerequisites to the narrow pass, not as permission to launch automatically.

## Q-B and interpretation limits

The existing chain-plan issue remains: `validate_plan` accepts an empty graph for a public chain, as my probe confirms. Every actor sees all public records, so it can also recompute/in-line prerequisites. Before Q-B, enforce required scheduling edges or explicitly redefine and measure the flexible planning treatment; do not infer serialized execution from the chain label. This does not invalidate the N=1 competence screen.

Q-A uses generous prespecified screening caps; Q-B uses success-conditioned calibration. They are not a matched N comparison. Keep the minimum-success gate, all failures/censoring and separate time/cost quantiles; stop if calibrated limits exceed authorized ceilings. Four roots per cell do not estimate a reliable service tail. A core comparison requires disjoint roots and identical envelopes across N; selection overhead and pre-launch-only selector features must be charged. No transfer access or optimal-size finding is licensed by qualification.

The focused author prior-art review is candidly incomplete. I reopened the [Kim et al. abstract](https://arxiv.org/abs/2512.08296), which already reports architecture/task dependence, and the [Tran–Kiela abstract](https://arxiv.org/abs/2604.02460), which directly challenges unmatched-compute multi-agent gains. Abstract checks do not certify their methods or a completed lab survey. The defensible prospective contribution is a resource-conditional launch rule under a frozen protocol, not the discovery that agent count matters.
