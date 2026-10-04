# Operator authorization: bounded v3 qualification

Recorded 2026-10-04 UTC by dmarz/discussion-bench-v3.

The operator's instruction after the repair report was: "okay once u document those fixes and responses to vishesh let's just start shipping the experiments". The fixes and [response](VISHESH-REVIEW-RESPONSE.md) were already committed and sent to reviewer inboxes.

We interpret this instruction as authorization to start the bounded S0 engineering qualification while Shadow's independent review remains pending. This interpretation was stated to the operator before preparation. It supersedes the earlier local workflow's requirement to wait for the v3 verdict before any model call. It does not represent independent approval, a passing hypothesis review, permission to open the confirmation holdout, or permission to conceal failed qualification.

Scope: one frozen Haiku 4.5 run, three agents, six previously reserved qualification worlds (20001–20006), paired clean/attacked evidence, four arms, three discussion/private rounds, 36 memory fixtures, 96 total cases and 636 calls with zero retries. Diagnose any execution or capability failure transparently before proposing a broader sweep. The confirmation IDs 30000–30023 remain closed. A dedicated exclusively claimed host may be created using the operator's earlier DigitalOcean authorization.

The lab-wide dmarz API budget is $500 across experiments per the operator's researcher directives. The run's 636-call cap and token ceilings bound this batch; its $100 conservative reservation ceiling is deliberately above the maximum expected reservation of this fixed plan and is not a $100 spending target. Record actual usage. Credentials come only from the existing encrypted private configuration, never this repository.

The launch manifest must preserve `independent_review: pending`, hash this authorization and the v2 results, and match exact current source and settings. The normal reviewed path remains available separately. The bounded operator path cannot authorize S2 or a different split.
