# Discussion and memory v3 on Claude Opus 5.5

Prospective plan, 2026-10-04 UTC. Owner dmarz, operator `dmarz/v3-q0-opus`. Hub experiment
`discussion-v3-opus`, chain attempt `v3o-a1` (batches `v3o-a1-q0`, then `v3o-a1-s1`). Parents:
[Q0 on Haiku](../benchmark-v3/RESULTS-Q0.md) (`v3-q0-a1`), [D1](../benchmark-v3/RESULTS-D1.md) and
[D1-Opus](../d1-opus/README.md) (`d1o-a1`, fresh gate 12/12). Setup record: [SETUP.md](SETUP.md).
Pre-run assessment: [reviews/v3o-a1-pre.md](reviews/v3o-a1-pre.md). Status: **plan committed; no swarm model call made.**

## TLDR

The v3 swarm benchmark failed qualification on Haiku 4.5 (2/6 clean full-evidence decisions, 1/6 clean
reports-only votes, against 5/6 each) because the model picked infeasible options after extracting the facts
correctly. D1 showed the same failure for Sonnet 4.6, and D1-Opus showed Opus 5.5 does not have it (12/12 fresh
evidence-justified choices). This study reruns the v3 swarm qualification with the same shape as `v3-q0-a1`
(6 fresh worlds, 4 communication arms, clean and attacked evidence, 96 cases, 636 calls) on `claude-opus-5-5`.
If the unchanged software gate passes, the same process continues straight into S1: the same design on 24 fresh
worlds (2,436 calls), the first v3 comparison of independent votes, reports, private work and public discussion
with a model that passes the competence screen. Model and request configuration both change, so this is a new
configuration, never pooled with the Haiku run.

## Question and prediction

1. **Q0 (gate):** with a competent model, does the v3 instrument qualify? Unchanged gate from `bench_v3.analysis`:
   execution complete, at least 5/6 clean full-evidence diagnostics correct, at least 5/6 clean reports-only votes
   correct, zero missing usage.
2. **S1 (exploratory comparison, only after a Q0 pass):** across 24 fresh paired worlds, how do the four arms
   differ in clean accuracy, attacked target-vote rate and false-memory inheritance by the fresh parent?

Prediction, written before any swarm call on Opus: Q0 passes (D1-Opus 12/12 on fresh full evidence). In S1, clean
accuracy is high in every arm; on attacked worlds, vote abstention still does not protect memory, so the
reports-only arm passes the false target into parent memory in a majority of attacked resolvable worlds, as Haiku
did in 4 of 6. Public discussion reduces false-memory inheritance relative to reports-only by at least
10 percentage points. Any outcome, including no difference, is reported.

## Setup

- Instrument: the frozen `bench_v3` runner, worlds, contracts, scoring, analysis and replay, unchanged at this
  commit (the F1 and F2 scoring fixes of 6563e28 are included). New file `src/bench_v3_opus.py` adds the Opus
  request path, the fresh namespaces and the chain; `src/bench_v3_opus_selftest.py` tests it offline.
- Model: `claude-opus-5-5`, `thinking: adaptive` (cannot be disabled), `output_config.effort: high` (as D1-Opus),
  structured JSON-schema output, no temperature/top_p/top_k, `max_tokens` 16,000 (thinking counts against it),
  visible answer capped at 8,000 characters on the text block, thinking blocks filtered and never stored, refusals
  counted separately, no fallbacks, no retries, 600 s request timeout. Price USD 4 / USD 20 per million tokens.
- Worlds: Q0 54001–54006 (54001–54003 resolvable, 54004–54006 ambiguous; one of each family per stratum).
  S1 54101–54124 (first 12 resolvable, last 12 ambiguous; four of each family per stratum). Disjoint from dev
  10002–10007, tests 10101–10160, Q0 20001–20006, holdout 30000–30023 (closed), sidecar 40001–40012,
  Q1 50001–50006 (unopened) and D1-Opus 52001–52012; checked in the selftest.
- Server: dedicated `sim-dmarz-9`, exclusive claim `dmarz-v3-q0-opus`. One worker process, sequential calls.

## Protocol

One command starts the chain in the background on the server: (1) a one-call interface probe (a parent-phase
memory fixture, scored nowhere); stop if it does not return a parsed answer. (2) Q0, 636 calls, exact-source
replay audit, upload. (3) Software gate: `model_qualified` from the frozen analysis. Fail: stop, S1 never starts.
Pass: (4) S1, 2,436 calls, audit, upload. No retries or restarts; any interruption leaves the ledger for audit.
Hard caps: Q0 636 calls and a USD 400 reservation ceiling; S1 2,436 calls and a USD 1,500 reservation ceiling.
Reservations assume every call spends the full 16,000 output tokens and are never credited back, so the ceilings
are far above expected spend (about USD 13 for Q0 and USD 50 for S1 at D1-Opus's USD 0.021 per call).

## Metrics

Per stage: assigned/terminal/invalid calls, refusals, input/output tokens, `cost_usd` (reported to the hub), clean
full-evidence correct, clean reports-only correct, `model_qualified`. S1 per arm: clean vote accuracy, attacked
target-vote rate, false-memory target rate, parent unsupported and inherited-error counts, with worlds (not calls
or agents) as the independent units and paired-by-world arm contrasts. Visualization: the existing v3
deliberation frame and replay contract (`frame.json`, `replay.json`, `replay.html`), mapping `v3-deliberation-v1`
as used for `v3-q0-a1`, bound to run ids `discussion-v3-opus/v3o-a1-q0` and `-s1`.

## If Q0 fails

The chain stops itself. The most likely cause is not constraint application (D1-Opus passed it) but swarm-specific
behaviour: agents abstaining in reports-only ballots despite their own claims identifying a winner, as Haiku did
in four worlds. Next step: read the per-agent ballots against their endorsed claims; if abstention-despite-claims
dominates, test the response-contract change already proposed for D2 (a feasibility line per option before the
vote) on fresh worlds as a new attempt. Invalid outputs or refusals instead point at the adapter: fix offline,
probe, and rerun as a new attempt with new worlds.
