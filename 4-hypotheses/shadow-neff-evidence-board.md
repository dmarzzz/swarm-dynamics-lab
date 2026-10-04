---
id: shadow-neff-evidence-board
type: hypothesis
title: Splitting evidence across agents lifts the N_eff ceiling only when peers carry evidence, not just answers
owner: shadow
agents: [shadow/sol-1]
status: proposed
created: 2026-10-03
surveys: [llm-agent-swarms]
closest_prior: [bertalanic-2026-ringelmann, begin-2026-preference, zhang-2026-silo, li-2026-diverse, liu-2026-social, rai-2026-when]
topics: [llm-agent-swarms]
keywords: [effective-sample-size, correlated-errors, evidence-aggregation, debate]
---

<!-- PROPOSAL ONLY. Not accepted, not run. Experiment build: cytonomy (vishesh) is taking the first pass on
5-experiments/toolkit/agent-experiments; this file states the claim and kill criteria so the protocol can be frozen against it. -->

## Claim

For same-model LLM agents on a binary ground-truth task, giving each agent a disjoint private evidence shard
moves the debate team out of the Ringelmann hard-ceiling regime (beta ~ 0, N_eff <= 2) into the sublinear
regime (beta > 0.3, N_eff at N = 16 at least twice the identical-evidence value), and this gain disappears
when peers exchange only answers instead of answers plus the evidence they cite.

## Grounding

- Same-model teams hit a flat N_eff ceiling of about 1.2 to 1.8 under dense debate on benchmark QA, and the
  noise placebo equals self-correction, so peer content adds nothing beyond re-evaluation
  ([[bertalanic-2026-ringelmann]]). Independent groups find the same ceiling in a prediction market
  ([[begin-2026-preference]], N_eff about 1.4 flat from N = 5 to 40) and in judge panels ([[kohli-2026-nine]]).
- In every one of those settings all agents see the same item. The ceiling may be a property of shared
  input, not of the model: [[li-2026-diverse]] reports that identical evidence makes forecasting deliberation
  herd and partitioned evidence removes most of that, and [[liu-2026-social]] derives a bounded N_eff that
  recovers toward N only under specific exposure conditions.
- Against: [[zhang-2026-silo]] shows coordination overhead on sharded inputs growing with N until it cancels
  the parallel gain, and [[rai-2026-when]] finds wrong-answer agreement survives even cross-family mixing on
  rare factual queries. So the ceiling could persist with sharding, through shared priors.
- [[pavlova-2026-flag]] is the closest task design (private crops of a hidden flag) but reports accuracy
  and endpoint classes, not rho_N or N_eff, and runs broadcast at one N.

## Novelty

- [[bertalanic-2026-ringelmann]]: defined N_eff = N / (1 + (N - 1) rho_N), fit rho_N = c N^-beta, ran
  the noise placebo, all on MMLU/GSM/GPQA where every agent sees the whole item. We use the same estimator and
  placebo, but the manipulated variable is evidence distribution, which they name as the falsification test
  and did not run.
- [[begin-2026-preference]]: N_eff vs N (5 to 40) in a non-interacting LMSR market, identical questions.
  We add interaction and split evidence. Small overlap in method (same Kish formula).
- [[zhang-2026-silo]]: sharded algorithmic tasks at N = 2 to 100, reports success and partial correctness,
  no correlation estimator and no belief dynamics. We measure rho_N and N_eff, with a placebo, on a
  belief task.
- [[li-2026-diverse]]: partitioned evidence improves Brier in a forecasting method (InfoDelphi), N not swept
  (abstract read). We sweep N, fit the Ringelmann regime and separate evidence-passing from answer-passing.
  If their full text already reports N_eff vs N, the novelty narrows to the answers-only ablation; check
  before acceptance.
- [[liu-2026-social]]: theory plus operator-controlled benchmark variants for bounded N_eff under
  attention limits. We provide a direct empirical rho_N on a sharded task that can test their escape
  condition. Honest difference: measurement versus theory, overlapping question.
- [[rai-2026-when]]: preregistered cross-family agreement on rare queries, no interaction. Used here only
  to set the difficulty tiers.

## Prediction

If true: under identical evidence, fitted beta ~ 0 and N_eff(16) <= 2 (replicates the ceiling). Under
sharded evidence with evidence-passing, beta > 0.3 and N_eff(16) >= 2x the identical-evidence value.
Under sharded evidence with answers-only messages, N_eff falls back to within 25% of identical-evidence.
The noise placebo stays at or below self-correction in all arms.

If false: sharded evidence-passing stays in the hard-ceiling regime (beta < 0.1, N_eff(16) < 1.5x
identical), meaning shared model priors, not shared input, set the ceiling. Or the gain appears equally with
answers-only, meaning sharding works through initial-condition diversity and the peer channel is irrelevant.

## Minimal experiment

Built on cytonomy's `5-experiments/toolkit/agent-experiments` harness (schemas, context-visibility controls,
preregistration template); the collective-sensing example is the scripted version of this design.

- Task: binary questions with a ground truth recoverable only by pooling shards (synthetic hidden-profile
  items in the style of [[li-2025-systematic]], three difficulty tiers matched to [[rai-2026-when]]'s
  common-vs-rare split). About 150 items.
- Arms (2 x 2 plus controls): evidence {identical, sharded} x message {answers-only, answers + cited
  evidence}; plus self-correction and the noise placebo (unrelated peers' answers) per
  [[bertalanic-2026-ringelmann]].
- N in {1, 2, 4, 8, 16}, 2 debate rounds, full connectivity, one open model at fixed temperature.
- Estimator: rho_N from pairwise post-communication agreement, N_eff via Kish, (c, beta) fit per arm with
  bootstrap CIs over items.
- Prior-artefact control: randomised initial assignments and reversed-wording items, per [[yang-2026-when]]
  and [[fukushima-2026-message]].
- Budget: about 150 items x 5 N x 6 arms x mean 6 agents x 2 rounds, roughly 50K calls on a small open model.
  One day on a hosted 8B endpoint; a pilot at N <= 4 first.

## Kill criteria

- Identical-evidence arm does not reproduce beta ~ 0 and N_eff(16) <= 2: the harness differs from the
  published setting and the comparison is uninterpretable. Fix the harness before testing anything else.
- Sharded evidence-passing N_eff(16) under 1.5x identical, with CIs excluding 2x: claim refuted.
- Answers-only arm matches evidence-passing within CIs: the mechanism part of the claim is refuted (sharding
  helps, the channel does not).
- The full text of [[li-2026-diverse]] or [[liu-2026-social]] already reports N_eff vs N with split
  evidence and a placebo: park as replication.
