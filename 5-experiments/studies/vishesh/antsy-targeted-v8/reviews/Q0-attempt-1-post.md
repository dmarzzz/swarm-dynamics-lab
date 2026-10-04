# Q0-attempt-1: the checker exceeded its execution deadline

Assessed 2026-10-04 by vishesh/codex-methods. Same-author scientific and operational review, not independent validation. Frozen execution source: `a3919814c9b6ed6cec4b7d4b6fb801d190620ba1`. The prospective [native plan](../NATIVE-Q0.md) and [pre-run assessment](Q0-pre.md) were public before dispatch. This assessment is retrospective.

## Decision

**Do not advance. Prepare a bounded execution repair for owner review.** Q0 failed operationally and did not establish qualification. The observed failure is a checker timeout, not evidence that the checker returned a wrong total. Neither a complementary-correction benefit nor correlated-error reduction can be estimated from the two completed pairs. No repair attempt or S1 was launched.

The owner-authorized direct route superseded the earlier central-only dispatch restriction for this exact Q0 scope. The existing central request was fenced before dispatch, and the existing team host was exclusively claimed. Scientific source, sample, thresholds, 40-call ceiling and zero incremental-charge envelope stayed unchanged. Host-side package/model inspection and 31 offline checks passed; those checks did not establish native latency feasibility.

## Full assignment accounting

| Scope | Observed |
|---|---:|
| Planned paired receipts / OCR calls | 20 / 40 |
| Complete pairs | 2 (train60–61) |
| Partial pair | 1 (train62) |
| Entirely unstarted pairs | 17 (train63–79) |
| Call starts / valid terminals / timeouts | 6 / 5 / 1 |
| Unstarted calls / unresolved starts | 34 / 0 |
| Hosted-model/API calls / incremental charge | 0 / USD0 |

The complete-pair analysis includes four valid outputs. The fifth valid output, primary reader on train62, abstained and remains in the partial record; it is not silently dropped from execution accounting or added to the paired efficacy denominator. The checker on train62 reached `TimeoutExpired` after **45.079 seconds**. All later assignments remained unstarted under the prespecified first-error stop. The outer manifest's `ValueError` is the coordinator's stop signal; the partial record preserves the causal exception category.

[Assignment ledger](../results/Q0-attempt-1/assignments.json), [call journal](../results/Q0-attempt-1/calls.jsonl), [partial record](../results/Q0-attempt-1/partial-record.json), [separate audit](../results/Q0-attempt-1/audit.json).

## What the actual traces establish

Five of five valid native outputs are retained privately with image and observation hashes. Replaying their saved OCR words through the unchanged field parser reproduces all five candidates; observation hashes match the native records. The public [trace audit](../results/Q0-attempt-1/trace-audit.json) contains amounts, reasons, dimensions, timing and hashes, not receipt text or operator context.

- On train60 both readers return `161000.00`, matching the evaluator reference.
- On train61 both return `17000.00`, matching the reference. Both record excluded-context handling.
- On train62 the primary returns `missing` with `excluded_context`; this is a valid abstention. The checker returns no retained answer before termination. Its inability to rescue this particular abstention is an execution observation, not a scored wrong answer.
- The first two images are 576×864; the third is 960×1706, about 3.29 times the pixel count. A larger detection/recognition workload is a plausible contributor. **The cause of the latency increase is not verified:** there are no import, initialization, detection or recognition phase timestamps. Cold initialization is included in all wall times.
- There is no retained checker intermediate output or stderr for the timeout. The launcher saves stderr only after `subprocess.run` returns normally; its timeout branch discards captured exception streams. Recovering that missing output after the fact is impossible. Do not claim to have inspected hidden reasoning or an OCR answer that was never saved.

The sixth call therefore supplies a known terminal timeout but incomplete diagnostic trace coverage. All assignment identities reconcile; the production `unique_journal: false` field actually requires the full expected sequence of40 calls and does **not** mean this run duplicated calls. The separate audit verifies no duplicates, orphan terminals or unresolved starts.

