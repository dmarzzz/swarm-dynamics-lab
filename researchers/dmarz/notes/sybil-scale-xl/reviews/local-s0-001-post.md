# Post-mortem: local-s0-001

- Stage: S0 offline (scripted, no model calls), on orbital-one, started 2026-10-04 ~06:01 UTC.
- Outcome: **interrupted, no rows recorded.** Only `worlds.jsonl.gz` (partial) was written before orbital-one ran out of memory at ~06:07:45 UTC and the Flight Deck sessions unit, including this operator, was killed.
- Causes: the main cause was an unrelated crash-looping service on orbital-one (about 8.6 GB per cycle, per dmarz/fleet-monitor). A contributing cause in this study's code: world preparation used one process per job up to the machine's 96 cores, so up to 24 forked processes held worlds of up to 8,748 identities at once. A concurrent plan-size calculation in the same session prepared another 144 worlds the same way.
- Repair: the preparation pool is now capped at 4 processes (src/study.py). Output is unaffected: selection and preparation remain deterministic and order-preserving, and 11/11 selftests pass after the change, including exact equality with the parent simulator at N=36–972.
- Next run: no further local S0 on orbital-one (fleet-monitor instruction: keep heavy simulation off this box). The scripted S0 runs as fleet-s0-001 on the claimed server sim-dmarz, which records peak memory for the S1 sizing.
