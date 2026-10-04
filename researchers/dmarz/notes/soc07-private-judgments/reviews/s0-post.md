# Post-mortem: s0-a1 and s0-a2 (scripted fixtures on the fleet)

- Experiment / owner / stage / date: soc07-private-judgments / dmarz (agent dmarz/soc07-private) / S0 scripted / 2026-10-04 UTC.
- Pre-run assessment: [s0-pre.md](s0-pre.md). Parent attempt: local-s0-001 on the builder's machine (69 of 69 checks).
- Disposition: **advance** to the reviewer's check of [s1-pre.md](s1-pre.md). No model call has been made by this study.

## What ran and what happened

| Attempt | Hub run | Revision | Runtime fingerprint | Result |
| --- | --- | --- | --- | --- |
| s0-a1 | `soc07-private-judgments/ae76d67b` | `b4e2cd5b25b151a733abe1f06ba87e3f327eb167` | `95b42e50…` | done; 69 of 69 checks; 482 seconds |
| s0-a2 | `soc07-private-judgments/bafeae75` | `61de92259f045fdd97255317a5f93dd0010119ad` | `afacff91…` | done; 69 of 69 checks; 463 seconds |

s0-a2 exists because the runtime changed after s0-a1: the S1-R gate gained two software checks (clean-regime competence and per-phase truncation), failed-call text is now kept in the journal, and S0 progress reports carry zero-call metrics. The generator, prompts and scorer hashes are identical in both attempts. s0-a1 is preserved as it ran; s0-a2 is the scripted prerequisite for the fingerprint that the paid stages would use.

- Planned, started, terminal, graded, analyzed (each attempt): 1,500 scripted episodes on 60 fixture worlds (1,200 team episodes under four policies, 240 replay, 60 single-solver), plus nine fault runs of 15 planned episodes each. Every planned episode has exactly one terminal record. The only episodes not completed are the ones the fault injections are meant to cut short (public budget exhaustion, leaked truth, controller crash).
- Calls, tokens, cost: 21,300 scripted calls in the main runs; **0 model calls, USD 0**. No credential was passed to the server for this stage; the launcher refuses to.
- Checks: 69 of 69 pass. Among them, team success in all 15 regime-by-arm cells matches the value fixed in advance for each of the four policies (for the evidence-following policy: 20 of 20 everywhere except VOTE in the informed-minority regime, 0 of 20); revision counts match (evidence-following: 80 useful, 0 harmful in the informed-minority regime; majority-following: 0 useful, 20 harmful there); no truth canary, canonical id or regime word in any of 5,100 contexts; first choices visible only in PUBLIC and only as choice and confidence; VOTE sees only its own records; public and private finals fork from one frozen context; all nine fault runs behave as specified.
- Expected versus observed: no difference.
- Server unit tests: 56 pass and 1 skipped of 57 at the first revision; 57 pass and 1 skipped of 58 at the second. The skipped test is the approval-pinning test, which needs `reviews/s1-pre.md`; that file is committed after the deployed revision, and the test passes on the builder's machine (58 of 58).

## Visualization review

- Mapping v1. Delivered per run: `final_frame.png`, `replay.gif` (13 frames, blocks 0 to 60 in steps of 5) and `initial_frame.png`, all 1800 x 1200. The launcher's `verify` step matched every uploaded artifact's SHA-256 to the server copy, decoded every frame and verified 15 journal hash chains.
- Agreement with recorded metrics: the final frame downloaded from the public site shows 20/20 in 14 cells and 0/20 for VOTE under informed minority, 100/100 useful and 0/200 harmful revisions in PRIVATE, PUBLIC and NEVER, and 5,100 scripted calls, equal to `analysis.json` for the evidence-following policy.
- Public site: the experiment and the run are listed with title, description, parameter labels and metrics; the three images load through the public route; `summary.json` is not served there (404), as intended.
- Limits: the S0 replay shows one policy accumulating over fixtures. It is not a model's behaviour and there is no within-episode view.

## Experiment-quality assessment

- This run tests the instrument, not the question. It shows that the scorer separates correction (evidence-following) from corruption (majority-following) and from stubbornness, that arms differ only where the plan says, and that failures stay in the denominator.
- What it cannot show: anything about the provider. The HTTP exchange, structured output and usage accounting are exercised only against a fake transport and a scripted provider. The first real request is S1-Q's first call.
- Not covered: a provider-side partial failure pattern (for example a burst of rate limits) under real concurrency; rendering under hub upload failures during a long run.

## Failure and repair ledger

| ID / kind | Observed evidence | Cause | Repair | Acceptance check | Status |
| --- | --- | --- | --- | --- | --- |
| S0-1 / execution (local, before the fleet) | First local suite run took 156 s; ledger recomputed totals on every transaction | Quadratic bookkeeping | Incremental counters | Local suite 74 s then 40 s; all checks pass | closed |
| S0-2 / measurement (local) | A crash lost the completed arms of the block in progress (4 episodes marked interrupted, 1 expected) | Episode records were written per block | Each episode record is written and synced when it closes | Crash check: exactly 1 interrupted, the rest incomplete | closed |
| S0-3 / measurement (local) | The "raw output never shown" check compared against a peer's identical valid output | Flawed check, not a leak | Injected malformed output carries a unique marker | Marker absent from every context | closed |
| S0-4 / operator | A background wait loop on the builder's machine never ended because its process match also matched itself | Operator error | Loop stopped by exact process id; status taken from the launcher instead | Run status and verify output above | closed |

## Next run

- Next action: reviewer reads the code and `s1-pre.md`. On an explicit go: commit `launch/s1-approval.json` pinned to the fingerprint, redeploy that commit, run S1-Q (12 calls), stop and report.
- Stop conditions and gates: see `s1-pre.md`.
- Blocker: none on the builder's side. No model call is possible until the approval record exists.
