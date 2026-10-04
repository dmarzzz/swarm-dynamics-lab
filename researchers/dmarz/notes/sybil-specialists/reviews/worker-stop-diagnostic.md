# Worker stop-policy diagnostic

2026-10-04 UTC; dmarz/sybil-specialists. Code inspection after the completed fleet S1 batch found that the generic reporter work loop catches a failed-cell exception and continues to the next assignment. That behavior conflicts with this instrument's declared stop-on-invalid policy. No failed or invalid cell occurred in the completed 34 runs, so their assigned denominator and results are unchanged.

The worker now takes one assignment at a time and lets the reporter Run context record a failure before propagating it out of the loop. A new offline injected-failure test confirms exactly one assignment is taken and the exception reaches the reporting context. All 15 offline checks pass. Simulation, rendering, scoring, frozen design and existing run outputs are unchanged. Install the revised source in verify-only mode and run the same 15 controls remotely; do not queue replacement scientific observations. Any later scientific stage at the new revision must requalify S0 under the coordinator's existing exact-source gate.

Disposition: bounded deployment verification, zero model calls/spend, no new experimental assignments. Record remote verification in the final fleet post-mortem before closing.
