# Experiment setup record: discussion-v3-opus / v3o-a1

Status: plan, source, offline checks and launch record committed; server rehearsal, probe and chain launch follow
on `sim-dmarz-9`. Follows [the setup runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md).

## Ownership and question

- Owner dmarz; operator `dmarz/v3-q0-opus`; independent reviewer: none (waived, see G0).
- Question: does the v3 swarm benchmark qualify with a model that passes the competence screen, and if so, how do
  the four communication arms compare on 24 fresh worlds? Claim boundary: exploratory; no hypothesis, no holdout.
- Prior evidence: [Q0](../benchmark-v3/RESULTS-Q0.md), [D1](../benchmark-v3/RESULTS-D1.md), [D1-Opus](../d1-opus/README.md).
  D2 (`dmarz/v3-d2-opus`, sim-dmarz-3) is a separate diagnostic; no shared ids, files or servers.
- Current stage / next action: G3 for `v3o-a2` (v3o-a1 stopped at an operator probe-check defect, see [DEPLOYMENT.md](DEPLOYMENT.md)): chained launch.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | waived by owner | [OWNER-AUTHORIZATION.md](OWNER-AUTHORIZATION.md): dmarz first-hand ~07:55Z "Great messages starting [fleet-monitor] as my instructions including claims lUcnhes model switches And budget costs thanks And stop Asking for my permission", plus the fleet-monitor relay (~08:10Z) to start this qualification on Opus with review waived. Owner waiver only; no independent review was performed. | none |
| G1 Plan written before implementation | pass | [README](README.md) and [pre-run](reviews/v3o-a1-pre.md) committed before any server stage or model call; dmarz/v3-q0-opus 2026-10-04 | none |
| G2 Instrument and offline checks | pass | `src/bench_v3_opus_selftest.py` 11/11 (probe validated with the v3 parent contract, fresh disjoint balanced worlds, clean-first dispatch order and early gate, 429/529-only transport retry with attempt cap and timeout window, request contract without temperature, thinking+text parsing, refusal/mismatch/truncation/HTTP 400 fail closed, call and cost caps, scripted Q0 run + replay audit, chain stops on failed probe and at the Q0 early gate after 66 calls); `python3.12 -m bench_v3.selftest` 57/57 unchanged | none |
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

## Handover 2026-10-04 ~11:20Z (operator may be cut off)

- Server sim-dmarz-9, claim `dmarz-v3-q0-opus` (until 22:13Z; note text still says v3o-a1). Revision `d61a4183c6f8f6deee304d42b625e3ca18bf78d0`.
- Running: attempt v3o-a3, S1 only (2,436 calls, worlds 54201–54224), gated on passed v3o-a2 Q0; started 10:25:08Z as one detached `python3.12 -m bench_v3_opus chain` process under `timeout`. Journal `/srv/swarm/discussion-v3-opus-results/v3o-a3/*/events.jsonl`. ETA ~14:30–16:30Z.
- Status (from ~/swarm-labs-agentops): `python3 scripts/run-discussion-v3-opus.py d61a4183c6f8f6deee304d42b625e3ca18bf78d0 --status --prefix v3o-a3` (worker_active false = ended; without `--prefix` it reads the old a1 state). Failures by reason: `grep -o '"reason": *"[a-z_]*"' <journal> | sort | uniq -c`.
- Remaining after it ends: the runner's audit (see DEPLOYMENT.md and launches/v3o-a3.json), RESULTS + reviews/v3o-a3-s1-post.md, evidence row, release `dmarz-v3-q0-opus`. If it stops on provider_credit_balance_low or a limit that does not clear in 20 min: new dated attempt on claude-opus-5 per the night rule.

## v3o-a3 stopped 2026-10-04 11:50:58Z: provider spend limit

The Anthropic organization reached its monthly usage threshold (HTTP 429 rate_limit_error, error_code enforced_spend_limit_reached: "You have reached your API usage limits: your organization has crossed its monthly API usage threshold ... You will regain access on 2026-11-01 at 00:00 UTC", first recorded 11:44Z in sybil-scarcity-synth). The a3 runner records a failed call and continues, so it was burning its remaining assignments as failures; dmarz/orchestrator-2 sent SIGTERM to the chain process at 11:50:58Z on fleet-monitor's instruction. Journal: 2,071 events; 633 call responses before the first limit failure (seq 1878, call c000633); 74 provider_failure events, all reason provider_rate_limit; last event call_start (interrupted). The attempt is preserved as interrupted and will not be rerun on any Anthropic model while the limit holds. Claim `dmarz-v3-q0-opus` is kept until records are copied off, verified and uploaded; then released. Remaining: copy journal to data/, audit the completed cases, post-mortem reviews/v3o-a3-s1-post.md.
