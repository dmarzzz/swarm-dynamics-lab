# Amendments to the scarcity plan

Dated 2026-10-04. Recorded by dmarz/pipeline-scarcity before any code of this study existed and before any run.

This study implements [the scarcity plan](../sybil-scarcity-plan/README.md) (draft v1, with its [setup record](../sybil-scarcity-plan/SETUP.md) and [design data](../sybil-scarcity-plan/design-plan.yaml)). The plan directory is frozen and is not edited. Everything the plan fixes stays as written except the items below.

## Source of these amendments

Amendments 1 to 6 were given to dmarz/pipeline-scarcity by the pipeline lead dmarz/pipeline in its build brief of 2026-10-04. The brief states that they were relayed to dmarz/pipeline by dmarz/fleet-monitor, the session dmarz is directing. This file records them as relayed. It does not quote dmarz and adds nothing to what was relayed. dmarz/pipeline-scarcity has not spoken with dmarz.

## Amendments as relayed

1. **Synthesizer.** Every paid stage uses `claude-opus-5-5`, not `claude-haiku-4-5-20251001` ("Opus for everything"). Consequences: no temperature is sent (the model rejects sampling parameters); thinking is always on; depth is set with `output_config.effort: low`, the setting of the sibling Opus studies [sybil-scale-xl A1](../sybil-scale-xl/AMENDMENT-A1.md) and [sybil-specialists-opus](../sybil-specialists-opus/README.md); the output limit is 8,000 tokens because thinking counts against it; list prices are USD 4 per million input tokens and USD 20 per million output tokens. The plan's "no thinking, temperature zero, 500 output tokens" no longer applies.
2. **Interface probe.** A one-call probe, P0, is the first paid step. The plan had no probe. P0 uses one clean packet built from engineering root 7790, which is neither an S1 root nor a Q0 root.
3. **Hard call caps.** P0 1, Q0 48, S1 1,440, study total 1,489. No retries and no slack. The plan's candidate cap of 1,550 attempted calls is replaced.
4. **Dollars.** Dollars are not the gate for these runs. The ledger still stops at a cap that the builder computes and justifies; see "Dollar cap" below.
5. **Launch routing and review.** The run is launched only by the orchestrator from the private run queue, after a same-researcher check by dmarz/fleet-monitor. Cross-researcher review is waived by dmarz for these exploratory runs (as relayed). The run has not been independently reviewed and no document of this study may say that it was.
6. **Preparation.** The plan's "NO START" status is superseded for preparation by the build brief: writing this package, its offline tests and its rehearsal. The package itself launches nothing. No stage of this study has run and no model call has been made.

## Contract additions (dmarz/pipeline, 2026-10-04)

These come from the [ready-chain contract](../pipeline/READY-CHAIN.md) and two follow-up messages from dmarz/pipeline to this builder on 2026-10-04. They are engineering rules of the pipeline, not statements by dmarz.

- Stages S0, P0, Q0 and S1 run as one chain. Each stage is admitted by a software gate on the previous stage at the same source hash.
- The adapter drops both `thinking` and `redacted_thinking` blocks before it requires exactly one text block.
- Caps and timeouts are part of the hashed design, so they are sized for the whole chain before the first stage.
- Run outputs go to the directory named by `STUDY_RESULTS_DIR`.

## Builder choices that differ from the plan's proposed limits

The plan called its limits proposals. These values are set by dmarz/pipeline-scarcity and are open to the lead's review.

| Item | Plan proposal | This study | Reason |
|---|---|---|---|
| Requests in flight | 2 | 4 | The build brief expects 4, the setting of the sibling Opus studies. |
| Request timeout | 120 s | 300 s | Thinking is on and a timed-out call stops the stage, because there are no retries. The scale-xl probe took 2.9 s on a packet of this size. |
| Stage timeout | 14,400 s | 14,400 s | Unchanged. |
| Chain timeout | none | 18,000 s | New: the contract needs one limit for the whole chain. |
| Dollar cap | USD 40 known plus USD 150 reserved | USD 390 on settled cost plus open reservations | See below. |
| Reservation basis | request bytes | input tokens from the free counting endpoint, plus 2% and 64 tokens, plus the full output limit | Same accounting as sybil-scale-xl A1. |
| Scripted stage | S0 | S0, with the same 168 outputs | Unchanged. |

### Dollar cap

Basis: a 486-report packet in this report format measured 23,536 Opus 5.5 input tokens and 38 output tokens in the sybil-scale-xl probe ([q0-a1 pre-run file](../sybil-scale-xl/reviews/q0-a1-pre.md)). This study's packets have the same number of reports and the same fields.

- Expected input: 1,489 calls × 23,536 tokens = 35,045,104 tokens × USD 4 per million = USD 140.18. Of that, S1 is 1,440 × 23,536 = 33,891,840 tokens = USD 135.57, Q0 is USD 4.52 and P0 is USD 0.09.
- Expected output: 1,489 calls × 40 to 500 tokens × USD 20 per million = USD 1.19 to USD 14.89.
- **Expected total: about USD 141 to USD 155.**
- Worst case per call: the reservation, which is (23,536 × 1.02 + 64) input tokens × USD 4 per million + 8,000 output tokens × USD 20 per million = USD 0.0963 + USD 0.1600 = USD 0.2563.
- Worst case for the chain: 1,489 × USD 0.2563 = USD 381.60. This needs every call to use the whole 8,000-token output limit.
- **Cap: USD 390**, the worst case plus about 2%. With this cap the call caps always bind before the dollar cap, so the dollar ledger cannot stop a chain that stays inside its call caps and output limit. The cap cannot be raised after qualification without repeating S0, P0 and Q0, because it is part of the hashed design.

The standing directive in [dmarz's README](../../README.md) sets USD 500 for model spend across all dmarz experiments. Other dmarz runs of 2026-10-04 draw on the same allowance. Amendment 4 says dollars are not the gate for these runs; this builder cannot reconcile the shared allowance and leaves that to dmarz/pipeline and dmarz/fleet-monitor before the run is queued.
