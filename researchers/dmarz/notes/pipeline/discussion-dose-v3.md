# discussion-dose-v3 (D2 diagnostic): decision package

Maintained by dmarz/results-analyst. Operator: dmarz/v3-d2-opus (sub-agent on halcyon), reviewer dmarz/fleet-monitor (same researcher), server sim-dmarz-3, claim `dmarz-discussion-v3-d2` to 15:33Z. Not a review. Last updated 2026-10-04T08:46Z.

## 1. Results so far

D2 `v3-d2-a1` **finished at 08:27:58Z: 72 of 72 valid**, USD 0.13 (results and post-run review on main, commit 0c2f38c6).

| Model | Canonical decisions | Single-option feasibility checks |
|---|---:|---:|
| Opus 5.5 (effort high) | 6 of 6 | 18 of 18 |
| Sonnet 4.6 | 5 of 6 | 16 of 18 |
| Haiku 4.5 | 5 of 6 | 16 of 18 |

Screens were 6 of 6 and 18 of 18, so Opus passed both and the other two failed both. Sonnet and Haiku miss the same two options, both sum-over-budget checks. On D1's original packaging the same worlds gave Haiku 2 of 6 and Sonnet 3 of 6, so the compact fact table removes most of their errors and leaves one arithmetic check. Six reused development worlds, one response per item.

## 2. Gate forecast

Done. D2 qualifies no model. sim-dmarz-3 is free after close-out.

## 3. Next run

- The swarm line is on Opus: discussion-v3-opus Q0 is running (see [discussion-v3-opus.md](discussion-v3-opus.md)). D2 does not gate it.
- D2's own follow-up, if a cheaper model is wanted later: the residual failure is a sum compared with a budget. A response contract that writes the sum before the feasibility answer is the one change to test, on fresh worlds, for Sonnet and Haiku only. Low priority while Opus qualifies.
- No successor is named for sim-dmarz-3.

## 4. Design notes for later runs

- D1, D1-Opus and D2 are three small screens (120, 72 and 72 calls) each with its own plan, rehearsal, review and server. Together they are under 15 minutes of model time. One diagnostic with all three models and both item types would have answered the same questions in one setup.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 3 and 4.
