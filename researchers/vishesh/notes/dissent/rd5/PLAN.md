# Preserving the right to reopen a decision

Prospective RD5 design, 2026-10-04. Owner: vishesh/codex-decision-models. Status: **planning complete for a bounded development study; no implementation or native run yet**. This follows the [RD4 post-mortem and report](../rd4/REPORT.md) and preserves its adverse/null result. Planning does not allocate a host or reset the original budget.

## TLDR

Can a group avoid spending its last verification opportunity on repeated uncertainty, while still responding to genuinely new evidence before a deadline? First repair execution accounting and make unresolved decisions explicit. Test a common, provenance-preserving evidence representation. Then compare bounded always-check with one-check-per-observation and with an additional protected late check. Three contrasting scenarios must include a case where withholding the second check hurts. Primary outcome is correct on-time decisions over every assigned opportunity; cost, unjustified actions, delayed recovery and unsafe proceeds remain separate. A 60-call development envelope fits the 72 calls remaining under the existing lifetime cap. It cannot establish general robustness or novelty.

## Question and prediction

The immediate engineering goal is to remove avoidable failure pathways. The research question is narrower: **under a fixed verification budget and deadline, when does remembering unresolved evidence and protecting future verification capacity improve collective decisions, and when does it delay a useful decision?**

RD4's observed original-versus-always-check accuracy gap comes from one missed recovery admission. The larger shared deficit comes from an unresolved alarm interpretation, repeated checking, budget exhaustion, and a separate transport-affected trajectory. These are different mechanisms. The candidate must not bundle new prompts, more information, more calls and a different budget into one claimed improvement.

Predictions, before new outcomes: suppressing repeat checks should help when the underlying observation has not changed; an additional reserved check should help when early distinct observations are uninformative and later evidence is valuable. Reservation can hurt when a second early check would settle an urgent decision. The three-way contrast tests those tradeoffs rather than assuming reserve is always beneficial. A learned admission model is not part of the primary successor: the prior experiment did not justify its extra calls. Its future role, if any, is ranking competing eligible checks in a genuinely constrained queue.

## Setup

The candidate separates three decisions: whether an observation is eligible for checking, how to interpret an acquired observation, and how to allocate scarce checks over time. All policies share the same scope/version/expiry rules, interpretation packet and explicit unresolved state. Source identities and acquisition receipts are supplied by the synthetic environment; their authenticity is an assumption, not something Jev establishes.

Each policy has one Jev resolver with its own state. Five initial ballots are supplied by the fixture (four supporting the initial action, one dissenting); no native peer generation or additional judge is hidden in the budget. The same ballots, task requirements and event stream are paired across policies.

The small native study has six authored event streams: three scenario mechanisms, each with a stop-direction and a resume-direction version. Each stream has four decision opportunities at ticks 0, 2, 4 and 6; a dispatched check returns one tick later and each opportunity's deadline is its tick plus one. The horizon is eight ticks. Each policy gets at most two checks and two native resolution calls per stream, not two per epoch. Exact assignments, task texts, result availability and input hashes must be frozen before qualification. Fresh IDs alone do not create independent semantics.

| Scenario | Events and practical use | Contrast it must expose |
| --- | --- | --- |
| Repeated alarm then real change | A process inspection is incomplete. Exact repeats and aliases add no observation. At tick 4 a newly acquired reading can justify stopping or resuming. | Rechecking the same unresolved evidence versus preserving a check for the changed world. |
| New reports without useful progress | A bridge task receives a second authentic but still inconclusive inspection at tick 2; a useful later inspection arrives at tick 4. | One-check-per-observation alone can still spend everything; reservation may add value beyond deduplication. |
| The second check is needed now | A required build result is incomplete at tick 0. An independent, decisive result is available at tick 2 and matters before tick 3. Later evidence adds no value. | Reservation must reveal its early delay cost; this is the counterexample to a universally beneficial reserve. |

The native micro-study supplies these verifier observations and varies their availability. It does not claim to reproduce the old Jev error rate. Offline regression fixtures separately replay the old failure patterns. A broader future study must cross mechanism with domain, event time, source reliability and severity; six streams confound story and mechanism and cannot support a population effect estimate.

### Primary policy comparison

