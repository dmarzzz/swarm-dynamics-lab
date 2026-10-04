# Experiment setup record: soc07-private-judgments-v2 (design v2)

Copied from [the setup template](../../../toolkit/agent-experiments/templates/experiment-setup.md) and filled for this study. Runbook: [EXPERIMENT-SETUP.md](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md). Status: prepared; not launched; not launch authorization.

## Ownership and question

- Owner / operator / design reviewer / review independence: dmarz / dmarz/orbital-orchestrator / dmarz/fleet-monitor reads the package (same researcher) / cross-researcher review waived by dmarz ([launch/review-waiver.md](launch/review-waiver.md)).
- Question, decision, primary contrast and claim boundary: README "Question and prediction"; PRIVATE minus PUBLIC team success; exploratory only.
- Research status: exploratory instrument (no reviewed survey, no accepted hypothesis).
- Previous study and lessons incorporated: v1 [soc07-private-judgments](../soc07-private-judgments/README.md): ceiling at S1-R on Opus 5.5 (run 807dfab8); lessons 1 (caps sized for the whole ladder before qualification), 3 (Opus request shape, probe first), 4 (chain the stages), 6 (read misses before changing anything), 8 (429/529 retry) in [pipeline/LESSONS.md](../pipeline/LESSONS.md).
- Current stage / next action / blocker: G3 pending. Next action: dmarz's go, then "Launch" below. Blocker: approval record, server and claim.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass (exploratory; waiver) | README; waiver; 2026-10-04, dmarz/orbital-orchestrator | none |
| G1 Plan written before implementation | pass | README, [preregistration.md](preregistration.md), [reviews/chain-001-pre.md](reviews/chain-001-pre.md), committed before any v2 run | none |
| G2 Instrument and offline checks | pass | Self-test 59 run, OK (0 skipped); local offline S0 73 of 73 checks, 0 model calls (orbital-one, 2026-10-04); fingerprint in chain-001-pre | server S0 repeats it as the first chain stage |
| G3 Current attempt admission | pending | — | dmarz's go, approval record, fresh server, claim |
| G4 Qualification before scientific escalation | pending | P0 and S1-Q are software-gated before S1-R | — |
| G5 Reconciliation and closeout | pending | — | post-mortem per stage |

## Design and instrument index

- Plan and amendments: README; `design.json` (`design_version: v2`, amendment V2); `execution.json` (launch manifest m3, budget, gates incl. `s1_informative`).
- Independent units: worlds (S1-Q 12, S1-R 24, S1-L 24); five agents per world in S1-L; two repeats; five arms.
- Splits: seed roots 731071 / 731072 (holdout, unused) / 731073; separate seed keys per stage.
- Generator, prompts, scorer, contexts: `src/generate.py`, `src/prompts.py`, `src/score.py`, `src/contexts.py`; hash groups in `src/config.py`.
- Offline checks: `python3 src/selftest.py`; `python3 src/worker.py --stage s0 --attempt <name>`.
- Launcher gate integration: `src/coordinator.py` (`PREREQUISITE`: p0 after s0, s1q after p0, s1r after s1q, s1l after s1r, each at the same fingerprint with `gate_passed = 1`); `src/launch.py` (approval record pins fingerprint, this pre-run assessment and the waiver).
- Visualization mapping: [reviews/chain-001-pre.md](reviews/chain-001-pre.md#visualization-mapping).

## Current attempt admission

Operations entry: manual (agentops launcher).

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | `python3 src/selftest.py`; `python3 check_plan.py` | see G2 |
| Prepare named stage | `scripts/run-soc07-private.py <commit> setup --study v2 --host <server> --agent dmarz/orbital-orchestrator` (agentops) | — |
| Dispatch named stage | `scripts/run-soc07-chain.py <commit> --study v2 --stages s0,p0,s1q,s1r,s1l --host <server> --agent dmarz/orbital-orchestrator` | — |
| Resume interrupted execution | unsupported: a stage is never resumed; a repair is a new attempt (`--attempt 2`) with its own pre-run note | — |
| Analyze saved evidence | `scripts/run-soc07-private.py <commit> status|verify --study v2 ...` | — |
| Stop and close out | stop the chain unit; the worker exits within its stage; release the claim after uploads | — |

## Launch (operator runbook, from the agentops repository root)

1. Server: a fresh dedicated box from dmarz's fleet (one experiment and one run per server). If none is idle, add one to `fleet.yml` on main, `tofu plan` targeted at that box only, apply, commit `generated/dmarz.json`, `task provision HOST=<server>` (wait for the first-boot apt lock), `~/swarm-orchestrator/refresh-ssh.sh`.
2. Claim: `python3 scripts/agentops.py claim dmarz-soc07-private-judgments-v2 --servers <server> --by dmarz/orbital-orchestrator --until 10h --experiment soc07-private-judgments-v2 --note "SOC-07 v2 chain S0,P0,S1-Q,S1-R,S1-L; Opus 5.5; USD 150 cap"`.
3. Approval (only on dmarz's go, quoting it): in swarm-lab, `python3 5-experiments/studies/dmarz/soc07-private-judgments-v2/launch/make_approval.py --stages p0,s1q,s1r,s1l --go "<dmarz's words, time, where>"`, commit and push; call the commit `C`.
4. Setup: `python3 scripts/run-soc07-private.py C setup --study v2 --host <server> --agent dmarz/orbital-orchestrator`. The printed `source_hash` must equal the fingerprint in chain-001-pre.
5. Chain, detached so it survives the operator session: `sudo systemd-run --unit soc07-v2-chain --uid=dmarz --gid=$(id -g) --setenv=HOME=$HOME --setenv=PATH=$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin --working-directory=$HOME/swarm-labs-agentops -p StandardOutput=append:$HOME/swarm-orchestrator/logs/soc07-v2-chain.log -p StandardError=append:$HOME/swarm-orchestrator/logs/soc07-v2-chain.log /usr/bin/python3 scripts/run-soc07-chain.py C --study v2 --stages s0,p0,s1q,s1r,s1l --host <server> --agent dmarz/orbital-orchestrator`.
6. The ledger at `/srv/swarm/soc07-v2-budget/ledger.jsonl` is created empty at the first paid stage; it is this study's own ledger and is never copied from v1.

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| local-s0-a1 (offline, not a hub run) | S0 / v2 | chain-001-pre | 1,500 scripted episodes, 21,300 scripted calls; 73 of 73 checks | engineering evidence only |

## Closeout

Pending.
