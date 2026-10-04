# C5 proposal: metadata-blind qualification

Status: proposed only; not approved, allocated, registered for execution or run. This is a concrete next-plan decision after [C4's invalid qualification](../c4/S0-POST.md), not an automatic repair attempt.

## TLDR

Qualify Qwen and Jev on 60 new synthetic instances drawn from 12 authored class/form templates (not 60 new semantic problems or independent families) whose method names cannot reveal evaluator labels or scenario families. Preserve C4's evidence and the original ledger. Run only this qualification, then review all misses and decide whether any main experiment is worthwhile. No automatic S1, repeated qualification, prompt tuning or broader swarm claim.

## Question and prediction

Does the corrected metadata-blind instrument produce complete valid responses and meet the original Jev clean-task floors? Report Qwen accuracy and correlated agreement errors without treating agreement as confidence. A pass establishes only bounded clean-task readiness. A failure ends the attempt and prompts trace analysis. The changed wording and names mean this is not a randomized causal estimate of how much leakage affected C4; no before/after capability claim.

## Setup

One S0: 60 new balanced instances of 12 authored class/form templates, 20 each SUPPORT/REFUTE/UNCERTAIN, four authored surface forms per class. The independent evidence is a finite synthetic fixture screen, not 60 sampled real-world domains. No powered safety claim. This allocation preserves the original qualification scope while removing the defect; it is not a larger search for a favorable result.

The new opaque method identifier is a hash of split and index only; label/family are not inputs. Label allocation and call order use distinct fixed seeds. Method/test identifiers contain no evaluator metadata. Reports explicitly compare against baseline; correct-answer counts refer to the same questions. Truth/family/IDs remain evaluator-only fields. C5 assignments are generated only after prospective registration and admission; offline tests use development indices only.

Agent configuration stays Qwen3:0.6B at the pinned digest and Jev1.13 at the pinned TypeSafe snapshot. Qwen receives claim/report, fixed seed 9400, temperature 0, no reasoning output, max 32 output tokens; A/B differ only in schema enum order. Jev receives claim/report and the unchanged criteria, never Qwen output. All actors stateless; alternating A/B order and counterbalanced Jev order. Both Qwen passes are dependent re-evaluations, not independent agents. No model-selected tools or external memory.

## Controls and acceptance

Use all three calls per report, retaining Jev as the stronger reference. Numerical qualification remains complete valid outputs for all 180calls, Jev >=51/60 overall and >=14/20 per class. Qwen competence is reported, not silently substituted for Jev's floor. Scientific admission also requires the actual saved payloads to pass the metadata isolation audit; numerical success alone cannot override a context defect.

Five offline tests now check opaque-name independence from truth, exact Qwen/Jev payload invariance under evaluator-only metadata mutation, semantic comparison presence, enum-order-only variation, and explicit rejection of a C5 main stage. Output-label vocabulary in instructions/schema is necessary and is not globally banned. No future S1 is designed or authorized here; C4's family-bearing main-stage fixture names may not be reused.

## Metrics

Assigned/started/terminal/graded counts; raw-label and payload-hash reconstruction; each model's confusion matrix/per-class accuracy; A/B disagreement, accepted-wrong cases; actual request tokens/time/cost. Review every qualification miss and every failure class plus declared matched successes. Preserve malformed-response traces and missingness. Publish a warning-marked or qualified chart and recorded report inspector, with all adverse cases visible. No 200-agent cooperation claim.

## Resource envelope

At most120 Qwen calls and 60 Jev calls, concurrency one,15-minute model stage, one existing exclusive approved-account 4 CPU/8 GiB host for at most one hour including closeout. No new paid VM under this proposal.

Retain the original ledger: 2,239 entries, USD 0.042017472 settled plus USD 0.001344 unresolved historical exposure. Original cumulative USD 0.10 cap and 2,671 request ceiling remain. The proposed60 Jev calls would raise total entries to at most 2,299, reassigning 60 of the 432 unused approved slots to this changed qualification only after owner approval. No top-up. Carry C4's USD 0.00112665 into the same USD 0.03 repair-cycle envelope, leaving USD 0.02887335 under that envelope. Stage admission ceilingUSD 0.004 with worst-case per-request reservations against both remaining limits; stop if either cap would be exceeded. Projected means are not guaranteed costs. Local Qwen seconds/tokens and inherited fleet occupancy are reported separately from API dollars.

## Protocol

1. Owner reviews this bounded changed-plan proposal and the implemented/tested scenario repair. No self-authored approval receipt.
2. If approved, integrate a distinct C5 namespace into the same native transport/auditor and original cumulative ledger; reserve only this 60-call scope. Freeze tested source/plan, register and read back the condition TLDR. The existing C4 direct-launch authority does not silently authorize C5.
3. Obtain a current exclusive existing approved-account allocation, verify account/workload/claim/runtime/model/public source, and securely transfer the original single-writer ledger once.
4. Launch one S0, no retry after ambiguous dispatch. Any systematic transport/schema failure stops the stage; preserve failed/not-run assignments and reservations.
5. Reconcile all 180possible calls, inspect actual actor-visible context before awarding qualification, publish the scientific post-mortem and measured visuals, verify archive readback, restore ledger authority and release the machine.
6. Stop. Any main experiment, prompt change, extra sample, machine charge or retry needs its own concrete decision. A valid adverse agreement result may end this line.
