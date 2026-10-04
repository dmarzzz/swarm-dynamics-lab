# discussion-dose-v3 (D2 diagnostic): decision package

Maintained by dmarz/results-analyst. Operator: dmarz/v3-d2-opus (sub-agent on halcyon), reviewer dmarz/fleet-monitor (same researcher), server sim-dmarz-3, claim `dmarz-discussion-v3-d2` to 15:33Z. Not a review. Last updated 2026-10-04T08:00Z.

## 1. Results so far

- D1 (`v3-d1-a1`, 05:01Z): 120 calls, USD 0.75. Sonnet 3 of 6 on both clean gates, Haiku 2 of 6 and 1 of 6. Neither cleared 5 of 6. Both models copied every input value correctly and then chose infeasible options.
- D2 (`v3-d2-a1`: canonical decisions plus single-option feasibility checks, 24 items x Haiku, Sonnet and Opus = 72 calls) is being built. As of 07:35Z the agent file says no model call until the pre-run review is on main and the reviewer says go. `benchmark-v3/d2/` is empty on main and no D2 run is on the hub.

## 2. Gate forecast

Nothing is running. When it runs, 72 calls should take 5 to 10 minutes (D1-Opus is doing 72 Opus calls in about 8 minutes).

## 3. Next run

D2 answers one question: is the failure in checking one option's feasibility (atomic) or in composing the checks into a choice (canonical)? Its plan already maps outcomes to proposals (D2-PLAN.md lines 119-124). What changes tonight is that D1-Opus (see [discussion-v3-d1-opus.md](discussion-v3-d1-opus.md)) reports first, at about 08:03Z.

- **If D1-Opus passes its fresh gate:** the swarm line moves to Opus and the next run is a v3 swarm qualification on Opus. D2 then explains the Haiku and Sonnet failures and is no longer on the critical path. It is still cheap (72 calls); run it, but do not let the Opus swarm plan wait for it.
- **If D1-Opus fails:** D2 becomes the deciding diagnostic for all three models and should launch as soon as its review is on main. Atomic fails: the task wording or the constraint encoding is the problem; fix the instrument. Atomic passes and canonical fails: change the response contract (a feasibility line per option before the choice) and test on fresh worlds.

Opus request rules for the D2 Opus arm: [LESSONS.md](LESSONS.md) item 3. The D1-Opus adapter on main (commit 573c4103) is a working reference.

## 4. Design notes for later runs

- D1, D1-Opus and D2 are three small screens (120, 72 and 72 calls) each with its own plan, rehearsal, review and server. Together they are under 15 minutes of model time. One diagnostic with all three models and both item types would have answered the same questions in one setup.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 3 and 4.
