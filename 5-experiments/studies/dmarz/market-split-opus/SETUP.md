# Experiment setup record: market-split-opus v1

Status: complete, 2026-10-04. This record is not launch authorization for a paid stage. It follows [the setup runbook](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md) and [the operations guide](../../../toolkit/agent-experiments/OPERATIONS.md). Written before implementation was run on the server and updated as gates produce evidence.

## Ownership and question

- Owner and operator: dmarz/market-split-opus (Claude Code session on halcyon). Design reviewer: dmarz/fleet-monitor, the session that launched this one. Both act for dmarz, so this is a same-researcher check. dmarz waived cross-researcher review for runs like this on 2026-10-04; the waiver is recorded as "not required by owner direction", never as a passed or independent review.
- Question: does the Sonnet pilot's firm-splitting result replicate with Claude Opus 5.5 on six fresh markets? Primary contrast: flexible-arm sustained evasion under firm-based minus owner-based regulation, paired by task. Claim boundary: one model configuration, six related markets, one owner against scripted rivals.
- Research status: exploratory replication of an exploratory pilot. No accepted hypothesis; the formal prior-art and hypothesis gates are incomplete, as in the parent study. S2 and holdout 1000-1999 are closed.
- Authority: dmarz's instruction relayed by the reviewer ("I would like to start testing with a strong model like opus"; later "use opus for everything going forward please"), the shared USD 500 allowance in `lab/researchers/dmarz/README.md`, and the reviewer's caps for this study (950 calls, USD 60).
- Previous work read: [Sonnet results](../market-split-api/RESULTS.md) and [post-mortem](../market-split-api/reviews/s1-002-post.md), [Haiku results](../market-split-haiku/RESULTS.md), the Haiku V2 truncation post-mortem and R0 post-mortem. Lessons taken: record stop reasons, give thinking room under the output ceiling, pin the public plan to a commit, gate on unpriced calls, one worker per server.
- Current stage and next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, time (UTC) and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and research gates | pass for exploratory scope only | Question and prediction in [README](README.md); formal survey and hypothesis gates not passed and not claimed. 2026-10-04, dmarz/market-split-opus | None for exploratory stages; S2 stays closed |
| G1 Plan before implementation | pass | [README](README.md), [preregistration.md](preregistration.md), `design.yaml` committed before any run on the server | None |
| G2 Instrument and offline checks | pass | 18/18 offline tests on `sim-test-01` in the pinned runtime and 18/18 locally, 2026-10-04 07:47, dmarz/market-split-opus. Real provider path not exercised | First real check is I0 |
| G3 Admission, s0-fleet-001 | pass | [s0-fleet-001-pre](reviews/s0-fleet-001-pre.md); claim merged 07:46; public plan at `8c27b690` checked by the launcher (bytes equal, sections present) before `run_start` | None |
| G3 and G5, s0-fleet-002 | pass | [pre](reviews/s0-fleet-002-pre.md), [post](reviews/s0-fleet-002-post.md): 6/6, identical to s0-fleet-001, 0 calls | None |
| G3 Admission, i0-001 / q0-001 / s1-001 | pass, subject to each software gate | [phase2-pre](reviews/phase2-pre.md), per-attempt files, and the reviewer's go in [phase2-go](reviews/phase2-go.md) (same-researcher check, not independent review). Issue O3 resolved there | Chain I0, Q0, S1 |
| G4 Qualification | pass | [i0-001-post](reviews/i0-001-post.md) 6/6; [q0-001-post](reviews/q0-001-post.md) 4/4 at 100% of the reference, floor 75%; hashes match the S1 source. 2026-10-04 08:05, dmarz/market-split-opus | S1 running |
| G5 Reconciliation, s0-fleet-001 | pass | [s0-fleet-001-post](reviews/s0-fleet-001-post.md): 6 assigned, 6 done, 12 valid episodes, 42 artifacts hash-verified, 0 calls | None |
| G5 Closeout of the study | pass | [s1-001-post](reviews/s1-001-post.md), [RESULTS](RESULTS.md); 126 artifacts read back, exact replay 864/864, ledger 902 priced calls / USD 15.344524; workers stopped; claim released (deployment.md). 2026-10-04, dmarz/market-split-opus | None; nothing further authorized |

## Design and instrument index

