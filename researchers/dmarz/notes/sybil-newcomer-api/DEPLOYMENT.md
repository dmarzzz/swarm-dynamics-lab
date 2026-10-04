# Deployment record

Experiment sybil-newcomer-api is an exploratory owner-authorized follow-up. Independent review was explicitly waived in WAIVER.md; model qualification, source gates, cost limits, complete records and honest reporting remain required. Formal S2 is disabled.

- Host: sim-dmarz-4.
- Exclusive claim: dmarz-sybil-followups, covering the two parallel owner-authorized follow-ups.
- S0 execution revision: `106d1082db3152af5bcf5e4539bca81adc13d57d`.
- Q0 execution revision: `996a4af01ebfff3071b88c60914472b171798053` (same frozen runtime).
- Frozen runtime fingerprint: `f38a9658dcb5e403e9dfaeccfd201c603b84d947ed085779374b278ceb4ef943`.
- Runtime: Python 3.12 with pinned requirements; isolated finite worker and output directory, at most two concurrent paid requests.
- Model: `claude-haiku-4-5-20251001`, temperature zero, structured six-field response, no tools/cache/retries.

| Stage | Run | State and reconciliation |
|---|---|---|
| Fleet S0 | `sybil-newcomer-api/68819f24` | Done, first attempt; 198/198 valid, 36/36 exact clean packets; zero API calls and spend |
| Q0 | `sybil-newcomer-api/f7b78b41` | Done, first attempt; 36/36 valid and exact, all qualification thresholds passed; $0.043560 actual |
| S1 | Ready, not launched | 1,944 paired scientific observations; exact-runtime S0/Q0 passed, subject to current allocation/budget check |

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
