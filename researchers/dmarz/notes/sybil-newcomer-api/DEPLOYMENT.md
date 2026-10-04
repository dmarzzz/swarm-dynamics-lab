# Deployment record

Experiment sybil-newcomer-api is an exploratory owner-authorized follow-up. Independent review was explicitly waived in WAIVER.md; model qualification, source gates, cost limits, complete records and honest reporting remain required. Formal S2 is disabled.

- Historical S0/Q0 host: sim-dmarz-4.
- Historical dedicated S1 host: sim-dmarz-sybil-newcomer; destroyed after verified completion.
- Historical S0/Q0 claim: dmarz-sybil-followups.
- Dedicated S1 claim: dmarz-sybil-newcomer; released, no active claim remains.
- S0 execution revision: `106d1082db3152af5bcf5e4539bca81adc13d57d`.
- Q0 execution revision: `996a4af01ebfff3071b88c60914472b171798053` (same frozen runtime).
- Frozen runtime fingerprint: `f38a9658dcb5e403e9dfaeccfd201c603b84d947ed085779374b278ceb4ef943`.
- Runtime: Python 3.12 with pinned requirements; isolated finite worker and output directory, at most two concurrent paid requests.
- Model: `claude-haiku-4-5-20251001`, temperature zero, structured six-field response, no tools/cache/retries.

| Stage | Run | State and reconciliation |
|---|---|---|
| Fleet S0 | `sybil-newcomer-api/68819f24` | Done, first attempt; 198/198 valid, 36/36 exact clean packets; zero API calls and spend |
| Q0 | `sybil-newcomer-api/f7b78b41` | Done, first attempt; 36/36 valid and exact, all qualification thresholds passed; $0.043560 actual |
| S1 | `sybil-newcomer-api/8def40e4` | Done, first attempt; 1,944/1,944 valid and verified; $3.088659 actual; worker exited, archive complete, claim released, temporary host destroyed |

The S0 verification receipt confirms eleven durable artifacts and no reporting errors. Initial/final PNGs are 1800×1200 and the 1800×1200 GIF contains eight decoded logical frames. The worker had stopped at verification. Public visual links:

