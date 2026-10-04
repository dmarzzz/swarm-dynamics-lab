# C4-S0 post-mortem: reliable execution, invalid qualification

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-regrowth-docs; source `1adeb586` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — C4 qualification contains expected-label leakage; its perfect Jev score does not establish clean capability. Basis: Actual serialized inputs and all 180 responses were reconstructed. Fully correlated Qwen errors are descriptive contaminated outcomes; S1 was withheld.
- **sample_size_summary:** 60/60 synthetic report units, four repeated forms/class; 180/180 calls, zero transport failures. Expected labels leaked in names: no valid clean qualification inference. S1 not run; calls are not independent domains.
<!-- experiment-evidence:end -->

**PI verdict: stop before S1.** The numerical qualification passed, but the instrument violated its declared information boundary. All qualification method names included their expected class. The unexecuted S1 source likewise includes scenario-family names in method identifiers. Jev's 60/60 is therefore not uncontaminated evidence of capability. C4 remains a preserved failed qualification, not a rescued success.

## Observed results and native traces

60/60 assigned reports completed; 180/180 calls terminated (120 Qwen,60 Jev), with no transport/schema failures. Runtime 168.42 seconds; API USD 0.00112665. Jev 60/60; Qwen A 40/60 and B 40/60. The variants agreed on every report, including all 20 errors, so the cascade referred nothing and retained all 20wrong answers. These are contaminated descriptive outcomes, not a validated savings estimate.

Every qualification miss was reviewed: all 20 SUPPORT cases received REFUTE from both Qwen variants. ExampleC4-S0-SUPPORT-7 says the method “outperformed baseline accuracy”; both raw Qwen answers say REFUTE while Jev says SUPPORT. Four matched successes spanning REFUTE/UNCERTAIN were also read. All180payloads and parsed outputs were recomputed. The first observable defect is in the scenario serializer before the model call; the parser faithfully retained the model output. Label leakage is proven. Whether either model used the leaked token, and why Qwen inverted SUPPORT, remain unknown. No hidden-reasoning diagnosis is claimed.

The nominal option-order variants differ as specified, but are empirically fully dependent here. Agreement is not calibrated confidence. At zero referrals the same-count random control also selects nobody; it cannot distinguish routing skill on this cohort.

## Design assessment and repair decision

The focused question, paired controls, explicit missingness, fixed sample and original cost ledger are strengths. The central weaknesses are label/family leakage, same-author synthetic scenario construction, repetitive qualification templates and weak confidence in the disagreement signal. Passing serialization-field allowlists did not establish information isolation inside text. The existing tests missed this.

Accepted repair: construct opaque identities without label/family inputs and counterfactually mutate evaluator-only metadata while holding semantic claim/report fixed; the entire serialized actor payload must remain unchanged. Keep class vocabulary in output instructions—globally banning SUPPORT would test the wrong property. Make baseline comparisons explicit. Preserve the executed source and all adverse outcomes. Do not change prompts, thresholds or scenario labels to make this run pass.

[C5 proposal](../c5/PLAN.md) is one 60-case metadata-blind qualification, no main stage or automatic retry. Five new offline development tests cover identity independence, complete Qwen/Jev payload invariance, meaningful comparison text, enum-order-only variation and rejection of an automatic S1. No C5 assignment set or provider call has been materialized. The proposal needs its changed-plan decision before resources or inference.

## Resources, evidence and release

The complete 123,791-byte native archive was uploaded and downloaded with SHA256 `7bb4c2dc37fe4ee6d080760cb2e775d521a3f77760e090fb51794300038e0cf4`. The original 2,179 ledger entries are unchanged; total 2,239, settledUSD 0.042017472 plus USD 0.001344 historical uncertain exposure. Remaining originalAPI allowanceUSD 0.056638528; no budget reset or new VM. Remote authority is closed, the original local ledger restored, ephemeral credential absent, study services stopped, and exclusive allocation released through the fleet workflow.

[Measured chart](https://swarm-live.pages.dev/api/a/healing-helping-hands/C4-S0/outcomes.png) · [Raw request/response journal](results/C4-S0/calls.jsonl) · [Structured eleven-dimension review](results/C4-S0/scientific-post-mortem.json) · [Archive receipt](results/C4-S0/archive-receipt.json).

Execution, numerical qualification, scientific validity, reporting and cost are separate: completed / passed / invalid / published / reconciled. No S1 launched. This post-mortem completes the C4 cycle; it does not authorize another attempt.
