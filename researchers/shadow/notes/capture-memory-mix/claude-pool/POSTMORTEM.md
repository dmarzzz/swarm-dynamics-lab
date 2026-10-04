# Pool attempt and recovery post-mortem

2026-10-04. Assessor: shadow/sol-mix-astra, owning-agent saved-data review. **Verdict: blocked.** No scientific result. Recovery controller Astra; requested experiment model Claude Sonnet5.5. Historical source8c4ce07e; native hashes and complete counts in [recovery-summary.json](recovery-summary.json). This is retrospective closeout, not a claim that a historical pre-run review occurred.

## Separate statuses

- Execution: historical qualification stopped after20 terminal HTTP failures; recovery saved-data audit completed.
- Response validity:0 valid model responses, no completion text.
- Qualification: not established. Old threshold additionally fails an offline non-copying negative control.
- Scientific conclusion: mixture rescue on Claude untested;0/4 paired roots.
- Process compliance: gaps in independent review, published preregistration, dollar reservations and effective-input retention.
- Reporting: historical failures preserved verbatim; findings, assignment table, source hashes and repeatable checker added. No model replay exists.

## Native evidence and accounting

Read all20 request rows and all20 terminal responses, all12 qualification results and STOP.json. Every request has exactly one terminal response, no duplicate request IDs, matching metadata and requested model. Four qualification assignments have four attempts each, four have one each and four are unstarted. Scientific allocation is eight unstarted episodes on four paired roots,456 unstarted decisions; planned total468 decisions including qualification. First request22:49:11.744114Z, last response22:51:07.656340Z, stop receipt22:51:10.611119Z. The code limits HTTP concurrency to4; errors arrive in five four-request waves with cooldowns. The recovery found no matching worker and launched none.

The first observable divergence is at transport:8 HTTP429 and12 HTTP503. There is no native answer to inspect for semantic correctness. Error bodies identify rate-limit and broker-unavailable classes, but cannot establish an account-level cause or a billing total. No retries or prompts were sent during recovery. Historical retries remain visible and are not fresh samples.

| Trace component | Expected/retained/inspected | Limitation |
|---|---|---|
| Physical request metadata |20/20/20|No serialized payload retained|
| Terminal status/error |20/20/20|No model response or returned-model identity|
| Qualification assignment histories |12/12/12|Four never dispatched; missing choices are not answers|
| Scientific decisions and trajectories |456 planned,0 generated|All eight episodes unstarted|
| Token/cost receipts |20 attempts,0 receipts|Actual spend and tokens unknown|
| Source/input |Frozen source and reused root file hashed|Reconstruction is not proof of provider delivery|

No experimental raw file was overwritten. Native hashes are checked by audit_saved.py; its output is deterministic and offline. Operator conversation and credentials are not actor inputs or published artifacts.

## Scientific assessment and eleven-dimension review

| Dimension | Status | Evidence/finding | Exact next action and acceptance |
|---|---|---|---|
| question |pass|Historical primary contrast is mix-minus-full change; FINDING limits it to these fixed post-capture roots|Retain scope; do not generalize to all swarms|
| scenarios |gap|Four scripted N12 roots,20 rounds; reference does not show a clear mixture rescue; no qualified model population|Reviewer must accept a standardized-state diagnostic claim or prospectively authorize a different fixture, never replace roots after model outcomes|
| controls |gap|Offline last-item copier passes old gate12/12, conflicting with majority on8/8 fixtures|Prospective non-copying/control criterion must reject this negative control before qualification|
| capability |unknown|No successful response, old gate tests parseability only|Fresh bounded qualification of reviewed instrument; do not infer model incapacity from HTTP errors|
| measurement |gap|Endpoint and pairing clear, but old plan analyzes complete pairs only and has no adequate missingness rule|Predeclare missing outcomes/bounds and minimum usable roots; keep absent effect unknown|
| sample_size |gap|Four dependent arm pairs, zero observed; no population precision|Declare feasibility-only precision or justify a future authorized sample; agents/calls are not independent n|
| agent_context |gap|Source uses chronological raw history, no privileged last-event field; actual payloads absent from journal|Future logger retains effective system/user messages and context hashes without operator state|
| data_integrity |pass|All20 physical IDs reconcile,12 control and8 episode assignments explicitly retained; native hashes verified|Keep every failed/unstarted unit in any future lineage ledger|
| resources |gap|20 unreceipted attempts, no historical dollar reservations|Reconcile/bound exposure and review durable worst-case pre-dispatch budget gate before releasing any part of USD5 hold|
| reproducibility |gap|Saved-data arithmetic reproducible, source pinned; old PREREG absent from pre-call commit and no independent review located|Publish prospectively and obtain applicable independent review before any future calls|
| visualization |pass|FINDING tables match saved counts; no model trajectory exists|Keep missing model traces absent, not zero; define replay mapping prospectively if a new study is admitted|

A pass here is scoped to its stated property, not a launch decision. Same-owner arithmetic checking does not satisfy independent research review.

## Issue dispositions and diagnosis

- **Pool unavailable:** accepted as observed transport failure; no unsupported root-cause/billing claim. A new health probe cannot cure the other admission defects, so none was spent.
- **Original instruction to resume unchanged lane:** rejected as unsafe operationally and scientifically. The old runner overwrites qualification/STOP and appends request IDs from1, has no hard dollar ledger and admits copying. Keeping it frozen and not invoking it preserves lineage.
- **Switch to OpenRouter if pool remains down:** authorized in principle by the recovery brief, but not admitted. No amendment was used to bypass review or budget reconciliation. No OpenRouter calls or credential reads occurred.
- **Replace weak reduced fixture:** not performed. The saved reference's near-zero comparison does not justify selecting more favorable roots. Four unchanged roots remain prospective assignments with no outcomes.
- **Prior parent-model successes:** not inherited as Claude evidence or competence. The raw-history versus privileged-last-field distinction is material; cross-model/policy pilot claims remain separate.
- **Missing public preregistration:** verified by original commit tree and untracked status. Preserve original PREREG wording as historical evidence, explicitly correct the unsupported publication statement in current reports. Never retroactively label the recovery commit preregistration.

## Budget and closeout

Actual historical model spend and token usage are unknown. Recovery made0 new model calls and incurredUSD0 incremental experimental API spend; no paid reviewer was invoked. The entireUSD5 recovery allowance is administratively unavailable until inherited uncertainty is reconciled. This is not a retroactive reservation, not proof that historical billing is bounded byUSD5, and not permission to borrow the separate freeze lane's budget. No retry, new study, alternate model, new infrastructure or post-deadline execution was launched.

This manual study has no assumed automatic operations adapter. The completed authored audit/post-mortem is the explicit closeout; no automatic scientific-review pass is claimed. Evidence metadata lives in FINDING.md within the owned directory, without editing the shared registry or submission files under the narrow ownership instruction. Sync is by explicit checked commit/rebase/push, not a persistent background timer.

**PARK.** Resume only with applicable independent review and research admission, a prospectively published competence/non-copying gate and plan, reconciled original spending exposure, audited pre-dispatch worst-case reservations and fresh provider/model qualification. The present23:30Z call cutoff is binding, and this closeout does not authorize a successor after it. No model experiment is needed to confirm the already demonstrated accounting/publication/gate defects. A future scientific attempt is blocked by those prerequisites, not waiting silently for pool health.
