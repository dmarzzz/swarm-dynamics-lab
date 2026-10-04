# Prospective connection-lifecycle repair before S50

Written 2026-10-04 UTC before the operational amendment. Keep Q50's frozen source06e0ff48 and closure84423a431d6758606c61938f475f7a8b0ecc22112126c4d426fef8ff35aed8d3 unchanged. Its bounded qualification is separately admitted. No change is applied to an active worker or original evidence.

PI's independent offline test run exposed ResourceWarnings. Owning-session reproduction on the frozen runtime performed60 reserves and60 settlements: peak53 GC-visible SQLite connections,25 before explicit collection and0 after. A SQLite connection's context manager commits/rolls back but does not close it; this is a real lifecycle defect. No evidence currently shows a transaction, cost or scientific-output discrepancy.

Before S50, wrap every runtime database connection in explicit close/finally, retaining transaction context and BEGIN IMMEDIATE. Ensure the read-only historical fingerprint connection closes too. Repeated reserve/settle, duplicate/error/rollback and stage-cap paths must leave zero open tracked connections without relying on garbage collection; original rows, atomicity and ambiguity semantics remain unchanged. Native request bodies, cases, sample counts, scorer, model, timing/cost envelope and no-retry policy are unchanged.

If Q50 passes and its source/packet/trace review remains applicable, bind its receipt to its original closure and record this exact operational-only successor amendment. Do not label the old closure as the new source. Main still requires a separate allocation, current admission, observed-latency feasibility and its own immutable public plan. This file does not fund or launch main.
