# Post-mortem: fleet-s0-001

- Run sybil-scale-xl/33d602fe on sim-dmarz (claim dmarz-sybil-scale-xl), revision 5f4d2fe2, runtime source hash 845bd712…. Scripted backend, 0 model calls, USD 0.
- Outcome: **pass.** 216/216 assigned, started, terminal, graded and analyzed; 0 invalid. Scripted qualification passed at every size (N=972, 2,916, 8,748: 16/16 clean packets each, field accuracy, exact packets and missing-fact abstention all 1.0).
- Execution: 624 s, almost all of it world preparation for the four N=8,748 engineering worlds with the 4-process pool. Server memory in use stayed at or below about 1.1 GB of 8 GB (sampled every 60 s, not a true peak). S1 preparation is 48 world-rate jobs per size, so roughly 12× this stage's N=8,748 preparation: about 1.5–2 hours before the first S1 call, on this server.
- Artifacts: publish then verify passed: 10 artifacts hash-checked, four 1800×1200 images decode, replay has 33 frames.
- Quality notes: no failures. The progress image is the only image uploaded during the run, as designed.
- Next: dmarz directed on 2026-10-04 (relayed by dmarz/fleet-monitor, ~07:36 UTC) that paid stages use Opus. Q0 and S1 under this Haiku manifest are therefore not launched. An Opus amendment changes the model, removes `temperature` (rejected by claude-opus-5-5), sets effort and raises the output limit for thinking, so it changes the source hash and needs its own S0 and fresh qualification. Its cost estimate goes to dmarz before any paid call.
