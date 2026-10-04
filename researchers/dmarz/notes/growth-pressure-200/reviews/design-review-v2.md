# Design review — v2 seeding × peer messaging

**Astra Ultra · 4 October 2026.** Same-researcher review by the owning dmarz/astra-ultra-review session, with separate subagents auditing inference and resource arithmetic. This is not independent researcher approval or native qualification. [Original v1 review](design-review.md) · [Amendment](../AMENDMENT-02.md).

## Reviewed contract

A = 0 assigned evaders / messaging off; B = 0/on; C = 4/off; D = 4/on. Three 200-owner batches each contain four isolated markets of 50. Five silent common opening rounds precede the four-way fork; every continuation runs 20 rounds.

Primary D − B. Secondary interaction (D − B) − (C − A), with all four arms resampled jointly at the market level. Twelve market pairs supply 24 focal owners and 552 fixed ordinary owners per arm; owners and decisions are not additional independent units.

## Findings incorporated

- The communication invitation is identical across arms. Only channel availability changes; ordinary goals and public economic observations remain available throughout. Seeders have no extra message budget or recruitment objective.
- Use “no separate bonus” for sending or persuading: messages may indirectly improve terminal wealth. Explicit send/pass makes communication salient without forcing a desired quotation or another model call.
- Off-channel messages cannot be delivered, and a blocked message does not erase valid economic actions. On-channel messages arrive next round, before action selection; no same-round back-and-forth or cross-branch memory leakage.
- A self-interested evader may keep the strategy private. Zero messaging or recruitment is retained, and is not a failed gate that permits new persuasion instructions.
- Point estimation requires every outcome used by that contrast to be known. Otherwise retain every market and report explicit bounds. Unknown A/C outcomes do not silently remove a known B/D pair from the primary contrast.
- The primary contrast has range [−1,1]; the interaction has range [−2,2]. All-zero reference bounds are approximately ±22.1 and ±44.2 percentage points, respectively. A degenerate bootstrap is not presented as certainty. Fewer market pairs and the wider interaction range limit precision.
- New-firm eligibility is fixed prospectively: registration at t, investment/transfer eligibility at t+1, added capacity productive at t+2. No extra owner, model call or resource is created.

## Arithmetic and publication checks

- Main: `3 × 200 × (5 + 4 × 20) = 51,000` decisions.
- Qualification: `48 + 8 × 6 + 600 + 2,400 = 3,096` decisions.
- Planned: `54,096`; ceiling of 1% additional attempts: `541`; maximum transport attempts: `54,637`.
- Twelve workers serve the twelve continuations. Opening load wave is 600 decisions; continuation wave is 2,400, balanced between messaging on and off.
- With observed opening/continuation wave limits of 60/90 seconds, the main projection with 25% margin remains `2,625 seconds`, or 43m45s. Qualification and closeout remain inside the one-hour execution target.
- Historical planned-call estimates are about $365–367, or $486 at the predecessor's maximum-context mean, before retries or existing portfolio spend. These are estimates, not verified current prices or a new budget.

The offline validator checks the factorial contract, silent opening, count arithmetic, retry ceiling, worker/load-wave matching, deadlines, token caps, uncertainty formulas and local document links. Its reviewer also checked malformed factorial, retry, denominator and interaction configurations. These software checks are not simulated economic evidence.

No material scientific-contract mismatch was found in the revised PLAN and design.json. Current quota, budget, economic reachability, native competence, source bindings and machine allocation remain unverified. No run or provider request was launched for this review.
