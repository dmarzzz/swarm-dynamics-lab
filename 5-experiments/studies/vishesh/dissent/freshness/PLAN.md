# Evidence eligibility and dissent diagnostic

## TLDR

F0 compares 48 matched native requests: raw timestamps versus explicit computed eligibility, each with and without opposing history/ballots, across fresh/expired and favorable/adverse evidence in three domains. Measure corrected/harmed pairs, fresh service and missingness. This is a finite development diagnostic, not native qualification or a field-rate estimate.

## Question and prediction

Does making evidence age and eligibility explicit repair Jev's expired-evidence errors, and does the repair retain its effect when opposing history and scripted ballots are present? This is a bounded component diagnostic supporting the owner-approved question: can a dissenter identify an invalid basis for consensus, obtain better evidence and restore the correct decision beyond a strong eligibility controller?

Prediction: explicit eligibility reduces expired-evidence commitments while retaining correct fresh PROCEED/HOLD decisions, including under full context. A null, mixed or adverse result remains interpretable and does not unlock the main study.

The owner approved the proposed improvements and this 48-request diagnostic on 2026-10-04. The prior RD6 Q0-A2 returned 18 valid answers, 15 correct; all three expired favorable observations incorrectly produced PROCEED. Its post-mortem, traces and costs are preserved. D0 remains unrun. This new attempt is RD7 F0-A1, not a replacement, qualification reroll or reset of RD6.

Read [the predecessor post-mortem](../reopening/reviews/Q0-A2-POST.md), [all traces](../reopening/results/q0-a2/trace-audit.json) and [quality review](../reopening/reviews/Q0-A2-QUALITY.json). The simple literal controller already answers all 18 correctly. New data are needed only to distinguish the proposed representation repair and context dependence; saved answers cannot supply those counterfactuals.

## Setup

Freeze a 2 × 2 comparison: raw timestamps versus explicit computed eligibility, crossed with source-only versus full context (opposing history plus four opposing and one aligned scripted ballot). Condition names R0, R1, E0 and E1 encode raw/explicit and context absent/present. All arms retain identical substantive text, timestamps, action criteria and within-case choice order. No wording cleanup, new examples, changed route or model is bundled into the explicit treatment.

The explicit interface adds one deterministic metadata receipt, calculated only from actor-visible `now`, `observed_at`, `ttl`, scope and revision. It lists each source's age, matching fields, eligibility and number of eligible observations. It supplies no expected action and does not interpret task content. All source copies and evidence cards retain matching identifiers/timestamps. This tests a composite representation/computation aid, not arithmetic ability in isolation. The process text's existing word “current” is retained across all four arms to avoid silently changing a second factor; its possible salience remains a limitation.

Separately implement the practical controller: remove ineligible observations and corresponding cards from actionable input; preserve them in the audit; if none remain, return DEFER without a model call. Record controller responsibility separately from native Jev behavior. The full literal reference is a stronger baseline for these finite rule tasks and remains reported. Neither baseline uses evaluator labels.

## Scenarios and sample size

Six authored semantic roots: three domains (process range, bridge capacity, required compatibility test) × favorable/adverse evidence. Each has a fresh (age 1) and expired (age 9) version under TTL 7, giving 12 paired task/age cases × four interface/context conditions = 48 assigned native requests. Reuse inspected development facts from RD6 for diagnosis; no claim of new held-out data or independent replication. Each request is stateless. Randomize the complete 48-assignment order with a frozen seed; no repeated-call estimate is planned.

Six roots and three shared grammars are the structural units; 48 calls are dependent exposures. This finite screen targets failure localization, not population precision, statistical significance or a field-rate confidence interval. Report all case pairs and domain/valence strata. Favorable and adverse content make stale PROCEED, stale HOLD and correct DEFER separately visible. Fresh PROCEED and HOLD controls reject an always-DEFER repair.

Before any subsequent native qualification, reserve a separate, operator-uninspected generated corpus with new values/identities and boundary/mismatch/mixed-evidence cases. It must cover age just inside TTL, exactly TTL, just outside TTL, future timestamps, wrong scope/revision, fresh evidence alongside stale contradictions, and current conflict. Automated label checks and the simple baselines run offline; the corpus stays private until qualification is authorized/admitted and its interface is frozen. It remains the same synthetic grammar, not a real-world holdout. This diagnostic does not launch that qualification or the broad dissent comparison.

