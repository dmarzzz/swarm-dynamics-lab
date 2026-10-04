# Theseus D2: held-out execution and case-order confirmation

Status: prospective protocol, written before D2 implementation. Planning only; no machine allocated and no model calls started. Researcher review is not required. The owning operator must complete source/runtime, public-plan and budget admission before execution.

## TLDR

Test whether one-case execution remains more reliable than eight-case batches on fresh balanced worlds, especially when irrelevant evidence conflicts and case order changes. Compare unchanged D1 conditions D and E, using six worlds, two task families, forward/reversed case orders and two native repetitions. Measure assigned strict accuracy, valid-action recall, false actions, contract failures, repeat/order consistency and cost. Maximum 432 calls and 768 assigned decisions; one worker, two hours, zero retries. This is model-specific executor qualification, not cultural preservation or a compute-matched comparison.

## Question and prediction

Does E retain competent execution when source mappings and case ordering vary, and does it prevent the positive-action misses observed in batched D?

Prediction, based on D1: E will be less sensitive to case grouping, while D may miss legitimate actions when irrelevant evidence conflicts. No directional source-label effect is assumed. Reversing a case's position tests order sensitivity, but cannot by itself identify an internal attention mechanism. Repeated identical requests assess observed native variability at temperature zero, not independent worlds.

Primary estimand: for each world, E minus D in assigned strict accuracy, equally weighting release and incident, the two orders and the two repetitions. Report all six world differences and their equally weighted mean. A 3 percentage-point gain is the prespecified practical contrast threshold; it is an engineering preference, not a significance threshold. No p-values or population error-rate bound from dependent case counts.

## Setup

Keep model claude-haiku-4-5-20251001, temperature 0, output limit 1200, keyed evidence and decisions-only output. Use the exact D1 D/E system text, rule wording and output schema. Preserve the same eight-case batching difference. The only context labels are release and incident; remove migration-old/new from this confirmation so repeated release semantics do not receive triple weight. Console renaming is reserved for a later transfer study.

Six fresh worlds use the following explicit mappings; the generator must accept a mapping argument rather than infer it from a seed's last digit:

| World seed | Class A source | Class B source |
|---|---|---|
| 7100 | probe | ledger |
| 7101 | probe | canary |
| 7102 | ledger | probe |
| 7103 | ledger | canary |
| 7104 | canary | probe |
| 7105 | canary | ledger |

Development seeds are 7000–7005. D1 seeds and its three discovered failure patterns are regression fixtures only, excluded from D2 outcomes. The six held-out seeds and acceptance rules are fixed before model calls; no outcome-driven seed selection.

Each world has eight cases, four per class. Every governing signal/freshness pair occurs once per class; each irrelevant column is an independently seeded permutation of the same four pairs. Keep the D1 irrelevant summary/queue fields and sorted JSON field order, matched across arms. New opaque IDs do not imply new reasoning tasks. Both task families see the same eight observations.

Use random.Random with separately named streams D2/ids/{seed}, D2/evidence/{seed}/{class}/{source}, D2/summary/{seed}/{class}/{case}, D2/queue/{seed}/{class}/{case}, and D2/order/{seed}; keep the stream definitions and Python version in the frozen manifest. The evidence stream permutes irrelevant columns only; governing rows enumerate 00,01,10,11. The base case order is one seeded permutation; its paired order is the exact reversal. Each case therefore appears once in an early position and once in a late position. Do not choose an order based on model outputs.

Before any call, require complete truth-table coverage and a manifest in which every governing source has at least one valid-release case where both irrelevant sources would block release. Record all conflict strata, including easy cases. Wrong-source, ignore-freshness and always-hold mutants must be distinguishable by the held-out manifest or its explicitly enumerated oracle fixtures as appropriate; any manifest identification failure blocks this version and requires a prospective amendment, not silent seed resampling.

## Protocol

For each world and task family:

1. Use the base order and its reversal.
2. Repeat each exact ordered condition twice, without feedback, memory, correction or agent history.
3. D receives all eight cases in one call. E receives eight independent one-case calls with the identical rule, mapping, command documentation and case contents.
4. Native repetitions have distinct assignment IDs but identical actor request bytes. E's order label controls only the corresponding presentation block; it conveys no extra context to the actor.
5. Shuffle the complete assignment schedule once using D2-dispatch-v1. Save the schedule and exact request hashes before dispatch. Do not reshuffle on failure.

Counts: 6 worlds × 2 families × 2 orders × 2 repetitions = 48 matched blocks. D uses 48 calls and E uses 384 calls: **432 calls total**. Each arm has 384 assigned decisions, including 192 release and 192 incident decisions. There are 48 distinct case records and 96 distinct case/family combinations, not 768 independent problems. Each arm has 48 repeated presentations of valid-release cases representing only 12 distinct eligible cases.

For release, ship iff the governing signal and freshness are both true; otherwise hold. For incident, choose the governing source iff its signal is true; otherwise none. Freshness is irrelevant to incident. The visible mapping is an executor ceiling, not acquired culture.

Calls are stateless, with one worker and zero retries, including ambiguous requests. First live responses belong to the assigned dataset. No excluded paid smoke calls. Persist a start record and reservation before transport and a terminal record before reporting. Stop on deadline, claim expiry, budget exhaustion, malformed admission or reporting failure. Preserve all completed records and mark every remaining assignment not run. Do not repair the actor or expand the stage while it is running.

