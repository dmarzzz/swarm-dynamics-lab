# Q4 follow-through budget authorization

**Current review status:** one researcher review is required and Dmarz’s design feedback satisfies it by owner instruction. The separate dossier review is retired. Q4 means the next qualification run, not another review. See [review resolution](REVIEW-RESOLUTION.md). Historical pending-review entries below describe earlier states.

2026-10-04 UTC: the user approved the pending request for up to USD 10 additional model spending and said someone will review the dossier. This is budget approval, not a completed independent review or a waiver of that review.

The existing shared authority was updated atomically from USD 45 to USD 55 under unique authorization `influence-q4-user-additional-10-2026-10-04`. Existing reservations remain USD 44.902316; unallocated authority at update was USD 10.097684. No old reservation, call count or lease was reset/refunded. The unique authorization record prevents adding the same increase twice. No model request was dispatched during this update.

Use this increase for the reviewed Q4 qualification and eligible narrow comparison. Before paid dispatch, reserve a non-overlapping host quota from the authority; the shared available balance is not an exclusive lease. The old USD 1.40 lease remains bound to its old allocation and must not be copied to a new host. Q4 has a pessimistic USD 3.15392 request envelope, with one transient retry per nominal call. Later stages require checking remaining quota and exact-source qualification; the USD 10 increment is an aggregate maximum, not USD 10 per stage.

Review task `review-influence-q4-dossiers` remains open at this update. The prior sim-dmarz-3 host is now claimed by another experiment. Recheck the private fleet and obtain a fresh exclusive allocation after review; do not reuse its expired allocation, interrupt its current workload, or provision against another owner's account. No infrastructure spending increase was requested or inferred from the model-budget approval.

Next: incorporate the reviewer verdict, freeze the reviewed source/config/dossiers, claim an idle authorized dedicated machine, reserve the finite quota, test the deployed source, and launch Q4. Advance only with all twelve valid acceptable outcomes under the exact matching signature. Preserve every failure and adverse decision.
