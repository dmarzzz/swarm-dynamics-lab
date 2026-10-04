# Experiment setup record: discussion-v3-opus / v3o-a1

Status: plan, source, offline checks and launch record committed; server rehearsal, probe and chain launch follow
on `sim-dmarz-9`. Follows [the setup runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md).

## Ownership and question

- Owner dmarz; operator `dmarz/v3-q0-opus`; independent reviewer: none (waived, see G0).
- Question: does the v3 swarm benchmark qualify with a model that passes the competence screen, and if so, how do
  the four communication arms compare on 24 fresh worlds? Claim boundary: exploratory; no hypothesis, no holdout.
- Prior evidence: [Q0](../benchmark-v3/RESULTS-Q0.md), [D1](../benchmark-v3/RESULTS-D1.md), [D1-Opus](../d1-opus/README.md).
  D2 (`dmarz/v3-d2-opus`, sim-dmarz-3) is a separate diagnostic; no shared ids, files or servers.
- Current stage / next action: G3 for `v3o-a1`: rehearsal, then the chained launch.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | waived by owner | [OWNER-AUTHORIZATION.md](OWNER-AUTHORIZATION.md): dmarz first-hand ~07:55Z "Great messages starting [fleet-monitor] as my instructions including claims lUcnhes model switches And budget costs thanks And stop Asking for my permission", plus the fleet-monitor relay (~08:10Z) to start this qualification on Opus with review waived. Owner waiver only; no independent review was performed. | none |
| G1 Plan written before implementation | pass | [README](README.md) and [pre-run](reviews/v3o-a1-pre.md) committed before any server stage or model call; dmarz/v3-q0-opus 2026-10-04 | none |
| G2 Instrument and offline checks | pass | `src/bench_v3_opus_selftest.py` 10/10 (fresh disjoint balanced worlds, clean-first dispatch order and early gate, 429/529-only transport retry with attempt cap and timeout window, request contract without temperature, thinking+text parsing, refusal/mismatch/truncation/HTTP 400 fail closed, call and cost caps, scripted Q0 run + replay audit, chain stops on failed probe and at the Q0 early gate after 66 calls); `python3.12 -m bench_v3.selftest` 57/57 unchanged | none |
| G3 Current attempt admission | pending | launch record `launches/v3o-a1.json` (source hashes, caps, authorization digest); claim `dmarz-v3-q0-opus` on sim-dmarz-9 | rehearsal and probe on the server, then chain |
| G4 Qualification before scientific escalation | software gate | Q0 `model_qualified`; S1 starts only on a pass | automatic |
| G5 Reconciliation and closeout | pending | | audit, post-mortem, claim release after the chain |

## Design and instrument index

- Plan [README.md](README.md); pre-run [reviews/v3o-a1-pre.md](reviews/v3o-a1-pre.md).
- Source: `../src/bench_v3_opus.py` (new) over unchanged `bench_v3/*`, `tasks.py`, `providers.py`.
- Units: Q0 6 worlds, S1 24 worlds (independent units); arms paired within world.
- Model/config: `claude-opus-5-5`, adaptive thinking, effort high, no temperature, max_tokens 16,000, 600 s, no retries, no fallbacks.
- Visualization mapping: `v3-deliberation-v1` (pre-run review).

## Current attempt admission

Operations entry: manual (no registry adapter).

| Operation | Exact command or unsupported reason | Evidence |
|---|---|---|
| Offline validation | `cd src && python3.12 bench_v3_opus_selftest.py && python3.12 -m bench_v3.selftest` | G2 |
| Prepare | agentops `python3 scripts/run-discussion-v3-opus.py <rev> --prepare` | pending |
| Rehearse (no model) | agentops `python3 scripts/run-discussion-v3-opus.py <rev> --rehearse` | pending |
| Launch chain | agentops `python3 scripts/run-discussion-v3-opus.py <rev>` | pending |
| Status | agentops `python3 scripts/run-discussion-v3-opus.py <rev> --status` | pending |
| Resume | unsupported by design; audit the saved ledger and start a new attempt | n/a |
| Close out | audit per stage (`python3 -m bench_v3_opus audit DIR`), post-mortem, release claim | pending |

- Budget authority: dmarz shared model budget; owner removed cost as a gate (relayed 07:42Z) and asked for running totals; `cost_usd` reported to the hub per stage.
- Credentials: dmarz Anthropic key via SOPS (`discussion-dose.sops.env`), ssh stdin into process memory only.
- Allocation: `sim-dmarz-9` (released by D1-Opus), exclusive claim `dmarz-v3-q0-opus`.