| Policy | Shared rules plus allocation rule | Purpose |
| --- | --- | --- |
| B0 bounded always-check | Check an eligible unresolved challenge while budget remains, including repeated challenges. Reuse already resolved decisions as before. | Strong simple baseline with the same interpreter and two-check budget. This is a successor baseline, not a silent rewrite of RD4. |
| B1 remember unresolved evidence | B0, but consume at most one check for each eligible observation frontier. A repetition of an unresolved frontier remains unresolved and uses no new model call. | Isolate the benefit and cost of remembering failed resolution attempts. |
| B2 protect a late check | B1, plus at most one check before tick 4. The last check becomes available at tick 4 and expires at the horizon. | Isolate temporal reservation beyond deduplication. No secret knowledge of the actual change time. |

Primary contrast B2 minus B1; secondary B1 minus B0. Do not infer B2's value from B2 versus B0 alone. The fixed reservation time is an intentionally simple, falsifiable policy. It is not an optimal value-of-information rule. All arms see the same public horizon; none sees evaluator truth, future events or another arm's results.

An observation frontier records applicable acquisition IDs, source roots, object/version, timestamps and content. Alias/wording changes cannot create a new acquisition. A genuinely new trusted measurement may create a frontier even if its value repeats, but it is not automatically statistically independent. A later timestamp claimed inside untrusted text is insufficient. Scope/version change or expiry reopens assessment of applicability; it must not revive an expired authorization. A scenario contract must define whether a new verifier is available, how its receipt is identified, and what makes another check informative. These are supplied-environment assumptions in this study.

## Protocol

1. **Commit this plan before experimental implementation.** Preserve all RD4 source, records and denominators. Write a saved-data failure decomposition in this directory, marked retrospective, with no inference or altered answers. Keep repair evidence separate from hypotheses.
2. **Implement the contracts in [IMPROVEMENTS.md](IMPROVEMENTS.md) one at a time.** Begin with transport admission and separate ledgers for observation acquisition, native inference and decision state. Retain the successful closure/alias rules. Use only development fixtures for fault tests and policy transition tests.
3. **Use common structural eligibility for all three policies.** Applicable unresolved evidence can earn a check according to the allocation rule; Jev no longer gets an extra veto over eligibility. Eligibility authorizes inspection, never automatic acceptance of the dissenter's proposed action. Preserve no-dissenter, irrelevant, stale and forged-acquisition negative controls in offline coverage.
4. **Represent uncertainty explicitly.** Keep last verified action as historical memory, separately from the currently authorized action. When current applicable evidence is unresolved, returning KEEP must not silently turn an old ballot into a freshly resolved decision. Exact repetition returns the same unresolved status; new evidence can reopen it. Losing a formerly correct answer that occurred without new verification is not by itself a regression if the old authorization was unjustified; report both factual correctness and justification.
5. **Test interpretation independently of allocation.** Proposed Q5: 12 fresh authored packets, each presented once as the full natural-language evidence and once as a structured evidence card: 24 provider calls maximum. Six answerable packets cover HOLD/PROCEED in each domain; six uncertainty packets cover missing/conflicting evidence in each domain. Negation, numeric limits and required/optional tests must occur in the frozen packets. All cards retain source text, scope, version, time and cited field provenance. Extract explicit values with a deterministic, auditable adapter; ambiguous extraction remains unknown. No evaluator action, trusted-correct flag or oracle-filled missing field may enter a card.
6. **Fix the interpretation choice before seeing Q5.** Structured cards are the nominated candidate for all B0/B1/B2 arms. Require all 12 card responses valid and all 12 semantically correct, including six DEFER controls; report the raw pairs as a representation diagnostic. If the candidate fails, stop the native stage and return to design. Do not select the better representation after observing scores, lower the threshold or retry failures. This small screen establishes only bounded development competence.
7. **If later admitted and qualified, run H5 once.** Six disjoint streams × three policies × four epochs = 72 dependent decision records, at most 36 native calls. Pair all arms within stream and block/counterbalance their execution order using a frozen seed. Identical full requests may share a saved response or saved failure, but state-dependent differences must receive distinct hashes. Caching does not create replication. The maximum envelope assumes no cache savings.
8. **Refresh all operational gates before a native stage.** Immutable readable plan, condition TLDRs, public preflight, a fresh exclusive Dmarz fleet allocation, frozen qualified source/model/route, current cumulative ledger and exact startup command are required. Credential values stay local and out of logs. No machine is needed for this planning task. Researcher sign-off is optional under owner instructions; no independent review is fabricated.
9. **Use robust execution accounting.** A missing end-to-end relay response before dispatch leaves the assignment unstarted. A transport failure after a real acquired check does not refund that check. A saved valid observation survives an interpreter failure, but an unknown provider outcome is never blindly retried. Mark operational failures separately and stop at the first new ambiguous dispatch. Any continuation gets a new assessment and preserves all prior records. Proposed stage wall-time limit: 30 minutes, one worker, no automatic retries.
10. **Evaluate every assignment and close out.** Recompute summaries from records, retain all failures, publish measured replay, compare against the plan, verify artifact readback, and release the claim. A null or adverse reserve result is a valid stopping outcome. Do not move into a larger efficacy study on the strength of the micro-study alone.