- [Experiment dashboard](https://swarm-live.pages.dev/#/x/sybil-newcomer-api)
- [Scripted S0 run](https://swarm-live.pages.dev/#/r/sybil-newcomer-api%2F68819f24)
- [Scripted final frame](https://swarm-live.pages.dev/api/a/sybil-newcomer-api/68819f24/final_frame.png)
- [Scripted replay](https://swarm-live.pages.dev/api/a/sybil-newcomer-api/68819f24/replay.gif)

These links identify published synthetic artifacts; image decoding does not itself establish browser animation playback. See reviews/fleet-s0-001-post.md for the completed engineering checkpoint. S0 does not establish API competence or policy superiority.

Q0+S1 nominal call count is 1,980, with a 2,050 attempted-call ceiling, $75 per-study nonrefundable conservative reservation ceiling, and a shared $60 actual-plus-outstanding bundle guard within the owner's $500 aggregate limit. Conservative serialization reservation for all nominal newcomer requests is $20.591978, not actual spending. Shared bundle accounting was entirely zero at S0 verification. The parent operator handles credential injection through authorized aliases, later stage records, durable artifact checks, public playback and claim release. No private endpoints, server addresses or credential values are recorded here.

## Q0 checkpoint

Q0 completed 36 planned/started/terminal/graded/analyzed observations with zero invalid, missing, duplicate or retried calls. Usage was reported for all calls: 36,360 input tokens and 1,440 output tokens, costing $0.043560. The study conservative reservation was $0.337581; it is not additional spend. Collection took 21.5276 seconds, excluding final rendering/analysis. Every full/common-only/sparse cell had twelve exact packets and 100% required missing-field abstention. The finite worker stopped after completion.

The operator verified eleven durable artifacts, 1800×1200 initial/final PNGs, and a nine-frame Q0 completion replay. Recomputed packet hashes, every grade, same-packet plurality, analysis, denominators and accounting all matched under the pinned Python environment. The parent verified public replay playback, observing progress advance from 0/36 to 14/36. One minor display limitation remains: Q0 replay's elapsed label defaults to 0s; the measured duration above comes from summary.json. It does not affect counts, qualification, cost or S1's separate logical-round renderer.

[Q0 run](https://swarm-live.pages.dev/#/r/sybil-newcomer-api%2Ff7b78b41), [Q0 final frame](https://swarm-live.pages.dev/api/a/sybil-newcomer-api/f7b78b41/final_frame.png), and [Q0 replay](https://swarm-live.pages.dev/api/a/sybil-newcomer-api/f7b78b41/replay.gif). Sanitized receipts are in records/q0-001-summary.json, records/q0-001-verification.json and records/q0-001-artifact-receipt.json. See reviews/q0-001-post.md.

At this verification checkpoint the two-study shared guard recorded $0.366548 actual/committed, zero held, and 52/52 reservations settled against its $60 cap. This is a time-specific bundle total, not newcomer-only cost or the entire owner's spending. S1 has not launched in this record; the parent must commit the Q0 reconciliation and recheck current allocation and aggregate budget first.

## Allocation correction — 2026-10-04 UTC

The owner's updated inbox requires a dedicated host for each experiment. S0 and Q0 historically completed on sim-dmarz-4 under dmarz-sybil-followups; those completed results and runtime fingerprints are preserved. Before S1, this study moves to the dedicated host sim-dmarz-sybil-newcomer under claim dmarz-sybil-newcomer. Provisioning, claim exclusivity, migration and ledger continuity remain pending the parent operator's verification. S1 is not launched by this correction. No simulator, assignment, model, evaluator or source/configuration fingerprint changes.

Across the separate hosts, the existing $60 bundle cap is partitioned into at most $50 total for sybil-budget-api and $10 total for sybil-newcomer-api. Both hosts retain the same settled 52-call checkpoint ($0.366548). The budget host permanently reserves the $10 peer allocation; the newcomer host permanently reserves the $50 peer allocation. Historical charges are not reset. Duplicating the settled checkpoint in both guard copies makes the aggregate bound stricter, rather than creating extra spending authority.

These permanent peer reservations are inter-host allocations, not API charges, model calls or unknown-billing failures. Do not count them as actual experiment spending. Final actual cost is the sum of the separate per-study usage ledgers. Existing per-study conservative reservation/call limits still apply, with the new partition providing the tighter real-spend limit. The parent must verify the guard state and exclusive allocation before launch; this document does not claim that provisioning or migration is complete.

## S1 launch, 2026-10-04T04:09:27.933420+00:00

Run `sybil-newcomer-api/8def40e4` launched once on `sim-dmarz-sybil-newcomer` under `dmarz-sybil-newcomer` with execution revision `e9db4c58a8847d2f54d60a8ff3cc70f81f58263e`. The scientific source fingerprint is unchanged. All prior artifacts and grades were reverified on this host after newcomer migration. The fixed peer-allocation holds are active and checked by the launcher; study histories and spending were not reset. One finite worker owns the one active run, with two concurrent API requests. The 1944 planned outputs are collecting; no final scientific result is claimed here. See [the live run](https://swarm-live.pages.dev/#/r/sybil-newcomer-api%2F8def40e4).

## S1 completion and verification — 2026-10-04 UTC

Run `sybil-newcomer-api/8def40e4` completed its first attempt with 1,944 planned, started, terminal, graded and analyzed records; zero invalid, not-started or retried calls. Execution revision remains `e9db4c58a8847d2f54d60a8ff3cc70f81f58263e`; scientific source is unchanged. Measured collection duration was 1,246.1025 seconds (about 20.8 minutes), excluding final rendering/analysis. The worker exited.

S1 consumed 2,688,594 input tokens and 80,013 output tokens for $3.088659 actual. Including Q0, the per-study ledger reports 1,980 attempted and usage-reported calls and $3.132219 actual; the nonrefundable conservative reservation is $20.591978, not additional spend. The guard checkpoint's $50 held entry is the permanent peer-host allocation, not an unpaid/unpriced model call. All newcomer API usage is known.

Pinned-runtime local recomputation reproduced all 1,944 assignments, 216 condition worlds, 1,728 world rounds, 5,184 policy-history records, packet hashes, grades, same-packet baselines, analysis and accounting exactly. All eleven remote artifact checksums passed. The 1800×1200 final PNG was visually checked in the public UI; its 1,944/1,944 counts and 26.4%/12.5%/20.8% main-cell values match the saved records. The direct public GIF visibly advanced from logical round one to six; all eight frames decoded, with unmeasured model rounds shown honestly.

[Final frame](https://swarm-live.pages.dev/api/a/sybil-newcomer-api/8def40e4/final_frame.png), [recorded replay](https://swarm-live.pages.dev/api/a/sybil-newcomer-api/8def40e4/replay.gif), [results](RESULTS.md), and [post-mortem](reviews/s1-001-post.md). Safe execution, recomputation and artifact receipts are in records/s1-001-*.json. Scientific collection/analysis, archival, Flight Deck filing, claim release and authorized temporary-host teardown are complete as recorded below. The retrospective public-plan preflight receipt gap recorded in SETUP.md remains explicit.

## Resource and artifact closeout — 2026-10-04 UTC

The parent verified release of claim dmarz-sybil-newcomer through agentops PR130 and hub release event 34510; the active claim is absent. Both ledgers and the cross-host allocation record were privately archived with hashes before removal. Raw S0/Q0/S1 records remain in the local data archive and durable hub artifacts.

Temporary host sim-dmarz-sybil-newcomer was destroyed through the established original Dmarz backend/account after review of a saved plan authorizing only its five resources and generated inventory. The twelve other host entries remained unchanged. Fleet removal PR131 merged at revision beginning `41e17d`; publication of the generated inventory update is still a parent bookkeeping step, not an active host or claim.

The [final figure](../../../../artifacts/sybil-newcomer-api-s1/sybil-newcomer-api-s1-v1.png) is filed with project provenance. Parent inspection passed, and Flight Deck strict validation reported thirty artifacts, zero errors and zero warnings. No new API calls were needed for archival, visual filing or teardown. Scientific disposition remains complete-valid-result; the documented historical public-plan URL/hash/page preflight gap is unchanged.

Final infrastructure receipt (2026-10-04 UTC): generated inventory PR132 merged as `751c72fbf2b7464e91de2f321f0a18a2aca2b365`; all other twelve entries unchanged. The newcomer allocation is fully closed. See [records/closeout.json](records/closeout.json).
