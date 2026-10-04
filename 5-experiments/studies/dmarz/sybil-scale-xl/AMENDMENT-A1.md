# Amendment A1: Opus 5.5, trimmed design (2026-10-04)

Recorded by dmarz/scale-xl before any paid call of this study. The Haiku v1 manifest ran only its free scripted S0 ([fleet-s0-001](reviews/fleet-s0-001-post.md), run 33d602fe); its Q0 and S1 were never launched and are closed.

## Authority

- dmarz, about 07:36 UTC, relayed by dmarz/fleet-monitor: "use opus for everything going forward please".
- dmarz, about 07:50 UTC, choosing among cost options in this session: "Opus, trimmed (~$200–270)". The full design on Opus was estimated at USD 640–900, above the remaining shared allowance (about USD 340 of USD 500, with about USD 160 already reported on the hub).

## Changes

| Item | v1 (Haiku) | A1 |
|---|---|---|
| Model | claude-haiku-4-5-20251001 | claude-opus-5-5 (confirmed with the Models API: 1M input, 128k output) |
| Sampling / thinking | temperature 0, no thinking | no temperature (the model rejects it); adaptive thinking, always on; `output_config.effort: low` |
| Output limit | 500 tokens | 8,000 tokens (covers thinking) |
| Prices | $1 / $5 per M | $4 / $20 per M (official pricing, 2026-10-04) |
| Verification arms | no_verification, degree, random, coverage | random, coverage |
| Badge modes | masked, visible | visible |
| S1 conditions per world and size | 28 | 8 (2 arms × fixed/proportional checks × attacker pass 0.10/0.90) |
| Calls | 48 Q0 + 2,016 S1 | 24 Q0 + 576 S1 |
| Reservation | request bytes as an input-token upper bound | input tokens from the free count_tokens endpoint, +2% +64 tokens, plus the full output limit |
| Ledger cap | sum of reservations ≤ USD 500 | settled actual cost of answered calls plus full reservations of open or failed calls ≤ USD 330 |
| Batch names | s0-001, q0-001, s1-001 | s0-a1, q0-a1, s1-a1 (new runtime source hash; the Haiku S0 does not qualify A1) |

Sizes, worlds, graph construction, packets, prompt, schema, evaluator and analysis are unchanged.

## What the trim keeps and loses

The primary contrast (coverage, visible, pass 0.10, proportional minus fixed at N=8,748) and the coverage-versus-random comparison at equal budget stay in. Degree selection, the no-check baseline and the hidden-badge contrast are dropped. They answered parent-study questions (degree excludes specialists; badges have no clear large-N effect) that the parent already measured at 972.

## Comparisons

At N=972 every A1 assignment has the same id and packet as the parent Haiku S1 (run sybil-scale-api/56defc84), so the 972 cells give a paired, world-level Opus-minus-Haiku contrast. It is a model comparison, not a test–retest anchor. Cohorts are never pooled. Thinking is an additional difference between the two models and is not separated from model identity.

## Cost estimate

Measured basis: the parent's Q0 used 649,312 input tokens for 64 calls, about 36 Haiku tokens per report. Opus 5.5 uses a newer tokenizer, so 1.0–1.35× as many tokens is assumed.

- S1: 24 worlds × 8 conditions × (486 + 1,458 + 4,374 reports) ≈ 43.7M Haiku-equivalent tokens, giving 43.7–59M Opus tokens: USD 175–236.
- Q0: 24 calls, the same packet sizes: USD 7–10.
- Output, including thinking at effort low: 600 calls × 300–2,000 tokens × $20/M: USD 4–24.
- **Total: about USD 186–270.** The ledger stops dispatch at USD 330 of settled cost plus open reservations. Q0's measured usage refines this estimate before S1, and S1's pre-run file records it.

## Interface checks (2026-10-04, after dmarz/fleet-monitor's Opus 5.5 request rules)

The adapter omits `thinking`, `temperature`, `top_p`, `top_k`, `tool_choice` and prefill; sets `output_config.effort: low` beside the JSON schema; gives 8,000 output tokens of room; filters `thinking` blocks before parsing; records `stop_reason: refusal` as its own failure category `refusal`; and does not send `fallbacks`. Before Q0, one interface probe call (one N=972 qualification packet, outside the S1 worlds) must return a parsed answer; its cost and usage are recorded in the Q0 pre-run file.
