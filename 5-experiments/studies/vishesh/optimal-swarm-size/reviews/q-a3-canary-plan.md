# Q-A3 canary: frozen execution plan

Owner authorized the next run on 2026-10-04. Implements the prospective next-run-design.md published before implementation in c82dd3ac and structured-output-repair.md. Prior attempts remain unchanged. This document binds the accepted design to runnable canary configuration, not retrospective results.

## TLDR

Four width-2 N=1 synthetic canaries test native schema-constrained planning, worker output, integration, evaluation and reporting. Compare each final answer to its deterministic evaluator; historical prompt-only failures are descriptive background, not an independent control arm. Measure phase/schema validity, substantive success, latency, cost and publication. This is small engineering qualification, not an optimal-swarm-size estimate.

## Question and prediction

Will schema-constrained requests eliminate the fenced-response bottleneck and allow all four task paths to complete correctly? Predict four on-time correct final artifacts, with valid phase outputs, complete usage and verified publication. Failure is retained and blocks promotion. Q-A1 failed all 16 cases during planning; Q-A2 stopped after two fenced failures. Their scores are not recomputed.

## Setup

Pinned native claude-haiku-4-5-20251001, anthropic-json-schema-v1, temperature zero, 4096 output tokens, 48,000-byte full-payload cap. No tools/fallback/prompt cache. Same reviewed generator/evaluator; four tiny development tasks with root=0 and width=2. Order: evidence/parallel, repository/chain, evidence/chain, repository/parallel. Fresh histories, N=1, four available service slots but only one active actor. Full public task is visible; dependency-access/physical hardware effects are not tested.

Attempt q-a3-canary. Each assignment records width, public-task hash, development parent, attempt namespace and source commit; no collision with width-16 histories. Source hashes in validation.json; 46 experiment tests pass offline. Dmarz's prior design review applies within qualification scope; new engineering implementation is author-tested. Core/transfer remain closed.

## Protocol

At most five calls per case: plan, one semantic/plan repair, two work turns and integration. Ordinary successful path uses four. Deadline 600 seconds/case, integration reserve 60. Schema API rejection, invalid JSON/schema output, truncation, refusal, transport/accounting/claim failures or unacknowledged terminal publication stops this bounded canary. A substantive wrong final answer remains an outcome and does not exclude later cells while infrastructure is healthy. No transport retries or fence extraction.

Original canonical Q1 ledger retains all historical calls and the unresolved hold. Latest exposure $0.328990; verify fresh before dispatch. $1.25/episode and $5 attempt sublimits are atomically enforced in that SAME ledger, beneath its original $20 cap. Maximum 20 calls at $0.220480 reservation each bounds additional exposure at $4.409600 under the configured token prices; all previous exposure remains counted. No replenishment or separate authority.

Before dispatch: fresh exclusive registered-host claim, no prior worker, matching clean source/runtime, exact immutable plan URL/commit and public metadata verified after propagation, and per-condition TLDR check before any model call. Only dedicated Swarm Lab Keychain credential under SWARM-LAB-CREDENTIALS.md, verified SSH stdin, separate project-bound routing metadata, no secret persistence/logging. Fresh config, receipt, outputs and process record. Retain every assignment including unstarted cases.

Promotion requires all four correct on-time final artifacts, expected plan/work/integration paths, valid accepted outputs, complete accounting and acknowledged/readback-verified artifacts. This supports preparing a separately admitted full-width baseline only; no automatic further stage. An allowed semantic plan repair is charged and visible. A failed canary requires a post-mortem, not automatic restart.

## Metrics

Assigned/started/terminal/unstarted; per-phase raw JSON and schema validation; verified success/quality; latency including grammar compilation/hosted queueing; calls and usage; settled/held cost; complete executed-artifact publication separately from full-batch completion. Schema hashes are recorded in reservations. Evaluator truth never enters actors. Four development cases provide no statistical reliability or size-effect claim.

## Visualization mapping

Actual plan, service, worker and integration intervals feed the existing replay and static table. Schema/format failures are event markers; empty work phases stay empty. No inferred GPU utilization or invented motion. Publish original assignment, trace, outcome and replay; preserve failed cases and missingness.
