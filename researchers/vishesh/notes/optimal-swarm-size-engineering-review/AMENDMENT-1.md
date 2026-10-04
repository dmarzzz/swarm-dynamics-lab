# Repair re-review amendment: E1–E3

**Verdict: PASS for the bounded offline E1–E3 engineering repairs.** No additional concrete Q-A code blocker was found in this re-review. This supersedes the original REVISE verdict only for the repaired source hashes linked below. It does **not** declare the paid batch launch-ready, validate the live reporting/provider integrations, or constitute formal cross-researcher approval.

Reviewer: vishesh/codex-independent-reviews, 2026-10-04 UTC. Reviewed checkout `b611356e` includes repair commit `afa309b8`, the published descendant of the supplied repair. [Exact reviewed hashes](repair-source-receipt.json) match every entry in the author's validation.json. The reviewer's [prospective repair plan](REPAIR-PLAN.md) was publicly fetched with identical bytes before testing; [receipt](repair-registration.json). The original review/post-mortem and author q1-engineering-response.md were read. No implementation or task claims were changed.

## Reproduced evidence

All **31 existing tests passed** ([log](repair-unit-tests.log)). The independent [regression script](repair_checks.py) and [results](repair-checks.json) revisit the original counterexamples, using only qualification public inputs and local mocks. The injected transport produces public arithmetic/sign-repair answers; none of these calls contacts a model or provider.

| Reviewer check | Repaired observation |
| --- | --- |
| Seven error categories | Deadline, HTTP 429, missing usage, route mismatch, missing credential, stage exhaustion and episode exhaustion remain distinct; each planning failure admits one call with no plan-repair retry. Stage exhaustion is fatal; episode exhaustion is not. |
| Raising progress callbacks | All 16 assignments complete all work and produce correct scripted final artifacts; 288 injected calls. Reporting faults are retained, and synthetic private diagnostic text is absent from traces. Previously each episode stopped after item one. |
| Upload returns incomplete | One completed outcome survives; 15 assignments are explicitly not started; exit 2 with publication_incomplete. |
| Initial public admission failure | Zero provider calls; one admission_failed plus 15 not_started states; all 16 state records retained; exit 2. |
| Fatal route mismatch | Exactly one provider call and one terminal failed outcome; 15 assignments not started; safe route_changed stop reason; exit 2. |
| Spooled upload/terminal acknowledgments | publication.json is persisted, contains all four artifact acknowledgments, and complete remains false. |

These are software diagnostics, not measured model qualification success or confirmation that the actual hub has these mocked behaviors. Original failed-counterexample logs remain unchanged.

## Disposition

**E1 closed offline.** Allowlisted SafeFailure codes cross the provider/engine boundary; the batch stops on fatal configuration, billing and stage errors. Unknown charges retain reservations. Model-plan parsing errors remain separately eligible for the predeclared single repair. The code does not claim that terminating a local provider process cancels remote billing. Successful charge records preserve route-match flags.

**E2 closed offline; live integration outstanding.** Initial public registration remains fail-closed. Progress uses a single asynchronous in-flight update, with failures journaled independently of model execution. Each hub delivery operation has a parent wait/termination bound, and final publication stores explicit acknowledgments, spooled/unknown state and an incomplete flag. Final wait is outside the recorded actor execution interval. The installed client contract is an author-inspected dependency; this reviewer did not independently access the selected host or run the new spawn wrapper against that client. Synthetic host validation must establish actual API signatures, process imports, credentials consumed privately, acknowledgments, public per-run visibility, artifacts and bounded failure behavior before the paid batch. Previous tests of the old wrapper do not satisfy this.

**E3 closed for the tested handled-exit paths.** All assignments are written before admission. The final reconciler keeps execution state, stop reason, exposure, outcome presence and publication separate and produces nonzero partial-completion status. Admission, fatal transport and upload failure are now represented explicitly. This is not a guarantee against abrupt process death, disk exhaustion or power loss: the immutable assigned manifest and durable evidence must still be reconciled by the operator after such interruptions. No fresh budget ledger or invisible replacement run is authorized by recovery.

## Remaining gates and scope

Before paid Q-A, the launch owner must still obtain the required non-vishesh package approval (task currently for dmarz), complete the new live synthetic reporting diagnostic, resolve approved credentials privately, verify served route/usage and price bounds, acquire a current exclusive allocation, preserve the one canonical $20 ledger, and refresh immutable source/config/public-plan receipts and per-run TLDR checks. Do not use this same-researcher amendment as independent_review_commit. None of those external prerequisites was resolved in this review.

The original chain-edge finding remains: an acyclic model plan can delete public chain prerequisites. It does not block N=1 competence screening by itself, but must be enforced or explicitly scoped before Q-B size comparisons. Transfer/core remain closed; the arithmetic grammar and test-based evaluator do not establish general repository repair competence. No new prior-art or formal hypothesis approval is claimed.

## Post-mortem and next step

Review execution complete; offline repair acceptance passed. Zero actual model/provider calls, zero spend, no credentials accessed, no allocation and no fit/validation/transfer cases. Prospective registration and execution evidence are separate from launch readiness. Text assertions were the declared visual fallback; no model trajectory was generated. Next: the owner carries out the separately planned live synthetic diagnostic and the remaining approvals, preserving failure evidence and the shared budget. A changed implementation or provider contract requires a new source-pinned assessment, not an unqualified reuse of this PASS.
