# R2 S1 pre-run assessment

2026-10-04, shadow/sol-cm2, same-author. Disposition **diagnostic-only, ready for the frozen comparison**. S0 ran 19:51:04Z to 19:51:15Z under published revision 29ddcfacd4d593669328984c747f32994c6d317b and AMENDMENT-R2.md. No S1 calls preceded this assessment.

## Qualification and reconciliation

- R2 S0: 12 assigned, 12 started, 12 terminal, 12 valid, 12 unanimous-name choices. Original threshold 12 valid and >=11 correct passes without any prompt/scoring repair.
- Every receipt reports `openai/gpt-4o-mini`; providers are Azure (7) and OpenAI (5). Frozen requests did not pin an upstream provider, so this is an OpenRouter-route diagnostic rather than a single-backend experiment. Both named providers satisfy the frozen parameter/price routing contract. Routing variability is a limitation, not silently treated as a controlled variable.
- Allowed first-token mass ranges 0.9999999255 to 1.0000000252, within the original numeric tolerance. Exact choices and logprobs are retained in results-r2/journal.jsonl.
- R2 reported S0 cost USD 0.000423, all 12 cost receipts present. Cumulative diagnostic: 13 starts including v1 HTTP403, USD 0.65 retained reservation, prior actual USD 0.05 exposure unresolved. The old denial remains separate and is not a valid observation.
- The full R2 run would reach 157 cumulative calls and USD 7.85 retained reservation, below USD 8. No retries, alternate endpoint, pool, key rotation or limit changes.

## Scientific stage and controls

Admit exactly the original 144 frozen assignments over 24 synthetic histories with six paired renderings. Input SHA-256 c9d24c92ff32abbdd3c961bb4446f07edf60ba9aff330417b5436b4cc71f2639. Use the identical qualified instrument, random order, behavioral scorer, 0.10 practical threshold, 10,000-history bootstrap and missingness bounds. At least 20 valid primary history pairs are required for a complete diagnostic. The original plan, amendment and source will be publicly byte-verified again before dispatch.

Offline checks: 8 original tests and 3 successor tests pass (11 tests in the successor suite include the 8 inherited cases). Successor tests cover cumulative carry-forward, source input hash, provider receipt, exact unchanged behavioral scoring, native-loop durable reservation before dispatch, immediate HTTP400 halt and HTTP429 halt with Retry-After retention. `lab.py check`: 0 errors, 5 unrelated existing library-link warnings.

Visualization mapping remains PLAN.md and AMENDMENT-R2.md: static per-history majority probability across six presentations, invalid/missing cells crossed, journal progress rather than a fictitious swarm animation. The saved-data checker will independently recompute scores, denominators, contrasts, intervals and dollars.

Limits remain explicit: synthetic indexed histories, disclosed true last event, no natural-history replay, no interacting swarm, no causal account of prior cross-model recovery, no independent research review. Qualification establishes only this instrument's unanimous controls. Stop rules and the earlier 21:25Z dispatch deadline remain unchanged.
