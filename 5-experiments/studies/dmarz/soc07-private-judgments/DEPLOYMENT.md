# Deployment and accounting

Exploratory development study, built and operated by dmarz/soc07-private on dmarz's instruction. Reviewer: dmarz/fleet-monitor; cross-researcher review waived by dmarz ([launch/review-waiver.md](launch/review-waiver.md)). S2 is closed. This file is the deployment record; it is updated after each stage.

## Fleet and source

- Host: sim-dmarz-3, exclusive claim `dmarz-soc07-private` held by dmarz/soc07-private (claimed 2026-10-04 03:29 UTC, currently until 2026-10-04 14:37 UTC, status `planned` while no worker runs). Before the claim the host had no active claim, load 0.00 and no worker process. Older checkouts of other studies on its disk were left untouched.
- Dedicated paths on the host: one checkout, one virtual environment and one budget ledger directory for this study. Addresses, the hub address and credentials are not in this repository.
- Deployed revision: `61de92259f045fdd97255317a5f93dd0010119ad`; runtime fingerprint `afacff913d48c50a8fb5b00efd8775454cfbc62dba841a8f6be919ea7144d9fe` (all `src/*.py`, `design.json`, `execution.json`, `experiment.json`, `requirements.txt`). Review notes and results do not change it.
- Server: Python 3.12.3 on x86_64, 4 logical CPUs, Pillow 11.3.0, standard-library HTTP. 58 unit tests ran at this revision: 57 pass and 1 is skipped (the approval-pinning test, which needs the pre-run assessment committed after this revision).
- Hub experiment: `soc07-private-judgments` ([public page](https://swarm-live.pages.dev/#/x/soc07-private-judgments)). One finite worker per stage, at most 5 requests in flight, no automatic re-execution.
- Launch manifest m1: `claude-haiku-4-5-20251001`, no reasoning allowance, temperature 0.7, output caps 256 / 256 / 64 / 64 and 128 for qualification. Credentials by alias only, passed from encrypted storage over ssh standard input to the worker's environment by the private launcher.

## Attempts

| Attempt | Hub run | Revision | Outcome |
| --- | --- | --- | --- |
| local-s0-001 | none (builder's machine) | working tree before `b4e2cd5` | 69 of 69 checks; outputs not kept in the repository |
| s0-a1 | `soc07-private-judgments/ae76d67b` | `b4e2cd5…` | done; 69 of 69 checks; 1,500 scripted episodes; 0 model calls; 482 s |
| s0-a2 | `soc07-private-judgments/bafeae75` | `61de922…` | done; 69 of 69 checks; 1,500 scripted episodes; 0 model calls; 463 s |
| s1q-a1, s1r-a1, s1l-a1 | not started | | wait for the reviewer's go and `launch/s1-approval.json` |

## Budget

Enforced cap USD 40 for the study (USD 30 public-decision path, USD 10 auxiliary private finals), inside dmarz's USD 500 total. Hard call caps: S1-Q 12, S1-R 672, S1-L 4,080. **Spent so far: USD 0, 0 model calls, 0 tokens.** The persistent ledger file does not exist yet; it is created by the first paid stage.

## Visual delivery

Each run uploads a final 1800 x 1200 frame, a replay GIF over completed blocks and an initial frame; paid stages also refresh a progress image at most every 20 seconds. The public site serves images only. Summaries, analyses, manifests, compressed episode files and journals are team-private hub artifacts and stay on the host.

## Handoff (4 October 2026 UTC): Phase 2 moves to dmarz/orbital-orchestrator on orbital-one

dmarz/soc07-private built Phase 1 on a machine that is being shut down and will not run Phase 2. Everything needed is in the two repositories and on sim-dmarz-3. **No model call has been made. No approval record exists.** Do not start a paid stage before dmarz/fleet-monitor sends an explicit go.

### Where things are

| Thing | Location |
| --- | --- |
| Study code, plan, amendments, reviews | swarm-lab `5-experiments/studies/dmarz/soc07-private-judgments/` |
| Launcher | swarm-labs-agentops `scripts/run-soc07-private.py` (on `main`) |
| Checkout on sim-dmarz-3 | `/srv/swarm/soc07-private-lab`, detached at `61de92259f045fdd97255317a5f93dd0010119ad`; the study is in `5-experiments/studies/dmarz/soc07-private-judgments/` inside it |
| Virtual environment on sim-dmarz-3 | `/srv/swarm/soc07-private-venv` (Python 3.12.3, Pillow 11.3.0) |
| Run outputs on sim-dmarz-3 | `results/<hub run id with __>-attempt-1/` inside the study directory, plus `results/<batch>-worker.log` and `results/worker-pid.json`. Untracked; the two S0 runs are there. |
| Budget ledger on sim-dmarz-3 | `/srv/swarm/soc07-private-budget/ledger.jsonl`. Does not exist yet; the first paid stage creates it. Never delete or copy it: it is the enforced USD 40 cap. |
| Model key | agentops `secrets/discussion-dose.sops.env`, aliases `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID` (the same key tonight's other Haiku studies use) |
| Hub prerequisite | S0 run `soc07-private-judgments/bafeae75`, done, `gate_passed = 1`, fingerprint `afacff91…`. S1-Q is only queued if this run's fingerprint equals the deployed one. |

Nothing exists only on the builder's machine. It held a throwaway Python environment for local tests and two shell helpers for polling; neither is needed.

### What the operator's machine needs

Both repositories; `python3` with PyYAML; `git`, `ssh`, `sops`; the age key, either at `<agentops>/keys.txt` or named by `SOPS_AGE_KEY_FILE`; ssh access to the fleet as user `dmarz` (the launcher builds its ssh configuration from `scripts/agentops.py ssh-config` with `AGENTOPS_ME=dmarz`). No DigitalOcean token is needed: the server exists and is provisioned.

### Claim

`dmarz-soc07-private` on sim-dmarz-3 is exclusive and held in the name `dmarz/soc07-private`. The launcher refuses to act unless the merged claim on agentops `main` is active, exclusive, alone on the host, and its `by` equals the launcher's `--agent` (default `dmarz/soc07-private`). Either keep the claim's `by` and extend it (`python3 scripts/agentops.py release dmarz-soc07-private --status running --until 6h --note "..."`), or release it and claim again as `dmarz/orbital-orchestrator` and pass `--agent dmarz/orbital-orchestrator` to every launcher call. Check `until` before each stage; S1-L needs about an hour.

### Steps, in order (from the agentops repository root)

```sh
# 0. Read-only check. Expect two S0 runs done, worker_active false, approval_present false.
python3 scripts/run-soc07-private.py 61de92259f045fdd97255317a5f93dd0010119ad status

# 1. Only after the reviewer's explicit go. In swarm-lab, from the study directory:
python3 launch/make_approval.py --stages s1q,s1r,s1l --go "<when and where dmarz/fleet-monitor said go>"
#    commit launch/s1-approval.json to swarm-lab main; call that commit <C>.
#    If the reviewer asked for code or configuration changes first: make them, run python3 src/selftest.py,
#    update the hashes in reviews/s1-pre.md, commit, deploy with setup, run `s0 --attempt 3`, and only then write the approval.

# 2. Deploy <C> (checks out the commit, runs the offline tests, about 5 minutes).
python3 scripts/run-soc07-private.py <C> setup          # source_hash must print afacff913d48c50a… unless code changed

# 3. S1-Q: 12 calls, about a minute.
python3 scripts/run-soc07-private.py <C> s1q
python3 scripts/run-soc07-private.py <C> status         # until the run is done or failed and worker_active is false
python3 scripts/run-soc07-private.py <C> verify
#    Stop. Write reviews/s1q-post.md. Report to the reviewer. Continue only if gate_passed = 1.

# 4. S1-R: 672 calls, roughly 30 to 40 minutes. Same status / verify / post-mortem / report.
python3 scripts/run-soc07-private.py <C> s1r

# 5. S1-L: 4,080 calls, roughly an hour. Same again.
python3 scripts/run-soc07-private.py <C> s1l
```

Each paid call of the launcher decrypts the two aliases locally with sops and sends them over ssh standard input; the remote step puts them only into the worker process's environment. They are never written to disk, never passed as arguments and never echoed; the launcher prints only a sanitized error for a paid step. The worker is one detached process under `timeout 15000s`; it takes exactly one queued hub run and exits. If the hub hands the run out again after a silence, the worker refuses (no automatic re-execution).

### Gates and caps (full text in [reviews/s1-pre.md](reviews/s1-pre.md))

- S1-Q passes with at least 10 of 12 correct and at least 11 of 12 valid, no halt and no crash. A competence failure ends manifest m1: no S1-R, no S1-L. The next step is then a dated amendment to `launch_manifest` in `execution.json` (model, reasoning allowance, `qualification_set` 1) plus a budget entry `"s1q.1": {"max_calls": 12, "public": 12, "aux": 0, "retry_allowance": 6}`, then S0 again, a new approval and a fresh S1-Q. No code change is needed for that.
- S1-R passes with at least 95% valid outputs, under 5% budget, timeout or overflow failures, at most 5% truncation in any phase, zero leaks, no duplicate or unplanned call, no halt or crash, and the focal agent correct in at least 13 of 16 clean-regime episodes in both PRIVATE and PUBLIC.
- The launcher refuses a stage whose prerequisite run is not `done` with `gate_passed = 1` at the same fingerprint, and refuses a batch id that already exists. A rerun is `--attempt 2` with its own pre-run note; S1-Q cannot be rerun under the same qualification set because its 12-call cap is then spent.
- Caps enforced by the ledger: USD 40 total (USD 30 public-decision path, USD 10 auxiliary private finals); calls 12, 672 and 4,080; transport attempts 18, 706 and 4,284. Expected spend about USD 7.
- After the last stage: analysis from `analysis.json` and the episode files, post-run review with actual tokens, calls and dollars, figures into `artifacts/` only through `.flightdeck/fd.py add`, results on `main`, then `python3 scripts/agentops.py release dmarz-soc07-private --note "..."`.

### Known gaps the next operator inherits

- The real provider exchange has never run. If the first S1-Q request is rejected (HTTP 400 and similar), the stage halts after one call; treat it as an execution failure and requalify on a new qualification set as above.
- The swarm-lab task `build-soc07-private-judgments` was released by dmarz/soc07-private for the next operator to claim.

## Closeout

Open. The claim is released only after the last authorized stage has finished or been stopped, artifacts are verified and the worker has exited.
