# Experiment setup record: discussion-dose-v3 / D2 (v3-d2-a1)

Status, 2026-10-04 08:40 UTC: **complete.** The 72-call run finished with 72 valid answers at the pinned commit
`aef218e8`; [results](RESULTS.md) and the [post-run review](../../reviews/v3-d2-a1-post.md) are published and the
claim is released. No successor is authorized or started. Follows the
[shared setup runbook](../../../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md) and the
[run review cycle](../../../../../toolkit/agent-experiments/RUN-REVIEW.md).

## Ownership and question

- Owner: dmarz. Builder and operator: `dmarz/v3-d2-opus` (Claude Code, a sub-agent of the fleet-monitor session).
  Reviewer: `dmarz/fleet-monitor`. Review independence: none. This is a same-researcher check under dmarz's review
  waiver for these runs; it is recorded as waived by owner direction, not as passed or independent.
- The D2 design was written by `dmarz/discussion-bench-v3` as [D2-PLAN](../D2-PLAN.md) and left unstarted. This
  agent took it over on dmarz's instruction as relayed by `dmarz/fleet-monitor`; the note is in
  `researchers/dmarz/inbox.md`.
- Question, decision and claim boundary: [PLAN](PLAN.md). Model under test: Claude Opus 5.5. Comparison arms:
  Sonnet 4.6 and Haiku 4.5.
- Research status: exploratory diagnostic instrument under [SEC-47](../../QUESTION-LINKS.md). No hypothesis
  promotion, fresh qualification, S1 or confirmation is authorized or implied.
- Related completed run: [D1-Opus](../../d1-opus/RESULTS.md) (`d1o-a1`, by `dmarz/d1-opus`): Opus 5.5 6/6 on these
  worlds and 12/12 on a fresh gate, on D1's packaging at effort `high`. D2 is therefore not on the path to
  qualifying Opus; it explains the Haiku and Sonnet failures and checks Opus on the compact format.
- Previous attempt and lessons: [D1 results](../RESULTS-D1.md), [D1 post-mortem](../../reviews/v3-d1-a1-post.md).
  Lessons used: both D1 models failed after correct extraction, so D2 removes extraction; never resubmit an
  ambiguous call; the launch-policy miss at D1 closeout is why the launch route is stated as a deviation here.
- Launch route, corrected after the go: `dmarz/fleet-monitor` states that Dan told the fleet monitor directly to
  pick two stopped experiments and run them on halcyon as managed sub-agents, which overrides the run-queue default.
  The pinned plan described that instruction as relayed and unconfirmed by this agent.
- Current stage: closed (G5).

## Gate evidence

| Gate | Status | Evidence, time and assessor | Blocker or next action |
|---|---|---|---|
| G0 Question and research gates | pass for diagnosis | Existing SEC-47 link and D1 post-mortem issue D1-C1; no formal hypothesis claimed. `dmarz/v3-d2-opus`, 2026-10-04 | Stay in bounded development scope |
| G1 Plan before implementation | pass | D2-PLAN first committed as `fb82a38f` (2026-10-04T04:59Z); the first D2 code is `df70c7e9` (2026-10-04T07:48Z). The amendment [PLAN](PLAN.md) was written after the code and before any model call, and fixes no detail after seeing a model output | None |
| G2 Instrument and offline checks | pass for offline software | 29 D2 tests, 15 D1 tests and 57 v3 tests pass on the server under Python 3.12.3 at the pinned commit; 29 D2 tests also pass locally under Python 3.9.6. All 48 canonical values match the retained clean Q0 records on both machines. Same-author checks. | Rehearsal on the server |
| G3 Attempt admission | pass | [Pre-run assessment](../../reviews/v3-d2-a1-pre.md); claim `dmarz-discussion-v3-d2` on `sim-dmarz-3`; [rehearsal receipt](launches/v3-d2-a1-rehearsal.json); go from `dmarz/fleet-monitor` (same-researcher check, not independent) recorded 2026-10-04T08:25Z; preflight passed; one-call Opus probe returned a parsed answer | None |
| G4 Qualification before escalation | not applicable | D2 is itself the diagnostic for a failed qualification; it qualifies nothing | None |
| G5 Reconciliation and closeout | pass | 72 assigned, started, terminal, valid; audit recomputed 72 of 72; hub artifacts read back; USD 0.127741 including the probe; [results](RESULTS.md), [post-run review](../../reviews/v3-d2-a1-post.md); claim released. `dmarz/v3-d2-opus`, 2026-10-04 | None |

## Design and instrument index

- Plan and amendment: [PLAN](PLAN.md) over the unchanged [D2-PLAN](../D2-PLAN.md).
- Fact table: [canonical-facts.json](canonical-facts.json), 48 values, no labels.
- Instrument: [diagnostic_v3_d2.py](../../src/diagnostic_v3_d2.py). Commands `table`, `prepare`, `rehearse`,
  `preflight`, `probe`, `run`, `audit`. It reuses `bench_v3` (journal, failure allowlist, evidence resolver,
  reference scorer, world generator, artifact publisher) and the `providers.Anthropic` boundary without editing them.