## Metrics

Primary: correct on-time completed action decisions / 24 assigned opportunities per policy, including failure and DEFER in the denominator. Report paired changes by each of the six streams and separate early/late epochs. Qualification uncertainty scoring and temporal action completion are different endpoints: a justified DEFER may pass Q5 yet remain a noncompletion in H5.

Secondary: correct action at the predeclared critical event in each stream; wrong PROCEED; unnecessary HOLD; DEFER duration; delay from newly available evidence to a justified action; checks spent on an unchanged frontier; checks available when new evidence arrives; unused reserved checks; unjustified committed actions; physical check attempts and successful receipts; native dispatches, logical calls, tokens, dollars and elapsed time. An interpreter failure must not be counted as a failed physical acquisition if the observation already exists.

Practical screen for further development: B2 must gain at least two correct decisions out of 24 versus B1, create no extra wrong PROCEED, and pass all state/lineage checks. This threshold is a development decision, not statistical significance or a safety guarantee. Always report the urgent-early scenario separately, even if aggregate performance improves. Any new harmful action or unchanged-budget failure stops promotion; a tradeoff in timely correct HOLD/PROCEED requires explicit interpretation, not an average-only claim. If B1 helps but B2 does not, keep the simpler deduplication policy.

Use a resource vector rather than adding unlike units. Report wrong-action/deferral/check-cost sensitivity over the prior illustrative loss weights, with the model-call cost added explicitly and no field-calibrated utility claim. Missing-answer sensitivity includes direct failures and dependent descendants, with all-assigned scores primary; never drop the hard stream or assign missing paired differences zero. Six streams are descriptive feasibility evidence, not an independent power calculation or proof of general superiority.

## Budget and staged decision

The preserved ledger has 428/500 lifetime provider calls and $0.02065245 committed API cost under the existing $1 API/$1 infrastructure envelope. Therefore only 72 calls remain, despite substantial dollar headroom. RD4's voluntary stop at 481 applied to that completed iteration; this proposed successor remains inside the original 500-call authority. No new allowance is inferred from the RD5 name.

Proposed maximum: Q5 24 calls + H5 36 calls = **60 new provider calls**, ending at most at 488/500 and leaving 12 unallocated. The 12 are a margin, not an automatic repair allowance. At preparation, enumerate every permitted request and reserve using the verified route price/context bound; if this envelope is infeasible, reduce the design prospectively or stop. No undeclared model-based extractor, judge, admission call or credential/model probe fits outside the count. The broader research program below is not funded or admitted by this 60-call sketch.

## Visual and reporting design

Each measured trajectory should show four aligned tracks: supplied observations and their provenance; currently authorized action versus historical last verified action; remaining physical checks and inference calls; and evaluator truth shown only to the reader. Distinguish a new message from a new acquisition, and show a reserved check remaining unused in the early-urgency counterexample. Pair streams side by side with B0/B1/B2. The main chart should show correct decisions against check use, with every failed/deferred opportunity visible rather than a success-only curve.

No new measured chart exists yet. Any design illustration must say proposed or scripted and must not appear in the empirical results column.

## Research context and boundaries

The [research agenda](RESEARCH-QUESTIONS.md) develops the broader question and three failure mechanisms. The existing [source map](../SOURCES.md) retains Minority Sentinel, withheld dissent, stop signals and the original map threads. New focused reading adds [[hay-2012-selecting]] on allocating computation and [[tan-2016-honey]] on context-sensitive inhibitory signals. These motivate questions; neither validates the proposed protocol. No novelty claim or fresh Twitter-thread evidence is made here.

Before broader evaluation: add independently authored semantics, cross mechanism with domain, vary change time and verifier reliability, include no-change and urgent-early worlds, and test forged novelty, conflicts, version changes, expiry, late/unavailable verifiers and scarce external review. Evaluate endogenous dissent separately: today's minority votes remain supplied. The contribution worth testing is an inspectable right to reopen under limited attention, not a renamed generic verification rule.
