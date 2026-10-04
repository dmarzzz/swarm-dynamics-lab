# Transport a2 post-mortem and prospective a3

2026-10-04 UTC. This document precedes the a3 implementation and call. The a2 outcome remains unchanged: one request, pinned model/provider matched, complete response and ordinary usage settled at 84 microdollars, but the answer included Markdown fences. Strict JSON parsing rejected it. The recorded generic transport_failed label is too broad; this was an output-format failure after successful transport. No task-competence or swarm-size result follows from it.

## TLDR

One exact-JSON diagnostic with explicit instructions excluding Markdown fences, versus the same expected {"ok":true}, before the reviewed N=1 screen. Measure format validity, pinned route, usage, cost, elapsed time and publication. Synthetic engineering qualification only. No parsing relaxation, retries, model change or budget increase.

## Question and prediction

Does explicit raw-JSON/no-fences wording produce a strictly parseable response? Predict one complete response equal to {"ok":true}. A failure blocks Q-A and remains in the denominator. Distinguish malformed output from transport faults with a safe fixed failure label.

## Setup

Use the same dedicated Swarm Lab Anthropic key and separately verified workspace routing, native pinned claude-haiku-4-5-20251001, prices, engine, task evaluator and exclusively claimed research-01. Follow SWARM-LAB-CREDENTIALS.md. Keep the original canonical Q1 budget.sqlite and its $20 total cap. Existing exposure is $0.220564: a1's unknown charge retains a $0.220480 hold and a2 settled $0.000084. No reset or assumed refund.

## Protocol

Freeze and publish this plan, register its immutable URL and verify the public condition TLDR before dispatch. New attempt anthropic-transport-q0-a3, fresh output directory and runtime-config-a3/public-plan-a3 receipts. Exactly one model call, 60 seconds, 4096 maximum output tokens, $0.220480 maximum hold, giving at most $0.441044 cumulative diagnostic exposure. Say to return raw JSON only, no Markdown fences or commentary. Preserve strict parsing unchanged and record malformed_output on parse failure. No saved-response replay counts as a new sample.

Only after a3 passes and all artifacts are acknowledged may the previously reviewed Q-A run: 16 N=1 assignments, 600 seconds each, 60 reserved for integration, $2/episode and original $20 overall shared with all diagnostics and Q-B. Use the same task prompts and evaluator; this amendment changes only the plumbing diagnostic. Read q1-pre.md and anthropic-amendment.md for the unchanged experimental design. Q-B/core remain closed pending their existing gates.

## Metrics

Assigned/attempted/valid counts, route match, token usage, settled and reserved cost, latency, exact-JSON success, and acknowledged publication. Keep a1 and a2 visible and do not conflate successful network access with valid model output.

## Visualization mapping

Publish actual service events, outcome, replay and publication receipt. Retain the fenced-answer failure as recorded. Q-A visualizations reflect actual task execution, not these one-message plumbing checks.
