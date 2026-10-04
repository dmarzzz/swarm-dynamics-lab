# 2026-10-04 dmarz/pipeline-verify

- 10:35Z Started as builder for research program v5 line V (`verify-cost-qwen`) under dmarz/pipeline. Read the builder briefs, AGENTS.md, READY-CHAIN.md, LESSONS.md, the program text, the phantom-coast PC5 contract, engine, plan, post-mortem and next-iteration note, and the reference packages (sybil-scarcity-opus, quota-splitting at 6b9adefa, the OpenRouter reference adapter).
- 10:42Z Plan pushed before any code: README, preregistration, design.yaml, experiment.yaml, SETUP.md, evidence registry row. Offline only; no model call, no server.
- 11:06Z Instrument, scorer, chain and rehearsal pushed as work in progress (a standby builder also committed the same files as f623847b while this session was rate-limited; nothing was lost).
- 11:50Z Code pinned at fa61358a (source hash 72895482): revised reference adapter 639e9501 taken unchanged, 84 selftests, offline S0 144/144, rehearsal 33/33 checks in 47 s. READY.yaml, RUN.md, VISUALIZATION.md, pre-run review chain-001 pushed. Nothing launched, no model call.
- Surprises: the first reference adapter could not resume a single-call stage inside its exact call cap (a billing stop leaves reservations behind); the lead's revision voids them. Row field `error` (the error probability) collided with the failure category; the category is now `failure`.
- Next: dmarz/fleet-monitor's same-researcher check, then the run-queue request by the lead.
- 12:00Z Attempt 001 ran (operator dmarz/fleet-monitor) and stopped at Q0: 24 valid, prose 10 of 12, table 8 of 12 optimal. Read the post-mortem and records.
- 12:45Z Attempt 002 (the one bounded repair) prepared: cost-then-choice answer, validation rules fixed in advance (13 tolerated forms, 13 invalid forms tested), set b, code commit 35404c24, source hash ef40246d, 87 selftests, rehearsal 37 of 37 checks. Pre-run review reviews/chain-002-pre.md, READY.yaml names it. Nothing launched, no model call.
- Surprise: storing rows with sorted keys lost the returned object's key order; the rehearsal's verify caught it; the object is now stored as JSON text.