## Metrics

Primary: strict assigned accuracy under the frozen full-response contract. As in D1, an invalid batch makes its assigned rows strict failures. Report per-row valid partial decisions separately so this batch penalty is visible rather than mistaken for a reasoning loss.

Secondary, all prespecified:

- Valid-release recall, false holds and false releases, with assigned positive/negative denominators. Always-hold must visibly fail the usefulness gate.
- Incident source-selection accuracy and false activation.
- Response received, expected ID present exactly once, command validity, schema validity and semantic correctness as separate fields. Never label a received invalid command as an absent response.
- Order consistency for the same case and repeat agreement for identical requests; report their world-level summaries. Report early/late error rates after matching case identities, and governing-source/conflict strata. These are descriptive mechanisms checks.
- Command meaning decoded using current commands and a prespecified diagnostic alias table: release aliases ship/hold; incident aliases none/probe/ledger/canary. Alias decoding never grants strict credit. Missing, duplicate or ambiguous IDs remain unscorable diagnostic rows and strict failures.
- Calls, input/output tokens, cost per assigned case and wall time. D/E do not match compute; a favorable result supports an accuracy/cost tradeoff, not intrinsic efficiency at equal resources.

Implement a second scorer directly from raw responses and evidence, without importing the primary scorer or its truth/command helper. Compare full strict outcomes, not only decoded partial correctness. Freeze tests for malformed schema, duplicate/unknown/missing IDs, wrong console, invalid command and whole-batch collateral failure. Any disagreement stops interpretation until the defect is explained without overwriting the original run.

## Qualification and decisions

A candidate must complete its full assigned set with no unresolved transport/accounting gaps, have 100% valid response contracts, achieve at least 377/384 strict correct overall (98%), at least 183/192 in each family (95%), and at least 61/64 in every world (95%). Additionally require at least 46/48 valid-release actions correct (95%) and zero false releases. These are deliberately stated engineering gates, not confidence guarantees about deployment reliability.

- E passes and D fails: retain E for a later culture feasibility study. Claim a material batching advantage only if the prespecified mean gain is at least 3 points and gains occur in at least four of six worlds; otherwise describe only the differing gate outcomes.
- Both pass: prefer the lower measured cost per assigned case, normally D; do not insist on atomic execution because it won D1.
- D passes and E fails: retain D provisionally and investigate the reversal.
- Both fail, or the run is operationally incomplete: publish the failure and diagnosis; do not start a culture study or silently retry. Plan at most one targeted repair separately if warranted.

Passing does not automatically launch another experiment. Freeze the chosen executor and revise the actual inheritance/turnover protocol prospectively.

## Budget and launch gates

Original cumulative authority remains USD5. D1 cost was USD0.178341 in model usage plus approximately USD0.007116 in infrastructure, leaving approximately USD4.814543. Reconcile any invoice difference and unresolved reservation before D2. Do not create a fresh USD5 or default USD2 budget.

Incremental D2 ceiling: USD4.00 model reservation plus USD0.25 infrastructure, total USD4.25 inside that remaining authority. Reserve it once under a unique D2 allocation linked to the D1 settlement. At previously verified USD1/M input and USD5/M output, with encoded request ceilings of 5000 bytes for D and 2000 for E and a conservative 512 input-token overhead, the entire planned reservation is:

48 × (5000 + 512 + 1200×5)/1,000,000 + 384 × (2000 + 512 + 1200×5)/1,000,000 = **USD3.821184**.

This is a conservative request envelope, not expected spend. D1 D/E usage scaled to 48 matched blocks suggests roughly USD0.354 model spend, an estimate that may change with the new cases. Verify current pricing and actual serialized request bounds before launch; stop rather than exceed them. One worker, two-hour run deadline, no retry allowance. Machine cost and all failed calls count toward the cumulative cap.

No host is needed during planning. At launch, use a fresh exclusive approved-account allocation; provision a new dedicated machine if no eligible host is free. D1's host was retired. Use the owner-designated credential route, clean pinned source and current operator assessment. Publish and register the immutable final plan and condition TLDRs, verify hashes and the actual public page, then dispatch. No researcher/inbox approval gate is reintroduced. Exact user prompts stay private.

## Visualization and closeout

Show the six world-level D/E contrasts, positive-action recall and cost next to overall accuracy. For order analysis, connect the same case's early and late positions; distinguish repeated samples from distinct cases. Show invalid, failed and unstarted assignments explicitly. The replay displays actor-visible evidence and output separately from evaluator-only truth.

Afterward, reconcile every assignment and charge, compare both scorers, write a postmortem and archive raw records with upload/readback hashes. Release the claim and retire temporary infrastructure after verifying worker exit and durable backups. Update the next culture design from the observed result, without moving this run's goalposts.

## PI review implementation clarification

See [D2-PI-REVIEW.md](D2-PI-REVIEW.md), written before implementation. Save raw actor text and served model; stop further dispatch on model mismatch, transport ambiguity or missing usage while retaining reservations. Atomic order labels contain identical inputs and support repeat variability only; interpret order effects within D. Mapping and world composition remain confounded. No original assignment, actor prompt or gate is changed.