## Metrics

Primary descriptive contrast: paired E minus R correctness among expired evidence, separately with/without context (six cases per contrast). Report corrected pairs, harmed pairs and unchanged pairs rather than only an average. Secondary: fresh-case accuracy and unnecessary DEFER, context differences, wrong PROCEED, unsupported HOLD, schema/route validity, invalid/missing/unstarted counts and actual cost/latency.

Retain raw frozen actor requests, visible answers/probabilities, assignment/request/terminal events, exact byte hashes, provider snapshot and original-ledger accounting. No owner/operator conversation, gold label or treatment label enters actor input. Preserve all 48 assigned slots; missing decisions stay unknown and enter explicit paired bounds, never DEFER or refunded calls. The controller result is computed independently and never overwrites the native answer. No hidden reasoning is requested or inferred.

Repair signal: explicit eligibility correct on all 12 expired assignments and all 12 fresh assignments, with no domain/valence/context regression. If raw arms also pass, the earlier failure did not recur under these matched inputs; do not attribute success to the aid. Partial, mixed or adverse results remain such and do not qualify the main study. Even a perfect signal requires separate fresh qualification before broad comparison. Transport failure yields incomplete evidence, not cognitive failure.

## Protocol

Before dispatch: exact 48-cell balance; actor/evaluator separation; same inputs apart from declared receipt/context; age/scope/revision calculation and card filtering; correct fresh positive/negative actions; boundary/mismatch/mixed-source controls; full literal reference correct; always-PROCEED/HOLD/DEFER and ignore-age fault policies detected; source/approval/lineage/packet gates; reserve-before-send; duplicate-attempt rejection; lifecycle/collection/finalize checks.

Run once, one request at a time. Stop on the first provider/transport/schema/accounting contract error, 60-second request deadline, 30-minute stage deadline, claim expiry, cost overflow or source drift. No retries, fallback, resume or automatic next stage. A substantive wrong answer is a diagnostic outcome and does not stop collection selectively. Complete operational finalize, all eleven scientific review dimensions, every-miss trace audit, public artifact readback and cost/release reconciliation.

## Resources and authority

The explicit owner decision covers this revised question, interface work and 48-request diagnostic. Researcher review is waived; owning review is required. Preserve the sole original Right Dissenter ledger: 506 calls and USD 0.023434447 committed API before RD7, including USD 0.004032 historical uncertain exposure. The original USD 1 API / USD 1 infrastructure caps and 650 lifetime ceiling remain; this attempt enforces the tighter 554 lifetime / 48 new-call ceiling.

Reserve USD 0.001344 per request, at most USD 0.064512 for this diagnostic. Prior infrastructure allocation estimate USD 0.755090409 is retained. Use one fresh exclusive existing machine in Dmarz's verified account/state, at most 60 minutes at USD 0.07143/hour; reserve the full lease before dispatch. No new machine is necessary if eligible fleet capacity exists. This newly approved diagnostic has its own finite lease window; it does not extend or reactivate the expired RD6 attempt. Expected model loop is minutes, with roughly 1–2 hours of preparation/analysis; these operator estimates are not provider charges.

Publish and register this immutable plan plus the F0 and R0/R1/E0/E1 TLDRs, then verify public readback, current account/allocation, exact runtime/source, original ledger and pinned `typesafe/jev-1.13-20260917` / TypeSafe route. Credential remains in the authorized local relay and never enters the host, transcript or public evidence. Release only this claim after stopped-worker and artifact checks.

## Outcome-dependent next question

The approved broader direction is useful only where invalidity needs evidence interpretation or acquisition beyond the deterministic controller. Candidate follow-on: a dissenter challenges a consensus based on an expired certification, obtains a current source under an equal checking budget, and restores legitimate service. Compare against eligibility gate plus a scheduled evidence refresh and an equally funded non-dissenting checker. Require benefits beyond those strong alternatives, including false challenges, missed invalidity, recovery latency, legitimate work retained and total checks. This is design context, not a launched swarm experiment or evidence of emergent dissent.
