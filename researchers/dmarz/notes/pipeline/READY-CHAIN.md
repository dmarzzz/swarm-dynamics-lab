# Ready-chain contract, version 1

Written by dmarz/pipeline on 2026-10-04. A study that follows this contract can be prepared in full before a
server is free and then launched with one command on any free server. The private launcher that drives it
is `scripts/run-ready-chain.py` in the agentops repository. This file is the public half: what a study
directory must contain and how its code must behave. Nothing here launches a run or grants spending
authority; a run starts only when the orchestrator takes a reviewed request from the private run queue.

## Names

For a study `<study>` (lowercase, digits and hyphens):

| Thing | Value |
|---|---|
| Study directory | `researchers/dmarz/notes/<study>/` |
| Hub experiment id | `<study>` |
| Server claim id | `dmarz-<study>` (taken by the operator at launch; `experiment: <study>`, exclusive) |
| Stages | `S0` scripted, `P0` one-call interface probe, `Q0` qualification, `S1` main stage |
| Batch names | `s0-001`, `p0-001`, `q0-001`, `s1-001` (a repaired attempt gets a new number and a new pre-run review) |

## Files

```
README.md           plan; sections TLDR, Question and prediction, Setup, Protocol, Metrics; evidence block
SETUP.md            setup record from tooling/agent-experiments/templates/experiment-setup.md
preregistration.md  frozen comparison, stop rules, budget
design.yaml         frozen design: model, effort, factors, worlds, budget and per-stage max_calls
experiment.yaml     hub registration (metrics include episodes, invalid, model_calls, input_tokens,
                    output_tokens, cost_usd, qualification_passed and the primary metric)
READY.yaml          the machine-readable summary the launcher reads (below)
VISUALIZATION.md    mapping per tooling/agent-experiments/RUN-VISUALIZATION.md
RUN.md              operator runbook: the exact launcher commands with --host <server>
manifest.json       assignment manifest per stage: counts, assignment ids and packet hashes, digest
requirements.txt    pinned dependencies
reviews/chain-001-pre.md   pre-run review per RUN-REVIEW.md covering S0, P0, Q0 and S1 of this chain
src/                sim.py study.py provider.py worker.py coordinator.py chain.py analyze.py render.py
                    manifest.py selftest.py rehearse.py
```

`READY.yaml` (strings and integers only; the launcher validates every value):

```yaml
contract: ready-chain-v1
study: <study>
experiment: <study>
stages: [S0, P0, Q0, S1]
model: claude-opus-5-5
effort: low
max_calls: {S0: 0, P0: 1, Q0: <n>, S1: <n>}
max_calls_total: <sum>
usd_cap: <ledger cap on settled cost plus open reservations>
chain_timeout_seconds: <hard wall-clock limit for the whole chain>
selftests: <number of tests src/selftest.py runs>
source_hash: <study.source_hash() at the pinned commit>
```

## Stage behaviour

- `S0` makes no model call. It answers every assignment of the engineering worlds and the qualification
  fixtures with the scripted plurality rule and passes only if every row is valid, every invariant
  holds and the scripted qualification passes.
- `P0` is the first paid step: exactly one call, on a qualification packet outside the S1 worlds, at the
  frozen model settings. It passes only if the response parses, the model id matches, usage is reported,
  the stop reason is `end_turn` and the answer equals the expected values. Its measured input and output
  tokens are written to its summary and to the hub.
- `Q0` is the clean qualification with the thresholds frozen in `design.yaml`.
- `S1` is the comparison. One call per assignment, no retries.

Every stage is one hub run. A stage ends `done` only when all of its rows are valid and, for S0, P0 and
Q0, its gate passed (`qualification_passed: 1`). Otherwise it ends `failed`, with every assignment
recorded as completed, failed or not started. Both endings report `episodes`, `invalid`, `model_calls`,
`input_tokens`, `output_tokens` and `cost_usd` (actual dollars from reported usage) in the run's metrics.

## Chain

`python src/chain.py run --stages S0,P0,Q0,S1` runs on the server as one detached process:

1. For each stage in order: `coordinator.enqueue(sr, stage)`, then take that run from the hub queue and
   execute it in this process.
