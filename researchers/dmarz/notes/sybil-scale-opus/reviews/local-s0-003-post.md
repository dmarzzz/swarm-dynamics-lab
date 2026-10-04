# Post-mortem: local-s0-003

Offline scripted S0 on orbital-one, 2026-10-04 ~08:30Z, after adding `src/probe.py` (one-call P0 interface probe on an engineering packet, cost counted in the study ledger). Source hash `621c867c6ff495da807988b90807ed7c82642c6112bc91c74271618572d0c96a`; this supersedes the hash stated in the retry amendment (`323f8b7b…`, local-s0-002, retained).

- 264/264 valid, 0 invalid, 0 model calls; qualification cells at all four sizes passed. 11/11 selftests.
- No failures. Next: fleet S0, then P0 (one Opus call), Q0, S1 on the claimed dedicated host.
