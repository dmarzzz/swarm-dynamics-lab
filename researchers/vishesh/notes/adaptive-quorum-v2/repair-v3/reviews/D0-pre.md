# Pre-run assessment: Antsy repair D0

Owner: vishesh/codex-methods. Parent: [v2 S0 post-mortem](../../reviews/S0-attempt-1-post.md).
Status: diagnostic-only. No scientific stage advancement or holdout access.

## Question and design

Locate the clean-task bottleneck: structured evidence representation, natural-language integration, atomic facts, missing information or tool-field authority. Compare JSON and concise plain-text representations of identical observations; probe atomic yes/no facts separately. Keep the English Laya checkpoint fixed. These are diagnostic prompts, not a tuned confirmatory model. Publish every case/variant, including failures.

Development task IDs 7400–7407 (not qualification/holdout IDs). Combined decisions are evaluated on complete clean observations with and without truthful tests; atomic cases cover scanned support, retention and accuracy. Inspect exact encoder truncation and option distinction. Include missing-candidate coverage tests offline. Cap 100 model calls, 20 minutes, zero hosted API spend; two CPU threads and one worker. No outcome retries. Runtime initialization failure gets its own recorded failure.

## Allocation and versions

Exclusive `sim-vishesh`, claim `vishesh-antsy-repair`, expires two hours after claim. Check merge/conflicts/workload immediately before launch. Pin Laya source `2e4d9c87e8b1621deb344eac7de5c7258f32f849` and English checkpoint `55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851`; record actual dependencies and deployment commit. CPU architecture differs from v2's Apple runtime; this is a new attempt, not bitwise replication. No secrets in records. The host contains only Antsy's isolated runtime and outputs.

## Decisions after D0

If facts are extracted but multi-constraint decisions fail, test a declared constrained architecture over actor-visible facts; no evaluator lookup. If plain language passes, freeze it before disjoint balanced qualification. If neither is competent, diagnose the smallest failing primitive; do not launch a noisy swarm sweep or silently switch to scripted actors. Any replacement checkpoint is a new predeclared diagnostic.

## Visualization mapping D0-v1

D0 is a static diagnostic matrix, not a temporal swarm run: rows are case IDs, columns are representation/primitive, cells show correct/incorrect/invalid and a visible denominator. No invented movement. Public final PNG plus raw receipts/JSON; the revised temporal study gets a separate replay mapping. Rendering does not invoke models. Verify cell counts against diagnostic JSON; missing cells remain missing, not correct. This is the explicitly justified static fallback for D0.
