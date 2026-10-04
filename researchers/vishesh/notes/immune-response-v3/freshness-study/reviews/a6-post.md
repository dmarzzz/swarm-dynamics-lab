# Immune Response — A6 qualification post-mortem

Retrospective owning-agent review, 2026-10-04. [Run](https://swarm-live.pages.dev/#/r/immune-response-v3%2F1004-193831-67f90f). Frozen source `4016ed91ceb5f999399abb719aa66e5f2d9172f9`; prospective [qualification plan](../QUALIFICATION-A6.md). [Reconciliation](a6-reconciliation.json), [quality review](a6-quality.json), [coverage figure](a6-coverage.png).

## Result and decision

**HOLD: qualification did not pass.** Three of eighteen permitted requests were dispatched. Two advisory responses succeeded with complete usage; the first controller request returned HTTP400. One episode started but none completed; five episodes and fifteen requests remained unstarted. There was no controller response or applied action. This is an operational/interface failure, not a measured failure of controller repair or restraint. No treatment effect is estimable and no retry or successor was launched.

The small qualification served its purpose: it exposed an unresolved hosted-interface gate before a larger comparison. Twenty-three offline tests and scripted reference success did not establish hosted acceptance of the revised schema.

## Full retained trace review

All three effective requests, both returned answers, both usage receipts and the terminal transport record were inspected. In healthy_fresh, all current checks were true. Gateway2 and worker2 share rpc-batch; worker2 reads schema-legacy; store1 supplies that format; gateway2 supports required bulk_checkout. Both advisors nevertheless recommended gateway1 and asserted incompatibility. That downgrade would break the current RPC pairing and remove the required feature. These are directly verifiable factual mistakes in two roles within one familiar world, not two independent replications or proof that a controller would follow them. The controller never returned an answer, so prose/action consistency and restart performance remain unmeasured.

The rejected controller request uses the repaired dependent schema with root-level anyOf; the two successful advisor requests use simple object schemas. Provider schema-subset incompatibility is a plausible explanation, **not a verified cause**. The relay retained HTTP400 but discarded the provider error details. Account/request constraints or another request-validation problem are not excluded. Do not claim that JSON Schema validity guarantees support by this hosted route. No additional paid diagnostic was dispatched.

## Accounting and evidence

Known new model cost USD0.002440; one request lacks usage. All three reservations, USD0.020187, remain counted. Original cumulative ledger: 408 requests, USD3.329282 reserved of USD8, including historical uncertainty. These reservations are not an actual-spend claim. No extra budget was needed or assigned. The newly available sim-shadow researcher allocation was used exclusively; no new machine was created. Existing shared-machine allocated cost is not separately measured. The quota-constrained new-machine request was cancelled to prevent duplicate provision.

The worker stopped; the local relay exited on its first error; the exact reverse tunnel was closed. Zero experimental Python processes and a closed remote relay port were verified before allocation release. The complete local transport trace, relay journal and unchanged ledger are retained. Seven hub artifacts were fetched and SHA256-matched. The hub index does not include the full transport trace; public reporting provides aggregate findings rather than claiming all raw traces are public. The request/usage audit reconciles all three IDs and hashes. The replay check contains zero transitions and must not be presented as positive evidence of native state replay.

## Visualization and next action

The coverage figure displays two returned calls, one failed call, fifteen unstarted calls, and zero completed episodes. There is no native time-series animation because no action executed; scripted frames would misrepresent this attempt. A future successful run retains the planned state/action/freshness animation mapping.

Decision: repair offline, keep larger collection on hold. First establish the hosted route's documented schema subset and design a lossless legal-action representation supported by it. Add safe allowlisted provider-error classification without logging arbitrary provider bodies, credentials or operator context. Preserve historical A6 unchanged. Then test every legal/illegal action mapping and the saved rejected payload offline, and propose a bounded hosted-contract qualification before spending again. Retain both factual-advice errors as substantive capability concerns; accepting a schema is not the same as passing repair and healthy-abstention gates. Any changed execution contract requires the corresponding owner decision before another attempt. Do not enlarge the swarm or relax the gate to obtain a favorable result.