2. `coordinator.enqueue` is the software gate. It refuses a stage unless exactly one run of the previous
   stage exists at the same `source_hash` with status `done`, `invalid == 0` and
   `qualification_passed == 1`, and refuses a batch name that already exists (no replay).
3. A failed stage stops the chain. Nothing further is queued, the process exits non-zero, and
   `results/chain-status.json` names the stage and the reason. There are no retries and no agent is
   needed between stages; a repair is a new attempt with its own pre-run review.
4. `results/chain-status.json` is rewritten atomically after every transition:
   `state` (`running`, `stopped_at_gate`, `completed`), and per stage the run id, status, calls, tokens,
   dollars, start and end times.

`python src/chain.py status` prints that file plus the ledger totals. `python src/chain.py verify` checks
every uploaded artifact's checksum against the hub, recomputes every saved grade and the analysis from
the saved rows. Each prints exactly one JSON object as the last line of stdout; `verify` exits non-zero
when a check fails. Neither needs a credential.

`chain.py run` exits 0 when every requested stage is done, 3 when it stopped at a failed stage or gate,
and with another non-zero code on an internal error. It accepts any ordered contiguous sub-list of the
stages (`--stages S0` alone, later `--stages P0,Q0,S1`); the coordinator gates still decide whether a
stage may start. It runs from any working directory.

Run outputs go under the directory named by `STUDY_RESULTS_DIR` (default `<study>/results/`, which is
git-ignored). On a server the launcher points it outside the checkout so the checkout stays clean.
`python3 src/selftest.py` prints the standard unittest summary; the launcher's setup step compares the
number of tests and `study.source_hash()` with `selftests` and `source_hash` in `READY.yaml`.

Environment on the server (set by the launcher; never written to a file, an argument or a log):
`SWARM_MODEL_API_KEY`, `SWARM_MODEL_WORKSPACE_ID`, `STUDY_BUDGET_LEDGER` (path of the persistent ledger),
`STUDY_RESULTS_DIR`, `SWARM_SOURCE`. The hub address and token come from the server's own configuration.

## Budget

`design.yaml` carries `budget.max_calls` per stage and `budget.max_attempted_calls` for the study. The
ledger refuses a reservation that would exceed either, or that would take settled cost plus open
reservations over `budget.aggregate_usd`. Reservations use the free token-counting endpoint for input
and the full output limit. Dollars are not the gate for these runs (dmarz, 2026-10-04); the call caps are
hard, and actual calls, tokens and dollars are reported to the hub.

## Opus 5.5 request rules

The adapter sends `model`, `max_tokens`, `system`, `messages` and
`output_config: {effort: <frozen>, format: {type: json_schema, schema: ...}}` and nothing else. It never
sends `thinking`, `temperature`, `top_p`, `top_k`, `tool_choice`, a prefilled assistant turn or
`fallbacks`. `max_tokens` leaves several thousand tokens of room because thinking counts against it.
Responses carry thinking blocks before the text block; the adapter drops them and requires exactly one
text block. `stop_reason: refusal` is recorded as the failure category `refusal`. List price is USD 4 per
million input tokens and USD 20 per million output tokens.

## Offline evidence required before a study is called ready

1. `python3 src/selftest.py` passes on the builder's machine (no network, no model call).
2. `python3 src/worker.py --stage S0 --attempt <name>` passes offline.
3. `python3 src/rehearse.py --hub-dir <dir with hub.py and swarm_report.py>` passes. It starts a
   throwaway hub on 127.0.0.1, replaces the model endpoint with a local stub, and runs the chain twice:
   once through all four stages, and once with a stub that fails qualification, which must stop the chain
   before S1 with nothing queued for S1. It refuses to run against any hub that is not on 127.0.0.1. A
   rehearsal answer is never a sample and never leaves the machine.
4. `manifest.json` equals what `src/manifest.py` regenerates.
5. The pre-run review is on `main` and names the pinned commit and the source hash.

## Review wording

These runs are exploratory. dmarz waived cross-researcher review for them (relayed by dmarz/fleet-monitor,
2026-10-04). dmarz/fleet-monitor reads each package before it is queued; that is a same-researcher check.
No document may describe such a run as independently reviewed.
