# Preregistration: memory-mix rescue on Claude (pool)

Owner: shadow (Sol lane `shadow/mix-claude-pool`), 2026-10-04. Written and pushed before any model call.

## Question

In a captured population after the committed (bad) agents are removed, does making a minority (1/3) of the honest
survivors short-memory (memory1: they remember only the last partner name) move the swarm back toward the original
convention more than an all-full-memory population, when every decision is made by Claude?

## Fixture (reused, not re-drawn)

- Roots: the four captured populations in [`../../capture-memory/freeze-claude/inputs.json`](../../capture-memory/freeze-claude/inputs.json)
  (tasks 160-163, seed 1, N=12, six committed agents removed, six honest survivors each with full raw history).
- Pairing schedules for 20 post-removal rounds: the fixed `schedules` stored in those roots.
- Prompt: freeze-claude system prompt and user prompt verbatim (raw chronological partner names, oldest first, no
  privileged last-event field).
- Conditions, both from the same root state:
  - `full`: all six survivors keep their full history.
  - `mix`: two of six (1/3) survivors, chosen by `random.Random("mix:<task_id>").sample`, are truncated to their last
    heard name and keep only the last name thereafter. Short ids are recorded in `scripted-reference.json`.
- 4 roots x 2 conditions = 8 episodes, 20 rounds each. Planned decisions: 456 episode + 12 qualification = 468.

## Model and transport

`claude-sonnet-5-5` through the local loopback Anthropic Messages pool (`127.0.0.1:18811`), same credential path as
freeze-claude `run.py`. max_tokens 16, default temperature. HTTP concurrency 4. Returned model id and usage are logged
per response. No other provider.

## Primary endpoint

Per root: d = (mix share_original[20] - mix share_original[0]) - (full share_original[20] - full share_original[0]),
share over the six honest survivors. Report mean d over 4 roots with a 95% paired root bootstrap (10,000 resamples,
seed 7). With only 4 roots the bootstrap has at most 35 distinct means; it is descriptive.

Reading rule: "rescue supported" only if mean d > 0 and the bootstrap lower bound > 0. Interval spanning 0 = no
evidence of rescue (inconclusive, not a null). Secondary: each arm's own change, per-round traces, switch counts.

## Scripted reference (computed offline before calls)

`scripted-reference.json` from `run.py prepare`, tanh rule beta=2.5 h=0.1 on memory mean:
- fixed draws: mean d = -0.042, CI [-0.250, +0.125], per root [0, +0.167, 0, -0.333]
- 500 Monte Carlo draws per root/condition: mean d = +0.007.
So at N=12 / 20 rounds the scripted rule predicts NO mixture rescue. A Claude rescue would be a departure from the
scripted rule, not a replication of it.

## Stop rules

- Qualification first: 12 decisions on fixed histories; pass needs >= 11/12 parseable (>= 90%). Fail = stop, write up.
- Backoff 20-30 s on any non-200; up to 4 attempts per decision. If > 50% of the first 20 attempts are 429/503/529,
  halt and write up as blocked. 400/401/403 halts.
- Any unparseable 200 reply in an episode ends that episode as failed (no resampling). Failed episodes are reported,
  and the primary is computed only over roots where both conditions completed (stated count).
- Hard ceiling 1,000 HTTP attempts. Hard stop at 23:30Z.
- Cost: unknown unless the pool returns usage; never asserted zero.
