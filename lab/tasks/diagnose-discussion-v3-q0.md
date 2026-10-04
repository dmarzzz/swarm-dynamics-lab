---
id: diagnose-discussion-v3-q0
type: task
title: Diagnose v3 Q0 constraint failures before fresh model qualification
kind: experiment
status: claimed
priority: p1
owner: dmarz/cloud-discussion-d1
for: dmarz
created: 2026-10-03
created_by: dmarz/discussion-bench-v3
depends_on:
- analyze-discussion-v3-q0
topics: []
claimed_at: 2026-10-04T04:08Z
updated: 2026-10-04T06:48Z
---

## Goal

Follow the Q0 post-mortem without changing its outcomes. The user authorized trying a smarter model. First isolate constraint application, report omissions and claim-to-vote consistency on already-open Q0 examples. Compare a stronger permitted model with prompt/evaluator held fixed before freezing a disjoint readiness batch. Keep confirmation closed and do not launch a broader sweep. This is a follow-up task, not a queued worker.

Read [Q0 results](../../5-experiments/studies/dmarz/discussion-dose/benchmark-v3/RESULTS-Q0.md) and [repair ledger](../../5-experiments/studies/dmarz/discussion-dose/reviews/v3-q0-a1-post.md).

Planning handoff: [NEXT-RUN.md](../../5-experiments/studies/dmarz/discussion-dose/benchmark-v3/NEXT-RUN.md) specifies D1/Q1 and cloud readiness. Include Shadow F1/F2 regression repairs before any paid launch; do not interpret the completed planning task as completed implementation.

## Done when

- [ ] Freeze a bounded diagnostic pre-run plan, provider model ID, source hashes, budget and zero/explicit retry policy; parent attempt v3-q0-a1.
- [ ] Compare clean extraction, atomic feasibility and claim-to-decision behavior; distinguish measured causes from hypotheses.
- [ ] Version stable aggregate float auditing for supported Python runtimes, with regression checks and no changes to frozen Q0 source/results.
- [ ] Review the strict extra-citation penalty and publish any amendment before new model calls.
- [ ] Repair and verify public replay delivery against the 252 saved Q0 frames; preserve other active experiments.
- [ ] If diagnosis supports advancement, freeze fresh disjoint qualification cases and retain both 5/6 competence gates; report every attempt and keep the 24 confirmation worlds closed.
