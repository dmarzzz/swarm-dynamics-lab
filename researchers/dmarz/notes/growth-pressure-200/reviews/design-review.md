# Astra Ultra design review — growth-pressure-200 v1

2026-10-04. Review by the owning dmarz/astra-ultra-review session with three parallel subagents checking economics, execution arithmetic and inference. **Same-researcher design review only**; not external validation, independent researcher approval, an implementation audit or native qualification.

## Changes incorporated before publication

- Raised the fixed potential-rival slots from the earlier conversational example of 6% capacity to 11%. At comparable utilization they can demonstrate actual levy avoidance immediately; 8% ordinary focal challengers face the growth-dependent choice. Capacity share still does not guarantee sales share.
- Added bounded owner-level cost advantages, reinvestment, depreciation and price pressure. Proportional reinvestment alone would not establish changing shares. No ordinary growth or cheating behavior is forced.
- Fixed the four potential-rival IDs across all doses, preserving all starting capital. Primary zero versus four; one versus zero is secondary. No claim that dose holds adversarial capital constant.
- Kept 20 continuation rounds, spending replication on 16 isolated markets rather than expanding models or scenarios. Market-level independence depends on actual isolation; the implementation must prove it.
- Retained every assigned focal, including baseline evaders and owners that never cross 10%. Distinguished new conversion from sustained continuation behavior, and assigned seeder dose from realized exposure.
- Clarified net operating cash profit for investment: registration and accrued overhead included; investment and depreciation excluded. Unpaid overhead remains a liability deducted from terminal wealth, so default does not create free terminal assets.
- Added an exact conservative interval for all-zero paired differences; bootstrap [0,0] must not be advertised as certainty. Unknown primary outcomes produce bounds across all assigned market pairs, never complete-case inference.
- Qualified both the 800-call opening wave and the 2,400-call continuation wave before main collection. These are observed durations, not estimated p95s. Added one global quota/budget governor and deadlines that include qualification, retries, draining and closeout.

## Arithmetic review

- Main decisions: `4 × 200 × (5 + 3 × 20) = 52,000`.
- Qualification decisions: `48 + 8 × 6 + 800 + 2,400 = 3,296`.
- Planned total: `55,296`; at most `553` additional transport attempts; maximum `55,849` HTTP attempts.
- At opening-wave 60 seconds and continuation-wave 90 seconds, `1.25 × (5 × 60 + 20 × 90) = 2,625 seconds`, inside the 2,640-second main window.
- Historical per-decision planning range gives approximately $373–375 before retries; the previous maximum-context mean gives approximately $497. Neither is a current quote or a fresh spending allowance.

## Remaining limitations

The economic calibration and compact packet are unrun. Seed execution, legal growth opportunities, accounting, insolvency and main-stage throughput must qualify. Current source/model/price bindings, shared remaining funds and machine allocations are absent. Twelve machines cannot overcome an account quota. The comparison estimates the total effect of competing against assigned evaders, not isolated social imitation or a universal tipping threshold. One scenario family and model remain exploratory.

No simulation, model request or server operation was performed for this review. See [SETUP](../SETUP.md) for the actual gates and next action.
