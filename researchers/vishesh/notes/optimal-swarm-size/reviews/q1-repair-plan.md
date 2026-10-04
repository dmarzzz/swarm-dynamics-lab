# Q1 engineering repair plan

Written before repair implementation, 2026-10-04 UTC. No paid calls. Addresses engineering review 273e35ed; does not substitute for cross-researcher approval.

E1: propagate allowlisted error codes only, including numeric HTTP codes, preserving reservations for unknown costs. Separate stage from episode cap exhaustion. Fatal route, credential, billing/schema and stage-cap faults stop subsequent admission; no transport retries. Test distinct faults and dispatch count.

E2: preserve the mandatory public admission check. Once admitted, progress failures are reporting events, not model failures. Persist local outcome before publication; save per-artifact acknowledgments and terminal delivery status, treating queued/spooled as unconfirmed. Bound publication operations and stop further episodes on incomplete publication. Keep durable outbox evidence for later explicit reconciliation.

E3: create all assignment records before dispatch and reconcile the entire manifest in a finally block. Distinguish not-started, admission-failed, interrupted and terminal, with null scores for unexecuted conditions and explicit publication state. On early stop report partial execution. Never reopen a new ledger to evade the shared $20 cap.

Verification: affected unit tests plus new fault-injection regressions, followed by a pinned review amendment. Existing reviewer counterexamples are expected to cease asserting the old behavior; preserve their original evidence unchanged. A later prospective synthetic host reporting diagnostic will validate the installed client contract before paid launch. Q-B scheduling-structure review remains separate and closed.