- Tests: [diagnostic_v3_d2_selftest.py](../../src/diagnostic_v3_d2_selftest.py); run from `src/` with
  `python3 -m unittest diagnostic_v3_d2_selftest`.
- Independent units: six world clusters. Per model 24 dependent calls; three models on identical inputs. Not 72
  independent samples.
- Split: only open development worlds 20001 to 20006. Q1 IDs 50001 to 50006, confirmation IDs 30000 to 30023 and
  sidecar IDs 40001 to 40012 are not generated or read. The probe request is hand-written and uses no world id.
- Models, settings and prices: the table in [PLAN](PLAN.md); also frozen in the manifest as `model_settings`.
- Leakage check: `reject_gold` refuses evaluator and prior-output fields in every actor input; the selftest checks
  every request's exact key set.
- Launcher: private agentops `scripts/run-discussion-v3-d2.py`. It checks the merged exclusive claim before every
  step. The paid steps are `preflight`, `probe`, `launch`; `run` in the instrument refuses without a preflight
  receipt under 30 minutes old and a passing probe receipt for the same manifest, and requires a hub run already
  started and bound to the manifest hash. There is no other entry point that sends a model request.
- Visualization mapping: `d2-call-ledger-v1` in [PLAN](PLAN.md).

## Current attempt admission

Operations entry: manual, through the private launcher. Private paths, addresses and receipts stay out of this
repository.

| Operation | Command (private launcher, run from the agentops checkout) | Evidence |
|---|---|---|
| Stage source and inputs, run tests | `run-discussion-v3-d2.py <commit> setup --q0-archive <retained archive>` | 29 / 15 / 57 tests pass on the server at the pinned commit |
| Freeze | `... <commit> prepare` | Manifest hash recorded in `launches/` after this commit |
| Zero-cost admission checks | `... <commit> admission-dry` | Same |
| Rehearse | `... <commit> rehearse`, then `status`, `duplicate`, `verify --batch v3-d2-a1-rehearsal` | Same |
| Paid, after the go | `... <commit> preflight --go-utc <time>`, `probe`, `launch` | Run once, 08:25 to 08:28 UTC |
| Verify and close | `... <commit> verify --batch v3-d2-a1`, `close` | Done; [accounting](results/v3-d2-a1/accounting.json) |
| Resume interrupted execution | Unsupported by design: audit with `--allow-interrupted`, never restart | |
| Stop | Create `v3-d2-a1.stop` in the ledger directory; stops the next dispatch only | |

- Attempt `v3-d2-a1`, parent `v3-d1-a1`, stage D2, status `diagnostic-only`.
- Immutable public plan: the URL and hash of [PLAN](PLAN.md) at the pinned commit are written into the frozen
  manifest and verified against the public bytes and page before dispatch.
- Budget authority: USD 5 cap for this run, given by the reviewer inside dmarz's standing USD 500 pool. Reservation
  USD 3.387356 including the probe. Calls: 72 assigned plus one probe; 24 per model adapter; one worker; one hour.
- Allocation: existing server `sim-dmarz-3`, exclusive claim `dmarz-discussion-v3-d2`, held by `dmarz/v3-d2-opus`
  until 2026-10-04T15:33Z. Checked idle before claiming: no active claim in git or on the hub, no worker process,
  no active run. No provisioning; this agent creates and destroys no server.
- Credentials: alias `secrets/discussion-dose.sops.env` in the private repository. The value goes over ssh standard
  input into process memory and is inherited by the service by variable name. It is not written to disk or passed
  as an argument.
- Go or no-go: go, from `dmarz/fleet-monitor` on dmarz's behalf, recorded 2026-10-04T08:25:14Z by the operator
  clock (the go message states 08:28 UTC). Effort `high`, the comparison arms and the 4,000-token ceiling were
  confirmed in the same message.

## Attempt and repair history

| Attempt / parent | Stage | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Disposition |
|---|---|---|---|---|
| v3-d2-a1 / v3-d1-a1 | D2 | [pre](../../reviews/v3-d2-a1-pre.md), [rehearsal](launches/v3-d2-a1-rehearsal.json), [accounting](results/v3-d2-a1/accounting.json) | 72 / 72 / 72 / 72 / 72 | [Post-mortem](../../reviews/v3-d2-a1-post.md): complete valid result. Opus 6/6 and 18/18; Sonnet and Haiku 5/6 and 16/18 |

## Closeout

- Execution passed; response validity 72/72; qualification not applicable; scientific conclusion exploratory;
  reporting complete.
- All 72 outcomes retained and audited; per-item table and summary in `results/v3-d2-a1/`.
- Actual cost USD 0.127741 (batch 0.125037, probe 0.002704) against a reservation of USD 3.387356 and a cap of
  USD 5; list-price calculation from reported usage, not invoice-reconciled.
- No missing outcomes or exclusions. Deviations are listed in the post-run review.
- Artifacts read back from the hub and matched. Worker and watchdog stopped. Claim released.
- Next action: none started. Any follow-up on the Haiku and Sonnet sum-predicate errors needs dmarz's decision and
  its own plan.
