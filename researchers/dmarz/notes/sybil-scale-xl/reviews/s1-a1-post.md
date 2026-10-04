# Post-mortem: s1-a1

- Run sybil-scale-xl/7a32ec63 (A1 runtime). Started at 07:54 UTC by the chain; stopped with SIGINT at ~08:20 UTC during input preparation. Hub status failed, 0 episodes, 0 model calls, USD 0.
- Cause: a deliberate operator stop to add the overload retry rule before any paid call ([AMENDMENT-A2.md](../AMENDMENT-A2.md)). No scientific observation was made or discarded.
- Next: s0-a2 → q0-a2 → s1-a2, chained at software gates.
