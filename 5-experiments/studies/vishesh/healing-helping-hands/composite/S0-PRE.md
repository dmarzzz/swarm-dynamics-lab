# C1-S0 pre-run assessment

2026-10-04 UTC. Self-assessment by vishesh/codex-regrowth-docs. **Diagnostic-only, subject to fresh runtime, public-page and budget receipts before dispatch.** No model observations have been collected. Previous post-mortem: ../practical/POST-02.md, read before design.

## Decision and design

Qualify the complete Qwen 0.6B + Jev agent, preserving the user's authorized Laya replacement. Compare paired Qwen-only and Jev-only on the same 60 reports. Jev-only is the meaningful inexpensive control; no assertion that a composite is better merely because it beats Qwen. Qwen's standalone score does not gate the composite. Jev-only and composite must each reach 51/60 overall and 14/20 each class, with all responses valid. Source-based correctness is separate from response validity.

Cases are balanced across support/refute/uncertain and include numeric comparisons, ties, negation and missing measurements. Six template families per class reused across names/values; this is a competence screen, not independent generalization evidence. Fresh C1 fixtures replace previously tuned screens. Qwen and Jev actors receive only projected claim/report fields, plus the Qwen label in the composite. Expected labels and downstream evaluator state never enter requests. Qwen wire parity with the previous typed extraction prompt is tested.

## Bounds and stopping

60 Qwen plus 120 Jev calls, concurrency one, 900-second worker limit, 30-second call limit. Stop on transport/schema failure and retain every assigned row as completed/failed/not-run. No automatic retries. Existing cumulative Jev ledger has 720 historical calls and USD 0.013004124 actual spend; remaining USD 0.086995876 under the unchanged USD 0.10 cap. Local relay reserves full-context worst case and only settles validated usage. C1 stage slots prevent alternative-proposal retries; frozen input hashes constrain outbound content. The original ledger is mandatory, never copied to independent spending workers. Credential stays in its approved local file and is never sent to the fleet host.

## Evidence before dispatch

16 new offline tests and 44 existing tests pass. Coverage includes truth projection, treatment pairing, Qwen wire parity, option rotation, class floor, missing outcomes, complete-composite admission despite bad Qwen, anchoring arithmetic, frozen relay allowlist, duplicate/uncertain spending and stale/missing admission checks. The public page displays the C1 TLDR, immutable PLAN.md URL and actual composite protocol. The initial registration was at edbc2e3f130ab41d01f781574c1911a89b80e2a2; freeze/register the completed instrument revision before execution.

Provider metadata rechecked 2026-10-04 at https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints: TypeSafe-only snapshot typesafe/jev-1.13-20260917, prompt USD 0.000000042/token and zero completion price. Relay verifies metadata again at startup; any drift blocks launch.

## Visualization mapping C1 / S0

Run ID healing-helping-hands/C1-S0, paired three-model screen. Live acknowledged counts of completed/assigned reports; retain complete observations and request journal. Final three-panel confusion figure includes missing outcomes, correction/damage/anchoring counts and assigned denominator. No animation of unrelated qualification cases. Synthetic missing/error fixtures are explicitly labeled SCRIPTED — NOT MODEL EVIDENCE. S1's planned 30-frame atlas view is checked using fabricated unit states, with damage/reconnection boundaries and no calls.

## Remaining admission actions

Fresh exclusive fleet claim, deployed source/dependency/model-digest checks, current shared budget receipt, immutable exact-source registration/readback, final go/no-go and five-minute admission receipt. Research-01 was read-only checked idle, but agentops refused the new claim because another experiment's expired claim still has status running. Do not override that claim or launch without resolution. No claim was created and no model/server was started. User was asked whether to retain fleet requirement or explicitly permit this run on the Mac; no exception is presumed.

## Allocation amendment before C1 inference

The user explicitly authorized new machines on Dmarz's established account. Newly installed credential matched all 12 known fleet hosts; account active. Only sim-healing-c1 was created from the original empty Vishesh infrastructure state. Fresh exclusive claim vishesh-healing-qwen-jev-c1 merged through fleet PR 145, three-hour expiry; provisioning PR 143 merged. Runtime setup is in progress. This supersedes the historical allocation blocker and withdraws the obsolete provisioning request. Model calls remain zero for C1. Refresh and record claim, idle workload, exact deployed source, model digest, public plan and cumulative ledger immediately before worker dispatch.
