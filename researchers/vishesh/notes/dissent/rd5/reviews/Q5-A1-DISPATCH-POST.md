# RD5 expired activation closeout

**Execution was blocked before the experimental worker started. There is no new Jev accuracy result.** Reconciled 2026 October 04 by vishesh/codex-decision-models. The first Q5 relay activation expired without dispatch; the reviewed next action preserves the already approved Q5/conditional H5 scope. [Structured reconciliation](../results/activation-a1/summary.json), [status figure](../results/activation-a1/dispatch-closeout.png), [renewal plan](../ACTIVATION-02.md).

## What happened

The prospective scientific plan, public registration, frozen source, dedicated allocation and initial remote relay health were prepared. The local relay opened around 08:44 UTC and closed automatically at 09:14 UTC. The central queue received the request but supplied no acknowledgement or dispatch record. Its availability or reason for not responding is unknown.

The original ledger shows zero RD5 provider reservations or responses. A trusted, read-only remote check at 15:19 found no Q5/H5 dispatch marker, supervisor marker, result directory or RD5 worker. The 24 frozen Q5 assignments remain unstarted. H5's 72 planned decisions were never admitted. Qualification is unknown, not failed; wrong-response count 0 is not evidence of correct answers. No native artifact readback can be claimed because no native artifacts exist.

The claim expired at 10:40 but remained labelled running until the explicit release at 15:20. This is an operational closeout failure. The earlier readiness statements were time-bound and became stale. We retain their history and correct current SETUP/RUN-STATUS rather than treating those assertions as live admission.

## Cause and correction

The observed failure is the missing central dispatch while a short local relay lease was already running. We do not infer why the coordinator did not acknowledge it. The actionable process defect was allocating and opening the relay before a confirmed launch slot, then leaving a stale ready request after the relay expired.

The renewed workflow requires coordinator acknowledgement first, then a fresh exclusive allocation, complete current admission, an actual forwarded health check and one central worker launch. The external wrapper now accepts explicit Q5-A2 identity and separate immutable paths, checks for either old/new dispatch under a shared stage lock, and rejects a near-expiry renewed relay. Five offline activation/fault checks passed. The scientific code and both prepared packets are unchanged; all 61 scientific offline checks still pass.

The original A1 relay fence remains in SQLite. Q5-A2 can use the same never-dispatched assignment IDs only after verifying zero RD5 calls and the untouched historical ledger. It cannot retry an ambiguous provider call, reset a counter or reuse the A1 activation. Native H5 still requires the complete source-bound Q5 bundle and its actual scientific post-mortem.

## Scientific interpretation against the plan

RD4 remains the latest native evidence: the original and symmetric gates scored 87/96 against always-check 88/96. Saved traces implicated both missed recovery admission and inconclusive checks consuming later capacity. That supports testing the narrow RD5 mechanism, not claiming that a repaired gate is already superior.

The approved Q5 separates source-card interpretation from allocation; H5 separates attempt memory from future-check reservation. The urgent-early scenario can falsify a general reservation benefit. Neither contrast was observed in this activation. The design still has six authored roots, known timing, one H5 domain and scripted ballots; it cannot establish population precision, independent semantic generalization or emergent swarm behavior.

The current PI recommendations are retained within their proper scope. Keep the matched resource cap and strong B0/B1 controls, report accepted wrong actions and urgent delay, and preserve root pairing. Defer random allocation, checker-reliability strata and unpredictable timing to a future decision rather than editing the approved cohort. Stop after Q5 failure, a valid H5 result or an unresolved external blocker; remaining call margin does not authorize another experiment.

## Accounting and limits

Original provider accounting is unchanged:428 calls; USD 0.016620450 settled and USD 0.004032 unresolved, for USD 0.020652450 committed. This activation added zero provider calls, tokens or model charges. All historical unresolved reservations remain.

The [infrastructure reconciliation](../results/activation-a1/resources.json) conservatively includes complete historical claim windows and the unused RD5 window through explicit release, not merely its earlier expiry. At the recorded hourly rate, total estimated infrastructure exposure is USD 0.690783567 including historical wrong-account compute. This is not a reconciled provider invoice; historical invoice gaps remain. A prospective90-minute allocation would bring this estimate to USD 0.797928567, subject to fresh price/account verification. No new allocation is held now.

The original USD 2 cumulative authority remains USD 1 API plus USD 1 infrastructure. Q5 and H5 together allow at most60 new calls and lifetime stop 488; twelve calls stay unallocated. No top-up, new ledger, credential transfer or host exception is asserted.

## Current decision

**Blocked on a confirmed authorized central dispatch slot.** Q5/H5 approval is already present and is not requested again. The separate direct-from-laptop exception remains unresolved. The private queue has been corrected to show the expired handoff and exact acknowledgement needed before fresh leases. No new host or relay was started in this review cycle.

The operational finalize hook records this as an operator-reconciled blocked dispatch, not a native model failure. The [eleven-dimension scientific review](Q5-A1-DISPATCH-QUALITY.json) supplies the assessment that an automatic scaffold cannot. A new native post-mortem, measured visualization and artifact readback remain required if central dispatch becomes available.
