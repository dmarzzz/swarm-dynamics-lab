# Post-mortem: q0-012

- Experiment / owner / stage / date: compositional-safety / dmarz (operated by dmarz/compositional-opus) / Q0, first stage of chain q0-012 → p1-004 / 2026-10-04 UTC.
- Pre-run assessment: [q0-012-pre.md](q0-012-pre.md) at source `e82617090e20508596b252219d190d6f2a56c41e` (design v11). Records: [records/q0-012](../records/q0-012/).
- Disposition: **stopped by the operator at 10:14:49 UTC to add billing-outage handling before a five-hour pilot; no qualification result.** p1-004 never started. Next action: `repair-and-rerun` as the chain [q0-013](q0-013-pre.md) → [p1-005](p1-005-pre.md) under design v12.

## What ran

Launched 10:11:30 UTC. 6 of 24 episodes finished, all on root 247, all valid and safe; 44 calls, **USD 0.396416**; no 429, 529 or 400 responses, no capacity waits. The open 247 D2 benign hub run was marked failed with its cost.

## Why it was stopped

dmarz/fleet-monitor relayed at about 10:14 UTC that the account's credit balance ran out from about 10:09 to 10:11 UTC: other Opus lanes received HTTP 400 with a credit-balance message. Under design v11 a 400 is final, so a recurrence during P1 would turn assignments into invalid episodes although no model output was involved. Stopping after six episodes cost about four minutes and USD 0.40; adding the rule after P1 had started would have cost far more.

The relay also asked for a 429/529 resend rule. v11 already has one (resend only on 429 and 529, honouring `retry-after`, up to 10 sends and 300 seconds per call, counted per call under one reservation). It is kept rather than reduced to two resends because the 10:06 to 10:11 UTC drain by another lane lasted about four and a half minutes.

## Next run

[q0-013](q0-013-pre.md) → [p1-005](p1-005-pre.md) under design v12.
