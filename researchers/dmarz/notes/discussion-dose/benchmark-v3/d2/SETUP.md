# Experiment setup record: discussion-dose-v3 / D2 (v3-d2-a1)

Status at this commit: instrument built and tested offline and on the server; plan and pre-run assessment written;
**no model call made**. The zero-model rehearsal runs at this commit and its receipt is added afterwards in
`launches/`. The paid run waits for the reviewer's explicit go. Follows the
[shared setup runbook](../../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and the
[run review cycle](../../../../../../tooling/agent-experiments/RUN-REVIEW.md).

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
- Previous attempt and lessons: [D1 results](../RESULTS-D1.md), [D1 post-mortem](../../reviews/v3-d1-a1-post.md).
  Lessons used: both D1 models failed after correct extraction, so D2 removes extraction; never resubmit an
  ambiguous call; the launch-policy miss at D1 closeout is why the launch route is stated as a deviation here.
- Current stage: G3 admission pending the rehearsal receipt and the reviewer's go.

## Gate evidence

| Gate | Status | Evidence, time and assessor | Blocker or next action |
|---|---|---|---|
| G0 Question and research gates | pass for diagnosis | Existing SEC-47 link and D1 post-mortem issue D1-C1; no formal hypothesis claimed. `dmarz/v3-d2-opus`, 2026-10-04 | Stay in bounded development scope |
| G1 Plan before implementation | pass | D2-PLAN first committed as `fb82a38f` (2026-10-04T04:59Z); the first D2 code is `df70c7e9` (2026-10-04T07:48Z). The amendment [PLAN](PLAN.md) was written after the code and before any model call, and fixes no detail after seeing a model output | None |
| G2 Instrument and offline checks | pass for offline software | 29 D2 tests, 15 D1 tests and 57 v3 tests pass on the server under Python 3.12.3 at source commit `9d119dfd`; 29 D2 tests also pass locally under Python 3.9.6. All 48 canonical values match the retained clean Q0 records on both machines. Same-author checks. | Rehearsal on the server |
| G3 Attempt admission | pending | [Pre-run assessment](../../reviews/v3-d2-a1-pre.md); claim `dmarz-discussion-v3-d2` on `sim-dmarz-3` merged 2026-10-04T07:33Z | Rehearsal receipt, then reviewer go, then preflight and probe |
| G4 Qualification before escalation | not applicable | D2 is itself the diagnostic for a failed qualification; it qualifies nothing | None |
| G5 Reconciliation and closeout | pending | | After the run |

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
| Stage source and inputs, run tests | `run-discussion-v3-d2.py <commit> setup --q0-archive <retained archive>` | 29 / 15 / 57 tests pass on the server at `9d119dfd` |
| Freeze | `... <commit> prepare` | Manifest hash recorded in `launches/` after this commit |
| Zero-cost admission checks | `... <commit> admission-dry` | Same |
| Rehearse | `... <commit> rehearse`, then `status`, `duplicate`, `verify --batch v3-d2-a1-rehearsal` | Same |
| Paid, after the go | `... <commit> preflight --go-utc <time>`, `probe`, `launch` | Not run |
| Verify and close | `... <commit> verify --batch v3-d2-a1`, `close` | Not run |
| Resume interrupted execution | Unsupported by design: audit with `--allow-interrupted`, never restart | |
| Stop | Create `v3-d2-a1.stop` in the ledger directory; stops the next dispatch only | |

- Attempt `v3-d2-a1`, parent `v3-d1-a1`, stage D2, status `diagnostic-only`.
- Immutable public plan: the URL and hash of [PLAN](PLAN.md) at the pinned commit are written into the frozen
  manifest and verified against the public bytes and page before dispatch.
- Budget authority: USD 5 cap for this run, given by the reviewer inside dmarz's standing USD 500 pool. Reservation
  USD 3.387556 including the probe. Calls: 72 assigned plus one probe; 24 per model adapter; one worker; one hour.
- Allocation: existing server `sim-dmarz-3`, exclusive claim `dmarz-discussion-v3-d2`, held by `dmarz/v3-d2-opus`
  until 2026-10-04T15:33Z. Checked idle before claiming: no active claim in git or on the hub, no worker process,
  no active run. No provisioning; this agent creates and destroys no server.
- Credentials: alias `secrets/discussion-dose.sops.env` in the private repository. The value goes over ssh standard
  input into process memory and is inherited by the service by variable name. It is not written to disk or passed
  as an argument.
- Go or no-go: pending. Decision-maker: `dmarz/fleet-monitor` on dmarz's behalf.

## Attempt and repair history

| Attempt / parent | Stage | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Disposition |
|---|---|---|---|---|
| v3-d2-a1 / v3-d1-a1 | D2 | [pre](../../reviews/v3-d2-a1-pre.md) | 72 / 0 / 0 / 0 / 0 | Not started |

## Closeout

Pending. Results go to `results/v3-d2-a1/` beside this file and the post-run review to
`reviews/v3-d2-a1-post.md`. The claim is released after artifact readback.
