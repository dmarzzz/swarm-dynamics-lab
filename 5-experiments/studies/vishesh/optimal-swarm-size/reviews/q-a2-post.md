# Q-A2 post-mortem

2026-10-04 UTC. Frozen implementation 056718f7a86b2807b05b6f952e34f4b1218393ed; prospective plan q-a2-plan.md verified at the exact public URL before dispatch. This post-mortem is retrospective.

16 assigned, 2 started/terminal/graded, 14 unstarted after the preregistered two-consecutive-malformed-output stop. Both terminal cases failed during planning and the single permitted repair; zero item work events. All four response-format events reported valid_json=false and fenced=true. Explicit no-fences wording did not reliably enforce raw JSON. No task competence or swarm-size conclusion is supported.

Both executed episodes' four artifacts and terminal reports were acknowledged. Batch execution_complete=false and publication_complete=false because 14 assignments were not executed/published; do not mistake that full-batch flag for a failed upload of the two terminal cases. Preserve all 16 assignments and missingness. Worker exited.

Four new model calls settled at 6,878 microdollars ($0.006878). Canonical ledger now has 39 calls, $0.108510 settled and the original unresolved $0.220480 hold, totaling $0.328990 exposure against $20. Remaining authority $19.671010; no reset, refund or replenishment. Q-A1 and all transport attempts remain separate.

Next engineering decision: investigate a declared structured-output mechanism or an explicitly specified extraction contract before any further paid attempt. Do not silently strip Markdown fences or retroactively rescore these as valid outputs. Any change requires its own prospective amendment and bounded qualification. Q-B/core remain closed. No further runs dispatched by this attempt.
