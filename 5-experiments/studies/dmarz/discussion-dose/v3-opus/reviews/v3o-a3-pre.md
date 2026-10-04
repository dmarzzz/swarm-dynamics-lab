# Pre-run assessment: v3o-a3 (probe, S1 only)

- Experiment / owner / operator: discussion-v3-opus / dmarz / dmarz/v3-q0-opus (operated by dmarz/orchestrator-2).
- Parents: `v3o-a2-q0` (passed; the admitting gate for this attempt) and the stopped `v3o-a2-s1`
  ([post-mortem](v3o-a2-s1-post.md), read before this assessment).
- Authority: dmarz's standing instructions relayed by fleet-monitor and his first-hand statement "Great messages
  starting [fleet-monitor] as my instructions including claims lUcnhes model switches And budget costs thanks And
  stop Asking for my permission" (2026-10-04 ~07:55Z); fleet-monitor recommended option (a), a new dated attempt,
  at ~10:13Z. Cross-researcher review waived by the owner ([OWNER-AUTHORIZATION.md](../OWNER-AUTHORIZATION.md));
  none performed.

## Design and assessment

Unchanged S1 design from [v3o-a1-pre](v3o-a1-pre.md): 24 worlds (12 resolvable, 12 ambiguous), 3 agents, 3
extra rounds, 4 arms, clean and attacked exposures, diagnostics and memory fixtures; 384 cases, 2,436 calls;
worlds are the independent units and arm contrasts are paired by world. S1 has no gate; it is exploratory.
Only change of sample: **fresh worlds 54201–54224**, disjoint from every used or reserved range (dev 10002–10007,
tests 10101–10160, 20001–20006, holdout 30000–30023, sidecar 40001–40012, 50001–50006, 52001–52012, Q0
54001–54006, retired 54101–54124; checked in source and selftest).

## Changes and unresolved issues

1. **S1-only chain.** `chain --s1-only` runs the one-call probe and then S1. Admission is the passed Q0 recorded in
   the launch record's `q0_gate`: the committed copy of `v3o-a2-q0/summary.json` (sha256 `26cd713a…`, identical to
   the server file) must hash-match and show `model_qualified` and `execution_complete`. Tested offline.
2. **Credit halt.** After one `provider_credit_balance_low` failure (recorded as an ordinary provider failure, never
   retried) the next dispatch raises `CreditHalt`, a BaseException the runner's per-call handler cannot absorb, so
   the stage stops and is reported failed with the ledger preserved instead of continuing with a hole. Tested.
3. Everything else is byte-identical in behaviour: Opus 5.5, adaptive thinking, effort high, no temperature, 16,000
   output tokens, 8,000-character visible cap, 600 s timeout, 429/529-only retries (at most 2), clean-first order,
   bench_v3 instrument and scoring unchanged. Selftests: bench_v3_opus 13/13, bench_v3 OK.

Risk: another credit outage. With the halt it now stops the stage at the first credit failure; any repair is a new
attempt. Risk: Opus rate limits; the workspace is near idle after scale-xl stopped.

## Frozen execution plan

Pinned to the commit that adds this file; launch record [`../launches/v3o-a3.json`](../launches/v3o-a3.json)
carries every source hash and the Q0 gate digest and is validated in-process before any call. Caps: probe 1 call
(USD 1 ceiling); S1 2,436 calls, attempt cap 2,679, USD 1,500 reservation ceiling. Expected actual cost about
USD 55–90 (a2 measured USD 0.0234 per successful S1 call), wall time about 4–6 h. Server sim-dmarz-9 under the
existing exclusive claim `dmarz-v3-q0-opus` (until 22:13Z), which names this study and this lane's agent. No
restarts. Credentials by SOPS -> ssh stdin -> process environment only. `cost_usd` reported to the hub.

## Visualization mapping

`v3-deliberation-v1`, unchanged: live `frame.json`, final frame, `replay.json` and `replay.html` from the journal;
failed or missing calls shown as invalid ballots, never interpolated. Bound to `discussion-v3-opus/v3o-a3-s1`.
