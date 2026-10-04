# Post-mortem: q0-a1

- Run sybil-scale-xl/a6b2a7b3, revision d8653369, source 0384b4cd…, claude-opus-5-5 at effort low. Launched by the scale-xl chain at the passed s0-a1 gate (s0-a1: 72/72 scripted rows, run 4673b7bd).
- Outcome: **pass at every size.** 24/24 calls valid; the qualification gate passed at N=972, 2,916 and 8,748. Cost USD 9.853084 actual (USD 13.88 reserved), inside the USD 7–12 estimate.
- Disposition: S1 under A1 (run 7a32ec63) launched automatically, then was stopped by the operator during input preparation with 0 model calls, to add the overload retry rule ([AMENDMENT-A2.md](../AMENDMENT-A2.md)). q0-a1 remains a valid qualification of the A1 runtime; A2 requalifies at its own runtime.
