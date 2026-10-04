# Experiment setup record: discussion-dose-v3 / D1

Status: D1 completed and audited; both clean diagnostic gates failed. The local operator launched exactly 120 calls; the cloud coordinator dispatched none. Results and post-mortem are published with this update; owner cleanup remains recorded in the lifecycle receipt. D2 is a plan only, not authorized to start. Follow the
[shared setup runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md).

## Ownership and question

Instrument coordinator: dmarz/cloud-discussion-d1. Sole deployment/paid launch owner:
dmarz/discussion-bench-v3 in the existing local operator environment. Independent
design reviews: [Vishesh](../../../../vishesh/notes/discussion-benchmark-v3-review/REVIEW.md)
and [Shadow](../../../../shadow/notes/review-discussion-benchmark-v3.md). This agent's
regression checks are engineering verification, not a new independent review.

Question/decision: [SEC-47](../QUESTION-LINKS.md), model-only constraint/evidence
diagnosis before any fresh qualification. Research status is exploratory instrument;
no hypothesis promotion, S1 or confirmation is authorized. [NEXT-RUN](NEXT-RUN.md)
and [Q0 post-mortem](../reviews/v3-q0-a1-post.md) define the existing design and
lessons. Current attempt `v3-d1-a1`, parent `v3-q0-a1`.

## Gate evidence

| Gate | Status | Evidence and assessor | Next action |
|---|---|---|---|
| G0 Question/research scope | pass for diagnosis | Existing question links/NEXT-RUN; no formal promotion | Stay in bounded development scope |
| G1 Prospective design | pass | Existing NEXT-RUN and frozen 60-request receipt; D1-PLAN deployment amendment | Freeze committed implementation |
| G2 Instrument | pass for offline software | [Validation](d1-offline-validation.json): 15 D1, 57 v3, 34 legacy, 12 v2 checks; coordinator Python 3.12.14 | Owner exact-Q0 integration/rehearsal still required |
| G3 D1 admission | passed for this completed batch | [Launch receipt](launches/v3-d1-a1.json): exact-Q0, rehearsal, provider/public-plan/budget checks | No renewed dispatch |
| G4 Scientific escalation | fail/closed | [D1](RESULTS-D1.md): Sonnet 3/6 and 3/6, Haiku 2/6 and 1/6, versus 5/6 each | [D2 plan](D2-PLAN.md) only; no S1/Q1/D2 launch |
| G5 D1 closeout | audit/readback passed; lifecycle tracked separately | [Results](RESULTS-D1.md), [post-mortem](../reviews/v3-d1-a1-post.md), [lifecycle](results/v3-d1-a1/lifecycle.json) | Complete owner cleanup after report publication |

## Design and instrument index

- Plan: [D1-PLAN](D1-PLAN.md), retaining [NEXT-RUN](NEXT-RUN.md) and its exact
  [planning receipt](next-run-planning-evidence.json). Model-only treatment; six
  world clusters, three report ballots/world and 36 fixed memory fixtures/model.
- Inputs/context: actual saved Q0 bodies plus frozen system/schema; hashes bound
  by `diagnostic_v3.py prepare`. Gold remains evaluator-only. No fresh worlds.
- Tests: `src/diagnostic_v3_selftest.py`, `python3.12 -m bench_v3.selftest`.
- Source/config/evaluator: manifest records committed revision and dependencies;
  prompts/strict citations unchanged. Quorum/failure/audit extensions are successors
  only. Frozen Q0 remains audited at 883d310 on Python 3.12.
- CLI/visualization: D1-PLAN's hub/CLI contract and `d1-call-ledger-v1` mapping.
  Public Q0 replay delivery is deferred independently, not a gate to this diagnostic.

## Current attempt admission

See [v3-d1-a1-pre](../reviews/v3-d1-a1-pre.md). `prepare` freezes current committed
documents and immutable public plan URL/hash; `preflight` verifies public bytes/page
and owner evidence before `run`. No prior plan is accepted by substitution.

Budget: standing $500 across dmarz experiments; 120 calls; one worker; 2000 output
tokens/call; 60000 input bytes; 120-second timeout; one-hour execution plus upload.
Owner supplies actual shared spend/non-overlapping reservations, verifies remaining
claim and records encrypted credentials by alias only. The private deployment
mode may be `owner-controlled-local-cleanup`, with cloud retrieval explicitly
unverified. This admits remote worker independence, not autonomous owner lifecycle.

Dedicated server/claim: sim-discussion-d1 / dmarz-discussion-d1. Owner reports
established account verification and only-new-host provisioning. Exact runtime
access, exclusive claim and rehearsal evidence must be checked by the operator.
No addresses/account IDs/state/secrets appear here. Sole paid dispatch remains the
parent operator. Cloud coordinator has no provider/hub/DO secret access and makes
zero model calls. No local state copy or second infrastructure writer is created.

## Attempt and repair history

Q0: 96 assigned/started/terminal/graded/analyzed, 636 physical calls, $4.387237;
execution passed, model qualification failed. Preserve its receipts/results.

F1/F2 partial repairs landed at 6563e28 by private-control. D1 extends the fixed
quorum correction with explicit incomplete/no-quorum and completion bounds, and
replaces arbitrary reason/class metadata with an allowlist. Narrow continuous-cell
float portability is versioned; structural conflict loss is labeled. Acceptance:
offline regressions plus exact retained input verification on the owner host.

## Closeout

D1 execution, validity, preservation and exact audits passed; both model competence
gates failed. All 120 assignments and responses are retained. The result report,
post-mortem and conservative budget settlement accompany this update. Claim release
and retirement of only the D1 host follow report publication and are tracked in the
lifecycle receipt. The D2 proposal must remain unstarted.

## D1 completed; D2 remains a proposal

D1 reconciled 120 assigned/started/terminal/graded/analyzed calls at $0.754780, zero invalid/provider failures or missing usage. Both clean gates failed for both models. Remote and local exact-source audits and six artifact readbacks passed. Preserve runtime e9678355 and all responses. [D2-PLAN](D2-PLAN.md) proposes 48 canonical/atomic probes on the same open worlds; no implementation, server, executable manifest or inference was started. The user requires this next plan published but unstarted. Do not reuse D1 admission or its reservation for D2.
