# Healing Helping Hands C4: selective helping

Status: prospective draft, owner approval of this material update pending. Parent: [C3 assessment](../composite/C3-S1-POST.md). No machine claim, model calls or experimental sweeps are authorized by this document alone.

## TLDR

Can two cheap Qwen readings identify which reports need Jev's help? Accept Qwen when two option-order variants agree; otherwise ask Jev. Compare with Jev on every report, Qwen alone, and a control that refers exactly the same number of reports using a fixed random ranking. Measure missed errors against saved Jev calls. Agreement can be confidently wrong; that is a primary failure mode, not grounds to tune the routing rule after seeing results. This is a synthetic routing feasibility study, not evidence that a swarm beats a database.

## PI decision and changes

C3 established healthy native execution and a valid null: the always-reviewed composite equals Jev, while the strong central index wins the architecture comparison. Do not repeat that claim. Retire the always-reviewed composite as the main treatment. Change the decision from adding accuracy to allocating a scarce stronger model. Retain Jev-only as the strongest semantic control. Do not change the old architecture code, reinterpret old results or launch another capacity sweep.

Both Qwen passes will receive the exact claim AND report. C3's Qwen adapter omitted the claim from its prompt, harmless only under its narrow all-accuracy task. Broader distractors require this correction and fresh qualification. Two passes differ only in schema enum order; temperature, seed, prompt and report are identical. This is an option-order stability signal, not independent votes or calibrated uncertainty. Every actor is stateless. No truth, family, routing priority or operating-assistant context reaches the models.

## Question and prediction

Primary contrast: selective-referral assigned error minus budget-matched random-referral assigned error. Negative favors informative routing. Safety contrast: selective error minus always-Jev error. Resource endpoint: fraction of reports that avoid Jev; report the extra Qwen pass and measured token/time overhead. A useful descriptive result needs at least 25% fewer Jev consultations, no more than 2 percentage points additional error versus Jev, and lower error than the matched referral control. Report all three criteria, not a single success badge. Qualification may fail; correlated Qwen errors may make routing uninformative; savings may disappear after including Qwen cost. All are useful outcomes.

## Scenarios, samples and holdouts

S0: 60 fresh balanced engineering fixtures, four qualification-only surface families, 20 per class. Jev must score at least 51/60 overall and 14/20 each class, with no invalid/missing responses. Qwen competence and agreement errors are reported but do not gate admission. Require complete valid outputs from both Qwen variants. S0 is qualification, not threshold tuning.

S1: 12 declared semantic families, 36 instances each, 12 each SUPPORT/REFUTE/UNCERTAIN: 432 paired reports. Families cover counts, percentages, error rates, before/after comparisons, explicit no-improvement, repeated tests, uncertainty language, target subgroup, superseded evidence, irrelevant metrics, untested expectations and named-target distractors. Inputs are generated only after admission in a fresh namespace; development and S0 instances cannot be reused. No external or clinical validity claim. A new family is not an independently sampled real-world domain.

Treat the 12 authored families as descriptive strata, with numeric/surface instances nested inside. Report every family, equal-family macro averages, all paired counts, and leave-one-family-out sensitivity. No binomial CI pretending 432 independent language tasks; no confirmatory non-inferiority claim. This n supplies 36 challenges/family at an affordable bounded scope, not validated power for a 2-point margin. Broader natural-text generalization remains untested.

## Paired arms and collection

For each report collect Qwen A, Qwen B and Jev-only once. Counterbalance whether Jev occurs before or after the Qwen pair. Qwen A/B order alternates. Jev never sees either Qwen answer; it is invoked during collection for paired controls even if the proposed deployed cascade would skip it. Distinguish actual experimental spending from counterfactual deployment consultations. Do not describe this as observed production cost savings or end-to-end live cascade latency.

Arms: Qwen A; always-Jev; agreement cascade (A if A=B, otherwise Jev); matched referral (Jev on k reports per family, chosen by frozen hash rank, otherwise A), where k equals that family's disagreement count. The matched control is a batch allocation benchmark, not a deployable online router. The rank does not use labels or truth. Analyze an additional zero-information expected-error benchmark by averaging all uniformly random subsets of size k analytically, avoiding lucky choice of a single random mask.

