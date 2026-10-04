---
id: review-sybil-newcomer-sonnet
type: task
title: "Review sybil-newcomer-sonnet, a Sonnet 4.6 replication of sybil-newcomer-api"
kind: review
status: open
priority: p1
owner: null
for: shadow
created: 2026-10-04
created_by: dmarz/newcomer-sonnet
depends_on: []
topics: [sybil-resistance]
---

## Goal

Independent cross-researcher review of `5-experiments/studies/dmarz/sybil-newcomer-sonnet` before its paid Q0/S1 stages. It is the completed Haiku study `sybil-newcomer-api` rerun on identical worlds with `claude-sonnet-4-6` as the synthesizer. Check that the source diff against the parent is limited to identifier, model id, prices, banner and the removed shared-budget partition; that Q0/S1 assignments are identical to the parent's (README and SETUP.md give the digests); that the prediction and cross-model analysis in preregistration.md are stated before outcomes; and that the budget and stop rules are sound. About 1,980 model calls, expected near $10.

## Done when

- A review file `2-surveys/reviews/sybil-newcomer-sonnet--<your-researcher>.md` with verdict pass or revise and the specific issues found.
- The owner's agent records the verdict in the study's SETUP.md G0.
