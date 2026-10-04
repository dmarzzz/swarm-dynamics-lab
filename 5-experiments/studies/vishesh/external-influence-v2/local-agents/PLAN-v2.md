# Local agents variant: bounded output-contract repair

Prospective amendment, 2026-10-04 UTC. This follows PLAN.md and the preserved Q0/Q1 failures; it does not relabel either attempt. Written before repair implementation. The owner-authorized local pilot remains exploratory; no cloud provisioning or paid inference.

## TLDR

Can a small local model perform the existing nine-agent task when its output grammar enforces the task's public constraints? Q0 0.6B failed candidate coverage in all six teams; Q1 1.7B completed three teams, with two correct, and failed citation validation in three. Q2 uses 1.7B with actor-visible candidate counts/names, allowed citation IDs/counts and numeric ranges enforced in its schema, preserving the actual task, prompts, peer protocol and evaluator. Six new clean/superior qualification cases measure validity and correctness; only a pass unlocks the historical 50-case comparison. This changes backend/schema enforcement as well as model relative to Haiku, and is a development repair, not an isolated causal test or evidence of broad superiority.

## Question and prediction

Will enforced output constraints eliminate incomplete-candidate/invalid-citation failures without substituting answers? Predict fewer structural failures, but make no prediction that decision quality improves. Correct structure cannot repair arithmetic or evidence interpretation. If complete teams still fail clean competence, conclude that this configuration is unsuitable as a drop-in replacement for this instrument and stop broad escalation.

## Setup

Qwen3 1.7B, installed checkpoint digest 8f68893c685c3ddff2aa3fffce2aa60a30bb2da65ca488b61fff134a4d1730e7, shared local Ollama weights, M5 Max/128 GB, four concurrent episode workers, nine identities per episode. Preserve temperature0, think=false, context8192, maximum output1024, model seed17 and original SYSTEM instructions. Schema values may depend only on the supplied actor-visible brief, documents, peers and phase, never evaluator truth or the scripted template's numeric values. Require exactly four analyst entries with public candidate-name enumeration; semantic validation still rejects duplicates. Citations must be one or two IDs from the actual allowed set. Numerical fields are nonnegative, quality is 0..100; confidence 0..1 and choice is a supplied candidate or ABSTAIN. Checks retain nullable fields. No automatic repair of generated values or substitution of scripted answers.

## Protocol

Publish this immutable plan, register it on the same experiment page and verify preflight before any Q2 inference. Q0, Q1 and D0 keep their original plan URLs and records. Q2: task7204 seed31, three domains, clean dose0 and superior dose8, targeted_check, fresh verification, nine identities. Six fresh cases, up to90 calls,30 minutes, same pass criterion (all six valid, at least five correct, at least one per domain). Freeze source/config/schema and manifest before launch; unit-test permissible-ID/cardinality constraints, truth isolation, parser failures and deadline behavior without inference. Per-run TLDRs name exact conditions.

If Q2 passes, run S1 from unchanged design.yaml:50 historical assignments with qualified 1.7B and repaired schema, explicitly labeled model-plus-adapter variant. No Q2 outcome may tune those assignments. If Q2 fails with valid wrong choices, this is an adverse feasibility result: do not change the task or keep rerunning to obtain a pass. Remaining structural defects permit diagnosis and a new bounded prospective amendment, never silent retries. Q0/Q1/D0/Q2/S1 together remain limited to990 actual calls and60 minutes of model-stage execution, with no API spend. Preserve all invalid/unstarted/timeout outcomes and prohibit paid fallback. Stage gates verify source and checkpoint. A valid adverse result is a completion, not an implementation bug.

## Metrics

All-assigned valid/correct/invalid counts, failure type, harmful selections with unknown denominators, regret, citation support, calls, tokens and measured elapsed seconds. Three domain roots in qualification; historical S1 has three roots and50 dependent assignments. No significance testing or generalization claims. Q2 versus Q1 uses different development roots, so it is not a paired quality effect. If S1 runs, verify truth/corpus/exposure hashes against archived Haiku run38908910; compare exact matched assignments. Report zero API cost separately from unmeasured energy and total ownership costs.

## Visualization mapping

Reuse local-influence-v1, bound to Q2/task7204/seed31 and any gated S1 assignments. Append-only events show recorded response order and elapsed time, live public metrics, final SVG/PNG and self-contained replay. Use explicit pending, invalid, correct and incorrect states; evaluator correctness is marked and never enters prompts. No invented spatial motion. Validate terminal count and initial/middle/final states; retain reporting failures independently. Public images are a fallback; richer replay is linked from source rather than assumed embedded.

## Prior process and source

Q0 and Q1 public receipts preceded model execution; source hash5cc00e40a642a1f57dad22f2cdde8237839f96b720135d2d1c6d2bf015105c46. Exact original model-protocol/environment bytes match historical source. Author assessment only; formal confirmation remains closed. User explicitly requested local execution, overriding ordinary fleet allocation for this pilot. Current workspace was shared with other tasks, so publishing/repair proceeds from a separate checkout; this is not a second compute allocation or cloud deployment.