- Plan: [README](README.md); frozen protocol: [preregistration.md](preregistration.md); design: `design.yaml`; issue ledger: [ISSUES.md](ISSUES.md).
- Independent unit: the market task. S1 has six tasks, each with three regulators and two arms: 18 bundles, 36 episodes, 864 calls. Calls, rounds and episodes inside a task are dependent. Six tasks is a pilot; no power claim.
- Splits: S0 and Q0 tasks 100/101; I0 probes 102-107; S1 110-115; holdout 1000-1999 closed. Offline test fixtures reuse task 20 with scripted transport only.
- Agent definition: system prompt `src/prompt.txt` (byte-identical to the pilot's); user message is the JSON observation from `sim.make_observation`; response schema `provider.SCHEMA`; no tools, memory or cross-call state.
- Versions: model `claude-opus-5-5`; Python 3.12.3, PyYAML 6.0.3, numpy 2.0.2, matplotlib 3.9.4, Pillow 11.3.0; engine and design hashes in each pre-run review.
- Offline checks: `src/selftest.py`, network blocked, 18 tests.
- Launcher gates: `scripts/run-market-split-opus.py` (agentops) checks the merged exclusive claim, the public plan bytes at the pinned commit, the checked-out revision, no other worker on the host, no stop marker and no reused attempt; paid stages need `--confirm-paid`. `coordinator.py` checks the committed `Status: ready` review, the duplicate attempt and the parent-stage gate. `worker.py` and `probe.py` can be started by hand on the server and would then skip the launcher's claim and plan checks; they still apply the coordinator gate, the frozen-source check and the ledger caps.
- Visualization mapping: `market-split-opus-v1`, described in the README.

## Current attempt admission

| Operation | Command | Evidence |
|---|---|---|
| Offline validation | `python3 src/selftest.py` | 18 tests |
| Deploy pinned source | `run-market-split-opus.py <commit> setup` | deployment.md |
| Scripted rehearsal | `run-market-split-opus.py <commit> S0` | s0-fleet-001 reviews |
| Paid stages | `run-market-split-opus.py <commit> I0\|Q0\|S1\|S1-continue --confirm-paid` | not admitted |
| Status and artifact check | `run-market-split-opus.py <commit> status\|verify` | post-mortems |
| Stop | `swarm-report pause -e market-split-opus`, or create `results/<attempt>-STOP` on the server | none yet |

- Credentials: aliases `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID` from the encrypted agentops store, passed over ssh stdin into the worker's environment only.
- Budget: 950 attempted calls and USD 160 for the study (raised from USD 60 by the reviewer before any model call), enforced by the ledger; one worker; no retries.

## Attempt and repair history

| Attempt / parent | Stage | Pre-review | Assigned / started / terminal | Post-mortem |
|---|---|---|---|---|
| s0-fleet-001 / none | S0 scripted | [pre](reviews/s0-fleet-001-pre.md) | 6 / 6 / 6 done; 12 episodes valid | [post](reviews/s0-fleet-001-post.md): advance to paid-stage review |
| s0-fleet-002 / s0-fleet-001 | S0 scripted, amended design | [pre](reviews/s0-fleet-002-pre.md) | 6 / 6 / 6 done | [post](reviews/s0-fleet-002-post.md): advance |
| i0-001 / s0-fleet-002 | I0 | [pre](reviews/i0-001-pre.md), [phase2-pre](reviews/phase2-pre.md) | 6 / 6 / 6 valid | [post](reviews/i0-001-post.md): advance |
| q0-001 / i0-001 | Q0 | [pre](reviews/q0-001-pre.md) | 2 bundles, 4 episodes, 32 calls, all valid | [post](reviews/q0-001-post.md): advance |
| s1-001 / q0-001 | S1 | [pre](reviews/s1-001-pre.md) | 18 / 18 / 18 done; 36 graded, 36 analyzed | [post](reviews/s1-001-post.md): complete-valid-result |

## Closeout

Execution complete; response validity 36/36; qualification passed; scientific conclusion: the pilot's result replicates with this configuration on six fresh markets (exploratory); process: plan and pre-run review on `main` before any model call, same-researcher review only; reporting: results, post-run review, figure and records filed. Actual cost USD 15.344524 over 902 priced calls; no outstanding reservation. Nothing missing or excluded. Workers stopped; claim released after uploads were verified. `sim-test-01` is an existing shared test server and is not destroyed by this study; its study directory, including the private ledger, is left in place. Next action: none without a new instruction.