## Scientific interpretation and measurement

On two complete pairs, both readers and all five replayed policies are correct twice, with no accepted error. This is a complete-case description only. Under an independent-binomial assumption, 2/2 correctness has a Wilson95 interval of approximately34.2–100%; 0/2 accepted errors has an upper bound of65.8%. Those intervals do not correct for order-dependent stopping, vendor/layout dependence or adaptive development. They are not population safety claims.

There are zero complete pairs where the primary is missing or wrong, so both conditional rescue denominators are zero: report **not estimable**, not a zero rescue rate. Pairwise error correlation is undefined with no error variation and only two complete pairs. Different engine names and architectures are no substitute for these missing measurements.

The checker took42.09s across its two completed calls versus10.20s for the primary. These are cold-worker recorded costs, not an estimate of production service latency. The summary's policy costs exclude the timed-out partial pair; use the full call journal for actual consumption. No claim of cost savings follows from the surviving easy pairs.

## Plan and instrument assessment

The research need remains sensible: determine whether paying for a second perceptual reader yields useful corrections rather than merely more agreeing answers. The singleton and fixed-controller references are appropriate for this feasibility stage. Both readers saw the same pixels with distinct OCR engines and the same parser; there was no peer output or evaluator label in the worker input. This isolates a candidate workflow, not independent evidence sources or an LLM swarm.

The weakness is execution qualification. Package inspection plus mocked tests passed without proving that the selected CPU engine would return on the necessary image range within45s including cold load. The frozen limit was correctly enforced; increasing it after seeing this miss would change the execution contract. The 20-receipt Q0 sample was a feasibility screen with broad uncertainty, not a rare-error study. Here18 pairs are incomplete/unobserved, making even that screen inconclusive.

The native PNG/GIF correctly show2/20 completed pairs and18 uncompleted, but their green complete-case bars understate the salient timeout. The added [closeout figure](../results/Q0-attempt-1/closeout.png) explicitly shows all40 assignments and the failed call. It is a saved-data report, not an additional experimental run. All three native GIF frames decoded; the final frame and supplementary plot were visually inspected. The public run page showed failed status,2/20 progress,5 valid calls and the two original image artifacts.

## Closeout and next session

All eight original hub artifacts were downloaded on the host and their SHA256 values matched. Original OCR/image traces and private admission evidence were separately backed up before release. Worker and native child absence was verified at16:47:35UTC; the exclusive allocation was then released. No model credential was needed, no new resource was provisioned, and no additional billable infrastructure was introduced. Historical Antsy spend remains unchanged and is not reset or refunded by this result.

The operations finalize hook recorded failed execution under lowercase local alias `q0-attempt-1`, because that CLI requires lowercase slugs. Native attempt identity remains **Q0-attempt-1** everywhere in results and the hub. Its generated operational scaffold is not scientific approval; this review plus [eleven-dimension evidence assessment](Q0-attempt-1-quality.json) completes the owning session's scientific assessment.

Before proposing another native attempt:

1. Add durable phase events and timeout stream retention; test timeout, signal and crash paths offline. Preserve the original failed artifacts and source.
2. Specify whether the intended service uses cold calls or a pinned persistent reader. Do not mix the resulting timing cohorts. A warmed worker would require fresh isolation/reset and memory checks.
3. Plan a bounded latency/capability diagnostic on explicitly development-designated inputs, including the failed image size. Do not silently resize, change the timeout, use a stronger machine or spend the remaining34 calls as a retry. Distinguish diagnosis of reused train62 from fresh qualification.
4. If that diagnostic is justified, write the exact call cap, independent receipt count, image-size strata, instrumentation, latency acceptance, maximum charge and stop rules. Keep competence thresholds unchanged; retain the fresh train80–99 possibility and unopened S1 only as prospective options, not automatic authorization.
5. Obtain owner approval of that concrete changed execution plan before allocation or launch. Choose park if expected information does not justify further preparation and runtime.
