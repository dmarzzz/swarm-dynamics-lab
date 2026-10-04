# Post-mortem: v3-d1-a1

2026-10-04 UTC. Parent `v3-q0-a1`; [pre-run assessment](v3-d1-a1-pre.md),
[prospective plan](../benchmark-v3/D1-PLAN.md),
[results and analysis](../benchmark-v3/RESULTS-D1.md).

## Decision

Execution and preservation passed. **Diagnostic competence failed for both models.**
Haiku achieved 2/6 full-evidence decisions and 1/6 report quorums; Sonnet achieved
3/6 and 3/6. The unchanged admission rule required at least 5/6 on both. No fresh
qualification, swarm sweep, D2, confirmation or other successor was launched.
The user explicitly requires the next plan to be published but not started.

## Assignment and accounting reconciliation

120 assigned → 120 started → 120 terminal → 120 graded → 120 analyzed; exactly
60 calls/model. No provider or invalid-output failures, retries, missing usage,
unresolved requests, duplicate dispatches or unstarted assignments. All model IDs
matched. Input/output totals 320,600 / 11,528; no cache tokens; observed model cost
$0.754780, split $0.189970 Haiku and $0.564810 Sonnet. Server and Codex orchestration
costs are separate and not invoice-reconciled. $4.110168 was conservatively reserved
within the standing shared $500 authority; no superseded tiny cap obstructed D1.

## Experimental interpretation

Sonnet improves report reading/decision coverage and handles omission and equal-rank
memory conflicts more consistently. Its three remaining full-evidence mistakes are
infeasible choices despite all facts being extracted correctly. It regresses on one
world that Haiku gets right. The clean competence problem is not fixed by this model
substitution. Both models propagate all six deliberately inherited false facts;
Sonnet also fails five of six correlated-copy fixtures under the policy-justified
criterion. These are substantive measured outcomes, not deployment failures.

D1 controls the saved actor request, not all possible model configurations or actual
token consumption. Haiku-generated packets, six reused worlds, no thinking budget
and different fixture/swarm-parent wording constrain interpretation. The independent
arithmetic implementation agrees with all 48 clean full/report decision labels.
All full-evidence raw outputs place the vote first; an ordering/contract explanation
is a hypothesis, not an identified cause. No inferential test is supported by this
small development comparison.

## Failure and limitation ledger

| Item | Evidence | Disposition |
|---|---|---|
| D1-C1: clean reasoning/contract failure | Both models below 5/6 on both gates; 48/48 extracted full-evidence facts correct/model | Open; propose canonical decisions and atomic feasibility probes; do not repeat D1 until a favorable result |
| D1-M1: origin handling | Policy-justified correlated-copy outcomes 0/6 Haiku, 1/6 Sonnet | Open; future origin/merge intervention must be a new treatment, not a rescore |
| D1-M2: supported false inheritance | 6/6 wrong-but-supported answers for both | Expected diagnostic harm; stronger reasoning cannot supply evidence absent from the packet |
| Q0 endpoint omissions | Abstention, ambiguous-world truth error and local support remain distinct | Not fixed by D1; retain original endpoints and predeclare any successor harm/utility changes |
| Q0 failure-path repairs | Exhaustive fixed-electorate tests, reason allowlist, narrow float portability checks; D1 exact audits pass | Software evidence passes; D1 had no real failed ballots/provider calls, so live failure handling remains exercised by tests/rehearsal only |
| First-boot package lock | One provisioning attempt met active cloud-init updates | Waited for updates; second provisioning passed; no paid call affected |
| Sparse-checkout preparation | Initial incomplete checkout preserved before correction | Helper corrected before freeze; exact source/input checks passed; no paid call affected |
| Owner inventory relocation | Concurrent legitimate owner apply moved generated output | Read authoritative state output and verify identity; no stale restore or second writer |
| Cloud lifecycle limitation | Hosted task wrote source but lacked raw-data/service credentials and authoritative fleet state | Remote worker/watchdog/upload independent of laptop; operator retrieved records locally and later retired the server through the authoritative always-on executor; no autonomous cloud lifecycle claimed |

## Verification and delivery

All 15 D1 software tests pass locally and remotely; the cloud coordinator's full
offline record has 118 tests. The real systemd rehearsal completed 120 scripted
assignments with zero model calls and one deliberate failure. Its failed hub status
is intentional; failure preservation, progress, durable events, six artifact
readbacks and duplicate refusal all passed. The paid run separately finished done.

The server-side watchdog observed healthy progress and ample available memory;
the paid service used Restart=no and a 65-minute hard bound. The exact-source
auditor recomputed all 120 paid requests and outcomes on server and local Python
3.12. All six original indexed artifacts match independent downloads. No actor
inputs or private infrastructure identifiers enter public tables.

Visualization mapping `d1-call-ledger-v1` uses the hub's actual call-count, cost and
failure series; the terminal API counters match the saved records. This is a
model-only diagnostic, not a swarm animation. The ordered journal and call latencies
are retained. Q0 replay delivery is separate and cannot be relabeled as verified
by this run's successful counters.

## Deployment-policy timing discovered at closeout

A new agentops run-queue instruction landed at 04:47:40 UTC, roughly 30 seconds
before the operator dispatched D1 at 04:48:10. The operator checkout/preflight used
the previously documented owner-initiated mode and did not pick up that new queue
rule before launch. This is a process miss, not an experimental-condition change.
It was discovered on the closeout refresh. The worker completed once, with no
retry or second coordinator. Future proposals explicitly require the current
always-on queue; no queue issue is filed for D2.

Closeout also discovered that owner infrastructure state had been transferred
to the always-on executor. The local copy must not be used for retirement or
new provisioning. Verify the current owner workflow and preserve all other servers.
This change does not retroactively establish cloud raw-artifact access for D1.

## Next action and closeout

Publish this report, the result tables and [D2 plan](../benchmark-v3/D2-PLAN.md).
The plan proposes 48 calls on the same open development worlds to separate simple
predicate application from multi-option decisions and evidence packaging. It is
**not authorized to launch**. No holdout or fresh-qualification world was opened.

Closeout completed at 05:17:22 UTC. The exclusive claim is released and the
temporary server is retired through the authoritative always-on owner workflow.
A saved, inspected infrastructure plan deleted only D1 resources; the provider
returned 404 for that server and all 21 other servers retained their identity,
addresses and size. The initial plan stopped on a stale off-fleet output lookup;
a narrow output filter repair allowed the targeted plan without changing another
server. Raw artifact and operator-control archives were hash-verified before
retirement. The worker had exited and the observer timer was stopped. See the
final [lifecycle receipt](../benchmark-v3/results/v3-d1-a1/lifecycle.json).
D2 is neither queued nor started.
