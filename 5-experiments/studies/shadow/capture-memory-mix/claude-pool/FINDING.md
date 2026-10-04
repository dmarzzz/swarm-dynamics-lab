# Memory-mix on Claude: blocked qualification, no behavioral result

- **evidence_confidence: 0/4 (Untested)** for the claim that one-third short-memory survivors rescue a captured Claude population relative to all-full memory.
- **sample_size_summary:** Observed: 0/4 paired roots, 0/8 scientific episodes. Qualification: 12 assigned, 8 attempted, 0 valid, 4 unstarted; 20 failed HTTP attempts. Planned: N12, six survivors, two arms, 20 rounds, 456 scientific decisions.
- Assessor: shadow/sol-mix-astra, 2026-10-04. Saved evidence: [recovery-summary.json](recovery-summary.json), [assignments.csv](assignments.csv). Source cohort: `8c4ce07e1597e9be8316c940ff91027701efbe4f`. Same-owner recovery, not independent research review.

## Finding

**The historical pool attempt never obtained a Claude completion.** Between 22:49:11Z and 22:51:07Z on October 4 it made 20 HTTP attempts requesting `claude-sonnet-5-5`: eight HTTP429 rate-limit errors and twelve HTTP503 broker-unavailable errors. All 20 have terminal records. No response contains a returned model identifier, token usage, cost, text choice or valid decision. Qualification stopped. None of the eight planned paired scientific episodes started.

Consequently there is **no estimated mixture effect, no confidence interval and no evidence for or against rescue**. The logical missing-outcome bound on mix-minus-full change is [-1,+1], not an empirical interval. Zero observed roots is not a zero effect. No Opus or OpenRouter request was made by this lane. Astra recovered and analyzed saved evidence; it did not serve as an experimental agent.

## Intended comparison, not an executed study

Four fixed scripted captured roots (tasks160-163, seed1) from freeze-claude were to be cloned to all-full memory versus a mixture with two of six honest survivors retaining only their latest heard name. The six committed agents were removed from the initialized N12 population. Paired existing schedules run for20 rounds. Raw partner-name histories are chronological and contain no separate true-last-event answer field. No roots, prompts or schedules were replaced during recovery.

The primary endpoint was the root-paired difference in original-convention share change, mix minus full. Planned uncertainty was a10,000-sample whole-root bootstrap, seed7. Four roots give weak, discrete precision and cannot establish general swarm behavior. The retained scripted reference gives **-0.0417 [-0.250,+0.125]** under fixed draws; its500-draw-per-root/arm average contrast is approximately+0.007. These are historical scripted outputs, not Claude observations, and do not predict a clear rescue in this reduced fixture.

The parent pilots were model/policy-specific. The prior reading-rule result used **GPT-4o-mini**, not Claude, and explicitly supplied the true last event. It does not establish competence for this unqualified raw-history prompt. The reduced N12 fixture also does not inherit the original N24/round50 freeze regime.

## Reconciliation

| Unit | Planned | Started | Valid | Failed | Unstarted |
|---|---:|---:|---:|---:|---:|
| Qualification assignments |12|8|0|8|4|
| Physical qualification attempts, including retries |at most1000 overall|20|0|20|not applicable|
| Scientific episodes |8|0|0|0|8|
| Scientific decisions |456|0|0|0|456|
| Paired scientific roots |4|0|0|0|4|

Qualification assignments0-3 each received four attempts; assignments4-7 each received one; assignments8-11 received none. The twelve rows in qualification.json must not be mistaken for twelve attempted model decisions. Every request ID reconciles to exactly one terminal response, with no unresolved in-flight request in the saved journal.

## Recovery found admission defects, not just an outage

1. **Public preregistration is not established.** The old PREREG.md claims it was pushed before calls, but was untracked when recovery began. The published source commit contains only run.py and scripted-reference.json. The original document is now preserved unchanged as a recovered historical artifact; this publication is retrospective and does not repair the missing pre-run registration.
2. **The old qualification gate admits copying.** It accepts11/12 parseable answers without a competence/non-copying requirement. An offline deterministic last-item copier passes12/12 while disagreeing with the history majority on all8 conflicting fixtures. This demonstrates a gate defect, not observed Claude copying. Coordination does not have an objectively correct majority answer; nevertheless parseability alone cannot support the intended non-copying qualification.
3. **No independent pre-review was located for this lane.** A same-owner recovery audit cannot supply the repository's different-researcher review. The parent hypothesis remains proposed, not accepted. The review waiver for Vishesh's studies does not apply here.
4. **The old runner has no dollar-reservation ledger.** Usage and dollar charges are unknown for all20 historical attempts. Request-count limits are not a USD5 cap.
5. **Historical trace coverage is incomplete.** Requests record assignment metadata, requested model and history length, but not the actual serialized payload. Prompts can be reconstructed from frozen source and fixtures; reconstructed inputs must not be presented as proof of delivered bytes.

The old runner remains frozen for audit and must not be relaunched. Recovery made **zero new model calls**, including zero pool health probes and zero OpenRouter calls. Transport health could not resolve the missing review, budget and qualification requirements, so probing would have added exposure without admitting a study. No credential was read for model dispatch.

## Costs and resources

- Historical actual dollars and input/output token counts: **unknown**, not zero. Twenty terminal errors lack billing receipts. Twelve broker errors state they occurred before an upstream request; that text is not a complete billing ledger.
- Recovery incremental experimental API spend: **USD0**, because no new model requests were sent.
- The authorized recovery lane ceiling is **USD5**. AllUSD5 is held administratively unavailable pending reconciliation of inherited exposure; admissible new spending isUSD0. This hold is **not** a verified upper bound on historical billing and is not a fabricated pre-dispatch reservation.
- No factory, freeze experiment, other lane's USD10 allowance, fleet allocation or shared submission document was changed. No matching worker remained active at recovery inspection. No infrastructure was provisioned.

## Reproduce without network or credentials

```sh
python3 5-experiments/studies/shadow/capture-memory-mix/claude-pool/audit_saved.py --check
```

The stdlib auditor does not import or execute the experiment runner. It reconciles every assignment/attempt, checks the original source bytes and native hashes, verifies short-agent selection and the456 planned decisions, and demonstrates the copier-admitting gate. It is a separate arithmetic implementation by the recovery owner, **not independent researcher validation**. [Post-mortem](POSTMORTEM.md), [setup](SETUP.md), [recovery assessment](RECOVERY-ASSESSMENT.md).

No model trajectory or animation is available because no model episode started. Tables are the honest static visualization fallback; missing trajectories are not drawn at zero.

## Submission-ready paragraph

A bounded Claude Sonnet5.5 check of all-full memory versus one-third short-memory survivors did not reach scientific evaluation: all20 qualification HTTP attempts failed (8 rate limits,12 broker-unavailable errors), yielding no valid model decision and0/4 paired roots. Recovery also found that the original parse-only qualification would admit a last-item copier, public preregistration was not established, and historical dollar usage was unreceipted. The lane was therefore closed without additional calls rather than weakening qualification or reporting a missing comparison as a null. Memory-mixture rescue on Claude remains untested.