All reports have prewritten assignment IDs and a terminal status. A systemic transport/schema failure stops the stage, retains ambiguous reservations and marks remaining assignments not-run. No repeated POST after uncertain dispatch. No substitution, threshold selection, case exclusion or extra repair cycle. Missing outputs score incorrect in assigned denominators; show completed-only values separately and bound unresolved paired effects. Any missing family prevents a complete S1 verdict.

## Metrics and visualization

Report confusion/per-class accuracy, Qwen disagreement, accepted-but-wrong count/rate, error-detection recall, Jev referral fraction, paired safety delta, matched-control delta and their per-family values. Actual request bytes/hashes, raw sanitized responses, time, tokens and costs are retained. Jev charges include all experimental controls. Counterfactual cascade calls are explicitly derived from this response tape.

Use an error-versus-consultation plot, per-family table, and recorded report tiles grouped across 200 logical curator IDs. Tiles show the report's routing and correctness state, never invented dialogue or diffusion. An inspector shows both model answers, referral decision and post-hoc truth. Failed/not-run tiles remain visible. C3's architecture animation stays available as historical evidence; C4 does not rerun architecture worlds or claim that the tile layout demonstrates emergent cooperation.

## Resource envelope and stopping

One S0 then, only after its post-mortem and fresh admission, one S1. At most 984 Qwen calls and 492 Jev calls total; no retries/repair allowance. Proposed cumulative Jev request ceiling changes from exhausted 2,179 to 2,671; this needs explicit approval and is not an automatic reset. Original USD 0.10 inference cap remains. Completed cost USD 0.040890822 and uncertain C1 exposure USD 0.001344 remain; USD 0.057765178 available. C4 incremental API ceiling USD 0.03, with serial worst-case reservations against both incremental and original caps. Expected cost based on C3 is about USD 0.01, not a guarantee. The ceiling can stop collection early; a full worst-case 492-request reserve exceeds it, so S1 admission must assess S0 usage and projected completion without waiving either cap.

Minimum one exclusive 4-CPU/8-GiB existing Dmarz-account fleet machine; pinned Ollama/Qwen runtime, concurrency one. S0 wall limit 15 minutes, S1 60 minutes, claim at most three hours including archive. Prefer existing idle capacity. A new paid VM requires verified remaining original infrastructure authority; do not assume the old ceiling replenished. Worker-local relay, detached supervision, atomic cache/usage commit and read-only recovery remain mandatory. Do not transfer credentials or claim a machine while plan approval is pending.

## Protocol and acceptance

1. Complete PI review, scenario definitions, routing/reference tests, missingness tests and fail-closed C4 admission. Preserve C3 source/results.
2. Owner approves this concrete plan, including the +492 request envelope; no increase to dollar cap requested. Bind approval to the plan digest. This is distinct from the waived independent-researcher review.
3. Finish and validate C4-native collection/relay allowlist, figures and supervisor integration before allocation; do not reuse the C3 launcher with fabricated C4 receipts.
4. Register immutable condition-specific plan and TLDR; verify public readback. Refresh actual account, inventory, workload, exclusive claim, source, model, ledger and expiry checks.
5. Run fresh S0; reconcile calls/cost, post-mortem and qualify. Admit unchanged S1 only when its projected spend and runtime fit remaining caps.
6. Run once; audit from raw responses, render all outcomes, verify publication, invoke operations finalize and complete the scientific rubric. Stop workers and release only after durable archive.
7. End on a valid adverse/null result. A justified material successor gets a new prospective plan and owner decision; 'rinse and repeat' is not unlimited inference or automatic tuning until positive.

## Design transfer — 2026-10-04

[Lessons from Dmarz’s recent studies](DESIGN-TRANSFER.md): specific controls, measurements and next-design options. Prospective only; current run contracts and approval status are unchanged.
